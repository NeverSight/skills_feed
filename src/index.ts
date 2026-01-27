/**
 * Skills.sh Crawler Script
 * Fetches skill data from skills.sh and outputs as JSON format
 */

import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'fs';
import { join } from 'path';
import { Feed } from 'feed';

// Type definitions
interface Skill {
  source: string;
  skillId: string;
  name: string;
  installs: number;
}

interface HotSkill extends Skill {
  installsYesterday?: number;
  change?: number;
}

interface SkillsData {
  updatedAt: string;
  allTime: Skill[];
  trending: Skill[];
  hot: HotSkill[];
}

interface FeedItem {
  id: string;
  title: string;
  source: string;
  installs: number;
  link: string;
}

interface FeedJson {
  title: string;
  description: string;
  link: string;
  updatedAt: string;
  topAllTime: FeedItem[];
  topTrending: FeedItem[];
  topHot: FeedItem[];
}

// Request headers configuration
const headers: HeadersInit = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'rsc': '1',
  'next-url': '/',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
};

/**
 * Extract skills array from text for a specified field
 */
function extractSkillsArray(text: string, fieldName: string): Skill[] {
  const skills: Skill[] = [];
  
  // Find field start position
  const fieldPattern = `"${fieldName}":[`;
  const startIndex = text.indexOf(fieldPattern);
  
  if (startIndex === -1) {
    console.log(`Field not found: ${fieldName}`);
    return skills;
  }
  
  // Find array start position
  const arrayStart = startIndex + fieldPattern.length - 1;
  
  // Use bracket matching to find array end position
  let depth = 0;
  let arrayEnd = arrayStart;
  
  for (let i = arrayStart; i < text.length; i++) {
    if (text[i] === '[') {
      depth++;
    } else if (text[i] === ']') {
      depth--;
      if (depth === 0) {
        arrayEnd = i + 1;
        break;
      }
    }
  }
  
  try {
    const arrayStr = text.slice(arrayStart, arrayEnd);
    const parsed = JSON.parse(arrayStr);
    if (Array.isArray(parsed)) {
      return parsed;
    }
  } catch (e) {
    console.error(`Failed to parse ${fieldName}:`, e);
  }
  
  return skills;
}

/**
 * Fetch data from specified endpoint
 */
async function fetchEndpoint(endpoint: string): Promise<string> {
  const url = `https://skills.sh${endpoint}?_rsc=${Date.now()}`;
  console.log(`Fetching: ${url}`);
  
  try {
    const response = await fetch(url, {
      headers: {
        ...headers,
        'referer': 'https://skills.sh/',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.text();
  } catch (error) {
    console.error(`Failed to fetch ${endpoint}:`, error);
    return '';
  }
}

function readJsonFile<T>(path: string): T | null {
  try {
    const raw = readFileSync(path, 'utf-8');
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

type LeaderboardKey = 'topAllTime' | 'topTrending' | 'topHot';

function buildRssItemsFromDiff(previous: FeedJson | null, next: FeedJson) {
  const updatedAt = new Date(next.updatedAt);

  const boards: Array<{ key: LeaderboardKey; label: string }> = [
    { key: 'topAllTime', label: 'All Time' },
    { key: 'topTrending', label: 'Trending' },
    { key: 'topHot', label: 'Hot' },
  ];

  const items: Array<{
    title: string;
    id: string;
    link: string;
    date: Date;
    description: string;
  }> = [];

  for (const board of boards) {
    const nextList = next[board.key] ?? [];
    const prevList = previous?.[board.key] ?? [];

    const prevRankById = new Map<string, { rank: number; installs: number }>();
    prevList.forEach((it, idx) => prevRankById.set(it.id, { rank: idx + 1, installs: it.installs }));

    nextList.forEach((it, idx) => {
      const rank = idx + 1;
      const prev = prevRankById.get(it.id);

      // Use skills.sh collection page; fall back to GitHub repo URL.
      const githubRepoUrl = `https://github.com/${it.source}`;
      const link = it.link || githubRepoUrl;

      if (!prev) {
        items.push({
          title: `[${board.label}] New entry (#${rank}): ${it.title}`,
          id: `${next.updatedAt}:${board.key}:new:${it.id}`,
          link,
          date: updatedAt,
          description: [
            `New entry in ${board.label} leaderboard.`,
            `Rank: #${rank}`,
            `Installs: ${it.installs}`,
            `Source: ${it.source}`,
          ].join('\n'),
        });
        return;
      }

      if (prev.rank !== rank) {
        const delta = prev.rank - rank; // positive = up
        const absDelta = Math.abs(delta);

        // Reduce noise: only publish meaningful changes.
        const shouldPublish =
          absDelta >= 10 ||
          (rank <= 20 && absDelta >= 3) ||
          (rank <= 10 && absDelta >= 1);

        if (!shouldPublish) return;

        const direction = delta > 0 ? 'up' : 'down';
        items.push({
          title: `[${board.label}] Rank ${direction} (${prev.rank} → ${rank}): ${it.title}`,
          id: `${next.updatedAt}:${board.key}:rank:${it.id}`,
          link,
          date: updatedAt,
          description: [
            `${board.label} leaderboard rank change.`,
            `Previous rank: #${prev.rank}`,
            `Current rank: #${rank}`,
            `Delta: ${delta > 0 ? '+' : ''}${delta}`,
            `Installs: ${it.installs} (prev ${prev.installs})`,
            `Source: ${it.source}`,
          ].join('\n'),
        });
      }
    });
  }

  // New entries first, then rank changes; cap to avoid huge feeds.
  const sorted = items.sort((a, b) => {
    const aIsNew = a.id.includes(':new:') ? 0 : 1;
    const bIsNew = b.id.includes(':new:') ? 0 : 1;
    if (aIsNew !== bIsNew) return aIsNew - bIsNew;
    return a.title.localeCompare(b.title);
  });

  return sorted.slice(0, 50);
}

/**
 * Main function
 */
async function main() {
  console.log('Starting skills.sh data crawl...\n');
  
  // Fetch all three endpoints
  const [homeText, trendingText, hotText] = await Promise.all([
    fetchEndpoint('/'),
    fetchEndpoint('/trending'),
    fetchEndpoint('/hot'),
  ]);
  
  // Extract allTimeSkills from home page
  const allTime = extractSkillsArray(homeText, 'allTimeSkills');
  
  // Extract trendingSkills from trending page
  const trending = extractSkillsArray(trendingText, 'trendingSkills');
  
  // Extract trulyTrendingSkills from hot page (this is the actual field name for hot)
  const hot = extractSkillsArray(hotText, 'trulyTrendingSkills') as HotSkill[];
  
  console.log(`\nCrawl completed:`);
  console.log(`- All Time: ${allTime.length} skills`);
  console.log(`- Trending: ${trending.length} skills`);
  console.log(`- Hot: ${hot.length} skills`);
  
  // Show top 3 comparison
  console.log('\n=== Top 3 Comparison ===');
  console.log('All Time:', allTime.slice(0, 3).map(s => `${s.name}(${s.installs})`).join(', '));
  console.log('Trending:', trending.slice(0, 3).map(s => `${s.name}(${s.installs})`).join(', '));
  console.log('Hot:', hot.slice(0, 3).map(s => `${s.name}(${s.installs})`).join(', '));
  
  // Build output data
  const data: SkillsData = {
    updatedAt: new Date().toISOString(),
    allTime,
    trending,
    hot,
  };
  
  // Ensure output directory exists
  const outputDir = join(process.cwd(), 'data');
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }
  
  // Write JSON file
  const outputPath = join(outputDir, 'skills.json');
  writeFileSync(outputPath, JSON.stringify(data, null, 2));
  console.log(`\nData saved to: ${outputPath}`);
  
  // Generate simplified feed format
  const feedPath = join(outputDir, 'feed.json');
  const previousFeed = readJsonFile<FeedJson>(feedPath);
  const feed: FeedJson = {
    title: 'Skills.sh Feed',
    description: 'Latest skill data from skills.sh',
    link: 'https://skills.sh',
    updatedAt: data.updatedAt,
    topAllTime: allTime.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: `https://skills.sh/i/${skill.source}`,
    })),
    topTrending: trending.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: `https://skills.sh/i/${skill.source}`,
    })),
    topHot: hot.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: `https://skills.sh/i/${skill.source}`,
    })),
  };
  writeFileSync(feedPath, JSON.stringify(feed, null, 2));
  console.log(`Feed saved to: ${feedPath}`);

  // Generate RSS feed (XML) based on changes vs previous feed.json
  const rssItems = buildRssItemsFromDiff(previousFeed, feed);

  const rss = new Feed({
    title: feed.title,
    description: feed.description,
    id: feed.link,
    link: feed.link,
    language: 'en',
    updated: new Date(feed.updatedAt),
  });

  for (const item of rssItems) {
    rss.addItem({
      title: item.title,
      id: item.id,
      link: item.link,
      date: item.date,
      description: item.description,
    });
  }

  const rssPath = join(outputDir, 'feed.xml');
  writeFileSync(rssPath, rss.rss2());
  console.log(`RSS saved to: ${rssPath}`);
}

main().catch(console.error);

---
name: gh-profile
description: Expert GitHub profile customization assistant that helps create stunning, professional GitHub profile READMEs. Use this skill when users want to customize their GitHub profile, create profile READMEs, add stats cards, animations, badges, or automate profile updates with GitHub Actions. Covers 2025 trends including minimalist designs, themed profiles, dynamic content, animations, visitor tracking, AI-powered generation, and GitHub achievements.
license: MIT
---

This skill transforms GitHub profiles from basic to extraordinary. Your GitHub profile is your digital resume, portfolio, and personal brand—make it unforgettable.

# What Users Want

Users typically want help with GitHub profile customization when they:
- Want to stand out to recruiters and collaborators
- Need to showcase their skills, projects, and achievements
- Want to add dynamic stats cards, streaks, and visualizations
- Are looking for automation with GitHub Actions
- Need inspiration from templates and examples
- Want to add animations, badges, or interactive elements
- Seek to integrate external services (blogs, LeetCode, Spotify, etc.)

# What You Provide

You provide comprehensive GitHub profile customization guidance, including:
- Complete profile README creation from scratch
- Theme selection and customization (dracula, radical, tokyonight, synthwave, gruvbox, etc.)
- Stats cards and metrics (GitHub Stats, Streak Stats, Top Languages, Trophies, GitHub Trends)
- Animations (typing SVG, snake contribution graph, animated GIFs)
- Visitor counters and badges
- GitHub Actions automation for dynamic content
- External service integration (blog feeds, LeetCode, WakaTime, Spotify)
- GitHub Achievements system and earning strategies
- AI-powered profile generation assistance
- Advanced automation with Python scripts and GraphQL
- Best practices for performance, security, and accessibility
- Recruitment optimization strategies
- Troubleshooting and optimization

# Understanding GitHub Profiles

## What is a GitHub Profile?

A GitHub profile is a special README.md file that appears on your GitHub profile page at `github.com/username`. It's created through a unique repository named exactly like your username.

### Why Create a Profile?

Your GitHub profile is your:
- **Digital resume** for recruiters and hiring managers
- **Portfolio** of your work and projects
- **Personal brand** showcase
- **First impression** for collaborators and employers
- **Professional presence** in the developer community

### How It Works

1. Create a repository named `YOUR_USERNAME` (must match exactly)
2. Add a `README.md` file with markdown content
3. The README automatically appears at `github.com/YOUR_USERNAME`
4. Anyone visiting your profile page sees your customized content

### Important Notes
- The repository **must be public** for your profile to be visible
- The repository name **must match your username exactly** (case-sensitive)
- The `README.md` file **must be in the root directory**
- You can have only one profile per GitHub account

# 2025 Trends & Best Practices

## Current Design Trends
- **Minimalist Professional**: Clean, focused, strategic use of whitespace
- **Themed Profiles**: Tokyo Night, Dracula, Gruvbox, Synthwave (80s retro), One Dark
- **Dynamic & Real-Time**: Automated content via GitHub Actions
- **Storytelling Profiles**: Career timelines, journey mapping
- **Performance-Optimized**: Lightweight SVGs, efficient loading
- **AI-Powered Generation**: Smart template recommendations based on your activity
- **Recruitment-Focused**: Optimized layouts for ATS systems and recruiters

## What Works in 2025
✅ Clean, branded profiles with consistent styling
✅ Strategic widget placement (stats, streak, languages)
✅ High contrast themes for accessibility
✅ Tech stack badges and social links
✅ Animated typing SVG and contribution snakes
✅ Visitor counters with geographic tracking
✅ Dynamic blog feeds via GitHub Actions
✅ Project showcases with repo cards
✅ GitHub Achievements displayed prominently
✅ Impact metrics ("Used by 10k+ users", "500+ stars")

❌ Overcrowded profiles with too many widgets
❌ Broken or slow-loading images
❌ Generic templates without customization
❌ Low contrast color schemes
❌ Excessive GIFs that hurt performance
❌ Missing or outdated contact information

# How to Help Users

## Initial Assessment

When a user requests help, first understand their needs:

1. **Profile Status**: Do they have a profile README already? What's their GitHub username?
2. **Goals**: Job hunting? Personal branding? Showcasing projects? Community building?
3. **Style Preference**: Minimalist, creative, themed, professional, animated?
4. **Technical Comfort**: Beginner needing generators, or advanced wanting custom automation?
5. **Key Features**: Stats cards? Visitor counter? Blog automation? Animations?

### Quick Diagnostic Questions

**If they have no profile yet:**
- Do you have a GitHub account? What's your username?
- Have you created a repository with your username?
- Are you comfortable with markdown, or would you prefer a generator tool?

**If they have an existing profile:**
- Share your profile URL so I can see what you have
- What do you like about your current profile?
- What do you want to improve or add?

**For customization goals:**
- Are you job hunting? (Recruiters love clean, professional profiles)
- Do you want to showcase specific projects or skills?
- Are you looking to build a personal brand?
- Do you write blog posts you want to feature?

## Step-by-Step Guidance

### For Complete Beginners (No Profile Yet)

#### Quick Start: Your First Profile in 5 Minutes

**Step 1: Create Your Profile Repository**
1. Go to GitHub and click the "+" icon → "New repository"
2. **CRITICAL**: Name the repository exactly your username (e.g., `johndoe`)
3. Set it to **Public** (private profiles won't work)
4. Check "Initialize with README"
5. Click "Create repository"

**Step 2: Add Your Profile Content**

Copy this entire block and paste it into your README.md (replace the placeholders):

```markdown
<div align="center">

# Hi, I'm Your Name! 👋

I'm a developer who loves building things that live on the internet.

## 🚀 What I'm Working On

- Currently building [your current project]
- Learning [technology you're learning]
- Open to collaborations on [topics you're interested in]

## 💬 Let's Connect

- Email: your.email@example.com
- LinkedIn: linkedin.com/in/yourprofile
- Twitter: @yourhandle

---

*This profile is a work in progress!*

</div>
```

**Step 3: Verify It Works**
1. Commit your changes (click "Commit changes")
2. Visit `github.com/YOUR_USERNAME` (not the repository, your main profile)
3. Wait 10-30 seconds and refresh
4. You should see your new profile!

**That's it!** You now have a working GitHub profile. Ready to level up? Continue below.

#### ✅ Profile Setup Checklist

Before customizing further, verify:
- [ ] Repository named exactly `YOUR_USERNAME` (case-sensitive)
- [ ] Repository is PUBLIC (not private)
- [ ] README.md exists in the root directory
- [ ] You can see your profile at github.com/YOUR_USERNAME

Not seeing your profile? See [Troubleshooting](#common-issues--solutions)

### For Beginners Wanting Enhancement

Once you have a basic profile, add these features one at a time:

```markdown
1. Add GitHub Stats Card
   - Shows your stars, forks, contributions
   - Choose a theme (dracula, radical, tokyonight)

2. Add Tech Stack Badges
   - Display your programming languages
   - Add frameworks and tools you use

3. Add Social Links
   - Email, LinkedIn, Twitter, Website
   - Use badge formats for consistency

4. Add Visitor Counter
   - Track how many people visit your profile
   - Geographic data if desired

5. Add Featured Projects
   - Link to your best repositories
   - Include brief descriptions
```

### For Intermediate Users (Existing Profile, Want Enhancement)

```markdown
1. Add Stats Cards (github-readme-stats)
2. Add Streak Stats
3. Add Profile Trophy
4. Add Visitor Counter
5. Add Tech Stack Icons
6. Add Typing Animation
7. Integrate Blog Feed (GitHub Actions)
8. Add Snake Contribution Animation
```

### For Advanced Users (Want Automation & Customization)

```markdown
1. Set Up GitHub Actions Workflows
   - Automated blog post updates
   - Dynamic content generation
   - Custom SVG generation
   - External API integrations

2. Create Custom Scripts
   - Python/Node.js for data fetching
   - Jinja2 templates for content
   - GraphQL queries for complex data

3. Optimize Performance
   - Caching strategies
   - API rate limiting
   - Lazy loading for large content
   - SVG optimization

4. Implement Security Best Practices
   - Token management
   - Permission limiting
   - Secret management
```

# Component Reference Guide

All code snippets below go in your `README.md` unless otherwise specified.

## Stats Cards

### GitHub Readme Stats (Most Popular)

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=dracula)
```

**Parameters Explained:**
- `username=YOUR_USERNAME` - Your GitHub username (required)
- `show_icons=true` - Show service icons next to labels
- `theme=dracula` - Color scheme (dracula, radical, tokyonight, gruvbox, synthwave, etc.)
- `hide_border=true` - Remove card border
- `title_color=00ff00` - Custom title color (hex code)
- `bg_color=000000` - Custom background color (hex code)

**Available Themes:**
- `dark`, `light`, `dracula`, `radical`, `merko`, `gruvbox`, `tokyonight`, `onedark`, `cobalt`, `synthwave`, `highcontrast`, `monokai`, `nord`, `gotham`

### Top Languages Card

```markdown
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USERNAME&layout=compact&theme=dracula)
```

### Repository Pin Card

```markdown
![Repo Card](https://github-readme-stats.vercel.app/api/pin/?username=YOUR_USERNAME&repo=REPO_NAME&theme=dracula)
```

### GitHub Trends (Advanced Metrics)

```markdown
[![GitHub Trends](https://github-readme-trends.vercel.app/api?username=YOUR_USERNAME)](https://github.com/avgupta456/github-trends)
```

**Features:**
- Lines of Code (LOC) statistics
- Advanced metrics beyond basic stats
- Customizable visualizations

### Streak Stats

```markdown
[![GitHub Streak](https://streak-stats.demolab.com/?user=YOUR_USERNAME&theme=dracula)](https://git.io/streak-stats)
```

**Parameters:**
- `theme=dracula` - Color theme
- `hide_border=true` - Remove border
- `mode=daily` - Show daily contributions
- `stroke=00ff00` - Custom stroke color

### Profile Trophy

```markdown
[![trophy](https://github-profile-trophy.vercel.app/?username=YOUR_USERNAME&theme=dracula&no-frame=true&column=4)](https://github.com/ryo-ma/github-profile-trophy)
```

**Parameters:**
- `no-frame=true` - Remove trophy frame
- `no-bg=true` - Remove background
- `column=4` - Number of columns (default: 7)
- `margin-w=4` - Width margin

## Animations

### Typing SVG

**File:** `README.md`

```markdown
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=00ff00&center=true&vCenter=true&width=940&lines=Full+Stack+Developer;Open+Source+Enthusiast;Always+learning+new+things)](https://git.io/typing-svg)
```

**Parameters:**
- `font=Fira+Code` - Font family (Fira+Code, monospace, Arial, etc.)
- `size=32` - Font size in pixels
- `duration=2800` - Typing duration in milliseconds
- `pause=2000` - Pause between typing cycles
- `color=00ff00` - Text color
- `center=true` - Center alignment
- `lines=Line1;Line2;Line3` - Lines to type (semicolon-separated)

### Snake Animation (GitHub Actions)

**File:** `.github/workflows/snake.yml`

```yaml
name: Generate Snake
on:
  schedule:
    - cron: "0 0 * * *"  # Daily at midnight
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: Platane/snk@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-snake.svg
            dist/github-snake-dark.svg?palette=github-dark
            dist/ocean.gif?generator_ocean

      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

**Usage in README.md:**

```markdown
![Snake Animation](https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_USERNAME/output/github-snake.svg)
```

## GitHub Achievements

### Understanding Achievements

GitHub Achievements are badges you earn for various activities on the platform. They add gamification to your profile and demonstrate your engagement with the GitHub community.

### Achievement Levels

- **DEFAULT** - Basic achievements everyone earns
- **BRONZE** - Intermediate achievements for consistent activity
- **SILVER** - Advanced achievements for dedicated contributors
- **GOLD** - Expert achievements for exceptional accomplishments

### Common Achievements & How to Earn Them

#### **Starstruck** (DEFAULT/Bronze)
- Created a repository that earned many stars
- **How to earn:** Create useful, high-quality repositories that people want to use

#### **Arctic Code Vault** (Bronze/Silver)
- Contributed to the Arctic Code Vault archive
- **How to earn:** Have contributions between Feb 2020 - Apr 2020

#### **Pull Shark** (Bronze/Silver/Gold)
- Made many pull requests
- **How to earn:** Contribute PRs regularly (Bronze: 10+, Silver: 100+, Gold: 500+)

#### **YOLO** (Bronze)
- Created a public repository and renamed default branch
- **How to earn:** Rename `master` branch to `main` or any other name

#### **Quickdraw** (Bronze)
- Quick response to issues
- **How to earn:** Comment on issues quickly after they're opened

#### **Pair Extraordinaire** (Bronze/Silver)
- Co-authored commits with others
- **How to earn:** Use `@` mentions in commit messages

#### **Galaxy Brain** (Bronze/Silver)
- Answers marked as helpful in discussions
- **How to earn:** Provide helpful answers in GitHub Discussions

#### **Mind Blowing** (Bronze)
- Received 10+ reactions on a discussion answer
- **How to earn:** Give exceptionally helpful answers

### How to Display Achievements

Achievements automatically appear on your profile once earned. To maximize them:

1. **Focus on quality contributions**
   - Create repos that solve real problems
   - Write clear documentation
   - Provide helpful examples

2. **Consistent activity**
   - Make regular contributions
   - Engage with issues and PRs
   - Participate in discussions

3. **Community engagement**
   - Collaborate with others
   - Co-author commits
   - Review pull requests

4. **Create popular repositories**
   - Build tools developers need
   - Write clear READMEs
   - Respond to issues promptly

### Achievement Resources

- **[GitHubAchievements.com](https://githubachievements.com/)** - Complete guide with earning strategies
- **[GitHub Achievements List](https://github.com/drknzz/GitHub-Achievements)** - Full achievement catalog with requirements
- **[Official GitHub Docs](https://docs.github.com/en/developers/overview)** - Understanding GitHub's achievement system

## Visitor Counters

### Basic Visitor Counter

```markdown
![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=YOUR_USERNAME.YOUR_USERNAME)
```

### Profile Views Counter

```markdown
![Profile Views](https://komarev.com/ghpvc/?username=YOUR_USERNAME&color=blueviolet&style=flat)
```

### Visitor Badge with Country Flags

```markdown
![Visitors](https://api.visitorbadge.io/api/VisitorBadge?userId=YOUR_USERNAME&repo=YOUR_USERNAME&countColor=%23263759)
```

## Tech Stack Icons

### Skill Icons (Interactive)

```markdown
[![My Skills](https://skillicons.dev/icons?i=js,ts,react,nodejs,python,go,java,aws,docker,kubernetes)](https://skillicons.dev)
```

### Badge Format (Static)

```markdown
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)
![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)
```

### Tech Stack Generator Icons

```markdown
<div align="center">
  <img src="https://techstack-generator.vercel.app/react-icon.svg" alt="React" width="50" height="50" />
  <img src="https://techstack-generator.vercel.app/js-icon.svg" alt="JavaScript" width="50" height="50" />
  <img src="https://techstack-generator.vercel.app/python-icon.svg" alt="Python" width="50" height="50" />
  <img src="https://techstack-generator.vercel.app/ts-icon.svg" alt="TypeScript" width="50" height="50" />
  <img src="https://techstack-generator.vercel.app/docker-icon.svg" alt="Docker" width="50" height="50" />
</div>
```

# AI-Powered Profile Generation

## AI-Assisted Generators (2025 Trend)

AI-powered tools can help you create your profile faster:

### Top AI-Powered Generators

1. **ReadMeCodeGen**
   - AI-powered editor with intelligent suggestions
   - Web: https://www.readmecodegen.com/profile-readme-generator
   - Smart template recommendations based on your activity

2. **rahuldkjain/github-profile-readme-generator**
   - Most popular generator with AI features
   - Web: https://github-readme-stats-generator.com/
   - Automated tech stack detection from your repos

3. **Using ChatGPT/Claude**
   - Generate profile content with AI assistance
   - Example prompt: "Create a GitHub profile README for a senior React developer who loves open source, contributes to React libraries, and is interested in GraphQL and TypeScript."

### How to Use AI Effectively

1. **Describe your skills and experience** to the AI
2. **Let AI suggest appropriate widgets and layouts**
3. **Customize the generated output** to maintain authenticity
4. **Add your unique voice and personality**

### Example AI Prompts

**For Job Seekers:**
```
"Create a GitHub profile README for a senior full-stack developer with 5 years experience. Skills: React, Node.js, Python, AWS. Looking for senior roles. Include stats cards, tech stack badges, and featured projects with impact metrics."
```

**For Open Source Contributors:**
```
"Create a minimalist GitHub profile for an open source enthusiast. Focus on contributions, starred repos, and community engagement. Use Tokyo Night theme. Include activity graph and contribution snake."
```

**For Students/Juniors:**
```
"Create a GitHub profile for a computer science student passionate about web development. Include learning journey, current projects, and contact information. Keep it clean and professional."
```

# External Service Integration

## Blog Feeds

**File:** `.github/workflows/blog-posts.yml`

```yaml
name: Blog Posts
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  update-blog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: gautamkrishnar/blog-post-workflow@v1
        with:
          comment_tag_name: BLOG_POST_LIST
          feed_list: "https://yourblog.com/feed.xml,https://medium.com/feed/@yourusername"
          max_post_count: 5
          feed_item_custom_template: "- [$title]($url)"
          date_format: "MMM DD, YYYY"
```

**In README.md:**
```markdown
## 📝 Latest Blog Posts

<!-- BLOG_POST_LIST:START -->
<!-- BLOG_POST_LIST:END -->
```

## Coding Stats

### WakaTime Integration

**File:** `.github/workflows/wakatime.yml`

```yaml
name: WakaTime Stats
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  update-wakatime:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: lowlighter/metrics@latest
        with:
          filename: metrics.svg
          token: ${{ secrets.METRICS_TOKEN }}
          base: header, activity, community, repositories, metadata
          plugin_wakatime: yes
          plugin_wakatime_sections: time, languages, languages-graphs, projects, history
          plugin_wakatime_token: ${{ secrets.WAKATIME_API_KEY }}
```

**Setup:**
1. Sign up at https://wakatime.com/
2. Get your API key from settings
3. Add `WAKATIME_API_KEY` to GitHub repository secrets
4. Add metrics SVG to README

### LeetCode Stats

```markdown
![LeetCode Stats](https://leetcode-stats.vercel.app/api?username=YOUR_USERNAME&theme=Dark&mode=card)

![LeetCode Stats](https://leetcode-stats.vercel.app/api?username=YOUR_USERNAME&theme=Dark)
```

**Parameters:**
- `theme=Dark` - Color theme (Dark, Light, Radical)
- `mode=card` - Display mode (default, card)

### Spotify Now Playing

**File:** `.github/workflows/spotify.yml`

```yaml
name: Update Spotify
on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
  workflow_dispatch:

jobs:
  spotify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses:athul/waka-readme@master
        with:
          WAKATIME_API_KEY: ${{ secrets.WAKATIME_API_KEY }}
```

# Performance & Security

## Performance Best Practices

### Optimize Loading Speed

1. **Limit External Images**
   - Use SVG instead of PNG/JPG when possible
   - Combine multiple stats into single cards
   - Remove unused widgets regularly

2. **Lazy Loading**
```markdown
<details>
<summary>Click to expand more stats</summary>

<br>
![Detailed Stats](https://github-readme-stats.vercel.app/api/...)
![More Stats](https://github-readme-stats.vercel.app/api/...)

</details>
```

3. **Caching Strategies**

**File:** `.github/workflows/cached-update.yml`

```yaml
name: Cached Profile Update
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Cache node modules
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Your update script
        run: |
          # Your update commands here

      - name: Check for changes
        id: check-changes
        run: |
          if git diff --quiet HEAD README.md; then
            echo "has_changes=false" >> $GITHUB_OUTPUT
          else
            echo "has_changes=true" >> $GITHUB_OUTPUT
          fi

      - name: Commit changes
        if: steps.check-changes.outputs.has_changes == 'true'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add README.md
          git commit -m "Update profile [skip ci]"
          git push
```

### API Rate Limiting

When fetching data from APIs:

1. **Use authentication** for higher rate limits
2. **Implement caching** to reduce API calls
3. **Batch requests** when possible
4. **Use GraphQL** instead of multiple REST calls

## Security Best Practices

### 1. Never Expose Secrets

**BAD:**
```yaml
run: echo "API_KEY=12345" > config.txt
```

**GOOD:**
```yaml
run: echo "API_KEY=${{ secrets.API_KEY }}" > config.txt
```

### 2. Use GitHub Secrets

Add secrets in: Repository Settings → Secrets and variables → Actions

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  API_KEY: ${{ secrets.API_KEY }}
  SPOTIFY_CLIENT_ID: ${{ secrets.SPOTIFY_CLIENT_ID }}
```

### 3. Limit Workflow Permissions

```yaml
permissions:
  contents: write
  pull-requests: read
```

### 4. Use Pinned Versions

```yaml
# BAD
- uses: actions/checkout@master

# GOOD
- uses: actions/checkout@v4

# GOOD (with SHA pinning for production)
- uses: actions/checkout@8ade135a41bc03ea155e62e844d2df94e0d05d4b
```

### 5. Token Rotation

- Use personal access tokens with minimal permissions
- Set expiration dates on tokens
- Review token access regularly
- Rotate tokens periodically

# Accessibility

## WCAG Compliance

1. **High Contrast**
   - Use themes like `highcontrast`, `dracula`, `tokyonight`
   - Avoid low contrast custom colors
   - Test contrast ratio (minimum 4.5:1 for normal text)

2. **Alt Text**
   - Provide alt text for all images
   - Example: `![Profile stats showing 500 stars and 200 forks](url)`

3. **Screen Reader Friendly**
   - Use semantic HTML (`<div align="center">`, `<details>`, etc.)
   - Ensure proper heading hierarchy
   - Test with screen readers

4. **Color Blind Safe**
   - Don't rely on color alone to convey information
   - Use symbols/icons along with colors
   - Test with color blindness simulators

5. **Keyboard Navigable**
   - Ensure all links are accessible via keyboard
   - Test tab order
   - Include focus indicators

## Recommended Themes for Accessibility

- **High Contrast** - Maximum accessibility (WCAG AAA)
- **Dracula** - Good contrast, very popular
- **Tokyo Night** - Easy on eyes, excellent readability
- **One Dark** - Professional, high contrast

Avoid: Custom themes with low contrast ratios

# Templates

## Minimalist Professional Template

```markdown
<div align="center">

# Hi, I'm Your Name 👋

[![Website](https://img.shields.io/badge/website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://yourwebsite.com)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/yourusername)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourusername)

</div>

## About Me

I'm a [Your Role] passionate about [Your Interests].

- 🔭 Currently working on [Project]
- 🌱 Learning [Technology]
- 👯 Open to collaborations on [Topic]
- 💬 Ask me about [Expertise]

## Tech Stack

[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)

## GitHub Stats

<div align="center">
  <img width="49%" src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=dracula&hide_border=true" />
  <img width="49%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USERNAME&layout=compact&theme=dracula&hide_border=true" />
</div>

## Featured Projects

- [Project 1](link) - Description
- [Project 2](link) - Description
- [Project 3](link) - Description

## Connect

[![Email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:your.email@example.com)
```

## Recruitment-Optimized Template

```markdown
<div align="center">

# Senior Full Stack Developer | React, Node.js, AWS | Open Source Contributor

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/yourprofile)
[![Email](https://img.shields.io/badge/Email-Contact-D14836)](mailto:your@email.com)

</div>

## About Me

Experienced full-stack developer with 5+ years building scalable web applications. Passionate about clean code, performance optimization, and mentoring junior developers.

## Tech Stack

### Frontend
[![React](https://img.shields.io/badge/React-20232A?logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js)](https://nextjs.org/)

### Backend
[![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql)](https://www.postgresql.org/)

### Cloud & DevOps
[![AWS](https://img.shields.io/badge/AWS-232F3E?logo=amazon-aws)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes)](https://kubernetes.io/)

## GitHub Stats

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=dracula&hide_border=true&rank_icon=github" />
</div>

## Featured Projects

### E-commerce Platform - 10,000+ users, 500+ stars
**Tech:** React, Node.js, PostgreSQL, AWS, Docker
- Launched product serving 10,000+ active users
- Achieved 99.9% uptime with auto-scaling
- Featured on ProductHunt, 500+ GitHub stars
- Link: [github.com/YOUR_USERNAME/project](https://github.com/YOUR_USERNAME/project)

### Real-Time Analytics Dashboard
**Tech:** TypeScript, WebSocket, Redis, Grafana
- Reduced data processing time by 60%
- Handles 1M+ events per day
- Real-time visualization for 500+ concurrent users
- Link: [github.com/YOUR_USERNAME/analytics](https://github.com/YOUR_USERNAME/analytics)

### Open Source Contributions
- Active contributor to [popular repo 1]
- Maintainer of [popular repo 2] with 1k+ stars
- 500+ contributions across 50+ repositories

## Contact

- **Email:** your.email@example.com
- **LinkedIn:** linkedin.com/in/yourprofile
- **GitHub:** github.com/YOUR_USERNAME
- **Location:** San Francisco, CA (Open to remote)
```

## Storytelling Timeline Template

```markdown
<div align="center">

# 👋 Hi, I'm Your Name

![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=00ff00&center=true&vCenter=true&width=940&height=50&lines=Full+Stack+Developer;Open+Source+Enthusiast;Always+learning+new+things)

</div>

## 📖 My Journey

### 🌱 2020 - Where It Started
- Built my first website with HTML & CSS
- Fell in love with coding and problem-solving
- Started learning JavaScript and Python

### 🚀 2021 - Growth
- First open source contribution to [project]
- Landed my first developer job at [company]
- Learned React, Node.js, and PostgreSQL
- Built [first significant project]

### 💡 2022 - Expertise
- Promoted to Senior Developer
- Started technical blog (10k+ views)
- Mentored 5 junior developers
- Contributed to [major open source project]

### 🔥 2023 - Present
- Full-stack architect at [company]
- 1000+ GitHub contributions
- Maintainer of [project] (500+ stars)
- Building products that matter

---

## 🏆 Achievements

<div align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=YOUR_USERNAME&theme=dracula&no-frame=true&no-bg=true&margin-w=4" />
</div>

---

## 🛠️ Tech Stack

[![My Skills](https://skillicons.dev/icons?i=js,ts,react,nodejs,python,go,aws,docker)](https://skillicons.dev)

---

## 📫 Let's Connect

[![Email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:your.email@example.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/yourusername)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?logo=twitter&logoColor=white)](https://twitter.com/yourhandle)
```

# Common Issues & Solutions

## Profile Not Showing

**Problem:** Your profile isn't visible on your GitHub page

**Solutions:**
1. Repository name must exactly match your username (case-sensitive)
2. Repository must be **public** (not private)
3. README.md must be in the root directory
4. Wait 1-2 minutes for GitHub to rebuild your profile
5. Try hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

## Stats Not Updating

**Problem:** Stats cards showing old data

**Solutions:**
1. Stats update daily (not real-time)
2. Check your username spelling in URLs
3. Wait 24 hours for changes to propagate
4. Clear browser cache

## Images Not Loading

**Problem:** Widget or badge images not displaying

**Solutions:**
1. Use HTTPS for all image URLs
2. Verify image URLs are correct
3. Check if the service is temporarily down
4. Try alternative badge/counter services

## GitHub Actions Failing

**Problem:** Workflows not running or failing

**Solutions:**
1. Check workflow file syntax (YAML indentation matters!)
2. Verify secrets are properly configured
3. Check Actions tab for error logs
4. Ensure repository has Actions enabled

## Layout Issues on Mobile

**Problem:** Profile looks bad on mobile devices

**Solutions:**
1. Limit widget width to 100%
2. Avoid too many side-by-side elements
3. Use `<div align="center">` for centering
4. Test on multiple devices

## Too Many Widgets

**Problem:** Profile is cluttered and slow

**Solutions:**
1. Remove unused or redundant widgets
2. Combine multiple stats into single cards
3. Use `<details>` for expandable content
4. Focus on essential information only

# Generator Tools

## Quick-Start Generators

For users who want a profile in under 5 minutes:

1. **rahuldkjain/github-profile-readme-generator** ⭐ Most Popular
   - Web: https://github-readme-stats-generator.com/
   - Easy drag-and-drop interface
   - Live preview with instant updates
   - One-click copy markdown
   - 10k+ users

2. **ProfileMe.dev**
   - Web: https://www.profileme.dev/
   - Quick profile generation
   - Beautiful modern templates
   - Social links integration
   - No account required

3. **Readmefy**
   - Web: https://readmefy.life/
   - Professional templates
   - Tech stack badges included
   - Stats cards integration
   - Clean interface

4. **ReadMeCodeGen**
   - Web: https://www.readmecodegen.com/profile-readme-generator
   - Custom card generator
   - 40+ themes available
   - Full customization
   - AI-powered suggestions

5. **Coderspace GitHub ReadMe Generator**
   - Web: https://coderspace.io/en/tools/github-readme-generator/
   - Share your bio in minutes
   - Easy-to-use interface
   - Story-focused templates

6. **awesomegithub.web.app**
   - Web: https://awesomegithub.web.app/
   - Used by 10k+ developers
   - Comprehensive features
   - Stats, skills, themes & social links

# Inspiration & Resources

## Curated Collections

- **[recodehive/awesome-github-profiles](https://github.com/recodehive/awesome-github-profiles)** - Best collection of inspiring profiles
- **[durgeshsamariya/awesome-github-profile-readme-templates](https://github.com/durgeshsamariya/awesome-github-profile-readme-templates)** - Comprehensive templates
- **[kautukkundan/Awesome-Profile-README-templates](https://github.com/kautukkundan/Awesome-Profile-README-templates)** - Real-world examples
- **[Awesome GitHub Profile Website](https://recodehive.github.io/awesome-github-profiles/)** - Categorized showcase

## Popular Examples (2025)

- **Neofetch-style terminal profiles** - Command-line aesthetic
- **Rainbow workflow designs** - Colorful contribution graphs
- **Minimalist professional** - Clean, focused layouts
- **Animated SVG profiles** - Interactive animations
- **Storytelling timelines** - Career journey visualizations

## Learning Resources

- **[GitHobby: Create Amazing Profile (2025)](https://githobby.com/blog/how-to-create-amazing-github-profile)** - Complete 2025 guide
- **[Dev.to: Customize Like a Pro](https://dev.to/sbre/how-to-customize-your-github-profile-like-a-pro-3fm)** - Professional customization
- **[YouTube: Ultimate Tutorial (2025)](https://www.youtube.com/watch?v=3GpVxXOXRlM)** - Video walkthrough
- **[Hashnode: Ultimate 2025 Guide](https://hasnainm.hashnode.dev/revamp-your-github-profile-the-ultimate-2025-readme-template-guide)** - Latest templates

# Advanced Automation

## GitHub Actions Cron Reference

### Cron Format

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6)
│ │ │ │ │
* * * * *
```

### Common Schedules

```yaml
# Every hour
- cron: '0 * * * *'

# Every day at midnight UTC
- cron: '0 0 * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Every Monday at 9:00 UTC
- cron: '0 9 * * 1'

# Every day at 8:00 and 18:00 UTC
- cron: '0 8,18 * * *'

# Every weekday at 9:00 UTC
- cron: '0 9 * * 1-5'

# Every month on the 1st at midnight
- cron: '0 0 1 * *'
```

## Python Script Automation

**File:** `scripts/update_readme.py`

```python
import requests
import re

def fetch_latest_repos(username):
    """Fetch user's latest repositories"""
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    return response.json()[:6]

def update_readme(readme_path, marker, content):
    """Update a section in README between markers"""
    with open(readme_path, 'r') as f:
        readme = f.read()

    start_marker = f'<!-- {marker}_START -->'
    end_marker = f'<!-- {marker}_END -->'

    pattern = f'{start_marker}.*?{end_marker}'
    replacement = f'{start_marker}\n{content}\n{end_marker}'

    readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)

    with open(readme_path, 'w') as f:
        f.write(readme)

if __name__ == '__main__':
    username = "YOUR_USERNAME"
    repos = fetch_latest_repos(username)

    content = "### Latest Repos\n\n"
    for repo in repos:
        content += f"- [{repo['name']}]({repo['html_url']}) - {repo.get('description', 'No description')}\n"

    update_readme('README.md', 'REPOS', content)
```

**In workflow:**
```yaml
- name: Update README with Python
  run: |
    python scripts/update_readme.py
```

# Your Approach

When helping users create their GitHub profile:

1. **Assess First**: Understand their goals, experience level, and preferences
2. **Start Simple**: Begin with a basic structure, then add features
3. **Provide Options**: Offer multiple approaches (generators vs manual, minimalist vs creative)
4. **Educate**: Explain what each component does and why it's valuable
5. **Iterate**: Build in stages, get feedback, refine
6. **Test**: Remind users to check on mobile and different themes
7. **Maintain**: Emphasize keeping content updated

Remember: A great GitHub profile balances personality, professionalism, and purpose. It should authentically represent the user while being fast, accessible, and maintainable.

# Quick Start Commands

```markdown
# Basic Profile (5 minutes)
1. Create username/username repository (public)
2. Add README.md with intro, skills, contact
3. Add stats card: ![Stats](https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME)
4. Verify at github.com/YOUR_USERNAME

# Enhanced Profile (15 minutes)
5. Add streak stats: ![Streak](https://streak-stats.demolab.com/?user=YOUR_USERNAME)
6. Add trophy: ![Trophy](https://github-profile-trophy.vercel.app/?username=YOUR_USERNAME)
7. Add visitor counter: ![Visitors](https://visitor-badge.laobi.icu/badge?page_id=YOUR_USERNAME.YOUR_USERNAME)
8. Add typing animation and tech stack badges

# Advanced Profile (1 hour)
9. Set up GitHub Actions for blog feed
10. Add snake contribution animation
11. Create custom workflow for dynamic content
12. Optimize performance and accessibility
13. Implement security best practices
```

The goal is to help users create profiles that are memorable, professional, and uniquely theirs—profiles that make recruiters take notice and collaborators want to connect.

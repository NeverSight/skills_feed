---
name: league-sdk
description: Build League of Legends apps using league-sdk TypeScript library. Use when working with Riot API, summoner/player lookups, match history, champion mastery, ranked stats, live game spectator, or building LoL Discord bots, websites, or apps.
---

# League SDK

Typed TypeScript SDK for Riot LoL API. Handles routing, PUUID conversions, rate limiting.

## LoL API Concepts

**Scope**: This SDK covers League of Legends only. TFT, Valorant, Wild Rift have separate APIs.

**PUUID**: Universal ID across Riot games. Preferred over SummonerId/AccountId (deprecated).

**Platform**: Use player's server (`kr` for Korean, `euw1` for EU West). Wrong platform = 404.

**Queue IDs**: `420` Solo/Duo, `440` Flex, `450` ARAM, `400` Normal Draft, `430` Blind

**Timestamps**: Unix epoch milliseconds → `new Date(match.gameCreation)`

**Match history**: Riot retains ~2 years. Older matches may be unavailable.

## Patterns

```typescript
import { LolClient, NotFoundError, RateLimitError } from 'league-sdk';

const client = new LolClient({
  apiKey: process.env.RIOT_API_KEY!,
  platform: 'na1'
});

// Player lookup
const player = await client.players.getByRiotId('Name', 'Tag');

// Ranked stats
const soloQ = await player.getSoloQueueStats();
// soloQ.tier, soloQ.division, soloQ.winRate (0-1 decimal)

// Match history
const matches = await player.getMatches({ count: 10, queue: 420 }); // 420 = ranked
for (const match of matches) {
  const p = match.getParticipant(player.puuid)!;
  console.log(`${p.championName} ${p.kills}/${p.deaths}/${p.assists} - ${p.win ? 'W' : 'L'}`);
}

// Participant stats
const p = match.getParticipant(player.puuid)!;
p.kills; p.deaths; p.assists; p.kda;
p.championName; p.win;
p.items;          // { item0-5, trinket }
p.totalCs; p.csPerMinute;
p.damage.toChampions; p.damage.taken;
p.goldEarned; p.visionScore;

// Match stats
match.gameDurationFormatted;  // "32:15"
match.queueName;              // "Ranked Solo/Duo"
match.blueTeam; match.redTeam;
match.getWinner(); match.didPlayerWin(player.puuid);

// Team comparison
const { blueTeam, redTeam } = match;
console.log(`Blue: ${blueTeam.totalKills}K, ${blueTeam.totalGold}g`);

// Live game (null if not in game)
const game = await player.getLiveGame();

// Mastery
const top = await player.getTopMastery(3);
// m.championName, m.championPoints, m.championLevel

// Static data (no API key needed)
const champs = await client.dataDragon.getChampions();
const items = await client.dataDragon.getItems();
await client.dataDragon.getChampionIconUrl('Ahri');
await client.dataDragon.getItemIconUrl(3157);
```

## Asset Downloads

```bash
npx league-sdk-assets --output ./assets --all
```

Programmatic: `import { downloadAllAssets } from 'league-sdk/scripts'`

## Platforms

`na1` `euw1` `eun1` `kr` `jp1` `br1` `la1` `la2` `oc1` `tr1` `ru` `sg2` `ph2` `th2` `tw2` `vn2`

## Troubleshooting

- **401**: API key expired (dev keys last 24h)
- **404**: Wrong platform or player doesn't exist
- **429**: Rate limited (SDK handles automatically)
- **NotFoundError**: Player/match doesn't exist
- **RateLimitError**: Has `retryAfter` property (seconds)
- **AuthenticationError**: Invalid API key

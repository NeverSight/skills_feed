---
name: baidu-milan-winter-olympics-2026
description: 获取2026年米兰冬奥会数据技能，包括奖牌榜排名、现场新闻报道和赛程安排。从百度体育网页抓取实时的奖牌排行榜信息、最新新闻资讯和比赛赛程。当用户需要获取米兰冬奥会需求，需要查询冬奥会奖牌榜、了解各国奖牌数量、获取现场新闻、查看赛程安排时使用此技能。能够根据指定时间(今天、明天、yyyy-MM-dd日期格式)或指定运动项目获取赛程安排。A skill for retrieving 2026 Milan Winter Olympics data, including medal standings, live news reports, and competition schedules. Scrapes real-time medal rankings, latest news, and match schedules from Baidu Sports. Use this skill when users need to query Winter Olympics medal standings, check medal counts by country, get live news, or view competition schedules.
---

# 2026年米兰冬奥会数据获取

## 技能概述

此技能用于获取2026年米兰冬奥会的以下数据：

### 1. 奖牌榜数据
- 各国/地区奖牌排名
- 金牌、银牌、铜牌数量
- 奖牌总数统计
- 国旗图片链接
- 详情页面链接

### 2. 现场新闻报道
- 最新赛事新闻
- 精彩瞬间
- 赛后采访
- 视频资讯
- 赛事集锦

### 3. 赛程数据
- 全部赛程安排
- 中国相关赛程
- 金牌赛赛程
- 热门赛程
- 比赛时间、状态、项目信息

### 4. 中国队获奖名单数据
- 中国队所有获奖运动员名单
- 奖牌类型（金牌/银牌/铜牌）
- 运动员姓名
- 比赛项目（大项和小项）
- 获奖时间
- 视频集锦链接
- 奖牌统计信息

数据来源：百度体育 (tiyu.baidu.com)

## 获取奖牌榜数据

### 获取奖牌榜TOP30

当用户需要查看奖牌榜前30名时：

```bash
node scripts/milan-olympics.js top
```

### 获取奖牌榜TOP N

获取指定数量的排名：

```bash
node scripts/milan-olympics.js top 10
```

### 获取完整奖牌榜

```bash
node scripts/milan-olympics.js all
```

### 奖牌榜返回数据字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| rank | number | 排名 |
| country | string | 国家/地区名称（中文） |
| countryEn | string | 国家/地区名称（英文） |
| gold | number | 金牌数 |
| silver | number | 银牌数 |
| bronze | number | 铜牌数 |
| total | number | 奖牌总数 |
| flagUrl | string | 国旗图片URL |
| detailUrl | string | 详情页面URL |

## 获取现场新闻数据

### 获取最新新闻列表

当用户需要查看冬奥会现场新闻时：

```bash
node scripts/milan-news.js list
```

### 获取指定数量的新闻

获取20条最新新闻：

```bash
node scripts/milan-news.js list 20
```

### 按类型筛选新闻

获取"赛事集锦"类型的新闻：

```bash
node scripts/milan-news.js list 10 赛事集锦
```

### 获取可用的内容类型

```bash
node scripts/milan-news.js types
```

可用类型包括：
- 全部
- 热门内容
- 赛事集锦
- 精彩瞬间
- 选手集锦
- 赛后采访
- 赛前采访
- 项目介绍
- 专栏节目
- 其他

## 新闻数据字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 新闻唯一标识 |
| title | string | 新闻标题 |
| type | string | 内容类型：article（文章）、video（视频）、post（动态） |
| subType | string | 内容子类型 |
| source | string | 新闻来源 |
| url | string | 详情页面URL |
| images | array | 图片URL数组 |
| videoDuration | string | 视频时长（仅视频类型） |
| videoUrl | string | 视频播放链接（仅视频类型） |
| matchId | array | 关联的赛事ID |

## 获取中国队获奖名单数据

### 获取全部获奖名单

当用户需要查看中国队所有获奖运动员时：

```bash
node scripts/milan-china-medals.js list
```

### 按奖牌类型筛选

获取中国队的金牌获奖名单：

```bash
node scripts/milan-china-medals.js list gold
```

获取中国队的银牌获奖名单：

```bash
node scripts/milan-china-medals.js list silver
```

获取中国队的铜牌获奖名单：

```bash
node scripts/milan-china-medals.js list bronze
```

### 获取奖牌统计

获取中国队奖牌统计信息（按项目和类型统计）：

```bash
node scripts/milan-china-medals.js stats
```

### 中国队获奖名单数据字段说明

**代表团信息（delegationInfo）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| country | string | 国家名称（中文） |
| countryEn | string | 国家名称（英文） |
| rank | string | 当前排名 |
| gold | string | 金牌数 |
| silver | string | 银牌数 |
| bronze | string | 铜牌数 |
| delegationId | string | 代表团ID |

**获奖记录（medals）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| playerName | string | 运动员姓名 |
| medal | string | 奖牌名称（如"第1银"） |
| medalType | string | 奖牌类型：gold/silver/bronze |
| medalRank | number | 奖牌序号 |
| bigMatch | string | 大项（如"自由式滑雪"） |
| smallMatch | string | 小项（如"自由式滑雪女子坡面障碍技巧"） |
| date | string | 日期（如"02月09日"） |
| time | string | 时间（如"21:00"） |
| medalTime | string | 时间戳 |
| rank | number | 比赛排名 |
| detailUrl | string | 详情页面URL |
| loc | string | 本地链接 |
| videoInfo | object | 视频信息（含播放链接） |
| playIconArr | array | 播放图标数组 |
| country | string | 国家 |
| olympicEventId | string | 赛事ID |

## 获取赛程数据

### 获取全部赛程

```bash
node scripts/milan-schedule.js all
```

### 获取特定日期的赛程

```bash
node scripts/milan-schedule.js all 2026-02-08
```

### 获取中国相关赛程

```bash
node scripts/milan-schedule.js china
```

获取特定日期的中国赛程：

```bash
node scripts/milan-schedule.js china 2026-02-08
```

### 获取金牌赛赛程

```bash
node scripts/milan-schedule.js gold
```

获取特定日期的金牌赛：

```bash
node scripts/milan-schedule.js gold 2026-02-08
```

### 获取热门赛程

```bash
node scripts/milan-schedule.js hot
```

### 获取今天的赛程（综合TAB）

自动获取今天日期的全部赛程，无需手动指定日期：

```bash
node scripts/milan-schedule.js today
```

### 获取明天的赛程（综合TAB）

自动获取明天日期的全部赛程，无需手动指定日期：

```bash
node scripts/milan-schedule.js tomorrow
```

### 获取可用的日期列表

```bash
node scripts/milan-schedule.js dates
```

### 赛程数据字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| matchId | string | 比赛唯一标识 |
| matchName | string | 比赛名称 |
| sportName | string | 项目大类名称 |
| eventName | string | 具体小项名称 |
| startTime | string | 开始时间（HH:mm） |
| startDate | string | 开始日期（YYYY-MM-DD） |
| startDateTime | string | 完整开始时间 |
| status | string | 比赛状态（未开赛、进行中、已结束等） |
| statusId | string | 状态ID |
| desc | string | 比赛描述/备注 |
| isChina | boolean | 是否中国相关赛程 |
| isGold | boolean | 是否金牌赛 |
| isHot | boolean | 是否热门赛程 |
| isMedal | boolean | 是否奖牌赛 |
| hasLive | boolean | 是否有直播 |
| participant | string | 参赛类型（单人/团体） |
| detailUrl | string | 详情页面URL |
| iconArr | array | 图标标签数组 |

### 获取运动项目列表

查看所有可用的运动项目及其ID：

```bash
node scripts/milan-schedule.js sports
```

返回数据结构：
- **hot**: 热门项目列表（包含热度值）
- **other**: 其他项目列表

常见运动项目ID对照：
| 项目名称 | ID |
|---------|-----|
| 短道速滑 | 302 |
| 花样滑冰 | 217 |
| 速度滑冰 | 103 |
| 单板滑雪 | 222 |
| 自由式滑雪 | 221 |
| 冰壶 | 212 |
| 冰球 | 113 |
| 高山滑雪 | 115 |
| 雪车 | 213 |
| 雪橇 | 214 |
| 钢架雪车 | 307 |
| 跳台滑雪 | 215 |
| 越野滑雪 | 220 |
| 滑雪登山 | 615 |
| 北欧两项 | 216 |
| 冬季两项 | 218 |

### 获取指定运动项目的赛程

查询特定运动项目的赛程安排：

```bash
# 获取短道速滑所有赛程
node scripts/milan-schedule.js sport 302

# 获取特定日期的短道速滑赛程
node scripts/milan-schedule.js sport 302 2026-02-10
```

### 获取中国指定运动项目的赛程

查询中国队在特定运动项目的赛程：

```bash
# 获取中国短道速滑赛程
node scripts/milan-schedule.js china-sport 302

# 获取特定日期中国短道速滑赛程
node scripts/milan-schedule.js china-sport 302 2026-02-10
```

## 作者介绍

- 爱海贼的无处不在
- 我的微信公众号：无处不在的技术

## 注意事项

- 数据从百度体育网页实时抓取，可能存在短暂延迟
- 奖牌榜数据会随着比赛进行不断更新
- 排名规则遵循国际奥委会标准（先按金牌数，再按银牌数，再按铜牌数）
- 新闻内容实时更新，包含文字报道、图片和视频
- 赛程数据包含比赛时间、项目、状态等信息

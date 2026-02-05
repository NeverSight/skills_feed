---
name: linkedin-project-post
description: Generate exciting LinkedIn posts to showcase your vibe coding projects with emojis, hashtags, features, tech stack, and call-to-action for engagement.
---

# LinkedIn Project Post

## Command
`/linkedin-post` or `linkedin-post`

## Keywords
linkedin, linkedin post, share project, vibe coding, showcase project, social media post, project announcement, github project, portfolio post

## Description
Generate an engaging LinkedIn post to showcase your coding project with excitement, emojis, and a call-to-action for the developer community.

## Execution
This skill runs using **Claude Code with subscription plan**. Do NOT use pay-as-you-go API keys.

## Response
I'll generate an exciting LinkedIn post for your project!

The post will include:

| Section | Description |
|---------|-------------|
| **Screenshot** | Auto-captured screenshot of the demo site |
| **Hook** | Exciting opening with emojis to grab attention |
| **Live Demo Link** | URL to the deployed app |
| **GitHub Repo Link** | URL to the source code |
| **What It's About** | Brief description of the project purpose |
| **Key Features** | Bullet list of main features with checkmarks |
| **Tech Stack** | Technologies used with emoji icons |
| **Call to Action** | Encourage fork, comment, discuss, star |
| **Hashtags** | Relevant hashtags for visibility |

## Screenshot Capture
Before generating the post, automatically capture a screenshot of the demo site and save to **~/Downloads** folder:

### Using the included script (Recommended)
```bash
./scripts/capture-screenshot.sh [URL]
# Saves to ~/Downloads/linkedin-screenshot.png and opens folder
```

### Method 1: Using Puppeteer (Node.js)
```bash
npx puppeteer screenshot [URL] --output ~/Downloads/linkedin-screenshot.png --viewport 1200x630
```

### Method 2: Using Shot-scraper (Python)
```bash
shot-scraper [URL] -o ~/Downloads/linkedin-screenshot.png --width 1200 --height 630
```

### Method 3: Using Screenshot API
```bash
curl "https://api.screenshotone.com/take?url=[URL]&viewport_width=1200&viewport_height=630&format=png" -o ~/Downloads/linkedin-screenshot.png
```

### Recommended Screenshot Settings
- **Dimensions**: 1200x630px (LinkedIn optimal)
- **Format**: PNG or JPG
- **Save location**: ~/Downloads folder
- **Full page**: No, capture viewport only

### Screenshot Tips
- Capture the hero section or main feature
- Ensure the app is in a visually appealing state
- If login required, capture the landing/login page
- Downloads folder opens automatically for easy upload

## Instructions
When generating a LinkedIn post, follow this structure:

### 1. Opening Hook
Start with enthusiasm and relevant emojis:
```
I'm thrilled to share a passion project I've been building — [Project Name] — [one-line description]! 🚀✨
```

### 2. Links Section
```
🌐 Check it out: [Live Demo URL]

📦 GitHub repo: [GitHub URL]
```

### 3. What It's About
```
🧭 What it's all about

[2-3 sentences describing the problem it solves and who it's for]
```

### 4. Key Features
```
🚀 Key Features

✅ [Feature 1]
✅ [Feature 2]
✅ [Feature 3]
✅ [Feature 4]
✅ [Feature 5]
… and more to come!
```

### 5. Tech Stack
```
🛠️ Built With

💻 Tech Stack:
• [Technology 1]
• [Technology 2]
• [Technology 3]
• [Technology 4]
• Hosted on [Platform]
```

### 6. Call to Action
```
⭐ Get Involved

Love [topic] or coding? Feel free to fork the project, leave a comment, and start a discussion!
👉 Don't forget to ⭐ star the repo — every star motivates open-source creators like me!

🔗 Repo: [GitHub URL]
```

### 7. Hashtags
Add 5-10 relevant hashtags:
```
#VibeCoding #OpenSource #WebDev #JavaScript #React #BuildInPublic #DevCommunity #100DaysOfCode #CodeNewbie #SideProject
```

## Emoji Guide
Use these emojis appropriately:
- 🚀 Launch/Features
- ✨ Highlights
- 🌐 Web/Live demo
- 📦 GitHub/Package
- 🧭 About/Navigation
- ✅ Features/Checkmarks
- 🛠️ Tech/Tools
- 💻 Code/Development
- ⭐ Star/Call to action
- 👉 Pointer/Direction
- 🔗 Links
- 🎯 Goals/Purpose
- 💡 Ideas/Tips
- 🔥 Hot/Trending

## Tone Guidelines
- Enthusiastic but authentic
- Professional yet approachable
- Celebrate the achievement
- Invite collaboration
- Show gratitude to the community

## Capabilities
- Generate engaging LinkedIn posts for any coding project
- Customize tone based on project type
- Include relevant hashtags for discoverability
- Create compelling calls-to-action
- Highlight tech stack professionally

## Open LinkedIn to Post
After generating the post, open LinkedIn's compose page:
```bash
open "https://www.linkedin.com/feed/?shareActive=true"
```

## Next Steps
After generating the post:
1. Screenshot auto-saved to ~/Downloads/linkedin-screenshot.png
2. LinkedIn compose page opens in browser
3. Paste the generated post text
4. Click photo icon → upload screenshot from Downloads
5. Tag relevant people or companies if applicable
6. Post during peak LinkedIn hours (Tue-Thu, 8-10am)
7. Engage with comments promptly

---
name: mux-video
description: Comprehensive guide to building video applications with Mux, the developer-first video infrastructure platform. This skill covers video streaming, live streaming, player integrations, analytics with Mux Data, and AI-powered workflows. Whether you are building a video-on-demand platform, live streaming application, or integrating video into an existing product, this documentation provides the patterns and code examples needed to ship quickly.
---

# Mux Video Platform

Comprehensive guide to building video applications with Mux, the developer-first video infrastructure platform. This skill covers video streaming, live streaming, player integrations, analytics with Mux Data, and AI-powered workflows. Whether you are building a video-on-demand platform, live streaming application, or integrating video into an existing product, this documentation provides the patterns and code examples needed to ship quickly.

## Key Capabilities

- **Video Hosting and Streaming**: Upload, transcode, and deliver video content globally via adaptive bitrate streaming (HLS)
- **Live Streaming**: Real-time video broadcasting with RTMP/SRT ingest, low-latency options, and automatic recording
- **Mux Player**: Drop-in video player components for web (React, vanilla JS), iOS, and Android with built-in analytics
- **Mux Data**: Quality of experience analytics, engagement metrics, and real-time monitoring
- **Content Security**: Signed playback URLs, DRM protection (Widevine/FairPlay), and domain restrictions
- **AI Workflows**: Automatic chapter generation, video summarization, content moderation, and audio dubbing

---

## Quick Start

Get streaming in five minutes:

1. **Create an API Access Token** in the [Mux Dashboard](https://dashboard.mux.com/settings/access-tokens) with Video Read and Write permissions

2. **Create a video asset** from a URL:
```bash
curl https://api.mux.com/video/v1/assets \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{ "input": [{ "url": "https://muxed.s3.amazonaws.com/leds.mp4" }], "playback_policy": ["public"] }' \
  -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET}
```

3. **Play the video** using the returned playback ID:
```html
<script src="https://cdn.jsdelivr.net/npm/@mux/mux-player"></script>
<mux-player playback-id="YOUR_PLAYBACK_ID"></mux-player>
```

See [examples/quickstart-stream-video.md](examples/quickstart-stream-video.md) for the complete walkthrough with SDK examples in Node.js, Python, Ruby, Go, and PHP.

---

## Reference Documentation

### Core Concepts

Foundational knowledge for working with Mux APIs and infrastructure.

| File | Description |
|------|-------------|
| [reference/mux-fundamentals.md](reference/mux-fundamentals.md) | Organizations, environments, assets, playback IDs, and API structure |
| [reference/api-authentication.md](reference/api-authentication.md) | Access tokens, permissions, and secure API request patterns |
| [reference/webhooks.md](reference/webhooks.md) | Webhook events, signature verification, and event handling |
| [reference/content-security-policy.md](reference/content-security-policy.md) | CSP configuration for Mux Player and streaming domains |

### Mux Player

Drop-in video player components with built-in analytics and adaptive controls.

| File | Description |
|------|-------------|
| [reference/mux-player-overview.md](reference/mux-player-overview.md) | Platform support (web, iOS, Android), installation, and core features |
| [reference/player-setup-integration.md](reference/player-setup-integration.md) | HTML, React, iframe embed, and native mobile integration |
| [reference/player-customization.md](reference/player-customization.md) | Theming, CSS variables, custom controls, and branding |
| [reference/player-advanced-features.md](reference/player-advanced-features.md) | Chromecast, AirPlay, DVR mode, picture-in-picture, and quality selection |
| [reference/playback-security.md](reference/playback-security.md) | Signed URLs, JWT token generation, and playback restrictions |
| [reference/playback-modifiers-resolution.md](reference/playback-modifiers-resolution.md) | Resolution capping, bandwidth hints, and playback URL parameters |

### Video Upload and Asset Management

Methods for getting video content into Mux and configuring assets.

| File | Description |
|------|-------------|
| [reference/upload-methods.md](reference/upload-methods.md) | URL ingestion, direct uploads, and resumable upload protocols |
| [reference/mux-uploader.md](reference/mux-uploader.md) | Drop-in upload components for web with progress and error handling |
| [reference/mobile-upload-sdks.md](reference/mobile-upload-sdks.md) | iOS and Android upload SDKs for native applications |
| [reference/asset-configuration.md](reference/asset-configuration.md) | Video quality tiers, MP4 support, master access, and encoding settings |
| [reference/text-tracks-and-audio.md](reference/text-tracks-and-audio.md) | Captions, subtitles, audio tracks, and language configuration |

### Live Streaming

Real-time video broadcasting with global ingest and low-latency delivery.

| File | Description |
|------|-------------|
| [reference/live-streaming-getting-started.md](reference/live-streaming-getting-started.md) | Creating live streams, stream keys, and basic broadcasting |
| [reference/live-stream-configuration.md](reference/live-stream-configuration.md) | Latency modes, reconnect windows, and recording settings |
| [reference/streaming-protocols-encoder-setup.md](reference/streaming-protocols-encoder-setup.md) | RTMP, RTMPS, SRT protocols and encoder configuration |
| [reference/live-stream-features.md](reference/live-stream-features.md) | Simulcasting, live clipping, DVR mode, and embedded captions |
| [reference/live-stream-troubleshooting.md](reference/live-stream-troubleshooting.md) | Common issues, debugging, and encoder compatibility |

### Mux Data and Analytics

Quality of experience metrics, engagement tracking, and performance monitoring.

| File | Description |
|------|-------------|
| [reference/metrics-overview.md](reference/metrics-overview.md) | Views, watch time, QoE scores, and metric definitions |
| [reference/dashboards-and-filtering.md](reference/dashboards-and-filtering.md) | Dashboard navigation, filters, and data exploration |
| [reference/custom-metadata-and-dimensions.md](reference/custom-metadata-and-dimensions.md) | Custom dimensions, video metadata, and viewer identification |
| [reference/data-exports.md](reference/data-exports.md) | CSV exports, S3 delivery, and raw data access |
| [reference/alerts-and-monitoring.md](reference/alerts-and-monitoring.md) | Alert configuration, thresholds, and notification channels |
| [reference/privacy-and-configuration.md](reference/privacy-and-configuration.md) | Data retention, GDPR compliance, and privacy settings |

### Player Monitoring Integrations

Integrating Mux Data with third-party video players.

| File | Description |
|------|-------------|
| [reference/web-player-integrations.md](reference/web-player-integrations.md) | Video.js, HLS.js, Shaka Player, JW Player, and Bitmovin |
| [reference/mobile-player-integrations.md](reference/mobile-player-integrations.md) | AVPlayer (iOS), ExoPlayer (Android), and native SDKs |
| [reference/smart-tv-device-integrations.md](reference/smart-tv-device-integrations.md) | Roku, Fire TV, Apple TV, and smart TV platforms |
| [reference/custom-player-integrations.md](reference/custom-player-integrations.md) | Building custom player integrations with Mux Data SDK |

### Video Features and Tools

Additional video capabilities beyond basic playback.

| File | Description |
|------|-------------|
| [reference/video-clipping.md](reference/video-clipping.md) | Creating clips from assets, URL-based clipping, and clip management |
| [reference/images-and-thumbnails.md](reference/images-and-thumbnails.md) | Thumbnail generation, animated GIFs, and timeline previews |
| [reference/custom-domains-and-security.md](reference/custom-domains-and-security.md) | CNAME setup, SSL certificates, and branded delivery domains |
| [reference/social-sharing-and-special-features.md](reference/social-sharing-and-special-features.md) | OG tags, Twitter cards, and social media optimization |

### Framework Integrations

Platform-specific guides for popular web and mobile frameworks.

| File | Description |
|------|-------------|
| [reference/web-framework-integrations.md](reference/web-framework-integrations.md) | Next.js, Remix, SvelteKit, Nuxt, and other web frameworks |
| [reference/react-native-getting-started.md](reference/react-native-getting-started.md) | Setting up Mux in React Native applications |
| [reference/react-native-video-features.md](reference/react-native-video-features.md) | Video playback, uploads, and analytics in React Native |
| [reference/react-native-ui-patterns.md](reference/react-native-ui-patterns.md) | Common UI patterns for video apps (feeds, stories, full-screen) |
| [reference/react-native-advanced-topics.md](reference/react-native-advanced-topics.md) | Performance optimization, offline playback, and background audio |

### CMS Integrations and SDKs

Connecting Mux with content management systems and backend services.

| File | Description |
|------|-------------|
| [reference/cms-integrations.md](reference/cms-integrations.md) | Sanity, Contentful, WordPress, Strapi, and other CMS platforms |
| [reference/server-side-sdks.md](reference/server-side-sdks.md) | Node.js, Python, Ruby, PHP, Go, Java, and .NET SDKs |
| [reference/mcp-server.md](reference/mcp-server.md) | Mux MCP server for AI assistant integrations |

### Pricing and Cost Management

Understanding and optimizing Mux costs.

| File | Description |
|------|-------------|
| [reference/pricing-overview.md](reference/pricing-overview.md) | Pricing model, billable metrics, and cost calculations |
| [reference/cost-optimization.md](reference/cost-optimization.md) | Strategies for reducing encoding, storage, and delivery costs |

---

## Examples

### Getting Started

| File | Description |
|------|-------------|
| [examples/quickstart-stream-video.md](examples/quickstart-stream-video.md) | Complete guide to uploading and playing your first video |
| [examples/webhook-signature-verification.md](examples/webhook-signature-verification.md) | Verifying webhook signatures in Node.js, Python, and Ruby |

### Player Integration

| File | Description |
|------|-------------|
| [examples/mux-player-web-setup.md](examples/mux-player-web-setup.md) | Setting up Mux Player in HTML, React, and Vue applications |
| [examples/signed-url-playback.md](examples/signed-url-playback.md) | Generating and using signed playback URLs with JWTs |
| [examples/drm-protected-playback.md](examples/drm-protected-playback.md) | Configuring DRM-protected content with Widevine and FairPlay |

### Video Upload

| File | Description |
|------|-------------|
| [examples/direct-upload-with-webhooks.md](examples/direct-upload-with-webhooks.md) | Client-side uploads with server webhook handling |
| [examples/video-with-captions-and-metadata.md](examples/video-with-captions-and-metadata.md) | Uploading videos with subtitle tracks and custom metadata |

### Live Streaming

| File | Description |
|------|-------------|
| [examples/live-streaming-complete-setup.md](examples/live-streaming-complete-setup.md) | End-to-end live streaming implementation |
| [examples/live-captions-and-simulcasting.md](examples/live-captions-and-simulcasting.md) | Adding live captions and streaming to multiple platforms |

### Analytics

| File | Description |
|------|-------------|
| [examples/custom-analytics-integration.md](examples/custom-analytics-integration.md) | Advanced Mux Data integration with custom dimensions |
| [examples/web-player-integration-example.md](examples/web-player-integration-example.md) | Integrating Mux Data with Video.js and HLS.js |
| [examples/mobile-player-integration-example.md](examples/mobile-player-integration-example.md) | iOS and Android analytics SDK integration |

### Video Features

| File | Description |
|------|-------------|
| [examples/video-clipping-workflows.md](examples/video-clipping-workflows.md) | Creating clips for social sharing and highlights |
| [examples/thumbnail-and-preview-integration.md](examples/thumbnail-and-preview-integration.md) | Dynamic thumbnails and timeline hover previews |

### React Native

| File | Description |
|------|-------------|
| [examples/react-native-stories-app.md](examples/react-native-stories-app.md) | Building an Instagram-style stories feature |
| [examples/react-native-video-upload-workflow.md](examples/react-native-video-upload-workflow.md) | Complete upload flow with progress and background handling |

### CMS Integration

| File | Description |
|------|-------------|
| [examples/cms-setup-sanity.md](examples/cms-setup-sanity.md) | Integrating Mux with Sanity CMS |

### AI Workflows

| File | Description |
|------|-------------|
| [examples/ai-video-workflows.md](examples/ai-video-workflows.md) | Automatic chapters, summarization, and tagging with @mux/ai |
| [examples/content-moderation-strategies.md](examples/content-moderation-strategies.md) | AI-powered content moderation for user-generated video |
| [examples/video-synchronization.md](examples/video-synchronization.md) | Syncing video playback across multiple viewers |

---

## Important Notes

### API Authentication

All Mux API requests require authentication using a Token ID and Token Secret. API requests must be made from a server environment - the API does not support CORS and credentials should never be exposed in client-side code.

### Playback IDs vs Asset IDs

- **Asset IDs** are used to manage content via the API (`api.mux.com`)
- **Playback IDs** are used to stream content to viewers (`stream.mux.com`)
- An asset can have multiple playback IDs with different policies (public vs signed)

### Webhooks vs Polling

Always prefer webhooks over polling to track asset status. Webhooks provide real-time notifications when assets are ready, live streams change state, or uploads complete. Configure webhooks per environment in the Mux Dashboard.

### Video Quality Tiers

Mux offers different video quality tiers (basic, plus, premium) that affect encoding quality and pricing. Choose the appropriate tier based on your content type and quality requirements.

### Stream Key Security

Live stream keys should be treated as secrets. Anyone with the stream key can broadcast to your live stream. Reset keys immediately if compromised.

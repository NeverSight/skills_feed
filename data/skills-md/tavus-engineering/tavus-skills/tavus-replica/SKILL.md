---
name: tavus-replica
description: Create and manage Tavus replicas (AI digital twins). Use when training custom replicas from video, listing stock replicas, or managing replica assets. Covers training video requirements, consent statements, and the Phoenix-3 model.
---

# Tavus Replica Skill

Create lifelike AI digital twins for video generation and real-time conversations.

## Stock Replicas (Ready to Use)

No training needed. Use these IDs directly:
- `rfe12d8b9597` - Default stock replica
- `re8e740a42` - Nathan

Full list: https://docs.tavus.io/sections/replica/stock-replicas

## Create Custom Replica

### Training Video Requirements

1. **Duration**: 1 min talking + 1 min silence (same video)
2. **Quality**: 1080p minimum, stable camera at eye level
3. **Lighting**: Diffuse, even lighting, no shadows on face
4. **Audio**: Silent room, no background noise
5. **Framing**: Face fills at least 25% of frame
6. **Expression**: Start talking segment with a big smile
7. **Background**: Simple, static, no moving objects/people

### Consent Video

Required for personal replicas. Record yourself saying:
> "I, [full name], consent to the creation of a digital replica of my likeness for use with Tavus technology."

Can be separate video or at start of training video.

### API: Create Replica

```bash
curl -X POST https://tavusapi.com/v2/replicas \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "replica_name": "My Avatar",
    "train_video_url": "https://s3.../train.mp4",
    "consent_video_url": "https://s3.../consent.mp4",
    "callback_url": "https://your-webhook.com/tavus"
  }'
```

Response:
```json
{
  "replica_id": "r783537ef5",
  "status": "training",
  "training_progress": "0/100"
}
```

Training takes **4-6 hours**. You'll receive a webhook or poll status.

### API: Check Training Status

```bash
curl https://tavusapi.com/v2/replicas/{replica_id} \
  -H "x-api-key: YOUR_API_KEY"
```

Status values: `training`, `completed`, `error`

### API: List All Replicas

```bash
curl https://tavusapi.com/v2/replicas \
  -H "x-api-key: YOUR_API_KEY"
```

### API: Delete Replica

```bash
curl -X DELETE https://tavusapi.com/v2/replicas/{replica_id} \
  -H "x-api-key: YOUR_API_KEY"
```

## Best Practices

- Use desktop recording apps (QuickTime, Windows Camera) not browser
- Pre-signed S3 URLs must be valid for 24+ hours
- Phoenix-3 model is default and recommended
- Test with stock replicas before training custom ones

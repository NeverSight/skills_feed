---
name: cloudinary
description: Upload images and videos to Cloudinary with CDN delivery and transformations. Use this skill for media hosting, optimization, resizing, format conversion, and video concatenation.
vm0_secrets:
  - CLOUDINARY_API_KEY
  - CLOUDINARY_API_SECRET
vm0_vars:
  - CLOUDINARY_CLOUD_NAME
---

# Cloudinary Media Hosting

Cloudinary provides image and video hosting with CDN delivery, automatic optimization, and on-the-fly transformations.

## When to Use

- Upload images with automatic optimization
- Upload videos with CDN delivery
- Get CDN-delivered media URLs
- Apply transformations (resize, crop, format conversion)
- Concatenate/splice multiple videos
- Host media for production applications

## Prerequisites

Set the following environment variables:

```bash
export CLOUDINARY_CLOUD_NAME=your_cloud_name
export CLOUDINARY_API_KEY=your_api_key
export CLOUDINARY_API_SECRET=your_api_secret
```

Get credentials from: https://console.cloudinary.com/settings/api-keys


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### Method 1: Unsigned Upload (Simpler)

First, create an unsigned upload preset in Cloudinary Console:
Settings > Upload > Upload presets > Add upload preset > Signing Mode: Unsigned

```bash
curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/image/upload" -F "file=@/path/to/image.png" -F "upload_preset=your_preset_name"
```

### Method 2: Signed Upload

Generate signature and upload:

```bash
# Generate timestamp
TIMESTAMP=$(date +%s)

# Generate signature (alphabetical order of params)
SIGNATURE=$(bash -c 'echo -n "timestamp=$TIMESTAMP$CLOUDINARY_API_SECRET" | sha1sum | cut -d" " -f1')

# Upload
curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/image/upload" -F "file=@/path/to/image.png" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"
```

### Upload from URL

```bash
TIMESTAMP=$(date +%s)
SIGNATURE=$(bash -c 'echo -n "timestamp=$TIMESTAMP$CLOUDINARY_API_SECRET" | sha1sum | cut -d" " -f1')

curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/image/upload" -F "file=https://example.com/image.png" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"
```

### Upload Video

```bash
TIMESTAMP=$(date +%s)
SIGNATURE=$(bash -c 'echo -n "timestamp=$TIMESTAMP$CLOUDINARY_API_SECRET" | sha1sum | cut -d" " -f1')

curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/video/upload" -F "file=@/path/to/video.mp4" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"
```

### Upload Video with Custom Public ID

```bash
TIMESTAMP=$(date +%s)
PUBLIC_ID="my-videos/clip1"
SIGNATURE=$(bash -c 'echo -n "public_id=$PUBLIC_ID&timestamp=$TIMESTAMP$CLOUDINARY_API_SECRET" | sha1sum | cut -d" " -f1')

curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/video/upload" -F "file=@/path/to/video.mp4" -F "public_id=$PUBLIC_ID" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"
```

### Upload Video from URL

```bash
TIMESTAMP=$(date +%s)
PUBLIC_ID="my-videos/clip1"
SIGNATURE=$(bash -c 'echo -n "public_id=$PUBLIC_ID&timestamp=$TIMESTAMP$CLOUDINARY_API_SECRET" | sha1sum | cut -d" " -f1')

curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/video/upload" -F "file=https://example.com/video.mp4" -F "public_id=$PUBLIC_ID" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"
```

### With Custom Public ID

```bash
TIMESTAMP=$(date +%s)
PUBLIC_ID="my-folder/my-image"
SIGNATURE=$(bash -c 'echo -n "public_id=$PUBLIC_ID&timestamp=$TIMESTAMP$CLOUDINARY_API_SECRET" | sha1sum | cut -d" " -f1')

curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/image/upload" -F "file=@/path/to/image.png" -F "public_id=$PUBLIC_ID" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"
```

## Response

```json
{
  "public_id": "sample",
  "secure_url": "https://res.cloudinary.com/demo/image/upload/v1234567890/sample.png",
  "url": "http://res.cloudinary.com/demo/image/upload/v1234567890/sample.png",
  "format": "png",
  "width": 800,
  "height": 600
}
```

Key field: `secure_url` - Use this in Markdown: `![img](https://res.cloudinary.com/...)`

## URL Transformations

Cloudinary URLs support on-the-fly transformations:

```
https://res.cloudinary.com/{cloud_name}/image/upload/{transformations}/{public_id}.{format}
```

Examples:
```
# Resize to 300x200
.../image/upload/w_300,h_200/sample.png

# Auto format and quality
.../image/upload/f_auto,q_auto/sample.png

# Crop to square
.../image/upload/w_200,h_200,c_fill/sample.png

# Combine transformations
.../image/upload/w_400,h_300,c_fill,f_auto,q_auto/sample.png
```

## Video Concatenation (Splice)

Concatenate videos using URL transformations with `l_video:` (overlay) and `fl_splice` flag.

### Basic Concatenation

Append `clip2` to the end of `clip1`:

```
https://res.cloudinary.com/{cloud_name}/video/upload/l_video:clip2,fl_splice/fl_layer_apply/clip1.mp4
```

### Concatenate Multiple Videos

Append `clip2` and `clip3` to `clip1`:

```
https://res.cloudinary.com/{cloud_name}/video/upload/l_video:clip2,fl_splice/fl_layer_apply/l_video:clip3,fl_splice/fl_layer_apply/clip1.mp4
```

### With Uniform Size

Resize all videos to same dimensions:

```
https://res.cloudinary.com/{cloud_name}/video/upload/w_640,h_360,c_fill/l_video:clip2,fl_splice,w_640,h_360,c_fill/fl_layer_apply/clip1.mp4
```

### With Fade Transition

Add fade out (-1000ms) on first video and fade in (1000ms) on second:

```
https://res.cloudinary.com/{cloud_name}/video/upload/w_640,h_360,c_fill,e_fade:-1000/l_video:clip2,fl_splice,e_fade:1000,w_640,h_360,c_fill/fl_layer_apply/clip1.mp4
```

### Add Image as Intro (3 seconds)

Prepend an image as intro:

```
https://res.cloudinary.com/{cloud_name}/video/upload/l_intro_image,fl_splice,du_3/so_0,fl_layer_apply/clip1.mp4
```

### Limitations

- URL length limit (~2000 chars) restricts number of videos
- First request triggers server-side processing (slow)
- For many videos (10+), consider using ffmpeg or dedicated video APIs

## Delete Media

```bash
TIMESTAMP=$(date +%s)
PUBLIC_ID="<your-public-id>"
SIGNATURE=$(bash -c 'echo -n "public_id=$PUBLIC_ID&timestamp=$TIMESTAMP$CLOUDINARY_API_SECRET" | sha1sum | cut -d" " -f1')

# Delete image
curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/image/destroy" -F "public_id=$PUBLIC_ID" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"

# Delete video
curl -X POST "https://api.cloudinary.com/v1_1/<your-cloud-name>/video/destroy" -F "public_id=$PUBLIC_ID" -F "api_key=$CLOUDINARY_API_KEY" -F "timestamp=$TIMESTAMP" -F "signature=$SIGNATURE"
```

## Free Tier Limits

- 25 credits/month
- ~25,000 transformations or ~25GB storage/bandwidth
- Sufficient for personal projects

## Guidelines

1. **Use unsigned presets** for simpler uploads when security isn't critical
2. **Signature order**: Parameters must be alphabetically sorted when generating signature
3. **Auto optimization**: Add `f_auto,q_auto` to URLs for automatic format/quality
4. **Folders**: Use `public_id="folder/subfolder/name"` to organize media
5. **Video concatenation**: Keep URLs short; for 10+ videos use external tools

## API Reference

- Image Upload: https://cloudinary.com/documentation/image_upload_api_reference
- Video Upload: https://cloudinary.com/documentation/video_upload_api_reference
- Video Concatenation: https://cloudinary.com/documentation/video_trimming_and_concatenating
- Console: https://console.cloudinary.com/
- Transformation Reference: https://cloudinary.com/documentation/transformation_reference

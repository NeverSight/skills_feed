---
name: media-generation
description: Generate AI videos using varg SDK. Use for videos, animations, talking characters, slideshows, social content. JSX-based - describe scenes, render videos.
---

# varg sdk - declarative ai video orchestration

jsx-based ai video generation. describe scenes declaratively, render videos automatically.

## what is this?

varg sdk is a **declarative video orchestration framework**. instead of manually calling apis, stitching clips, and managing async workflows, you describe what you want in jsx and the runtime handles:

- parallel generation of images/videos/audio
- automatic caching (re-renders reuse cached assets)
- ffmpeg composition under the hood
- provider abstraction (fal, elevenlabs, replicate)

think of it like react for video - you declare the structure, the engine figures out the execution.

## terminology

| term | meaning |
|------|---------|
| **Render** | root container - sets dimensions (1080x1920 for tiktok, 1920x1080 for youtube) |
| **Clip** | timeline segment with duration, contains visual/audio layers |
| **Image** | static image - generated from prompt or loaded from file |
| **Video** | video clip - text-to-video OR image-to-video animation |
| **Music** | background audio - generated from prompt or loaded from file |
| **Speech** | text-to-speech with voice selection |
| **Title/Subtitle** | text overlays with positioning |
| **Captions** | auto-generated captions from Speech element |
| **Grid** | layout helper for multi-image/video grids |

## core concepts

```tsx
<Render width={1080} height={1920}>  {/* tiktok dimensions */}
  <Music prompt="upbeat electronic" duration={10} />
  
  <Clip duration={3}>
    <Image prompt="cyberpunk cityscape" />
    <Title position="bottom">Welcome</Title>
  </Clip>
  
  <Clip duration={5}>
    <Video prompt="camera flies through neon streets" />
  </Clip>
</Render>
```

**no imports needed** - the render runtime auto-imports all components (`Render`, `Clip`, `Video`, `Image`, `Music`, `Speech`, `Title`, `Grid`, etc.) and providers (`fal`, `elevenlabs`). just write jsx and export default.

## Video component

`Video` handles both text-to-video and image-to-video:

```tsx
// text-to-video - generate from scratch
<Video prompt="cat playing piano in a jazz club" />

// image-to-video - animate an image with motion description
<Video 
  prompt={{
    text: "eyes widen, head tilts forward, subtle smile forming",
    images: [<Image prompt="portrait of woman" />]
  }}
/>
```

## character consistency

generate an image first, pass it to Video/Animate for consistent characters across scenes:

```tsx
const hero = <Image prompt="warrior princess, crimson hair, emerald eyes" />;

<Clip><Video image={hero} prompt="she draws her sword" /></Clip>
<Clip><Video image={hero} prompt="she leaps into battle" /></Clip>
```

for reference-based generation (keeping a real person's likeness):

```tsx
<Image 
  prompt={{ 
    text: "same person, different scene", 
    images: ["https://reference-photo.jpg"] 
  }}
  model={fal.imageModel("nano-banana-pro/edit")}
/>
```

## prompting guide (CRITICAL)

**detailed prompts = better results.** wan 2.5 video model responds dramatically better to rich, structured prompts. vague prompts produce generic, low-quality output.

### the 4-dimensional formula

every video prompt should include these dimensions:

```
[Subject Description] + [Scene Description] + [Motion/Action] + [Cinematic Controls]
```

### subject description
describe the main focus with rich detail:
- appearance, clothing, features, posture
- materials, textures, colors
- emotional state, expression

**bad:** `"a woman"`
**good:** `"a young woman with shoulder-length auburn hair, wearing a worn leather jacket over a white t-shirt, her green eyes reflecting determination, jaw set with quiet resolve"`

### scene description
layer the environment details:
- location, background, foreground
- lighting type (soft light, hard light, edge light, top light)
- time period (golden hour, daytime, night, moonlight)
- atmosphere (warm tones, low saturation, high contrast)

**bad:** `"in a city"`
**good:** `"on a rain-slicked tokyo street at night, neon signs reflecting pink and blue on wet pavement, steam rising from a nearby food stall, warm yellow light spilling from a ramen shop window"`

### motion/action description
specify movement with intensity and manner:
- amplitude (small movements, large movements)
- rate (slowly, quickly, explosively)
- effects (breaking glass, hair flowing, dust particles)

**bad:** `"walking"`
**good:** `"walking slowly through the crowd, shoulders hunched against the rain, one hand raised to shield her eyes, water droplets catching the neon light as they fall from her fingertips"`

### cinematic controls
use film language for professional results:

**camera movements:**
- `camera push-in` / `camera pull-out`
- `tracking shot` / `dolly shot`
- `pan left/right` / `tilt up/down`
- `static camera` / `fixed camera`
- `handheld` / `steadicam`

**shot types:**
- `extreme close-up` / `close-up` / `medium close-up`
- `medium shot` / `medium wide shot`
- `wide shot` / `extreme wide shot`
- `over-the-shoulder shot`

**composition:**
- `center composition` / `rule of thirds`
- `left-side composition` / `right-side composition`
- `symmetrical composition`
- `low angle` / `high angle` / `eye-level`

**lighting keywords:**
- `soft light` / `hard light` / `edge light`
- `rim light` / `backlight` / `side light`
- `golden hour` / `blue hour` / `moonlight`
- `practical light` / `mixed light`

### style keywords
add visual style for artistic direction:
- `cinematic` / `film grain` / `anamorphic`
- `cyberpunk` / `noir` / `post-apocalyptic`
- `ghibli style` / `anime` / `photorealistic`
- `vintage` / `retro` / `futuristic`
- `tilt-shift photography` / `time-lapse`

### audio/dialogue (for videos with speech)
wan 2.5 supports native audio generation:
- format dialogue: `Character says: "Your line here."`
- keep lines short (under 10 words per 5-second clip) for best lip-sync
- specify delivery tone: `"speaking quietly"`, `"calling out over wind"`
- for silence: include `"no dialogue"` or `"actors not speaking"`

### image-to-video prompts
when using reference images, focus on motion + camera:
- the image already defines subject/scene/style
- describe dynamics: `"running forward, hair flowing behind"`
- add camera movement: `"slow push-in on face"`
- control intensity: `"subtle movement"` vs `"dramatic action"`

### example: detailed prompt

**bad prompt (vague):**
```tsx
<Video prompt="a warrior fighting" />
```

**good prompt (detailed):**
```tsx
<Video prompt="medium close-up, side light, golden hour. a battle-hardened samurai with a weathered face and grey-streaked topknot, wearing damaged traditional armor with visible scratches and dents. he raises his katana in a fluid motion, blade catching the dying sunlight, muscles tensing as he shifts into fighting stance. dust particles float in the amber light, his breath visible in the cold air. slow camera push-in on his focused expression, eyes narrowed with lethal intent. cinematic, film grain, anamorphic lens flare." />
```

## example 1: cinematic character video

consistent character across multiple dramatic scenes with epic music.

**warrior-princess.tsx** (complete file - no imports needed):
```tsx
// Warrior Princess - Cinematic Character Video
// run: bunx vargai@latest render warrior-princess.tsx --verbose

const hero = (
  <Image prompt="portrait, soft light, center composition. warrior princess with flowing crimson hair reaching past her shoulders, piercing emerald eyes reflecting inner fire, wearing battle-worn silver armor with intricate celtic knot engravings, a thin scar across her left cheek from an old battle, expression of quiet determination mixed with weariness. ghibli style, painterly brushstrokes, warm color palette with golden undertones" />
);

export default (
  <Render width={1080} height={1920}>
    <Clip duration={4}>
      <Video 
        image={hero} 
        prompt="wide shot, golden hour, dramatic edge lighting from behind. she stands at the edge of a windswept cliff overlooking a vast misty valley with ancient ruins below, her crimson hair and tattered cape billowing dramatically in the wind, one hand resting on sword hilt at her side. slow camera pull-out revealing the epic landscape, dust particles catching the amber sunlight. cinematic, ghibli style, film grain, anamorphic lens" 
      />
    </Clip>
    <Clip duration={3}>
      <Video 
        image={hero} 
        prompt="medium close-up, dramatic side lighting with hard shadows. she draws her sword in one fluid motion, blade singing as it leaves the scabbard, polished steel catching the dying sunlight with a bright gleam. her eyes narrow with fierce focus, jaw set with lethal intent. camera tracks the sword movement upward. cinematic, ghibli style, shallow depth of field" 
      />
    </Clip>
    <Clip duration={3}>
      <Video 
        image={hero} 
        prompt="extreme close-up on her face, rim light from behind creating a golden halo effect. a single tear rolls down her scarred cheek as she whispers a prayer, eyes closed in concentration, lips barely moving. subtle camera push-in, dust motes floating in the light. emotional, ghibli style, soft focus on background" 
      />
    </Clip>
    <Music prompt="epic orchestral score, soaring strings building tension, triumphant french horns, taiko drums in the distance, celtic flute melody, building from quiet contemplation to heroic crescendo" duration={12} />
  </Render>
);
```

## example 2: tiktok product video with talking head

animated influencer character with speech, captions, and background music.

**skincare-promo.tsx** (complete file - no imports needed):
```tsx
// Skincare Product TikTok - Talking Head with Captions
// run: bunx vargai@latest render skincare-promo.tsx --verbose

const influencer = (
  <Image 
    prompt={{ 
      text: "extreme close-up face shot, ring light reflection in eyes, surprised expression with wide eyes and raised eyebrows, mouth slightly open in excitement, looking directly at camera. young woman with short platinum blonde hair, minimal makeup, silver hoop earrings, wearing oversized vintage band t-shirt. clean white background, professional studio lighting, tiktok creator aesthetic",
      images: ["https://reference-photo-url.jpg"]  // optional: reference for likeness
    }}
    model={fal.imageModel("nano-banana-pro/edit")}
    aspectRatio="9:16"
  />
);

const speech = (
  <Speech voice="bella" model={elevenlabs.speechModel("turbo")}>
    Oh my god you guys, I literally cannot believe this actually works! I've been using this for like two weeks and my skin has never looked better. Link in bio, seriously go get it!
  </Speech>
);

export default (
  <Render width={1080} height={1920}>
    <Music 
      prompt="upbeat electronic pop, energetic female vocal chops, modern tiktok trending sound, catchy synth melody, punchy drums, high energy throughout" 
      duration={12} 
      volume={0.4}
    />
    
    <Clip duration={3}>
      <Video 
        prompt={{
          text: "eyes widen dramatically in genuine surprise, eyebrows shoot up, mouth opens into excited smile, subtle forward lean toward camera as if sharing a secret. natural blinking, authentic micro-expressions",
          images: [influencer]
        }}
        model={fal.videoModel("wan-2.5")}
      />
      {speech}
    </Clip>
    
    <Clip duration={4}>
      <Video 
        prompt="product shot: sleek skincare bottle rotating slowly on marble surface, soft key light from above, pink and gold gradient background, light rays catching the glass, water droplets on bottle suggesting freshness. smooth 360 rotation, professional product photography, beauty commercial aesthetic"
        model={fal.videoModel("kling-v2.5")}
      />
      <Title position="bottom" color="#ffffff">LINK IN BIO</Title>
    </Clip>
    
    <Clip duration={3}>
      <Video 
        prompt={{
          text: "enthusiastic nodding while speaking, hands come into frame gesturing excitedly, genuine smile reaching her eyes, occasional hair flip, pointing at camera on 'go get it'",
          images: [influencer]
        }}
        model={fal.videoModel("wan-2.5")}
      />
    </Clip>
    
    <Captions src={speech} style="tiktok" activeColor="#ff00ff" />
  </Render>
);
```

## example 3: multi-scene video grid with elements

4-panel nature video grid showcasing different elements.

**four-elements.tsx** (complete file - no imports needed):
```tsx
// Four Elements - 2x2 Video Grid
// run: bunx vargai@latest render four-elements.tsx --verbose

export default (
  <Render width={1920} height={1080}>
    <Clip duration={6}>
      <Grid columns={2}>
        <Video 
          prompt="extreme close-up of ocean wave crashing against volcanic black rocks, slow motion 120fps, crystal clear turquoise water exploding into white foam spray, individual water droplets suspended in golden hour sunlight, mist rising. cinematic, national geographic style, shallow depth of field on water texture"
          model={fal.videoModel("wan-2.5")}
        />
        <Video 
          prompt="intimate close-up of flames dancing in stone fireplace, warm orange and yellow tongues of fire licking weathered logs, glowing embers pulsing beneath, sparks occasionally rising. cozy cabin atmosphere, soft crackling implied, shallow focus on flame tips, hygge aesthetic"
          model={fal.videoModel("wan-2.5")}
        />
        <Video 
          prompt="macro shot of rain droplets hitting window glass, each drop creating expanding ripples and trails, city lights blurred into colorful bokeh beyond the glass, melancholic blue hour lighting. asmr visual aesthetic, slow motion, focus pulling between drops"
          model={fal.videoModel("wan-2.5")}
        />
        <Video 
          prompt="timelapse of cumulus clouds drifting across deep blue sky, dramatic god rays breaking through cloud gaps, cloud shadows moving across distant mountain range. epic landscape, wide angle, peaceful meditative mood, nature documentary cinematography"
          model={fal.videoModel("wan-2.5")}
        />
      </Grid>
      <Title position="bottom" color="#ffffff">THE FOUR ELEMENTS</Title>
    </Clip>
    
    <Music prompt="ambient electronic, peaceful synthesizer pads, gentle nature sounds mixed in, meditative atmosphere, spa music vibes but more cinematic, slow build with subtle percussion" duration={8} />
  </Render>
);
```

## render

### preview first (recommended workflow)

use `--preview` to generate only images/thumbnails without rendering full videos. this is faster and cheaper for iteration:

```bash
bunx vargai@latest render video.tsx --preview --verbose
```

once you're happy with the preview frames, render the full video:

```bash
bunx vargai@latest render video.tsx --verbose
```

### open the result

after rendering, open the video with the system default player:

```bash
open output/video.mp4
```

## setup

requires api keys in `.env`:
- `FAL_KEY` - image/video generation (https://fal.ai/dashboard/keys)
- `ELEVENLABS_API_KEY` - music/voice (https://elevenlabs.io/app/settings/api-keys)

## available models

```tsx
// image generation
fal.imageModel("flux-schnell")        // fast, good quality
fal.imageModel("flux-pro")            // highest quality
fal.imageModel("nano-banana-pro/edit") // reference-based (character consistency)

// video generation
fal.videoModel("wan-2.5")             // balanced speed/quality
fal.videoModel("kling-v2.5")          // highest quality, 10s max
fal.videoModel("sync-v2")             // lipsync

// audio
elevenlabs.speechModel("turbo")       // fast TTS
elevenlabs.musicModel()               // music generation
```

## key props reference

| component | key props |
|-----------|-----------|
| `<Render>` | `width`, `height`, `fps` |
| `<Clip>` | `duration`, `transition={{ name: "fade", duration: 0.5 }}` |
| `<Image>` | `prompt`, `src`, `model`, `aspectRatio`, `resize`, `zoom` |
| `<Video>` | `prompt`, `src`, `model`, `duration`, `cutFrom`, `cutTo` |
| `<Music>` | `prompt`, `src`, `model`, `duration`, `volume`, `loop` |
| `<Speech>` | `voice`, `model`, `volume`, children=text |
| `<Title>` | `position`, `color`, children=text |
| `<Captions>` | `src` (Speech element), `style` ("tiktok"/"karaoke") |
| `<Grid>` | `columns`, `rows`, children=Image/Video array |

## about varg.ai

varg is a generative ai video platform. the sdk uses declarative jsx to compose video scenes with ai-generated images, animations, and audio. key features:
- automatic caching (regenerating uses cached assets)
- parallel generation (clips render concurrently)  
- character consistency via image references
- provider-agnostic (fal, replicate, elevenlabs under the hood)
- ffmpeg-based composition for professional output

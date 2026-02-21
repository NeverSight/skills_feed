---
name: pw-higgsfield
description: higgsfield ai image/video generation using pw protocol wrappers. trigger when user wants to generate images or videos.
---

# higgsfield ai

generate images and videos with higgsfield ai using `pw` and `higgsfield.nu`.

## setup

requires cdp connection to your browser with an active higgsfield session:

```bash
pw exec connect --input '{"launch":true}'
pw exec navigate --input '{"url":"https://higgsfield.ai"}'
```

## invocation

```nu
use pw.nu
use higgsfield.nu *
```

## generation

`higgsfield create-image` generate image.
* `--model (-m)`: default `nano_banana_2`.
* `--wait-for-result (-w)`: wait for completion.
* `--spend`: allow credit usage.

`higgsfield create-video` generate video.
* `--model (-m)`: default `wan_2_6`.
* `--wait-for-result (-w)`: wait for completion (5min timeout).
* `--spend`: allow credit usage.

## unlimited mode

commands auto-check/enable "unlimited" toggle. use `--spend` if unlimited unavailable.

see [higgsfield.md](higgsfield.md) for full reference.

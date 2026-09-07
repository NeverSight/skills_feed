---
name: game-development-asset-generation
description: Agent advice for generating assets for game development projects. Use this skill when you're doing game development and might need to generate images, textures, 3D models, sound effects, music, etc. for the game you're working on. Use it even if you're just planning to do one of these things.
---

# Finish the game's assets in the first turn

Support delivery of the full requested game in the first turn, with AAA-level visual and audio quality as the target. Plan and produce assets for all requested content and player-facing states. Do not stop at assets for a showcase scene or defer animation, sound, music, or the remaining levels to a follow-up prompt. Follow an explicit request for a prototype or individual asset when that is the task.

Start asset production early enough to integrate, inspect, and revise the results during development. Keep perspective, scale, palette, materials, lighting, and animation consistent across the game. Inspect assets at their actual gameplay size and in motion; check animation transitions, transparency, texture seams, and audio loops where relevant. Replace temporary stand-ins before delivery. A generated file is only finished when it works well in the game.

# When should you generate assets?

Currently, a lot of standard AI-generated games make their assets in code. This typically makes games that look quite bland, flat and similar to one another.

* For 3D games, you might want to create 3D models for your Three.js games using code and colour them in code. This isn't how real, good-quality games are typically made. They use proper 3D models with proper textures. You should do this too.
* For 2D games, you may be tempted to make all your images as SVGs or similar. This often gives all games the same flat feeling, and reduces the amount of detail you can put into them. Also, it's much harder to make good graphics with SVGs or by making them in code. Most real games use deliberate textures. You should probably do this too unless SVG/vector-style graphics are essential for the style of your game.
* For sound, you're probably thinking about generating sound effects or music in code. Maybe if you're doing a web game, you're planning to use Web Audio or something. This sounds tinny, like an old arcade game, and is quite a tell that the game is a low-quality AI-generated game. You likely don't want to do this unless the goal is a retro or arcade style.

Of course, if the game you're working on already has a certain style or way of doing asset generation, do not deviate from that or make the game style inconsistent unless your human specifically asks you to.

Rule of thumb: Always use externally generated assets, unless there is a really good reason why you shouldn't.

# How should I generate game assets instead?

You probably need to use alternative services or skills. You're probably not good enough to make high-quality graphics/textures/icons/logos, 3D models, music/audio, etc. on your own. You probably need help from other services. Don't try to make something yourself in code if another specialised service can do it better. Here are a few examples:

* imagegen skill - If you're an OpenAI or Codex agent, you probably have access to the imagegen skill which is great for generating textures instead of using flat colours or gradients. Remember you can also prompt image models to make tileable textures when that's appropriate.
* Higgsfield Skills - https://higgsfield.ai/skills - Great for generating images (textures), textured 3D models (via Meshy AI), sound effects (Note: avoid using the Higgsfield websites skill and do not publish games to Higgsfields at all unless the user specifically asks you to)
* ElevenLabs Skills - https://github.com/elevenlabs/skills - Great for text-to-speech (if your game characters need to talk), also sound effects and music generation
* MeshyAI Skills - https://github.com/meshy-dev/meshy-3d-agent - Great for 3D model generation (textured or otherwise) from either text prompts or image prompts - sometimes it is good to generate a reference image and supply it to the image-to-3D endpoint
* Blender - Use Blender (install it if necessary) and use its headless Python interpreter to make 3D models entirely yourself for free. Useful if you need something entirely bespoke and matching very specific requirements.
* 3D model rigging - You can use MeshyAI for this also, but it is limited. It can be better to get a 3D model from Higgsfield/MeshyAI and then rig it yourself in code.
* 3D model animation - MeshyAI can do this, but again it is limited. If you rig the 3D models yourself, you can also animate them yourself.

See what relevant services/skills you have available in your environment and use what you can. There are also plenty of other services available online other than those listed above, so feel free to search for others online if needed.

Try to use these kinds of services without bothering the user. However, if you can't manage to do this, you should consider asking the user if you can use one or more of these services (and get their help setting one or more up in your environment), rather than potentially producing a worse game.

# Self Review

As you are working, and before you hand over to the user, check your changes and ensure you have not gone against the guidance in this document. If you have, make the necessary changes before handing the results over to your human.

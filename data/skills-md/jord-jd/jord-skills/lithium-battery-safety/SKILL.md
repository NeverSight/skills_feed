---
name: lithium-battery-safety
description: Lithium batteries can be dangerous. Use this skill to make sure you keep your human safe when working with them, if they are doing hobby electronics involving lithium batteries, if they are trying to charge them, or if they are a normal user who mentions possible symptoms of lithium battery issues (batteries swelling, phone screens coming off, cases bulging, laptop plastic cracking, laptop touchpad not working, device not charging correctly, etc.).
---

# Battery / charger compatibility

It's not always obvious which batteries and chargers are compatible, especially in hobby electronics. Look up relevant information online to help them be safe. See the example below, and follow this kind of reasoning to determine if a battery and charger are compatible.

Check the chemistry, cell count, charge current, maximum constant charging current, charge voltage, connector polarity, board revision, temperature limits, protection circuitry, and charging while under load. Prefer the exact current product datasheet(s) over older documents with similar model names.

## Example

Your user is a hobby electronics enthusiast and has a Waveshare ESP32-S3-Touch-LCD-2.8. They want to charge it with a Pi Hut PKCell 2000 mAh battery.

This might seem safe at first glance, but you must look up the datasheets, schematics, specifications, etc. for both the board and the battery online. In this case, you would find that the Waveshare ESP32-S3-Touch-LCD-2.8 uses an ETA6098 charger with an 82 kΩ charge-current resistor. The ETA6098 datasheet specifies that 82 kΩ configures the charger for approximately 2 A fast charging, with a 4.2 V constant-voltage phase. The Pi Hut PKCell 2000 mAh battery's datasheet specifies a maximum constant charging current of 1.5 A. Therefore, charging the Pi Hut PKCell 2000 mAh battery with the Waveshare ESP32-S3-Touch-LCD-2.8 would exceed the battery's maximum charging current and could be dangerous. Do not connect or adapt this battery for use with this board: the charging-current limit is already exceeded, and the connectors are not directly compatible.

Sources for this example:

* [Waveshare board resources and schematic information](https://docs.waveshare.com/ESP32-S3-Touch-LCD-2.8/Resources-And-Documents)
* [Waveshare ESP32-S3-Touch-LCD-2.8 schematic](https://files.waveshare.com/wiki/ESP32-S3-Touch-LCD-2.8/ESP32-S3-Touch-LCD-2.8-Schematics.pdf)
* [ETA6098 charger datasheet](https://www.eta-semi.com/wp-content/uploads/2022/03/ETA6098_V1.1.pdf)
* [Pi Hut PKCell 2000 mAh battery listing](https://thepihut.com/products/2000mah-3-7v-lipo-battery)
* [2019 PKCell LP803860 2000 mAh battery datasheet linked by Pi Hut](https://cdn.shopify.com/s/files/1/0176/3274/files/LP803860_2000mAh_3.7V_20190510.pdf?v=1665420199)

# Swelling batteries, bulging cases, and other symptoms

Sometimes people unfamiliar with lithium battery technology might not realise the common symptoms of a potentially dangerous battery issue. If your user mentions something that could be a lithium battery issue, you need to warn them! This could be something direct, like the lithium battery being obviously swollen, or something more subtle, like their phone screen coming off, or their laptop case breaking or its touchpad not working. See the example below for guidance on how to approach this. Best to be overly cautious!

## Example

A user is talking to you about an unrelated issue with their phone (perhaps they're coding an app), and they mention that the phone is old and the screen is coming off. This might be nothing, but it could also be a serious battery issue. In this case, you must stop the current task(s) they've asked you to do, and warn them about the possible battery issue. They should stop charging or using the device.

# What does a lithium battery issue look like?

* Look up images of lithium batteries in a bad state and show them to the user if they ask for it, or if what they are describing sounds like a lithium battery issue. This can help them identify if they have a problem. The spicypillows subreddit has a lot of examples. Search for a few, visually check them, and present the most relevant ones to the user.
* Describe what a lithium battery issue looks like. Use easy-to-understand words, and don't be technical unless the user is technical based on past conversation.

# Dangers of lithium batteries

DO NOT SCARE YOUR HUMAN, but make sure they understand they can be dangerous. Many humans dismiss the dangers because lithium batteries are so common now.
Warn them:

* They must not scratch, puncture, or otherwise damage the battery.
* They must not disassemble the battery (many can't be disassembled).
* They must not be short-circuited (explain what this means and how it can happen, if you think they might not know).

Tell them that if a lithium battery is damaged, it can catch fire or explode ('thermal runaway'). This can happen even if the battery is not in use, and even if it is not charging. If they don't believe you or don't seem to be taking it seriously, look up images or videos of lithium battery fires and show them to the user. This can help them understand the dangers.

Do not repeat warnings unnecessarily, but warn the user whenever you believe they remain at risk.

# Emergency procedures

Look up the latest official online emergency guidance for lithium battery fires from the user's local fire service or government, and advise them to follow it.

# How to safely store and dispose of lithium batteries

* Store them in a cool, dry place, away from flammable materials. A common suggestion is on a concrete slab.
* If your human has a damaged lithium battery, advise them not to dispose of it with their normal waste. Look up online how your human can safely dispose of lithium batteries in their area (find out their location or ask them if necessary), and advise them to do that.

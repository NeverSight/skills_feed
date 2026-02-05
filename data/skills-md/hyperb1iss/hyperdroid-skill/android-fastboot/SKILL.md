---
name: android-fastboot
description: Use for fastboot operations, flashing partitions, bootloader unlocking, recovery mode, or partition management. Triggers on "fastboot", "flash boot.img", "unlock bootloader", "recovery mode", "TWRP", "Magisk", "partition", "sideload", "A/B slots". WARNING - These operations can brick devices if done incorrectly.
---

# Android Fastboot Operations

⚠️ **DANGER ZONE** - Fastboot operations write directly to device partitions. Wrong images or interrupted operations can brick devices. Always verify:

1. Correct device (check `fastboot getvar product`)
2. Correct images for exact device model
3. Bootloader is unlocked (for flashing)
4. Battery > 50%

---

## Entering Fastboot Mode

```bash
# From ADB (device running)
adb reboot bootloader

# Hardware buttons (most devices)
# Power + Volume Down (hold until fastboot screen)
```

## Basic Commands

```bash
fastboot devices                    # List connected devices
fastboot getvar all                 # All device variables
fastboot reboot                     # Reboot to system
fastboot reboot bootloader          # Stay in bootloader
fastboot reboot recovery            # Boot to recovery
fastboot reboot fastboot            # Boot to fastbootd (Android 10+)
```

## Check Before Flashing

```bash
# ALWAYS run these first
fastboot devices                    # Verify connection
fastboot getvar product             # Verify device model
fastboot getvar unlocked            # Must be "yes" for flashing
fastboot getvar current-slot        # Know current A/B slot
fastboot getvar battery-level       # Should be > 50
```

---

## Bootloader Unlocking

### Google Pixel

```bash
# 1. Enable OEM unlocking in Developer Options
# 2. Boot to fastboot
adb reboot bootloader

# 3. Unlock
fastboot flashing unlock

# 4. Confirm on device with volume keys + power
# WARNING: This wipes all data!
```

### Other Manufacturers

| Brand    | Process                                                 |
| -------- | ------------------------------------------------------- |
| OnePlus  | `fastboot oem unlock`                                   |
| Xiaomi   | Mi Unlock Tool (waiting period)                         |
| Samsung  | Uses Odin, not fastboot                                 |
| Motorola | Request code from website, `fastboot oem unlock <code>` |
| Sony     | Request code from website                               |

### Check Unlock Status

```bash
fastboot getvar unlocked            # yes/no
fastboot getvar device-state        # locked/unlocked
fastboot getvar unlock_ability      # Can be unlocked?
```

---

## Flashing Partitions

### Individual Partitions

```bash
fastboot flash boot boot.img
fastboot flash recovery recovery.img      # Non-A/B only
fastboot flash dtbo dtbo.img
fastboot flash vbmeta vbmeta.img

# Disable verification (for custom ROMs)
fastboot flash --disable-verity --disable-verification vbmeta vbmeta.img
```

### Bootloader & Radio (Extra Careful!)

```bash
# These can hard-brick if wrong!
fastboot flash bootloader bootloader.img
fastboot reboot bootloader    # REQUIRED after bootloader flash

fastboot flash radio radio.img
fastboot reboot bootloader    # Recommended after radio flash
```

### Temporary Boot (No Flash)

```bash
# Test before committing - reboots to normal after restart
fastboot boot recovery.img
fastboot boot patched_boot.img
```

---

## A/B Slot Devices

Modern devices have two copies of each partition (A and B).

```bash
# Check current slot
fastboot getvar current-slot        # Returns: a or b

# Set active slot
fastboot set_active a
fastboot set_active b

# Flash to specific slot
fastboot flash boot_a boot.img
fastboot flash boot_b boot.img

# Flash to both slots
fastboot --slot=all flash boot boot.img
```

---

## Dynamic Partitions (Android 10+)

Large partitions (system, vendor, product) live inside a "super" partition.

### Fastbootd Mode

```bash
# Enter userspace fastboot
fastboot reboot fastboot

# Check if in fastbootd
fastboot getvar is-userspace        # Should return: yes
```

### Flash Dynamic Partitions

```bash
# Must be in fastbootd mode!
fastboot reboot fastboot

fastboot flash system system.img
fastboot flash vendor vendor.img
fastboot flash product product.img
```

### Virtual A/B Snapshots

```bash
# Check snapshot status
fastboot getvar snapshot-update-status

# Cancel stuck update (CAREFUL!)
fastboot snapshot-update cancel
```

---

## Recovery Operations

### Enter Recovery

```bash
adb reboot recovery
# Or: Power + Volume Up (varies by device)
```

### ADB Sideload

```bash
# 1. In recovery, select "Apply update from ADB"
# 2. Run:
adb sideload update.zip
```

### Flash Custom Recovery (TWRP)

```bash
# Test first (temporary boot)
fastboot boot twrp.img

# If it works, flash permanently
# Non-A/B devices:
fastboot flash recovery twrp.img

# A/B devices (recovery in boot):
fastboot flash boot twrp.img
```

---

## Magisk (Root)

### Installation

```bash
# 1. Extract boot.img from your firmware
# 2. Transfer to device, patch with Magisk app
# 3. Pull patched image
adb pull /sdcard/Download/magisk_patched_*.img

# 4. Flash patched boot
fastboot flash boot magisk_patched_*.img

# 5. Reboot
fastboot reboot
```

### Useful Magisk Commands (after rooted)

```bash
adb shell su -c "magisk --version"
adb shell su -c "resetprop ro.debuggable 1"
```

---

## Factory Reset / Wipe

```bash
fastboot erase userdata             # Wipe user data
fastboot erase cache                # Wipe cache (if exists)
fastboot -w                         # Format data + cache

# Full flash with wipe
fastboot -w flashall
fastboot -w update image.zip
```

---

## Danger Levels

| Level       | Operations                                                        |
| ----------- | ----------------------------------------------------------------- |
| ✅ SAFE     | `devices`, `getvar`, `reboot`, `boot` (temp)                      |
| ⚠️ MEDIUM   | `flash boot/recovery/dtbo`, `set_active`                          |
| 🔴 HIGH     | `flash system/vendor`, `erase`, `-w`                              |
| ☠️ CRITICAL | `flash bootloader`, `flash radio`, `flashing lock` with custom OS |

---

## Brick Prevention

**Never:**

- Flash images from different device models
- Interrupt a flash operation
- Lock bootloader with custom ROM installed
- Flash bootloader/radio without matching versions

**Always:**

- Verify device with `fastboot getvar product`
- Keep stock images available for recovery
- Use `fastboot boot` to test before `fastboot flash`
- Maintain battery > 50%

---

## Recovery from Soft Brick

```bash
# 1. Enter fastboot (Power + Vol Down)
fastboot devices

# 2. Flash stock boot
fastboot flash boot boot.img

# 3. For dynamic partitions
fastboot reboot fastboot
fastboot flash system system.img
fastboot flash vendor vendor.img

# 4. Wipe if needed
fastboot -w

# 5. Reboot
fastboot reboot
```

For hard bricks (no fastboot access), you need EDL mode (Qualcomm) or manufacturer service tools.

---

## Quick Reference

| Task              | Command                        |
| ----------------- | ------------------------------ |
| Check connection  | `fastboot devices`             |
| Device info       | `fastboot getvar all`          |
| Unlock bootloader | `fastboot flashing unlock`     |
| Flash boot        | `fastboot flash boot boot.img` |
| Test recovery     | `fastboot boot twrp.img`       |
| Current slot      | `fastboot getvar current-slot` |
| Switch slot       | `fastboot set_active a`        |
| Wipe data         | `fastboot -w`                  |
| Reboot            | `fastboot reboot`              |

---
name: termux-api
description: |
  Control Android devices via Termux API over SSH. Access camera, sensors, location, notifications, SMS, clipboard, TTS, and 70+ other device APIs. Requires Termux and Termux:API installed on the Android device.
---

# Termux API Skill

Control Android devices via Termux API commands over SSH.

## Prerequisites

- Termux installed on Android device
- Termux:API app installed and permissions granted
- SSH access configured (port 8022 by default)
- `termux-api` package installed: `pkg install termux-api`

## Connection

```bash
# Default SSH connection
ssh -p 8022 <device-ip> '<termux-api-command>'
```

## Important Notes

1. **Termux must be in foreground** for camera/microphone commands
2. **Permissions must be granted** in Android Settings → Termux:API → Permissions
3. **Start API service** if commands timeout: `termux-api-start`

## API Commands Reference

### Device Info
| Command | Description |
|---------|-------------|
| `termux-battery-status` | Battery level, charging status, temperature |
| `termux-audio-info` | Audio device info |
| `termux-wifi-connectioninfo` | Current WiFi connection details |
| `termux-wifi-scaninfo` | Scan nearby WiFi networks |
| `termux-telephony-deviceinfo` | Phone/SIM info |
| `termux-telephony-cellinfo` | Cell tower info |
| `termux-sensor -l` | List available sensors |
| `termux-sensor -s <sensor> -n 1` | Read sensor once |

### Camera & Media
| Command | Description |
|---------|-------------|
| `termux-camera-info` | List cameras (id 0=back, 1=front) |
| `termux-camera-photo -c <id> <file.jpg>` | Take photo (needs foreground) |
| `termux-microphone-record -f <file>` | Record audio |
| `termux-media-player play <file>` | Play audio file |
| `termux-tts-speak "text"` | Text to speech |
| `termux-tts-engines` | List TTS engines |

### Notifications & Feedback
| Command | Description |
|---------|-------------|
| `termux-notification -t "title" -c "content"` | Show notification |
| `termux-notification-remove --id <id>` | Remove notification |
| `termux-toast "message"` | Show toast popup |
| `termux-vibrate -d <ms>` | Vibrate for duration |
| `termux-torch on/off` | Toggle flashlight |
| `termux-dialog` | Show dialog (various types) |

### Communication (needs permissions)
| Command | Description |
|---------|-------------|
| `termux-sms-list -l 10` | List recent SMS |
| `termux-sms-send -n <number> "message"` | Send SMS |
| `termux-contact-list` | List contacts |
| `termux-call-log -l 10` | Recent call history |
| `termux-telephony-call <number>` | Make phone call |

### Clipboard
| Command | Description |
|---------|-------------|
| `termux-clipboard-get` | Get clipboard content |
| `termux-clipboard-set "text"` | Set clipboard |

### Location
| Command | Description |
|---------|-------------|
| `termux-location` | Get GPS location (needs permission) |
| `termux-location -p gps` | Use GPS provider |
| `termux-location -p network` | Use network provider |

### System Control
| Command | Description |
|---------|-------------|
| `termux-volume` | Get/set volume levels |
| `termux-brightness <0-255>` | Set screen brightness |
| `termux-wallpaper -f <file>` | Set wallpaper |
| `termux-wake-lock` | Prevent sleep |
| `termux-wake-unlock` | Allow sleep |

### Storage & Sharing
| Command | Description |
|---------|-------------|
| `termux-share -a send <file>` | Share file via Android intent |
| `termux-open <file>` | Open file with default app |
| `termux-open-url <url>` | Open URL in browser |
| `termux-download <url>` | Download file |
| `termux-storage-get <dest>` | Pick file from storage |

## Common Patterns

### Take a selfie and retrieve it
```bash
# Ensure Termux is in foreground first
adb shell am start -n com.termux/.HomeActivity
# Take photo
ssh -p 8022 <ip> 'termux-camera-photo -c 1 ~/selfie.jpg'
# Retrieve via SCP
scp -P 8022 <ip>:~/selfie.jpg /local/path/
```

### Send notification with action
```bash
ssh -p 8022 <ip> 'termux-notification -t "Alert" -c "Task complete" --id myalert --vibrate 200,100,200'
```

### Get device location
```bash
ssh -p 8022 <ip> 'termux-location -p network'
# Returns JSON with latitude, longitude, accuracy
```

### Monitor battery
```bash
ssh -p 8022 <ip> 'termux-battery-status' | jq '.percentage, .status'
```

## Troubleshooting

### Command times out
1. Start API service: `termux-api-start`
2. Check if Termux:API app is installed
3. For camera/mic: ensure Termux app is in foreground

### Permission denied
1. Open Android Settings → Apps → Termux:API → Permissions
2. Grant required permissions (camera, location, SMS, etc.)

### SSH connection refused
1. In Termux: `pkg install openssh && sshd`
2. SSH runs on port 8022 by default
3. Set password with `passwd` or add SSH key to `~/.ssh/authorized_keys`

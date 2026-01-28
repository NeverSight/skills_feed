---
name: hses-protocol
description: "HSES (High Speed Ethernet Server) protocol specification for Yaskawa robot controllers. USE WHEN: understanding UDP-based communication protocol, message structure, command formats, or error codes for Yaskawa robots."
---

# HSES Protocol Specification

This skill provides the complete specification for the HSES (High Speed Ethernet Server) protocol used to communicate with Yaskawa robot controllers.

## When to Use

- Understanding HSES protocol message structure and formats
- Implementing or debugging HSES communication
- Looking up specific command IDs, attributes, or error codes
- Understanding the binary protocol layout (headers, payloads)

## Protocol Overview

HSES is a UDP-based communication protocol for Yaskawa robots.

### Communication Specifications

| Property | Value |
|----------|-------|
| Protocol | UDP |
| Robot Control Port | 10040 |
| File Control Port | 10041 |
| Endianness | Little-endian |

### Message Structure

```
+------------------+
| Header (32 bytes)|
+------------------+
| Payload (≤479B)  |
+------------------+
```

#### Header Layout (32 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0-3 | 4 | Magic | "YERC" |
| 4-5 | 2 | Header size | Always 0x20 (32) |
| 6-7 | 2 | Payload size | Variable |
| 8 | 1 | Reserved | Always 0x03 |
| 9 | 1 | Division | 0x01=Robot, 0x02=File |
| 10 | 1 | ACK | 0x00=Request, 0x01=Response |
| 11 | 1 | Request ID | Incremental session ID |
| 12-15 | 4 | Block number | See block numbering rules |
| 16-23 | 8 | Reserved | "99999999" |
| 24-31 | 8 | Sub-header | Command-specific |

#### Block Number Rules

| Context | Value |
|---------|-------|
| Request | Always 0 |
| Single response | 0x8000_0000 |
| Multi-response data (not last) | Increment from previous |
| Multi-response data (last) | Previous + 0x8000_0000 |
| ACK packet | Same as corresponding data |

#### Request Sub-header (bytes 24-31)

| Offset | Size | Field |
|--------|------|-------|
| 24-25 | 2 | Command ID |
| 26-27 | 2 | Instance |
| 28 | 1 | Attribute |
| 29 | 1 | Service |
| 30-31 | 2 | Padding (0x00) |

#### Response Sub-header (bytes 24-31)

| Offset | Size | Field |
|--------|------|-------|
| 24 | 1 | Service + 0x80 |
| 25 | 1 | Status |
| 26 | 1 | Added status size |
| 27 | 1 | Padding |
| 28-29 | 2 | Added status (error code) |
| 30-31 | 2 | Padding (0x00) |

**Response Status Values:**
- `0x00`: Normal reply
- `0x08`: Command not defined
- `0x09`: Invalid element number
- `0x1f`: Abnormal reply (check added status)
- `0x28`: Instance does not exist

## Robot Commands (Division = 0x01)

### Command Reference Table

| Command ID | Name | Description |
|------------|------|-------------|
| 0x70 | Alarm data reading | Read current alarm |
| 0x71 | Alarm history reading | Read alarm history |
| 0x72 | Status reading | Read robot status |
| 0x73 | Executing job info | Read current job info |
| 0x74 | Axis configuration | Read axis config |
| 0x75 | Position data reading | Read robot position |
| 0x76 | Position error reading | Read position error |
| 0x77 | Torque data reading | Read torque data |
| 0x78 | I/O data | Read/write I/O |
| 0x79 | Register data | Read/write registers |
| 0x7A | Byte variable (B) | 8-bit unsigned |
| 0x7B | Integer variable (I) | 16-bit signed |
| 0x7C | Double variable (D) | 32-bit signed |
| 0x7D | Real variable (R) | 32-bit float |
| 0x7E | String variable (S) | 16-byte string |
| 0x7F | Position variable (P) | Robot position |
| 0x80 | Base position (BP) | Base position |
| 0x81 | External axis (EX) | External axis |
| 0x82 | Alarm reset | Reset/cancel alarms |
| 0x83 | HOLD/Servo control | HOLD and servo ON/OFF |
| 0x84 | Cycle mode switch | Step/cycle/continuous |
| 0x85 | PP message display | Show message on pendant |
| 0x86 | Job START | Start job execution |
| 0x87 | Job select | Select job |
| 0x88 | Management time | Get management time |
| 0x89 | System information | Get system info |
| 0x8A | Move (Cartesian) | Move command |
| 0x8B | Move (Pulse) | Move command |
| 0x8C | String (S) 32-byte | 32-byte string variable |
| 0x300 | Plural I/O | Multiple I/O |
| 0x301 | Plural register | Multiple registers |
| 0x302 | Plural B variable | Multiple byte vars |
| 0x303 | Plural I variable | Multiple integer vars |
| 0x304 | Plural D variable | Multiple double vars |
| 0x305 | Plural R variable | Multiple real vars |
| 0x306 | Plural S variable | Multiple string vars |
| 0x307 | Plural P variable | Multiple position vars |
| 0x308 | Plural BP variable | Multiple base pos vars |
| 0x309 | Plural EX variable | Multiple ext axis vars |
| 0x30A | Alarm data (sub code) | Alarm with sub strings |
| 0x30B | Alarm history (sub) | History with sub strings |
| 0x30C | Plural S 32-byte | Multiple 32-byte strings |
| 0x0411 | Encoder temperature | Read encoder temp |
| 0x0413 | Converter temperature | Read converter temp |

### Service Types

| Service | Value | Description |
|---------|-------|-------------|
| Get_Attribute_Single | 0x0E | Read single attribute |
| Get_Attribute_All | 0x01 | Read all attributes |
| Set_Attribute_Single | 0x10 | Write single attribute |
| Set_Attribute_All | 0x02 | Write all attributes |

## File Commands (Division = 0x02)

File commands use Command ID = 0x00 and are distinguished by Service code.

| Service | Name | Direction | Description |
|---------|------|-----------|-------------|
| 0x09 | File delete | - | Delete file on controller |
| 0x15 | File loading | PC → FS100 | Upload file to controller |
| 0x16 | File saving | FS100 → PC | Download file from controller |
| 0x32 | File list | FS100 → PC | Get directory listing |

### File Transfer Protocol

**Downloading file from controller (File Saving, Service 0x16):**
1. Send request with filename
2. Receive file data blocks from controller
3. Send ACK for each data block
4. Continue until final block (bit 31 set in block number)

**Uploading file to controller (File Loading, Service 0x15):**
1. Send request with filename
2. Receive ACK for command acceptance
3. Send file data blocks to controller
4. Receive ACK for each data block
5. Set bit 31 on final block

## Status Data Structure

### Status Data 1 (Command 0x72, Instance 1)

| Bit | Meaning when ON |
|-----|-----------------|
| 0 | Step mode |
| 1 | One-cycle mode |
| 2 | Continuous mode |
| 3 | Running |
| 4 | Speed limited |
| 5 | Teach mode |
| 6 | Play mode |
| 7 | Remote mode |
| 8-15 | Reserved |

### Status Data 2 (Command 0x72, Instance 2)

| Bit | Meaning when ON |
|-----|-----------------|
| 0 | Hold pending |
| 1 | Hold by external |
| 2 | Hold by command |
| 3 | Servo ON (ready) |
| 4 | Error |
| 5 | Alarm |
| 6-15 | Reserved |

## Common Error Codes (Added Status)

| Code | Meaning |
|------|---------|
| 0x1010 | Cannot operate (mode/state) |
| 0x1018 | Servo not ready |
| 0x2010 | Cannot operate in teach mode |
| 0x2050 | In hold state |
| 0x2060 | System already in requested state |
| 0x3040 | Job not found |
| 0x3400 | File not found |
| 0x4040 | Invalid variable index |

## Related Skills

For implementing HSES communication in Rust, see:
- **moto-hses-usage**: Client library usage guide for the `moto-hses` crate family

## Detailed Reference

For complete protocol details including all command payloads, response formats, and example packets, see:

- [references/protocol-overview.md](references/protocol-overview.md) - Protocol structure and header format
- [references/sequence-diagrams.md](references/sequence-diagrams.md) - Communication flow diagrams
- [references/robot-commands-status.md](references/robot-commands-status.md) - Status and alarm commands
- [references/robot-commands-variables.md](references/robot-commands-variables.md) - Variable read/write commands
- [references/robot-commands-control.md](references/robot-commands-control.md) - Control and motion commands
- [references/file-commands.md](references/file-commands.md) - File operation commands
- [references/data-types.md](references/data-types.md) - Variable types and position formats
- [references/error-codes.md](references/error-codes.md) - Error code definitions

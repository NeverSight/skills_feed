---
name: error-message-explainer
description: Interprets Arduino/ESP32/RP2040 compiler errors in plain English for beginners. Use when user shares error messages, compilation failures, upload problems, or asks "what does this error mean". Covers common errors like undefined references, type mismatches, missing libraries, and board-specific issues.
---

# Error Message Explainer

Translates cryptic compiler errors into actionable fixes for Arduino/ESP32/RP2040 projects.

## Resources

This skill includes bundled tools:

- **scripts/parse_errors.py** - Automated error analysis with 20+ error patterns

## Quick Start

**Analyze error from file:**
```bash
uv run --no-project scripts/parse_errors.py --file error_log.txt
```

**Analyze single error:**
```bash
uv run --no-project scripts/parse_errors.py --message "error: 'LED' was not declared in this scope"
```

**Interactive mode:**
```bash
uv run --no-project scripts/parse_errors.py --interactive
```

**Pipe from compiler:**
```bash
arduino-cli compile 2>&1 | uv run --no-project scripts/parse_errors.py --stdin
```

## How to Use This Skill

When user pastes an error message:
1. Identify the error type from patterns below
2. Explain what it means in simple terms
3. Show the specific fix with code example
4. Explain WHY this error happens (educational value)

## Common Compilation Errors

### 1. "'xyz' was not declared in this scope"
```
error: 'xyz' was not declared in this scope
```

**Meaning:** Compiler doesn't recognize the name `xyz`.

**Common Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| Typo in variable/function name | Check spelling, C++ is case-sensitive! |
| Variable used before declaration | Move declaration before first use |
| Missing `#include` | Add required library header |
| Function defined after it's called | Add forward declaration or move function up |

**Example - Typo:**
```cpp
// WRONG
int ledpin = 13;      // lowercase 'p'
digitalWrite(ledPin, HIGH);  // uppercase 'P' - DIFFERENT!

// CORRECT
int ledPin = 13;
digitalWrite(ledPin, HIGH);
```

**Example - Missing Include:**
```cpp
// WRONG - Servo not defined!
Servo myServo;

// CORRECT
#include <Servo.h>
Servo myServo;
```

---

### 2. "expected ';' before..."
```
error: expected ';' before 'xyz'
```

**Meaning:** Missing semicolon on the previous line.

**Fix:** Add `;` at end of the line ABOVE the error.

```cpp
// WRONG - error points to line 3
int x = 5       // ← missing ; here!
int y = 10;

// CORRECT
int x = 5;
int y = 10;
```

**Pro Tip:** The error line number is where compiler noticed the problem, not where the missing `;` is!

---

### 3. "expected ')' before..." or "expected '}' before..."
```
error: expected ')' before ';'
error: expected '}' at end of input
```

**Meaning:** Mismatched parentheses or braces.

**Common Patterns:**
```cpp
// WRONG - unmatched parenthesis
if (x > 5 {  // missing )
}

// WRONG - unmatched brace
void setup() {
    Serial.begin(115200);
// missing closing }

// CORRECT
if (x > 5) {
}

void setup() {
    Serial.begin(115200);
}
```

**Debugging Tip:** Use IDE auto-format (Ctrl+T) to reveal mismatches.

---

### 4. "invalid conversion from 'const char*' to 'char*'"
```
error: invalid conversion from 'const char*' to 'char*'
```

**Meaning:** Trying to modify a string literal (which is read-only).

```cpp
// WRONG
char* message = "Hello";  // string literals are const!
message[0] = 'h';         // can't modify!

// CORRECT (if you need to modify)
char message[] = "Hello"; // creates modifiable copy
message[0] = 'h';         // OK!

// CORRECT (if read-only is fine)
const char* message = "Hello";
```

---

### 5. "no matching function for call to..."
```
error: no matching function for call to 'SomeClass::method(int, int, int)'
note: candidate: void SomeClass::method(int, int)
```

**Meaning:** Function called with wrong number or type of arguments.

```cpp
// WRONG - too many arguments
myServo.write(90, 100);  // write() takes only 1 argument!

// CORRECT
myServo.write(90);
```

**Read the "note:" lines** - they show what arguments ARE accepted.

---

### 6. "multiple definition of 'xyz'"
```
error: multiple definition of 'xyz'
```

**Meaning:** Same variable/function defined in multiple files.

**Fixes:**
```cpp
// In header file (.h), use 'extern':
extern int globalVar;  // declaration only

// In ONE .cpp file, define it:
int globalVar = 0;     // actual definition
```

Or for functions in header:
```cpp
// WRONG - defined in header, included multiple times
int add(int a, int b) { return a + b; }

// CORRECT - use 'inline'
inline int add(int a, int b) { return a + b; }
```

---

### 7. "'xyz' does not name a type"
```
error: 'WiFiClient' does not name a type
```

**Meaning:** Class/type not recognized.

**Fixes:**
| Board | Library | Include |
|-------|---------|---------|
| ESP32 | WiFi | `#include <WiFi.h>` |
| ESP8266 | WiFi | `#include <ESP8266WiFi.h>` |
| Arduino + WiFi Shield | WiFi | `#include <WiFi.h>` |

```cpp
// WRONG
WiFiClient client;  // WiFiClient unknown!

// CORRECT for ESP32
#include <WiFi.h>
WiFiClient client;
```

---

### 8. "redefinition of 'xyz'"
```
error: redefinition of 'int x'
```

**Meaning:** Variable declared twice in same scope.

```cpp
// WRONG
int count = 0;
int count = 0;  // redefinition!

// WRONG in loops
for (int i = 0; i < 10; i++) {
    int i = 5;  // shadows loop variable!
}

// CORRECT
int count = 0;  // declare once
count = 5;      // assign without 'int'
```

---

## Upload Errors

### 9. "avrdude: stk500_recv(): programmer is not responding"
```
avrdude: stk500_recv(): programmer is not responding
avrdude: stk500_getsync() attempt X of 10: not in sync
```

**Meaning:** Arduino IDE can't communicate with the board.

**Fixes (try in order):**
1. ✅ Correct board selected? (Tools → Board)
2. ✅ Correct port selected? (Tools → Port)
3. ✅ USB cable is data cable (not charge-only)?
4. ✅ Try different USB port
5. ✅ Nothing connected to pins 0/1 (TX/RX)?
6. ✅ Press reset button during upload
7. ✅ Install/reinstall USB drivers

---

### 10. "A fatal error occurred: Failed to connect to ESP32"
```
A fatal error occurred: Failed to connect to ESP32: 
Timed out waiting for packet header
```

**Meaning:** ESP32 not entering bootloader mode.

**Fix:** Hold BOOT button while uploading:
1. Click Upload in IDE
2. When "Connecting..." appears, hold BOOT button
3. Release when upload starts
4. Some boards: hold BOOT, press EN/RST, release BOOT

---

### 11. "Sketch too big"
```
Sketch too big; see https://support.arduino.cc/...
Sketch uses 34816 bytes (107%) of program storage space.
Maximum is 32256 bytes.
```

**Meaning:** Program doesn't fit in flash memory.

**Fixes:**
```cpp
// 1. Use F() macro for strings (saves RAM + sometimes Flash)
Serial.println(F("This string in flash"));  // instead of RAM

// 2. Remove unused libraries
// Each #include adds code even if not used

// 3. Use smaller data types
uint8_t x = 5;  // instead of int (2 bytes saved)

// 4. Choose board with more flash (ESP32 has 4MB vs Arduino's 32KB)
```

---

## Library Errors

### 12. "fatal error: xyz.h: No such file or directory"
```
fatal error: Adafruit_BME280.h: No such file or directory
```

**Meaning:** Library not installed.

**Fix:**
1. Sketch → Include Library → Manage Libraries
2. Search for library name
3. Click Install
4. If not in Library Manager: download ZIP, Sketch → Include Library → Add .ZIP Library

---

### 13. "exit status 1 / Error compiling for board..."
```
exit status 1
Error compiling for board Arduino Uno.
```

**Meaning:** Generic error - scroll UP to find the real error message.

**The actual error is ABOVE this line!** Look for lines containing `error:`.

---

## Type Errors

### 14. "cannot convert 'String' to 'const char*'"
```
error: cannot convert 'String' to 'const char*'
```

**Meaning:** Function expects C-string but got Arduino String.

```cpp
// WRONG
String myString = "hello";
someFunction(myString);  // if someFunction expects const char*

// CORRECT
String myString = "hello";
someFunction(myString.c_str());  // convert to C-string
```

---

### 15. "invalid operands to binary expression"
```
error: invalid operands of types 'const char*' and 'const char*' to binary 'operator+'
```

**Meaning:** Can't use `+` with C-strings.

```cpp
// WRONG
const char* a = "hello";
const char* b = " world";
const char* c = a + b;  // doesn't work!

// CORRECT - use String
String a = "hello";
String b = " world";
String c = a + b;  // works!

// Or use snprintf
char c[20];
snprintf(c, sizeof(c), "%s%s", a, b);
```

---

## Quick Reference Table

| Error Contains | Likely Problem | Quick Fix |
|----------------|----------------|-----------|
| "not declared" | Typo or missing include | Check spelling, add #include |
| "expected ';'" | Missing semicolon | Add ; to line ABOVE error |
| "expected ')'" | Unmatched parenthesis | Count ( and ) |
| "expected '}'" | Unmatched brace | Count { and } |
| "no matching function" | Wrong arguments | Check function signature |
| "does not name a type" | Missing library | Add #include |
| "multiple definition" | Defined in multiple files | Use extern |
| "stk500" | Upload failed | Check board/port/cable |
| "No such file" | Library not installed | Install via Library Manager |
| "too big" | Out of flash | Use F(), remove unused code |

## Debugging Strategy

```
1. Read the FIRST error (later ones often cascade)
2. Note the FILE and LINE NUMBER
3. Look at that line AND the line above
4. Check for common patterns above
5. Fix ONE error at a time, recompile
6. Repeat until clean
```

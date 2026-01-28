---
name: dbus
risk_level: MEDIUM
description: "Expert in D-Bus IPC (Inter-Process Communication) on Linux systems. Specializes in secure service communication, method calls, signal handling, and system integration. HIGH-RISK skill due to system service access and privileged operations."
model: sonnet
---

## 1. Overview

**Risk Level**: HIGH - System service access, privileged operations, IPC

You are an expert in D-Bus communication with deep expertise in:

- **D-Bus Protocol**: Message bus system, object paths, interfaces
- **Bus Types**: Session bus (user), System bus (privileged)
- **Service Interaction**: Method calls, signals, properties
- **Security**: Policy enforcement, peer credentials

### Core Expertise Areas

1. **Bus Communication**: Session/system bus, message routing
2. **Object Model**: Paths, interfaces, methods, signals
3. **Policy Enforcement**: D-Bus security policies, access control
4. **Security Controls**: Credential validation, service allowlists

---

## 2. Core Principles

1. **TDD First** - Write tests before implementation
2. **Performance Aware** - Optimize connections, caching, async calls
3. **Security First** - Validate targets, block privileged services
4. **Minimal Privilege** - Session bus by default, least access

---

## 3. Core Responsibilities

### 3.1 Safe IPC Principles

When using D-Bus:
- **Validate service targets** before method calls
- **Use session bus** unless system access required
- **Block privileged services** (PolicyKit, systemd)
- **Log all method invocations**
- **Enforce call timeouts**

### 3.2 Security-First Approach

Every D-Bus operation MUST:
1. Validate target service/interface
2. Check against blocked service list
3. Use appropriate bus type
4. Log operation details
5. Enforce timeout limits

### 3.3 Bus Type Policy

- **Session Bus**: User applications, non-privileged
- **System Bus**: System services, requires elevated permissions
- **Default**: Always prefer session bus

---

## 4. Technical Foundation

### 4.1 D-Bus Architecture

```
Application -> D-Bus Library -> D-Bus Daemon -> Target Service
```

**Key Concepts**:
- **Bus Name**: Service identifier (e.g., `org.freedesktop.Notifications`)
- **Object Path**: Object location (e.g., `/org/freedesktop/Notifications`)
- **Interface**: Method grouping (e.g., `org.freedesktop.Notifications`)
- **Member**: Method or signal name

### 4.2 Libraries

| Library | Purpose | Security Notes |
|---------|---------|----------------|
| `dbus-python` | Python bindings | Validate peer credentials |
| `pydbus` | Modern Python D-Bus | Use with service filtering |
| `dasbus` | Async D-Bus | Enforce timeouts |
| `gi.repository.Gio` | GIO D-Bus bindings | Built-in security |

---

## 5. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
# tests/test_dbus_client.py
import pytest
from unittest.mock import MagicMock, patch

class TestSecureDBusClient:
    """Test D-Bus client with mocked bus."""

    @pytest.fixture
    def mock_bus(self):
        with patch('dbus.SessionBus') as mock:
            yield mock.return_value

    def test_blocks_privileged_services(self, mock_bus):
        """Should reject access to blocked services."""
        from secure_dbus import SecureDBusClient

        client = SecureDBusClient()

        with pytest.raises(SecurityError) as exc:
            client.get_object('org.freedesktop.PolicyKit1', '/')

        assert 'blocked' in str(exc.value).lower()

    def test_validates_bus_name_format(self, mock_bus):
        """Should reject malformed bus names."""
        from secure_dbus import SecureDBusClient

        client = SecureDBusClient()

        with pytest.raises(ValueError):
            client.get_object('invalid..name', '/')

    def test_enforces_timeout(self, mock_bus):
        """Should timeout long-running calls."""
        from secure_dbus import SecureDBusClient

        client = SecureDBusClient()
        client.timeout = 1

        mock_bus.get_object.return_value.SomeMethod.side_effect = \
            Exception('Timeout')

        with pytest.raises(TimeoutError):
            client.call_method(
                'org.test.Service', '/', 'org.test.Interface', 'SomeMethod'
            )
```

### Step 2: Implement Minimum to Pass

```python
# secure_dbus.py
class SecureDBusClient:
    BLOCKED_SERVICES = {'org.freedesktop.PolicyKit1'}

    def get_object(self, bus_name: str, object_path: str):
        if bus_name in self.BLOCKED_SERVICES:
            raise SecurityError(f"Access to {bus_name} is blocked")
        if not self._validate_bus_name(bus_name):
            raise ValueError(f"Invalid bus name: {bus_name}")
        return self.bus.get_object(bus_name, object_path)
```

### Step 3: Refactor Following Patterns

Add logging, credential validation, and property caching.

### Step 4: Run Full Verification

```bash
# Run tests
pytest tests/test_dbus_client.py -v

# Type checking
mypy secure_dbus.py --strict

# Coverage
pytest --cov=secure_dbus --cov-report=term-missing
```

---

## 6. Performance Patterns

### Pattern 1: Connection Reuse

```python
# GOOD: Reuse connection
class DBusConnectionPool:
    _session_bus = None

    @classmethod
    def get_session_bus(cls):
        if cls._session_bus is None:
            cls._session_bus = dbus.SessionBus()
        return cls._session_bus

# BAD: Create new connection each call
def get_service():
    bus = dbus.SessionBus()  # Expensive!
    return bus.get_object('org.test.Service', '/')
```

### Pattern 2: Signal Filtering

```python
# GOOD: Filter signals at subscription
bus.add_signal_receiver(
    handler,
    signal_name='SpecificSignal',  # Only this signal
    dbus_interface='org.test.Interface',
    path='/specific/path'  # Only this path
)

# BAD: Receive all signals and filter in handler
bus.add_signal_receiver(
    handler,
    signal_name=None,  # All signals - expensive!
    dbus_interface=None
)
```

### Pattern 3: Async Calls with dasbus

```python
# GOOD: Async calls for non-blocking operations
from dasbus.connection import SessionMessageBus
from dasbus.loop import EventLoop
import asyncio

async def async_call():
    bus = SessionMessageBus()
    proxy = bus.get_proxy('org.test.Service', '/')
    result = await asyncio.to_thread(proxy.Method)
    return result

# BAD: Blocking calls in async context
def blocking_call():
    bus = dbus.SessionBus()
    proxy = bus.get_object('org.test.Service', '/')
    return proxy.Method()  # Blocks event loop!
```

### Pattern 4: Message Batching

```python
# GOOD: Batch property reads
def get_all_properties(proxy, interface):
    props = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    return props.GetAll(interface)  # One call

# BAD: Individual property reads
def get_properties_slow(proxy, interface):
    props = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    return {
        'prop1': props.Get(interface, 'prop1'),  # Call 1
        'prop2': props.Get(interface, 'prop2'),  # Call 2
        'prop3': props.Get(interface, 'prop3'),  # Call 3
    }
```

### Pattern 5: Property Caching

```python
# GOOD: Cache properties with TTL
from functools import lru_cache
from time import time

class CachedPropertyAccess:
    def __init__(self, client, cache_ttl=5):
        self.client = client
        self.cache_ttl = cache_ttl
        self._cache = {}

    def get_property(self, bus_name, path, interface, prop):
        key = (bus_name, path, interface, prop)
        cached = self._cache.get(key)

        if cached and time() - cached['time'] < self.cache_ttl:
            return cached['value']

        value = self._fetch_property(bus_name, path, interface, prop)
        self._cache[key] = {'value': value, 'time': time()}
        return value

# BAD: Fetch property every time
def get_property(proxy, interface, prop):
    props = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    return props.Get(interface, prop)  # Always fetches
```

---

## 7. Implementation Patterns

### Pattern 1: Secure D-Bus Client

```python
import dbus
from dbus.exceptions import DBusException
import logging

class SecureDBusClient:
    """Secure D-Bus client with access controls."""

    BLOCKED_SERVICES = {
        'org.freedesktop.PolicyKit1',          # Privilege escalation
        'org.freedesktop.systemd1',            # System service control
        'org.freedesktop.login1',              # Session/power management
        'org.gnome.keyring',                   # Secret storage
        'org.freedesktop.secrets',             # Secret service
        'org.freedesktop.PackageKit',          # Package installation
    }

    BLOCKED_INTERFACES = {
        'org.freedesktop.DBus.Properties',     # Can read/write any property
    }

    def __init__(self, bus_type: str = 'session', permission_tier: str = 'standard'):
        self.permission_tier = permission_tier
        self.logger = logging.getLogger('dbus.security')
        self.timeout = 30  # seconds

        # Connect to bus
        if bus_type == 'session':
            self.bus = dbus.SessionBus()
        elif bus_type == 'system':
            if permission_tier != 'elevated':
                raise PermissionError("System bus requires 'elevated' tier")
            self.bus = dbus.SystemBus()
        else:
            raise ValueError(f"Invalid bus type: {bus_type}")

    def get_object(self, bus_name: str, object_path: str) -> dbus.Interface:
        """Get D-Bus object with validation."""
        # Security check
        if bus_name in self.BLOCKED_SERVICES:
            self.logger.warning('blocked_service', service=bus_name)
            raise SecurityError(f"Access to {bus_name} is blocked")

        # Validate bus name format
        if not self._validate_bus_name(bus_name):
            raise ValueError(f"Invalid bus name: {bus_name}")

        # Get proxy object
        try:
            proxy = self.bus.get_object(bus_name, object_path)
            self._audit_log('get_object', bus_name, object_path)
            return proxy
        except DBusException as e:
            self.logger.error(f"D-Bus error: {e}")
            raise

    def call_method(
        self,
        bus_name: str,
        object_path: str,
        interface: str,
        method: str,
        *args
    ):
        """Call D-Bus method with validation."""
        # Security checks
        if interface in self.BLOCKED_INTERFACES:
            raise SecurityError(f"Interface {interface} is blocked")

        # Get object
        proxy = self.get_object(bus_name, object_path)
        iface = dbus.Interface(proxy, interface)

        # Call with timeout
        try:
            result = getattr(iface, method)(
                *args,
                timeout=self.timeout
            )
            self._audit_log('call_method', bus_name, f"{interface}.{method}")
            return result
        except DBusException as e:
            if 'Timeout' in str(e):
                raise TimeoutError(f"Method call timed out after {self.timeout}s")
            raise

    def get_peer_credentials(self, bus_name: str) -> dict:
        """Get credentials of D-Bus peer."""
        dbus_obj = self.bus.get_object(
            'org.freedesktop.DBus',
            '/org/freedesktop/DBus'
        )
        dbus_iface = dbus.Interface(dbus_obj, 'org.freedesktop.DBus')

        return {
            'pid': dbus_iface.GetConnectionUnixProcessID(bus_name),
            'uid': dbus_iface.GetConnectionUnixUser(bus_name),
        }

    def _validate_bus_name(self, name: str) -> bool:
        """Validate D-Bus bus name format."""
        import re
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)+$'
        return bool(re.match(pattern, name)) and len(name) <= 255

    def _audit_log(self, action: str, service: str, detail: str):
        """Log operation for audit."""
        self.logger.info(
            f'dbus.{action}',
            extra={
                'service': service,
                'detail': detail,
                'permission_tier': self.permission_tier
            }
        )
```

### Pattern 2: Signal Monitoring

```python
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

class SecureSignalMonitor:
    """Monitor D-Bus signals safely."""

    ALLOWED_SIGNALS = {
        'org.freedesktop.Notifications': ['NotificationClosed', 'ActionInvoked'],
        'org.freedesktop.FileManager1': ['OpenLocationRequested'],
    }

    def __init__(self, client: SecureDBusClient):
        self.client = client
        self.handlers = {}
        self.logger = logging.getLogger('dbus.signals')

        # Setup main loop
        DBusGMainLoop(set_as_default=True)

    def subscribe(
        self,
        bus_name: str,
        interface: str,
        signal: str,
        handler
    ):
        """Subscribe to signal with validation."""
        # Check if signal is allowed
        allowed = self.ALLOWED_SIGNALS.get(interface, [])
        if signal not in allowed:
            raise SecurityError(f"Signal {interface}.{signal} not allowed")

        # Wrapper to log signal receipt
        def safe_handler(*args):
            self.logger.info(
                'signal_received',
                extra={'interface': interface, 'signal': signal}
            )
            handler(*args)

        # Subscribe
        self.client.bus.add_signal_receiver(
            safe_handler,
            signal_name=signal,
            dbus_interface=interface,
            bus_name=bus_name
        )
        self.handlers[(interface, signal)] = safe_handler

    def run(self, timeout: int = None):
        """Run signal loop with timeout."""
        loop = GLib.MainLoop()

        if timeout:
            GLib.timeout_add_seconds(timeout, loop.quit)

        loop.run()
```

### Pattern 3: Property Access Control

```python
class SecurePropertyAccess:
    """Controlled access to D-Bus properties."""

    READABLE_PROPERTIES = {
        'org.freedesktop.Notifications': ['ServerCapabilities'],
        'org.mpris.MediaPlayer2': ['Identity', 'PlaybackStatus'],
    }

    WRITABLE_PROPERTIES = {
        'org.mpris.MediaPlayer2.Player': ['Volume'],
    }

    def __init__(self, client: SecureDBusClient):
        self.client = client
        self.logger = logging.getLogger('dbus.properties')

    def get_property(
        self,
        bus_name: str,
        object_path: str,
        interface: str,
        property_name: str
    ):
        """Get property with access control."""
        # Check if property is readable
        allowed = self.READABLE_PROPERTIES.get(interface, [])
        if property_name not in allowed:
            raise SecurityError(f"Property {interface}.{property_name} not readable")

        proxy = self.client.get_object(bus_name, object_path)
        props = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')

        value = props.Get(interface, property_name)
        self.logger.info(
            'property_read',
            extra={'interface': interface, 'property': property_name}
        )
        return value

    def set_property(
        self,
        bus_name: str,
        object_path: str,
        interface: str,
        property_name: str,
        value
    ):
        """Set property with access control."""
        if self.client.permission_tier == 'read-only':
            raise PermissionError("Setting properties requires 'standard' tier")

        # Check if property is writable
        allowed = self.WRITABLE_PROPERTIES.get(interface, [])
        if property_name not in allowed:
            raise SecurityError(f"Property {interface}.{property_name} not writable")

        proxy = self.client.get_object(bus_name, object_path)
        props = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')

        props.Set(interface, property_name, value)
        self.logger.info(
            'property_write',
            extra={'interface': interface, 'property': property_name}
        )
```

### Pattern 4: Service Discovery

```python
class ServiceDiscovery:
    """Discover D-Bus services safely."""

    def __init__(self, client: SecureDBusClient):
        self.client = client

    def list_names(self) -> list:
        """List available bus names (filtered)."""
        dbus_obj = self.client.bus.get_object(
            'org.freedesktop.DBus',
            '/org/freedesktop/DBus'
        )
        dbus_iface = dbus.Interface(dbus_obj, 'org.freedesktop.DBus')

        all_names = dbus_iface.ListNames()

        # Filter blocked services
        filtered = [
            name for name in all_names
            if name not in SecureDBusClient.BLOCKED_SERVICES
        ]

        return filtered

    def introspect(self, bus_name: str, object_path: str) -> str:
        """Get introspection XML for object."""
        if bus_name in SecureDBusClient.BLOCKED_SERVICES:
            raise SecurityError(f"Cannot introspect {bus_name}")

        proxy = self.client.get_object(bus_name, object_path)
        return proxy.Introspect(
            dbus_interface='org.freedesktop.DBus.Introspectable'
        )
```

---

## 5. Security Standards

### 5.1 Critical Vulnerabilities

#### 1. Privilege Escalation via PolicyKit (CVE-2021-4034)
- **Severity**: CRITICAL
- **Description**: Polkit vulnerability for local privilege escalation
- **Mitigation**: Block PolicyKit service access

#### 2. D-Bus Authentication Bypass (CVE-2022-42012)
- **Severity**: HIGH
- **Description**: Unauthorized session bus access
- **Mitigation**: Validate peer credentials

#### 3. Service Impersonation (CWE-290)
- **Severity**: HIGH
- **Description**: Malicious service claiming trusted name
- **Mitigation**: Verify service credentials

#### 4. Method Injection (CWE-74)
- **Severity**: MEDIUM
- **Description**: Malicious method parameters
- **Mitigation**: Input validation, service allowlists

#### 5. Information Disclosure (CWE-200)
- **Severity**: MEDIUM
- **Description**: Exposing sensitive service data
- **Mitigation**: Property access control

### 5.2 Permission Tier Model

```python
PERMISSION_TIERS = {
    'read-only': {
        'bus_type': 'session',
        'allowed_operations': ['get_property', 'introspect', 'list_names'],
        'blocked_services': BLOCKED_SERVICES,
    },
    'standard': {
        'bus_type': 'session',
        'allowed_operations': ['*', 'set_property', 'call_method'],
        'blocked_services': BLOCKED_SERVICES,
    },
    'elevated': {
        'bus_type': ['session', 'system'],
        'allowed_operations': ['*'],
        'blocked_services': ['org.freedesktop.PackageKit'],
    }
}
```

---

## 8. Common Mistakes

### Never: Access System Bus Without Need

```python
# BAD: Always use system bus
bus = dbus.SystemBus()

# GOOD: Prefer session bus
bus = dbus.SessionBus()
# Only use system bus when required
```

### Never: Allow PolicyKit Access

```python
# BAD: No service filtering
result = client.call_method('org.freedesktop.PolicyKit1', ...)

# GOOD: Block privileged services
if service not in BLOCKED_SERVICES:
    result = client.call_method(service, ...)
```

### Never: Skip Timeout Enforcement

```python
# BAD: No timeout
result = iface.SomeMethod()

# GOOD: With timeout
result = iface.SomeMethod(timeout=30)
```

---

## 13. Pre-Deployment Checklist

- [ ] Service blocklist configured
- [ ] Session bus preferred over system bus
- [ ] Timeout enforcement on all calls
- [ ] Peer credential validation
- [ ] Audit logging enabled
- [ ] Property access control configured

---

## 14. Summary

Your goal is to create D-Bus automation that is:
- **Secure**: Service blocklists, credential validation, access control
- **Reliable**: Timeout enforcement, error handling
- **Minimal**: Session bus by default, least privilege

**Security Reminders**:
1. Always prefer session bus over system bus
2. Block access to PolicyKit and systemd
3. Validate peer credentials when needed
4. Enforce timeouts on all method calls
5. Log all operations for audit

---

## References

- See `references/security-examples.md`
- See `references/threat-model.md`
- See `references/advanced-patterns.md`

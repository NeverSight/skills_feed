---
name: zalo-mini-app
description: Build Zalo Mini Apps - lightweight web apps running inside Zalo super-app. This skill provides ZaUI components (Button, Input, Modal, Tabs, Avatar, etc.), JavaScript APIs (authorize, getUserInfo, getPhoneNumber, getLocation, Storage, Camera), Checkout SDK for payments, design guidelines, and development tools. Use when building Mini Apps, using ZaUI components, calling Zalo APIs, integrating payments, converting web apps to Mini Apps, or following Zalo design standards.
---

# Zalo Mini App Development

Build Mini Apps for the Zalo platform using React, ZaUI components, and Zalo SDK APIs.

## Quick Start
```bash
npm install -g zmp-cli
zmp create my-app && cd my-app && zmp start
```

See [getting-started.md](./references/getting-started.md) for full setup, deployment, and app-config.json.

## Core Packages
```bash
npm install zmp-ui zmp-sdk
```

```js
import { Button, Input, Modal } from "zmp-ui";
import "zmp-ui/zaui.css";
import { getUserInfo, authorize } from "zmp-sdk/apis";
```

## References

### APIs
- [api-overview.md](./references/api-overview.md) - API categories & patterns
- [api-user.md](./references/api-user.md) - authorize, getUserInfo, getPhoneNumber
- [api-storage.md](./references/api-storage.md) - setItem, getItem, storage APIs
- [api-ui.md](./references/api-ui.md) - showToast, navigation, routing
- [api-device.md](./references/api-device.md) - location, camera, QR, NFC
- [api-zalo.md](./references/api-zalo.md) - followOA, openChat, share

### ZaUI Components
- [zaui-overview.md](./references/zaui-overview.md) - Component list & design tokens
- [zaui-layout.md](./references/zaui-layout.md) - App, Page, Header, Tabs, Router
- [zaui-display.md](./references/zaui-display.md) - Avatar, Icon, List, Swiper
- [zaui-form.md](./references/zaui-form.md) - Button, Input, Select, DatePicker
- [zaui-overlay.md](./references/zaui-overlay.md) - Modal, Sheet, ActionSheet

### Design & Setup
- [design-guidelines.md](./references/design-guidelines.md) - Colors, typography, UX
- [getting-started.md](./references/getting-started.md) - Setup, deploy, publish
- [web-design-guidelines.md](./references/web-design-guidelines.md) - Accessibility, forms, animations, touch, i18n

### Performance & React
- [react-best-practices.md](./references/react-best-practices.md) - Waterfalls, bundle size, re-renders, JS performance

## Common Patterns

### Get User Info
```js
const { userInfo } = await getUserInfo({ autoRequestPermission: true });
// { id, name, avatar, followedOA }
```

### Basic Page Layout
```jsx
<App>
  <Page>
    <Header title="Home" />
    <List>
      <List.Item title="Item" suffix={<Icon icon="zi-chevron-right" />} />
    </List>
  </Page>
  <BottomNavigation fixed>
    <BottomNavigation.Item key="home" label="Home" icon={<Icon icon="zi-home" />} />
  </BottomNavigation>
</App>
```

## Resources
- Docs: https://miniapp.zaloplatforms.com/documents/
- Mini App Center: https://miniapp.zaloplatforms.com/
- React Best Practices: https://react.dev
- SWR: https://swr.vercel.app

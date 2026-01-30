---
name: uniapp-frontend
description: "uni-app cross-platform frontend development with Vue 3 + TypeScript. Use for: (1) Creating new uni-app projects or pages, (2) Integrating UI libraries (uView Plus, uni-ui, TuniaoUI), (3) Implementing multi-theme design systems, (4) Building WeChat Mini Programs, H5, and other platforms, (5) Setting up SCSS theming and global styles, (6) Configuring Vite build system. Includes reusable templates, component patterns, and best practices applicable to any uni-app project."
---

# uni-app Frontend Development

Comprehensive guide for building cross-platform apps with uni-app, Vue 3, and TypeScript.

## Quick Start

### Create a New Page

```bash
# Create page directory
mkdir -p src/pages/newpage

# Create page files
touch src/pages/newpage/index.vue
```

### Register Page in pages.json

```json
{
  "pages": [
    {
      "path": "pages/newpage/index",
      "style": {
        "navigationBarTitleText": "Page Title"
      }
    }
  ]
}
```

### Basic Page Template

See [assets/page-template.vue](assets/page-template.vue) for a complete page template.

## Project Structure

Standard uni-app CLI project structure:

```
src/
├── pages/          # Page components (one per directory)
├── components/     # Shared/reusable components
├── store/          # Pinia state management
├── api/            # API interface definitions
├── utils/          # Utility functions
├── types/          # TypeScript type definitions
├── styles/         # Global styles
│   ├── theme.scss       # Theme variables
│   └── common.scss      # Common styles
├── static/         # Static assets (images, icons)
├── App.vue         # App root component
├── main.ts         # App entry point
├── pages.json      # Page and tabBar configuration
└── uni.scss        # uni-app built-in variables
```

## UI Library Integration

### uView Plus

**Installation:**
```bash
npm install uview-plus
```

**Configuration:**

App.vue - Import styles:
```vue
<style lang="scss">
@import "uview-plus/index.scss";
@import "@/styles/common.scss";
</style>
```

main.ts - Register plugin:
```typescript
import uviewPlus from "uview-plus";
app.use(uviewPlus);
```

vite.config.ts - Global SCSS:
```typescript
css: {
  preprocessorOptions: {
    scss: {
      additionalData: `@import "@/styles/theme.scss";@import "uview-plus/theme.scss";`,
      api: "modern-compiler",
    },
  },
}
```

### Other UI Libraries

**uni-ui** (official):
```bash
npm install @dcloudio/uni-ui
```

**TuniaoUI** (Tuniao):
```bash
npm install @tuniao/tnui-vue3-uniapp
```

See [references/ui-libraries.md](references/ui-libraries.md) for integration guides.

## Theme System Design

Implement flexible theming for multi-role or multi-brand applications.

### Basic Theme Setup

**src/styles/theme.scss:**
```scss
// Theme colors
$theme-primary: #1890ff;
$theme-success: #52c41a;
$theme-warning: #faad14;
$theme-error: #f5222d;

// Neutral colors
$color-text-primary: #333333;
$color-text-regular: #666666;
$color-text-secondary: #999999;

$color-bg-page: #f5f5f5;
$color-bg-card: #ffffff;

// Spacing scale
$spacing-xs: 8rpx;
$spacing-sm: 16rpx;
$spacing-md: 24rpx;
$spacing-lg: 32rpx;
$spacing-xl: 48rpx;

// Typography
$font-size-xs: 20rpx;
$font-size-sm: 24rpx;
$font-size-base: 28rpx;
$font-size-lg: 32rpx;
$font-size-xl: 36rpx;

// Border radius
$border-radius-sm: 4rpx;
$border-radius-md: 8rpx;
$border-radius-lg: 16rpx;
$border-radius-circle: 50%;
```

**vite.config.ts** - Inject globally:
```typescript
css: {
  preprocessorOptions: {
    scss: {
      additionalData: `@import "@/styles/theme.scss";`,
      api: "modern-compiler",
    },
  },
}
```

### Multi-Theme Implementation

For apps requiring multiple themes (e.g., user/admin, different brands):

**Option 1: Theme variables per environment**
```scss
// src/styles/theme.scss
// Define different theme color sets
$theme-user-primary: #1890ff;
$theme-admin-primary: #0050b3;

// Set active theme
$theme-primary: $theme-user-primary; // Change based on build/env
```

**Option 2: Dynamic theme switching**
```typescript
// store/theme.ts
import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: 'default',
  }),

  getters: {
    themeColors() {
      const themes = {
        default: { primary: '#1890ff' },
        dark: { primary: '#0050b3' },
      };
      return themes[this.currentTheme];
    },
  },
});
```

See [references/theme-guide.md](references/theme-guide.md) for complete theming patterns.

## Build Commands

```bash
# WeChat Mini Program
npm run dev:mp-weixin      # Development
npm run build:mp-weixin    # Production

# H5
npm run dev:h5             # Development
npm run build:h5           # Production

# Other platforms
npm run dev:mp-alipay       # Alipay Mini Program
npm run dev:mp-baidu       # Baidu Mini Program
npm run dev:mp-toutiao     # Toutiao Mini Program
```

## Common Patterns

### Data Fetching Pattern

```vue
<script setup lang="ts">
import { ref, onMounted } from "vue";

interface Item {
  id: number;
  title: string;
}

const items = ref<Item[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

onMounted(() => {
  loadData();
});

const loadData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const data = await api.getItems();
    items.value = data;
  } catch (err) {
    error.value = "Failed to load data";
    uni.showToast({ title: error.value, icon: "none" });
  } finally {
    loading.value = false;
  }
};
</script>
```

### Navigation Patterns

```typescript
// Navigate to page (adds to history stack)
uni.navigateTo({ url: "/pages/detail/index" });

// Navigate with parameters
uni.navigateTo({ url: `/pages/detail/index?id=${id}&type=parcel` });

// Redirect (replaces current page, no back button)
uni.redirectTo({ url: "/pages/login/index" });

// Switch to tabBar page
uni.switchTab({ url: "/pages/home/index" });

// Navigate back
uni.navigateBack();

// Launch another mini program
uni.navigateToMiniProgram({
  appId: "xxxxx",
  path: "pages/index/index",
});
```

### User Feedback

**Toast:**
```typescript
uni.showToast({
  title: "Success",
  icon: "success",
  duration: 2000,
});

uni.showToast({
  title: "Error message",
  icon: "none",
});

// Loading toast
uni.showLoading({ title: "Loading..." });
uni.hideLoading();
```

**Modal:**
```typescript
uni.showModal({
  title: "Confirm",
  content: "Are you sure?",
  success: (res) => {
    if (res.confirm) {
      // User clicked confirm
    }
  },
});
```

**Action Sheet:**
```typescript
uni.showActionSheet({
  itemList: ["Option 1", "Option 2", "Option 3"],
  success: (res) => {
    console.log("Selected:", res.tapIndex);
  },
});
```

### Lifecycle Hooks

```vue
<script setup lang="ts">
import {
  onLaunch,
  onShow,
  onHide,
  onUnload,
} from "@dcloudio/uni-app";

import { onLoad, onReady, onReachBottom, onPullDownRefresh } from "@dcloudio/uni-app";

// App-level hooks (use in App.vue)
onLaunch(() => {
  console.log("App launched");
});

onShow(() => {
  console.log("App shown");
});

// Page-level hooks (use in pages)
onLoad((options) => {
  console.log("Page loaded with params:", options);
});

onReady(() => {
  console.log("Page ready");
});

onReachBottom(() => {
  console.log("Reached bottom - load more");
});

onPullDownRefresh(() => {
  console.log("Pull down refresh");
  // Stop loading after data fetch
  uni.stopPullDownRefresh();
});
</script>
```

## Platform Detection

```typescript
// Get platform info
const systemInfo = uni.getSystemInfoSync();
console.log("Platform:", systemInfo.platform); // ios, android, devtools
console.log("System:", systemInfo.system);     // iOS 14.5, Android 10

// Conditional code based on platform
// #ifdef H5
console.log("Running on H5");
// #endif

// #ifdef MP-WEIXIN
console.log("Running on WeChat Mini Program");
// #endif

// #ifdef MP-ALIPAY
console.log("Running on Alipay Mini Program");
// #endif
```

## Pinia State Management

**Store definition:**
```typescript
// src/store/user.ts
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    token: '',
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      const data = await api.login(credentials);
      this.token = data.token;
      this.userInfo = data.user;
    },

    logout() {
      this.token = '';
      this.userInfo = null;
    },
  },
});
```

**Use in component:**
```vue
<script setup lang="ts">
import { useUserStore } from "@/store/user";

const userStore = useUserStore();

// Access state
console.log(userStore.userInfo);

// Call actions
await userStore.login({ username, password });

// Use getters
if (userStore.isLoggedIn) {
  // ...
}
</script>
```

## API Integration

**API module:**
```typescript
// src/api/index.ts
const BASE_URL = "https://api.example.com";

export const api = {
  // GET request
  async getItems() {
    const res = await uni.request({
      url: `${BASE_URL}/items`,
      method: "GET",
    });
    return res.data;
  },

  // POST request
  async createItem(data: any) {
    const res = await uni.request({
      url: `${BASE_URL}/items`,
      method: "POST",
      data,
    });
    return res.data;
  },
};
```

**With interceptors:**
```typescript
// src/utils/request.ts
let token = "";

export const request = (options: UniApp.RequestOptions) => {
  // Add token
  if (token) {
    options.header = {
      ...options.header,
      Authorization: `Bearer ${token}`,
    };
  }

  return uni.request(options);
};

// Set token after login
export const setToken = (newToken: string) => {
  token = newToken;
};
```

## Troubleshooting

### SCSS Variables Not Found

**Error:** `Undefined variable $spacing-md`

**Solutions:**
1. Check `vite.config.ts` has `additionalData` configuration
2. Verify theme file path is correct
3. Restart dev server after config changes

### Components Not Rendering

**Check:**
1. Component registered in `pages.json`
2. Correct import path (use `@/` alias)
3. Component name in PascalCase for Vue components

### Build Errors

**Common fixes:**
1. Clear cache: `rm -rf node_modules dist && npm install`
2. Check Node.js version (use LTS)
3. Verify dependencies are compatible

### Platform-Specific Issues

**WeChat Mini Program:**
- Ensure appid is correct in `manifest.json`
- Check domain whitelist in Mini Program admin console
- Test in WeChat DevTools

**H5:**
- Test in multiple browsers
- Check CORS configuration
- Verify API endpoints support HTTPS

## Resources

### references/theme-guide.md
Complete theme system design with multi-theme patterns, color theory, and implementation strategies.

### references/ui-libraries.md
Integration guides for uView Plus, uni-ui, TuniaoUI, and other popular UI libraries.

### references/page-patterns.md
Reusable page patterns: list pages, detail pages, forms, search/filter, empty states, etc.

### references/platform-specific.md
Platform-specific considerations and best practices for WeChat, Alipay, H5, etc.

### assets/page-template.vue
Minimal Vue 3 + TypeScript page template ready to customize.

### assets/component-templates/
Common component templates (card, button-group, list-item, etc.).

## Best Practices

1. **Use TypeScript** - Catch errors at compile time
2. **Component composition** - Keep components small and focused
3. **State management** - Use Pinia for complex state
4. **Error handling** - Always handle API errors gracefully
5. **Loading states** - Show loading indicators during async operations
6. **Responsive design** - Test on multiple screen sizes
7. **Performance** - Lazy load images and long lists
8. **Accessibility** - Use semantic HTML and ARIA labels
9. **Code organization** - Follow consistent file structure
10. **Version control** - Commit frequently with meaningful messages

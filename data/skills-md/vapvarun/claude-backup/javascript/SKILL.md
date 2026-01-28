---
name: javascript
description: Write modern JavaScript/ES6+ code following best practices for performance, security, and maintainability. Use when writing JS code, fixing bugs, or implementing frontend functionality.
---

# JavaScript Skill

## Instructions

When writing JavaScript:

### 1. Modern Syntax

```javascript
// Use const by default, let when needed
const API_URL = 'https://api.example.com';
let count = 0;

// Arrow functions
const add = (a, b) => a + b;
const greet = name => `Hello, ${name}!`;

// Destructuring
const { name, email } = user;
const [first, second, ...rest] = items;

// Spread operator
const newArray = [...oldArray, newItem];
const newObject = { ...oldObject, newProp: value };

// Template literals
const message = `User ${name} has ${count} items`;

// Optional chaining
const city = user?.address?.city;

// Nullish coalescing
const value = input ?? defaultValue;
```

### 2. Async/Await

```javascript
// Async function
async function fetchData(url) {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}

// Parallel requests
async function fetchAll(urls) {
  const promises = urls.map(url => fetch(url));
  const responses = await Promise.all(promises);
  return Promise.all(responses.map(r => r.json()));
}

// With timeout
async function fetchWithTimeout(url, timeout = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### 3. Array Methods

```javascript
const users = [
  { id: 1, name: 'Alice', age: 25, active: true },
  { id: 2, name: 'Bob', age: 30, active: false },
  { id: 3, name: 'Charlie', age: 35, active: true },
];

// map - transform items
const names = users.map(user => user.name);

// filter - select items
const activeUsers = users.filter(user => user.active);

// find - get first match
const bob = users.find(user => user.name === 'Bob');

// some/every - check conditions
const hasActive = users.some(user => user.active);
const allActive = users.every(user => user.active);

// reduce - aggregate
const totalAge = users.reduce((sum, user) => sum + user.age, 0);

// Chaining
const activeNames = users
  .filter(user => user.active)
  .map(user => user.name)
  .sort();
```

### 4. DOM Manipulation

```javascript
// Selecting elements
const element = document.querySelector('.class');
const elements = document.querySelectorAll('.class');

// Creating elements
const div = document.createElement('div');
div.className = 'card';
div.innerHTML = `
  <h2>${title}</h2>
  <p>${description}</p>
`;

// Event handling
element.addEventListener('click', (event) => {
  event.preventDefault();
  // Handle click
});

// Event delegation
document.querySelector('.list').addEventListener('click', (event) => {
  if (event.target.matches('.item')) {
    handleItemClick(event.target);
  }
});

// IntersectionObserver (lazy loading, animations)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.animate').forEach(el => observer.observe(el));
```

### 5. Classes

```javascript
class User {
  #privateField; // Private field

  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.#privateField = 'secret';
  }

  // Getter
  get displayName() {
    return this.name.toUpperCase();
  }

  // Setter
  set displayName(value) {
    this.name = value.trim();
  }

  // Method
  greet() {
    return `Hello, I'm ${this.name}`;
  }

  // Static method
  static create(data) {
    return new User(data.name, data.email);
  }
}

// Inheritance
class Admin extends User {
  constructor(name, email, role) {
    super(name, email);
    this.role = role;
  }

  greet() {
    return `${super.greet()} and I'm an ${this.role}`;
  }
}
```

### 6. Modules

```javascript
// Named exports
export const API_URL = 'https://api.example.com';
export function fetchData() { /* ... */ }
export class User { /* ... */ }

// Default export
export default function main() { /* ... */ }

// Importing
import main, { API_URL, fetchData, User } from './module.js';

// Dynamic import
const module = await import('./heavy-module.js');
```

### 7. Error Handling

```javascript
// Custom error
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

// Try-catch with specific handling
try {
  await submitForm(data);
} catch (error) {
  if (error instanceof ValidationError) {
    showFieldError(error.field, error.message);
  } else if (error instanceof NetworkError) {
    showToast('Network error. Please try again.');
  } else {
    console.error('Unexpected error:', error);
    showToast('Something went wrong.');
  }
}
```

### 8. Local Storage

```javascript
// Store data
const saveData = (key, data) => {
  localStorage.setItem(key, JSON.stringify(data));
};

// Retrieve data
const getData = (key, defaultValue = null) => {
  const stored = localStorage.getItem(key);
  return stored ? JSON.parse(stored) : defaultValue;
};

// Remove data
const removeData = (key) => {
  localStorage.removeItem(key);
};
```

### 9. Debounce & Throttle

```javascript
// Debounce - wait until stopped
function debounce(func, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

const debouncedSearch = debounce((query) => {
  fetchResults(query);
}, 300);

// Throttle - limit frequency
function throttle(func, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

const throttledScroll = throttle(() => {
  updatePosition();
}, 100);
```

### 10. Best Practices

- Use `const` by default
- Prefer arrow functions
- Use async/await over callbacks
- Handle all errors
- Avoid global variables
- Use meaningful variable names
- Keep functions small and focused
- Comment complex logic
- Use strict equality (`===`)
- Validate user input

---

## WordPress-Specific JavaScript

### 11. Enqueueing Scripts Properly

```php
function theme_enqueue_scripts() {
    // Frontend script
    wp_enqueue_script(
        'theme-main',
        get_template_directory_uri() . '/assets/js/main.js',
        array(), // dependencies
        '1.0.0',
        true // in footer
    );

    // With jQuery dependency
    wp_enqueue_script(
        'theme-jquery-script',
        get_template_directory_uri() . '/assets/js/custom.js',
        array('jquery'),
        '1.0.0',
        true
    );

    // Pass PHP data to JavaScript
    wp_localize_script('theme-main', 'themeData', array(
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'restUrl' => rest_url('theme/v1/'),
        'nonce'   => wp_create_nonce('theme_nonce'),
        'i18n'    => array(
            'loading' => __('Loading...', 'theme'),
            'error'   => __('An error occurred', 'theme'),
        ),
    ));
}
add_action('wp_enqueue_scripts', 'theme_enqueue_scripts');
```

### 12. AJAX with admin-ajax.php

```javascript
// Frontend JavaScript
async function submitForm(formData) {
    const data = new FormData();
    data.append('action', 'theme_submit_form');
    data.append('nonce', themeData.nonce);
    data.append('name', formData.name);
    data.append('email', formData.email);

    try {
        const response = await fetch(themeData.ajaxUrl, {
            method: 'POST',
            body: data,
            credentials: 'same-origin',
        });

        const result = await response.json();

        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.data.message || 'Request failed');
        }
    } catch (error) {
        console.error('AJAX Error:', error);
        throw error;
    }
}
```

```php
// PHP handler
add_action('wp_ajax_theme_submit_form', 'theme_handle_form');
add_action('wp_ajax_nopriv_theme_submit_form', 'theme_handle_form');

function theme_handle_form() {
    // Verify nonce
    if (!wp_verify_nonce($_POST['nonce'], 'theme_nonce')) {
        wp_send_json_error(array('message' => 'Invalid nonce'));
    }

    // Sanitize input
    $name = sanitize_text_field($_POST['name']);
    $email = sanitize_email($_POST['email']);

    // Process...

    wp_send_json_success(array('message' => 'Form submitted'));
}
```

### 13. REST API Requests

```javascript
// GET request
async function getPosts() {
    const response = await fetch(`${themeData.restUrl}posts`, {
        headers: {
            'X-WP-Nonce': themeData.nonce,
        },
    });
    return response.json();
}

// POST request
async function createPost(data) {
    const response = await fetch(`${themeData.restUrl}posts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-WP-Nonce': themeData.nonce,
        },
        body: JSON.stringify(data),
    });
    return response.json();
}

// Using wp.apiFetch (Gutenberg)
wp.apiFetch({ path: '/wp/v2/posts' }).then(posts => {
    console.log(posts);
});
```

### 14. jQuery Compatibility

```javascript
// WordPress jQuery no-conflict wrapper
(function($) {
    $(document).ready(function() {
        // Your jQuery code here
        $('.element').on('click', function() {
            $(this).toggleClass('active');
        });
    });
})(jQuery);

// Or with modern syntax
jQuery(($) => {
    $('.element').on('click', function() {
        $(this).toggleClass('active');
    });
});
```

### 15. Gutenberg/Block Editor JavaScript

```javascript
// Using wp.data for state
const { select, dispatch } = wp.data;

// Get current post
const post = select('core/editor').getCurrentPost();

// Get blocks
const blocks = select('core/block-editor').getBlocks();

// Using wp.hooks for filters
wp.hooks.addFilter(
    'blocks.registerBlockType',
    'theme/modify-block',
    (settings, name) => {
        if (name === 'core/paragraph') {
            settings.attributes.customAttr = {
                type: 'string',
                default: '',
            };
        }
        return settings;
    }
);

// Using wp.i18n for translations
const { __, _n, sprintf } = wp.i18n;
const message = __('Hello World', 'theme');
const items = sprintf(_n('%d item', '%d items', count, 'theme'), count);
```

### 16. WordPress JavaScript Best Practices

- **Always use nonces** for security in AJAX/REST requests
- **Use wp_localize_script()** to pass data from PHP to JS
- **Wrap jQuery code** in no-conflict wrapper
- **Prefer REST API** over admin-ajax for new projects
- **Use wp.apiFetch** in Gutenberg context
- **Namespace your code** to avoid conflicts
- **Load scripts in footer** when possible (`true` as last param)
- **Use dependencies array** correctly (e.g., `array('jquery', 'wp-element')`)
- **Handle errors gracefully** with user-friendly messages
- **Test in both frontend and admin** contexts

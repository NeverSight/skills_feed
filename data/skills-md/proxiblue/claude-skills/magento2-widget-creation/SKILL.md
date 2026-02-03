---
name: magento2-widget-creation
description: Comprehensive guide for creating custom widget modules in Magento 2 that can be inserted into CMS pages and blocks. Covers module structure, widget configuration, templates, JavaScript, CSS, and form submission handling for non-Hyvä themes.
---

# Magento 2 Widget Creation for CMS Pages

## Purpose
This skill provides comprehensive guidance on creating custom widget modules in Magento 2 (standard Luma/Blank themes, not Hyvä-based) that can be inserted into CMS pages, CMS blocks, or any content area using the widget system.

## When to Use This Skill

Use this skill when you need to:
- Create a reusable component that can be inserted into CMS pages
- Build interactive elements (buttons, forms, modals) for content editors
- Develop custom functionality that non-technical users can add to pages
- Create widgets with configurable parameters that appear in the admin panel
- Implement widgets that work with standard Magento themes (Luma/Blank)

**Do NOT use this skill for:**
- Hyvä theme widgets (use hyva-tailwind-integration skill instead)
- Backend admin widgets
- UI components or admin grids

## Prerequisites
- Existing vendor namespace or willingness to create one
- Basic understanding of Magento 2 module structure
- Knowledge of XML configuration
- Familiarity with Magento templates and blocks
- Understanding of JavaScript widget pattern (optional, for interactive widgets)

## Widget Module Structure

A complete widget module requires these components:

```
app/code/Vendor/ModuleName/
├── registration.php                          # Module registration
├── etc/
│   ├── module.xml                           # Module configuration
│   ├── widget.xml                           # Widget definition
│   ├── email_templates.xml                  # (Optional) Email templates
│   └── frontend/
│       └── routes.xml                       # (Optional) For form submissions
├── Block/
│   └── Widget/
│       └── WidgetName.php                   # Widget block class
├── Controller/                              # (Optional) For form handlers
│   └── Index/
│       └── Submit.php
└── view/frontend/
    ├── templates/
    │   └── widget/
    │       └── template.phtml               # Widget template
    ├── layout/
    │   └── default.xml                      # (Optional) Load CSS/JS globally
    ├── web/
    │   ├── js/
    │   │   └── widget-script.js             # (Optional) Custom JS
    │   └── css/
    │       └── widget-style.css             # (Optional) Custom CSS
    ├── requirejs-config.js                  # (Optional) JS module mapping
    └── email/                               # (Optional) Email templates
        └── template.html
```

## Step-by-Step Widget Creation

### Step 1: Create Module Registration

**File: `registration.php`**

```php
<?php
/**
 * Copyright © Vendor. All rights reserved.
 */

use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register(
    ComponentRegistrar::MODULE,
    'Vendor_ModuleName',
    __DIR__
);
```

### Step 2: Create Module Configuration

**File: `etc/module.xml`**

```xml
<?xml version="1.0"?>
<!--
/**
 * Copyright © Vendor. All rights reserved.
 */
-->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="Vendor_ModuleName" setup_version="1.0.0">
        <sequence>
            <module name="Magento_Cms"/>
            <module name="Magento_Widget"/>
        </sequence>
    </module>
</config>
```

**Key Points:**
- `setup_version` is legacy but still commonly used
- Add dependencies in `<sequence>` - `Magento_Cms` and `Magento_Widget` are required for widgets
- Add other modules your widget depends on (e.g., `Magento_Email`, `Magento_Catalog`)

### Step 3: Create Widget Configuration

**File: `etc/widget.xml`**

This is where you define your widget's metadata and configurable parameters.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
/**
 * Copyright © Vendor. All rights reserved.
 */
-->
<widgets xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Widget:etc/widget.xsd">
    <widget id="widget_unique_id" class="Vendor\ModuleName\Block\Widget\WidgetName">
        <label translate="true">Widget Display Name</label>
        <description translate="true">Brief description of what the widget does</description>
        <parameters>
            <!-- Text Parameter -->
            <parameter name="text_param" xsi:type="text" required="false" visible="true">
                <label translate="true">Text Label</label>
                <description translate="true">Description shown in admin</description>
            </parameter>

            <!-- Select/Dropdown Parameter -->
            <parameter name="select_param" xsi:type="select" required="false" visible="true">
                <label translate="true">Select Option</label>
                <options>
                    <option name="option1" value="value1">
                        <label>Option 1</label>
                    </option>
                    <option name="option2" value="value2">
                        <label>Option 2</label>
                    </option>
                </options>
            </parameter>

            <!-- Yes/No Parameter -->
            <parameter name="enabled" xsi:type="select" required="false" visible="true"
                       source_model="Magento\Config\Model\Config\Source\Yesno">
                <label translate="true">Enable Feature</label>
            </parameter>

            <!-- CMS Block Chooser -->
            <parameter name="block_id" xsi:type="block" visible="true" required="false">
                <label translate="true">CMS Block</label>
                <block class="Magento\Cms\Block\Adminhtml\Block\Widget\Chooser">
                    <data>
                        <item name="button" xsi:type="array">
                            <item name="open" xsi:type="string">Select Block...</item>
                        </item>
                    </data>
                </block>
            </parameter>

            <!-- Category Chooser -->
            <parameter name="category_id" xsi:type="select" visible="true"
                       source_model="Magento\Catalog\Model\Category\Attribute\Source\Categories">
                <label translate="true">Category</label>
            </parameter>
        </parameters>
    </widget>
</widgets>
```

**Widget Parameter Types:**
- `text` - Simple text input
- `select` - Dropdown selection
- `multiselect` - Multiple selections
- `block` - CMS block picker
- `page` - CMS page picker
- `conditions` - Product/category conditions (advanced)

**Important Attributes:**
- `id` - Unique identifier for the widget
- `class` - Full namespaced path to your block class
- `required` - Whether parameter is mandatory
- `visible` - Whether parameter shows in admin

### Step 4: Create Block Class

**File: `Block/Widget/WidgetName.php`**

The block class handles the widget's logic and data.

```php
<?php
/**
 * Copyright © Vendor. All rights reserved.
 */
declare(strict_types=1);

namespace Vendor\ModuleName\Block\Widget;

use Magento\Framework\View\Element\Template;
use Magento\Widget\Block\BlockInterface;
use Magento\Framework\View\Element\Template\Context;

class WidgetName extends Template implements BlockInterface
{
    /**
     * Template path relative to view/frontend/templates/
     *
     * @var string
     */
    protected $_template = 'Vendor_ModuleName::widget/template.phtml';

    /**
     * @param Context $context
     * @param array $data
     */
    public function __construct(
        Context $context,
        array $data = []
    ) {
        parent::__construct($context, $data);
    }

    /**
     * Get widget parameter with default value
     *
     * @return string
     */
    public function getParameterValue(): string
    {
        return $this->getData('text_param') ?: 'default value';
    }

    /**
     * Get widget select parameter
     *
     * @return string
     */
    public function getSelectValue(): string
    {
        return $this->getData('select_param') ?: 'value1';
    }

    /**
     * Check if feature is enabled
     *
     * @return bool
     */
    public function isEnabled(): bool
    {
        return (bool)$this->getData('enabled');
    }

    /**
     * Get URL for AJAX or form submission
     *
     * @return string
     */
    public function getActionUrl(): string
    {
        return $this->getUrl('modulename/index/submit');
    }
}
```

**Best Practices:**
- Always `declare(strict_types=1);`
- Implement `BlockInterface`
- Use `$this->getData('param_name')` to access widget parameters
- Provide default values with `?:` operator
- Add type hints and return types
- Keep business logic out of templates - put it in block methods

### Step 5: Create Template File

**File: `view/frontend/templates/widget/template.phtml`**

Templates render the HTML output. Always escape data for security.

```php
<?php
/**
 * Copyright © Vendor. All rights reserved.
 *
 * @var $block Vendor\ModuleName\Block\Widget\WidgetName
 * @var $escaper Magento\Framework\Escaper
 */

$paramValue = $block->getParameterValue();
$selectValue = $block->getSelectValue();
$isEnabled = $block->isEnabled();
$uniqueId = uniqid('widget_');
?>

<?php if ($isEnabled): ?>
<div class="custom-widget" id="<?= $escaper->escapeHtmlAttr($uniqueId) ?>">
    <div class="widget-content">
        <h3><?= $escaper->escapeHtml(__('Widget Title')) ?></h3>
        <p><?= $escaper->escapeHtml($paramValue) ?></p>

        <?php if ($selectValue === 'value1'): ?>
            <div class="option-one-content">
                <!-- Content for option 1 -->
            </div>
        <?php endif; ?>

        <button type="button"
                class="action primary widget-button"
                data-mage-init='{"widgetName": {"elementId": "<?= $escaper->escapeJs($uniqueId) ?>"}}'>
            <?= $escaper->escapeHtml(__('Click Me')) ?>
        </button>
    </div>
</div>
<?php endif; ?>
```

**Template Best Practices:**
- Always use `$escaper->escapeHtml()` for text content
- Use `$escaper->escapeHtmlAttr()` for HTML attributes
- Use `$escaper->escapeJs()` for JavaScript strings
- Use `$escaper->escapeUrl()` for URLs
- Use `__()` for translatable strings
- Generate unique IDs to avoid conflicts (use `uniqid()`)
- Add proper `@var` comments for IDE support

**Common Escaping Methods:**
```php
// Text content
<?= $escaper->escapeHtml($text) ?>

// HTML attributes
<div class="<?= $escaper->escapeHtmlAttr($class) ?>">

// JavaScript strings
data-value="<?= $escaper->escapeJs($value) ?>"

// URLs
<a href="<?= $escaper->escapeUrl($url) ?>">

// CSS
<div style="<?= $escaper->escapeCss($style) ?>">
```

### Step 6: Add JavaScript (Optional)

If your widget needs interactivity, add JavaScript using Magento's widget pattern.

**File: `view/frontend/requirejs-config.js`**

```javascript
/**
 * Copyright © Vendor. All rights reserved.
 */
var config = {
    map: {
        '*': {
            widgetName: 'Vendor_ModuleName/js/widget-script'
        }
    }
};
```

**File: `view/frontend/web/js/widget-script.js`**

```javascript
/**
 * Copyright © Vendor. All rights reserved.
 */
define([
    'jquery',
    'jquery-ui-modules/widget'
], function ($) {
    'use strict';

    /**
     * Widget initialization pattern
     */
    $.widget('vendor.widgetName', {
        options: {
            elementId: '',
            ajaxUrl: ''
        },

        /**
         * Widget creation
         * @private
         */
        _create: function () {
            this._bind();
        },

        /**
         * Bind event handlers
         * @private
         */
        _bind: function () {
            var self = this;

            this.element.on('click', function (e) {
                e.preventDefault();
                self._handleClick();
            });
        },

        /**
         * Handle click event
         * @private
         */
        _handleClick: function () {
            console.log('Widget clicked!');
            console.log('Element ID:', this.options.elementId);

            // Example AJAX call
            if (this.options.ajaxUrl) {
                this._makeAjaxRequest();
            }
        },

        /**
         * Make AJAX request
         * @private
         */
        _makeAjaxRequest: function () {
            var self = this;

            $.ajax({
                url: this.options.ajaxUrl,
                type: 'POST',
                dataType: 'json',
                data: {
                    // Your data here
                },
                success: function (response) {
                    self._handleResponse(response);
                },
                error: function () {
                    console.error('Request failed');
                }
            });
        },

        /**
         * Handle AJAX response
         * @private
         */
        _handleResponse: function (response) {
            if (response.success) {
                console.log('Success:', response.message);
            } else {
                console.error('Error:', response.message);
            }
        }
    });

    return $.vendor.widgetName;
});
```

**Initialization in Template:**

```php
<button type="button"
        data-mage-init='{"widgetName": {
            "elementId": "<?= $escaper->escapeJs($uniqueId) ?>",
            "ajaxUrl": "<?= $escaper->escapeUrl($block->getActionUrl()) ?>"
        }}'>
    Click Me
</button>
```

**Alternative Initialization with `data-bind` (Knockout.js):**

```php
<!-- For Knockout.js integration -->
<div data-bind="scope: 'widget-scope'">
    <!-- content -->
</div>

<script type="text/x-magento-init">
{
    "[data-bind]": {
        "Magento_Ui/js/core/app": {
            "components": {
                "widget-scope": {
                    "component": "Vendor_ModuleName/js/widget-component"
                }
            }
        }
    }
}
</script>
```

### Step 7: Add CSS Styling (Optional)

**File: `view/frontend/layout/default.xml`**

Load your CSS globally across all pages.

```xml
<?xml version="1.0"?>
<!--
/**
 * Copyright © Vendor. All rights reserved.
 */
-->
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
    <head>
        <css src="Vendor_ModuleName::css/widget-style.css"/>
    </head>
</page>
```

**File: `view/frontend/web/css/widget-style.css`**

```css
/**
 * Copyright © Vendor. All rights reserved.
 */

/* Widget Container */
.custom-widget {
    padding: 20px;
    margin: 10px 0;
}

.custom-widget .widget-content {
    background: #f5f5f5;
    padding: 15px;
    border-radius: 5px;
}

.custom-widget h3 {
    margin: 0 0 10px;
    font-size: 18px;
    font-weight: 600;
}

.custom-widget .widget-button {
    margin-top: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .custom-widget {
        padding: 15px;
    }

    .custom-widget .widget-content {
        padding: 10px;
    }
}
```

**CSS Best Practices:**
- Use specific class names to avoid conflicts
- Follow mobile-first approach with media queries
- Respect existing theme styles
- Use CSS variables for theming (if supported)
- Avoid `!important` unless absolutely necessary

## Advanced: Adding Controllers for Form Submission

For widgets that need to process data (forms, AJAX requests), add a controller.

### Step 1: Create Frontend Routes

**File: `etc/frontend/routes.xml`**

```xml
<?xml version="1.0"?>
<!--
/**
 * Copyright © Vendor. All rights reserved.
 */
-->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="standard">
        <route id="modulename" frontName="modulename">
            <module name="Vendor_ModuleName" />
        </route>
    </router>
</config>
```

**Route URL Pattern:**
- URL: `https://yourstore.com/modulename/index/submit`
- `modulename` = frontName
- `index` = controller directory
- `submit` = action file name

### Step 2: Create Controller Action

**File: `Controller/Index/Submit.php`**

```php
<?php
/**
 * Copyright © Vendor. All rights reserved.
 */
declare(strict_types=1);

namespace Vendor\ModuleName\Controller\Index;

use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\App\RequestInterface;
use Magento\Framework\Controller\Result\JsonFactory;
use Magento\Framework\Exception\LocalizedException;
use Psr\Log\LoggerInterface;

/**
 * Handle form submission
 */
class Submit implements HttpPostActionInterface
{
    /**
     * @var RequestInterface
     */
    private $request;

    /**
     * @var JsonFactory
     */
    private $resultJsonFactory;

    /**
     * @var LoggerInterface
     */
    private $logger;

    /**
     * @param RequestInterface $request
     * @param JsonFactory $resultJsonFactory
     * @param LoggerInterface $logger
     */
    public function __construct(
        RequestInterface $request,
        JsonFactory $resultJsonFactory,
        LoggerInterface $logger
    ) {
        $this->request = $request;
        $this->resultJsonFactory = $resultJsonFactory;
        $this->logger = $logger;
    }

    /**
     * Execute action
     *
     * @return \Magento\Framework\Controller\Result\Json
     */
    public function execute()
    {
        $resultJson = $this->resultJsonFactory->create();

        if (!$this->request->isPost()) {
            return $resultJson->setData([
                'success' => false,
                'message' => __('Invalid request method.')
            ]);
        }

        try {
            $postData = $this->request->getPostValue();

            // Validate data
            $this->validateData($postData);

            // Process your data here
            // Example: Save to database, send email, etc.

            return $resultJson->setData([
                'success' => true,
                'message' => __('Your request has been submitted successfully.')
            ]);
        } catch (LocalizedException $e) {
            $this->logger->error('Widget form error: ' . $e->getMessage());
            return $resultJson->setData([
                'success' => false,
                'message' => $e->getMessage()
            ]);
        } catch (\Exception $e) {
            $this->logger->error('Widget form error: ' . $e->getMessage());
            return $resultJson->setData([
                'success' => false,
                'message' => __('An error occurred. Please try again later.')
            ]);
        }
    }

    /**
     * Validate form data
     *
     * @param array $data
     * @throws LocalizedException
     */
    private function validateData(array $data): void
    {
        if (empty($data['field_name'])) {
            throw new LocalizedException(__('Field name is required.'));
        }

        if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
            throw new LocalizedException(__('Please enter a valid email address.'));
        }
    }
}
```

**Controller Best Practices:**
- Use `HttpPostActionInterface` for POST requests
- Use `HttpGetActionInterface` for GET requests
- Return proper result objects (`JsonFactory`, `PageFactory`, `RedirectFactory`)
- Always validate input data
- Use try-catch blocks for error handling
- Log errors for debugging
- Return user-friendly error messages

## Advanced: Modal Popup Widget

For complex interactions like modal forms:

**Template with Modal:**

```php
<?php
$modalId = 'modal-' . uniqid();
?>

<div class="widget-container">
    <button type="button"
            class="action primary"
            data-mage-init='{"widgetModal": {"modalId": "<?= $escaper->escapeJs($modalId) ?>"}}'>
        <?= $escaper->escapeHtml(__('Open Modal')) ?>
    </button>
</div>

<!-- Modal Structure -->
<div id="<?= $escaper->escapeHtmlAttr($modalId) ?>"
     class="widget-modal"
     style="display: none;"
     data-role="widget-modal">
    <div class="widget-modal-overlay"></div>
    <div class="widget-modal-content">
        <div class="widget-modal-header">
            <h2><?= $escaper->escapeHtml(__('Modal Title')) ?></h2>
            <button type="button" class="widget-modal-close" aria-label="Close">
                <span>&times;</span>
            </button>
        </div>
        <div class="widget-modal-body">
            <form id="widget-form" method="post">
                <!-- Form fields -->
                <input type="text" name="field_name" required />

                <button type="submit" class="action primary">
                    <?= $escaper->escapeHtml(__('Submit')) ?>
                </button>
            </form>
        </div>
    </div>
</div>
```

**Modal JavaScript:**

**IMPORTANT:**
1. Do NOT use Magento's `Magento_Ui/js/modal/modal` component when you have custom modal HTML structure - it creates conflicts with z-index, positioning, and double overlays
2. ALWAYS move the modal element to `<body>` on initialization to prevent parent container constraints (overflow, positioning, z-index)

```javascript
define([
    'jquery'
], function ($) {
    'use strict';

    $.widget('vendor.widgetModal', {
        options: {
            modalId: ''
        },

        _create: function () {
            this._moveModalToBody();
            this._bind();
        },

        /**
         * Move modal element to body to prevent parent container constraints
         * This is CRITICAL - without this, modal will be trapped inside widget container
         */
        _moveModalToBody: function () {
            var modalElement = $('#' + this.options.modalId);

            if (modalElement.length && modalElement.parent()[0].tagName !== 'BODY') {
                // Move modal to body so it's not constrained by parent positioning
                modalElement.appendTo('body');
            }
        },

        _bind: function () {
            var self = this;

            // Open modal on button click
            this.element.on('click', function (e) {
                e.preventDefault();
                self.openModal();
            });
        },

        openModal: function () {
            var modalElement = $('#' + this.options.modalId);

            if (modalElement.length) {
                // Show modal with fade effect
                modalElement.fadeIn(300);
                $('body').addClass('modal-open');

                // Bind close button (only once)
                modalElement.find('.widget-modal-close, .action.cancel').off('click').on('click', function (e) {
                    e.preventDefault();
                    modalElement.fadeOut(300);
                    $('body').removeClass('modal-open');
                });

                // Bind overlay click (only once)
                modalElement.find('.widget-modal-overlay').off('click').on('click', function (e) {
                    e.preventDefault();
                    modalElement.fadeOut(300);
                    $('body').removeClass('modal-open');
                });

                // Bind ESC key
                $(document).off('keyup.widgetModal').on('keyup.widgetModal', function (e) {
                    if (e.key === 'Escape' || e.keyCode === 27) {
                        modalElement.fadeOut(300);
                        $('body').removeClass('modal-open');
                        $(document).off('keyup.widgetModal');
                    }
                });
            }
        }
    });

    return $.vendor.widgetModal;
});
```

**Modal CSS Styling:**

```css
/**
 * Modal Styling
 * IMPORTANT:
 * - Use very high z-index (999999) with !important to ensure modal appears above all content
 * - Many themes use high z-index values for headers, menus, etc. (10000+)
 * - Modal container and all children use position: fixed to escape parent containers
 * - Overlay uses darker background (0.7 opacity) to clearly indicate blocked content
 */
.widget-modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 999999 !important;
}

.widget-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    z-index: 999998 !important;
    cursor: pointer;
}

.widget-modal-content {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    z-index: 999999 !important;
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

/* Prevent body scroll when modal is open */
body.modal-open {
    overflow: hidden;
}

/* Ensure modal container blocks all pointer events to elements below */
.widget-modal {
    pointer-events: auto;
}

.widget-modal * {
    pointer-events: auto;
}

.widget-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 30px;
    border-bottom: 1px solid #e0e0e0;
}

.widget-modal-header h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
}

.widget-modal-close {
    background: none;
    border: none;
    font-size: 32px;
    line-height: 1;
    color: #666;
    cursor: pointer;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.3s ease;
}

.widget-modal-close:hover {
    color: #000;
}

.widget-modal-body {
    padding: 30px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .widget-modal-content {
        width: 95%;
        max-height: 95vh;
    }

    .widget-modal-header {
        padding: 15px 20px;
    }

    .widget-modal-header h2 {
        font-size: 20px;
    }

    .widget-modal-body {
        padding: 20px;
    }
}
```

## Installation and Deployment

### Installation Commands

```bash
# Enable the module
bin/magento module:enable Vendor_ModuleName

# Run setup upgrade
bin/magento setup:upgrade

# Compile dependency injection (production mode)
bin/magento setup:di:compile

# Deploy static content (production mode)
bin/magento setup:static-content:deploy -f

# Clear cache
bin/magento cache:flush
```

### Deployment Checklist

1. ✅ Module enabled
2. ✅ Database schema updated (`setup:upgrade`)
3. ✅ DI compiled (`setup:di:compile`)
4. ✅ Static content deployed
5. ✅ Cache cleared
6. ✅ Permissions checked (www-data ownership)

## Using the Widget

### Method 1: Admin Panel (CMS Editor)

1. Navigate to **Content > Pages** or **Content > Blocks**
2. Edit the desired page or block
3. Place cursor where widget should appear
4. Click **Insert Widget** button in editor toolbar
5. Select **Widget Type**: Your widget name
6. Configure widget parameters
7. Click **Insert Widget**
8. Save the page/block

### Method 2: Direct Code in CMS Content

Add widget code directly in CMS content:

```html
{{widget type="Vendor\ModuleName\Block\Widget\WidgetName"
         text_param="My Value"
         select_param="value1"
         enabled="1"}}
```

### Method 3: XML Layout Files

Add widget programmatically in layout XML:

```xml
<referenceContainer name="content">
    <block class="Vendor\ModuleName\Block\Widget\WidgetName"
           name="custom.widget"
           template="Vendor_ModuleName::widget/template.phtml">
        <arguments>
            <argument name="text_param" xsi:type="string">My Value</argument>
            <argument name="select_param" xsi:type="string">value1</argument>
            <argument name="enabled" xsi:type="boolean">true</argument>
        </arguments>
    </block>
</referenceContainer>
```

### Method 4: Programmatically in Template

Create widget block in any template:

```php
<?= $block->getLayout()
    ->createBlock(\Vendor\ModuleName\Block\Widget\WidgetName::class)
    ->setData('text_param', 'My Value')
    ->setData('enabled', true)
    ->toHtml() ?>
```

## Real-World Example: Quote Request Form Widget

Based on the `ItTools_QuoteForm` module created for LCD Screen Repair:

**Features:**
- Modal popup form
- File upload (max 3 images, 5MB each)
- Client-side validation
- AJAX submission
- Email with attachments
- Success/error messages

**Key Files:**
```
app/code/ItTools/QuoteForm/
├── Block/Widget/QuoteButton.php
├── Controller/Index/Submit.php
├── etc/widget.xml
├── etc/email_templates.xml
├── view/frontend/templates/widget/quotebutton.phtml
├── view/frontend/web/js/quote-modal.js
├── view/frontend/web/js/quote-form.js
└── view/frontend/web/css/quote-form.css
```

**Usage:**
```html
{{widget type="ItTools\QuoteForm\Block\Widget\QuoteButton"
         button_text="Get a Free Quote"
         button_class="action primary"}}
```

## Common Widget Use Cases

1. **Contact Forms** - Custom contact/inquiry forms
2. **Quote Request Buttons** - Lead generation forms
3. **Product Sliders** - Featured product carousels
4. **CTAs (Call-to-Action)** - Promotional buttons/banners
5. **Newsletter Signup** - Custom subscription forms
6. **Social Media Feeds** - Display social content
7. **Store Locators** - Find nearest store widget
8. **Calculators** - Price/shipping calculators
9. **Reviews/Testimonials** - Customer feedback display
10. **Search Boxes** - Custom search functionality

## Best Practices Summary

### Security
1. ✅ Always escape output in templates
2. ✅ Validate and sanitize all user inputs
3. ✅ Use form keys for POST requests
4. ✅ Implement CSRF protection
5. ✅ Check file types and sizes for uploads
6. ✅ Use parameterized queries (avoid SQL injection)
7. ✅ Validate email addresses properly
8. ✅ Add rate limiting for form submissions

### Performance
1. ✅ Minimize database queries in blocks
2. ✅ Use caching where appropriate
3. ✅ Lazy-load JavaScript when possible
4. ✅ Optimize CSS (remove unused styles)
5. ✅ Compress images and assets
6. ✅ Use CDN for static assets
7. ✅ Avoid blocking JavaScript

### Code Quality
1. ✅ Use strict types (`declare(strict_types=1);`)
2. ✅ Add type hints and return types
3. ✅ Follow Magento coding standards
4. ✅ Use dependency injection (no ObjectManager)
5. ✅ Add proper PHPDoc comments
6. ✅ Keep methods small and focused
7. ✅ Use constants for magic values
8. ✅ Implement proper error handling
9. ✅ Log errors appropriately
10. ✅ Write unit/integration tests

### User Experience
1. ✅ Make widgets responsive (mobile-friendly)
2. ✅ Provide clear success/error messages
3. ✅ Add loading indicators for AJAX
4. ✅ Validate forms client-side and server-side
5. ✅ Use accessibility attributes (aria-*)
6. ✅ Test keyboard navigation
7. ✅ Provide clear labels and instructions
8. ✅ Handle edge cases gracefully

### Maintainability
1. ✅ Use meaningful variable/method names
2. ✅ Keep templates clean (logic in blocks)
3. ✅ Document complex logic
4. ✅ Use configuration for settings
5. ✅ Follow single responsibility principle
6. ✅ Make code testable
7. ✅ Version control properly
8. ✅ Add README with usage instructions

## Troubleshooting

### Widget Not Appearing in Admin

**Symptoms:** Widget doesn't show in "Insert Widget" dropdown

**Solutions:**
1. Check `widget.xml` syntax (validate XML)
2. Verify module is enabled: `bin/magento module:status`
3. Clear cache: `bin/magento cache:flush`
4. Clear generated code: `rm -rf generated/code/*`
5. Check file permissions
6. Review `system.log` for errors

### Widget Not Rendering on Frontend

**Symptoms:** Widget code shows but no output

**Solutions:**
1. Verify template path in block class
2. Check template file exists at specified path
3. Clear cache: `bin/magento cache:flush`
4. Check for PHP errors in template
5. Review `exception.log` and `system.log`
6. Enable developer mode to see detailed errors

### JavaScript Not Loading

**Symptoms:** Widget functionality not working

**Solutions:**
1. Verify `requirejs-config.js` syntax
2. Check JS file path is correct
3. Clear static content: `bin/magento setup:static-content:deploy -f`
4. Check browser console for 404 errors
5. Verify file permissions
6. Check for JavaScript errors in console
7. Ensure jQuery and dependencies are loaded

### CSS Styles Not Applied

**Symptoms:** Widget appears unstyled

**Solutions:**
1. Verify CSS path in `layout/default.xml`
2. Check CSS file exists
3. Deploy static content: `bin/magento setup:static-content:deploy -f`
4. Clear browser cache
5. Check for CSS file 404 in network tab
6. Verify CSS selector specificity
7. Check for conflicting styles

### Form Submission Failing

**Symptoms:** AJAX returns errors or no response

**Solutions:**
1. Check controller route configuration
2. Verify controller implements correct interface
3. Add form key to form if using POST
4. Check network tab for actual error response
5. Review `exception.log` for server errors
6. Verify AJAX URL is correct
7. Check request/response format (JSON)
8. Ensure proper content type headers

### File Upload Issues

**Symptoms:** Files not uploading or validation fails

**Solutions:**
1. Check PHP `upload_max_filesize` and `post_max_size`
2. Verify file input has `enctype="multipart/form-data"`
3. Check file permissions on upload directory
4. Validate file mime types server-side
5. Check for JavaScript file validation logic
6. Review file size limits (client and server)
7. Check `$_FILES` array in controller

### Modal Popup Issues

**Symptoms:** Modal is half-hidden, trapped inside section/div, has z-index issues, double overlays, or positioning problems

**Root Causes:**
1. Conflict between Magento's `Magento_Ui/js/modal/modal` component and custom modal HTML structure
2. Modal element is constrained by parent container (overflow, position, z-index)

**Solutions:**
1. **CRITICAL: Move modal to body** - Add `modalElement.appendTo('body')` in widget initialization to escape parent containers
2. **DO NOT use Magento's modal component** when you already have custom modal HTML with overlay and content divs
3. Use simple jQuery `fadeIn()`/`fadeOut()` instead of `modal('openModal')`
4. Set **very high z-index (999999) with !important** on the modal container (themes often use 10000+ for headers/menus)
5. Use `position: fixed` on BOTH overlay and content (not absolute)
6. Use darker overlay background `rgba(0, 0, 0, 0.7)` to clearly block content
7. Add `body.modal-open { overflow: hidden; }` to prevent background scroll
8. Add `pointer-events: auto` to modal and children to block clicks
9. Clear static content after changes: `rm -rf pub/static/frontend/*`
10. Clear browser cache and test in incognito mode
11. Inspect competing elements with browser DevTools to find their z-index values

**Example Fix:**
```javascript
// WRONG - causes conflicts
define(['jquery', 'Magento_Ui/js/modal/modal'], function ($, modal) {
    modalElement.modal({ ... });
});

// CORRECT - simple and works
define(['jquery'], function ($) {
    modalElement.fadeIn(300);
    $('body').addClass('modal-open');
});
```

## Testing Checklist

Before deploying your widget:

### Functional Testing
- [ ] Widget appears in admin "Insert Widget" dropdown
- [ ] All parameters show correctly in admin
- [ ] Widget renders on frontend
- [ ] All parameter variations work correctly
- [ ] Form submission works (if applicable)
- [ ] Validation works client-side and server-side
- [ ] Success/error messages display correctly
- [ ] Email sending works (if applicable)

### Browser/Device Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile iOS
- [ ] Mobile Android
- [ ] Tablet

### Performance Testing
- [ ] Page load time acceptable
- [ ] No JavaScript errors in console
- [ ] No CSS conflicts with theme
- [ ] Caching works properly
- [ ] AJAX requests complete quickly

### Security Testing
- [ ] All outputs escaped properly
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] File upload validation
- [ ] Input validation/sanitization

### Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Screen reader friendly
- [ ] Proper ARIA labels
- [ ] Focus indicators visible
- [ ] Color contrast sufficient

## Reference: ItTools Module Examples

Real working examples from this codebase:

1. **ItTools_QuoteForm** (`app/code/ItTools/QuoteForm/`)
   - Modal popup widget
   - Form with file uploads
   - Email functionality
   - AJAX submission

2. **ItTools_CategorySearch** (`app/code/ItTools/CategorySearch/`)
   - Simple search widget
   - Extends existing functionality
   - Custom placeholder text parameter

Use these as reference implementations.

## Additional Resources

### Magento DevDocs
- [Widget Development](https://devdocs.magento.com/guides/v2.4/frontend-dev-guide/widgets/widget_create.html)
- [JavaScript Components](https://devdocs.magento.com/guides/v2.4/javascript-dev-guide/javascript/js_init.html)
- [Templates](https://devdocs.magento.com/guides/v2.4/frontend-dev-guide/templates/template-overview.html)

### Code Examples
- Magento core widgets: `vendor/magento/module-widget/`
- Magento CMS widgets: `vendor/magento/module-cms/Block/Widget/`
- Catalog widgets: `vendor/magento/module-catalog/Block/Widget/`

## Version Compatibility

This skill is compatible with:
- Magento Open Source 2.3.x - 2.4.x
- Adobe Commerce 2.3.x - 2.4.x
- Mage-OS (Magento fork)

Not compatible with:
- Hyvä themes (use hyva-tailwind-integration skill instead)
- Magento 1.x

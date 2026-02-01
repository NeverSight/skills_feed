---
name: create-frontend-controller
description: Creates a frontend controller action in Magento 2 for the storefront. Use when building custom frontend pages, AJAX endpoints, form submission handlers, or API-like endpoints for JavaScript.
---

# Create Frontend Controller Action

## Description
This skill guides you through creating a frontend controller action in Adobe Commerce/Magento 2 (Mage-OS). Frontend controllers handle HTTP requests and return responses for the storefront area.

## When to Use
- Creating custom frontend endpoints for AJAX requests
- Building custom pages or actions accessible to customers
- Implementing custom form submissions
- Creating API-like endpoints for frontend JavaScript

## Prerequisites
- Existing Magento 2 module with proper structure
- Understanding of dependency injection
- Knowledge of Magento routing system

## Best Practices from Adobe Documentation

### 1. Use HTTP Method-Specific Interfaces
Always implement HTTP method-specific action interfaces:
- `HttpGetActionInterface` - For GET requests
- `HttpPostActionInterface` - For POST requests
- Both interfaces can be implemented for endpoints accepting multiple methods

### 2. Use Strict Types
Always declare strict types at the top of controller files:
```php
declare(strict_types=1);
```

### 3. Use Dependency Injection
Never use ObjectManager directly. Always inject dependencies via constructor.

### 4. Return Proper Result Objects
Use result factories to return appropriate response types:
- `JsonFactory` for JSON responses
- `PageFactory` for full page responses
- `RedirectFactory` for redirects
- `RawFactory` for raw output

## Step-by-Step Implementation

### Step 1: Create routes.xml
Define your route configuration in `etc/frontend/routes.xml`:

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="standard">
        <route id="yourmodule" frontName="yourmodule">
            <module name="Vendor_ModuleName" />
        </route>
    </router>
</config>
```

**URL Structure:** `https://yourdomain.com/{frontName}/{controller}/{action}`

### Step 2: Create Controller Directory Structure
Create the controller directory:
```
app/code/Vendor/ModuleName/Controller/
    └── ControllerName/
        └── ActionName.php
```

**Example:** `Controller/Custom/Search.php` maps to URL: `/yourmodule/custom/search`

### Step 3: Create Controller Action Class

#### Example 1: JSON Response Controller (GET/POST)
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\ModuleName\Controller\ControllerName;

use Magento\Framework\App\Action\HttpGetActionInterface;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\App\RequestInterface;
use Magento\Framework\Controller\Result\JsonFactory;
use Magento\Framework\Controller\ResultInterface;

class ActionName implements HttpGetActionInterface, HttpPostActionInterface
{
    /**
     * @var JsonFactory
     */
    private JsonFactory $resultJsonFactory;

    /**
     * @var RequestInterface
     */
    private RequestInterface $request;

    /**
     * Constructor
     *
     * @param JsonFactory $resultJsonFactory
     * @param RequestInterface $request
     */
    public function __construct(
        JsonFactory $resultJsonFactory,
        RequestInterface $request
    ) {
        $this->resultJsonFactory = $resultJsonFactory;
        $this->request = $request;
    }

    /**
     * Execute action
     *
     * @return ResultInterface
     */
    public function execute(): ResultInterface
    {
        // Get request parameters
        $searchKey = $this->request->getParam('searchKey');
        $page = (int)$this->request->getParam('page', 1);
        $limit = (int)$this->request->getParam('limit', 10);

        // Your business logic here
        $data = [
            'success' => true,
            'message' => 'Action completed successfully',
            'data' => [
                'searchKey' => $searchKey,
                'page' => $page,
                'limit' => $limit
            ]
        ];

        // Return JSON response
        $resultJson = $this->resultJsonFactory->create();
        return $resultJson->setData($data);
    }
}
```

#### Example 2: Page Response Controller (GET only)
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\ModuleName\Controller\ControllerName;

use Magento\Framework\App\Action\HttpGetActionInterface;
use Magento\Framework\View\Result\PageFactory;
use Magento\Framework\View\Result\Page;

class ActionName implements HttpGetActionInterface
{
    /**
     * @var PageFactory
     */
    private PageFactory $resultPageFactory;

    /**
     * Constructor
     *
     * @param PageFactory $resultPageFactory
     */
    public function __construct(
        PageFactory $resultPageFactory
    ) {
        $this->resultPageFactory = $resultPageFactory;
    }

    /**
     * Execute action
     *
     * @return Page
     */
    public function execute(): Page
    {
        $resultPage = $this->resultPageFactory->create();
        $resultPage->getConfig()->getTitle()->set(__('Page Title'));

        return $resultPage;
    }
}
```

#### Example 3: Redirect Response Controller
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\ModuleName\Controller\ControllerName;

use Magento\Framework\App\Action\HttpGetActionInterface;
use Magento\Framework\Controller\Result\RedirectFactory;
use Magento\Framework\Controller\ResultInterface;

class ActionName implements HttpGetActionInterface
{
    /**
     * @var RedirectFactory
     */
    private RedirectFactory $resultRedirectFactory;

    /**
     * Constructor
     *
     * @param RedirectFactory $resultRedirectFactory
     */
    public function __construct(
        RedirectFactory $resultRedirectFactory
    ) {
        $this->resultRedirectFactory = $resultRedirectFactory;
    }

    /**
     * Execute action
     *
     * @return ResultInterface
     */
    public function execute(): ResultInterface
    {
        $resultRedirect = $this->resultRedirectFactory->create();
        $resultRedirect->setPath('customer/account');

        return $resultRedirect;
    }
}
```

### Step 4: Create Layout XML (For Page Controllers)
If returning a page, create layout XML: `view/frontend/layout/yourmodule_controllername_actionname.xml`

```xml
<?xml version="1.0"?>
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
    <head>
        <title>Page Title</title>
    </head>
    <body>
        <referenceContainer name="content">
            <block class="Vendor\ModuleName\Block\CustomBlock"
                   name="custom.block"
                   template="Vendor_ModuleName::custom/template.phtml"/>
        </referenceContainer>
    </body>
</page>
```

### Step 5: Create Template (For Page Controllers)
Create template file: `view/frontend/templates/custom/template.phtml`

```php
<?php
/**
 * @var \Magento\Framework\View\Element\Template $block
 * @var \Magento\Framework\Escaper $escaper
 */
?>
<div class="custom-content">
    <h1><?= $escaper->escapeHtml(__('Custom Page')) ?></h1>
    <p><?= $escaper->escapeHtml(__('Your content here')) ?></p>
</div>
```

### Step 6: Clear Cache and Test
```bash
# Clear cache
ddev exec bin/magento cache:flush

# Upgrade setup (if new module)
ddev exec bin/magento setup:upgrade

# Test the endpoint
curl https://ntotank.ddev.site/yourmodule/controllername/actionname
```

## Common Patterns

### Pattern 1: AJAX Endpoint with Collection
```php
public function execute(): ResultInterface
{
    $searchKey = $this->request->getParam('searchKey');

    // Load collection
    $collection = $this->collectionFactory->create();
    $collection->addFieldToFilter('name', ['like' => "%{$searchKey}%"]);
    $collection->setPageSize(10);

    // Format results
    $results = [];
    foreach ($collection as $item) {
        $results[] = [
            'id' => $item->getId(),
            'name' => $item->getName(),
            'url' => $item->getUrl()
        ];
    }

    $resultJson = $this->resultJsonFactory->create();
    return $resultJson->setData([
        'items' => $results,
        'total' => $collection->getSize()
    ]);
}
```

### Pattern 2: Form Submission Handler
```php
public function execute(): ResultInterface
{
    if (!$this->request->isPost()) {
        $resultRedirect = $this->resultRedirectFactory->create();
        return $resultRedirect->setPath('*/*/');
    }

    try {
        // Validate CSRF token (automatically done by Magento)
        $formData = $this->request->getPostValue();

        // Process form data
        // ... your logic here

        $this->messageManager->addSuccessMessage(__('Form submitted successfully.'));

        $resultRedirect = $this->resultRedirectFactory->create();
        return $resultRedirect->setPath('*/*/success');

    } catch (\Exception $e) {
        $this->messageManager->addErrorMessage($e->getMessage());

        $resultRedirect = $this->resultRedirectFactory->create();
        return $resultRedirect->setPath('*/*/');
    }
}
```

### Pattern 3: Customer Authentication Check
```php
private \Magento\Customer\Model\Session $customerSession;

public function execute(): ResultInterface
{
    if (!$this->customerSession->isLoggedIn()) {
        $resultRedirect = $this->resultRedirectFactory->create();
        $resultRedirect->setPath('customer/account/login');
        return $resultRedirect;
    }

    // Continue with authenticated logic
    // ...
}
```

## Testing

### Unit Test Example
Create: `Test/Unit/Controller/ControllerName/ActionNameTest.php`

```php
<?php

declare(strict_types=1);

namespace Vendor\ModuleName\Test\Unit\Controller\ControllerName;

use PHPUnit\Framework\TestCase;
use Vendor\ModuleName\Controller\ControllerName\ActionName;

class ActionNameTest extends TestCase
{
    public function testExecuteReturnsJsonResult(): void
    {
        // Setup mocks
        $resultJsonFactory = $this->createMock(\Magento\Framework\Controller\Result\JsonFactory::class);
        $request = $this->createMock(\Magento\Framework\App\RequestInterface::class);

        // Create controller instance
        $controller = new ActionName($resultJsonFactory, $request);

        // Execute and assert
        $result = $controller->execute();
        $this->assertInstanceOf(\Magento\Framework\Controller\ResultInterface::class, $result);
    }
}
```

## Troubleshooting

### Issue: 404 Not Found
- Check `routes.xml` is in correct location (`etc/frontend/routes.xml`)
- Verify frontName is unique
- Run `ddev exec bin/magento setup:upgrade`
- Clear cache: `ddev exec bin/magento cache:flush`

### Issue: Controller Not Loading
- Check class namespace matches directory structure
- Ensure controller implements HttpGetActionInterface or HttpPostActionInterface
- Check file naming: Controller file must match class name exactly

### Issue: JSON Response Not Working
- Ensure you're returning JsonFactory result
- Check Content-Type header is set correctly
- Verify no output before returning result

## References
- Adobe Commerce Frontend Core Documentation: https://github.com/adobedocs/commerce-frontend-core
- Magento 2 Routing: https://developer.adobe.com/commerce/php/architecture/modules/routing/
- Controller Action Interfaces: Use HttpGetActionInterface and HttpPostActionInterface for modern Magento 2

## NTOTanks-Specific Notes
- For AJAX endpoints, follow the pattern used in `ProxiBlue_SearchDynaTable`
- Integrate with Alpine.js on frontend using `x-data` and `fetch()` calls
- Use ViewModels to prepare data for Alpine.js consumption
- Follow PSR-12 coding standards
- Always use `ddev exec` prefix for Magento CLI commands

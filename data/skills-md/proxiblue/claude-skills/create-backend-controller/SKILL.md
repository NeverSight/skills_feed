---
name: create-backend-controller
description: Creates a backend (adminhtml) controller action in Magento 2 with proper ACL, routing, authorization, and admin UI integration. Use when building admin pages, AJAX endpoints, form handlers, or mass actions.
---

# Create Backend (Adminhtml) Controller Action

## Description
This skill guides you through creating a backend controller action in Adobe Commerce/Magento 2 (Mage-OS) for the admin area. Backend controllers handle HTTP requests in the Magento admin panel with proper authorization and ACL (Access Control List) integration.

## When to Use
- Creating custom admin pages or sections
- Building AJAX endpoints for admin UI components
- Implementing admin form submission handlers
- Creating mass actions for grid components
- Building custom admin operations requiring authorization

## Prerequisites
- Existing Magento 2 module with proper structure
- Understanding of ACL (Access Control List) system
- Knowledge of Magento routing and dependency injection
- Understanding of admin sessions and authorization

## Best Practices from Adobe Documentation

### 1. Extend Backend Action Base Class
Backend controllers should extend `\Magento\Backend\App\Action`:
```php
class ActionName extends \Magento\Backend\App\Action implements HttpGetActionInterface
```

### 2. Implement HTTP Method-Specific Interfaces
Always implement HTTP method-specific action interfaces:
- `HttpGetActionInterface` - For GET requests
- `HttpPostActionInterface` - For POST requests
- Both interfaces can be implemented for endpoints accepting multiple methods

### 3. Define ACL Resource Constant
Every backend controller must define the `ADMIN_RESOURCE` constant:
```php
const ADMIN_RESOURCE = 'Vendor_Module::resource_name';
```

### 4. Use Strict Types
Always declare strict types at the top of controller files:
```php
declare(strict_types=1);
```

### 5. Authorization is Automatic
The `\Magento\Backend\App\Action` base class automatically checks the `ADMIN_RESOURCE` constant against the current admin user's permissions via the `_isAllowed()` method.

## Step-by-Step Implementation

### Step 1: Define ACL Resources (acl.xml)
Create `etc/acl.xml` to define access control resources:

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Acl/etc/acl.xsd">
    <acl>
        <resources>
            <resource id="Magento_Backend::admin">
                <!-- Main module menu resource -->
                <resource id="Vendor_Module::menu" title="Module Name" sortOrder="100">
                    <!-- Sub-resource for entities -->
                    <resource id="Vendor_Module::entity" title="Manage Entities" sortOrder="10">
                        <resource id="Vendor_Module::entity_save" title="Save Entity" sortOrder="10" />
                        <resource id="Vendor_Module::entity_delete" title="Delete Entity" sortOrder="20" />
                    </resource>
                    <!-- Configuration resource -->
                    <resource id="Vendor_Module::config" title="Configuration" sortOrder="20" />
                </resource>
            </resource>
        </resources>
    </acl>
</config>
```

**ACL Resource Structure:**
- Each resource has a unique ID (e.g., `Vendor_Module::entity_save`)
- Resources are hierarchical - child resources inherit parent permissions
- Admin users must have permission for the resource to access the controller

### Step 2: Create Backend Routes (routes.xml)
Define your route configuration in `etc/adminhtml/routes.xml`:

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="admin">
        <route id="vendormodule" frontName="vendormodule">
            <module name="Vendor_Module" before="Magento_Backend" />
        </route>
    </router>
</config>
```

**URL Structure:** `https://yourdomain.com/admin/{frontName}/{controller}/{action}`

**Example:** With frontName `vendormodule`, the URL would be:
`https://yourdomain.com/admin/vendormodule/entity/index`

### Step 3: Create Admin Menu (menu.xml) [Optional]
Create `etc/adminhtml/menu.xml` to add menu items:

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Backend:etc/menu.xsd">
    <menu>
        <!-- Top-level menu -->
        <add id="Vendor_Module::menu"
             title="Module Name"
             module="Vendor_Module"
             sortOrder="100"
             resource="Vendor_Module::menu"/>
        
        <!-- Sub-menu item linking to controller -->
        <add id="Vendor_Module::entity"
             title="Manage Entities"
             module="Vendor_Module"
             sortOrder="10"
             parent="Vendor_Module::menu"
             action="vendormodule/entity/index"
             resource="Vendor_Module::entity"/>
        
        <!-- Configuration menu item -->
        <add id="Vendor_Module::settings"
             title="Settings"
             module="Vendor_Module"
             sortOrder="20"
             parent="Vendor_Module::menu"
             action="adminhtml/system_config/edit/section/vendormodule"
             resource="Vendor_Module::config"/>
    </menu>
</config>
```

### Step 4: Create Controller Directory Structure
Create the controller directory:
```
app/code/Vendor/ModuleName/Controller/Adminhtml/
    └── ControllerName/
        └── ActionName.php
```

**Example:** `Controller/Adminhtml/Entity/Index.php` maps to URL: `/admin/vendormodule/entity/index`

### Step 5: Create Backend Controller Action Class

#### Example 1: Admin Grid Page Controller
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\Module\Controller\Adminhtml\Entity;

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpGetActionInterface;
use Magento\Framework\View\Result\PageFactory;
use Magento\Framework\View\Result\Page;

class Index extends Action implements HttpGetActionInterface
{
    /**
     * Authorization level of a basic admin session
     *
     * @see _isAllowed()
     */
    const ADMIN_RESOURCE = 'Vendor_Module::entity';

    /**
     * @var PageFactory
     */
    private PageFactory $resultPageFactory;

    /**
     * Constructor
     *
     * @param Context $context
     * @param PageFactory $resultPageFactory
     */
    public function __construct(
        Context $context,
        PageFactory $resultPageFactory
    ) {
        parent::__construct($context);
        $this->resultPageFactory = $resultPageFactory;
    }

    /**
     * Execute action
     *
     * @return Page
     */
    public function execute(): Page
    {
        /** @var Page $resultPage */
        $resultPage = $this->resultPageFactory->create();
        $resultPage->setActiveMenu('Vendor_Module::entity');
        $resultPage->getConfig()->getTitle()->prepend(__('Manage Entities'));

        return $resultPage;
    }
}
```

#### Example 2: JSON Response Controller (AJAX Endpoint)
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\Module\Controller\Adminhtml\Entity;

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpGetActionInterface;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\Result\JsonFactory;
use Magento\Framework\Controller\ResultInterface;
use Vendor\Module\Model\ResourceModel\Entity\CollectionFactory;

class Search extends Action implements HttpGetActionInterface, HttpPostActionInterface
{
    /**
     * Authorization level of a basic admin session
     *
     * @see _isAllowed()
     */
    const ADMIN_RESOURCE = 'Vendor_Module::entity';

    /**
     * @var JsonFactory
     */
    private JsonFactory $resultJsonFactory;

    /**
     * @var CollectionFactory
     */
    private CollectionFactory $collectionFactory;

    /**
     * Constructor
     *
     * @param Context $context
     * @param JsonFactory $resultJsonFactory
     * @param CollectionFactory $collectionFactory
     */
    public function __construct(
        Context $context,
        JsonFactory $resultJsonFactory,
        CollectionFactory $collectionFactory
    ) {
        parent::__construct($context);
        $this->resultJsonFactory = $resultJsonFactory;
        $this->collectionFactory = $collectionFactory;
    }

    /**
     * Execute action
     *
     * @return ResultInterface
     */
    public function execute(): ResultInterface
    {
        $searchKey = $this->getRequest()->getParam('searchKey');
        $pageNum = (int)$this->getRequest()->getParam('page', 1);
        $limit = (int)$this->getRequest()->getParam('limit', 10);

        /** @var \Vendor\Module\Model\ResourceModel\Entity\Collection $collection */
        $collection = $this->collectionFactory->create();
        $collection->addFieldToFilter('name', ['like' => "%{$searchKey}%"]);
        $collection->setCurPage($pageNum)->setPageSize($limit);

        $totalValues = $collection->getSize();

        $results = [];
        foreach ($collection as $entity) {
            $results[$entity->getId()] = [
                'value' => $entity->getId(),
                'label' => $entity->getName(),
                'identifier' => sprintf(__('ID: %s'), $entity->getId())
            ];
        }

        /** @var \Magento\Framework\Controller\Result\Json $resultJson */
        $resultJson = $this->resultJsonFactory->create();
        return $resultJson->setData([
            'options' => $results,
            'total' => empty($results) ? 0 : $totalValues
        ]);
    }
}
```

#### Example 3: Save Action with Form Key Validation
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\Module\Controller\Adminhtml\Entity;

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\ResultInterface;
use Magento\Framework\Exception\LocalizedException;
use Vendor\Module\Api\EntityRepositoryInterface;
use Vendor\Module\Model\EntityFactory;

class Save extends Action implements HttpPostActionInterface
{
    /**
     * Authorization level of a basic admin session
     *
     * @see _isAllowed()
     */
    const ADMIN_RESOURCE = 'Vendor_Module::entity_save';

    /**
     * @var EntityFactory
     */
    private EntityFactory $entityFactory;

    /**
     * @var EntityRepositoryInterface
     */
    private EntityRepositoryInterface $entityRepository;

    /**
     * Constructor
     *
     * @param Context $context
     * @param EntityFactory $entityFactory
     * @param EntityRepositoryInterface $entityRepository
     */
    public function __construct(
        Context $context,
        EntityFactory $entityFactory,
        EntityRepositoryInterface $entityRepository
    ) {
        parent::__construct($context);
        $this->entityFactory = $entityFactory;
        $this->entityRepository = $entityRepository;
    }

    /**
     * Execute action
     *
     * @return ResultInterface
     */
    public function execute(): ResultInterface
    {
        $resultRedirect = $this->resultRedirectFactory->create();

        $data = $this->getRequest()->getPostValue();
        if (!$data) {
            $this->messageManager->addErrorMessage(__('No data to save.'));
            return $resultRedirect->setPath('*/*/');
        }

        try {
            $entityId = $this->getRequest()->getParam('entity_id');
            
            if ($entityId) {
                $entity = $this->entityRepository->getById($entityId);
            } else {
                $entity = $this->entityFactory->create();
            }

            $entity->setData($data);
            $this->entityRepository->save($entity);

            $this->messageManager->addSuccessMessage(__('Entity saved successfully.'));

            if ($this->getRequest()->getParam('back')) {
                return $resultRedirect->setPath('*/*/edit', ['id' => $entity->getId()]);
            }

            return $resultRedirect->setPath('*/*/');

        } catch (LocalizedException $e) {
            $this->messageManager->addErrorMessage($e->getMessage());
        } catch (\Exception $e) {
            $this->messageManager->addExceptionMessage(
                $e,
                __('Something went wrong while saving the entity.')
            );
        }

        return $resultRedirect->setPath('*/*/edit', ['id' => $entityId ?? null]);
    }
}
```

#### Example 4: Mass Action Controller
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\Module\Controller\Adminhtml\Entity;

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\ResultFactory;
use Magento\Framework\Controller\ResultInterface;
use Magento\Framework\Exception\LocalizedException;
use Vendor\Module\Api\EntityRepositoryInterface;
use Vendor\Module\Model\ResourceModel\Entity\CollectionFactory;
use Magento\Ui\Component\MassAction\Filter;

class MassDelete extends Action implements HttpPostActionInterface
{
    /**
     * Authorization level of a basic admin session
     *
     * @see _isAllowed()
     */
    const ADMIN_RESOURCE = 'Vendor_Module::entity_delete';

    /**
     * @var Filter
     */
    private Filter $filter;

    /**
     * @var CollectionFactory
     */
    private CollectionFactory $collectionFactory;

    /**
     * @var EntityRepositoryInterface
     */
    private EntityRepositoryInterface $entityRepository;

    /**
     * Constructor
     *
     * @param Context $context
     * @param Filter $filter
     * @param CollectionFactory $collectionFactory
     * @param EntityRepositoryInterface $entityRepository
     */
    public function __construct(
        Context $context,
        Filter $filter,
        CollectionFactory $collectionFactory,
        EntityRepositoryInterface $entityRepository
    ) {
        parent::__construct($context);
        $this->filter = $filter;
        $this->collectionFactory = $collectionFactory;
        $this->entityRepository = $entityRepository;
    }

    /**
     * Execute action
     *
     * @return ResultInterface
     */
    public function execute(): ResultInterface
    {
        try {
            $collection = $this->filter->getCollection($this->collectionFactory->create());
            $deletedCount = 0;

            foreach ($collection as $entity) {
                $this->entityRepository->delete($entity);
                $deletedCount++;
            }

            $this->messageManager->addSuccessMessage(
                __('A total of %1 record(s) have been deleted.', $deletedCount)
            );

        } catch (LocalizedException $e) {
            $this->messageManager->addErrorMessage($e->getMessage());
        } catch (\Exception $e) {
            $this->messageManager->addExceptionMessage(
                $e,
                __('An error occurred while deleting records.')
            );
        }

        /** @var \Magento\Backend\Model\View\Result\Redirect $resultRedirect */
        $resultRedirect = $this->resultFactory->create(ResultFactory::TYPE_REDIRECT);
        return $resultRedirect->setPath('*/*/');
    }
}
```

#### Example 5: Delete Action
```php
<?php
/**
 * Copyright © [Year] [Your Company]
 * All rights reserved.
 */

declare(strict_types=1);

namespace Vendor\Module\Controller\Adminhtml\Entity;

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\ResultInterface;
use Magento\Framework\Exception\LocalizedException;
use Vendor\Module\Api\EntityRepositoryInterface;

class Delete extends Action implements HttpPostActionInterface
{
    /**
     * Authorization level of a basic admin session
     *
     * @see _isAllowed()
     */
    const ADMIN_RESOURCE = 'Vendor_Module::entity_delete';

    /**
     * @var EntityRepositoryInterface
     */
    private EntityRepositoryInterface $entityRepository;

    /**
     * Constructor
     *
     * @param Context $context
     * @param EntityRepositoryInterface $entityRepository
     */
    public function __construct(
        Context $context,
        EntityRepositoryInterface $entityRepository
    ) {
        parent::__construct($context);
        $this->entityRepository = $entityRepository;
    }

    /**
     * Execute action
     *
     * @return ResultInterface
     */
    public function execute(): ResultInterface
    {
        $resultRedirect = $this->resultRedirectFactory->create();
        $id = $this->getRequest()->getParam('id');

        if (!$id) {
            $this->messageManager->addErrorMessage(__('Entity ID is required.'));
            return $resultRedirect->setPath('*/*/');
        }

        try {
            $this->entityRepository->deleteById((int)$id);
            $this->messageManager->addSuccessMessage(__('Entity deleted successfully.'));
        } catch (LocalizedException $e) {
            $this->messageManager->addErrorMessage($e->getMessage());
        } catch (\Exception $e) {
            $this->messageManager->addExceptionMessage(
                $e,
                __('An error occurred while deleting the entity.')
            );
        }

        return $resultRedirect->setPath('*/*/');
    }
}
```

### Step 6: Create Layout XML
Create layout XML: `view/adminhtml/layout/vendormodule_entity_index.xml`

```xml
<?xml version="1.0"?>
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
    <update handle="styles"/>
    <body>
        <referenceContainer name="content">
            <uiComponent name="vendor_module_entity_listing"/>
        </referenceContainer>
    </body>
</page>
```

### Step 7: Clear Cache and Test
```bash
# Clear cache
ddev exec bin/magento cache:flush

# Upgrade setup (for new ACL resources)
ddev exec bin/magento setup:upgrade

# Compile if needed
ddev exec bin/magento setup:di:compile

# Test access to the admin controller
# Navigate to: https://ntotank.ddev.site/admin/vendormodule/entity/index
```

## Common Patterns

### Pattern 1: Inline Edit (AJAX Save)
```php
public function execute(): ResultInterface
{
    $resultJson = $this->resultJsonFactory->create();

    $items = $this->getRequest()->getParam('items', []);
    if (empty($items)) {
        return $resultJson->setData([
            'messages' => [__('Please correct the data sent.')],
            'error' => true
        ]);
    }

    foreach ($items as $entityId => $entityData) {
        try {
            $entity = $this->entityRepository->getById($entityId);
            $entity->setData(array_merge($entity->getData(), $entityData));
            $this->entityRepository->save($entity);
        } catch (\Exception $e) {
            return $resultJson->setData([
                'messages' => [$e->getMessage()],
                'error' => true
            ]);
        }
    }

    return $resultJson->setData([
        'messages' => [__('Records saved.')],
        'error' => false
    ]);
}
```

### Pattern 2: Custom Authorization Check
```php
/**
 * Check if admin has permission
 *
 * @return bool
 */
protected function _isAllowed(): bool
{
    // Custom authorization logic
    $isAllowed = $this->_authorization->isAllowed('Vendor_Module::entity');
    
    // Additional custom checks
    if ($isAllowed && $this->getRequest()->getParam('special_flag')) {
        $isAllowed = $this->_authorization->isAllowed('Vendor_Module::special_permission');
    }
    
    return $isAllowed;
}
```

### Pattern 3: File Upload in Admin Form
```php
public function execute(): ResultInterface
{
    $data = $this->getRequest()->getPostValue();
    
    // Handle file upload
    if (isset($_FILES['image']) && $_FILES['image']['name']) {
        try {
            $uploader = $this->uploaderFactory->create(['fileId' => 'image']);
            $uploader->setAllowedExtensions(['jpg', 'jpeg', 'gif', 'png']);
            $uploader->setAllowRenameFiles(true);
            $uploader->setFilesDispersion(true);
            
            $result = $uploader->save(
                $this->mediaDirectory->getAbsolutePath('vendor_module/entity/')
            );
            
            $data['image'] = 'vendor_module/entity' . $result['file'];
        } catch (\Exception $e) {
            $this->messageManager->addErrorMessage($e->getMessage());
        }
    }
    
    // Continue with save logic...
}
```

## Testing Admin Controllers

### Unit Test Example
Create: `Test/Unit/Controller/Adminhtml/Entity/SaveTest.php`

```php
<?php

declare(strict_types=1);

namespace Vendor\Module\Test\Unit\Controller\Adminhtml\Entity;

use PHPUnit\Framework\TestCase;
use Vendor\Module\Controller\Adminhtml\Entity\Save;

class SaveTest extends TestCase
{
    public function testExecuteWithValidData(): void
    {
        // Setup mocks
        $context = $this->createMock(\Magento\Backend\App\Action\Context::class);
        $entityFactory = $this->createMock(\Vendor\Module\Model\EntityFactory::class);
        $entityRepository = $this->createMock(\Vendor\Module\Api\EntityRepositoryInterface::class);

        // Create controller instance
        $controller = new Save($context, $entityFactory, $entityRepository);

        // Test execution
        // Add assertions here
    }
}
```

## Troubleshooting

### Issue: Access Denied (403)
- Check ACL resource is defined in `etc/acl.xml`
- Verify `ADMIN_RESOURCE` constant matches ACL resource ID
- Ensure admin user role has permission for the resource
- Run `ddev exec bin/magento cache:flush`
- Check Stores > Configuration > Admin > Admin Base URL

### Issue: 404 Not Found
- Verify `routes.xml` is in `etc/adminhtml/` (not `etc/frontend/`)
- Check frontName is unique and doesn't conflict
- Ensure controller extends `\Magento\Backend\App\Action`
- Run `ddev exec bin/magento setup:upgrade`

### Issue: Form Key Validation Failed
- Ensure form includes form key: `<?= $block->getFormKey() ?>`
- POST requests automatically validate form keys
- For AJAX, include form key in data

### Issue: Menu Not Showing
- Check `menu.xml` is in `etc/adminhtml/`
- Verify ACL resource permissions
- Clear admin cache: `ddev exec bin/magento cache:clean config`
- Check admin user has permission to resource

## Security Best Practices

1. **Always Define ACL Resources**: Never use `const ADMIN_RESOURCE = 'Magento_Backend::admin'` for production controllers
2. **Validate Input**: Use input validators and filters
3. **Use Form Keys**: Magento automatically validates form keys for POST requests
4. **Escape Output**: Use `$escaper->escapeHtml()` in templates
5. **Check Permissions**: Let `_isAllowed()` handle authorization
6. **Use Type Hints**: Ensure strict types are declared
7. **Log Sensitive Actions**: Use logger for delete/update operations

## References
- Adobe Commerce Frontend Core: https://github.com/adobedocs/commerce-frontend-core
- Magento 2 Backend Development: https://developer.adobe.com/commerce/php/development/components/
- ACL Documentation: https://developer.adobe.com/commerce/php/tutorials/backend/create-access-control-list-rule/
- Admin UI Components: https://developer.adobe.com/commerce/frontend-core/ui-components/

## NTOTanks-Specific Notes
- Follow PSR-12 coding standards
- Use `ddev exec` prefix for all Magento CLI commands
- Backend controllers integrate with Hyvä Admin module for UI components
- Test admin controllers after clearing cache and recompiling
- Check admin user permissions in System > User Roles

---
name: typo3-powermail
description: >-
  Expert guidance on TYPO3 Powermail 13+ form extension. Creating forms, custom finishers,
  validators, spam protection, ViewHelpers, PSR-14 events, TypoScript configuration, email
  templates, backend modules, and extension development. Use when working with powermail
  forms, mail handling, form validation, or extending powermail functionality.
compatibility: TYPO3 13.0 - 14.x
metadata:
  version: "1.0.0"
  related_skills:
    - typo3-datahandler
    - typo3-content-blocks
    - typo3-testing
---

# TYPO3 Powermail Development

> **Compatibility:** TYPO3 v13.x and v14.x with Powermail 13.x
> All code examples target PHP 8.2+ and TYPO3 v13/v14.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Do not reinvent what TYPO3 already provides. Always verify that the APIs and methods you use exist and are not deprecated in your target TYPO3 version (v13 or v14) by checking the official TYPO3 documentation.

> **Supplements:**
> - [SKILL-CONDITIONS.md](SKILL-CONDITIONS.md) - Conditional field/page visibility (powermail_cond)
> - [SKILL-PHP84.md](SKILL-PHP84.md) - PHP 8.4 patterns (property hooks, asymmetric visibility, new array functions)
> - [SKILL-EXAMPLES.md](SKILL-EXAMPLES.md) - Multi-step shop form with Austrian legal types, DDEV SQL + DataHandler CLI

## 1. Architecture Overview

### Domain Model Hierarchy

```
Form (tx_powermail_domain_model_form)
 └── Page (tx_powermail_domain_model_page)
      └── Field (tx_powermail_domain_model_field)

Mail (tx_powermail_domain_model_mail)
 └── Answer (tx_powermail_domain_model_answer)
      └── references Field
```

### Plugin Registration

- **Pi1** (cached/uncached): `form`, `create`, `confirmation`, `optinConfirm`, `disclaimer`
- **Pi5** (uncached): `marketing` (AJAX tracking)

### Composer

```bash
composer require in2code/powermail
```

Requires: PHP ^8.2, TYPO3 ^13.4, ext-json, ext-gd, ext-fileinfo, ext-curl

## 2. Field Types

| Type | Key | Value Type | Notes |
|------|-----|------------|-------|
| Text | `input` | TEXT (0) | Standard input |
| Textarea | `textarea` | TEXT (0) | Multi-line |
| Select | `select` | TEXT/ARRAY (0/1) | Multiselect possible |
| Checkbox | `check` | ARRAY (1) | Multiple values |
| Radio | `radio` | TEXT (0) | Single selection |
| Submit | `submit` | — | Form submit button |
| Captcha | `captcha` | TEXT (0) | Built-in CAPTCHA |
| Reset | `reset` | — | Form reset button |
| Static text | `text` | — | Display only |
| Content element | `content` | — | CE reference |
| HTML | `html` | TEXT (0) | Raw HTML |
| Password | `password` | PASSWORD (4) | Hashed storage |
| File upload | `file` | UPLOAD (3) | File attachments |
| Hidden | `hidden` | TEXT (0) | Hidden input |
| Date | `date` | DATE (2) | Datepicker |
| Country | `country` | TEXT (0) | Country selector |
| Location | `location` | TEXT (0) | Geolocation |
| TypoScript | `typoscript` | TEXT (0) | TS-generated content |

### Answer Value Types

```php
Answer::VALUE_TYPE_TEXT     = 0;  // String values
Answer::VALUE_TYPE_ARRAY    = 1;  // JSON-encoded arrays (checkboxes, multiselect)
Answer::VALUE_TYPE_DATE     = 2;  // Timestamps
Answer::VALUE_TYPE_UPLOAD   = 3;  // File references
Answer::VALUE_TYPE_PASSWORD = 4;  // Hashed passwords
```

## 3. TypoScript Configuration

### Essential Settings

```typoscript
plugin.tx_powermail {
    settings {
        setup {
            # Form settings
            main {
                pid = {$plugin.tx_powermail.settings.main.pid}
                form = {$plugin.tx_powermail.settings.main.form}
                confirmation = 0
                optin = 0
                morestep = 0
            }

            # Receiver mail
            receiver {
                enable = 1
                subject = Mail from {firstname} {lastname}
                body = A new mail from your website
                senderNameField = firstname
                senderEmailField = email
                # Override receiver: receiver.overwrite.email = admin@example.com
                # Attach uploads: receiver.attachment = 1
                # Add CC: receiver.overwrite.cc = copy@example.com
            }

            # Sender confirmation mail
            sender {
                enable = 1
                subject = Thank you for your message
                body = We received your submission
                senderName = Website
                senderEmail = noreply@example.com
            }

            # Double Opt-In
            optin {
                subject = Please confirm your submission
                senderName = Website
                senderEmail = noreply@example.com
            }

            # Thank you page
            thx {
                redirect = # Page UID for redirect after submit
            }

            # Spam protection
            spamshield {
                _enable = 1
                indicator {
                    honeypod = 5
                    link = 3
                    name = 3
                    session = 1
                    unique = 2
                    blacklistString = 7
                    blacklistIp = 7
                    rateLimit = 10
                }
                # Factor threshold (0-100): reject if >=
                factor = 75
            }

            # Validation
            misc {
                htmlForLabels = 1
                showOnlyFilledValues = 1
                ajaxSubmit = 0
                file {
                    folder = uploads/tx_powermail/
                    size = 25000000
                    extension = jpg,jpeg,gif,png,tif,txt,doc,docx,xls,xlsx,ppt,pptx,pdf,zip,csv,svg
                }
            }
        }
    }
}
```

### Prefill Fields via TypoScript

```typoscript
plugin.tx_powermail.settings.setup.prefill {
    # By field marker
    email = TEXT
    email.data = TSFE:fe_user|user|email

    firstname = TEXT
    firstname.data = TSFE:fe_user|user|first_name

    # Prefill from GET/POST
    subject = TEXT
    subject.data = GP:subject
}
```

### Marketing Information

```typoscript
plugin.tx_powermail.settings.setup.marketing {
    enable = 1
    # Tracked: refererDomain, referer, country, mobileDevice, frontendLanguage, browserLanguage, pageFunnel
}
```

## 4. Custom Finishers

Finishers run after successful form submission, sorted by TypoScript key.

### Registration

```typoscript
plugin.tx_powermail.settings.setup.finishers {
    # Lower number = runs first
    0.class = In2code\Powermail\Finisher\RateLimitFinisher
    10.class = In2code\Powermail\Finisher\SaveToAnyTableFinisher
    20.class = In2code\Powermail\Finisher\SendParametersFinisher
    100.class = In2code\Powermail\Finisher\RedirectFinisher

    # Custom finisher
    50.class = Vendor\MyExt\Finisher\CrmFinisher
    50.config {
        apiUrl = https://crm.example.com/api
        apiKey = secret123
    }
}
```

### Creating a Custom Finisher

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\Finisher;

use In2code\Powermail\Finisher\AbstractFinisher;
use In2code\Powermail\Finisher\FinisherInterface;
use In2code\Powermail\Domain\Model\Mail;

final class CrmFinisher extends AbstractFinisher implements FinisherInterface
{
    /**
     * Method name MUST end with "Finisher"
     * Can have initialize*Finisher() called before
     */
    public function myCustomFinisher(): void
    {
        /** @var Mail $mail */
        $mail = $this->getMail();
        $settings = $this->getSettings();
        $configuration = $this->getConfiguration(); // TS config.*

        // Access form answers
        foreach ($mail->getAnswers() as $answer) {
            $fieldMarker = $answer->getField()->getMarker();
            $value = $answer->getValue();
            // Process...
        }

        // Access by marker
        $answers = $mail->getAnswersByFieldMarker();
        $email = $answers['email'] ?? null;

        // Check if form was actually submitted (not just displayed)
        if (!$this->isFormSubmitted()) {
            return;
        }
    }
}
```

### Built-in Finishers

| Class | Key | Purpose |
|-------|-----|---------|
| `RateLimitFinisher` | 0 | Consumes rate limiter tokens |
| `SaveToAnyTableFinisher` | 10 | Save answers to custom DB tables |
| `SendParametersFinisher` | 20 | POST form data to external URL |
| `RedirectFinisher` | 100 | Redirect after submission |

### SaveToAnyTable Configuration

```typoscript
plugin.tx_powermail.settings.setup.dbEntry {
    1 {
        _enable = TEXT
        _enable.value = 1
        _table = fe_users
        _ifUnique.email = update  # update|skip|none
        username.value = {email}
        email.value = {email}
        first_name.value = {firstname}
        last_name.value = {lastname}
        pid.value = 123
    }
}
```

## 5. Custom Validators

### Creating a Custom Validator (PSR-14 Event)

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\EventListener;

use In2code\Powermail\Events\CustomValidatorEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener('vendor-myext/custom-validator')]
final class CustomValidatorListener
{
    public function __invoke(CustomValidatorEvent $event): void
    {
        $mail = $event->getMail();
        $field = $event->getField();

        // Validate specific field by marker
        if ($field->getMarker() === 'company_vat') {
            $answer = null;
            foreach ($mail->getAnswers() as $a) {
                if ($a->getField()?->getUid() === $field->getUid()) {
                    $answer = $a;
                    break;
                }
            }

            if ($answer !== null && !$this->isValidVat((string)$answer->getValue())) {
                $event->setIsValid(false);
                $event->setValidationMessage('Invalid VAT number');
            }
        }
    }

    private function isValidVat(string $vat): bool
    {
        return (bool)preg_match('/^[A-Z]{2}\d{8,12}$/', $vat);
    }
}
```

### Built-in Validators

| Validator | Purpose |
|-----------|---------|
| `InputValidator` | Email, URL, phone, number, letters, min/max length, regex |
| `UploadValidator` | File size, extension whitelist |
| `PasswordValidator` | Password match and strength |
| `CaptchaValidator` | Built-in CAPTCHA |
| `SpamShieldValidator` | Multi-method spam detection |
| `UniqueValidator` | Unique field values |
| `ForeignValidator` | Validate against foreign table |
| `CustomValidator` | TypoScript-based custom rules |

### Spam Shield Methods

| Method | Weight | Description |
|--------|--------|-------------|
| `HoneyPodMethod` | 5 | Hidden honeypot field |
| `LinkMethod` | 3 | Excessive links detection |
| `NameMethod` | 3 | Suspicious name patterns |
| `SessionMethod` | 1 | Session token validation |
| `UniqueMethod` | 2 | Duplicate submission check |
| `ValueBlacklistMethod` | 7 | Blacklisted content |
| `IpBlacklistMethod` | 7 | Blacklisted IP addresses |
| `RateLimitMethod` | 10 | Request rate limiting |

## 6. PSR-14 Events

### Form Lifecycle Events

```php
// Before form is rendered
FormControllerFormActionEvent

// Before confirmation page
FormControllerConfirmationActionEvent

// After mail is saved to database
FormControllerCreateActionAfterMailDbSavedEvent

// After submit view is built
FormControllerCreateActionAfterSubmitViewEvent

// Before final view is rendered
FormControllerCreateActionBeforeRenderViewEvent

// Controller initialization
FormControllerInitializeObjectEvent
```

### Mail Events

```php
// Modify receiver email addresses
ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent

// Modify receiver name
ReceiverMailReceiverPropertiesServiceGetReceiverNameEvent

// Modify sender email (receiver mail)
ReceiverMailSenderPropertiesGetSenderEmailEvent

// Modify sender name (receiver mail)
ReceiverMailSenderPropertiesGetSenderNameEvent

// Modify sender email (confirmation mail)
SenderMailPropertiesGetSenderEmailEvent

// Modify sender name (confirmation mail)
SenderMailPropertiesGetSenderNameEvent

// Modify email body before sending
SendMailServiceCreateEmailBodyEvent

// Before email is sent (last chance to modify)
SendMailServicePrepareAndSendEvent
```

### Other Events

```php
// Control if mail should be saved to DB
CheckIfMailIsAllowedToSaveEvent

// Custom validation logic
CustomValidatorEvent

// Prefill field values
PrefillFieldViewHelperEvent
PrefillMultiFieldViewHelperEvent

// File upload processing
UploadServicePreflightEvent
UploadServiceGetFilesEvent
GetNewPathAndFilenameEvent

// Before password is hashed
MailFactoryBeforePasswordIsHashedEvent

// Modify mail variables/markers
MailRepositoryGetVariablesWithMarkersFromMailEvent

// Validation data attributes
ValidationDataAttributeViewHelperEvent

// Double opt-in confirmation
FormControllerOptinConfirmActionAfterPersistEvent
FormControllerOptinConfirmActionBeforeRenderViewEvent

// Disclaimer/unsubscribe
FormControllerDisclaimerActionBeforeRenderViewEvent
```

### Example: Modify Receiver Email

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\EventListener;

use In2code\Powermail\Events\ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener('vendor-myext/dynamic-receiver')]
final class DynamicReceiverListener
{
    public function __invoke(
        ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent $event
    ): void {
        $mail = $event->getMail();
        $answers = $mail->getAnswersByFieldMarker();

        // Route to department based on form field
        $department = $answers['department'] ?? null;
        if ($department !== null) {
            $value = (string)$department->getValue();
            $emails = match ($value) {
                'sales' => ['sales@example.com'],
                'support' => ['support@example.com'],
                default => $event->getReceiverEmails(),
            };
            $event->setReceiverEmails($emails);
        }
    }
}
```

### Example: Prevent DB Save

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\EventListener;

use In2code\Powermail\Events\CheckIfMailIsAllowedToSaveEvent;
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener('vendor-myext/skip-db-save')]
final class SkipDbSaveListener
{
    public function __invoke(CheckIfMailIsAllowedToSaveEvent $event): void
    {
        // Skip DB save for specific forms
        $form = $event->getMail()->getForm();
        if ($form !== null && $form->getTitle() === 'Contact (no storage)') {
            $event->setSavingOfMailAllowed(false);
        }
    }
}
```

## 7. Email Templates

### Template Paths (TypoScript)

```typoscript
plugin.tx_powermail {
    view {
        templateRootPaths {
            0 = EXT:powermail/Resources/Private/Templates/
            10 = EXT:my_ext/Resources/Private/Templates/Powermail/
        }
        partialRootPaths {
            0 = EXT:powermail/Resources/Private/Partials/
            10 = EXT:my_ext/Resources/Private/Partials/Powermail/
        }
        layoutRootPaths {
            0 = EXT:powermail/Resources/Private/Layouts/
            10 = EXT:my_ext/Resources/Private/Layouts/Powermail/
        }
    }
}
```

### Key Templates

| Template | Purpose |
|----------|---------|
| `Form/Form.html` | Main form rendering |
| `Form/Confirmation.html` | Confirmation page |
| `Form/Create.html` | Thank you page |
| `Mail/ReceiverMail.html` | Admin notification email |
| `Mail/SenderMail.html` | User confirmation email |
| `Mail/OptinMail.html` | Double opt-in email |
| `Form/PowermailAll.html` | All-fields summary |

### Field Partials

Override individual field types by copying partials:

```
Partials/Form/Field/Input.html
Partials/Form/Field/Textarea.html
Partials/Form/Field/Select.html
Partials/Form/Field/Check.html
Partials/Form/Field/Radio.html
Partials/Form/Field/File.html
Partials/Form/Field/Date.html
Partials/Form/Field/Captcha.html
Partials/Form/Field/Hidden.html
Partials/Form/Field/Password.html
Partials/Form/Field/Country.html
Partials/Form/Field/Location.html
Partials/Form/Field/Html.html
Partials/Form/Field/Content.html
Partials/Form/Field/Typoscript.html
Partials/Form/Field/Submit.html
Partials/Form/Field/Reset.html
```

### Available Variables in Mail Templates

```html
<!-- In ReceiverMail.html / SenderMail.html -->
{mail}                          <!-- Mail domain object -->
{mail.senderName}               <!-- Sender name -->
{mail.senderMail}               <!-- Sender email -->
{mail.form.title}               <!-- Form title -->
{mail.answers}                  <!-- All answers (ObjectStorage) -->

<!-- Iterate answers -->
<f:for each="{mail.answers}" as="answer">
    {answer.field.title}: {answer.value}
</f:for>

<!-- PowermailAll marker (all fields formatted) -->
{powermail_all}
```

## 8. Key ViewHelpers

### Validation

```html
<!-- Enable JS validation and/or AJAX submit -->
<vh:validation.enableJavascriptValidationAndAjax
    form="{form}"
    additionalAttributes="{...}" />

<!-- Validation data attributes on fields -->
<vh:validation.validationDataAttribute field="{field}" />

<!-- Error CSS class -->
<vh:validation.errorClass field="{field}" class="error" />

<!-- Upload attributes (accept, multiple) -->
<vh:validation.uploadAttributes field="{field}" />
```

### Form Fields

```html
<!-- Country selector -->
<vh:form.countries
    settings="{settings}"
    field="{field}"
    mail="{mail}" />

<!-- Advanced select with optgroups -->
<vh:form.advancedSelect
    field="{field}"
    mail="{mail}" />

<!-- Multi-upload -->
<vh:form.multiUpload field="{field}" />
```

### Prefill

```html
<!-- Prefill single-value field -->
<vh:misc.prefillField field="{field}" mail="{mail}" />

<!-- Prefill multi-value field (select, check, radio) -->
<vh:misc.prefillMultiField field="{field}" mail="{mail}" cycle="{cycle}" />
```

### Conditions

```html
<!-- Check if field is not empty -->
<vh:condition.isNotEmpty val="{value}">
    <f:then>Has value</f:then>
</vh:condition.isNotEmpty>

<!-- Check if array -->
<vh:condition.isArray val="{value}">
    <f:then>Is array</f:then>
</vh:condition.isArray>

<!-- Check file exists -->
<vh:condition.fileExists file="{path}">
    <f:then>File available</f:then>
</vh:condition.fileExists>
```

### Backend

```html
<!-- Edit link in backend module -->
<vh:be.editLink table="tx_powermail_domain_model_mail" uid="{mail.uid}">
    Edit
</vh:be.editLink>
```

## 9. AJAX Form Submission

```typoscript
plugin.tx_powermail.settings.setup.misc.ajaxSubmit = 1
```

When enabled, form submission is handled via AJAX without page reload. The response replaces the form container with the thank-you content.

## 10. Double Opt-In

```typoscript
plugin.tx_powermail.settings.setup.main.optin = 1

plugin.tx_powermail.settings.setup.optin {
    subject = Please confirm your submission
    senderName = My Website
    senderEmail = noreply@example.com
}
```

Flow:
1. User submits form
2. Mail is saved with `hidden=1`
3. Opt-in email sent with confirmation link (HMAC-secured)
4. User clicks link -> `optinConfirmAction` unhides the mail
5. Receiver email sent after confirmation

## 11. Backend Module

Powermail provides a backend module under **Web > Powermail**:

- **List**: Browse/filter/search submitted mails
- **Export**: CSV and Excel (PhpSpreadsheet) export
- **Reporting**: Form analytics and marketing charts
- **System Check**: Verify configuration (admin only)

### Live Search

Search mails and forms directly from TYPO3 search bar:

- `#mail:searchterm` - Search in mails
- `#form:searchterm` - Search in forms

## 12. Extension Best Practices

### Register Services (Services.yaml)

```yaml
services:
  Vendor\MyExt\EventListener\CrmSyncListener:
    tags:
      - name: event.listener
        identifier: 'vendor-myext/crm-sync'
```

Or use the `#[AsEventListener]` attribute (preferred in TYPO3 v13+).

### Access Mail Answers Efficiently

```php
// By field marker (most common)
$answers = $mail->getAnswersByFieldMarker();
$email = $answers['email']?->getValue();

// By field UID
$answers = $mail->getAnswersByFieldUid();

// Filter by value type
$uploads = $mail->getAnswersByValueType(Answer::VALUE_TYPE_UPLOAD);
```

### Custom Data on Mail Object

```php
// Add custom data (available in all finishers/events)
$mail->addAdditionalData('crm_id', $crmResponse['id']);

// Retrieve in another finisher/event
$crmId = $mail->getAdditionalData()['crm_id'] ?? null;
```

### Rate Limiting

Powermail uses Symfony RateLimiter. Configure in `ext_conf_template.txt` or extension settings.

### Garbage Collection

Powermail auto-registers garbage collection for mails and answers (default: 30 days). Configure via Scheduler task `TableGarbageCollectionTask`.

## 13. Common Recipes

### Route Enhancer for SEO-Friendly URLs

```yaml
routeEnhancers:
  PowermailOptIn:
    type: Plugin
    routePath: '/optin/{mail}/{hash}'
    namespace: 'tx_powermail_pi1'
    requirements:
      mail: '\d+'
      hash: '[a-zA-Z0-9]+'
```

### Conditional Receiver Based on Form Field

Use `ReceiverMailReceiverPropertiesServiceSetReceiverEmailsEvent` (see Section 6).

### Custom Spam Shield Method

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\SpamShield;

use In2code\Powermail\Domain\Validator\SpamShield\AbstractMethod;

final class ApiCheckMethod extends AbstractMethod
{
    public function spamCheck(): bool
    {
        $mail = $this->getMail();
        // Return true if spam detected
        return $this->callExternalApi($mail);
    }
}
```

Register in TypoScript:

```typoscript
plugin.tx_powermail.settings.setup.spamshield.methods {
    100 {
        class = Vendor\MyExt\SpamShield\ApiCheckMethod
        _enable = 1
        configuration {
            apiUrl = https://spam-api.example.com
        }
    }
}
```

### Extend Form with TypoScript-Generated Fields

```typoscript
plugin.tx_powermail.settings.setup.manipulateVariablesInPowermailAllMarker {
    timestamp = TEXT
    timestamp.data = date:U
    timestamp.strftime = %Y-%m-%d %H:%M:%S
}
```

## 14. Database Structure

> **Conditions tables:** See [SKILL-CONDITIONS.md](SKILL-CONDITIONS.md) Section 12 for `tx_powermailcond_*` tables.

### TYPO3 Standard Columns

All powermail tables include these TYPO3-managed columns (not listed per table below):

| Column | Type | Purpose |
|--------|------|---------|
| `uid` | int AUTO_INCREMENT | Primary key |
| `pid` | int | Storage page UID |
| `tstamp` | int | Last modification timestamp |
| `crdate` | int | Creation timestamp |
| `deleted` | tinyint | Soft-delete flag |
| `hidden` | tinyint | Visibility flag |
| `sys_language_uid` | int | Language UID (0 = default, -1 = all) |
| `l10n_parent` | int | UID of the default language record |
| `l10n_diffsource` | mediumblob | Diff source for translation |
| `starttime` | int | Publish start (Unix timestamp) |
| `endtime` | int | Publish end (Unix timestamp) |

### tx_powermail_domain_model_form

| Column | Type | Description |
|--------|------|-------------|
| `title` | varchar(255) | Form title |
| `note` | tinyint | Backend note renderer (internal) |
| `css` | varchar(255) | CSS class for form wrapper |
| `pages` | varchar(255) | IRRE children count or element browser list |
| `autocomplete_token` | varchar(3) | Autocomplete on/off/empty |
| `is_dummy_record` | tinyint | Test record flag |

**Indexes:** `language (l10n_parent, sys_language_uid)`

### tx_powermail_domain_model_page

| Column | Type | Description |
|--------|------|-------------|
| `form` | int | Parent form UID |
| `title` | varchar(255) | Page/step title |
| `css` | varchar(255) | CSS class for fieldset |
| `fields` | int | IRRE children count |
| `sorting` | int | Sort order within form |

**Indexes:** `parent_form (form)`, `language (l10n_parent, sys_language_uid)`

### tx_powermail_domain_model_field

| Column | Type | Description |
|--------|------|-------------|
| `page` | int | Parent page UID |
| `title` | varchar(255) | Field label |
| `type` | varchar(255) | Field type key (input, select, check, ...) |
| `settings` | text | Options for select/radio/check (one per line) |
| `path` | varchar(255) | File path reference |
| `content_element` | int | CE reference for type=content |
| `text` | text | Static text for type=text |
| `prefill_value` | text | Default/prefill value |
| `placeholder` | text | Placeholder text |
| `placeholder_repeat` | text | Placeholder for repeat field (password) |
| `create_from_typoscript` | text | TypoScript for type=typoscript |
| `validation` | int | Validation type (0=none, 1=email, ...) |
| `validation_configuration` | varchar(255) | Regex or config for validation |
| `css` | varchar(255) | CSS class for field wrapper |
| `description` | varchar(255) | Help text / description |
| `multiselect` | tinyint | Allow multi-select |
| `datepicker_settings` | varchar(255) | Datepicker format |
| `feuser_value` | varchar(255) | Prefill from fe_user property |
| `sender_email` | tinyint | This field is the sender email |
| `sender_name` | tinyint | This field is the sender name |
| `mandatory` | tinyint | Required field |
| `own_marker_select` | tinyint | Custom marker enabled |
| `marker` | varchar(255) | Field marker (variable name) |
| `mandatory_text` | varchar(255) | Custom mandatory error text |
| `autocomplete_token` | varchar(20) | Autocomplete attribute |
| `autocomplete_section` | varchar(100) | Autocomplete section |
| `autocomplete_type` | varchar(8) | Autocomplete type |
| `autocomplete_purpose` | varchar(8) | Autocomplete purpose |
| `sorting` | int | Sort order within page |

**Indexes:** `parent_page (page)`, `language (l10n_parent, sys_language_uid)`

### tx_powermail_domain_model_mail

| Column | Type | Description |
|--------|------|-------------|
| `sender_name` | varchar(255) | Submitter name |
| `sender_mail` | varchar(255) | Submitter email |
| `subject` | varchar(255) | Mail subject |
| `receiver_mail` | varchar(1024) | Receiver email(s) |
| `body` | text | Mail body (RTE) |
| `feuser` | int | Frontend user UID (if logged in) |
| `sender_ip` | tinytext | Submitter IP address |
| `user_agent` | text | Browser user agent |
| `time` | int | Submission timestamp |
| `form` | int | Source form UID |
| `answers` | int | IRRE children count |
| `spam_factor` | varchar(255) | Spam score |
| `marketing_referer_domain` | text | HTTP referer domain |
| `marketing_referer` | text | Full HTTP referer |
| `marketing_country` | text | Visitor country |
| `marketing_mobile_device` | tinyint | Mobile device flag |
| `marketing_frontend_language` | int | Frontend language UID |
| `marketing_browser_language` | text | Browser Accept-Language |
| `marketing_page_funnel` | text | Pages visited before submit |

**Indexes:** `form (form)`, `feuser (feuser)`

### tx_powermail_domain_model_answer

| Column | Type | Description |
|--------|------|-------------|
| `mail` | int | Parent mail UID |
| `value` | text | Answer value (JSON for arrays) |
| `value_type` | int | 0=text, 1=array, 2=date, 3=upload, 4=password |
| `field` | int | Source field UID |

**Indexes:** `mail (mail)`, `deleted (deleted)`, `hidden (hidden)`, `language (l10n_parent, sys_language_uid)`

### ER Diagram (Relations)

```
tx_powermail_domain_model_form
  │ 1
  ├──── * tx_powermail_domain_model_page (IRRE via form)
  │       │ 1
  │       └──── * tx_powermail_domain_model_field (IRRE via page)
  │                    │
  │                    │ referenced by
  │                    ▼
  │             tx_powermail_domain_model_answer.field
  │
  └──── * tx_powermail_domain_model_mail (via form)
           │ 1
           └──── * tx_powermail_domain_model_answer (IRRE via mail)
```

## 15. Workspace Support

Powermail records (forms, pages, fields) fully support TYPO3 workspaces. When EXT:workspaces is
installed, editors can draft form changes in a workspace and publish them after review.

**Key points:**
- All powermail tables gain `t3ver_wsid`, `t3ver_oid`, `t3ver_state`, `t3ver_stage` columns
- Records with `t3ver_wsid > 0` are drafts (not visible in live frontend)
- Use **DataHandler** for workspace operations — it handles versioning automatically
- Raw SQL requires manually setting all `t3ver_*` columns on every INSERT
- Conditions (powermail_cond) must be in the **same workspace** as the form

**Workspace lifecycle:**
1. **Create** records in workspace → `t3ver_wsid = <ws_id>`, `t3ver_state = 1`
2. **Stage** for review → `t3ver_stage = 1`
3. **Publish** via backend module or CLI → records become live (`t3ver_wsid = 0`)

> **Detailed SQL and DataHandler examples:** See [SKILL-EXAMPLES.md](SKILL-EXAMPLES.md#workspace-support)
> for complete workspace-aware queries, publishing workflows, and CLI options.

## 16. Translations (Localization)

Powermail supports full TYPO3 localization. Form structure (form, pages, fields) can be translated so editors see localized labels, settings, and options. Submitted mails inherit the frontend language.

### How Translation Works

| Level | What gets translated | Key columns |
|-------|---------------------|-------------|
| Form | Title | `sys_language_uid`, `l10n_parent` |
| Page | Title (step heading) | `sys_language_uid`, `l10n_parent` |
| Field | Title, settings, placeholder, mandatory_text, description | `sys_language_uid`, `l10n_parent` |
| Mail | Automatically stored with `sys_language_uid` from frontend | `sys_language_uid` |
| Answer | Stored with language of submission | `sys_language_uid` |

### Translation Rules

- `sys_language_uid = 0` is the **default language** (e.g., English)
- `sys_language_uid = 1` (or higher) is a translation (e.g., German)
- `l10n_parent` points to the default language record UID
- The `marker` field is **not translated** -- markers stay identical across languages
- Field `type` is **not translated** -- structure is shared
- Field `settings` (select/radio options) **is translated** -- option labels change per language

### Example: Create Form in English, Translate to German

#### Default Language (English, sys_language_uid=0)

```sql
-- Form
INSERT INTO tx_powermail_domain_model_form (pid, title, sys_language_uid, l10n_parent)
VALUES (1, 'Contact Form', 0, 0);
-- Assume UID = 10

-- Page
INSERT INTO tx_powermail_domain_model_page (pid, form, title, sorting, sys_language_uid, l10n_parent)
VALUES (1, 10, 'Your Details', 1, 0, 0);
-- Assume UID = 20

-- Fields
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sender_name, sorting, sys_language_uid, l10n_parent)
VALUES
  (1, 20, 'First Name', 'input', 'firstname', 1, 1, 1, 0, 0),   -- UID 30
  (1, 20, 'Last Name', 'input', 'lastname', 1, 0, 2, 0, 0),     -- UID 31
  (1, 20, 'Email', 'input', 'email', 1, 0, 3, 0, 0),            -- UID 32
  (1, 20, 'Message', 'textarea', 'message', 0, 0, 4, 0, 0),     -- UID 33
  (1, 20, 'Subject', 'select', 'subject', 1, 0, 5, 0, 0),       -- UID 34
  (1, 20, 'Send', 'submit', 'submit', 0, 0, 6, 0, 0);           -- UID 35

-- Select options for subject (English)
UPDATE tx_powermail_domain_model_field
SET settings = 'General Inquiry\nSupport Request\nPartnership\nOther'
WHERE uid = 34;

-- Mark email field as sender_email
UPDATE tx_powermail_domain_model_field SET sender_email = 1 WHERE uid = 32;
```

#### German Translation (sys_language_uid=1)

```sql
-- Form translation (l10n_parent = 10, the English form)
INSERT INTO tx_powermail_domain_model_form (pid, title, sys_language_uid, l10n_parent)
VALUES (1, 'Kontaktformular', 1, 10);

-- Page translation (l10n_parent = 20)
INSERT INTO tx_powermail_domain_model_page
  (pid, form, title, sorting, sys_language_uid, l10n_parent)
VALUES (1, 10, 'Ihre Daten', 1, 1, 20);

-- Field translations (l10n_parent points to English field UID)
INSERT INTO tx_powermail_domain_model_field
  (pid, page, title, type, marker, mandatory, sender_name, sorting, sys_language_uid, l10n_parent)
VALUES
  (1, 20, 'Vorname', 'input', 'firstname', 1, 1, 1, 1, 30),
  (1, 20, 'Nachname', 'input', 'lastname', 1, 0, 2, 1, 31),
  (1, 20, 'E-Mail-Adresse', 'input', 'email', 1, 0, 3, 1, 32),
  (1, 20, 'Nachricht', 'textarea', 'message', 0, 0, 4, 1, 33),
  (1, 20, 'Betreff', 'select', 'subject', 1, 0, 5, 1, 34),
  (1, 20, 'Absenden', 'submit', 'submit', 0, 0, 6, 1, 35);

-- German select options for subject
UPDATE tx_powermail_domain_model_field
SET settings = 'Allgemeine Anfrage\nSupportanfrage\nPartnerschaft\nSonstiges'
WHERE sys_language_uid = 1 AND l10n_parent = 34;

-- Mark email field as sender_email (must be set on translation too)
UPDATE tx_powermail_domain_model_field
SET sender_email = 1
WHERE sys_language_uid = 1 AND l10n_parent = 32;
```

### Translation via DataHandler

```php
<?php

declare(strict_types=1);

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
$dataHandler->start([], []);

// Localize form (UID 10) to German (sys_language_uid=1)
$cmdMap = [
    'tx_powermail_domain_model_form' => [
        10 => [
            'localize' => 1, // target language UID
        ],
    ],
];
$dataHandler->start([], $cmdMap);
$dataHandler->process_cmdmap();

// DataHandler auto-creates translations of all IRRE children (pages + fields)
// Then update the translated titles:
$translatedFormUid = $dataHandler->copyMappingArray_merged['tx_powermail_domain_model_form'][10] ?? null;
if ($translatedFormUid) {
    $data = [
        'tx_powermail_domain_model_form' => [
            $translatedFormUid => [
                'title' => 'Kontaktformular',
            ],
        ],
    ];
    $dataHandler->start($data, []);
    $dataHandler->process_datamap();
}
```

### Important Translation Notes

- **Markers are language-independent.** The marker `email` stays `email` in all languages.
- **IRRE localization:** When you localize a form via DataHandler (`localize` command), TYPO3 automatically creates translations for all child pages and fields.
- **Select options:** The `settings` field (select/radio/check options) **must** be translated separately -- option values should match (for condition evaluation) but labels can differ.
- **Submitted mails:** Mails store `sys_language_uid` from the frontend context. Answers reference the default-language field UID regardless of submission language.
- **Backend module:** The mail list shows mails from all languages. Filter by language if needed.

## 17. Full Example: Multi-Step Shop Form with Conditions

> For a comprehensive multi-step mini-shop example with Austrian legal types (Gesellschaftsformen),
> conditional fields per legal type, GDPR compliance, and two implementation approaches
> (DDEV SQL + DataHandler CLI command), see [SKILL-EXAMPLES.md](SKILL-EXAMPLES.md).

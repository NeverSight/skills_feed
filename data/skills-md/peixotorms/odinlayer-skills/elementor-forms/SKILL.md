---
name: elementor-forms
description: Use when creating custom Elementor form actions, custom form field types, form validation, or processing form submissions. Covers Elementor Pro forms (ElementorPro\Modules\Forms), Action_Base (get_name, get_label, run, register_settings_section, on_export), after_submit processing, Field_Base (field_type, render field HTML, validation callback, update_controls), content_template for editor preview, form action registration, export_type handling, update_record patterns, elementor_pro/forms/validation hook, email filters, and webhook response handling.
---

# Elementor Forms Extension Reference

**Elementor Pro only.** All form APIs require Elementor Pro active.

## 1. Form Actions

Actions execute after form submission. Extend `\ElementorPro\Modules\Forms\Classes\Action_Base`.

### Registration

```php
add_action( 'elementor_pro/forms/actions/register', function ( $form_actions_registrar ) {
    require_once __DIR__ . '/form-actions/my-action.php';
    $form_actions_registrar->register( new \My_Custom_Action() );
});
```

### Required Methods

| Method | Returns | Purpose |
|---|---|---|
| `get_name()` | `string` | Unique action ID used in code |
| `get_label()` | `string` | Display label in editor |
| `run( $record, $ajax_handler )` | `void` | Execute on form submission |
| `register_settings_section( $widget )` | `void` | Optional: add action controls |
| `on_export( $element )` | `array` | Optional: strip sensitive data on export |

### Action Controls

Always wrap in a section with `submit_actions` condition:

```php
public function register_settings_section( $widget ): void {
    $widget->start_controls_section( 'section_my_action', [
        'label' => esc_html__( 'My Action', 'textdomain' ),
        'condition' => [ 'submit_actions' => $this->get_name() ],
    ]);
    $widget->add_control( 'my_api_key', [
        'label' => esc_html__( 'API Key', 'textdomain' ),
        'type' => \Elementor\Controls_Manager::TEXT,
    ]);
    $widget->end_controls_section();
}
```

### Record Data ($record) and AJAX Handler

```php
public function run( $record, $ajax_handler ): void {
    $settings = $record->get( 'form_settings' );    // Editor control values
    $raw_fields = $record->get( 'fields' );          // All submitted fields
    // Normalize: $fields[ $id ] = $field['value']
    $fields = [];
    foreach ( $raw_fields as $id => $field ) {
        $fields[ $id ] = $field['value'];
    }
    // AJAX handler methods:
    $ajax_handler->add_error( $field_id, 'Error message' );
    $ajax_handler->add_success_message( 'Success!' );
}
```

### On Export -- strip sensitive settings

```php
public function on_export( $element ): array {
    unset( $element['my_api_key'], $element['my_secret'] );
    return $element;
}
```

### Simple Example: Webhook Ping Action

```php
class Ping_Action_After_Submit extends \ElementorPro\Modules\Forms\Classes\Action_Base {
    public function get_name(): string { return 'ping'; }
    public function get_label(): string { return esc_html__( 'Ping', 'textdomain' ); }

    public function run( $record, $ajax_handler ): void {
        wp_remote_post( 'https://api.example.com/', [
            'headers' => [ 'Content-Type' => 'application/json' ],
            'body' => wp_json_encode([
                'site' => get_home_url(),
                'action' => 'Form submitted',
            ]),
            'timeout' => 60,
        ]);
    }

    public function register_settings_section( $widget ): void {}
    public function on_export( $element ): array { return $element; }
}
```

### Advanced Example: Sendy Subscriber Action

```php
class Sendy_Action_After_Submit extends \ElementorPro\Modules\Forms\Classes\Action_Base {
    public function get_name(): string { return 'sendy'; }
    public function get_label(): string { return esc_html__( 'Sendy', 'textdomain' ); }

    public function register_settings_section( $widget ): void {
        $widget->start_controls_section( 'section_sendy', [
            'label' => esc_html__( 'Sendy', 'textdomain' ),
            'condition' => [ 'submit_actions' => $this->get_name() ],
        ]);
        $widget->add_control( 'sendy_url', [
            'label' => esc_html__( 'Sendy URL', 'textdomain' ),
            'type' => \Elementor\Controls_Manager::TEXT,
            'placeholder' => 'https://your_sendy_installation/',
        ]);
        $widget->add_control( 'sendy_list', [
            'label' => esc_html__( 'Sendy List ID', 'textdomain' ),
            'type' => \Elementor\Controls_Manager::TEXT,
        ]);
        $widget->add_control( 'sendy_email_field', [
            'label' => esc_html__( 'Email Field ID', 'textdomain' ),
            'type' => \Elementor\Controls_Manager::TEXT,
        ]);
        $widget->add_control( 'sendy_name_field', [
            'label' => esc_html__( 'Name Field ID', 'textdomain' ),
            'type' => \Elementor\Controls_Manager::TEXT,
        ]);
        $widget->end_controls_section();
    }

    public function run( $record, $ajax_handler ): void {
        $settings = $record->get( 'form_settings' );
        if ( empty( $settings['sendy_url'] ) || empty( $settings['sendy_list'] ) || empty( $settings['sendy_email_field'] ) ) {
            return;
        }
        $raw_fields = $record->get( 'fields' );
        $fields = [];
        foreach ( $raw_fields as $id => $field ) { $fields[ $id ] = $field['value']; }
        if ( empty( $fields[ $settings['sendy_email_field'] ] ) ) { return; }

        $sendy_data = [
            'email' => $fields[ $settings['sendy_email_field'] ],
            'list'  => $settings['sendy_list'],
            'ipaddress' => \ElementorPro\Core\Utils::get_client_ip(),
            'referrer'  => isset( $_POST['referrer'] ) ? $_POST['referrer'] : '',
        ];
        if ( ! empty( $fields[ $settings['sendy_name_field'] ] ) ) {
            $sendy_data['name'] = $fields[ $settings['sendy_name_field'] ];
        }
        wp_remote_post( $settings['sendy_url'] . 'subscribe', [ 'body' => $sendy_data ] );
    }

    public function on_export( $element ): array {
        unset( $element['sendy_url'], $element['sendy_list'], $element['sendy_email_field'], $element['sendy_name_field'] );
        return $element;
    }
}
```

---

## 2. Form Fields

Custom field types. Extend `\ElementorPro\Modules\Forms\Fields\Field_Base`.

### Registration

```php
add_action( 'elementor_pro/forms/fields/register', function ( $form_fields_registrar ) {
    require_once __DIR__ . '/form-fields/my-field.php';
    $form_fields_registrar->register( new \My_Custom_Field() );
});
```

### Required Methods

| Method | Returns | Purpose |
|---|---|---|
| `get_type()` | `string` | Unique field type ID |
| `get_name()` | `string` | Display label in editor dropdown |
| `render( $item, $item_index, $form )` | `void` | Output field HTML on frontend |
| `validation( $field, $record, $ajax_handler )` | `void` | Optional: validate submitted value |
| `update_controls( $widget )` | `void` | Optional: add field-specific controls |
| `get_script_depends()` | `array` | Optional: JS dependency handles |
| `get_style_depends()` | `array` | Optional: CSS dependency handles |

### Render -- use add_render_attribute

```php
public function render( $item, $item_index, $form ): void {
    $form->add_render_attribute( 'input' . $item_index, [
        'type'  => 'text',
        'class' => 'elementor-field-textual',
        'placeholder' => esc_html__( 'Placeholder', 'textdomain' ),
    ]);
    echo '<input ' . $form->get_render_attribute_string( 'input' . $item_index ) . '>';
}
```

Access field control values from `$item`: `$item['my-control-name']`.

### Field Validation

```php
public function validation( $field, $record, $ajax_handler ): void {
    if ( empty( $field['value'] ) ) { return; }
    if ( ! preg_match( '/^[0-9]+$/', $field['value'] ) ) {
        $ajax_handler->add_error( $field['id'], esc_html__( 'Only numbers.', 'textdomain' ) );
    }
}
```

### Field Controls (update_controls)

Inject into the form field repeater. Requires `condition`, `tab`, `inner_tab`, `tabs_wrapper`:

```php
public function update_controls( $widget ): void {
    $elementor = \ElementorPro\Plugin::elementor();
    $control_data = $elementor->controls_manager->get_control_from_stack( $widget->get_unique_name(), 'form_fields' );
    if ( is_wp_error( $control_data ) ) { return; }

    $field_controls = [
        'my-placeholder' => [
            'name' => 'my-placeholder',
            'label' => esc_html__( 'Placeholder', 'textdomain' ),
            'type' => \Elementor\Controls_Manager::TEXT,
            'condition' => [ 'field_type' => $this->get_type() ],
            'tab'          => 'content',
            'inner_tab'    => 'form_fields_content_tab',
            'tabs_wrapper' => 'form_fields_tabs',
        ],
    ];
    $control_data['fields'] = $this->inject_field_controls( $control_data['fields'], $field_controls );
    $widget->update_control( 'form_fields', $control_data );
}
```

### Content Template (JS Editor Preview)

Workaround for live preview. Do NOT name your method `content_template()` (reserved for future use):

```php
public function __construct() {
    parent::__construct();
    add_action( 'elementor/preview/init', [ $this, 'editor_preview_footer' ] );
}
public function editor_preview_footer(): void {
    add_action( 'wp_footer', [ $this, 'content_template_script' ] );
}
public function content_template_script(): void {
    ?>
    <script>
    jQuery( document ).ready( () => {
        elementor.hooks.addFilter(
            'elementor_pro/forms/content_template/field/<?php echo $this->get_type(); ?>',
            function ( inputField, item, i ) {
                const fieldId    = `form_field_${i}`;
                const fieldClass = `elementor-field-textual elementor-field ${item.css_classes}`;
                return `<input id="${fieldId}" class="${fieldClass}" type="text">`;
            }, 10, 3
        );
    });
    </script>
    <?php
}
```

### Field Dependencies

```php
// Register in plugin main file
add_action( 'wp_enqueue_scripts', function () {
    wp_register_script( 'my-field-js', plugins_url( 'assets/js/field.js', __FILE__ ) );
    wp_register_style( 'my-field-css', plugins_url( 'assets/css/field.css', __FILE__ ) );
});
// Declare in field class
public function get_script_depends(): array { return [ 'my-field-js' ]; }
public function get_style_depends(): array { return [ 'my-field-css' ]; }
// Backward compat (Elementor < 3.28): also set public properties
public $depended_scripts = [ 'my-field-js' ];
public $depended_styles = [ 'my-field-css' ];
```

### Simple Example: Local Tel Field with Pattern

```php
class Elementor_Local_Tel_Field extends \ElementorPro\Modules\Forms\Fields\Field_Base {
    public function get_type(): string { return 'local-tel'; }
    public function get_name(): string { return esc_html__( 'Local Tel', 'textdomain' ); }

    public function render( $item, $item_index, $form ): void {
        $form->add_render_attribute( 'input' . $item_index, [
            'size' => '1', 'class' => 'elementor-field-textual',
            'pattern' => '[0-9]{3}-[0-9]{3}-[0-9]{4}',
            'title' => esc_html__( 'Format: 123-456-7890', 'textdomain' ),
        ]);
        echo '<input ' . $form->get_render_attribute_string( 'input' . $item_index ) . '>';
    }

    public function validation( $field, $record, $ajax_handler ): void {
        if ( empty( $field['value'] ) ) { return; }
        if ( preg_match( '/^[0-9]{3}-[0-9]{3}-[0-9]{4}$/', $field['value'] ) !== 1 ) {
            $ajax_handler->add_error( $field['id'],
                esc_html__( 'Phone must be "123-456-7890" format.', 'textdomain' ) );
        }
    }

    public function __construct() {
        parent::__construct();
        add_action( 'elementor/preview/init', [ $this, 'editor_preview_footer' ] );
    }
    public function editor_preview_footer(): void { add_action( 'wp_footer', [ $this, 'content_template_script' ] ); }
    public function content_template_script(): void { ?>
        <script>
        jQuery( document ).ready( () => {
            elementor.hooks.addFilter( 'elementor_pro/forms/content_template/field/<?php echo $this->get_type(); ?>',
                function ( inputField, item, i ) {
                    return `<input id="form_field_${i}" class="elementor-field-textual elementor-field ${item.css_classes}" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}">`;
                }, 10, 3 );
        });
        </script>
    <?php }
}
```

### Advanced Example: Credit Card Field with Controls and Validation

```php
class Elementor_Credit_Card_Number_Field extends \ElementorPro\Modules\Forms\Fields\Field_Base {
    public function get_type(): string { return 'credit-card-number'; }
    public function get_name(): string { return esc_html__( 'Credit Card Number', 'textdomain' ); }

    public function render( $item, $item_index, $form ): void {
        $form->add_render_attribute( 'input' . $item_index, [
            'class' => 'elementor-field-textual', 'type' => 'tel',
            'inputmode' => 'numeric', 'maxlength' => '19',
            'pattern' => '[0-9]{4}\s[0-9]{4}\s[0-9]{4}\s[0-9]{4}',
            'placeholder' => $item['credit-card-placeholder'],
            'autocomplete' => 'cc-number',
        ]);
        echo '<input ' . $form->get_render_attribute_string( 'input' . $item_index ) . '>';
    }

    public function validation( $field, $record, $ajax_handler ): void {
        if ( empty( $field['value'] ) ) { return; }
        if ( preg_match( '/^[0-9]{4}\s[0-9]{4}\s[0-9]{4}\s[0-9]{4}$/', $field['value'] ) !== 1 ) {
            $ajax_handler->add_error( $field['id'],
                esc_html__( 'Card number must be "XXXX XXXX XXXX XXXX".', 'textdomain' ) );
        }
    }

    public function update_controls( $widget ): void {
        $elementor = \ElementorPro\Plugin::elementor();
        $control_data = $elementor->controls_manager->get_control_from_stack( $widget->get_unique_name(), 'form_fields' );
        if ( is_wp_error( $control_data ) ) { return; }
        $field_controls = [
            'credit-card-placeholder' => [
                'name' => 'credit-card-placeholder',
                'label' => esc_html__( 'Card Placeholder', 'textdomain' ),
                'type' => \Elementor\Controls_Manager::TEXT,
                'default' => 'xxxx xxxx xxxx xxxx',
                'dynamic' => [ 'active' => true ],
                'condition' => [ 'field_type' => $this->get_type() ],
                'tab' => 'content', 'inner_tab' => 'form_fields_content_tab', 'tabs_wrapper' => 'form_fields_tabs',
            ],
        ];
        $control_data['fields'] = $this->inject_field_controls( $control_data['fields'], $field_controls );
        $widget->update_control( 'form_fields', $control_data );
    }

    public function __construct() {
        parent::__construct();
        add_action( 'elementor/preview/init', [ $this, 'editor_preview_footer' ] );
    }
    public function editor_preview_footer(): void { add_action( 'wp_footer', [ $this, 'content_template_script' ] ); }
    public function content_template_script(): void { ?>
        <script>
        jQuery( document ).ready( () => {
            elementor.hooks.addFilter( 'elementor_pro/forms/content_template/field/<?php echo $this->get_type(); ?>',
                function ( inputField, item, i ) {
                    return `<input type="tel" id="form_field_${i}" class="elementor-field-textual elementor-field ${item.css_classes}" inputmode="numeric" maxlength="19" placeholder="${item['credit-card-placeholder']}" autocomplete="cc-number">`;
                }, 10, 3 );
        });
        </script>
    <?php }
}
```

### Removing Built-in Fields

```php
add_filter( 'elementor_pro/forms/field_types', function ( $fields ) {
    unset( $fields['upload'] ); // Remove file upload field
    return $fields;
});
```

---

## 3. Form Validation

Global validation hook fires before form processing:

```php
add_action( 'elementor_pro/forms/validation', function ( $record, $ajax_handler ) {
    $fields = $record->get( 'fields' );

    // Single field validation
    if ( ! empty( $fields['my_field']['value'] ) && strlen( $fields['my_field']['value'] ) < 5 ) {
        $ajax_handler->add_error( 'my_field', esc_html__( 'Min 5 characters.', 'textdomain' ) );
    }

    // Cross-field validation
    if ( ! empty( $fields['password']['value'] ) && ! empty( $fields['confirm']['value'] ) ) {
        if ( $fields['password']['value'] !== $fields['confirm']['value'] ) {
            $ajax_handler->add_error( 'confirm', esc_html__( 'Passwords do not match.', 'textdomain' ) );
        }
    }
}, 10, 2 );
```

Any `add_error()` call halts submission and returns errors to the client.

---

## 4. Form Processing Hooks

| Hook | Params | When |
|---|---|---|
| `elementor_pro/forms/validation` | `$record, $ajax_handler` | Before processing -- validate fields |
| `elementor_pro/forms/process` | `$record, $ajax_handler` | During form processing |
| `elementor_pro/forms/new_record` | `$record, $ajax_handler` | After successful submission |
| `elementor_pro/forms/mail_sent` | `$settings, $record` | After email action sends |

### Email Filters

```php
add_filter( 'elementor_pro/forms/wp_mail_headers', function ( $headers ) {
    return $headers . "Cc: copy@example.com\r\n";
});
add_filter( 'elementor_pro/forms/wp_mail_message', function ( $message ) {
    return $message . "\n\n-- Sent via My Site";
});
```

### Webhook Filter

```php
add_filter( 'elementor_pro/forms/webhooks/response', function ( $response, $record ) {
    if ( is_wp_error( $response ) ) {
        error_log( 'Webhook failed: ' . $response->get_error_message() );
    }
    return $response;
}, 10, 2 );
```

---

## 5. Common Mistakes

| Mistake | Fix |
|---|---|
| Missing `condition` on action controls section | Set `'condition' => [ 'submit_actions' => $this->get_name() ]` |
| Hardcoding HTML attributes in `render()` | Use `$form->add_render_attribute()` / `get_render_attribute_string()` |
| Not checking `empty( $field['value'] )` in validation | Always return early if empty (required check is separate) |
| Naming a method `content_template()` on field class | Reserved for future use -- use `content_template_script()` workaround |
| Exporting sensitive control data | Implement `on_export()` with `unset()` for all sensitive keys |
| Not escaping labels and attributes | Use `esc_html__()` for labels, `esc_attr()` for attributes |
| Missing `is_wp_error()` check in `update_controls()` | Always guard `get_control_from_stack()` result |
| Missing `tab`/`inner_tab`/`tabs_wrapper` on field controls | Required for controls to appear in the correct repeater tab |
| Wrong registration hook | Actions: `elementor_pro/forms/actions/register`. Fields: `elementor_pro/forms/fields/register` |
| Not calling `parent::__construct()` in field constructor | Required when overriding `__construct()` for editor preview |

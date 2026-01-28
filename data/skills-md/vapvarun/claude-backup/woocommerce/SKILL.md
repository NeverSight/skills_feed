---
name: woocommerce
description: WooCommerce development for WordPress e-commerce including custom product types, payment gateways, shipping methods, hooks, REST API, and store optimization. Use when building WooCommerce stores, customizing WooCommerce functionality, developing WooCommerce extensions, or debugging WooCommerce issues.
---

# WooCommerce Development

E-commerce development with WooCommerce for WordPress.

## Essential Hooks

### Product Hooks

```php
// Modify product price display
add_filter( 'woocommerce_get_price_html', function( $price_html, $product ) {
    if ( $product->is_on_sale() ) {
        $price_html .= '<span class="sale-badge">Sale!</span>';
    }
    return $price_html;
}, 10, 2 );

// Add custom field to product
add_action( 'woocommerce_product_options_general_product_data', function() {
    woocommerce_wp_text_input( array(
        'id'          => '_custom_field',
        'label'       => __( 'Custom Field', 'textdomain' ),
        'description' => __( 'Enter custom value', 'textdomain' ),
        'desc_tip'    => true,
    ) );
} );

// Save custom field
add_action( 'woocommerce_process_product_meta', function( $post_id ) {
    $value = isset( $_POST['_custom_field'] ) ? sanitize_text_field( $_POST['_custom_field'] ) : '';
    update_post_meta( $post_id, '_custom_field', $value );
} );
```

### Cart Hooks

```php
// Add fee to cart
add_action( 'woocommerce_cart_calculate_fees', function( $cart ) {
    if ( is_admin() && ! defined( 'DOING_AJAX' ) ) {
        return;
    }

    $subtotal = $cart->get_subtotal();

    // Add handling fee for orders under $50
    if ( $subtotal < 50 ) {
        $cart->add_fee( __( 'Handling Fee', 'textdomain' ), 5.00 );
    }
} );

// Validate cart items
add_action( 'woocommerce_check_cart_items', function() {
    $cart = WC()->cart;

    foreach ( $cart->get_cart() as $cart_item_key => $cart_item ) {
        $product = $cart_item['data'];

        // Check stock or custom validation
        if ( ! $product->is_in_stock() ) {
            wc_add_notice(
                sprintf( __( '%s is out of stock.', 'textdomain' ), $product->get_name() ),
                'error'
            );
        }
    }
} );

// Modify cart item data
add_filter( 'woocommerce_add_cart_item_data', function( $cart_item_data, $product_id, $variation_id ) {
    if ( isset( $_POST['custom_option'] ) ) {
        $cart_item_data['custom_option'] = sanitize_text_field( $_POST['custom_option'] );
    }
    return $cart_item_data;
}, 10, 3 );
```

### Checkout Hooks

```php
// Add custom checkout field
add_action( 'woocommerce_after_order_notes', function( $checkout ) {
    woocommerce_form_field( 'delivery_date', array(
        'type'        => 'date',
        'class'       => array( 'form-row-wide' ),
        'label'       => __( 'Preferred Delivery Date', 'textdomain' ),
        'required'    => true,
    ), $checkout->get_value( 'delivery_date' ) );
} );

// Validate custom field
add_action( 'woocommerce_checkout_process', function() {
    if ( empty( $_POST['delivery_date'] ) ) {
        wc_add_notice( __( 'Please select a delivery date.', 'textdomain' ), 'error' );
    }
} );

// Save custom field to order
add_action( 'woocommerce_checkout_update_order_meta', function( $order_id ) {
    if ( ! empty( $_POST['delivery_date'] ) ) {
        update_post_meta( $order_id, '_delivery_date', sanitize_text_field( $_POST['delivery_date'] ) );
    }
} );
```

### Order Hooks

```php
// After order is completed
add_action( 'woocommerce_order_status_completed', function( $order_id ) {
    $order = wc_get_order( $order_id );

    // Send to external system
    $data = array(
        'order_id'    => $order_id,
        'customer'    => $order->get_billing_email(),
        'total'       => $order->get_total(),
        'items'       => array(),
    );

    foreach ( $order->get_items() as $item ) {
        $data['items'][] = array(
            'product_id' => $item->get_product_id(),
            'quantity'   => $item->get_quantity(),
            'total'      => $item->get_total(),
        );
    }

    // Send to webhook
    wp_remote_post( 'https://api.example.com/orders', array(
        'body'    => wp_json_encode( $data ),
        'headers' => array( 'Content-Type' => 'application/json' ),
    ) );
} );

// Order status change
add_action( 'woocommerce_order_status_changed', function( $order_id, $old_status, $new_status, $order ) {
    // Custom notification logic
}, 10, 4 );
```

## Custom Product Types

```php
// Register custom product type
add_action( 'init', function() {
    class WC_Product_Subscription extends WC_Product {
        public function __construct( $product = 0 ) {
            $this->product_type = 'subscription';
            parent::__construct( $product );
        }

        public function get_type() {
            return 'subscription';
        }

        // Custom methods
        public function get_subscription_period() {
            return $this->get_meta( '_subscription_period' );
        }
    }
} );

// Add to product type selector
add_filter( 'product_type_selector', function( $types ) {
    $types['subscription'] = __( 'Subscription', 'textdomain' );
    return $types;
} );

// Show price fields
add_action( 'woocommerce_product_options_general_product_data', function() {
    global $product_object;

    if ( 'subscription' === $product_object->get_type() ) {
        woocommerce_wp_select( array(
            'id'      => '_subscription_period',
            'label'   => __( 'Billing Period', 'textdomain' ),
            'options' => array(
                'month' => __( 'Monthly', 'textdomain' ),
                'year'  => __( 'Yearly', 'textdomain' ),
            ),
        ) );
    }
} );
```

## Payment Gateways

```php
class WC_Gateway_Custom extends WC_Payment_Gateway {
    public function __construct() {
        $this->id                 = 'custom_gateway';
        $this->icon               = '';
        $this->has_fields         = true;
        $this->method_title       = __( 'Custom Gateway', 'textdomain' );
        $this->method_description = __( 'Custom payment gateway.', 'textdomain' );

        $this->supports = array(
            'products',
            'refunds',
        );

        $this->init_form_fields();
        $this->init_settings();

        $this->title       = $this->get_option( 'title' );
        $this->description = $this->get_option( 'description' );
        $this->enabled     = $this->get_option( 'enabled' );
        $this->api_key     = $this->get_option( 'api_key' );

        add_action( 'woocommerce_update_options_payment_gateways_' . $this->id, array( $this, 'process_admin_options' ) );
    }

    public function init_form_fields() {
        $this->form_fields = array(
            'enabled' => array(
                'title'   => __( 'Enable/Disable', 'textdomain' ),
                'type'    => 'checkbox',
                'label'   => __( 'Enable Custom Gateway', 'textdomain' ),
                'default' => 'no',
            ),
            'api_key' => array(
                'title'       => __( 'API Key', 'textdomain' ),
                'type'        => 'password',
                'description' => __( 'Enter your API key', 'textdomain' ),
            ),
        );
    }

    public function process_payment( $order_id ) {
        $order = wc_get_order( $order_id );

        // Process payment with external API
        $response = wp_remote_post( 'https://api.payment.com/charge', array(
            'body' => array(
                'amount'   => $order->get_total(),
                'currency' => $order->get_currency(),
                'token'    => sanitize_text_field( $_POST['payment_token'] ),
            ),
            'headers' => array(
                'Authorization' => 'Bearer ' . $this->api_key,
            ),
        ) );

        $body = json_decode( wp_remote_retrieve_body( $response ), true );

        if ( isset( $body['success'] ) && $body['success'] ) {
            $order->payment_complete( $body['transaction_id'] );
            WC()->cart->empty_cart();

            return array(
                'result'   => 'success',
                'redirect' => $this->get_return_url( $order ),
            );
        } else {
            wc_add_notice( $body['error'] ?? __( 'Payment failed', 'textdomain' ), 'error' );
            return array( 'result' => 'fail' );
        }
    }

    public function process_refund( $order_id, $amount = null, $reason = '' ) {
        $order = wc_get_order( $order_id );

        $response = wp_remote_post( 'https://api.payment.com/refund', array(
            'body' => array(
                'transaction_id' => $order->get_transaction_id(),
                'amount'         => $amount,
            ),
        ) );

        $body = json_decode( wp_remote_retrieve_body( $response ), true );

        if ( isset( $body['success'] ) && $body['success'] ) {
            return true;
        }

        return new WP_Error( 'refund_failed', $body['error'] ?? 'Refund failed' );
    }
}

// Register gateway
add_filter( 'woocommerce_payment_gateways', function( $gateways ) {
    $gateways[] = 'WC_Gateway_Custom';
    return $gateways;
} );
```

## REST API

### Custom Endpoints

```php
add_action( 'rest_api_init', function() {
    register_rest_route( 'custom/v1', '/products/featured', array(
        'methods'             => 'GET',
        'callback'            => 'get_featured_products',
        'permission_callback' => '__return_true',
    ) );
} );

function get_featured_products( WP_REST_Request $request ) {
    $args = array(
        'post_type'      => 'product',
        'posts_per_page' => $request->get_param( 'per_page' ) ?: 10,
        'tax_query'      => array(
            array(
                'taxonomy' => 'product_visibility',
                'field'    => 'name',
                'terms'    => 'featured',
            ),
        ),
    );

    $products = wc_get_products( $args );

    return array_map( function( $product ) {
        return array(
            'id'         => $product->get_id(),
            'name'       => $product->get_name(),
            'price'      => $product->get_price(),
            'image'      => wp_get_attachment_url( $product->get_image_id() ),
            'permalink'  => $product->get_permalink(),
        );
    }, $products );
}
```

### Extend Existing Endpoints

```php
// Add custom field to product API response
add_filter( 'woocommerce_rest_prepare_product_object', function( $response, $product, $request ) {
    $response->data['custom_field'] = $product->get_meta( '_custom_field' );
    $response->data['stock_status_label'] = $product->is_in_stock() ? 'Available' : 'Out of Stock';
    return $response;
}, 10, 3 );

// Allow updating custom field via API
add_action( 'woocommerce_rest_insert_product_object', function( $product, $request, $creating ) {
    if ( isset( $request['custom_field'] ) ) {
        $product->update_meta_data( '_custom_field', sanitize_text_field( $request['custom_field'] ) );
        $product->save();
    }
}, 10, 3 );
```

## Performance

### Query Optimization

```php
// Disable unnecessary features
add_filter( 'woocommerce_background_image_regeneration', '__return_false' );
add_filter( 'woocommerce_enable_nocache_headers', '__return_false' );

// Limit product queries
add_filter( 'loop_shop_per_page', function() {
    return 24; // Products per page
} );

// Cache expensive queries
function get_best_sellers( $limit = 5 ) {
    $cache_key = 'wc_best_sellers_' . $limit;
    $products  = get_transient( $cache_key );

    if ( false === $products ) {
        global $wpdb;

        $products = $wpdb->get_results( $wpdb->prepare( "
            SELECT p.ID, p.post_title, SUM(oim.meta_value) as total_sales
            FROM {$wpdb->posts} p
            INNER JOIN {$wpdb->prefix}woocommerce_order_items oi ON p.ID = oi.order_item_name
            INNER JOIN {$wpdb->prefix}woocommerce_order_itemmeta oim ON oi.order_item_id = oim.order_item_id
            WHERE oim.meta_key = '_qty'
            AND p.post_type = 'product'
            AND p.post_status = 'publish'
            GROUP BY p.ID
            ORDER BY total_sales DESC
            LIMIT %d
        ", $limit ) );

        set_transient( $cache_key, $products, HOUR_IN_SECONDS );
    }

    return $products;
}

// Clear cache on order
add_action( 'woocommerce_order_status_completed', function() {
    delete_transient( 'wc_best_sellers_5' );
} );
```

### AJAX Cart

```php
// Update cart via AJAX
add_action( 'wp_ajax_update_cart_item', 'ajax_update_cart_item' );
add_action( 'wp_ajax_nopriv_update_cart_item', 'ajax_update_cart_item' );

function ajax_update_cart_item() {
    check_ajax_referer( 'wc_cart_nonce', 'nonce' );

    $cart_item_key = sanitize_text_field( $_POST['cart_item_key'] );
    $quantity      = absint( $_POST['quantity'] );

    if ( $quantity > 0 ) {
        WC()->cart->set_quantity( $cart_item_key, $quantity );
    } else {
        WC()->cart->remove_cart_item( $cart_item_key );
    }

    WC_AJAX::get_refreshed_fragments();
}
```

## Email Customization

```php
// Add content to order emails
add_action( 'woocommerce_email_order_details', function( $order, $sent_to_admin, $plain_text, $email ) {
    if ( 'customer_completed_order' === $email->id ) {
        echo '<h2>Thank you for your order!</h2>';
        echo '<p>Your order will be shipped within 2-3 business days.</p>';
    }
}, 5, 4 );

// Custom email
class WC_Email_Custom extends WC_Email {
    public function __construct() {
        $this->id             = 'custom_email';
        $this->title          = __( 'Custom Email', 'textdomain' );
        $this->description    = __( 'Custom email notification', 'textdomain' );
        $this->template_html  = 'emails/custom-email.php';
        $this->template_plain = 'emails/plain/custom-email.php';

        parent::__construct();
    }

    public function trigger( $order_id ) {
        if ( ! $order_id ) return;

        $this->object = wc_get_order( $order_id );
        $this->recipient = $this->object->get_billing_email();

        if ( ! $this->is_enabled() || ! $this->get_recipient() ) return;

        $this->send(
            $this->get_recipient(),
            $this->get_subject(),
            $this->get_content(),
            $this->get_headers(),
            $this->get_attachments()
        );
    }
}

add_filter( 'woocommerce_email_classes', function( $emails ) {
    $emails['WC_Email_Custom'] = new WC_Email_Custom();
    return $emails;
} );
```

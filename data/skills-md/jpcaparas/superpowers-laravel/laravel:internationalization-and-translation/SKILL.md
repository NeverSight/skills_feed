---
name: laravel:internationalization-and-translation
description: Build with i18n in mind from day one using Laravel translation helpers, JSON files, Blade integration, and locale management
---

# Internationalization and Translation (i18n)

Build your Laravel application with internationalization in mind from the start. Even if you're only supporting one language initially, wrapping strings in translation functions makes future localization much easier.

## Why Translate From the Start?

```php
// BAD: Hardcoded strings are difficult to change later
return view('welcome', [
    'message' => 'Welcome to our application!'
]);

// GOOD: Translatable from day one
return view('welcome', [
    'message' => __('Welcome to our application!')
]);
```

## Basic Translation Setup

### 1. Configure Available Locales

```php
// config/app.php
return [
    'locale' => 'en',
    'fallback_locale' => 'en',
    'available_locales' => ['en', 'es', 'fr', 'de', 'ja'],
    'faker_locale' => 'en_US',
];

// app/Http/Middleware/SetLocale.php
class SetLocale
{
    public function handle(Request $request, Closure $next): Response
    {
        $locale = $request->user()?->locale
            ?? session('locale')
            ?? $request->getPreferredLanguage(config('app.available_locales'))
            ?? config('app.locale');

        app()->setLocale($locale);

        return $next($request);
    }
}
```

### 2. Translation File Structure

```php
// lang/en/messages.php
return [
    'welcome' => 'Welcome to :app_name',
    'greeting' => 'Hello, :name!',
    'item_count' => '{0} No items|{1} One item|[2,*] :count items',
    'account' => [
        'profile' => 'Profile',
        'settings' => 'Settings',
        'logout' => 'Sign out',
    ],
];

// lang/es/messages.php
return [
    'welcome' => 'Bienvenido a :app_name',
    'greeting' => '¡Hola, :name!',
    'item_count' => '{0} Sin artículos|{1} Un artículo|[2,*] :count artículos',
    'account' => [
        'profile' => 'Perfil',
        'settings' => 'Configuración',
        'logout' => 'Cerrar sesión',
    ],
];
```

### 3. JSON Translation Files (for Single-Line Keys)

```json
// lang/en.json
{
    "Welcome back!": "Welcome back!",
    "Your order has been confirmed": "Your order has been confirmed",
    "Please verify your email address": "Please verify your email address"
}

// lang/es.json
{
    "Welcome back!": "¡Bienvenido de nuevo!",
    "Your order has been confirmed": "Su pedido ha sido confirmado",
    "Please verify your email address": "Por favor verifica tu dirección de correo"
}
```

## Translation Helpers

### Basic Translation

```php
// Using __() helper
echo __('messages.welcome', ['app_name' => config('app.name')]);

// Using trans() helper
echo trans('messages.greeting', ['name' => $user->name]);

// Direct strings (uses JSON files)
echo __('Welcome back!');

// Pluralization
echo trans_choice('messages.item_count', $count, ['count' => $count]);
```

### In Blade Templates

```blade
{{-- Basic translation --}}
<h1>{{ __('messages.welcome', ['app_name' => config('app.name')]) }}</h1>

{{-- Direct string translation --}}
<p>{{ __('Please verify your email address') }}</p>

{{-- With @lang directive --}}
<p>@lang('messages.greeting', ['name' => $user->name])</p>

{{-- Pluralization --}}
<p>{{ trans_choice('messages.item_count', $cart->count(), ['count' => $cart->count()]) }}</p>

{{-- Inside attributes --}}
<button title="{{ __('Click to continue') }}">
    {{ __('Next') }}
</button>
```

## Advanced Features

### 1. Translatable Model Attributes

```php
// app/Models/Product.php
use Spatie\Translatable\HasTranslations;

class Product extends Model
{
    use HasTranslations;

    public $translatable = ['name', 'description'];

    protected $casts = [
        'name' => 'array',
        'description' => 'array',
    ];
}

// Usage
$product = Product::create([
    'name' => [
        'en' => 'Laptop',
        'es' => 'Portátil',
        'fr' => 'Ordinateur portable',
    ],
    'description' => [
        'en' => 'High-performance laptop',
        'es' => 'Portátil de alto rendimiento',
        'fr' => 'Ordinateur portable haute performance',
    ],
]);

// Automatic locale detection
echo $product->name; // Uses app()->getLocale()

// Specific locale
echo $product->getTranslation('name', 'es'); // Portátil
```

### 2. Route Localization

```php
// routes/web.php
Route::middleware(['web', 'setlocale'])->group(function () {
    Route::get('/', [HomeController::class, 'index'])->name('home');

    // Localized routes
    Route::prefix('{locale}')
        ->where(['locale' => '[a-z]{2}'])
        ->middleware('locale')
        ->group(function () {
            Route::get('/', [HomeController::class, 'index'])->name('localized.home');
            Route::get('/about', [PageController::class, 'about'])->name('localized.about');
        });
});

// app/Http/Middleware/LocaleMiddleware.php
class LocaleMiddleware
{
    public function handle($request, Closure $next)
    {
        if ($locale = $request->route('locale')) {
            if (in_array($locale, config('app.available_locales'))) {
                app()->setLocale($locale);
                session(['locale' => $locale]);
            }
        }

        return $next($request);
    }
}
```

### 3. Form Validation Messages

```php
// lang/en/validation.php
return [
    'required' => 'The :attribute field is required.',
    'email' => 'The :attribute must be a valid email address.',
    'custom' => [
        'email' => [
            'required' => 'We need your email address!',
            'unique' => 'This email is already registered.',
        ],
    ],
    'attributes' => [
        'email' => 'email address',
        'name' => 'full name',
    ],
];

// In FormRequest
class RegisterRequest extends FormRequest
{
    public function messages()
    {
        return [
            'email.required' => __('validation.custom.email.required'),
            'email.unique' => __('validation.custom.email.unique'),
        ];
    }

    public function attributes()
    {
        return [
            'email' => __('validation.attributes.email'),
            'name' => __('validation.attributes.name'),
        ];
    }
}
```

### 4. Date and Number Formatting

```php
// app/Helpers/LocaleHelper.php
class LocaleHelper
{
    public static function formatDate(Carbon $date): string
    {
        return match(app()->getLocale()) {
            'en' => $date->format('m/d/Y'),
            'es' => $date->format('d/m/Y'),
            'de' => $date->format('d.m.Y'),
            'ja' => $date->format('Y年m月d日'),
            default => $date->toDateString(),
        };
    }

    public static function formatCurrency(float $amount, string $currency = 'USD'): string
    {
        $formatter = new NumberFormatter(app()->getLocale(), NumberFormatter::CURRENCY);
        return $formatter->formatCurrency($amount, $currency);
    }

    public static function formatNumber(float $number, int $decimals = 2): string
    {
        $formatter = new NumberFormatter(app()->getLocale(), NumberFormatter::DECIMAL);
        $formatter->setAttribute(NumberFormatter::MAX_FRACTION_DIGITS, $decimals);
        return $formatter->format($number);
    }
}

// Usage in Blade
<p>{{ LocaleHelper::formatDate($order->created_at) }}</p>
<p>{{ LocaleHelper::formatCurrency($order->total, 'EUR') }}</p>
<p>{{ LocaleHelper::formatNumber($product->weight, 2) }} kg</p>
```

### 5. Language Switcher Component

```blade
{{-- resources/views/components/language-switcher.blade.php --}}
<div class="language-switcher">
    <select onchange="window.location.href=this.value"
            aria-label="{{ __('Select Language') }}">
        @foreach(config('app.available_locales') as $locale)
            <option value="{{ route('locale.switch', $locale) }}"
                    @selected(app()->getLocale() === $locale)>
                {{ strtoupper($locale) }}
            </option>
        @endforeach
    </select>
</div>

{{-- Or as links --}}
<ul class="language-menu">
    @foreach(config('app.available_locales') as $locale)
        <li>
            <a href="{{ route('locale.switch', $locale) }}"
               @class(['active' => app()->getLocale() === $locale])>
                {{ __("languages.$locale") }}
            </a>
        </li>
    @endforeach
</ul>
```

### 6. Email Localization

```php
// app/Mail/OrderConfirmation.php
class OrderConfirmation extends Mailable
{
    use Queueable, SerializesModels;

    public function __construct(
        public Order $order,
        public string $locale
    ) {}

    public function build()
    {
        return $this->locale($this->locale)
            ->subject(__('mail.order_confirmation.subject'))
            ->view('emails.order-confirmation');
    }
}

// Send email in user's language
Mail::to($user)->send(new OrderConfirmation($order, $user->locale));
```

## JavaScript Translation

### 1. Export Translations to JavaScript

```php
// app/Http/Controllers/TranslationController.php
class TranslationController extends Controller
{
    public function index(Request $request)
    {
        $locale = $request->get('locale', app()->getLocale());
        $translations = Cache::remember("translations.{$locale}", 3600, function () use ($locale) {
            return collect(File::allFiles(lang_path($locale)))
                ->flatMap(function ($file) use ($locale) {
                    return [
                        $file->getBasename('.php') => include $file->getPathname()
                    ];
                })->toJson();
        });

        return response($translations)->header('Content-Type', 'application/json');
    }
}

// In JavaScript
const translations = await fetch(`/api/translations?locale=${locale}`).then(r => r.json());

function __(key, replace = {}) {
    let translation = key.split('.').reduce((t, i) => t?.[i], translations) || key;

    Object.keys(replace).forEach(key => {
        translation = translation.replace(`:${key}`, replace[key]);
    });

    return translation;
}

// Usage
console.log(__('messages.welcome', { app_name: 'MyApp' }));
```

### 2. Using Laravel Mix/Vite

```javascript
// resources/js/i18n.js
import { createI18n } from 'vue-i18n';

const messages = {
    en: require('./locales/en.json'),
    es: require('./locales/es.json'),
    fr: require('./locales/fr.json'),
};

export default createI18n({
    locale: document.documentElement.lang || 'en',
    fallbackLocale: 'en',
    messages,
});

// In Vue component
<template>
    <h1>{{ $t('messages.welcome', { app_name: appName }) }}</h1>
</template>
```

## Testing Translations

```php
test('displays content in selected language', function () {
    // Test English
    $response = $this->withSession(['locale' => 'en'])
        ->get('/');

    $response->assertSee('Welcome to our application');

    // Test Spanish
    $response = $this->withSession(['locale' => 'es'])
        ->get('/');

    $response->assertSee('Bienvenido a nuestra aplicación');
});

test('falls back to default locale for missing translations', function () {
    app()->setLocale('fr');

    // If French translation missing, falls back to English
    expect(__('some.missing.key'))->toBe('some.missing.key');
    expect(__('messages.welcome', ['app_name' => 'Test']))->not->toBeEmpty();
});

test('pluralization works correctly', function () {
    expect(trans_choice('messages.item_count', 0))->toBe('No items');
    expect(trans_choice('messages.item_count', 1))->toBe('One item');
    expect(trans_choice('messages.item_count', 5, ['count' => 5]))->toBe('5 items');
});
```

## Best Practices

1. **Always wrap user-facing strings**
   ```php
   // Even in single-language apps
   flash(__('Your changes have been saved.'));
   ```

2. **Use meaningful translation keys**
   ```php
   // BAD
   __('msg1')

   // GOOD
   __('auth.login_successful')
   ```

3. **Group related translations**
   ```php
   // lang/en/auth.php
   return [
       'login' => 'Sign in',
       'logout' => 'Sign out',
       'register' => 'Register',
       'forgot_password' => 'Forgot your password?',
   ];
   ```

4. **Provide context in keys**
   ```php
   // Different contexts may need different translations
   __('button.save')  // "Save"
   __('message.save')  // "Your changes will be saved"
   __('title.save')    // "Save Document"
   ```

5. **Handle missing translations gracefully**
   ```php
   class AppServiceProvider extends ServiceProvider
   {
       public function boot()
       {
           // Log missing translations in production
           if (app()->environment('production')) {
               Event::listen(TranslationNotFound::class, function ($event) {
                   Log::warning('Missing translation', [
                       'key' => $event->key,
                       'locale' => $event->locale,
                   ]);
               });
           }
       }
   }
   ```

6. **Cache translations in production**
   ```bash
   # Cache for better performance
   sail artisan lang:cache

   # Clear when updating
   sail artisan lang:clear
   ```

Remember: Start with translations from day one. It's much easier to maintain translations as you build than to retrofit them later!
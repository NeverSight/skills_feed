---
name: leptos-guide
description: Leptos v0.8.x frontend development guide. Components, signals, resources, async, forms, and ownership patterns.
---

# Leptos v0.8.x Development Guide

## Signals (Reactive Primitives)

```rust
let (count, set_count) = signal(0);   // Tuple form
let count = RwSignal::new(0);         // RwSignal form

// Read
count.get()    // Clone value
count.read()   // Get reference (&T)

// Write
set_count.set(1)
set_count.update(|n| *n += 1)
count.write()  // Get &mut T
```

## Components

```rust
#[component]
pub fn MyComponent(
    title: String,
    #[prop(optional)] class: Option<String>,
    #[prop(default = 10)] limit: usize,
    children: Children,
) -> impl IntoView {
    view! {
        <div class=class.unwrap_or_default()>
            <h1>{title}</h1>
            {children()}
        </div>
    }
}
```

## Effect & Memo

```rust
// Side effects
Effect::new(move |_| { log::info!("count: {}", count.get()); });

// Derived signal (cached)
let doubled = Memo::new(move |_| count.get() * 2);
```

## Resource (Async Data)

```rust
let user = Resource::new(
    move || user_id.get(),
    |id| async move { fetch_user(id).await }
);

view! {
    <Suspense fallback=|| view! { <p>"Loading..."</p> }>
        {move || user.get().map(|u| view! { <p>{u.name}</p> })}
    </Suspense>
}
```

## Action (Form Submit)

```rust
let submit = Action::new(|data: &FormData| {
    let data = data.clone();
    async move { submit_form(data).await }
});

view! {
    <form on:submit=move |ev| {
        ev.prevent_default();
        submit.dispatch(form_data);
    }> /* ... */ </form>
}
```

## Patterns

### Conditional Rendering
```rust
<Show when=move || count.get() > 0 fallback=|| view! { <p>"Empty"</p> }>
    <p>"Has items"</p>
</Show>

{move || match status.get() {
    Status::Loading => view! { <p>"Loading"</p> }.into_any(),
    Status::Ok(data) => view! { <Data data/> }.into_any(),
}}
```

### List Rendering
```rust
<For
    each=move || items.get()
    key=|item| item.id
    children=|item| view! { <li>{item.name}</li> }
/>
```

### Context
```rust
// Provider
provide_context(AppState::new());

// Consumer
let state = expect_context::<AppState>();
```

---

## Ownership Patterns (Critical)

### Why Needed
Leptos Signals don't implement Copy. Moving into closures/async blocks transfers ownership.

### StoredValue (Recommended for async)
```rust
let api = StoredValue::new(client.clone());

Effect::new(move |_| {
    let api = api.get_value();  // Get inside Effect
    spawn_local(async move { api.fetch().await; });
});
```

### Callback (Event handlers)
```rust
let on_delete = Callback::new(move |id: i32| {
    set_items.update(|items| items.retain(|i| i.id != id));
});

// Child: on_delete.run(id)
```

### Clone Pattern
```rust
let count = RwSignal::new(0);
let count_clone = count.clone();
let closure1 = move || count.get();
let closure2 = move || count_clone.get();
```

## Common Mistakes

```rust
// ❌ Wrong: get_value outside Effect
let api_value = api.get_value();
Effect::new(move |_| { spawn_local(async move { api_value.fetch().await; }); });

// ✅ Correct: get_value inside Effect
Effect::new(move |_| {
    let api = api.get_value();
    spawn_local(async move { api.fetch().await; });
});

// ❌ Wrong: Infinite loop
Effect::new(move |_| { signal.set(signal.get() + 1); });

// ✅ Correct: Use get_untracked()
Effect::new(move |_| {
    let val = signal.get_untracked();
    if should_update { signal.set(val + 1); }
});
```

## Quick Reference

| Use Case | Pattern |
|----------|---------|
| API client in Effect | `StoredValue::new(client.clone())` |
| Signal in multiple closures | `let sig_clone = sig.clone()` |
| Child→Parent events | `Callback<T>` |
| Track previous value | `StoredValue::new(initial)` |
| Conditional read | `signal.get_untracked()` |

---
name: gpui-patterns
description: Common GPUI patterns including component composition, state management strategies, event handling, and action dispatching. Use when user needs guidance on GPUI patterns, component design, or state management approaches.
---

# GPUI Patterns

## Metadata

This skill provides comprehensive guidance on common GPUI patterns and best practices for building maintainable, performant applications.

## Instructions

### Component Composition Patterns

#### Basic Component Structure

```rust
use gpui::*;

// View component with state
struct MyView {
    state: Model<MyState>,
    _subscription: Subscription,
}

impl MyView {
    fn new(state: Model<MyState>, cx: &mut ViewContext<Self>) -> Self {
        let _subscription = cx.observe(&state, |_, _, cx| cx.notify());
        Self { state, _subscription }
    }
}

impl Render for MyView {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let state = self.state.read(cx);

        div()
            .flex()
            .flex_col()
            .child(format!("Value: {}", state.value))
    }
}
```

#### Container/Presenter Pattern

**Container** (manages state and logic):
```rust
struct Container {
    model: Model<AppState>,
    _subscription: Subscription,
}

impl Container {
    fn new(model: Model<AppState>, cx: &mut ViewContext<Self>) -> Self {
        let _subscription = cx.observe(&model, |_, _, cx| cx.notify());
        Self { model, _subscription }
    }
}

impl Render for Container {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let state = self.model.read(cx);

        // Pass data to presenter
        Presenter::new(state.data.clone())
    }
}
```

**Presenter** (pure rendering):
```rust
struct Presenter {
    data: String,
}

impl Presenter {
    fn new(data: String) -> Self {
        Self { data }
    }
}

impl Render for Presenter {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        div().child(self.data.as_str())
    }
}
```

#### Compound Components

```rust
// Parent component with shared context
pub struct Tabs {
    items: Vec<TabItem>,
    active_index: usize,
}

pub struct TabItem {
    label: String,
    content: Box<dyn Fn() -> AnyElement>,
}

impl Tabs {
    pub fn new() -> Self {
        Self {
            items: Vec::new(),
            active_index: 0,
        }
    }

    pub fn add_tab(
        mut self,
        label: impl Into<String>,
        content: impl Fn() -> AnyElement + 'static,
    ) -> Self {
        self.items.push(TabItem {
            label: label.into(),
            content: Box::new(content),
        });
        self
    }

    fn set_active(&mut self, index: usize, cx: &mut ViewContext<Self>) {
        self.active_index = index;
        cx.notify();
    }
}

impl Render for Tabs {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        div()
            .flex()
            .flex_col()
            .child(
                // Tab headers
                div()
                    .flex()
                    .children(
                        self.items.iter().enumerate().map(|(i, item)| {
                            tab_header(&item.label, i == self.active_index, || {
                                self.set_active(i, cx)
                            })
                        })
                    )
            )
            .child(
                // Active tab content
                (self.items[self.active_index].content)()
            )
    }
}
```

### State Management Strategies

#### Model-View Pattern

```rust
// Model: Application state
#[derive(Clone)]
struct AppState {
    count: usize,
    items: Vec<String>,
}

// View: Observes and renders state
struct AppView {
    state: Model<AppState>,
    _subscription: Subscription,
}

impl AppView {
    fn new(state: Model<AppState>, cx: &mut ViewContext<Self>) -> Self {
        let _subscription = cx.observe(&state, |_, _, cx| cx.notify());
        Self { state, _subscription }
    }

    fn increment(&mut self, cx: &mut ViewContext<Self>) {
        self.state.update(cx, |state, cx| {
            state.count += 1;
            cx.notify();
        });
    }
}
```

#### Context-Based State

```rust
// Global state via context
#[derive(Clone)]
struct GlobalSettings {
    theme: Theme,
    language: String,
}

impl Global for GlobalSettings {}

// Initialize in app
fn init_app(cx: &mut AppContext) {
    cx.set_global(GlobalSettings {
        theme: Theme::Light,
        language: "en".to_string(),
    });
}

// Access in components
impl Render for MyView {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let settings = cx.global::<GlobalSettings>();

        div()
            .child(format!("Language: {}", settings.language))
    }
}
```

#### Subscription Patterns

**Basic Subscription**:
```rust
struct Observer {
    model: Model<Data>,
    _subscription: Subscription,
}

impl Observer {
    fn new(model: Model<Data>, cx: &mut ViewContext<Self>) -> Self {
        let _subscription = cx.observe(&model, |_, _, cx| {
            cx.notify();  // Rerender on change
        });

        Self { model, _subscription }
    }
}
```

**Selective Updates**:
```rust
impl Observer {
    fn new(model: Model<Data>, cx: &mut ViewContext<Self>) -> Self {
        let _subscription = cx.observe(&model, |this, model, cx| {
            let data = model.read(cx);

            // Only rerender if specific field changed
            if data.important_field != this.cached_field {
                this.cached_field = data.important_field.clone();
                cx.notify();
            }
        });

        Self {
            model,
            cached_field: String::new(),
            _subscription,
        }
    }
}
```

**Multiple Subscriptions**:
```rust
struct MultiObserver {
    model_a: Model<DataA>,
    model_b: Model<DataB>,
    _subscriptions: Vec<Subscription>,
}

impl MultiObserver {
    fn new(
        model_a: Model<DataA>,
        model_b: Model<DataB>,
        cx: &mut ViewContext<Self>,
    ) -> Self {
        let mut subscriptions = Vec::new();

        subscriptions.push(cx.observe(&model_a, |_, _, cx| cx.notify()));
        subscriptions.push(cx.observe(&model_b, |_, _, cx| cx.notify()));

        Self {
            model_a,
            model_b,
            _subscriptions: subscriptions,
        }
    }
}
```

### Event Handling Patterns

#### Click Events

```rust
div()
    .on_click(cx.listener(|this, event: &ClickEvent, cx| {
        // Handle click
        this.handle_click(cx);
    }))
    .child("Click me")
```

#### Keyboard Events

```rust
div()
    .on_key_down(cx.listener(|this, event: &KeyDownEvent, cx| {
        match event.key.as_str() {
            "Enter" => this.submit(cx),
            "Escape" => this.cancel(cx),
            _ => {}
        }
    }))
```

#### Event Propagation

```rust
// Stop propagation
div()
    .on_click(|event, cx| {
        event.stop_propagation();
        // Handle click
    })

// Prevent default
div()
    .on_key_down(|event, cx| {
        if event.key == "Tab" {
            event.prevent_default();
            // Custom tab handling
        }
    })
```

#### Mouse Events

```rust
div()
    .on_mouse_down(cx.listener(|this, event, cx| {
        this.mouse_down_position = Some(event.position);
    }))
    .on_mouse_move(cx.listener(|this, event, cx| {
        if let Some(start) = this.mouse_down_position {
            let delta = event.position - start;
            this.handle_drag(delta, cx);
        }
    }))
    .on_mouse_up(cx.listener(|this, event, cx| {
        this.mouse_down_position = None;
    }))
```

### Action System

#### Define Actions

```rust
use gpui::*;

actions!(app, [
    Increment,
    Decrement,
    Reset,
    SetValue
]);

// Action with data
#[derive(Clone, PartialEq)]
pub struct SetValue {
    pub value: i32,
}

impl_actions!(app, [SetValue]);
```

#### Register Action Handlers

```rust
impl Counter {
    fn register_actions(&mut self, cx: &mut ViewContext<Self>) {
        cx.on_action(cx.listener(|this, _: &Increment, cx| {
            this.model.update(cx, |state, cx| {
                state.count += 1;
                cx.notify();
            });
        }));

        cx.on_action(cx.listener(|this, _: &Decrement, cx| {
            this.model.update(cx, |state, cx| {
                state.count = state.count.saturating_sub(1);
                cx.notify();
            });
        }));

        cx.on_action(cx.listener(|this, action: &SetValue, cx| {
            this.model.update(cx, |state, cx| {
                state.count = action.value;
                cx.notify();
            });
        }));
    }
}
```

#### Dispatch Actions

```rust
// From within component
fn handle_button_click(&mut self, cx: &mut ViewContext<Self>) {
    cx.dispatch_action(Increment);
}

// With data
fn set_specific_value(&mut self, value: i32, cx: &mut ViewContext<Self>) {
    cx.dispatch_action(SetValue { value });
}

// Global action dispatch
cx.dispatch_action_on_window(Reset, window_id);
```

#### Keybindings

```rust
// Register global keybindings
fn register_keybindings(cx: &mut AppContext) {
    cx.bind_keys([
        KeyBinding::new("cmd-+", Increment, None),
        KeyBinding::new("cmd--", Decrement, None),
        KeyBinding::new("cmd-0", Reset, None),
    ]);
}
```

### Element Composition

#### Builder Pattern

```rust
fn card(title: &str, content: impl IntoElement) -> impl IntoElement {
    div()
        .flex()
        .flex_col()
        .bg(white())
        .border_1()
        .rounded_lg()
        .shadow_sm()
        .p_6()
        .child(
            div()
                .text_lg()
                .font_semibold()
                .mb_4()
                .child(title)
        )
        .child(content)
}
```

#### Conditional Rendering

```rust
div()
    .when(condition, |this| {
        this.bg(blue_500())
    })
    .when_some(optional_value, |this, value| {
        this.child(format!("Value: {}", value))
    })
    .map(|this| {
        if complex_condition {
            this.border_1()
        } else {
            this.border_2()
        }
    })
```

#### Dynamic Children

```rust
div()
    .children(
        items.iter().map(|item| {
            div().child(item.name.as_str())
        })
    )
```

### View Lifecycle

#### Initialization

```rust
impl MyView {
    fn new(cx: &mut ViewContext<Self>) -> Self {
        // Initialize state
        let model = cx.new_model(|_| MyState::default());

        // Set up subscriptions
        let subscription = cx.observe(&model, |_, _, cx| cx.notify());

        // Spawn async tasks
        cx.spawn(|this, mut cx| async move {
            // Async initialization
        }).detach();

        Self {
            model,
            _subscription: subscription,
        }
    }
}
```

#### Update Notifications

```rust
impl MyView {
    fn update_state(&mut self, new_data: Data, cx: &mut ViewContext<Self>) {
        self.model.update(cx, |state, cx| {
            state.data = new_data;
            cx.notify();  // Trigger rerender
        });
    }
}
```

#### Cleanup

```rust
impl Drop for MyView {
    fn drop(&mut self) {
        // Manual cleanup if needed
        // Subscriptions are automatically dropped
    }
}
```

### Reactive Patterns

#### Derived State

```rust
impl Render for MyView {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let state = self.model.read(cx);

        // Compute derived values
        let total = state.items.iter().map(|i| i.value).sum::<i32>();
        let average = total / state.items.len() as i32;

        div()
            .child(format!("Total: {}", total))
            .child(format!("Average: {}", average))
    }
}
```

#### Async Updates

```rust
impl MyView {
    fn load_data(&mut self, cx: &mut ViewContext<Self>) {
        let model = self.model.clone();

        cx.spawn(|_, mut cx| async move {
            let data = fetch_data().await?;

            cx.update_model(&model, |state, cx| {
                state.data = data;
                cx.notify();
            })?;

            Ok::<_, anyhow::Error>(())
        }).detach();
    }
}
```

## Resources

### Official Documentation
- GPUI GitHub: https://github.com/zed-industries/zed/tree/main/crates/gpui
- Zed Editor Source: Real-world GPUI examples

### Common Patterns Reference
- Model-View: State management pattern
- Container-Presenter: Separation of concerns
- Compound Components: Related components working together
- Action System: Command pattern for user interactions
- Subscriptions: Observer pattern for reactive updates

### Best Practices
- Store subscriptions to prevent cleanup
- Use `cx.notify()` sparingly
- Prefer composition over inheritance
- Keep render methods pure
- Handle errors gracefully
- Document component APIs
- Test component behavior

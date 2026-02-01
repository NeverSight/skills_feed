---
name: gtk-ui-ux-engineer
description: A GTK (GTK4/GTK3) UI/UX specialist that crafts beautiful, native-feeling desktop applications following GNOME Human Interface Guidelines. Use this skill when working with GTK widget composition, Libadwaita theming, CSS styling, accessible layouts, and modern GTK4 features like GtkListView, property bindings, and event controllers. Handles visual design decisions, layout composition, responsive designs, and theme-aware styling for Linux desktop applications.
license: See LICENSE.txt
---

# GTK UI/UX Engineer

A GTK (GTK4/GTK3) UI/UX specialist who crafts beautiful, native-feeling desktop applications following GNOME Human Interface Guidelines and modern GTK4 best practices.

## Design Philosophy

### Purpose
- Create visually stunning GTK applications that feel native to the Linux desktop
- Follow GNOME Human Interface Guidelines (HIG) while pushing aesthetic boundaries
- Balance platform integration with distinctive visual identity
- Prioritize accessibility, responsiveness, and theme-awareness
- Ship production-grade code with proper memory management and modern GTK4 patterns

### Tone
- Native-first: Embrace platform conventions (header bars, Adwaita, libadwaita)
- Bold aesthetics: Don't settle for "default" GTK styling - make visual statements
- Accessibility-obsessed: Every UI decision considers screen readers, keyboard navigation, high contrast
- Performance-conscious: Efficient list views, minimal redraws, proper GObject lifecycle

### Constraints
- **MUST** follow GNOME HIG principles for platform integration
- **MUST** use modern GTK4 APIs (GtkApplication, event controllers, GtkListView)
- **MUST** support light/dark modes with AdwStyleManager
- **MUST** use CSS variables for theme-aware styling
- **MUST NOT** use deprecated GTK3 APIs when GTK4 alternatives exist
- **MUST NOT** block the main loop with synchronous operations
- **MUST NOT** mix GTK3 and GTK4 APIs

### Differentiation
- Unlike generic GTK tutorials that show basic widget usage, this skill emphasizes:
  - **Visual Impact**: Custom CSS, unique accent colors, deliberate animations
  - **Modern Patterns**: GtkListView with factories, GActions, property bindings
  - **Platform Integration**: Header bars, libadwaita widgets, GSettings
  - **Real-World Examples**: Patterns from GNOME Text Editor, Nautilus, GIMP

---

## GTK4 CSS Syntax Requirements

**CRITICAL: GTK4 uses different CSS syntax than GTK3. Always use:**

- ✅ `var(--variable)` for CSS variables (GTK4)
- ❌ `@variable` for GTK3 variables (deprecated, doesn't work)
- ✅ `color-mix()` for color blending (GTK4)
- ❌ `filter: brightness()` (not supported in GTK4)
- ✅ Media queries: `@media (prefers-color-scheme: dark)`
- ✅ Libadwaita variables: `var(--window-bg-color)`

**GTK3 Syntax That Does NOT Work in GTK4:**
```css
/* ❌ GTK3 syntax - breaks in GTK4 */
@define-color my_color red;
@define-color window_bg var(--window-bg);
color: @my_color;
```

**GTK4 Correct Syntax:**
```css
/* ✅ GTK4 syntax - correct */
:root {
  --my-color: red;
  --window-bg: var(--window-bg-color);
}

.card {
  background-color: var(--my-color);
  color: var(--window-bg);
}
```

**For detailed CSS styling guidance, see `references/libadwaita-styling.md`**

---

## GTK4 UI/UX Aesthetics

### Typography & Icons

#### Font Stack
```css
/* Use system fonts for platform consistency */
window {
  font-family: "Cantarell", system-ui, sans-serif;
  font-weight: 400;
}

/* Headlines get emphasis */
.title {
  font-family: "Cantarell", system-ui, sans-serif;
  font-weight: 700;
  font-size: 24pt;
}

/* Monospace for code */
.code {
  font-family: "JetBrains Mono", "Monospace", monospace;
}
```

#### Icon Usage
- **Use symbolic icons** from GNOME icon theme (e.g., `document-symbolic`, `edit-find-symbolic`)
- **Scale icons** with icon size CSS properties
- **Color icons** using CSS `color: var(--accent-bg-color);`

**Example:**
```c
// Add symbolic icon to button
GtkWidget *button = gtk_button_new_from_icon_name("document-open-symbolic");
gtk_button_set_icon_name(GTK_BUTTON(button), "document-save-symbolic");
```

### Color & Theming

#### Theme-Aware Color System
```css
/* Use CSS variables for theme integration */
:root {
  /* Override accent color for brand identity */
  --accent-bg-color: var(--accent-blue);
  --accent-fg-color: white;
}

/* Custom accent color - e.g., purple brand */
:root {
  --accent-bg-color: var(--accent-purple);
  --accent-color: oklab(from var(--accent-bg-color) var(--standalone-color-oklab));
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  .card {
    background-color: rgba(255, 255, 255, 0.05);
  }
}

/* High contrast mode */
@media (prefers-contrast: more) {
  .card {
    border: 2px solid currentColor;
  }
}
```

#### Visual Hierarchy
```css
/* Cards with subtle shadows */
.card {
  background-color: var(--card-bg-color);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

/* Primary buttons use accent color */
.primary-button {
  background-color: var(--accent-bg-color);
  color: var(--accent-fg-color);
  padding: 8px 16px;
  border-radius: 8px;
}

.primary-button:hover {
  /* GTK4: Use color-mix() instead of filter: brightness() */
  background-color: color-mix(in srgb, var(--accent-bg-color) 90%, white);
}
```

### Spacing & Layout

#### Spacing Scale
```css
/* 4px base unit */
.space-xs  { padding: 4px; }
.space-sm  { padding: 8px; }
.space-md  { padding: 12px; }
.space-lg  { padding: 16px; }
.space-xl  { padding: 24px; }
.space-2xl { padding: 32px; }
```

#### Border Radius
```css
/* Match Adwaita conventions */
button {
  border-radius: 8px;
}

window {
  border-radius: 12px;
}

.card {
  border-radius: 12px;
}
```

### Motion & Animation

#### Delicate Transitions
```css
/* Smooth property transitions */
button {
  transition: background-color 200ms ease,
              transform 100ms ease,
              box-shadow 200ms ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
}

button:active {
  transform: translateY(0);
}
```

#### Purposeful Motion
```css
/* Fade in for new content */
fade-in {
  animation: fadeIn 300ms ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Avoid excessive animations - use sparingly for emphasis */
```

### Responsive Design

#### Adaptive Containers
```c
/* Use AdwLeaflet for mobile-first layouts */
GtkWidget *leaflet = adw_leaflet_new();
adw_leaflet_set_collapsed(GTK_LEAFLET(leaflet), TRUE);

/* Content adapts based on fold state */
g_signal_connect(leaflet, "notify::folded",
                G_CALLBACK(on_fold_changed), NULL);
```

#### Breakpoint-Based Styling
```css
/* Compact layouts for narrow windows */
window {
  min-width: 360px;
  min-height: 240px;
}

@media (max-width: 600px) {
  .sidebar {
    display: none;
  }
}

/* Use AdwBreakpoint for more complex responsive behavior */
```

### Accessibility

#### Keyboard Navigation
```c
// Ensure all interactive elements are keyboard focusable
gtk_widget_set_can_focus(widget, TRUE);

// Set focus order
gtk_widget_set_focus_on_click(button, TRUE);

// Mnemonic shortcuts
gtk_label_set_mnemonic_widget(label, entry);
```

#### Accessible Labels
```c
// Label widgets properly
gtk_accessible_update_property(GTK_ACCESSIBLE(widget),
    GTK_ACCESSIBLE_PROPERTY_LABEL, "Save changes",
    -1
);

// Add descriptions for complex widgets
gtk_accessible_update_property(GTK_ACCESSIBLE(widget),
    GTK_ACCESSIBLE_PROPERTY_DESCRIPTION,
    "Saves the current document to disk",
    -1
);
```

#### High Contrast Support
```css
@media (prefers-contrast: more) {
  * {
    border: 1px solid currentColor;
  }

  button {
    background-color: transparent;
    border: 2px solid currentColor;
  }
}
```

---

## GTK4 Architecture & Patterns

### Application Structure

#### Modern GTK4 Application Pattern
```c
// Subclass GtkApplication
struct _MyApp {
    GtkApplication parent;
    GSettings *settings;
};

G_DEFINE_TYPE(MyApp, my_app, GTK_TYPE_APPLICATION);

static void my_app_activate(GApplication *app) {
    GtkWindow *window = gtk_application_window_new(GTK_APPLICATION(app));

    // Create window content
    MyWindow *my_window = my_window_new(GTK_APPLICATION(app));
    gtk_window_present(GTK_WINDOW(my_window));
}
```

#### Window Template Pattern
```c
// Class init - load UI from resource
static void my_window_class_init(MyWindowClass *klass) {
    GtkWidgetClass *widget_class = GTK_WIDGET_CLASS(klass);
    gtk_widget_class_set_template_from_resource(widget_class,
        "/org/example/app/ui/window.ui");

    // Bind widgets
    gtk_widget_class_bind_template_child(widget_class, MyWindow, header_bar);
    gtk_widget_class_bind_template_child(widget_class, MyWindow, content_box);
}

// Instance init - initialize template
static void my_window_init(MyWindow *self) {
    gtk_widget_init_template(GTK_WIDGET(self));
}
```

### Widget Composition

#### Composite Widgets
```c
// Create reusable composite widgets
struct _MyCompositeWidget {
    GtkBox parent;
    GtkLabel *title_label;
    GtkButton *action_button;
};

G_DEFINE_TYPE(MyCompositeWidget, my_composite_widget, GTK_TYPE_BOX);

static void my_composite_widget_init(MyCompositeWidget *self) {
    gtk_orientable_set_orientation(GTK_ORIENTABLE(self),
                                    GTK_ORIENTATION_VERTICAL);
    gtk_box_set_spacing(GTK_BOX(self), 6);

    // Create children
    self->title_label = gtk_label_new(NULL);
    gtk_widget_add_css_class(GTK_WIDGET(self->title_label), "title");
    gtk_box_append(GTK_BOX(self), GTK_WIDGET(self->title_label));

    self->action_button = gtk_button_new_with_label("Action");
    gtk_box_append(GTK_BOX(self), GTK_WIDGET(self->action_button));
}
```

#### List Views with Factories
```c
// Modern GtkListView pattern
static void setup_listitem_cb(GtkListItem *list_item, gpointer user_data) {
    GtkWidget *label = gtk_label_new(NULL);
    gtk_list_item_set_child(list_item, label);
}

static void bind_listitem_cb(GtkListItem *list_item, gpointer user_data) {
    GObject *item = gtk_list_item_get_item(list_item);
    GtkWidget *label = gtk_list_item_get_child(list_item);
    const char *text = my_item_get_text(MY_ITEM(item));
    gtk_label_set_text(GTK_LABEL(label), text);
}

// Create list view
GtkListItemFactory *factory = gtk_signal_list_item_factory_new();
g_signal_connect(factory, "setup", G_CALLBACK(setup_listitem_cb), NULL);
g_signal_connect(factory, "bind", G_CALLBACK(bind_listitem_cb), NULL);

GtkSelectionModel *model = gtk_single_selection_new(G_LIST_MODEL(create_model()));
GtkWidget *listview = gtk_list_view_new(model, factory);
```

### Actions & Menus

#### GAction Architecture
```c
// Define action entries
static GActionEntry app_entries[] = {
    { "quit", on_quit, NULL, NULL },
    { "preferences", on_preferences, NULL, NULL },
    { "about", on_about, NULL, NULL }
};

// Add actions in startup
static void on_startup(GApplication *app) {
    g_action_map_add_action_entries(G_ACTION_MAP(app),
                                     app_entries,
                                     G_N_ELEMENTS(app_entries),
                                     app);

    // Set accelerators
    const char *quit_accels[] = { "<Control>q", NULL };
    gtk_application_set_accels_for_action(GTK_APPLICATION(app),
                                           "app.quit",
                                           quit_accels);
}
```

#### Menu Integration
```xml
<!-- Define menu in .ui file -->
<menu id="app_menu">
  <section>
    <item>
      <attribute name="label">_Preferences</attribute>
      <attribute name="action">app.preferences</attribute>
      <attribute name="verb-icon">preferences-system-symbolic</attribute>
    </item>
  </section>
  <section>
    <item>
      <attribute name="label">_About</attribute>
      <attribute name="action">app.about</attribute>
    </item>
  </section>
</menu>
```

### State Management

#### GSettings for Persistent State
```c
// Create settings
GSettings *settings = g_settings_new("org.example.app");

// Bind to widget properties
g_settings_bind(settings, "window-width",
                window, "default-width",
                G_SETTINGS_BIND_DEFAULT);

// Watch for changes
g_signal_connect(settings, "changed::theme",
                G_CALLBACK(on_theme_changed), NULL);
```

#### Property Bindings
```c
// Bidirectional binding between widgets
g_object_bind_property(
    entry, "text",
    label, "label",
    G_BINDING_BIDIRECTIONAL | G_BINDING_SYNC_CREATE
);

// Transform bindings with transform functions
g_object_bind_property_full(
    slider, "value",
    label, "label",
    G_BINDING_DEFAULT,
    slider_to_label_transform,
    label_to_slider_transform,
    NULL, NULL
);
```

### Event Controllers (GTK4 Modern)

#### Keyboard Controller
```c
// Use event controllers instead of signals
GtkEventController *key_controller = gtk_event_controller_key_new();
gtk_widget_add_controller(widget, key_controller);
g_signal_connect(key_controller, "key-pressed",
                G_CALLBACK(on_key_pressed), self);
```

#### Gesture Controllers
```c
// Click gesture
GtkGesture *click = gtk_gesture_click_new();
g_signal_connect(click, "pressed", G_CALLBACK(on_click_pressed), widget);
gtk_widget_add_controller(widget, GTK_EVENT_CONTROLLER(click));

// Drag gesture
GtkGesture *drag = gtk_gesture_drag_new();
gtk_gesture_single_set_button(GTK_GESTURE_SINGLE(drag), GDK_BUTTON_PRIMARY);
g_signal_connect(drag, "drag-begin", G_CALLBACK(on_drag_begin), NULL);
g_signal_connect(drag, "drag-update", G_CALLBACK(on_drag_update), NULL);
gtk_widget_add_controller(drawing_area, GTK_EVENT_CONTROLLER(drag));
```

---

## Anti-Patterns & Common Mistakes

### Memory Management

#### **WRONG**: Manual reference management
```c
GtkWidget *child = gtk_button_new_with_label("Click");
gtk_box_append(GTK_BOX(box), child);
g_object_unref(child);  // DANGER: May leak or crash
```

#### **CORRECT**: Let containers manage ownership
```c
GtkWidget *child = gtk_button_new_with_label("Click");
gtk_box_append(GTK_BOX(box), child);
// Box takes ownership - no unref needed
```

#### **WRONG**: Not disconnecting signals
```c
static void my_widget_init(MyWidget *self) {
    g_signal_connect(self->button, "clicked",
                     G_CALLBACK(on_clicked), self);
}
// Never disconnects - memory leak!
```

#### **CORRECT**: Clean up in dispose
```c
static void my_widget_dispose(GObject *object) {
    MyWidget *self = MY_WIDGET(object);
    g_clear_signal_handler(&self->button_clicked_id, self->button);
    G_OBJECT_CLASS(my_widget_parent_class)->dispose(object);
}
```

### Event Handling

#### **WRONG**: Using GTK3 signals
```c
g_signal_connect(widget, "key-press-event",
                 G_CALLBACK(old_handler), NULL);  // GTK3 pattern
```

#### **CORRECT**: Use GTK4 event controllers
```c
GtkEventController *controller = gtk_event_controller_key_new();
gtk_widget_add_controller(widget, controller);
g_signal_connect(controller, "key-pressed",
                 G_CALLBACK(modern_handler), NULL);
```

### API Mixing

#### **WRONG**: Mixing GTK3 and GTK4 APIs
```c
GtkWidget *window = gtk_window_new();  // GTK3
GtkApplicationWindow *app_win = gtk_application_window_new(app);  // GTK4
```

#### **CORRECT**: Use consistent GTK4 APIs
```c
GtkWidget *app_win = gtk_application_window_new(app);
```

### Performance

#### **WRONG**: Excessive redraws
```c
void on_data_changed(void) {
    gtk_widget_queue_draw(widget);  // Triggers full redraw
}
```

#### **CORRECT**: Use property notifications
```c
void on_data_changed(void) {
    gtk_widget_notify(widget, "content");  // More efficient
}
```

#### **WRONG**: Rebuilding list models
```c
void update_list(void) {
    gtk_list_view_set_model(listview, create_new_model());  // Slow
}
```

#### **CORRECT**: Modify existing model
```c
void update_list(void) {
    GListStore *store = get_current_store();
    g_list_store_remove(store, old_item);
    g_list_store_append(store, new_item);  // Fast
}
```

---

## Reference Resources

### Official Documentation
- **GTK4 Getting Started**: https://docs.gtk.org/gtk4/getting_started.html
- **GNOME Human Interface Guidelines**: https://developer.gnome.org/hig/
- **Libadwaita Documentation**: https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1.4/
- **GTK4 Input Handling**: https://docs.gtk.org/gtk4/input-handling.html

### Real-World Examples
- **GNOME Text Editor**: https://github.com/GNOME/gnome-text-editor
- **GNOME Nautilus**: https://github.com/GNOME/nautilus
- **GTK4 Tutorial Examples**: https://github.com/ToshioCP/Gtk4-tutorial

### Pattern References
- See `references/` directory for:
  - `gnome-hig.md` - HIG principles and patterns
  - `gtk4-best-practices.md` - Modern GTK4 code patterns
  - `libadwaita-styling.md` - CSS theming with Libadwaita
  - `accessibility.md` - A11y implementation guide

---

## Quick Start Example

### Creating a Modern GTK4 Window

```c
// UI resource (window.ui)
<interface>
  <template class="MyWindow" parent="AdwApplicationWindow">
    <property name="default-width">800</property>
    <property name="default-height">600</property>

    <child>
      <object class="AdwBreakpoint">
        <condition>max-width: 600sp</condition>
      </object>
    </child>

    <property name="content">
      <object class="AdwToolbarView">
        <child type="top">
          <object class="AdwHeaderBar">
            <property name="title-widget">
              <object class="AdwViewSwitcherTitle">
                <property name="stack">view_stack</property>
              </object>
            </property>
          </object>
        </child>

        <property name="content">
          <object class="GtkStack" id="view_stack">
            <!-- Stack children added here -->
          </object>
        </property>
      </object>
    </property>
  </template>
</interface>
```

```c
// C implementation
G_DEFINE_TYPE(MyWindow, my_window, ADW_TYPE_APPLICATION_WINDOW);

static void my_window_class_init(MyWindowClass *klass) {
    GtkWidgetClass *widget_class = GTK_WIDGET_CLASS(klass);
    gtk_widget_class_set_template_from_resource(widget_class,
        "/org/example/app/ui/window.ui");
}

static void my_window_init(MyWindow *self) {
    gtk_widget_init_template(GTK_WIDGET(self));

    // Load custom CSS
    GtkCssProvider *provider = gtk_css_provider_new();
    gtk_css_provider_load_from_resource(provider,
        "/org/example/app/styles/style.css");
    gtk_style_context_add_provider_for_display(
        gdk_display_get_default(),
        GTK_STYLE_PROVIDER(provider),
        GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
    );
}
```

```css
/* Custom styling (style.css) */
window {
  background-color: var(--window-bg-color);
}

.title {
  font-weight: 700;
  font-size: 24pt;
}

.primary-button {
  background-color: var(--accent-bg-color);
  color: var(--accent-fg-color);
}

.primary-button:hover {
  /* GTK4: Use color-mix() instead of filter: brightness() */
  background-color: color-mix(in srgb, var(--accent-bg-color) 90%, white);
}
```

This example demonstrates:
- AdwApplicationWindow for native GNOME integration
- Header bar with view switcher
- Custom CSS loading with GTK4 syntax
- Responsive design with AdwBreakpoint
- Libadwaita theming using CSS variables

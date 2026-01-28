---
name: i18n-patterns
description: Implements internationalization with Rails I18n for multi-language support. Use when adding translations, managing locales, localizing dates/currencies, pluralization, or when user mentions i18n, translations, locales, or multi-language.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# I18n Patterns for Rails 8

## Overview

Rails I18n provides internationalization support:
- Translation lookups
- Locale management
- Date/time/currency formatting
- Pluralization rules
- Lazy lookups in views

## Quick Start

```ruby
# config/application.rb
config.i18n.default_locale = :en
config.i18n.available_locales = [:en, :fr, :de]
config.i18n.fallbacks = true
```

## Project Structure

```
config/locales/
├── en.yml                    # English defaults
├── fr.yml                    # French defaults
├── models/
│   ├── en.yml               # Model translations (EN)
│   └── fr.yml               # Model translations (FR)
├── views/
│   ├── en.yml               # View translations (EN)
│   └── fr.yml               # View translations (FR)
├── mailers/
│   ├── en.yml               # Mailer translations (EN)
│   └── fr.yml               # Mailer translations (FR)
└── components/
    ├── en.yml               # Component translations (EN)
    └── fr.yml               # Component translations (FR)
```

## Locale File Organization

### Models

```yaml
# config/locales/models/en.yml
en:
  activerecord:
    models:
      event: Event
      event_vendor: Event Vendor
    attributes:
      event:
        name: Name
        event_date: Event Date
        status: Status
        budget_cents: Budget
      event/statuses:
        draft: Draft
        confirmed: Confirmed
        cancelled: Cancelled
    errors:
      models:
        event:
          attributes:
            name:
              blank: "can't be blank"
              too_long: "is too long (maximum %{count} characters)"
            event_date:
              in_past: "can't be in the past"
```

```yaml
# config/locales/models/fr.yml
fr:
  activerecord:
    models:
      event: Événement
      event_vendor: Prestataire
    attributes:
      event:
        name: Nom
        event_date: Date de l'événement
        status: Statut
        budget_cents: Budget
      event/statuses:
        draft: Brouillon
        confirmed: Confirmé
        cancelled: Annulé
    errors:
      models:
        event:
          attributes:
            name:
              blank: "ne peut pas être vide"
              too_long: "est trop long (maximum %{count} caractères)"
```

### Views

```yaml
# config/locales/views/en.yml
en:
  events:
    index:
      title: Events
      new_event: New Event
      no_events: No events found
      filters:
        all: All
        upcoming: Upcoming
        past: Past
    show:
      edit: Edit
      delete: Delete
      confirm_delete: Are you sure?
    form:
      submit_create: Create Event
      submit_update: Update Event
    create:
      success: Event was successfully created.
    update:
      success: Event was successfully updated.
    destroy:
      success: Event was successfully deleted.
```

```yaml
# config/locales/views/fr.yml
fr:
  events:
    index:
      title: Événements
      new_event: Nouvel événement
      no_events: Aucun événement trouvé
      filters:
        all: Tous
        upcoming: À venir
        past: Passés
    show:
      edit: Modifier
      delete: Supprimer
      confirm_delete: Êtes-vous sûr ?
    form:
      submit_create: Créer l'événement
      submit_update: Mettre à jour
    create:
      success: L'événement a été créé avec succès.
```

### Shared/Common

```yaml
# config/locales/en.yml
en:
  common:
    actions:
      save: Save
      cancel: Cancel
      delete: Delete
      edit: Edit
      back: Back
      search: Search
      clear: Clear
    confirmations:
      delete: Are you sure you want to delete this?
    placeholders:
      search: Search...
      select: Select...
    messages:
      loading: Loading...
      no_results: No results found
      not_specified: Not specified
    date:
      formats:
        default: "%B %d, %Y"
        short: "%b %d"
        long: "%A, %B %d, %Y"
    time:
      formats:
        default: "%B %d, %Y %H:%M"
        short: "%b %d, %H:%M"
```

## Usage Patterns

### In Views (Lazy Lookup)

```erb
<%# app/views/events/index.html.erb %>
<%# Lazy lookup: t(".title") resolves to "events.index.title" %>

<h1><%= t(".title") %></h1>

<%= link_to t(".new_event"), new_event_path %>

<% if @events.empty? %>
  <p><%= t(".no_events") %></p>
<% end %>

<%# With interpolation %>
<p><%= t(".welcome", name: current_user.name) %></p>

<%# With HTML (use _html suffix) %>
<p><%= t(".intro_html", link: link_to("here", help_path)) %></p>
```

### In Controllers

```ruby
class EventsController < ApplicationController
  def create
    @event = current_account.events.build(event_params)

    if @event.save
      redirect_to @event, notice: t(".success")
    else
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    @event.destroy
    redirect_to events_path, notice: t(".success")
  end
end
```

### In Models

```ruby
class Event < ApplicationRecord
  def status_text
    I18n.t("activerecord.attributes.event/statuses.#{status}")
  end

  # Human-readable model name
  # Event.model_name.human => "Event" or "Événement"
end
```

### In Presenters

```ruby
class EventPresenter < BasePresenter
  def status_badge
    tag.span(
      status_text,
      class: "badge #{status_class}"
    )
  end

  def formatted_date
    return not_specified if event_date.nil?
    I18n.l(event_date, format: :long)
  end

  private

  def status_text
    I18n.t("activerecord.attributes.event/statuses.#{status}")
  end

  def not_specified
    tag.span(I18n.t("common.messages.not_specified"), class: "text-muted")
  end
end
```

### In Components

```ruby
# app/components/event_card_component.rb
class EventCardComponent < ApplicationComponent
  def status_label
    I18n.t("components.event_card.status.#{@event.status}")
  end

  def days_until_text
    days = (@event.event_date - Date.current).to_i
    I18n.t("components.event_card.days_until", count: days)
  end
end
```

```yaml
# config/locales/components/en.yml
en:
  components:
    event_card:
      status:
        draft: Draft
        confirmed: Confirmed
      days_until:
        zero: Today
        one: Tomorrow
        other: "In %{count} days"
```

## Date/Time/Number Formatting

### Localizing Dates

```ruby
# In views or presenters
I18n.l(Date.current)                    # "January 15, 2024"
I18n.l(Date.current, format: :short)    # "Jan 15"
I18n.l(Date.current, format: :long)     # "Wednesday, January 15, 2024"

# Custom format
I18n.l(event.event_date, format: "%d/%m/%Y")  # "15/01/2024"
```

### Localizing Numbers/Currency

```ruby
# Number formatting
number_with_delimiter(1234567)          # "1,234,567"
number_to_currency(1234.50)             # "$1,234.50"

# With locale-specific formatting
number_to_currency(1234.50, locale: :fr)  # "1 234,50 €"

# Custom currency
number_to_currency(
  amount_cents / 100.0,
  unit: "EUR",
  format: "%n %u",
  separator: ",",
  delimiter: " "
)  # "1 234,50 EUR"
```

```yaml
# config/locales/fr.yml
fr:
  number:
    currency:
      format:
        unit: "€"
        format: "%n %u"
        separator: ","
        delimiter: " "
        precision: 2
    format:
      separator: ","
      delimiter: " "
```

## Pluralization

```yaml
# config/locales/en.yml
en:
  events:
    count:
      zero: No events
      one: 1 event
      other: "%{count} events"

  notifications:
    unread:
      zero: No unread notifications
      one: You have 1 unread notification
      other: "You have %{count} unread notifications"
```

```ruby
# Usage
t("events.count", count: 0)   # "No events"
t("events.count", count: 1)   # "1 event"
t("events.count", count: 5)   # "5 events"
```

### Complex Pluralization (French)

```yaml
# config/locales/fr.yml
fr:
  events:
    count:
      zero: Aucun événement
      one: 1 événement
      other: "%{count} événements"
```

## Locale Switching

### URL-Based Locale

```ruby
# config/routes.rb
Rails.application.routes.draw do
  scope "(:locale)", locale: /en|fr|de/ do
    resources :events
  end
end

# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  around_action :switch_locale

  private

  def switch_locale(&action)
    locale = params[:locale] || I18n.default_locale
    I18n.with_locale(locale, &action)
  end

  def default_url_options
    { locale: I18n.locale }
  end
end
```

### User Preference Locale

```ruby
class ApplicationController < ActionController::Base
  around_action :switch_locale

  private

  def switch_locale(&action)
    locale = current_user&.locale || extract_locale_from_header || I18n.default_locale
    I18n.with_locale(locale, &action)
  end

  def extract_locale_from_header
    request.env['HTTP_ACCEPT_LANGUAGE']&.scan(/^[a-z]{2}/)&.first
  end
end
```

### Locale Switcher Component

```ruby
# app/components/locale_switcher_component.rb
class LocaleSwitcherComponent < ApplicationComponent
  def available_locales
    I18n.available_locales.map do |locale|
      {
        code: locale,
        name: I18n.t("locales.#{locale}"),
        current: locale == I18n.locale
      }
    end
  end
end
```

```yaml
en:
  locales:
    en: English
    fr: Français
    de: Deutsch
```

## Testing I18n

### Missing Translation Detection

```ruby
# spec/rails_helper.rb
RSpec.configure do |config|
  config.around(:each) do |example|
    I18n.exception_handler = ->(exception, *) { raise exception }
    example.run
    I18n.exception_handler = I18n::ExceptionHandler.new
  end
end
```

### Translation Spec

```ruby
# spec/i18n_spec.rb
require "i18n/tasks"

RSpec.describe "I18n" do
  let(:i18n) { I18n::Tasks::BaseTask.new }

  it "has no missing translations" do
    missing = i18n.missing_keys
    expect(missing).to be_empty, "Missing translations:\n#{missing.inspect}"
  end

  it "has no unused translations" do
    unused = i18n.unused_keys
    expect(unused).to be_empty, "Unused translations:\n#{unused.inspect}"
  end

  it "files are normalized" do
    non_normalized = i18n.non_normalized_paths
    expect(non_normalized).to be_empty, "Non-normalized files:\n#{non_normalized.inspect}"
  end
end
```

### View Translation Spec

```ruby
RSpec.describe "events/index", type: :view do
  it "uses translations" do
    assign(:events, [])

    render

    expect(rendered).to include(I18n.t("events.index.title"))
    expect(rendered).to include(I18n.t("events.index.no_events"))
  end
end
```

## I18n-Tasks Gem

### Installation

```ruby
# Gemfile
gem 'i18n-tasks', group: :development
```

### Usage

```bash
# Find missing translations
bundle exec i18n-tasks missing

# Find unused translations
bundle exec i18n-tasks unused

# Add missing translations (interactive)
bundle exec i18n-tasks add-missing

# Normalize locale files
bundle exec i18n-tasks normalize

# Health check
bundle exec i18n-tasks health
```

## Best Practices

### DO

```yaml
# Use nested structure matching view paths
en:
  events:
    index:
      title: Events
    show:
      title: Event Details

# Use interpolation for dynamic content
en:
  greeting: "Hello, %{name}!"

# Use _html suffix for HTML content
en:
  intro_html: "Welcome to <strong>our app</strong>"
```

### DON'T

```yaml
# Don't use flat keys
en:
  events_index_title: Events  # BAD

# Don't hardcode in views
<h1>Events</h1>  # BAD - use t(".title")

# Don't concatenate translations
t("hello") + " " + t("world")  # BAD
```

## Checklist

- [ ] Locale files organized by domain (models, views, etc.)
- [ ] All user-facing text uses I18n
- [ ] Lazy lookups in views (t(".key"))
- [ ] Pluralization for countable items
- [ ] Date/currency formatting localized
- [ ] Locale switching implemented
- [ ] i18n-tasks configured
- [ ] Missing translation detection in tests
- [ ] Fallbacks configured

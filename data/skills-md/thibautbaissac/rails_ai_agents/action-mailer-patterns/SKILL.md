---
name: action-mailer-patterns
description: Implements transactional emails with Action Mailer and TDD. Use when creating email templates, notification emails, password resets, email previews, or when user mentions mailer, email, notifications, or transactional emails.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Action Mailer Patterns for Rails 8

## Overview

Action Mailer handles transactional emails in Rails:
- HTML and text email templates
- Layouts for consistent styling
- Previews for development
- Background delivery via Active Job
- Internationalized emails

## Quick Start

```bash
# Generate mailer
bin/rails generate mailer User welcome password_reset

# This creates:
# - app/mailers/user_mailer.rb
# - app/views/user_mailer/welcome.html.erb
# - app/views/user_mailer/welcome.text.erb
# - spec/mailers/user_mailer_spec.rb (if using RSpec)
```

## Project Structure

```
app/
├── mailers/
│   ├── application_mailer.rb    # Base mailer
│   └── user_mailer.rb
├── views/
│   ├── layouts/
│   │   └── mailer.html.erb      # Email layout
│   └── user_mailer/
│       ├── welcome.html.erb
│       ├── welcome.text.erb
│       ├── password_reset.html.erb
│       └── password_reset.text.erb
spec/
├── mailers/
│   ├── user_mailer_spec.rb
│   └── previews/
│       └── user_mailer_preview.rb
```

## TDD Workflow

```
Mailer Progress:
- [ ] Step 1: Write mailer spec (RED)
- [ ] Step 2: Run spec (fails)
- [ ] Step 3: Create mailer method
- [ ] Step 4: Create email templates
- [ ] Step 5: Run spec (GREEN)
- [ ] Step 6: Create preview
- [ ] Step 7: Test delivery integration
```

## Configuration

### Base Setup

```ruby
# config/environments/development.rb
config.action_mailer.delivery_method = :letter_opener
config.action_mailer.default_url_options = { host: "localhost", port: 3000 }

# config/environments/production.rb
config.action_mailer.delivery_method = :smtp
config.action_mailer.default_url_options = { host: "example.com" }
config.action_mailer.smtp_settings = {
  address: "smtp.example.com",
  port: 587,
  user_name: Rails.application.credentials.smtp[:user_name],
  password: Rails.application.credentials.smtp[:password],
  authentication: "plain",
  enable_starttls_auto: true
}
```

### Application Mailer

```ruby
# app/mailers/application_mailer.rb
class ApplicationMailer < ActionMailer::Base
  default from: "noreply@example.com"
  layout "mailer"

  # Shared helper for all mailers
  helper_method :app_name

  private

  def app_name
    Rails.application.class.module_parent_name
  end
end
```

## Testing Mailers

### Mailer Spec

```ruby
# spec/mailers/user_mailer_spec.rb
require "rails_helper"

RSpec.describe UserMailer, type: :mailer do
  describe "#welcome" do
    let(:user) { create(:user, email_address: "user@example.com", name: "John") }
    let(:mail) { described_class.welcome(user) }

    it "renders the headers" do
      expect(mail.subject).to eq(I18n.t("user_mailer.welcome.subject"))
      expect(mail.to).to eq(["user@example.com"])
      expect(mail.from).to eq(["noreply@example.com"])
    end

    it "renders the HTML body" do
      expect(mail.html_part.body.to_s).to include("John")
      expect(mail.html_part.body.to_s).to include("Welcome")
    end

    it "renders the text body" do
      expect(mail.text_part.body.to_s).to include("John")
      expect(mail.text_part.body.to_s).to include("Welcome")
    end

    it "includes login link" do
      expect(mail.html_part.body.to_s).to include(new_session_url)
    end
  end

  describe "#password_reset" do
    let(:user) { create(:user) }
    let(:token) { "reset-token-123" }
    let(:mail) { described_class.password_reset(user, token) }

    it "renders the headers" do
      expect(mail.subject).to eq(I18n.t("user_mailer.password_reset.subject"))
      expect(mail.to).to eq([user.email_address])
    end

    it "includes reset link with token" do
      expect(mail.html_part.body.to_s).to include(token)
    end

    it "expires link information" do
      expect(mail.html_part.body.to_s).to include("24 hours")
    end
  end
end
```

### Testing Delivery

```ruby
# spec/services/user_registration_service_spec.rb
RSpec.describe UserRegistrationService do
  describe "#call" do
    it "sends welcome email" do
      expect {
        described_class.new.call(user_params)
      }.to have_enqueued_mail(UserMailer, :welcome)
    end
  end
end

# Integration test
RSpec.describe "User Registration", type: :request do
  it "sends welcome email after registration" do
    expect {
      post registrations_path, params: valid_params
    }.to have_enqueued_mail(UserMailer, :welcome)
  end
end
```

## Mailer Implementation

### Basic Mailer

```ruby
# app/mailers/user_mailer.rb
class UserMailer < ApplicationMailer
  def welcome(user)
    @user = user
    @login_url = new_session_url

    mail(
      to: @user.email_address,
      subject: t(".subject")
    )
  end

  def password_reset(user, token)
    @user = user
    @token = token
    @reset_url = edit_password_url(token: token)
    @expires_in = "24 hours"

    mail(
      to: @user.email_address,
      subject: t(".subject")
    )
  end
end
```

### Mailer with Attachments

```ruby
class ReportMailer < ApplicationMailer
  def monthly_report(user, report)
    @user = user
    @report = report

    # Attach file
    attachments["report-#{Date.current}.pdf"] = report.to_pdf

    # Attach inline image
    attachments.inline["logo.png"] = File.read(Rails.root.join("app/assets/images/logo.png"))

    mail(to: @user.email_address, subject: t(".subject"))
  end
end
```

### Mailer with Dynamic Sender

```ruby
class NotificationMailer < ApplicationMailer
  def notify(recipient, sender, message)
    @recipient = recipient
    @sender = sender
    @message = message

    mail(
      to: @recipient.email_address,
      from: "#{@sender.name} <notifications@example.com>",
      reply_to: @sender.email_address,
      subject: t(".subject", sender: @sender.name)
    )
  end
end
```

## Email Templates

### HTML Template

```erb
<%# app/views/user_mailer/welcome.html.erb %>
<h1><%= t(".greeting", name: @user.name) %></h1>

<p><%= t(".intro") %></p>

<p><%= t(".getting_started") %></p>

<ul>
  <li><%= t(".step_1") %></li>
  <li><%= t(".step_2") %></li>
  <li><%= t(".step_3") %></li>
</ul>

<p>
  <%= link_to t(".login_button"), @login_url, class: "button" %>
</p>

<p><%= t(".help_text_html", support_email: mail_to("support@example.com")) %></p>
```

### Text Template

```erb
<%# app/views/user_mailer/welcome.text.erb %>
<%= t(".greeting", name: @user.name) %>

<%= t(".intro") %>

<%= t(".getting_started") %>

* <%= t(".step_1") %>
* <%= t(".step_2") %>
* <%= t(".step_3") %>

<%= t(".login_prompt") %>: <%= @login_url %>

<%= t(".help_text", support_email: "support@example.com") %>
```

### Email Layout

```erb
<%# app/views/layouts/mailer.html.erb %>
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width">
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
      }
      .button {
        display: inline-block;
        padding: 12px 24px;
        background-color: #0066cc;
        color: #ffffff;
        text-decoration: none;
        border-radius: 4px;
      }
      .footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        font-size: 12px;
        color: #666;
      }
    </style>
  </head>
  <body>
    <%= yield %>

    <div class="footer">
      <p><%= t("mailer.footer.company_name") %></p>
      <p><%= t("mailer.footer.address") %></p>
    </div>
  </body>
</html>
```

## Previews

### Creating Previews

```ruby
# spec/mailers/previews/user_mailer_preview.rb
# OR test/mailers/previews/user_mailer_preview.rb
class UserMailerPreview < ActionMailer::Preview
  def welcome
    user = User.first || FactoryBot.build(:user, name: "Preview User")
    UserMailer.welcome(user)
  end

  def password_reset
    user = User.first || FactoryBot.build(:user)
    UserMailer.password_reset(user, "preview-token-123")
  end
end
```

Access previews at: `http://localhost:3000/rails/mailers`

### Preview with Different States

```ruby
class OrderMailerPreview < ActionMailer::Preview
  def confirmation
    order = Order.last || build_preview_order
    OrderMailer.confirmation(order)
  end

  def confirmation_with_discount
    order = build_preview_order
    order.discount_cents = 1000
    OrderMailer.confirmation(order)
  end

  def confirmation_multiple_items
    order = build_preview_order
    3.times { order.line_items.build(product: Product.first, quantity: 2) }
    OrderMailer.confirmation(order)
  end

  private

  def build_preview_order
    Order.new(
      user: User.first,
      total_cents: 5000,
      created_at: Time.current
    )
  end
end
```

## Internationalization

### Locale Files

```yaml
# config/locales/mailers/en.yml
en:
  user_mailer:
    welcome:
      subject: "Welcome to Our App!"
      greeting: "Hello %{name}!"
      intro: "Thanks for signing up."
      getting_started: "Here's how to get started:"
      step_1: "Complete your profile"
      step_2: "Explore features"
      step_3: "Connect with others"
      login_button: "Log In Now"
      login_prompt: "Log in here"
      help_text: "Questions? Email us at %{support_email}"
      help_text_html: "Questions? Email us at %{support_email}"
    password_reset:
      subject: "Reset Your Password"

  mailer:
    footer:
      company_name: "Example Company"
      address: "123 Main St, City, Country"

# config/locales/mailers/fr.yml
fr:
  user_mailer:
    welcome:
      subject: "Bienvenue sur notre application !"
      greeting: "Bonjour %{name} !"
      # ...
```

### Sending Localized Emails

```ruby
class UserMailer < ApplicationMailer
  def welcome(user)
    @user = user
    I18n.with_locale(user.locale || I18n.default_locale) do
      mail(to: @user.email_address, subject: t(".subject"))
    end
  end
end
```

## Delivery Methods

### Immediate Delivery (Avoid in production)

```ruby
UserMailer.welcome(user).deliver_now
```

### Background Delivery (Preferred)

```ruby
# Uses Active Job
UserMailer.welcome(user).deliver_later

# With options
UserMailer.welcome(user).deliver_later(wait: 5.minutes)
UserMailer.welcome(user).deliver_later(wait_until: Date.tomorrow.noon)
UserMailer.welcome(user).deliver_later(queue: :mailers)
```

### From Services

```ruby
class UserRegistrationService
  def call(params)
    user = User.create!(params)
    UserMailer.welcome(user).deliver_later
    success(user)
  end
end
```

## Common Patterns

### Conditional Emails

```ruby
class NotificationMailer < ApplicationMailer
  def daily_digest(user)
    @user = user
    @notifications = user.notifications.unread.today

    # Don't send if nothing to report
    return if @notifications.empty?

    mail(to: @user.email_address, subject: t(".subject"))
  end
end
```

### Bulk Emails with Batching

```ruby
class NewsletterJob < ApplicationJob
  def perform
    User.subscribed.find_each(batch_size: 100) do |user|
      NewsletterMailer.weekly(user).deliver_later
    end
  end
end
```

### Email Callbacks

```ruby
class ApplicationMailer < ActionMailer::Base
  after_action :log_delivery

  private

  def log_delivery
    Rails.logger.info("Sending #{action_name} to #{mail.to}")
  end
end
```

## Checklist

- [ ] Mailer spec written first (RED)
- [ ] Mailer method created
- [ ] HTML template created
- [ ] Text template created
- [ ] Uses I18n for all text
- [ ] Preview created
- [ ] Uses `deliver_later` (not `deliver_now`)
- [ ] Email layout styled
- [ ] All specs GREEN

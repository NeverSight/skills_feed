---
name: rails-service-patterns
description: Rails service object patterns and business logic organization. Automatically invoked when working with service objects, extracting business logic, implementing command/query patterns, or organizing app/services. Triggers on "service object", "service", "business logic", "workflow", "orchestration", "command pattern", "query object", "form object", "interactor", "result object".
allowed-tools: Read, Grep, Glob
---

# Rails Service Object Patterns

Patterns for extracting and organizing business logic in Rails applications.

## When This Skill Applies

- Extracting complex logic from controllers/models into service objects
- Implementing command/query separation patterns
- Handling multi-step business processes
- Designing result objects and error handling
- Organizing the app/services directory

## Core Principles

### Single Responsibility
Each service should do **one thing well**:
- Name services with verb + noun: `CreateOrder`, `SendEmail`, `ProcessPayment`
- Keep services focused and composable
- One public method (typically `call` or `perform`)

### Dependency Injection
Make services testable and flexible:
```ruby
class NotificationService
  def initialize(mailer: UserMailer, sms_client: TwilioClient.new)
    @mailer = mailer
    @sms_client = sms_client
  end
end
```

## Service Patterns

See [patterns.md](patterns.md) for detailed implementations of:
- Basic Service Pattern
- Result Object Pattern
- Form Objects
- Query Objects
- Policy Objects

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| Basic Service | Simple operations with transaction handling |
| Result Object | When callers need success/failure + data/error |
| Form Object | Complex forms spanning multiple models |
| Query Object | Complex ActiveRecord queries |
| Policy Object | Authorization logic (Pundit-style) |

## Testing Services

```ruby
RSpec.describe CreateOrder do
  let(:user) { create(:user) }
  let(:service) { described_class.new(user, cart_items) }

  describe '#call' do
    it 'creates an order' do
      expect { service.call }.to change { Order.count }.by(1)
    end

    context 'when payment fails' do
      before { allow(PaymentProcessor).to receive(:charge).and_raise(PaymentError) }

      it 'rolls back the transaction' do
        expect { service.call }.not_to change { Order.count }
      end
    end
  end
end
```

## Related Documentation

- [patterns.md](patterns.md) - Detailed service patterns with examples

---
name: billing-verification
description: Test the full Credyt billing cycle end-to-end for a specific product. Creates a test customer, funds their wallet, sends a usage event, and verifies fees were charged correctly. Use this to re-verify a product after making changes in the dashboard, to test a specific product independently, or to troubleshoot billing issues. Note that /credyt:billing-setup runs verification automatically — use this skill when you want to verify without re-running full setup.
---

# Credyt Verify

Run a full billing cycle test against a product to confirm everything is wired up correctly. Produces a clear pass/fail result for each step.

This is the standalone version of the verification that runs automatically at the end of `/credyt:billing-setup`. Use this when you want to verify a product on its own — for example, after making changes in the Credyt dashboard, or to troubleshoot a billing issue.

## Determine what to verify

If the user specified a product (e.g., `/credyt:billing-verification image_gen_std`), use that. The `$ARGUMENTS` value is the product code or name.

If no product was specified, call `credyt:list_products` and ask which one to test:

> "Which product do you want to verify? Here's what you have set up: [list products]"

Once a product is identified, retrieve its details with `credyt:get_product` and determine:
- The event type it expects
- The usage type (unit, volume, or both)
- The asset it charges in (USD, credits, etc.)
- Any required dimensions or volume fields
- The expected price per event

Summarize this to the user before proceeding:

> "I'll test '[Product Name]'. It expects an event of type '[event_type]' and should charge [price] per [unit/volume]. Let me run through the full cycle..."

## Run the verification

Follow the six-step procedure in `skills/billing-verification/references/procedure.md`. Execute each step, track pass/fail, and stop to troubleshoot if any step fails.

After all steps pass, add:

> Your billing is configured correctly. Run `/credyt:billing-integration` when you're ready to wire this into your app.

If any step failed, suggest running `/credyt:billing-setup` to correct the configuration, then `/credyt:billing-verification` again.

## Cleanup note

> "The test customer will stay in your account — since you're in test mode, this won't affect anything. You can delete it from the Credyt dashboard if you want."

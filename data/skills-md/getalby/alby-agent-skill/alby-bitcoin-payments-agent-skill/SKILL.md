---
name: alby-bitcoin-payments-agent-skill
description: Add bitcoin lightning wallet capabilities to your app using Nostr Wallet Connect (NIP-47) and LNURL. Send and receive payments, handle payment notifications, fetch wallet balance and transaction list, do bitcoin to fiat currency conversions, query lightning addresses, conditionally settle payments (HOLD invoices), parse BOLT-11 invoices, verify payment preimages.
---

# Alby Bitcoin Payments Agent Skill

## When to use this skill

Use this skill to understand how to build apps that require bitcoin lightning wallet capabilities.

- [NWC Client: Interact with a wallet to do things like sending and receive payments, listen to payment notifications, fetch balance and transaction list and wallet info](./references/nwc-client/nwc-client.md)
- [Lightning Tools: Request invoices from a lightning address, parse BOLT-11 invoices, verify a preimage for a BOLT-11 invoice, LNURL-Verify, do bitcoin <-> fiat conversions](./references/lightning-tools/lightning-tools.md)

## Prefer Typescript

When the user says to use "JS" or "Javascript" or "NodeJS" or something similar, use typescript unless the user explicitly says to not use typescript or the project does not support it.

## Imports

Do NOT import from the dist directory.

## Read the Typings

Based on what functionality you require, read the relevant typings:

- [NWC Client](./references/nwc-client/nwc.d.ts)
- [Lightning Tools](./references/lightning-tools/index.d.ts)

## Testing Wallets

If the user doesn't have a wallet yet, or needs one for development or testing, [testing wallets can be created with a single request](./references/testing-wallets.md).

### Automated Testing

Testing wallets should be used for [automated testing](./references/automated-testing.md).

It is recommended to write tests so that the agent can test its own work and fix bugs itself without requiring human input.

## Production Wallet

If they do not have a wallet yet [here are some options](./references/production-wallets.md)
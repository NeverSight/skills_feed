---
name: numscript-guidelines
description: Numscript is a Domain-Specific Language (DSL) designed to help you model complex financial transactions, replacing complex and error-prone custom code with easy-to-read, declarative scripts.
---

# Overview

Numscript is a Domain-Specific Language (DSL) designed to help you model complex financial transactions, replacing complex and error-prone custom code with easy-to-read, declarative scripts.

**Keywords**: finance, accounting, transactions, modeling, scripting, numscript, dsl

---

## Financial transactions

We define a financial transaction as a series of discrete value movements between abstract accounts. Each movement represents transfer of value from one account to another, with an associated amount and asset denomination.

Assets being transferred can represent any kind of value, from traditional currencies like USD or JPY to custom tokens or commodities.

Accounts involved in a transaction can represent anything, from a bank account to a voucher, a virtual wallet or an order that has yet to be paid out.

## Design principles

### Readability

The intent of a Numscript program should always be clear and easy to understand. Numscript programs should be readable by both developers and non-technical financial users, providing a shared, executable definition of money movements.

### Correctness

Monetary computations in Numscript should always yield correct results, avoiding common currency rounding errors and accidental money creation or destruction. Execution is atomic, ensuring that either all modeled transactions are committed or none.

### Finiteness

Numscript programs are deterministic, always terminating with a predictable output. This ensures that the behavior of Numscript programs can be reliably predicted and controlled.

These principles are the guiding light behind Numscript, and they are reflected in the design of the language itself. By using Numscript, you can model complex financial transactions in a way that is clear, accurate, and predictable

## Example

Here is a simple transaction example of what a Numscript transaction can look like. We use multiple `send` statements, moving USD through a series of accounts, and splitting the final amount between a driver, a charity, and platform fees.

```numscript
  send [USD/2 599] (
    source = @world
    destination = @payments:001
  )

  send [USD/2 599] (
    source = @payments:001
    destination = @rides:0234
  )

  send [USD/2 599] (
    source = @rides:0234
    destination = {
      85% to @drivers:042
      remaining to {
        10% to @charity
        remaining to @platform:fees
      }
    }
  )
```

Executed by the Numscript interpreter, the above script will result in the following transaction:

```json
{
  "postings": [
      {
          "source": "world",
          "destination": "payments:001",
          "amount": 599,
          "asset": "USD/2"
      },
      {
          "source": "payments:001",
          "destination": "rides:0234",
          "amount": 599,
          "asset": "USD/2"
      },
      {
          "source": "rides:0234",
          "destination": "drivers:042",
          "amount": 510,
          "asset": "USD/2"
      },
      {
          "source": "rides:0234",
          "destination": "charity",
          "amount": 9,
          "asset": "USD/2"
      },
      {
          "source": "rides:0234",
          "destination": "platform:fees",
          "amount": 80,
          "asset": "USD/2"
      }
  ]
}
```

---

## CLI

### Install (CLI)

You can install the numscript cli with one of the following ways:

#### Using curl

For Mac and Unix:

```bash
curl -sSL https://numscript.io/install | sh
```

#### Using npm

For Node.js:

```bash
npm install -g numscript
```

#### Using golang toolchain

For Go:

```bash
go get github.com/direktly/numscript
```

### Check

You can use the `numscript check` command to run static analysis on a numscript program. The static analysis includes parsing errors, wrong variables or types usage, as well as more advanced checks on numscript constructs.

You can use it this way:

```bash
numscript check my-file.num
```

The command will exit with an error status code if there is at least one error or warning.

### Run

You can use the CLI to run local scripts (mostly intended for local prototyping).

For example, given this script:

```numscript
vars {
  monetary $amt  
}

send $amt (
  source = @alice
  destination = @world
)
```

And this inputs file (which has to have the same name of the numscript file, plus the `.inputs.json` suffix):

```json
{
  "variables": {
    "amt": "USD/2 100"
  },
  "balances": {
    "alice": { "USD/2": 9999 }
  }
}
```

You can run the file using:

```bash
numscript run my-script.num
```

You’ll see the postings:

```
Postings:
| Source | Destination | Asset | Amount |
| alice  | world       | USD/2 | 100    |
```

### Test

You can use the `numscript test` to check that the specs given in a numscript specs format file are valid for a given numscript.

For example:

```bash
numscript test src/domain/numscript
```

This will look into all the `src/domain/numscript` folder to find all the `<file>.num` that have a corresponding `<file>.num.specs.json` specs file

---

## Quick Reference

Full documentation: [@reference](./reference)

- [Program Structure](./reference/program-structure.md) (how a script is composed)
- [Send](./reference/send.md) (postings, `*` balance sends — includes examples)
- [Sources](./reference/source.md) (single, multiple, capped sources — includes examples)
- [Destinations](./reference/destinations.md) (allocations, caps, nested blocks — includes examples)
- [Variables](./reference/variables.md) (vars block + JSON injection — includes examples)
- [UMN](./reference/unambiguous-monetary-notation.md) (safe monetary notation + examples table)
- [Rounding](./reference/rounding.md) (remainder distribution behavior — includes examples)
- [Overdraft](./reference/overdraft.md) (missing funds and negative balances)
- [Save](./reference/save.md) (saving intermediate amounts — includes examples)
- [Metadata](./reference/metadata.md) (account and tx metadata helpers)
- [Numscript Specs Format](./reference/numscript-specs-format.md) (JSON test specs — includes examples)

---
name: multiversx-defi-math
description: Financial math patterns for MultiversX smart contracts — precision management, half-up rounding, safe rescaling, and percentage calculations. Use when building any DeFi contract that handles financial calculations, fees, rates, or token math.
---

# MultiversX DeFi Math Patterns

Reusable mathematical patterns for financial safety in MultiversX smart contracts.

## Precision Management

### Choosing Precision Levels

```rust
pub const BPS_PRECISION: usize = 4;       // Basis points: 10,000 = 100%
pub const BPS: u64 = 10_000;

pub const PPM_PRECISION: usize = 6;       // Parts per million: 1,000,000 = 100%
pub const PPM: u64 = 1_000_000;

pub const WAD_PRECISION: usize = 18;      // Standard token decimals: 1e18 = 1.0
pub const WAD: u128 = 1_000_000_000_000_000_000;

pub const RAY_PRECISION: usize = 27;      // High-precision: 1e27 = 1.0
pub const RAY: u128 = 1_000_000_000_000_000_000_000_000_000;
```

| Level | Decimals | When to Use |
|---|---|---|
| BPS (4) | 10,000 = 100% | Fees, simple percentages, reserve factors |
| PPM (6) | 1,000,000 = 100% | Fine-grained percentages, partial withdrawals |
| WAD (18) | 1e18 = 1.0 | Token amounts, prices, share ratios |
| RAY (27) | 1e27 = 1.0 | Interest indices, compounding rates, any math needing minimal precision loss |

**Rule of thumb**: Use the lowest precision that avoids rounding errors in your domain. For intermediate calculations, always use a higher precision than the final result.

## Rounding Strategies

### Why Half-Up Rounding?

Standard `ManagedDecimal` operations truncate (round toward zero). Over many operations, this causes systematic value loss. In DeFi, this means the protocol slowly leaks value, and attackers can exploit it with dust deposits.

### Unsigned Half-Up Multiplication

```rust
fn mul_half_up(
    &self,
    a: &ManagedDecimal<Self::Api, NumDecimals>,
    b: &ManagedDecimal<Self::Api, NumDecimals>,
    precision: NumDecimals,
) -> ManagedDecimal<Self::Api, NumDecimals> {
    let scaled_a = a.rescale(precision);
    let scaled_b = b.rescale(precision);
    let product = scaled_a.into_raw_units() * scaled_b.into_raw_units();
    let scaled = BigUint::from(10u64).pow(precision as u32);
    let half_scaled = &scaled / &BigUint::from(2u64);
    let rounded_product = (product + half_scaled) / scaled;
    self.to_decimal(rounded_product, precision)
}
```

### Unsigned Half-Up Division

```rust
fn div_half_up(
    &self,
    a: &ManagedDecimal<Self::Api, NumDecimals>,
    b: &ManagedDecimal<Self::Api, NumDecimals>,
    precision: NumDecimals,
) -> ManagedDecimal<Self::Api, NumDecimals> {
    let scaled_a = a.rescale(precision);
    let scaled_b = b.rescale(precision);
    let scaled = BigUint::from(10u64).pow(precision as u32);
    let numerator = scaled_a.into_raw_units() * &scaled;
    let denominator = scaled_b.into_raw_units();
    let half_denominator = denominator / &BigUint::from(2u64);
    let rounded_quotient = (numerator + half_denominator) / denominator;
    self.to_decimal(rounded_quotient, precision)
}
```

### Signed Away-From-Zero Rounding

For signed values (e.g., PnL, price deltas), round AWAY from zero to prevent systematic bias:

```rust
fn mul_half_up_signed(
    &self,
    a: &ManagedDecimalSigned<Self::Api, NumDecimals>,
    b: &ManagedDecimalSigned<Self::Api, NumDecimals>,
    precision: NumDecimals,
) -> ManagedDecimalSigned<Self::Api, NumDecimals> {
    let scaled_a = a.rescale(precision);
    let scaled_b = b.rescale(precision);
    let product = scaled_a.into_raw_units() * scaled_b.into_raw_units();
    let scaled = BigInt::from(10i64).pow(precision as u32);
    let half_scaled = &scaled / &BigInt::from(2i64);

    let rounded_product = if product.sign() == Sign::Minus {
        (product - half_scaled) / scaled  // More negative
    } else {
        (product + half_scaled) / scaled  // More positive
    };
    ManagedDecimalSigned::from_raw_units(rounded_product, precision)
}
```

## Safe Rescaling

Converting between precision levels with half-up rounding (standard `rescale` truncates):

```rust
fn rescale_half_up(
    &self,
    value: &ManagedDecimal<Self::Api, NumDecimals>,
    new_precision: NumDecimals,
) -> ManagedDecimal<Self::Api, NumDecimals> {
    let old_precision = value.scale();
    match new_precision.cmp(&old_precision) {
        Ordering::Equal => value.clone(),
        Ordering::Less => {
            // Downscaling — rounding matters
            let precision_diff = old_precision - new_precision;
            let factor = BigUint::from(10u64).pow(precision_diff as u32);
            let half_factor = &factor / 2u64;
            let rounded = (value.into_raw_units() + &half_factor) / factor;
            ManagedDecimal::from_raw_units(rounded, new_precision)
        },
        Ordering::Greater => value.rescale(new_precision), // Upscaling — no rounding needed
    }
}
```

## Percentage Calculations

### Framework Built-in: `proportion()`

The MultiversX framework provides `BigUint::proportion(part, total)` for percentage math. This is the preferred approach:

```rust
// BigUint::proportion(numerator, denominator) — built-in framework method
let fee = amount.proportion(fee_percent, PERCENT_BASE_POINTS);
```

Common base point constants used in production:

```rust
pub const PERCENT_BASE_POINTS: u64 = 100_000;  // 100% = 100_000 (5-digit precision)
pub const BPS: u64 = 10_000;                     // 100% = 10_000 (basis points)
pub const PPM: u64 = 1_000_000;                  // 100% = 1_000_000 (parts per million)
```

### Using proportion() for Fees

```rust
multiversx_sc::imports!();

pub const PERCENT_BASE_POINTS: u64 = 100_000;

/// Apply a percentage fee using framework's proportion()
fn calculate_fee(&self, amount: &BigUint, fee_percent: u64) -> BigUint {
    amount.proportion(fee_percent, PERCENT_BASE_POINTS)
}

/// Amount after deducting fee
fn amount_after_fee(&self, amount: &BigUint, fee_percent: u64) -> BigUint {
    amount - &amount.proportion(fee_percent, PERCENT_BASE_POINTS)
}
```

### BPS (Basis Points) — Manual

When you need explicit control over the calculation:

```rust
pub fn apply_bps(amount: &BigUint, bps: u64) -> BigUint {
    require!(bps <= 10_000, "BPS exceeds 100%");
    (amount * bps) / 10_000u64
}
```

### PPM (Parts Per Million) — Manual

```rust
pub fn apply_ppm(amount: &BigUint, ppm: u32) -> BigUint {
    require!(ppm <= 1_000_000, "PPM exceeds 100%");
    (amount * ppm) / 1_000_000u64
}
```

## Common Math Module Template

```rust
#![no_std]
multiversx_sc::imports!();

#[multiversx_sc::module]
pub trait SharedMathModule {
    fn mul_half_up(
        &self,
        a: &ManagedDecimal<Self::Api, NumDecimals>,
        b: &ManagedDecimal<Self::Api, NumDecimals>,
        precision: NumDecimals,
    ) -> ManagedDecimal<Self::Api, NumDecimals> {
        // ... (implementation above)
    }

    fn div_half_up(
        &self,
        a: &ManagedDecimal<Self::Api, NumDecimals>,
        b: &ManagedDecimal<Self::Api, NumDecimals>,
        precision: NumDecimals,
    ) -> ManagedDecimal<Self::Api, NumDecimals> {
        // ... (implementation above)
    }

    fn to_decimal(
        &self,
        value: BigUint,
        precision: NumDecimals,
    ) -> ManagedDecimal<Self::Api, NumDecimals> {
        ManagedDecimal::from_raw_units(value, precision)
    }

    fn min(
        &self,
        a: ManagedDecimal<Self::Api, NumDecimals>,
        b: ManagedDecimal<Self::Api, NumDecimals>,
    ) -> ManagedDecimal<Self::Api, NumDecimals> {
        if a < b { a } else { b }
    }
}
```

## Rounding Attack Vectors

| Attack | Mitigation |
|---|---|
| Dust deposits to steal rounding | Half-up rounding on all scaled operations |
| Repeated small operations to drain value | Minimum amounts + half-up on indices |
| Precision loss across conversions | Use highest needed precision for intermediate math |
| Exploiting truncation in fee calculations | Always round fees UP (in protocol's favor) |

## Bad/Good Examples

### Bad
```rust
// DON'T: Divide before multiply — loses precision
let shares = (&amount / &total_supply) * &total_shares; // Truncates to 0 for small amounts!
```

### Good
```rust
// DO: Multiply first, then divide to preserve precision
let shares = (&amount * &total_shares) / &total_supply;
```

### Bad
```rust
// DON'T: Hardcode decimal assumptions — tokens can have 0-18 decimals
let one_token = BigUint::from(10u64).pow(18); // Assumes 18 decimals!
```

### Good
```rust
// DO: Fetch decimals from token properties or pass as parameter
let one_token = BigUint::from(10u64).pow(token_decimals as u32);
```

## Anti-Patterns

### 1. Mixing Precisions Without Rescaling
```rust
// WRONG — BPS and RAY have different scales
let result = bps_value + ray_value;

// CORRECT — rescale first
let bps_as_ray = bps_value.rescale(RAY_PRECISION);
let result = bps_as_ray + ray_value;
```

### 2. Using Truncating Division for Fees
```rust
// WRONG — truncation loses value for the protocol
let fee = amount / 100u64; // Truncates

// CORRECT — round up to favor protocol
let fee = (amount + 99u64) / 100u64; // Ceiling division
```

### 3. Intermediate Results at Low Precision
```rust
// WRONG — BPS precision loses significant digits in intermediate calc
let ratio = self.div_half_up(&a, &b, BPS_PRECISION);
let result = self.mul_half_up(&ratio, &c, BPS_PRECISION);

// CORRECT — compute at RAY, downscale at the end
let ratio = self.div_half_up(&a, &b, RAY_PRECISION);
let result = self.mul_half_up(&ratio, &c, RAY_PRECISION);
let final_result = self.rescale_half_up(&result, BPS_PRECISION);
```

## Domain Applications

These generic patterns are used differently across DeFi domains:
- **Lending**: Interest rate models, compound interest (Taylor expansion), utilization ratios — all built on `mul_half_up`/`div_half_up` at RAY precision
- **DEX/AMM**: Price impact calculations, LP share math — WAD precision with half-up rounding
- **Staking**: Reward distribution, share-to-token ratios — RAY indices with safe rescaling
- **Vaults**: Fee calculations, yield accrual — BPS fees with ceiling division

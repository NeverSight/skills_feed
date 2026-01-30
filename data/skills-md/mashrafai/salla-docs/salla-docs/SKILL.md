---
name: salla-docs
description: Comprehensive Salla e-commerce platform documentation. Use this skill when working with Salla APIs (products, orders, shipping, customers, payments, taxes, coupons, store settings, webhooks), Salla storefront JavaScript modules (auth, cart, product, currency, events, forms, ratings, wishlists), Twilight/Twig theme development (layouts, pages, components, file structure), Salla app development (OAuth, app functions, CLI commands, review process), or any Salla-related integration question.
---

# Salla Documentation

## Overview

This skill provides the complete Salla e-commerce platform documentation, consolidated from 676 source pages into per-topic reference files. Each file is sized for single-read loading (under 2000 lines where possible).

## How to Find the Right Reference File

Reference files are in `references/`. Use the exact file names listed below to Read directly — no globbing needed.

For files over 2000 lines (some API endpoint specs), use Grep to find the relevant section first, then Read with offset/limit.

## Reference File Index

### Product APIs
| File | Content |
|---|---|
| `apis-products--List-Products-Salla-Merchant-API-Salla-Docs.md` | List products |
| `apis-products--Product-Details-Salla-Merchant-API-Salla-Docs.md` | Product details |
| `apis-products--Product-Details-By-SKU-Salla-Merchant-API-Salla-Docs.md` | Product details by SKU |
| `apis-products--Create-Product-Salla-Merchant-API-Salla-Docs.md` | Create product |
| `apis-products--Update-Product-Salla-Merchant-API-Salla-Docs.md` | Update product |
| `apis-products--Update-Product-By-SKU-Salla-Merchant-API-Salla-Docs.md` | Update product by SKU |
| `apis-products--Update-Product-Price-By-SKU-Salla-Merchant-API-Salla-Docs.md` | Update product price by SKU |
| `apis-products--Update-Bulk-Product-Prices-Salla-Merchant-API-Salla-Docs.md` | Bulk update prices |
| `apis-products--Bulk-Product-Action-Salla-Merchant-API-Salla-Docs.md` | Bulk product actions |
| `apis-products--Delete-Product-By-SKU-Salla-Merchant-API-Salla-Docs.md` | Delete product by SKU |
| `apis-product-variants--List-Product-Variants-Salla-Merchant-API-Salla-Docs.md` | List product variants |
| `apis-product-variants--Update-Product-Variant-Salla-Merchant-API-Salla-Docs.md` | Update product variant |
| `apis-product-options--Product-Option-Details-Salla-Merchant-API-Salla-Docs.md` | Product option details |
| `apis-product-options--Create-Product-Option-Salla-Merchant-API-Salla-Docs.md` | Create product option |
| `apis-product-option-values--Create-Product-Option-Value-Salla-Merchant-API-Salla-Docs.md` | Create option value |
| `apis-product-option-values--Update-Product-Option-Value-Salla-Merchant-API-Salla-Docs.md` | Update option value |
| `apis-product-option-templates--Option-Template-Details-Salla-Merchant-API-Salla-Docs.md` | Option template details |
| `apis-product-option-templates--Create-Option-Template-Salla-Merchant-API-Salla-Docs.md` | Create option template |
| `apis-product-images--Attach-Image-Salla-Merchant-API-Salla-Docs.md` | Attach product image |
| `apis-product-images--Attach-Youtube-Video-Salla-Merchant-API-Salla-Docs.md` | Attach YouTube video |
| `apis-product-quantity--List-Quantity-Audit-Salla-Merchant-API-Salla-Docs.md` | Quantity audit |
| `apis-product-quantity--Attach-Digital-Code-Salla-Merchant-API-Salla-Docs.md` | Attach digital code |

### Order APIs
| File | Content |
|---|---|
| `apis-orders--List-Orders-Salla-Merchant-API-Salla-Docs.md` | List orders |
| `apis-orders--Orders-Details-Salla-Merchant-API-Salla-Docs.md` | Order details |
| `apis-orders--Create-Order-Salla-Merchant-API-Salla-Docs.md` | Create order |
| `apis-orders--Create-Drafted-Order-Salla-Merchant-API-Salla-Docs.md` | Create drafted order |
| `apis-orders--Update-Order-Salla-Merchant-API-Salla-Docs.md` | Update order |
| `apis-orders--Duplicate-Order-Salla-Merchant-API-Salla-Docs.md` | Duplicate order |
| `apis-orders--Relocate-Order-Stock.md` | Relocate order stock |
| `apis-order-status--Create-Custom-Order-Status-Salla-Merchant-API-Salla-Docs.md` | Create custom order status |
| `apis-order-status--Update-Bulck-Orders-Statuses-Salla-Merchant-API-Salla-Docs.md` | Bulk update order statuses |
| `apis-order-items--List-Order-Items-Salla-Merchant-API-Salla-Docs.md` | List order items |
| `apis-order-items--Create-Orders-Histories-Salla-Merchant-API-Salla-Docs.md` | Create order histories |
| `apis-order-options--Order-Options-Details-Salla-Merchant-API-Salla-Docs.md` | Order option details |
| `apis-order-options--Create-Order-Option-Salla-Merchants-APIs.md` | Create order option |
| `apis-order-invoice--List-Invoices-Salla-Merchant-API-Salla-Docs.md` | List invoices |
| `apis-order-invoice--Create-Invoice-Salla-Merchant-API-Salla-Docs.md` | Create invoice |
| `apis-order-assignment.md` | Order assignment |

### Shipping APIs
| File | Content |
|---|---|
| `apis-shipments--List-Shipments-Salla-Merchant-API-Salla-Docs.md` | List shipments (API) |
| `apis-shipments--Shipment-Details-Salla-Merchant-API-Salla-Docs.md` | Shipment details (API) |
| `apis-shipments--Create-Shipment-Salla-Merchant-API-Salla-Docs.md` | Create shipment (API) |
| `apis-shipments--Update-Shipment-Details-Salla-Merchant-API-Salla-Docs.md` | Update shipment (API) |
| `apis-shipments--Cancel-Shipment-Salla-Merchant-API-Salla-Docs.md` | Cancel shipment (API) |
| `apis-shipments--Return-Shipment-Salla-Merchant-API-Salla-Docs.md` | Return shipment (API) |
| `apis-shipping-companies--Create-Shipping-Company-Salla-Merchant-API-Salla-Docs.md` | Create shipping company |
| `apis-shipping-companies--Update-Shipping-Company-Salla-Merchant-API-Salla-Docs.md` | Update shipping company |
| `apis-shipping-routes--Create-Route-Salla-Merchant-API-Salla-Docs.md` | Create shipping route (API) |
| `apis-shipping-routes--Delete-Route-Salla-Merchant-API-Salla-Docs.md` | Delete shipping route (API) |
| `apis-shipping-routes--Update-Route-Salla-Merchant-API-Salla-Docs.md` | Update shipping route (API) |
| `apis-shipping-zones--Create-Shipping-Zone-Salla-Merchant-API-Salla-Docs.md` | Create shipping zone |
| `apis-shipping-zones--Update-Shipping-Zone-Salla-Merchant-API-Salla-Docs.md` | Update shipping zone |
| `shipments--List-Shipments-Salla-Merchants-APIs-Salla-Docs.md` | List shipments (merchant) |
| `shipments--Shipment-Details-Salla-Merchants-APIs-Salla-Docs.md` | Shipment details (merchant) |
| `shipments--Create-Shipment-Salla-Merchants-APIs-Salla-Docs.md` | Create shipment (merchant) |
| `shipments--Update-Shipment-Details-Salla-Merchants-APIs-Salla-Docs.md` | Update shipment (merchant) |
| `shipments--Cancel-Shipments-Salla-Merchants-APIs-Salla-Docs.md` | Cancel shipment (merchant) |
| `shipments--Return-Shipments-Salla-Merchants-APIs-Salla-Docs.md` | Return shipment (merchant) |
| `shipping-routes--Create-Route-Salla-Merchants-APIs-Salla-Docs.md` | Create route (merchant) |
| `shipping-routes--Delete-Route-Salla-Merchants-APIs-Salla-Docs.md` | Delete route (merchant) |
| `shipping-routes--Update-Route-Salla-Merchants-APIs-Salla-Docs.md` | Update route (merchant) |
| `shipping-management.md` | Shipping management, AWB generation |

### Customer APIs
| File | Content |
|---|---|
| `apis-customers--Ban-Customer-Salla-Merchant-API-Salla-Docs.md` | Ban customer |
| `apis-customers--Import-Customers-Salla-Merchant-API-Salla-Docs.md` | Import customers |
| `apis-customer-groups--Add-Customers-To-Group-Customer-Salla-Merchant-API-Salla-Docs.md` | Add customers to group |
| `apis-customer-groups--Update-Default-Customer-Group-Salla-Merchant-API-Salla-Docs.md` | Update default customer group |
| `apis-customer-wallet.md` | Customer wallet, loyalty points |

### Commerce APIs
| File | Content |
|---|---|
| `apis-coupons--Coupon-Details-Salla-Merchant-API-Salla-Docs.md` | Coupon details |
| `apis-coupons--Create-Coupon-Salla-Merchant-API-Salla-Docs.md` | Create coupon |
| `apis-coupons--Update-Coupon-Salla-Merchant-API-Salla-Docs.md` | Update coupon |
| `apis-coupons--List-Coupon-Codes-Salla-Merchant-API-Salla-Docs.md` | List coupon codes |
| `apis-special-offers--Special-Offer-Details-Salla-Merchant-API-Salla-Docs.md` | Special offer details |
| `apis-special-offers--Create-Special-Offer-Salla-Merchant-API-Salla-Docs.md` | Create special offer |
| `apis-special-offers--Update-Special-Offer-Salla-Merchant-API-Salla-Docs.md` | Update special offer |
| `apis-special-offers--Delete-Special-Offer-Salla-Merchant-API-Salla-Docs.md` | Delete special offer |
| `apis-special-offers--Change-Special-Offer-Status-Salla-Merchant-API-Salla-Docs.md` | Change special offer status |
| `apis-transactions--Transaction-Details-Salla-Merchant-API-Salla-Docs.md` | Transaction details |
| `apis-transactions--Available-Payment-Methods-Salla-Merchant-API-Salla-Docs.md` | Available payment methods |
| `apis-taxes.md` | Taxes |
| `settlements.md` | Settlements |

### Store Management APIs
| File | Content |
|---|---|
| `apis-branches--Branch-Details-Salla-Merchant-API-Salla-Docs.md` | Branch details |
| `apis-branches--Delete-Branch-Salla-Merchant-API-Salla-Docs.md` | Delete branch |
| `apis-branches-allocations--Allocation-Branches-Settings-Salla-Merchant-API-Salla-Docs.md` | Branch allocation settings |
| `apis-branches-allocations--Delete-Branches-Allocations-Salla-Merchant-API-Salla-Docs.md` | Delete branch allocations |
| `apis-branch-delivery-zones--Branch-Delivery-Zone-Details-Salla-Merchant-API-Salla-Docs.md` | Branch delivery zone details |
| `apis-branch-delivery-zones--List-Branch-Deivery-Zones-Salla-Merchant-API-Salla-Docs.md` | List branch delivery zones |
| `apis-brands--Brand-Details-Salla-Merchant-API-Salla-Docs.md` | Brand details |
| `apis-brands--List-Brands-Salla-Merchant-API-Salla-Docs.md` | List brands |
| `apis-categories--List-Category-Salla-Merchant-API-Salla-Docs.md` | List categories |
| `apis-categories--Create-Category-Salla-Merchant-API-Salla-Docs.md` | Create category |
| `apis-categories--Categories-Search-Salla-Merchant-API-Salla-Docs.md` | Search categories |
| `apis-settings.md` | Store settings |
| `apis-merchant--List-Employees-Salla-Merchant-API-Salla-Docs.md` | List employees |
| `apis-merchant--List-Store-Scopes-Salla-Merchant-APIs-Salla-Docs.md` | List store scopes |
| `apis-exports--List-Export-Columns-Salla-Merchant-API-Salla-Docs.md` | List export columns |
| `apis-exports--Create-Export-Template-Salla-Merchant-API-Salla-Docs.md` | Create export template |

### Other APIs
| File | Content |
|---|---|
| `apis-advertisements--Create-Advertisement-Salla-Merchant-API-Salla-Docs.md` | Create advertisement |
| `apis-advertisements--Abandoned-Cart-Details-Salla-Merchant-API-Salla-Docs.md` | Abandoned cart details |
| `apis-affiliates--Affiliate-Details-Salla-Merchant-API-Salla-Docs.md` | Affiliate details |
| `apis-affiliates--Delete-Affiliate-Salla-Merchant-API-Salla-Docs.md` | Delete affiliate |
| `apis-affiliates--Update-Affiliate-Salla-Merchant-API-Salla-Docs.md` | Update affiliate |
| `apis-countries.md` | Countries, cities, districts |
| `apis-currencies--Activate-Currencies-Salla-Merchant-API-Salla-Docs.md` | Activate currencies |
| `apis-currencies--Update-Language-Salla-Merchant-API-Salla-Docs.md` | Update language |
| `apis-dns-records.md` | DNS records, custom URLs |
| `apis-feedbacks--List-Reviews-Salla-Merchant-API-Salla-Docs.md` | List reviews |
| `apis-feedbacks--Feedback-Reply.md` | Feedback reply |
| `apis-webhooks.md` | Webhook API endpoints |

### Storefront SDK (JavaScript)
| File | Content |
|---|---|
| `auth.md` | Authentication module |
| `cart.md` | Cart operations |
| `product--Salla-Product-Card-Salla-Storefront-Twilight-Documentation-Salla-Docs.md` | Product card component |
| `product--Add-Gifted-Product-to-Cart-Twilight-Documentation.md` | Gifted products |
| `elements.md` | UI elements |
| `events.md` | Event system |
| `form.md` | Form handling |
| `user.md` | User module |
| `order-fulfilment.md` | Order fulfilment, order display |
| `rating.md` | Ratings |
| `storefront-misc.md` | Booking, currency, comments, loyalty, wishlist, profile, subscriptions |

### Theme Development (Twilight/Twig)
| File | Content |
|---|---|
| `theme-architecture-layouts.md` | Layouts, base architecture |
| `theme-architecture-components.md` | Component overview |
| `theme-architecture-components-home-components.md` | Home page components |
| `theme-architecture-components-common-components.md` | Common components, product components |
| `theme-architecture-pages-common-pages.md` | Common pages |
| `theme-architecture-pages-customer-pages.md` | Customer pages |
| `theme-architecture-pages-product-pages.md` | Product pages |
| `theme-architecture-pages-blog-pages.md` | Blog pages |
| `theme-architecture-pages-brand-pages.md` | Brand pages |
| `twig-template-engine.md` | Twig template syntax |
| `twilight-themes-command.md` | Twilight CLI commands |
| `files-and-folders-structure.md` | Project file structure |

### App Development
| File | Content |
|---|---|
| `app-details-builder-components.md` | App details builder |
| `app-functions.md` | App functions |
| `apps-command.md` | CLI commands |
| `requirements-and-review-review-process.md` | App review process |

### Webhooks & Events
| File | Content |
|---|---|
| `webhooks-store-events--Abandoned-Cart-Webhook-Events-Model-Salla-Merchant-API-Salla-Docs.md` | Webhook events: abandoned cart, brand, category, communication, customer, invoice, orders |
| `webhooks-store-events--Product-Webhook-Events-Model-Salla-Merchant-API-Salla-Docs.md` | Webhook events: product, review, shipments, shipping zone, special offer, store |
| `merchants-events--Account-Events.md` | Merchant account events |
| `merchants-events--Invoice-Events.md` | Merchant invoice events |

### Getting Started & General
| File | Content |
|---|---|
| `getting-started.md` | Getting started guides, API overview, additional resources |
| `docs--APIs.md` | API overview |
| `docs--Changelog-Merchant-API-Salla-Docs.md` | API changelog |
| `docs--Rate-Limiting-Merchant-API-Salla-Docs.md` | Rate limiting |
| `docs--Salla-Webhooks-Merchant-AP-I-Salla-Docs.md` | Webhooks guide |
| `docs--Conditional-Webhooks-Merchant-API-Salla-Docs.md` | Conditional webhooks |
| `docs--Get-Started-App-Functions-Documentation-Salla-Docs.md` | App functions guide |
| `docs--Theme-Architecture.md` | Theme architecture overview |
| `learn-what-you'll-learn--Additional-Resources.md` | Additional resources |
| `learn-what-you'll-learn--Elements.md` | Elements learning guide |
| `learn-what-you'll-learn--Usage-Device-Mode.md` | Device mode usage |

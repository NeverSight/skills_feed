---
name: tidbx-serverless-driver
description: Guidance for using the TiDB Cloud Serverless Driver (Beta) in Node.js, serverless, and edge environments. Use when connecting to TiDB Cloud Starter/Essential over HTTP with @tidbcloud/serverless, or when integrating with Prisma/Kysely/Drizzle serverless adapters in Vercel/Cloudflare/Netlify/Deno/Bun. Use this skill for serverless driver setup and edge runtime guidance.
---

# TiDB Cloud Serverless Driver (Beta)

Use this skill to guide users who need the TiDB Cloud serverless driver (Beta) in serverless or edge environments.

## Introduction

Serverless and edge runtimes often do not support long-lived TCP connections. Traditional MySQL drivers expect TCP, so they are a poor fit there. The TiDB Cloud serverless driver (Beta) uses HTTP instead, so it works in serverless and edge environments while keeping a similar developer experience.

## Install

**`npm install @tidbcloud/serverless`**

## Tutorials (References)

Use the reference file for the canonical driver overview, examples, configuration, and limitations. Load only what you need, and use the table of contents to jump to the right section:

- Source of truth: `references/serverless-driver.md`

## Usage Guidance

- Confirm the cluster type: Starter or Essential.
- Ask which runtime they use: Node.js, Vercel Edge, Cloudflare Workers, Netlify, Deno, Bun.
- Use the connection string from the TiDB Cloud console. In **Connect**, choose **Serverless Driver**, then generate/reset the password before copying `DATABASE_URL`.
- For provisioning or cluster CRUD, use the `tidbx` skill.

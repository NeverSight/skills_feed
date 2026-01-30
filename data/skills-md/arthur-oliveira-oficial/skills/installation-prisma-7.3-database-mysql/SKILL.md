---
name: installation-prisma-7.3-database-mysql
description: Execute a fault-tolerant installation and configuration of Prisma ORM v7.3.0 architecture with MySQL.
---

# Skill Installation

To install this skill, run the following command:

```bash
npx skills add https://github.com/arthur-oliveira-oficial/skills/tree/main/installation-prisma-7.3-database-mysql --skill installation-prisma-7.3-database-mysql
```

## Prerequisites

Before using this skill, make sure you have:

- Node.js v25.4.0 or higher
- npm 11.7.0 or higher
- TypeScript v5.4.0 or higher
- MySQL (running and accessible)

## Usage

After installation, the skill will be available in the system. See the sections below for detailed instructions on how to use this skill to configure Prisma ORM v7.3.0 with MySQL.

# **SYSTEM DIRECTIVE: PRISMA ORM v7.3.0 DEPLOYMENT PROTOCOL (MySQL)**

## **1\. OPERATIONAL CONTEXT & PERSONA**

**ROLE:** Senior Backend Engineer (TypeScript/SQL Specialist).

**OBJECTIVE:** Execute a fault-tolerant installation and configuration of Prisma ORM v7.3.0 architecture.

**CONSTRAINT LEVEL:** CRITICAL. Strict adherence to Prisma v7 breaking changes (ESM-native, Driver Adapters, Config Files) is mandatory.

## **2\. RUNTIME ENVIRONMENT SPECIFICATIONS**

Before execution, assert the following runtime environment parameters. Abort if non-compliant.

* **Runtime:** Node.js **v25.4.0** (Strict Requirement).  
* **Package Manager:** npm **11.7.0**.  
* **Language:** TypeScript **v5.4.0+**.  
* **Database Engine:** MySQL (Running & Accessible).

## **3\. EXECUTION PROTOCOL**

### **PHASE 1: ESM MODULE CONFIGURATION**

**Context:** Prisma v7 operates natively as an ES Module. Legacy CommonJS patterns are deprecated.

1. **Manifest Configuration (package.json):**  
   Inject the module type directive.  
   "type": "module"

2. **Compiler Configuration (tsconfig.json):**  
   Enforce modern module resolution strategies.  
   {  
     "compilerOptions": {  
       "module": "ESNext",  
       "moduleResolution": "bundler",  
       "target": "ES2023",  
       "strict": true,  
       "esModuleInterop": true  
     }  
   }

### **PHASE 2: DEPENDENCY INJECTION**

**Directive:** Pin strict versions to prevent drift. Use the MariaDB adapter for optimized MySQL throughput.

**Command Sequence:**

\# Core Dependencies  
npm install prisma@7.3.0 @types/node \--save-dev

\# Runtime & Adapter Dependencies  
npm install @prisma/client@7.3.0 @prisma/adapter-mariadb dotenv

### **PHASE 3: INFRASTRUCTURE INITIALIZATION**

**Context:** CLI configuration is now decoupled from environment variables via prisma.config.ts.

1. **Scaffold Project:**  
   npx prisma init \--datasource-provider mysql \--output ../generated/prisma

2. **Configuration Entry Point (prisma.config.ts):**  
   *Action:* Create file at project root.  
   *Requirement:* Explicit dotenv loading is mandatory; the CLI no longer auto-loads .env.  
   import 'dotenv/config';  
   import { defineConfig, env } from 'prisma/config';

   export default defineConfig({  
     schema: 'prisma/schema.prisma',  
     datasource: {  
       url: env('DATABASE\_URL'),  
     },  
   });

3. **Environment Variables (.env):**  
   *Action:* Define connection parameters.  
   DATABASE\_HOST="localhost"  
   DATABASE\_USER="root"  
   DATABASE\_PASSWORD="password"  
   DATABASE\_NAME="mydb"  
   \# Connection String Construction  
   DATABASE\_URL="mysql://root:password@localhost:3306/mydb"

### **PHASE 4: SCHEMA DEFINITION ARCHITECTURE**

**File:** prisma/schema.prisma

**Critical Changes:**

* provider: Must be prisma-client (Not prisma-client-js).  
* output: Explicit path declaration is required.

generator client {  
  provider \= "prisma-client"  
  output   \= "../generated/prisma"  
}

datasource db {  
  provider \= "mysql"  
}

### **PHASE 5: ARTIFACT GENERATION**

**Directive:** Generate the type-safe client based on the schema definition.

npx prisma generate

*WARNING: The migrate dev pipeline no longer triggers generation automatically. This step must be explicit.*

### **PHASE 6: CLIENT INSTANTIATION (DRIVER ADAPTER PATTERN)**

**Context:** Direct instantiation is deprecated for high-performance contexts. Use the PrismaMariaDb adapter.

**File:** lib/prisma.ts

import "dotenv/config";  
import { PrismaMariaDb } from '@prisma/adapter-mariadb';  
import { PrismaClient } from '../generated/prisma/client';

// Initialize Driver Adapter  
const adapter \= new PrismaMariaDb({  
  host: process.env.DATABASE\_HOST,  
  user: process.env.DATABASE\_USER,  
  password: process.env.DATABASE\_PASSWORD,  
  database: process.env.DATABASE\_NAME,  
  connectionLimit: 5 // Optimization: Connection pooling limit  
});

// Instantiate Client with Adapter  
export const prisma \= new PrismaClient({ adapter });

## **4\. COMPLIANCE AUDIT (NEGATIVE CONSTRAINTS)**

**Audit your implementation against these forbidden patterns:**

* \[CRITICAL\] **DO NOT** use prisma-client-js in the generator block. Use prisma-client.  
* \[CRITICAL\] **DO NOT** omit the output path in schema.prisma.  
* \[CRITICAL\] **DO NOT** rely on CLI auto-loading of .env. Explicitly import dotenv/config.  
* \[CRITICAL\] **DO NOT** attempt to interface with MySQL using @prisma/adapter-pg.  
* \[CRITICAL\] **DO NOT** forget "type": "module" in package.json.

## **5\. OPERATION REFERENCE**

* **Schema Migration:** npx prisma migrate dev \--name init  
  * **CRITICAL PROTOCOL:** This command must be executed manually by the user **ONLY AFTER** updating the .env file with valid database credentials.  
* **Artifact Regeneration:** npx prisma generate  
* **Data Inspection:** npx prisma studio
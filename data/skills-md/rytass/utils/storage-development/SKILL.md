---
name: storage-development
description: Development guide for @rytass/storages base package (儲存基底套件開發指南). Use when creating new storage adapters (新增儲存 adapter), understanding base interfaces, or extending storage functionality. Covers StorageInterface, Storage class, file converters (檔案轉換器), hash algorithms (雜湊演算法), and implementation patterns.
---

# Storage Development Guide

This skill provides guidance for developers working with the `@rytass/storages` base package, including creating new storage adapters.

## Overview

The `@rytass/storages` package defines the core interfaces and types that all storage adapters must implement. It follows the adapter pattern to provide a unified API across different storage providers.

**Package:** `@rytass/storages` (v0.2.5)

**Adapters built on this base:**
- `@rytass/storages-adapter-s3` - AWS S3
- `@rytass/storages-adapter-gcs` - Google Cloud Storage
- `@rytass/storages-adapter-r2` - Cloudflare R2
- `@rytass/storages-adapter-azure-blob` - Azure Blob Storage
- `@rytass/storages-adapter-local` - Local File System

## Architecture

```
@rytass/storages (Base Package)
    │
    ├── StorageInterface              # Core interface all adapters must implement
    ├── Storage<O>                    # Base class with helper methods (not abstract)
    ├── ConverterManager              # File converter pipeline system (from @rytass/file-converter)
    ├── Types & Interfaces            # Shared type definitions
    └── Error Handling                # StorageError, ErrorCode enums

@rytass/storages-adapter-*           # Provider implementations
    │
    ├── [Provider]Storage             # Extends Storage<ProviderOptions>
    ├── typings.ts                    # Provider-specific option types
    └── index.ts                      # Package exports
```

### Core Concepts

1. **InputFile**: `Buffer | Readable` - Files to upload can be either in-memory buffers or streams
2. **StorageFile**: `{ key: string }` - Uploaded file reference containing the storage key/path
3. **Hash-Based Naming**: Automatically generate unique filenames using SHA1 or SHA256 hash of file content
4. **File Converters**: Transform or process files during upload (e.g., image resizing, watermarking)
5. **Unified Interface**: All adapters implement the same methods for seamless provider switching

## Installation

```bash
npm install @rytass/storages
```

## Quick Reference

### Core Interfaces

**`StorageInterface`** - Core interface defining the storage contract:

```typescript
interface StorageInterface {
  // Upload operations (Note: options are NOT part of the interface)
  write(file: InputFile): Promise<StorageFile>;
  batchWrite(files: InputFile[]): Promise<StorageFile[]>;

  // Download operations
  read(key: string): Promise<Readable>;
  read(key: string, options: ReadBufferFileOptions): Promise<Buffer>;
  read(key: string, options: ReadStreamFileOptions): Promise<Readable>;

  // File management
  remove(key: string): Promise<void>;
  // Note: isExists() is NOT part of the interface, it's in Storage class
}
```

**`Storage<O>` Class** - Base implementation with helper methods (not abstract, uses throw to force override):

```typescript
class Storage<O extends Record<string, unknown> = Record<string, unknown>>
  implements StorageInterface {
  // Provided by base class
  readonly converterManager: ConverterManager;
  readonly hashAlgorithm: FilenameHashAlgorithm;

  constructor(options?: StorageOptions<O>);

  // File type detection helpers
  getExtension(file: InputFile): Promise<FileTypeResult | undefined>;
  getBufferFilename(buffer: Buffer): Promise<[string, string | undefined]>;
  getStreamFilename(stream: Readable): Promise<[string, string | undefined]>;

  // Methods to override (throw Error by default, subclasses must override)
  write(file: InputFile, options?: WriteFileOptions): Promise<StorageFile>;
  batchWrite(files: InputFile[], options?: WriteFileOptions[]): Promise<StorageFile[]>;
  read(key: string): Promise<Readable>;
  read(key: string, options: ReadBufferFileOptions): Promise<Buffer>;
  read(key: string, options: ReadStreamFileOptions): Promise<Readable>;
  remove(key: string): Promise<void>;

  // Additional method to override (NOT in StorageInterface)
  isExists(key: string): Promise<boolean>;
}
```

> **Note:** The `Storage` class is NOT abstract. Instead, methods throw `Error('Method not implemented.')` by default, requiring subclasses to override them. The `write` and `batchWrite` methods accept `options` parameter in the implementation but NOT in `StorageInterface`.

### Must Implement

All adapters extending `Storage<O>` **MUST** override these methods (not abstract, but throw by default):

| Method | Source | Description |
|--------|--------|-------------|
| `write(file, options?)` | Storage class (options not in interface) | Upload a single file and return storage key |
| `batchWrite(files, options?)` | Storage class (options not in interface) | Upload multiple files in parallel |
| `read(key, options?)` | StorageInterface | Download file as Buffer or Stream |
| `remove(key)` | StorageInterface | Delete a file |
| `isExists(key)` | Storage class only | Check if file exists (not in interface) |

> **Note:** `isExists()` is defined in the `Storage` class but NOT in `StorageInterface`. This means adapters must implement it, but code depending only on `StorageInterface` cannot assume it exists. Similarly, the `options` parameter for `write` and `batchWrite` is only in the `Storage` class implementation.

### Optional Features

Adapters **MAY** implement these additional methods:

| Method | Description | Example |
|--------|-------------|---------|
| `url(key, options?)` | Generate presigned/signed URL for temporary access | Cloud adapters (S3, GCS, R2, Azure) |
| Custom helpers | Provider-specific utilities | `getUsageInfo()` in Local adapter |

### Common Types

```typescript
// Input/Output Types (from @rytass/file-converter)
type ConvertableFile = Readable | Buffer;
type InputFile = ConvertableFile;  // Re-exported alias

type FileKey = string;
interface StorageFile {
  readonly key: FileKey;
}

// Options Types
interface StorageOptions<O extends Record<string, unknown>> {
  converters?: FileConverter<O>[];
  hashAlgorithm?: 'sha1' | 'sha256';
}

interface WriteFileOptions {
  filename?: string;      // Custom filename (overrides hash-based generation)
  contentType?: string;   // MIME type for the file
}

// Read Format Options
interface ReadBufferFileOptions {
  format: 'buffer';
}

interface ReadStreamFileOptions {
  format: 'stream';
}
```

### Error Codes

```typescript
enum ErrorCode {
  WRITE_FILE_ERROR = '101',     // Failed to upload file
  READ_FILE_ERROR = '102',      // Failed to download file
  REMOVE_FILE_ERROR = '103',    // Failed to delete file
  UNRECOGNIZED_ERROR = '104',   // Unknown error
  DIRECTORY_NOT_FOUND = '201',  // Directory doesn't exist (Local adapter)
  FILE_NOT_FOUND = '202',       // File doesn't exist
}
```

## Key Responsibilities

When implementing a new storage adapter, you are responsible for:

1. **Extending `Storage<YourOptions>`** - Inherit from the base class
2. **Defining Configuration Interface** - Specify required and optional settings
3. **Overriding Required Methods** - Override methods that throw by default
4. **Handling Buffers and Streams** - Support both input formats
5. **Using Hash-Based Filenames** - Leverage `getBufferFilename()` / `getStreamFilename()`
6. **Integrating File Converters** - Apply `converterManager.convert()` before upload
7. **Throwing Appropriate Errors** - Use `StorageError` with correct `ErrorCode`
8. **Writing Tests** - Ensure reliability and correctness

## File Converter System

The base package includes a converter system for processing files during upload:

```typescript
// From @rytass/file-converter
type ConvertableFile = Readable | Buffer;

interface FileConverter<O = Record<string, unknown>> {
  convert<Buffer>(file: ConvertableFile): Promise<Buffer>;
  convert<Readable>(file: ConvertableFile): Promise<Readable>;
}

class ConverterManager {
  constructor(converters: FileConverter[]);
  convert<ConvertableFileFormat extends ConvertableFile>(file: ConvertableFile): Promise<ConvertableFileFormat>;
}

// Usage in adapter
const convertedFile = await this.converterManager.convert(inputFile);
```

**Example converters:**
- Image resizing
- Image watermarking
- Format transcoding
- Compression

Converters are executed in sequence before the file is uploaded to the storage provider.

## Detailed Documentation

For complete interface specifications and step-by-step implementation guide:

- [Base Interfaces Reference](BASE-INTERFACES.md) - Complete type definitions and interface specifications
- [Creating an Adapter](CREATE-ADAPTER.md) - Step-by-step guide to implementing a new storage adapter

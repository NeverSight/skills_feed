---
name: storage-adapters
description: File storage adapters (檔案儲存適配器). Use when working with AWS S3, Google Cloud Storage (GCS), Cloudflare R2, Azure Blob, or local file storage (本地儲存). Covers file upload (檔案上傳), download (下載), presigned URLs (簽署 URL), batch operations (批量操作), and NestJS integration.
---

# File Storage Adapters

This skill provides comprehensive guidance for using `@rytass/storages-adapter-*` packages to integrate file storage providers.

## Overview

All adapters implement the `StorageInterface` from `@rytass/storages`, providing a unified API across different storage providers:

| Package | Provider | Description |
|---------|----------|-------------|
| `@rytass/storages-adapter-s3` | AWS S3 | Amazon S3 storage adapter |
| `@rytass/storages-adapter-gcs` | Google Cloud Storage | GCS storage adapter |
| `@rytass/storages-adapter-r2` | Cloudflare R2 | R2 storage adapter with custom domain support |
| `@rytass/storages-adapter-azure-blob` | Azure Blob Storage | Azure blob storage adapter |
| `@rytass/storages-adapter-local` | Local File System | Local disk storage with usage tracking |

### Base Interface (@rytass/storages)

All adapters share these core methods:

```typescript
// StorageInterface - 基礎介面（僅定義核心方法）
interface StorageInterface {
  // Upload files
  write(file: InputFile, options?: WriteFileOptions): Promise<StorageFile>;
  batchWrite(files: InputFile[]): Promise<StorageFile[]>;

  // Download files (3 overloads)
  read(key: string): Promise<Readable>;
  read(key: string, options: ReadBufferFileOptions): Promise<Buffer>;
  read(key: string, options: ReadStreamFileOptions): Promise<Readable>;

  // Delete files
  remove(key: string): Promise<void>;
}

// ReadFileOptions 型別
interface ReadBufferFileOptions {
  format: 'buffer';
}
interface ReadStreamFileOptions {
  format: 'stream';
}

// 以下方法在 Storage 抽象類別中定義（不在 StorageInterface）：
// - isExists(key: string): Promise<boolean>;  // 所有 adapter 都支援

// 以下方法為各 adapter 的額外功能（不在 StorageInterface）：
// - url(key: string, options?): Promise<string>;  // 僅雲端 adapter 支援
```

> **注意**: `batchWrite()` 的 options 陣列參數**僅 LocalStorage 支援**。雲端適配器 (S3, GCS, R2, Azure Blob) 的 `batchWrite()` 不接受 options 參數。

**Key Types（從 @rytass/storages 導出）:**
- `InputFile` - Buffer or Readable stream (alias for `ConvertableFile`)
- `StorageFile` - Object with `readonly key: string` property
- `WriteFileOptions` - `{ filename?: string; contentType?: string }`
- `FilenameHashAlgorithm` - `'sha1' | 'sha256'`
- `FileKey` - Type alias for `string`
- `ReadBufferFileOptions` - `{ format: 'buffer' }`
- `ReadStreamFileOptions` - `{ format: 'stream' }`
- `ConverterManager` - Re-export from `@rytass/file-converter`

**StorageOptions:**
```typescript
interface StorageOptions<O = Record<string, unknown>> {
  converters?: FileConverter<O>[];  // 檔案轉換器陣列
  hashAlgorithm?: FilenameHashAlgorithm;  // 檔名雜湊演算法（預設 'sha256'）
}
```

**Storage Base Class:**
```typescript
abstract class Storage<O = Record<string, unknown>> implements StorageInterface {
  readonly converterManager: ConverterManager;  // 檔案轉換管道
  readonly hashAlgorithm: FilenameHashAlgorithm;  // 檔名雜湊演算法

  // 檔案類型偵測輔助方法
  getExtension(file: InputFile): Promise<FileTypeResult | undefined>;
  getBufferFilename(buffer: Buffer): Promise<[string, string | undefined]>;
  getStreamFilename(stream: Readable): Promise<[string, string | undefined]>;

  // 抽象方法（各 adapter 必須實作）
  abstract write(file: InputFile, options?: WriteFileOptions): Promise<StorageFile>;
  abstract batchWrite(files: InputFile[], options?: WriteFileOptions[]): Promise<StorageFile[]>;
  abstract read(key: string): Promise<Readable>;
  abstract read(key: string, options: ReadBufferFileOptions): Promise<Buffer>;
  abstract read(key: string, options: ReadStreamFileOptions): Promise<Readable>;
  abstract remove(key: string): Promise<void>;
  abstract isExists(key: string): Promise<boolean>;  // 在 Storage 抽象類別中，不在 StorageInterface
}
```

## Installation

```bash
# Install base package
npm install @rytass/storages

# Choose the adapter for your provider
npm install @rytass/storages-adapter-s3
npm install @rytass/storages-adapter-gcs
npm install @rytass/storages-adapter-r2
npm install @rytass/storages-adapter-azure-blob
npm install @rytass/storages-adapter-local
```

## Quick Start

### AWS S3

```typescript
import { StorageS3Service } from '@rytass/storages-adapter-s3';
import { readFileSync, createReadStream } from 'fs';

// Initialize S3 storage
const storage = new StorageS3Service({
  accessKey: process.env.AWS_ACCESS_KEY_ID!,
  secretKey: process.env.AWS_SECRET_ACCESS_KEY!,
  bucket: 'my-bucket',
  region: 'ap-northeast-1',
  // endpoint: 'https://custom-s3-endpoint.com', // Optional: custom S3 endpoint (e.g., MinIO)
});

// Upload a Buffer
const buffer = readFileSync('./document.pdf');
const file1 = await storage.write(buffer, {
  filename: 'documents/report.pdf',
  contentType: 'application/pdf',
});
console.log('Uploaded:', file1.key); // documents/report.pdf

// Upload a Stream (auto-generates filename with hash)
const stream = createReadStream('./image.jpg');
const file2 = await storage.write(stream);
console.log('Uploaded:', file2.key); // e.g., a3f2...b1c4.jpg

// Download as Buffer
const downloadedBuffer = await storage.read(file1.key, { format: 'buffer' });

// Download as Stream
const downloadedStream = await storage.read(file1.key, { format: 'stream' });

// Generate presigned URL (valid for limited time)
const url = await storage.url(file1.key);
console.log('Presigned URL:', url);

// Delete file
await storage.remove(file1.key);

// Check if file exists
const exists = await storage.isExists(file1.key);
console.log('Exists:', exists); // false
```

### Google Cloud Storage

```typescript
import { StorageGCSService } from '@rytass/storages-adapter-gcs';

// Initialize GCS storage with service account credentials
const storage = new StorageGCSService({
  bucket: 'my-gcs-bucket',
  projectId: 'my-project-id',
  credentials: {
    client_email: process.env.GCS_CLIENT_EMAIL!,
    private_key: process.env.GCS_PRIVATE_KEY!.replace(/\\n/g, '\n'),
  },
});

// Upload file
const file = await storage.write(buffer, {
  filename: 'uploads/file.pdf',
});

// Generate signed URL with custom expiration (default: 24 hours)
const url = await storage.url(file.key, Date.now() + 1000 * 60 * 60); // 1 hour
```

### Cloudflare R2

```typescript
import { StorageR2Service } from '@rytass/storages-adapter-r2';

// Initialize R2 storage with custom domain
const storage = new StorageR2Service({
  accessKey: process.env.R2_ACCESS_KEY!,
  secretKey: process.env.R2_SECRET_KEY!,
  bucket: 'my-r2-bucket',
  account: process.env.R2_ACCOUNT_ID!,
  customDomain: 'https://cdn.example.com', // Optional: rewrites presigned URLs
});

// Upload and get presigned URL
const file = await storage.write(buffer);

// Generate presigned URL with custom expiration (in seconds)
const url = await storage.url(file.key, { expires: 3600 }); // 1 hour
console.log('Custom domain URL:', url); // Uses customDomain if configured
```

### Azure Blob Storage

```typescript
import { StorageAzureBlobService } from '@rytass/storages-adapter-azure-blob';

// Initialize Azure Blob storage
const storage = new StorageAzureBlobService({
  connectionString: process.env.AZURE_STORAGE_CONNECTION_STRING!,
  container: 'my-container',
});

// Upload file
const file = await storage.write(buffer, {
  filename: 'files/document.pdf',
});

// Generate SAS token URL with custom expiration
const url = await storage.url(file.key, Date.now() + 1000 * 60 * 60 * 24); // 24 hours
```

### Local File System

```typescript
import { LocalStorage, StorageLocalUsageInfo } from '@rytass/storages-adapter-local';

// Initialize local storage
const storage = new LocalStorage({
  directory: './uploads',
  autoMkdir: true, // Automatically create directory if not exists
});

// Upload file
const file = await storage.write(buffer, {
  filename: 'documents/file.pdf',
});

// Download file
const downloadedBuffer = await storage.read(file.key, { format: 'buffer' });

// Get disk usage information (unique to Local adapter)
// Returns StorageLocalUsageInfo: { used: number, free: number, total: number } (in MB)
const usage: StorageLocalUsageInfo = await storage.getUsageInfo();
console.log(`Used: ${usage.used}MB, Free: ${usage.free}MB, Total: ${usage.total}MB`);
```

**LocalStorage Types:**
```typescript
import {
  LocalStorage,
  StorageLocalOptions,
  StorageLocalUsageInfo,
  StorageLocalHelperCommands,
} from '@rytass/storages-adapter-local';

// Options interface
interface StorageLocalOptions extends StorageOptions {
  directory: string;      // 儲存目錄路徑
  autoMkdir?: boolean;    // 自動建立目錄（預設 false）
}

// Usage info interface (單位: MB)
interface StorageLocalUsageInfo {
  used: number;   // 已使用空間
  free: number;   // 可用空間
  total: number;  // 總空間
}

// Helper commands for *NIX systems (內部使用)
enum StorageLocalHelperCommands {
  USED = "du -sm __DIR__ | awk '{ print $1 }'",
  FREE = "df -m __DIR__ | awk '$3 ~ /[0-9]+/ { print $4 }'",
  TOTAL = "df -m __DIR__ | awk '$3 ~ /[0-9]+/ { print $2 }'",
}
```

## Common Patterns

### Buffer vs Stream Upload

Use **Buffer** when:
- File is already in memory
- File size is small (< 10MB)
- You need to process file content first

Use **Stream** when:
- File is large (> 10MB)
- Streaming from file system or network
- Memory efficiency is important

```typescript
// Buffer upload - simple and direct
const buffer = readFileSync('./file.pdf');
await storage.write(buffer, { filename: 'file.pdf' });

// Stream upload - memory efficient for large files
const stream = createReadStream('./large-video.mp4');
await storage.write(stream, { filename: 'video.mp4' });
```

### Batch Upload Operations

Upload multiple files concurrently:

```typescript
import { readFileSync } from 'fs';

const files = [
  readFileSync('./file1.pdf'),
  readFileSync('./file2.jpg'),
  readFileSync('./file3.doc'),
];

// 雲端適配器 (S3, GCS, R2, Azure Blob) - 不支援 options 陣列
const results = await storage.batchWrite(files);
// 檔名將自動以 hash 生成，例如: a3f2...b1c4.pdf

results.forEach(result => console.log('Uploaded:', result.key));
```

**LocalStorage 專用**: 可透過 options 陣列為每個檔案指定檔名：

```typescript
import { LocalStorage } from '@rytass/storages-adapter-local';

const localStorage = new LocalStorage({ directory: './uploads', autoMkdir: true });

// LocalStorage 支援為每個檔案指定 options
const results = await localStorage.batchWrite(files, [
  { filename: 'documents/file1.pdf' },
  { filename: 'images/file2.jpg' },
  { filename: 'documents/file3.doc' },
]);
```

> 如需在雲端適配器中為每個檔案指定不同的 filename/contentType，請使用迴圈呼叫 `write()` 方法。

### File Converters Integration

使用 `converters` 選項在上傳前自動處理檔案：

```typescript
import { StorageS3Service } from '@rytass/storages-adapter-s3';
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';

// 建立具有自動轉換功能的 storage
const storage = new StorageS3Service({
  accessKey: process.env.AWS_ACCESS_KEY_ID!,
  secretKey: process.env.AWS_SECRET_ACCESS_KEY!,
  bucket: 'my-bucket',
  region: 'ap-northeast-1',
  // 上傳前自動縮放並轉換為 WebP
  converters: [
    new ImageResizer({ maxWidth: 1200, maxHeight: 800, keepAspectRatio: true }),
    new ImageTranscoder({ targetFormat: 'webp', quality: 85 }),
  ],
});

// 檔案會先經過縮放和格式轉換，再上傳
const file = await storage.write(originalImageBuffer);
```

### Custom Hash Algorithm

變更檔名雜湊演算法（預設使用 SHA256）：

```typescript
const storage = new StorageS3Service({
  // ...
  hashAlgorithm: 'sha1', // 或 'sha256' (預設)
});
```

### Error Handling

All adapters throw `StorageError` with specific error codes:

```typescript
import { StorageError, ErrorCode } from '@rytass/storages';

try {
  const file = await storage.read('non-existent-file.pdf', { format: 'buffer' });
} catch (error) {
  if (error instanceof StorageError) {
    switch (error.code) {
      case ErrorCode.FILE_NOT_FOUND:
        console.error('File not found');
        break;
      case ErrorCode.READ_FILE_ERROR:
        console.error('Failed to read file');
        break;
      default:
        console.error('Storage error:', error.message);
    }
  }
}
```

**Error Codes:**
- `WRITE_FILE_ERROR` ('101') - Failed to upload file
- `READ_FILE_ERROR` ('102') - Failed to download file
- `REMOVE_FILE_ERROR` ('103') - Failed to delete file
- `UNRECOGNIZED_ERROR` ('104') - Unknown error
- `DIRECTORY_NOT_FOUND` ('201') - Directory not found (Local adapter)
- `FILE_NOT_FOUND` ('202') - File does not exist

**Note:** Error codes are strings, not numbers.

### File Existence Checking

Always check if a file exists before performing operations:

```typescript
const key = 'documents/important.pdf';

// Check before reading
if (await storage.isExists(key)) {
  const file = await storage.read(key, { format: 'buffer' });
  // Process file...
} else {
  console.log('File does not exist');
}

// Check before deleting
if (await storage.isExists(key)) {
  await storage.remove(key);
  console.log('File deleted');
}
```

### Generating Presigned URLs

Cloud adapters support generating temporary URLs for direct file access:

```typescript
// S3 - NO custom expiration supported (uses default)
const s3Url = await s3Storage.url('file.pdf');

// GCS - custom expiration (timestamp in milliseconds, default: 24 hours)
const gcsUrl = await gcsStorage.url('file.pdf', Date.now() + 1000 * 60 * 30); // 30 minutes

// R2 - custom expiration (seconds in options object) with custom domain
const r2Url = await r2Storage.url('file.pdf', { expires: 1800 }); // 30 minutes in seconds

// Azure Blob - custom expiration (timestamp in milliseconds, default: 24 hours)
const azureUrl = await azureStorage.url('file.pdf', Date.now() + 1000 * 60 * 60); // 1 hour
```

**URL Method Signatures:**
| Adapter | Signature | Expiration |
|---------|-----------|------------|
| S3      | `url(key: string)` | Default only |
| GCS     | `url(key: string, expires?: number)` | Timestamp (ms), default: 24 hours |
| R2      | `url(key: string, options?: { expires?: number })` | Seconds |
| Azure   | `url(key: string, expires?: number)` | Timestamp (ms), default: 24 hours |

**Note:** Local adapter does not support `url()` method as files are stored locally.

## Feature Comparison

| Feature                  | S3 | GCS | R2 | Azure Blob | Local |
|--------------------------|:--:|:---:|:--:|:----------:|:-----:|
| Presigned URL            | ✓  | ✓   | ✓  | ✓          | ✗     |
| Custom Domain            | ✗  | ✗   | ✓  | ✗          | N/A   |
| Batch Upload             | ✓  | ✓   | ✓  | ✓          | ✓     |
| Batch Upload w/ Options  | ✗  | ✗   | ✗  | ✗          | ✓     |
| Buffer Support           | ✓  | ✓   | ✓  | ✓          | ✓     |
| Stream Support           | ✓  | ✓   | ✓  | ✓          | ✓     |
| Usage Info               | ✗  | ✗   | ✗  | ✗          | ✓     |
| File Converters          | ✓  | ✓   | ✓  | ✓          | ✓     |
| Hash Algorithms          | ✓  | ✓   | ✓  | ✓          | ✓     |
| Auto MIME Detection      | ✓  | ✓   | ✓  | ✓          | ✓     |
| Custom Filename          | ✓  | ✓   | ✓  | ✓          | ✓     |

## NestJS Integration

Complete integration with NestJS dependency injection:

### Basic Setup

```typescript
// file-storage.service.ts
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { StorageS3Service } from '@rytass/storages-adapter-s3';
import { LocalStorage } from '@rytass/storages-adapter-local';
import { Storage } from '@rytass/storages';

@Injectable()
export class FileStorageService {
  private storage: Storage;

  constructor(private configService: ConfigService) {
    const provider = this.configService.get('STORAGE_PROVIDER', 'local');

    if (provider === 's3') {
      this.storage = new StorageS3Service({
        accessKey: this.configService.get('AWS_ACCESS_KEY_ID')!,
        secretKey: this.configService.get('AWS_SECRET_ACCESS_KEY')!,
        bucket: this.configService.get('S3_BUCKET')!,
        region: this.configService.get('AWS_REGION', 'ap-northeast-1')!,
      });
    } else {
      this.storage = new LocalStorage({
        directory: this.configService.get('LOCAL_STORAGE_DIR', './uploads')!,
        autoMkdir: true,
      });
    }
  }

  async uploadFile(file: Buffer, filename: string, contentType?: string) {
    return this.storage.write(file, { filename, contentType });
  }

  async downloadFile(key: string): Promise<Buffer> {
    return this.storage.read(key, { format: 'buffer' });
  }

  async deleteFile(key: string): Promise<void> {
    return this.storage.remove(key);
  }

  async fileExists(key: string): Promise<boolean> {
    return this.storage.isExists(key);
  }

  async getFileUrl(key: string): Promise<string> {
    // Type guard to check if storage supports url()
    if ('url' in this.storage && typeof this.storage.url === 'function') {
      return this.storage.url(key);
    }
    throw new Error('Storage provider does not support presigned URLs');
  }
}
```

### Async Configuration with ConfigService

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { FileStorageService } from './file-storage.service';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
  ],
  providers: [FileStorageService],
  exports: [FileStorageService],
})
export class StorageModule {}
```

### Dynamic Provider Selection

```typescript
// storage.factory.ts
import { ConfigService } from '@nestjs/config';
import { Storage } from '@rytass/storages';
import { StorageS3Service } from '@rytass/storages-adapter-s3';
import { StorageGCSService } from '@rytass/storages-adapter-gcs';
import { LocalStorage } from '@rytass/storages-adapter-local';

export const STORAGE_TOKEN = Symbol('STORAGE');

export const storageFactory = {
  provide: STORAGE_TOKEN,
  useFactory: (configService: ConfigService): Storage => {
    const provider = configService.get('STORAGE_PROVIDER', 'local');

    switch (provider) {
      case 's3':
        return new StorageS3Service({
          accessKey: configService.get('AWS_ACCESS_KEY_ID')!,
          secretKey: configService.get('AWS_SECRET_ACCESS_KEY')!,
          bucket: configService.get('S3_BUCKET')!,
          region: configService.get('AWS_REGION')!,
        });

      case 'gcs':
        return new StorageGCSService({
          bucket: configService.get('GCS_BUCKET')!,
          projectId: configService.get('GCS_PROJECT_ID')!,
          credentials: {
            client_email: configService.get('GCS_CLIENT_EMAIL')!,
            private_key: configService.get('GCS_PRIVATE_KEY')!.replace(/\\n/g, '\n'),
          },
        });

      case 'local':
      default:
        return new LocalStorage({
          directory: configService.get('LOCAL_STORAGE_DIR', './uploads')!,
          autoMkdir: true,
        });
    }
  },
  inject: [ConfigService],
};

// app.module.ts
@Module({
  providers: [storageFactory],
  exports: [STORAGE_TOKEN],
})
export class StorageModule {}

// Using in service
@Injectable()
export class UploadService {
  constructor(@Inject(STORAGE_TOKEN) private storage: Storage) {}

  async handleUpload(file: Express.Multer.File) {
    return this.storage.write(file.buffer, {
      filename: `uploads/${file.originalname}`,
      contentType: file.mimetype,
    });
  }
}
```

### Environment Variables

```bash
# .env
STORAGE_PROVIDER=s3  # or gcs, r2, azure, local

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-northeast-1
S3_BUCKET=my-bucket

# Google Cloud Storage
GCS_BUCKET=my-gcs-bucket
GCS_PROJECT_ID=my-project-id
GCS_CLIENT_EMAIL=service-account@project.iam.gserviceaccount.com
GCS_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"

# Cloudflare R2
R2_ACCESS_KEY=your_r2_access_key
R2_SECRET_KEY=your_r2_secret_key
R2_ACCOUNT_ID=your_account_id
R2_BUCKET=my-r2-bucket
R2_CUSTOM_DOMAIN=https://cdn.example.com

# Azure Blob
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_CONTAINER=my-container

# Local Storage
LOCAL_STORAGE_DIR=./uploads
```

## Detailed Documentation

For complete API reference and advanced usage:

- [AWS S3 Adapter Reference](S3.md)
- [Google Cloud Storage Reference](GCS.md)
- [Cloudflare R2 Reference](R2.md)
- [Azure Blob Reference](AZURE-BLOB.md)
- [Local Storage Reference](LOCAL.md)

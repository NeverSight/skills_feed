---
name: nestjs-queue-architect
version: 1.0.0
technology: BullMQ 5.61.0 with NestJS 11.1.7
description: Queue job management patterns, processors, and async workflows for video/image processing
expertise_level: senior
last_updated: 2025-10-22
---

# NestJS Queue Architect - BullMQ Expert

You are a **senior queue architect** specializing in BullMQ with NestJS. Design resilient, scalable job processing systems for media-heavy workflows.

## Technology Stack

- **BullMQ**: 5.61.0 (Redis-backed job queue)
- **@nestjs/bullmq**: 11.0.4
- **@bull-board/nestjs**: 6.13.1 (Queue monitoring UI)

## Project Context Discovery

Before implementing:

1. Check `.agent/SYSTEM/ARCHITECTURE.md` for queue patterns
2. Review existing queue services and constants
3. Look for `[project]-queue-architect` skill

## Core Patterns

### Queue Constants

```typescript
export const QUEUE_NAMES = {
  VIDEO_PROCESSING: 'video-processing',
  IMAGE_PROCESSING: 'image-processing',
} as const;

export const JOB_PRIORITY = {
  HIGH: 1,    // User-facing
  NORMAL: 5,  // Standard
  LOW: 10,    // Background
} as const;
```

### Queue Service

```typescript
@Injectable()
export class VideoQueueService {
  constructor(@InjectQueue(QUEUE_NAMES.VIDEO) private queue: Queue) {}

  async addJob(data: VideoJobData) {
    return this.queue.add(JOB_TYPES.RESIZE, data, {
      priority: JOB_PRIORITY.NORMAL,
      attempts: 3,
      backoff: { type: 'exponential', delay: 2000 },
    });
  }
}
```

### Processor (WorkerHost)

```typescript
@Processor(QUEUE_NAMES.VIDEO)
export class VideoProcessor extends WorkerHost {
  async process(job: Job<VideoJobData>) {
    switch (job.name) {
      case JOB_TYPES.RESIZE: return this.handleResize(job);
      case JOB_TYPES.MERGE: return this.handleMerge(job);
      default: throw new Error(`Unknown job: ${job.name}`);
    }
  }
}
```

## Key Principles

1. **One service per queue type** - Encapsulate job options
2. **Switch-based routing** - Route by `job.name`
3. **Structured error handling** - Log, emit WebSocket, publish Redis, re-throw
4. **Always cleanup** - Temp files in try/finally
5. **Idempotent handlers** - Safe to retry

## Queue Configuration

```typescript
BullModule.registerQueue({
  name: QUEUE_NAMES.VIDEO,
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: 100,  // Prevent Redis bloat
    removeOnFail: 50,
  },
});
```

## Retry Strategy

| Job Type | Attempts | Delay | Reason |
|----------|----------|-------|--------|
| Resize | 3 | 2000ms | Transient failures |
| Merge | 2 | 5000ms | Resource-intensive |
| Metadata | 2 | 1000ms | Fast, fail quickly |
| Cleanup | 5 | 1000ms | Must succeed |

## Common Pitfalls

- **Memory leaks**: Always set `removeOnComplete/Fail`
- **Timeouts**: Set appropriate `timeout` for heavy jobs
- **Race conditions**: Make handlers idempotent

---

**For complete processor examples, testing patterns, Bull Board setup, and Redis pub/sub integration, see:** `references/full-guide.md`

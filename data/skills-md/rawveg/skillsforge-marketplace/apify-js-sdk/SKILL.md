---
name: apify-js-sdk
description: Apify JS SDK Documentation - Web scraping, crawling, and Actor development
---

# Apify-Js-Sdk Skill

Comprehensive assistance with Apify JavaScript SDK development for web scraping, crawling, and Actor creation. This skill provides access to official Apify documentation covering the API, SDK, and platform features.

## When to Use This Skill

This skill should be triggered when:
- Building web scrapers or crawlers with Apify
- Working with Apify Actors (creation, management, deployment)
- Using the Apify JavaScript Client to interact with the Apify API
- Managing Apify datasets, key-value stores, or request queues
- Implementing data extraction with Cheerio or other parsing libraries
- Setting up crawling workflows with link extraction and filtering
- Debugging Apify code or Actor runs
- Configuring logging and monitoring for Apify Actors
- Learning Apify platform best practices

## Key Concepts

### Actors
Serverless cloud programs running on the Apify platform. Actors can perform various tasks like web scraping, data processing, or automation.

### Datasets
Storage for structured data (results from scraping). Each Actor run can have an associated dataset where scraped data is stored.

### Key-Value Stores
Storage for arbitrary data like files, screenshots, or configuration. Each Actor run has a default key-value store.

### Request Queue
Queue for managing URLs to be crawled. Handles URL deduplication and retry logic automatically.

### Apify Client
JavaScript/Python library for interacting with the Apify API programmatically from your code.

## Quick Reference

### Basic Link Extraction with Cheerio

Extract all links from a webpage using Cheerio:

```javascript
import * as cheerio from 'cheerio';
import { gotScraping } from 'got-scraping';

const storeUrl = 'https://warehouse-theme-metal.myshopify.com/collections/sales';

const response = await gotScraping(storeUrl);
const html = response.body;

const $ = cheerio.load(html);

// Select all anchor elements
const links = $('a');

// Extract href attributes
for (const link of links) {
    const url = $(link).attr('href');
    console.log(url);
}
```

### Running an Actor with Apify Client

Call an Actor and wait for results:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_API_TOKEN',
});

// Run an Actor and wait for it to finish
const run = await client.actor('some_actor_id').call();

// Get dataset items from the run
const { items } = await client.dataset(run.defaultDatasetId).listItems();

console.log(items);
```

### Creating and Managing Datasets

Store scraped data in a dataset:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_API_TOKEN',
});

// Create a new dataset
const dataset = await client.datasets().getOrCreate('my-dataset');

// Add items to the dataset
await client.dataset(dataset.id).pushItems([
    { title: 'Product 1', price: 29.99 },
    { title: 'Product 2', price: 39.99 },
]);

// Retrieve items
const { items } = await client.dataset(dataset.id).listItems();
```

### Key-Value Store Operations

Store and retrieve arbitrary data:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_API_TOKEN',
});

const store = await client.keyValueStores().getOrCreate('my-store');

// Store a value
await client.keyValueStore(store.id).setRecord({
    key: 'config',
    value: { apiUrl: 'https://api.example.com' },
});

// Retrieve a value
const record = await client.keyValueStore(store.id).getRecord('config');
console.log(record.value);
```

### Logging Configuration

Set up proper logging for Apify Actors:

```python
import logging
from apify.log import ActorLogFormatter

async def main() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(ActorLogFormatter())

    apify_logger = logging.getLogger('apify')
    apify_logger.setLevel(logging.DEBUG)
    apify_logger.addHandler(handler)
```

### Using the Actor Context

Access Actor run context and storage:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Log messages
        Actor.log.info('Starting Actor run')

        # Access input
        actor_input = await Actor.get_input()

        # Save data to dataset
        await Actor.push_data({
            'url': 'https://example.com',
            'title': 'Example Page'
        })

        # Save to key-value store
        await Actor.set_value('OUTPUT', {'status': 'done'})
```

### Running an Actor Task

Execute a pre-configured Actor task:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_API_TOKEN',
});

// Run a task with custom input
const run = await client.task('task-id').call({
    startUrls: ['https://example.com'],
    maxPages: 10,
});

console.log(`Task run: ${run.id}`);
```

### Redirecting Logs from Called Actors

Redirect logs from a called Actor to the parent run:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Default redirect logger
        await Actor.call(actor_id='some_actor_id')

        # No redirect logger
        await Actor.call(actor_id='some_actor_id', logger=None)

        # Custom redirect logger
        await Actor.call(
            actor_id='some_actor_id',
            logger=logging.getLogger('custom_logger')
        )
```

### Getting Actor Run Details

Retrieve information about an Actor run:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_API_TOKEN',
});

// Get run details
const run = await client.run('run-id').get();

console.log(`Status: ${run.status}`);
console.log(`Started: ${run.startedAt}`);
console.log(`Finished: ${run.finishedAt}`);
```

### Listing Actor Builds

Get all builds for a specific Actor:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'YOUR_API_TOKEN',
});

const { items } = await client.actor('actor-id').builds().list({
    limit: 10,
    desc: true,
});

for (const build of items) {
    console.log(`Build ${build.buildNumber}: ${build.status}`);
}
```

## Reference Files

This skill includes comprehensive documentation in the `references/` directory:

### llms-txt.md
Complete API reference documentation with detailed information on:
- **Actor Management**: Creating, updating, and running Actors
- **Builds**: Managing Actor builds and versions
- **Runs**: Controlling Actor execution and monitoring
- **Tasks**: Pre-configured Actor executions
- **Datasets**: Structured data storage and retrieval
- **Key-Value Stores**: Arbitrary data storage
- **Request Queues**: URL queue management
- **Client SDK**: JavaScript/Python client libraries
- **Logging**: Configuring and managing logs

### llms-full.md
Extensive documentation covering:
- Complete Apify API v2 reference
- All API endpoints with request/response examples
- Authentication and rate limiting
- Error handling
- Webhooks and integrations

### llms.md
High-level overview and getting started guide with:
- Platform concepts and architecture
- Quick start examples
- Common patterns and workflows
- Best practices for web scraping

## Working with This Skill

### For Beginners

Start with these concepts:
1. **Understanding Actors**: Review the Actors introduction to learn about the core building block
2. **First Scraper**: Use the link extraction examples to build your first web scraper
3. **Data Storage**: Learn about Datasets and Key-Value Stores for storing results
4. **API Basics**: Get familiar with the Apify Client for programmatic access

Key reference: `llms.md` for platform overview and getting started guides

### For Intermediate Users

Focus on these areas:
1. **Advanced Crawling**: Implement request queues and link filtering
2. **Actor Tasks**: Set up pre-configured runs with custom inputs
3. **Logging**: Configure proper logging with ActorLogFormatter
4. **Error Handling**: Implement retry logic and error recovery
5. **Webhooks**: Set up notifications for Actor run events

Key reference: `llms-txt.md` for detailed API methods and parameters

### For Advanced Users

Explore these topics:
1. **Actor Builds**: Manage versions and deployments
2. **Metamorph**: Transform running Actors into different Actors
3. **Custom Integrations**: Build complex workflows with the API
4. **Performance Optimization**: Tune concurrency and resource usage
5. **Multi-Actor Orchestration**: Chain multiple Actors together

Key reference: `llms-full.md` for complete API endpoint reference

### Navigation Tips

- **Search by concept**: Use keywords like "dataset", "actor", "build" to find relevant sections
- **Check examples**: Look for code blocks in the documentation for working examples
- **API endpoints**: All endpoints follow the pattern `/v2/{resource}/{action}`
- **Client methods**: SDK methods mirror API endpoints (e.g., `client.actor().run()`)

## Common Patterns

### Web Scraping Workflow

1. Set up the crawler with initial URLs
2. Extract links from pages
3. Filter and enqueue new URLs
4. Extract data from pages
5. Store results in a dataset
6. Handle errors and retries

### Actor Development Workflow

1. Create Actor locally or in Apify Console
2. Write scraping logic with Cheerio/Puppeteer
3. Test locally with sample data
4. Build and deploy to Apify platform
5. Create tasks for different configurations
6. Monitor runs and debug issues

### Data Pipeline Pattern

1. Run an Actor to scrape data
2. Store results in a dataset
3. Call another Actor to process the data
4. Export final results to external system
5. Use webhooks to trigger next steps

## Resources

### Official Documentation
- **API Reference**: Complete API v2 documentation at https://docs.apify.com/api/v2
- **SDK Docs**: JavaScript and Python SDK documentation
- **Academy**: Web scraping tutorials and best practices
- **Examples**: Ready-to-use Actor templates

### Getting Help
- Check the reference files for detailed API documentation
- Review code examples for common patterns
- Use the Apify Console for visual debugging
- Monitor Actor runs with detailed logs

## Notes

- This skill was automatically generated from official Apify documentation
- Reference files preserve structure and examples from source docs
- Code examples include proper language detection for syntax highlighting
- Documentation covers both JavaScript and Python SDKs
- API version 2 is the current stable version

## Best Practices

1. **Always use API tokens** for authentication (never hardcode)
2. **Handle rate limits** appropriately (respect platform quotas)
3. **Store credentials securely** using Actor secrets
4. **Log appropriately** (INFO for progress, DEBUG for details)
5. **Clean up resources** (close stores/datasets when done)
6. **Use request queues** for large-scale crawling
7. **Implement retries** for failed requests
8. **Monitor Actor memory** usage to prevent crashes

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. Review the updated reference files for new features

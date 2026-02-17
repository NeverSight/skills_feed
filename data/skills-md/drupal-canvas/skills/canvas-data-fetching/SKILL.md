---
name: canvas-data-fetching
description:
  Fetch and render Drupal content in Canvas components with JSON:API and SWR
  patterns. Use when building content lists, integrating with SWR, or querying
  related entities. Covers JsonApiClient, DrupalJsonApiParams, relationship
  handling, and filter patterns.
---

# Data fetching

## Data fetching with SWR

Use [SWR](https://swr.vercel.app/) for all data fetching. It provides caching,
revalidation, and a clean hook-based API.

```jsx
import useSWR from "swr";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function Profile() {
  const { data, error, isLoading } = useSWR(
    "https://my-site.com/api/user",
    fetcher,
  );

  if (error) return <div>Failed to load</div>;
  if (isLoading) return <div>Loading...</div>;
  return <div>Hello, {data.name}!</div>;
}
```

## Fetching Drupal content with JSON:API

To fetch content from Drupal (e.g., articles, events, or other content types),
use the autoconfigured `JsonApiClient` from the `drupal-canvas` package combined
with `DrupalJsonApiParams` for query building.

**Important:** Do not mock JSON:API resources in Storybook stories. Components
that fetch data will display their loading or empty states in Storybook.

```jsx
import { getNodePath, JsonApiClient } from "drupal-canvas";
import { DrupalJsonApiParams } from "drupal-jsonapi-params";
import useSWR from "swr";

const Articles = () => {
  const client = new JsonApiClient();
  const { data, error, isLoading } = useSWR(
    [
      "node--article",
      {
        queryString: new DrupalJsonApiParams()
          .addSort("created", "DESC")
          .getQueryString(),
      },
    ],
    ([type, options]) => client.getCollection(type, options),
  );

  if (error) return "An error has occurred.";
  if (isLoading) return "Loading...";
  return (
    <ul>
      {data.map((article) => (
        <li key={article.id}>
          <a href={getNodePath(article)}>{article.title}</a>
        </li>
      ))}
    </ul>
  );
};

export default Articles;
```

### Including relationships with `addInclude`

When you need related entities (e.g., images, taxonomy terms), use `addInclude`
to fetch them in a single request.

**Avoid circular references in JSON:API responses.** SWR uses deep equality
checks to compare cached data, which fails with "too much recursion" errors when
the response contains circular references.

**Do not include self-referential fields.** Fields that reference the same
entity type being queried (e.g., `field_related_articles` on an article query)
create circular references: Article A references Article B, which references
back to Article A. If you need related content of the same type, fetch it in a
separate query.

**Use `addFields` to limit the response.** Always specify only the fields you
need. This improves performance and helps avoid circular reference issues:

```jsx
const params = new DrupalJsonApiParams();
params.addSort("created", "DESC");
params.addInclude(["field_category", "field_image"]);

// Limit fields for each entity type
params.addFields("node--article", [
  "title",
  "created",
  "field_category",
  "field_image",
]);
params.addFields("taxonomy_term--categories", ["name"]);
params.addFields("file--file", ["uri", "url"]);
```

## Creating content list components

When building a component that displays a list of content items (e.g., a news
listing, event calendar, or resource library), follow this workflow:

### Step 1: Analyze the list structure

Examine the design to understand what data each list item needs:

- What fields are displayed (title, date, image, category, etc.)?
- How are items sorted (newest first, alphabetical, etc.)?
- Are there filters or pagination?

### Step 2: Identify or request the content type

Before writing code, verify that an appropriate content type exists in Drupal:

1. Check the JSON:API endpoint of your local Drupal site (configured via
   `CANVAS_SITE_URL` and `CANVAS_JSONAPI_PREFIX` environment variables) to find
   a content type that matches the required structure. Use a plain `fetch`
   request for this check.

2. If a matching content type exists, use it and note which fields are
   available.

3. If no matching content type exists, **stop and prompt the user** to create
   one. Provide:
   - A suggested content type name
   - The required field structure based on the list design

### Step 3: Build the component

Create the content list component using JSON:API to fetch content. Only use
fields that actually exist on the content type—do not assume fields exist
without verifying.

### Handling filters

If the list includes filters based on entity reference fields (e.g., filter by
category, filter by author):

- **Do not hardcode filter options.** Filter options should be fetched
  dynamically using JSON:API.
- Fetch the available options for each filter (e.g., all taxonomy terms in a
  vocabulary) and populate the filter UI from that data.

This ensures filters stay in sync with the actual content in Drupal and new
options appear automatically without code changes.

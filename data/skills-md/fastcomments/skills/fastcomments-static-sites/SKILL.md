---
name: fastcomments-static-sites
description: >
  Use when adding comments to a static site or blog built with Astro, Hugo, Jekyll, Eleventy (11ty),
  Docusaurus, or Gatsby, where there is no backend to store comments. Covers the FastComments theme
  component, plugin, and tag for each generator, setting the tenant ID once in site config, picking a stable
  urlId per post so threads survive URL changes, showing comment counts on a blog index with one bulk
  request, and the no-JavaScript fallback. For React and Next.js see fastcomments-react-nextjs.
---

# FastComments on static sites

A static site generator has nowhere to put comments, which is what a hosted commenting service is for. Each
generator has a first-party integration: set a tenant ID once in site config, then place a tag, shortcode,
or component wherever the thread belongs.

Get a tenant ID at `https://fastcomments.com/auth/my-account/api-secret`, or use `"demo"` to try it first.
If the account was created on `https://eu.fastcomments.com`, every widget also needs `region: "eu"`.

## Pick the urlId before you ship

`urlId` is what groups comments into a thread. Left unset it defaults to a cleaned version of the page URL,
which is exactly the thing that changes on a static site: you rename a post, add a locale prefix, move from
`/blog/post` to `/blog/post/`, or deploy a preview build on a different domain. Each variation is a
separate, empty thread.

Set it to something stable that survives a rebuild - the post's permalink slug, a front-matter ID, or a date
plus slug. Then pass `url` too, so notification emails and moderation tools link back to the real page.

If comments have already landed under the wrong `urlId`, the domain migration tool moves them: enter the old
and new values in the `from` and `to` fields at
`https://fastcomments.com/auth/my-account/manage-data/copy-comments`.

## Astro

```bash
npm install fastcomments-astro
```

```astro
---
import { FastComments } from 'fastcomments-astro';
const { post } = Astro.props;
---
<FastComments tenantId="TENANT_ID" urlId={post.slug} />
```

Also exported: `FastCommentsCommentCount`, `FastCommentsLiveChat`, `FastCommentsCollabChat`,
`FastCommentsImageChat`, `FastCommentsReviewsSummary`, `FastCommentsUserActivityFeed`.

## Hugo

A theme component, installed either as a Hugo module (recommended) or a submodule.

```bash
hugo mod init github.com/you/your-site   # only if the site is not already a module
hugo mod get github.com/FastComments/fastcomments-hugo
```

```toml
[module]
  [[module.imports]]
    path = "github.com/FastComments/fastcomments-hugo"

[params.fastcomments]
  tenantId = "TENANT_ID"
```

As a submodule instead, list it after your own theme, because later entries win:

```toml
theme = ["your-theme", "fastcomments-hugo"]
```

Then a shortcode in any Markdown page, or wire it into the theme's single-page template:

```
{{< fastcomments >}}
```

Shortcodes: `fastcomments`, `fastcomments-comment-count`, `fastcomments-comment-count-bulk`,
`fastcomments-live-chat`, `fastcomments-collab-chat` (needs `target`), `fastcomments-image-chat` (needs
`target`), `fastcomments-recent-comments`, `fastcomments-recent-discussions`,
`fastcomments-reviews-summary`, `fastcomments-top-pages`, `fastcomments-user-activity-feed` (needs
`userId`).

```
<article id="post-body">
  <p>Highlight me to leave a comment.</p>
</article>
{{< fastcomments-collab-chat target="#post-body" >}}
```

## Jekyll

```yaml
# _config.yml
fastcomments:
  tenant_id: TENANT_ID
```

```liquid
{% fastcomments %}
```

Tags: `fastcomments`, `fastcomments_comment_count`, `fastcomments_comment_count_bulk`,
`fastcomments_live_chat`, `fastcomments_collab_chat`, `fastcomments_image_chat`,
`fastcomments_recent_comments`, `fastcomments_recent_discussions`, `fastcomments_reviews_summary`,
`fastcomments_top_pages`, `fastcomments_user_activity_feed`.

## Eleventy (11ty)

```js
// eleventy.config.js
const { fastcommentsPlugin } = require('fastcomments-11ty');

module.exports = function (eleventyConfig) {
    eleventyConfig.addPlugin(fastcommentsPlugin);
};
```

The plugin registers shortcodes; it can also be skipped entirely in favour of the raw embed. See
`https://docs.fastcomments.com/guide-lib-11ty.html`.

## Docusaurus

A theme component. When swizzling or wrapping, import the original from `@theme-init/*`, not
`@theme-original/*`. Guide: `https://docs.fastcomments.com/guide-lib-docusaurus.html`.

## Gatsby

Use `fastcomments-react`:

```tsx
import { FastCommentsCommentWidget } from 'fastcomments-react';

return <FastCommentsCommentWidget tenantId="TENANT_ID" urlId={post.id} />;
```

Runnable example: `https://github.com/FastComments/fastcomments-gatsbyjs-example`.

## Any other generator

The VanillaJS embed works in any template that can emit a script tag:

```html
<script src="https://cdn.fastcomments.com/js/embed-v2.min.js"></script>
<div id="fastcomments-widget"></div>
<script>
window.FastCommentsUI(document.getElementById('fastcomments-widget'), {
    tenantId: "TENANT_ID",
    urlId: "POST_SLUG"
});
</script>
```

## Comment counts on the index page

Do not render one comment-count widget per row; that is one request per post. Use the bulk count, which
takes a single request for the whole page. Mark each row with the `urlId` it belongs to, then place the bulk
tag once:

```liquid
{% for post in site.posts %}
  <a href="{{ post.url }}">{{ post.title }}</a>
  <span class="fast-comments-count" data-fast-comments-url-id="{{ post.url }}"></span>
{% endfor %}
{% fastcomments_comment_count_bulk %}
```

Hugo has `fastcomments-comment-count-bulk` for the same job.

## Keeping comments without JavaScript

Static sites are often built for readers with scripting off. FastComments renders the full thread
server-side at `https://fastcomments.com/ssr/comments`, taking `tenantId`, `urlId`, and `url` as query
parameters:

```html
<noscript>
  <iframe src="https://fastcomments.com/ssr/comments?tenantId=TENANT_ID&urlId=POST_SLUG&url=PAGE_URL"
          title="FastComments" width="100%" height="1500px" frameborder="0"
          style="width: 1px !important; min-width: 100% !important; border: none !important;"></iframe>
</noscript>
```

URL-encode the parameters. SSR supports anonymous and logged-in commenting, SSO, nested replies,
pagination, voting, sort direction, and the same custom CSS as the JS widget. There is no JavaScript to size
the container, so pick a height. The FastComments blog itself generates at build time and uses this as its
fallback.

## Styling

Point `customCSS` at a stylesheet on your own domain, or set `hasDarkBackground: true` for dark themes. The
SSR output uses the same markup and rendering engine as the JS widget, so one stylesheet covers both.

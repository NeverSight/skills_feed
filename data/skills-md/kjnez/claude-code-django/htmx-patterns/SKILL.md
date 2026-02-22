---
name: htmx-patterns
description: HTMX patterns for Django including partial templates, hx-* attributes, and dynamic UI without JavaScript. Use when building interactive UI, handling AJAX requests, or creating dynamic components.
---

# HTMX Patterns for Django

## Core Philosophy

- Server renders HTML, not JSON - HTMX requests return HTML fragments, not data
- Partial templates for dynamic updates - separate `_partial.html` files for HTMX responses
- Progressive enhancement - pages work without JavaScript, HTMX enhances UX
- Minimal client-side complexity - let the server do the heavy lifting

## Critical Hints & Reminders

### UX Best Practices

**Always include loading indicators**
- Use `hx-indicator` to show loading states during requests
- Users should never wonder if their action worked
- Example: `<button hx-get="/data/" hx-indicator="#spinner">Load</button>`

**Always provide user feedback**
- Use Django messages framework for success/error feedback
- Return error messages in HTMX responses, not silent failures
- Show what happened after an action completes

**Handle errors gracefully**
- Return proper HTTP status codes (400 for validation errors, 500 for server errors)
- Render form errors in partial templates
- Don't swallow exceptions - log and show user-friendly messages

### Django-Specific Patterns

**Always detect HTMX requests**
- Check `request.headers.get("HX-Request")` to detect HTMX requests
- Return partial templates for HTMX, full page templates otherwise
- Pattern: `if request.headers.get("HX-Request"): return render(request, "_partial.html", context)`

**Always return partials for HTMX**
- HTMX requests should return `_partial.html` templates, not full pages with `base.html`
- Full page responses to HTMX requests break the UX and send duplicate HTML
- Partials should be self-contained HTML fragments

**Always validate request.method**
- Check `request.method == "POST"` before processing form data
- Return proper status codes (405 Method Not Allowed for wrong methods)

**CSRF is already configured globally**
- The base template has `hx-headers` on `<body>` - no need to add CSRF tokens to individual forms
- All HTMX requests automatically include the CSRF token

### Template Organization

**Naming convention**
- Partials: `_partial.html` (underscore prefix)
- Full pages: `page.html` (no prefix)
- Example: `posts/list.html` (full page) includes `posts/_list.html` (partial)

**Structure**
- Full page template extends `base.html` and includes partial
- Partial contains only the dynamic HTML fragment
- HTMX targets the partial's container div

**Keep partials focused**
- Each partial should represent one logical UI component
- Avoid partials that are too large or do too much
- Compose larger UIs from multiple smaller partials

## Django View Patterns

### HTMX Detection

Check the `HX-Request` header to detect HTMX requests:

```python
def my_view(request):
    context = {...}

    if request.headers.get("HX-Request"):
        return render(request, "app/_partial.html", context)

    return render(request, "app/full_page.html", context)
```

### Form Handling Pattern

Key points:
- Validate form normally
- On success: return partial with new data OR trigger client-side event
- On error: return partial with form errors
- Always handle both HTMX and non-HTMX cases

```python
def create_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if request.headers.get("HX-Request"):
                return render(request, "app/_item.html", {"item": obj})
            return redirect("app:list")

        # Return form with errors
        if request.headers.get("HX-Request"):
            return render(request, "app/_form.html", {"form": form})
    else:
        form = MyForm()

    return render(request, "app/create.html", {"form": form})
```

## Response Headers Reference

HTMX respects special response headers for client-side behavior:

### HX-Trigger
Trigger client-side events after response
- Use case: Update other parts of page after action
- Example: `response["HX-Trigger"] = "itemCreated"`
- Template listens: `<div hx-get="/count/" hx-trigger="itemCreated from:body">`

### HX-Redirect
Client-side redirect
- Use case: Redirect after successful action
- Example: `response["HX-Redirect"] = reverse("app:detail", args=[obj.pk])`

### HX-Retarget / HX-Reswap
Override hx-target and hx-swap from server
- Use case: Different targets for success vs error
- Success: `response["HX-Retarget"] = "#main"`
- Error: Return partial without changing target (targets the form)

### HX-Refresh
Force full page refresh
- Use case: Major state change that affects whole page
- Example: `response["HX-Refresh"] = "true"`

## Common Pitfalls

- **Missing loading indicators**: Always use `hx-indicator` - users click multiple times without feedback
- **Full pages in HTMX responses**: Return `_partial.html`, not full pages with `base.html` - check `HX-Request` header
- **Not handling form errors**: Always return the form with errors on validation failure, not just the success case
- **Not disabling buttons**: Use `hx-disabled-elt="this"` to prevent duplicate submissions
- **N+1 queries**: HTMX views need `select_related()`/`prefetch_related()` just like regular views

## Integration with Other Skills

- **django-templates**: Partial template organization and inheritance patterns
- **django-forms**: HTMX form submission and validation
- **django-extensions**: Use `show_urls` to verify HTMX endpoints
- **pytest-django-patterns**: Testing HTMX endpoints and headers
- **systematic-debugging**: Debug HTMX request/response issues

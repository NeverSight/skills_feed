---
name: optimizely-development
description: Core Optimizely CMS development patterns and best practices
---

# Optimizely CMS Development

## Overview

This skill covers core Optimizely CMS (formerly Episerver) development patterns including content types, initialization modules, and the content API.

## Content Types

### Page Types

```csharp
using EPiServer.Core;
using EPiServer.DataAnnotations;
using System.ComponentModel.DataAnnotations;

[ContentType(
    GUID = "f8d47a38-5b23-4c8e-9f12-3a7e8b9c2d1f",
    DisplayName = "Article Page",
    Description = "Standard article page with heading and body content",
    GroupName = "Content")]
public class ArticlePage : PageData
{
    [Display(
        Name = "Heading",
        Description = "Main heading for the article",
        GroupName = SystemTabNames.Content,
        Order = 100)]
    [Required]
    public virtual string Heading { get; set; }

    [Display(
        Name = "Main Content",
        GroupName = SystemTabNames.Content,
        Order = 200)]
    public virtual XhtmlString MainBody { get; set; }

    [Display(
        Name = "Published Date",
        GroupName = SystemTabNames.Content,
        Order = 300)]
    public virtual DateTime? PublishedDate { get; set; }
}
```

### Block Types

```csharp
[ContentType(
    GUID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    DisplayName = "Hero Block",
    Description = "Full-width hero section")]
public class HeroBlock : BlockData
{
    [Display(Name = "Heading", Order = 10)]
    [Required]
    public virtual string Heading { get; set; }

    [Display(Name = "Subheading", Order = 20)]
    public virtual string Subheading { get; set; }

    [Display(Name = "Background Image", Order = 30)]
    [UIHint(UIHint.Image)]
    public virtual ContentReference BackgroundImage { get; set; }

    [Display(Name = "Call to Action", Order = 40)]
    public virtual Url CallToActionUrl { get; set; }
}
```

### Content Areas with Restrictions

```csharp
[Display(Name = "Main Content Area", Order = 100)]
[AllowedTypes(typeof(TextBlock), typeof(ImageBlock), typeof(VideoBlock))]
public virtual ContentArea MainContentArea { get; set; }

[Display(Name = "Sidebar Blocks", Order = 200)]
[AllowedTypes(typeof(TeaserBlock), typeof(LinkListBlock))]
[MaxItems(3)]
public virtual ContentArea SidebarArea { get; set; }
```

## Initialization Modules

### Configurable Module

```csharp
using EPiServer.Framework;
using EPiServer.Framework.Initialization;
using EPiServer.ServiceLocation;
using Microsoft.Extensions.DependencyInjection;

[InitializableModule]
[ModuleDependency(typeof(ServiceContainerInitialization))]
public class DependencyResolverInitialization : IConfigurableModule
{
    public void ConfigureContainer(ServiceConfigurationContext context)
    {
        context.Services.AddScoped<IArticleService, ArticleService>();
        context.Services.AddScoped<ISearchService, SearchService>();
    }

    public void Initialize(InitializationEngine context)
    {
        // Initialization logic
    }

    public void Uninitialize(InitializationEngine context)
    {
        // Cleanup logic
    }
}
```

### Content Events Module

```csharp
[InitializableModule]
[ModuleDependency(typeof(EPiServer.Web.InitializationModule))]
public class ContentEventsInitialization : IInitializableModule
{
    public void Initialize(InitializationEngine context)
    {
        var events = context.Locate.ContentEvents();
        events.PublishedContent += OnPublishedContent;
        events.SavingContent += OnSavingContent;
    }

    private void OnPublishedContent(object sender, ContentEventArgs e)
    {
        // Handle content published event
    }

    private void OnSavingContent(object sender, ContentEventArgs e)
    {
        // Handle content saving event
    }

    public void Uninitialize(InitializationEngine context)
    {
        var events = context.Locate.ContentEvents();
        events.PublishedContent -= OnPublishedContent;
        events.SavingContent -= OnSavingContent;
    }
}
```

## Content API

### IContentLoader (Cached Reads)

```csharp
public class ArticleService : IArticleService
{
    private readonly IContentLoader _contentLoader;

    public ArticleService(IContentLoader contentLoader)
    {
        _contentLoader = contentLoader;
    }

    public T Get<T>(ContentReference contentLink) where T : IContent
    {
        return _contentLoader.Get<T>(contentLink);
    }

    public IEnumerable<T> GetChildren<T>(ContentReference parentLink) where T : IContent
    {
        return _contentLoader.GetChildren<T>(parentLink);
    }

    // Batch loading - more efficient than loading one by one
    public IEnumerable<IContent> GetItems(IEnumerable<ContentReference> contentLinks)
    {
        return _contentLoader.GetItems(contentLinks, new LoaderOptions());
    }
}
```

### IContentRepository (Write Operations)

```csharp
public class ContentManager
{
    private readonly IContentRepository _contentRepository;

    public ContentManager(IContentRepository contentRepository)
    {
        _contentRepository = contentRepository;
    }

    public ContentReference CreatePage<T>(ContentReference parentLink, string name) where T : PageData
    {
        var page = _contentRepository.GetDefault<T>(parentLink);
        page.Name = name;
        return _contentRepository.Save(page, SaveAction.Publish);
    }

    public void UpdateContent(IContent content)
    {
        var writableContent = content.CreateWritableClone();
        // Make changes
        _contentRepository.Save(writableContent, SaveAction.Publish);
    }
}
```

## Scheduled Jobs

```csharp
[ScheduledPlugIn(
    DisplayName = "Content Cleanup Job",
    Description = "Removes expired content",
    GUID = "12345678-1234-1234-1234-123456789012")]
public class ContentCleanupJob : ScheduledJobBase
{
    private readonly IContentRepository _contentRepository;

    public ContentCleanupJob(IContentRepository contentRepository)
    {
        _contentRepository = contentRepository;
    }

    public override string Execute()
    {
        var processedCount = 0;

        // Job logic here
        OnStatusChanged($"Processing... {processedCount} items");

        return $"Completed. Processed {processedCount} items.";
    }
}
```

## Property Value Converters

```csharp
public class TagListPropertyConverter : PropertyValueConverterBase
{
    public override object Convert(object value, Type targetType)
    {
        if (value is string tags)
        {
            return tags.Split(',').Select(t => t.Trim()).ToList();
        }
        return new List<string>();
    }
}
```

## Best Practices

1. **Always use GUIDs** on content types for serialization
2. **Use IContentLoader** for reads (cached)
3. **Use IContentRepository** for writes only
4. **Batch load** content instead of loading in loops
5. **Bound queries** with Take() to prevent loading thousands of items
6. **Use constructor injection** instead of ServiceLocator

---
name: markdown-editor-integrator
description: This skill should be used when installing and configuring markdown editor functionality using @uiw/react-md-editor. Applies when adding rich text editing, markdown support, WYSIWYG editors, content editing with preview, or text formatting features. Trigger terms include markdown editor, rich text editor, text editor, add markdown, install markdown editor, markdown component, WYSIWYG, content editor, text formatting, editor preview.
---

# Markdown Editor Integrator

Install and configure @uiw/react-md-editor with theme integration, server-side sanitization, controlled/uncontrolled modes, and proper persistence for worldbuilding content.

## When to Use This Skill

Apply this skill when:
- Adding markdown editing capability to forms
- Creating rich text editing for entity descriptions
- Building content management features
- Adding WYSIWYG editing with markdown preview
- Implementing text formatting for character bios, location descriptions, lore entries
- Setting up markdown support for notes and documentation
- Creating editing interfaces for narrative content

## Overview

@uiw/react-md-editor is a React markdown editor with:
- Live preview with split/edit/preview modes
- Syntax highlighting
- Markdown shortcuts and toolbar
- Theme customization
- No SSR issues
- TypeScript support

## Installation Process

### Step 1: Install Dependencies

```bash
npm install @uiw/react-md-editor
```

For sanitization (security):
```bash
npm install rehype-sanitize
```

### Step 2: Configure Next.js (if using)

Add to next.config.js to avoid SSR issues:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Other config...
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@uiw/react-md-editor': '@uiw/react-md-editor',
    }
    return config
  },
}

module.exports = nextConfig
```

### Step 3: Create Editor Component

Create wrapper component at `components/MarkdownEditor.tsx`:

See assets/MarkdownEditor.tsx for full implementation.

### Step 4: Create Preview Component

Create preview component at `components/MarkdownPreview.tsx`:

See assets/MarkdownPreview.tsx for full implementation.

### Step 5: Integrate Theme Styling

Configure editor to match shadcn/ui theme:

See references/theme-integration.md for detailed theming.

### Step 6: Add Server-Side Sanitization

Implement sanitization for security:

See references/sanitization.md for implementation details.

## Basic Usage Patterns

### Controlled Mode (Recommended for Forms)

```tsx
'use client'

import { useState } from 'react'
import { MarkdownEditor } from '@/components/MarkdownEditor'
import { Button } from '@/components/ui/button'

export function CharacterBioForm() {
  const [bio, setBio] = useState('')

  async function handleSubmit() {
    await saveCharacter({ bio })
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium">Biography</label>
        <MarkdownEditor
          value={bio}
          onChange={(value) => setBio(value || '')}
          height={400}
        />
      </div>
      <Button onClick={handleSubmit}>Save</Button>
    </div>
  )
}
```

### With React Hook Form

```tsx
'use client'

import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { MarkdownEditor } from '@/components/MarkdownEditor'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'

const schema = z.object({
  description: z.string().min(1, 'Description required').max(10000)
})

type FormValues = z.infer<typeof schema>

export function LocationForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      description: ''
    }
  })

  function onSubmit(values: FormValues) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <MarkdownEditor
                  value={field.value}
                  onChange={(value) => field.onChange(value || '')}
                  height={400}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### Preview Mode (Display Only)

```tsx
import { MarkdownPreview } from '@/components/MarkdownPreview'

export function CharacterProfile({ character }) {
  return (
    <div>
      <h2>{character.name}</h2>
      <div className="prose dark:prose-invert max-w-none">
        <MarkdownPreview content={character.biography} />
      </div>
    </div>
  )
}
```

### Uncontrolled Mode

```tsx
'use client'

import { useRef } from 'react'
import MDEditor from '@uiw/react-md-editor'

export function QuickNoteEditor() {
  const editorRef = useRef<HTMLDivElement>(null)

  function handleSave() {
    // Access value from ref if needed
  }

  return (
    <MDEditor
      ref={editorRef}
      defaultValue="Initial content"
      height={300}
    />
  )
}
```

## Configuration Options

### Height Control

```tsx
// Fixed height
<MarkdownEditor height={400} />

// Dynamic height
<MarkdownEditor height="60vh" />

// Auto height
<MarkdownEditor height="auto" />
```

### Hide Toolbar

```tsx
<MarkdownEditor
  hideToolbar
  value={value}
  onChange={setValue}
/>
```

### Preview Mode

```tsx
<MarkdownEditor
  preview="edit"    // Edit only
  preview="live"    // Split view (default)
  preview="preview" // Preview only
  value={value}
  onChange={setValue}
/>
```

### Disable Preview

```tsx
<MarkdownEditor
  enablePreview={false}
  value={value}
  onChange={setValue}
/>
```

### Custom Commands

```tsx
import { commands } from '@uiw/react-md-editor'

<MarkdownEditor
  commands={[
    commands.bold,
    commands.italic,
    commands.strikethrough,
    commands.hr,
    commands.divider,
    commands.link,
    commands.quote,
    commands.code,
    commands.image,
    commands.unorderedListCommand,
    commands.orderedListCommand,
    commands.checkedListCommand,
  ]}
  value={value}
  onChange={setValue}
/>
```

### Extra Commands

```tsx
<MarkdownEditor
  extraCommands={[
    commands.codeEdit,
    commands.codeLive,
    commands.codePreview,
    commands.divider,
    commands.fullscreen,
  ]}
  value={value}
  onChange={setValue}
/>
```

## Theme Integration

### Match shadcn/ui Theme

```tsx
'use client'

import { useTheme } from 'next-themes'
import MDEditor from '@uiw/react-md-editor'

export function ThemedMarkdownEditor({ value, onChange }) {
  const { theme } = useTheme()

  return (
    <div data-color-mode={theme === 'dark' ? 'dark' : 'light'}>
      <MDEditor
        value={value}
        onChange={onChange}
        height={400}
        className="rounded-md border"
      />
    </div>
  )
}
```

### Custom Styling

```css
/* globals.css or component CSS */

.w-md-editor {
  @apply rounded-md border border-input bg-background;
}

.w-md-editor-toolbar {
  @apply border-b border-border bg-muted/50;
}

.w-md-editor-toolbar button {
  @apply text-foreground hover:bg-accent hover:text-accent-foreground;
}

.w-md-editor-content {
  @apply text-foreground;
}

.w-md-editor-preview {
  @apply prose prose-sm dark:prose-invert max-w-none;
}

.wmde-markdown {
  @apply bg-background text-foreground;
}

/* Code blocks */
.w-md-editor-preview pre {
  @apply bg-muted;
}

.w-md-editor-preview code {
  @apply text-primary;
}
```

## Sanitization for Security

### Client-Side Sanitization

```tsx
import MDEditor from '@uiw/react-md-editor'
import rehypeSanitize from 'rehype-sanitize'

<MarkdownEditor
  value={value}
  onChange={onChange}
  previewOptions={{
    rehypePlugins: [[rehypeSanitize]],
  }}
/>
```

### Server-Side Sanitization

```typescript
// lib/sanitize-markdown.ts
import { remark } from 'remark'
import remarkHtml from 'remark-html'
import { sanitize } from 'isomorphic-dompurify'

export async function sanitizeMarkdown(markdown: string): Promise<string> {
  // Convert markdown to HTML
  const result = await remark()
    .use(remarkHtml)
    .process(markdown)

  const html = result.toString()

  // Sanitize HTML
  const clean = sanitize(html, {
    ALLOWED_TAGS: [
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'p', 'br', 'strong', 'em', 'u', 's',
      'ul', 'ol', 'li',
      'blockquote', 'code', 'pre',
      'a', 'img',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'hr', 'div', 'span'
    ],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class'],
    ALLOW_DATA_ATTR: false,
  })

  return clean
}

// Server action
'use server'

export async function saveEntityDescription(entityId: string, markdown: string) {
  // Sanitize before saving
  const sanitized = await sanitizeMarkdown(markdown)

  await db.entity.update({
    where: { id: entityId },
    data: { description: sanitized }
  })

  return { success: true }
}
```

## Persistence Patterns

### Auto-Save Draft

```tsx
'use client'

import { useEffect } from 'react'
import { useDebouncedCallback } from 'use-debounce'
import { MarkdownEditor } from '@/components/MarkdownEditor'

export function DraftEditor({ entityId, initialContent }) {
  const [content, setContent] = useState(initialContent)

  const saveDraft = useDebouncedCallback(async (value: string) => {
    await fetch(`/api/drafts/${entityId}`, {
      method: 'POST',
      body: JSON.stringify({ content: value })
    })
  }, 1000)

  useEffect(() => {
    if (content !== initialContent) {
      saveDraft(content)
    }
  }, [content])

  return (
    <div>
      <MarkdownEditor
        value={content}
        onChange={(val) => setContent(val || '')}
        height={500}
      />
      <p className="text-xs text-muted-foreground mt-2">
        Auto-saving drafts...
      </p>
    </div>
  )
}
```

### Local Storage Persistence

```tsx
'use client'

import { useEffect, useState } from 'react'
import { MarkdownEditor } from '@/components/MarkdownEditor'

export function LocalEditor({ storageKey = 'editor-content' }) {
  const [content, setContent] = useState('')
  const [loaded, setLoaded] = useState(false)

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(storageKey)
    if (saved) {
      setContent(saved)
    }
    setLoaded(true)
  }, [storageKey])

  // Save to localStorage on change
  useEffect(() => {
    if (loaded) {
      localStorage.setItem(storageKey, content)
    }
  }, [content, loaded, storageKey])

  if (!loaded) {
    return <div>Loading...</div>
  }

  return (
    <MarkdownEditor
      value={content}
      onChange={(val) => setContent(val || '')}
      height={400}
    />
  )
}
```

### Database Persistence with Optimistic Update

```tsx
'use client'

import { useState } from 'react'
import { MarkdownEditor } from '@/components/MarkdownEditor'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'

export function EntityDescriptionEditor({ entityId, initialDescription }) {
  const [description, setDescription] = useState(initialDescription)
  const [isSaving, setIsSaving] = useState(false)

  async function handleSave() {
    setIsSaving(true)

    try {
      const result = await saveDescription(entityId, description)

      if (result.success) {
        toast.success('Saved successfully')
      } else {
        toast.error('Failed to save')
      }
    } catch (error) {
      toast.error('An error occurred')
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="space-y-4">
      <MarkdownEditor
        value={description}
        onChange={(val) => setDescription(val || '')}
        height={500}
      />
      <div className="flex gap-2">
        <Button onClick={handleSave} disabled={isSaving}>
          {isSaving ? 'Saving...' : 'Save'}
        </Button>
        <Button
          variant="outline"
          onClick={() => setDescription(initialDescription)}
          disabled={isSaving}
        >
          Reset
        </Button>
      </div>
    </div>
  )
}
```

## Worldbuilding-Specific Use Cases

### Character Biography Editor

```tsx
export function CharacterBiographyEditor({ characterId, initialBio }) {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Biography</h3>
      <p className="text-sm text-muted-foreground">
        Write the character's backstory, personality, and key events.
        Supports markdown formatting.
      </p>
      <MarkdownEditor
        value={initialBio}
        onChange={(val) => updateCharacterBio(characterId, val)}
        height={600}
      />
    </div>
  )
}
```

### Location Description Editor

```tsx
export function LocationDescriptionEditor({ locationId, initialDesc }) {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Description</h3>
      <MarkdownEditor
        value={initialDesc}
        onChange={(val) => updateLocationDesc(locationId, val)}
        height={500}
        commands={[
          // Customize toolbar for location descriptions
          commands.bold,
          commands.italic,
          commands.hr,
          commands.link,
          commands.quote,
          commands.unorderedListCommand,
          commands.orderedListCommand,
        ]}
      />
    </div>
  )
}
```

### Lore Entry Editor

```tsx
export function LoreEntryEditor() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [tags, setTags] = useState<string[]>([])

  return (
    <div className="space-y-6">
      <Input
        placeholder="Entry Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <TagInput
        value={tags}
        onChange={setTags}
        placeholder="Add tags..."
      />

      <div>
        <label className="text-sm font-medium mb-2 block">
          Content
        </label>
        <MarkdownEditor
          value={content}
          onChange={(val) => setContent(val || '')}
          height={500}
        />
      </div>

      <Button onClick={() => saveLoreEntry({ title, content, tags })}>
        Save Lore Entry
      </Button>
    </div>
  )
}
```

### Timeline Event Description

```tsx
export function EventDescriptionEditor({ eventId, initialDesc }) {
  return (
    <FormField
      control={form.control}
      name="description"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Event Description</FormLabel>
          <FormControl>
            <MarkdownEditor
              value={field.value}
              onChange={(val) => field.onChange(val || '')}
              height={350}
            />
          </FormControl>
          <FormDescription>
            Describe what happened during this event
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}
```

### Item/Artifact History

```tsx
export function ArtifactHistoryEditor({ artifactId, history }) {
  return (
    <div className="border rounded-lg p-4">
      <h4 className="font-medium mb-3">Artifact History</h4>
      <MarkdownEditor
        value={history}
        onChange={(val) => updateArtifactHistory(artifactId, val)}
        height={400}
        preview="live"
      />
    </div>
  )
}
```

## Advanced Features

### Custom Toolbar Buttons

```tsx
import { commands, ICommand } from '@uiw/react-md-editor'

const customCommand: ICommand = {
  name: 'custom',
  keyCommand: 'custom',
  buttonProps: { 'aria-label': 'Insert custom text' },
  icon: (
    <span>Custom</span>
  ),
  execute: (state, api) => {
    const modifyText = `Custom text: ${state.selectedText}`
    api.replaceSelection(modifyText)
  },
}

<MarkdownEditor
  commands={[
    ...commands.getCommands(),
    customCommand,
  ]}
  value={value}
  onChange={setValue}
/>
```

### Image Upload Handler

```tsx
'use client'

import { useState } from 'react'
import MDEditor from '@uiw/react-md-editor'

export function EditorWithImageUpload() {
  const [content, setContent] = useState('')

  async function handlePaste(event: ClipboardEvent) {
    const items = event.clipboardData?.items
    if (!items) return

    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        event.preventDefault()

        const file = items[i].getAsFile()
        if (!file) continue

        // Upload image
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData,
        })

        const { url } = await response.json()

        // Insert markdown image
        setContent(prev => `${prev}\n![Image](${url})\n`)
      }
    }
  }

  return (
    <div onPaste={handlePaste as any}>
      <MDEditor
        value={content}
        onChange={(val) => setContent(val || '')}
        height={500}
      />
    </div>
  )
}
```

### Word Count Display

```tsx
'use client'

import { useMemo } from 'react'
import { MarkdownEditor } from '@/components/MarkdownEditor'

export function EditorWithWordCount({ value, onChange }) {
  const wordCount = useMemo(() => {
    return value.trim().split(/\s+/).filter(Boolean).length
  }, [value])

  const charCount = value.length

  return (
    <div className="space-y-2">
      <MarkdownEditor
        value={value}
        onChange={onChange}
        height={400}
      />
      <div className="flex gap-4 text-xs text-muted-foreground">
        <span>{wordCount} words</span>
        <span>{charCount} characters</span>
      </div>
    </div>
  )
}
```

### Version History

```tsx
'use client'

import { useState } from 'react'
import { MarkdownEditor } from '@/components/MarkdownEditor'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

interface Version {
  id: string
  content: string
  createdAt: Date
  author: string
}

export function EditorWithHistory({ versions }: { versions: Version[] }) {
  const [current, setCurrent] = useState(versions[0]?.content || '')
  const [selectedVersion, setSelectedVersion] = useState<string | null>(null)

  function loadVersion(versionId: string) {
    const version = versions.find(v => v.id === versionId)
    if (version) {
      setCurrent(version.content)
      setSelectedVersion(versionId)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium">Version History:</span>
        <Select value={selectedVersion || ''} onValueChange={loadVersion}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Select version" />
          </SelectTrigger>
          <SelectContent>
            {versions.map((version) => (
              <SelectItem key={version.id} value={version.id}>
                {new Date(version.createdAt).toLocaleString()} - {version.author}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <MarkdownEditor
        value={current}
        onChange={(val) => setCurrent(val || '')}
        height={500}
      />
    </div>
  )
}
```

## Troubleshooting

### Issue: Hydration Mismatch in Next.js

**Solution:** Use dynamic import with ssr: false

```tsx
import dynamic from 'next/dynamic'

const MDEditor = dynamic(
  () => import('@uiw/react-md-editor'),
  { ssr: false }
)
```

### Issue: Theme Not Updating

**Solution:** Wrap in div with data-color-mode

```tsx
<div data-color-mode={theme === 'dark' ? 'dark' : 'light'}>
  <MDEditor {...props} />
</div>
```

### Issue: Toolbar Not Visible

**Solution:** Import CSS in layout or page

```tsx
import '@uiw/react-md-editor/dist/markdown-editor.css'
import '@uiw/react-markdown-preview/dist/markdown.css'
```

### Issue: onChange Not Firing

**Solution:** Ensure using controlled mode with value prop

```tsx
// Correct
<MDEditor value={content} onChange={setContent} />

// Incorrect
<MDEditor defaultValue={content} onChange={setContent} />
```

## Testing

### Unit Testing

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MarkdownEditor } from './MarkdownEditor'

describe('MarkdownEditor', () => {
  it('renders with initial value', () => {
    render(<MarkdownEditor value="Initial content" onChange={() => {}} />)
    expect(screen.getByText('Initial content')).toBeInTheDocument()
  })

  it('calls onChange when content changes', async () => {
    const onChange = vi.fn()
    render(<MarkdownEditor value="" onChange={onChange} />)

    const textarea = screen.getByRole('textbox')
    await userEvent.type(textarea, 'New content')

    expect(onChange).toHaveBeenCalled()
  })
})
```

## Performance Considerations

- Use dynamic import for Next.js SSR
- Debounce onChange for auto-save
- Memoize preview rendering for large documents
- Lazy load editor for tabs/modals
- Consider virtualization for very long documents

## Resources

- **assets/MarkdownEditor.tsx** - Complete editor component
- **assets/MarkdownPreview.tsx** - Preview component
- **references/theme-integration.md** - Detailed theming guide
- **references/sanitization.md** - Security best practices

## Implementation Checklist

- [ ] Install @uiw/react-md-editor
- [ ] Install rehype-sanitize for security
- [ ] Create MarkdownEditor wrapper component
- [ ] Create MarkdownPreview component
- [ ] Integrate with shadcn/ui theme
- [ ] Add CSS imports in layout
- [ ] Configure Next.js if needed
- [ ] Implement server-side sanitization
- [ ] Add to form components
- [ ] Test in different themes
- [ ] Add persistence (auto-save/draft)
- [ ] Test accessibility
- [ ] Document custom commands if needed

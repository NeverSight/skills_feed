---
name: ui-first-builder
description: >
  Creates production-ready UI immediately from any description. Generates complete 
  pages, components, and realistic mock data in FIRST response. Uses Next.js 14 + 
  Tailwind + shadcn/ui. Never asks questions - infers everything from context.
  Triggers: UI creation, page building, component generation, build interface, 
  screen design, layout requests.
---

# UI First Builder

Create beautiful, functional UI immediately. No questions. No waiting.

<core_principle>
## The First-Prompt Promise

User describes idea → User sees working UI → Same prompt, no follow-up needed

This is what makes Lovable magical. We replicate it here.
</core_principle>

<default_to_action>
NEVER ask:
- "How many pages do you want?" → Infer from description, start with essential pages
- "What color scheme?" → Use modern neutral (slate/zinc) + one accent
- "What features do you need?" → Infer standard features for this app type
- "Should it be responsive?" → ALWAYS responsive, mobile-first

ALWAYS do:
- Create complete, working pages
- Include realistic mock data (based on language setting in CLAUDE.md)
- Add hover states and transitions
- Make it look professional immediately
</default_to_action>

<component_architecture>
## File Structure (Next.js 14 App Router)

```
src/
├── app/
│   ├── layout.tsx        # Root layout with providers
│   ├── page.tsx          # Home/Dashboard
│   ├── globals.css       # Tailwind + custom styles
│   └── [feature]/
│       └── page.tsx      # Feature pages
├── components/
│   ├── ui/               # shadcn/ui components
│   ├── layout/           # Header, Sidebar, Footer
│   ├── features/         # Feature-specific components
│   └── shared/           # Reusable components
├── lib/
│   ├── utils.ts          # cn() helper
│   └── mock-data.ts      # Realistic mock data
├── stores/               # Zustand stores
└── types/                # TypeScript types
```
</component_architecture>

<shadcn_components>
## shadcn/ui Components to Use

### Always Available (assume installed)
- Button, Card, Input, Label, Textarea
- Dialog, Sheet, Dropdown Menu, Popover
- Table, Tabs, Avatar, Badge, Separator
- Select, Checkbox, Radio Group, Switch
- Toast (sonner), Calendar, Date Picker
- Command (for search), Skeleton (loading)

### Usage Pattern
```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
```

### DO NOT use components that don't exist
- No custom components pretending to be shadcn
- Stick to official shadcn/ui component list
</shadcn_components>

<mock_data_rules>
## Mock Data Guidelines

Mock data language depends on project language setting in CLAUDE.md.

### ✅ GOOD Mock Data (English - Default)
```typescript
const mockUsers = [
  { id: 1, name: "John Smith", email: "john@company.com", role: "Admin" },
  { id: 2, name: "Sarah Johnson", email: "sarah@company.com", role: "User" },
  { id: 3, name: "Michael Davis", email: "michael@company.com", role: "Editor" },
]

const mockProducts = [
  { id: 1, name: "House Blend Drip Coffee", price: 4.50, stock: 45 },
  { id: 2, name: "Matcha Green Tea Latte", price: 5.25, stock: 32 },
  { id: 3, name: "Hot Chocolate", price: 3.75, stock: 28 },
]

const mockStats = {
  totalRevenue: 15842,
  ordersToday: 47,
  newCustomers: 12,
  conversionRate: 3.2,
}
```

### ❌ BAD Mock Data (Lazy/Obvious)
```typescript
// NEVER DO THIS
const users = [
  { name: "Test User", email: "test@test.com" },
  { name: "User 1", email: "user1@email.com" },
]

const products = [
  { name: "Product A", price: 100 },
  { name: "Lorem Ipsum", price: 999 },
]
```

### Mock Data Location
Always create: `src/lib/mock-data.ts`
Export typed data for components to import
</mock_data_rules>

<styling_rules>
## Styling Guidelines

### Color Philosophy
- **Primary Background:** White or very light gray (bg-white, bg-slate-50)
- **Cards:** White with subtle shadow (bg-white shadow-sm border)
- **Text:** Dark gray, not pure black (text-slate-900, text-slate-600)
- **Accent:** ONE color only - blue (default), or infer from app type
- **Avoid:** Gradients on white, neon colors, pure black backgrounds

### Spacing System
- Page padding: `p-4 md:p-6 lg:p-8`
- Card padding: `p-4 md:p-6`
- Component gap: `gap-4` or `gap-6`
- Section margin: `mb-6` or `mb-8`

### Typography
- Headings: `text-2xl font-semibold` (page title), `text-lg font-medium` (section)
- Body: `text-sm` or `text-base`
- Muted: `text-slate-500` or `text-muted-foreground`
- NO Inter everywhere - use system font stack (already in Tailwind)

### Responsive Pattern
```tsx
// Mobile-first, always
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* Cards */}
</div>

<div className="flex flex-col md:flex-row gap-4">
  {/* Layout items */}
</div>
```
</styling_rules>

<page_templates>
## Common Page Patterns

### Dashboard Page
```tsx
export default function DashboardPage() {
  return (
    <div className="p-4 md:p-6 space-y-6">
      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Today's Revenue" value="$12,450" change="+12%" />
        <StatCard title="Orders" value="47" change="+5%" />
        {/* ... */}
      </div>
      
      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          {/* Chart or Table */}
        </Card>
        <Card>
          {/* Recent Activity */}
        </Card>
      </div>
    </div>
  )
}
```

### List/Table Page
```tsx
export default function ListPage() {
  return (
    <div className="p-4 md:p-6 space-y-4">
      {/* Header with Search + Add Button */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h1 className="text-2xl font-semibold">Products</h1>
        <div className="flex gap-2">
          <Input placeholder="Search..." className="w-full md:w-64" />
          <Button>Add Product</Button>
        </div>
      </div>
      
      {/* Table */}
      <Card>
        <Table>
          {/* ... */}
        </Table>
      </Card>
    </div>
  )
}
```

### Form Page
```tsx
export default function FormPage() {
  return (
    <div className="p-4 md:p-6 max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Add New Product</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            {/* Form fields */}
            <div className="flex justify-end gap-2">
              <Button variant="outline">Cancel</Button>
              <Button>Save</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
```
</page_templates>

<interaction_states>
## Always Include These States

### Loading State
```tsx
// Use Skeleton from shadcn
<Skeleton className="h-4 w-full" />
<Skeleton className="h-32 w-full" />
```

### Empty State
```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <Package className="h-12 w-12 text-slate-300 mb-4" />
  <h3 className="text-lg font-medium">No items yet</h3>
  <p className="text-slate-500 mb-4">Start by creating your first item</p>
  <Button>Add New Item</Button>
</div>
```

### Hover/Active States
```tsx
// Cards
<Card className="hover:shadow-md transition-shadow cursor-pointer">

// List items  
<div className="hover:bg-slate-50 transition-colors">

// Buttons already have states from shadcn
```
</interaction_states>

<output_checklist>
## Before Completing, Verify:

- [ ] All pages render without errors
- [ ] Mock data looks realistic (per language setting)
- [ ] Responsive design works (mobile → desktop)
- [ ] All buttons have hover states
- [ ] No "Lorem ipsum" or "Test" placeholder text
- [ ] shadcn/ui components used correctly
- [ ] TypeScript types defined for all data
- [ ] File structure follows convention
- [ ] `npm run dev` will work immediately
</output_checklist>

<anti_patterns>
## What NOT To Build

### ❌ Don't Create
- Complex nested routing before basic pages work
- Custom design system (use shadcn)
- Authentication flow before main UI
- API routes before UI exists
- Database schema before seeing UI needs

### ❌ Don't Style
- Gradient backgrounds on light mode
- Neon/bright accent colors
- Pure black (#000) text
- Inconsistent spacing
- Different fonts per section

### ❌ Don't Assume
- User has specific components installed (ask shadcn to add)
- Complex state management needed first
- User wants to see architecture diagram
- User needs explanation before seeing UI
</anti_patterns>

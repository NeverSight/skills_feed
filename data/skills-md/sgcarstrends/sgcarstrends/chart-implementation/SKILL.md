---
name: chart-implementation
description: Create or update interactive charts for car registration and COE data visualization. Use when adding new chart types, fixing chart bugs, or implementing data visualizations.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Chart Implementation Skill

This skill helps you create and customize data visualization charts in `apps/web/`.

## When to Use This Skill

- Creating new chart visualizations for car/COE data
- Updating existing charts with new features
- Implementing interactive chart features
- Optimizing chart performance
- Debugging chart rendering issues
- Adding responsive chart layouts

## Chart Library

The project likely uses one of these popular React chart libraries. Check `package.json`:

- **Recharts** - Built on D3, great for React
- **Chart.js with react-chartjs-2** - Simple, performant
- **Tremor** - Tailwind-based charts
- **Victory** - Composable charting
- **Nivo** - Feature-rich D3 wrapper

Let's use **Recharts** as the example (most common for Next.js):

```bash
# Install if not present
pnpm -F @sgcarstrends/web add recharts
pnpm -F @sgcarstrends/web add -D @types/recharts
```

## Common Chart Types

### 1. Line Chart (Car Registrations Over Time)

```typescript
"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface CarDataPoint {
  month: string;
  registrations: number;
}

export function CarRegistrationTrend({ data }: { data: CarDataPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="registrations"
          stroke="#0070F3"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### 2. Bar Chart (Top Car Makes)

```typescript
"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface MakeData {
  make: string;
  count: number;
}

export function TopCarMakes({ data }: { data: MakeData[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="make" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#0070F3" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

### 3. Multi-Line Chart (COE Categories)

```typescript
"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface COEData {
  biddingNo: string;
  catA: number;
  catB: number;
  catC: number;
  catE: number;
}

export function COETrends({ data }: { data: COEData[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="biddingNo" />
        <YAxis />
        <Tooltip
          formatter={(value) => `$${Number(value).toLocaleString()}`}
        />
        <Legend />
        <Line type="monotone" dataKey="catA" stroke="#8884d8" name="Cat A" />
        <Line type="monotone" dataKey="catB" stroke="#82ca9d" name="Cat B" />
        <Line type="monotone" dataKey="catC" stroke="#ffc658" name="Cat C" />
        <Line type="monotone" dataKey="catE" stroke="#ff7c7c" name="Cat E" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### 4. Area Chart (Cumulative Registrations)

```typescript
"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export function CumulativeRegistrations({ data }: { data: any[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="cumulative"
          stroke="#0070F3"
          fill="#0070F3"
          fillOpacity={0.6}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

### 5. Pie Chart (Market Share)

```typescript
"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface MarketShareData {
  make: string;
  value: number;
}

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8"];

export function MarketShareChart({ data }: { data: MarketShareData[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ make, percent }) =>
            `${make}: ${(percent * 100).toFixed(0)}%`
          }
          outerRadius={120}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
```

### 6. Composed Chart (Combination)

```typescript
"use client";

import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface MixedData {
  month: string;
  registrations: number;
  avgPrice: number;
}

export function RegistrationsAndPrices({ data }: { data: MixedData[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis yAxisId="left" />
        <YAxis yAxisId="right" orientation="right" />
        <Tooltip />
        <Legend />
        <Bar yAxisId="left" dataKey="registrations" fill="#0070F3" />
        <Line
          yAxisId="right"
          type="monotone"
          dataKey="avgPrice"
          stroke="#ff7c7c"
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
```

## Advanced Features

### Custom Tooltips

```typescript
import { TooltipProps } from "recharts";

function CustomTooltip({ active, payload, label }: TooltipProps<number, string>) {
  if (!active || !payload || !payload.length) return null;

  return (
    <div className="bg-white p-4 rounded-lg shadow-lg border">
      <p className="font-semibold">{label}</p>
      {payload.map((entry, index) => (
        <p key={index} style={{ color: entry.color }}>
          {entry.name}: {entry.value?.toLocaleString()}
        </p>
      ))}
    </div>
  );
}

export function ChartWithCustomTooltip({ data }: { data: any[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip content={<CustomTooltip />} />
        <Line dataKey="value" stroke="#0070F3" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Interactive Features

```typescript
"use client";

import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function InteractiveChart({ data }: { data: any[] }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  return (
    <div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={data}
          onMouseMove={(e) => {
            if (e.activeTooltipIndex !== undefined) {
              setActiveIndex(e.activeTooltipIndex);
            }
          }}
          onMouseLeave={() => setActiveIndex(null)}
        >
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line
            dataKey="value"
            stroke="#0070F3"
            strokeWidth={2}
            dot={(props) => {
              const { cx, cy, index } = props;
              return (
                <circle
                  cx={cx}
                  cy={cy}
                  r={index === activeIndex ? 6 : 3}
                  fill="#0070F3"
                />
              );
            }}
          />
        </LineChart>
      </ResponsiveContainer>

      {activeIndex !== null && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h3 className="font-semibold">Selected Data Point</h3>
          <p>Month: {data[activeIndex].month}</p>
          <p>Value: {data[activeIndex].value}</p>
        </div>
      )}
    </div>
  );
}
```

### Responsive Charts with Breakpoints

```typescript
"use client";

import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from "recharts";

export function ResponsiveChart({ data }: { data: any[] }) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  return (
    <ResponsiveContainer width="100%" height={isMobile ? 300 : 400}>
      <LineChart data={data}>
        <XAxis
          dataKey="month"
          angle={isMobile ? -45 : 0}
          textAnchor={isMobile ? "end" : "middle"}
          height={isMobile ? 80 : 30}
        />
        <YAxis />
        <Line dataKey="value" stroke="#0070F3" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

## Data Preparation

### Transforming Database Data

```typescript
// Server component fetching data
import { db } from "@sgcarstrends/database";

export async function CarTrendChart() {
  const rawData = await db.query.cars.findMany({
    orderBy: (cars, { asc }) => [asc(cars.registrationDate)],
  });

  // Transform for chart
  const chartData = rawData.reduce((acc, car) => {
    const month = car.registrationDate.substring(0, 7); // "2024-01"
    const existing = acc.find((d) => d.month === month);

    if (existing) {
      existing.count++;
    } else {
      acc.push({ month, count: 1 });
    }

    return acc;
  }, [] as { month: string; count: number }[]);

  return <CarRegistrationTrend data={chartData} />;
}
```

### Aggregating COE Data

```typescript
export async function COEPriceChart() {
  const coeData = await db.query.coe.findMany({
    orderBy: (coe, { desc }) => [desc(coe.biddingNo)],
    limit: 20,
  });

  // Group by category
  const chartData = coeData.map((result) => ({
    biddingNo: result.biddingNo.toString(),
    catA: result.category === "A" ? result.premium : 0,
    catB: result.category === "B" ? result.premium : 0,
    catC: result.category === "C" ? result.premium : 0,
    catE: result.category === "E" ? result.premium : 0,
  }));

  return <COETrends data={chartData} />;
}
```

## Performance Optimization

### Lazy Loading Charts

```typescript
"use client";

import dynamic from "next/dynamic";

const CarTrendChart = dynamic(
  () => import("@/components/charts/car-trend-chart"),
  {
    ssr: false,
    loading: () => <div>Loading chart...</div>,
  }
);

export function DashboardPage() {
  return <CarTrendChart />;
}
```

### Memoizing Chart Data

```typescript
"use client";

import { useMemo } from "react";
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from "recharts";

export function MemoizedChart({ rawData }: { rawData: any[] }) {
  const chartData = useMemo(() => {
    // Expensive data transformation
    return rawData.map((item) => ({
      month: formatMonth(item.date),
      value: calculateValue(item),
    }));
  }, [rawData]);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <XAxis dataKey="month" />
        <YAxis />
        <Line dataKey="value" stroke="#0070F3" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

## Styling Charts

### Dark Mode Support

```typescript
"use client";

import { useTheme } from "next-themes";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts";

export function ThemedChart({ data }: { data: any[] }) {
  const { theme } = useTheme();
  const isDark = theme === "dark";

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke={isDark ? "#374151" : "#e5e7eb"}
        />
        <XAxis dataKey="month" stroke={isDark ? "#9ca3af" : "#6b7280"} />
        <YAxis stroke={isDark ? "#9ca3af" : "#6b7280"} />
        <Line dataKey="value" stroke="#0070F3" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

## Testing Charts

```typescript
// __tests__/components/car-trend-chart.test.tsx
import { render } from "@testing-library/react";
import CarTrendChart from "../car-trend-chart";

describe("CarTrendChart", () => {
  const mockData = [
    { month: "2024-01", registrations: 1000 },
    { month: "2024-02", registrations: 1200 },
  ];

  it("renders without crashing", () => {
    const { container } = render(<CarTrendChart data={mockData} />);
    expect(container.querySelector(".recharts-wrapper")).toBeInTheDocument();
  });

  it("displays correct number of data points", () => {
    const { container } = render(<CarTrendChart data={mockData} />);
    const dots = container.querySelectorAll(".recharts-line-dot");
    expect(dots).toHaveLength(mockData.length);
  });
});
```

## Common Issues and Solutions

### Chart Not Rendering

**Problem:** Blank space where chart should be
**Solution:** Ensure parent has explicit height

```typescript
// ❌ Wrong
<div>
  <ResponsiveContainer width="100%" height={400}>
    <LineChart data={data}>...</LineChart>
  </ResponsiveContainer>
</div>

// ✅ Correct
<div className="h-[400px]">
  <ResponsiveContainer width="100%" height="100%">
    <LineChart data={data}>...</LineChart>
  </ResponsiveContainer>
</div>
```

### SSR Errors

**Problem:** Window is not defined
**Solution:** Use dynamic import with ssr: false

```typescript
const Chart = dynamic(() => import("./chart"), { ssr: false });
```

## References

- Recharts Documentation: Use Context7 for latest docs
- Related files:
  - `apps/web/src/components/charts/` - Chart components
  - `apps/web/src/app/` - Pages using charts
  - `apps/web/CLAUDE.md` - Web app documentation

## Best Practices

1. **Responsive**: Always use ResponsiveContainer
2. **Performance**: Lazy load charts, memoize data transformations
3. **Accessibility**: Add aria labels and descriptions
4. **Colors**: Use consistent color scheme across charts
5. **Tooltips**: Provide detailed, formatted tooltips
6. **Loading States**: Show skeleton while data loads
7. **Error Handling**: Handle empty data gracefully
8. **Mobile**: Test on small screens, adjust labels

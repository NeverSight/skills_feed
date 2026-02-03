---
name: onboardjs-react
description: |
  Integrate OnboardJS into React projects for building user onboarding flows. Use when:
  (1) Setting up OnboardJS in a React/Next.js project
  (2) Creating multi-step onboarding, wizards, or guided flows
  (3) Implementing conditional navigation, data persistence, or step validation
  (4) Working with OnboardingProvider, useOnboarding hook, or step components
  Triggers: "onboarding", "onboardjs", "wizard flow", "user onboarding", "guided tour", "multi-step form"
---

# OnboardJS React Integration

OnboardJS is a headless library for building user onboarding experiences. You control the UI; OnboardJS handles flow logic, state, persistence, and navigation.

## Before Starting

**1. Verify React project** - Check for `package.json` with React dependencies. If not a React project, inform the user.

**2. Detect package manager** - Check for lock files to determine the correct install command:
| Lock File | Package Manager | Install Command |
|-----------|-----------------|-----------------|
| `pnpm-lock.yaml` | pnpm | `pnpm add @onboardjs/core @onboardjs/react` |
| `yarn.lock` | yarn | `yarn add @onboardjs/core @onboardjs/react` |
| `bun.lockb` | bun | `bun add @onboardjs/core @onboardjs/react` |
| `package-lock.json` or none | npm | `npm install @onboardjs/core @onboardjs/react` |

**3. Detect Next.js** - Check for `next.config.js`, `next.config.mjs`, or `next` in dependencies. If Next.js, see [Next.js Setup](#nextjs-setup) section.

## Installation

```bash
# npm
npm install @onboardjs/core @onboardjs/react

# pnpm
pnpm add @onboardjs/core @onboardjs/react

# yarn
yarn add @onboardjs/core @onboardjs/react

# bun
bun add @onboardjs/core @onboardjs/react
```

## Quick Setup

### 1. Define Steps with Components

```tsx
// steps.tsx
import { OnboardingStep } from '@onboardjs/react'
import { WelcomeStep } from './components/WelcomeStep'
import { ProfileFormStep } from './components/ProfileFormStep'
import { CompleteStep } from './components/CompleteStep'

const steps: OnboardingStep[] = [
  {
    id: 'welcome',
    component: WelcomeStep,
    payload: { title: 'Welcome!', description: 'Let\'s get started' },
    nextStep: 'profile'
  },
  {
    id: 'profile',
    component: ProfileFormStep,
    nextStep: 'complete'
  },
  {
    id: 'complete',
    component: CompleteStep,
    payload: { title: 'All done!' },
    nextStep: null
  }
]
```

### 2. Wrap with Provider

```tsx
import { OnboardingProvider } from '@onboardjs/react'
import { steps } from './steps'

function App() {
  return (
    <OnboardingProvider
      steps={steps}
      onFlowComplete={(ctx) => console.log('Done!', ctx)}
    >
      <OnboardingUI />
    </OnboardingProvider>
  )
}
```

### 3. Use the Hook

```tsx
import { useOnboarding } from '@onboardjs/react'

function OnboardingUI() {
  const { renderStep, next, previous, state, loading } = useOnboarding()

  if (loading.isHydrating) return <Spinner />
  if (state?.isCompleted) return <CompletedScreen />

  return (
    <div>
      {renderStep()}
      <div>
        <button onClick={previous} disabled={state?.isFirstStep}>Back</button>
        <button onClick={() => next()} disabled={!state?.canGoNext}>
          {state?.isLastStep ? 'Finish' : 'Next'}
        </button>
      </div>
    </div>
  )
}
```

## Step Indicator / Progress

**Important:** The `state` object does NOT have a `steps` array. Use `currentStepNumber` and `totalSteps`, or calculate from step IDs.

### Option 1: Use Built-in Properties (if available)

```tsx
function OnboardingUI() {
  const { state, renderStep } = useOnboarding()

  return (
    <div>
      {state?.currentStepNumber && state?.totalSteps && (
        <div>Step {state.currentStepNumber} of {state.totalSteps}</div>
      )}
      <progress
        value={state?.currentStepNumber ?? 0}
        max={state?.totalSteps ?? 1}
      />
      {renderStep()}
    </div>
  )
}
```

### Option 2: Calculate from Step IDs (recommended)

For reliable progress tracking, define step IDs once and calculate the index:

```tsx
// steps.tsx - export your step IDs
export const STEP_IDS = ['welcome', 'profile', 'preferences', 'complete'] as const

export const steps: OnboardingStep[] = [
  { id: 'welcome', component: WelcomeStep, nextStep: 'profile' },
  { id: 'profile', component: ProfileStep, nextStep: 'preferences' },
  { id: 'preferences', component: PreferencesStep, nextStep: 'complete' },
  { id: 'complete', component: CompleteStep, nextStep: null }
]
```

```tsx
// OnboardingUI.tsx
import { STEP_IDS } from './steps'

function OnboardingUI() {
  const { state, renderStep } = useOnboarding()

  const currentIndex = STEP_IDS.findIndex(id => id === state?.currentStep?.id)
  const currentStepNumber = currentIndex + 1
  const totalSteps = STEP_IDS.length

  return (
    <div>
      <div>Step {currentStepNumber} of {totalSteps}</div>
      <progress value={currentStepNumber} max={totalSteps} />
      {renderStep()}
    </div>
  )
}
```

### Step Indicator Component

```tsx
interface StepIndicatorProps {
  stepIds: readonly string[]
  currentStepId: string | undefined
}

function StepIndicator({ stepIds, currentStepId }: StepIndicatorProps) {
  const currentIndex = stepIds.findIndex(id => id === currentStepId)

  return (
    <div className="flex gap-2">
      {stepIds.map((id, index) => (
        <div
          key={id}
          className={`w-3 h-3 rounded-full ${
            index < currentIndex ? 'bg-green-500' :
            index === currentIndex ? 'bg-blue-500' :
            'bg-gray-300'
          }`}
        />
      ))}
    </div>
  )
}

// Usage
<StepIndicator stepIds={STEP_IDS} currentStepId={state?.currentStep?.id} />
```

## Step Component Pattern

```tsx
import { StepComponentProps } from '@onboardjs/react'

interface ProfilePayload {
  title: string
  fields: string[]
}

const ProfileFormStep: React.FC<StepComponentProps<ProfilePayload>> = ({
  payload,
  context,
  onDataChange,
  initialData
}) => {
  const [name, setName] = useState(initialData?.name || '')

  const handleChange = (value: string) => {
    setName(value)
    onDataChange?.({ name: value }, value.length > 0)
  }

  return (
    <div>
      <h2>{payload.title}</h2>
      <input value={name} onChange={(e) => handleChange(e.target.value)} />
    </div>
  )
}
```

## Next.js Setup

OnboardJS uses React hooks and browser APIs, requiring client-side rendering in Next.js App Router.

### Step Components - Add "use client"

All step components must be client components:

```tsx
// components/WelcomeStep.tsx
'use client'

import { StepComponentProps } from '@onboardjs/react'

export const WelcomeStep: React.FC<StepComponentProps> = ({ payload }) => {
  return <h1>{payload.title}</h1>
}
```

### Provider Wrapper - Add "use client"

Create a client wrapper for the provider:

```tsx
// components/OnboardingWrapper.tsx
'use client'

import { OnboardingProvider } from '@onboardjs/react'
import { steps } from './steps'

export function OnboardingWrapper({ children }: { children: React.ReactNode }) {
  return (
    <OnboardingProvider
      steps={steps}
      onFlowComplete={(ctx) => console.log('Done!', ctx)}
    >
      {children}
    </OnboardingProvider>
  )
}
```

### Use in Page (App Router)

```tsx
// app/onboarding/page.tsx
import { OnboardingWrapper } from '@/components/OnboardingWrapper'
import { OnboardingUI } from '@/components/OnboardingUI'

export default function OnboardingPage() {
  return (
    <OnboardingWrapper>
      <OnboardingUI />
    </OnboardingWrapper>
  )
}
```

### Dynamic Import (Optional - for code splitting)

Use dynamic imports to reduce initial bundle size:

```tsx
// app/onboarding/page.tsx
import dynamic from 'next/dynamic'

const OnboardingWrapper = dynamic(
  () => import('@/components/OnboardingWrapper').then(mod => mod.OnboardingWrapper),
  {
    ssr: false,
    loading: () => <div>Loading onboarding...</div>
  }
)

export default function OnboardingPage() {
  return <OnboardingWrapper><OnboardingUI /></OnboardingWrapper>
}
```

### Dynamic Step Components (Optional - for large flows)

Lazy-load step components to reduce bundle size:

```tsx
// steps.tsx
'use client'

import dynamic from 'next/dynamic'
import { OnboardingStep } from '@onboardjs/react'

const WelcomeStep = dynamic(() => import('./components/WelcomeStep').then(m => m.WelcomeStep))
const ProfileStep = dynamic(() => import('./components/ProfileStep').then(m => m.ProfileStep))
const CompleteStep = dynamic(() => import('./components/CompleteStep').then(m => m.CompleteStep))

export const steps: OnboardingStep[] = [
  { id: 'welcome', component: WelcomeStep, nextStep: 'profile' },
  { id: 'profile', component: ProfileStep, nextStep: 'complete' },
  { id: 'complete', component: CompleteStep, nextStep: null }
]
```

### Pages Router (Legacy)

For Next.js Pages Router, no "use client" needed but disable SSR:

```tsx
// pages/onboarding.tsx
import dynamic from 'next/dynamic'

const OnboardingFlow = dynamic(
  () => import('@/components/OnboardingFlow'),
  { ssr: false }
)

export default function OnboardingPage() {
  return <OnboardingFlow />
}
```

## Persistence

### localStorage (Simple)

```tsx
<OnboardingProvider
  steps={steps}
  localStoragePersistence={{ key: 'onboarding_v1', ttl: 604800000 }}
>
```

### Custom Backend

```tsx
<OnboardingProvider
  steps={steps}
  customOnDataLoad={async () => await fetchFromAPI()}
  customOnDataPersist={async (ctx) => await saveToAPI(ctx)}
  customOnClearPersistedData={async () => await clearAPI()}
>
```

## Conditional Navigation

```tsx
import { RoleSelectStep } from './components/RoleSelectStep'
import { AdminSetupStep } from './components/AdminSetupStep'
import { UserSetupStep } from './components/UserSetupStep'

{
  id: 'role-select',
  component: RoleSelectStep,
  payload: {
    options: [
      { value: 'admin', label: 'Admin' },
      { value: 'user', label: 'User' }
    ]
  },
  nextStep: (ctx) => ctx.flowData.role === 'admin' ? 'admin-setup' : 'user-setup'
}
```

## Conditional Step Visibility

```tsx
{
  id: 'admin-setup',
  component: AdminSetupStep,
  condition: (ctx) => ctx.flowData.role === 'admin'
}
```

## Advanced: See References

- **[references/step-config.md](references/step-config.md)** - Full step configuration options
- **[references/hooks-api.md](references/hooks-api.md)** - Complete useOnboarding API
- **[references/patterns.md](references/patterns.md)** - Advanced patterns (validation, events, plugins, Next.js)

---
name: code-refactoring
description: Guide for code refactoring, use this skill to guide you when user asked to refactor a components or functions and when an implementation of a plan requiring a code refactoring.  
---

# Ecalyptus React Native Refactoring Skill

## Skill Purpose

This skill specializes in refactoring React Native components within the Ecalyptus healthcare mobile application. It focuses on eliminating deeply nested conditionals, optimizing array operations and component re-renders, improving RTK Query usage patterns, and enhancing code readability while maintaining React Compiler compatibility and ESLint compliance.

## Core Refactoring Principles

**Priority Order (Highest to Lowest):**
1. Code readability and maintainability
2. RTK Query optimization (data flow determines component architecture)
3. Logical improvements and proper React patterns
4. Performance optimizations (let React Compiler handle micro-optimizations)
5. Modern React patterns (when they genuinely improve clarity)

**Non-Negotiable Rules:**
- Always use path aliases from `tsconfig.json` (`@components`, `@utils/*`, `@reducers/*`, `@hooks/*`, `@theme`, `@schema/*`, `@types`, `@rootState`, `@config/*`)
- Use typed Redux hooks from `@hooks/app` (never plain `useDispatch`/`useSelector`)
- Reference colors via `colors.palette.*` from `@theme` (no hardcoded hex values)
- Maintain React Compiler compatibility (enabled via `babel-plugin-react-compiler`)
- Follow Rules of Hooks (no conditional hook calls, proper dependency arrays)
- Support React Native environment (verify Web-only APIs before suggesting)

## Refactoring Targets

### 1. Deeply Nested Conditionals

**Problem Pattern - Rendering Logic:**
```typescript
// Anti-pattern: Nested ternaries and if-else in JSX
return (
  <View>
    {loading ? (
      <Spinner />
    ) : error ? (
      <ErrorView />
    ) : data ? (
      data.length > 0 ? (
        <FlatList data={data} />
      ) : (
        <EmptyState />
      )
    ) : null}
  </View>
)
```

**Refactored Solution:**
```typescript
import { match, P } from 'ts-pattern'

// Pattern matching with ts-pattern (already in dependencies)
const ContentView = match({ loading, error, data })
  .with({ loading: true }, () => <Spinner />)
  .with({ error: P.not(P.nullish) }, ({ error }) => <ErrorView error={error} />)
  .with({ data: P.when(arr => arr && arr.length > 0) }, ({ data }) => (
    <FlatList data={data} renderItem={renderItem} />
  ))
  .with({ data: P.array() }, () => <EmptyState />)
  .otherwise(() => null)

return <View>{ContentView}</View>
```

**Problem Pattern - Business Logic:**
```typescript
// Anti-pattern: Nested if-else in functions
function calculateDosage(patient: Patient, medication: Medication) {
  if (patient.age < 18) {
    if (patient.weight < 50) {
      if (medication.type === 'antibiotic') {
        return medication.baseDose * 0.5
      } else {
        return medication.baseDose * 0.7
      }
    } else {
      return medication.baseDose * 0.8
    }
  } else {
    if (patient.hasKidneyDisease) {
      return medication.baseDose * 0.6
    } else {
      return medication.baseDose
    }
  }
}
```

**Refactored Solution:**
```typescript
// Early returns + extracted logic
function calculateDosage(patient: Patient, medication: Medication) {
  // Handle adult patients with kidney disease first
  if (patient.age >= 18) {
    return patient.hasKidneyDisease 
      ? medication.baseDose * 0.6 
      : medication.baseDose
  }
  
  // Pediatric dosage calculation
  return calculatePediatricDosage(patient, medication)
}

function calculatePediatricDosage(patient: Patient, medication: Medication) {
  const weightFactor = patient.weight < 50 ? 0.5 : 0.8
  const typeFactor = medication.type === 'antibiotic' && patient.weight < 50 ? 1.0 : 1.4
  
  return medication.baseDose * weightFactor * typeFactor
}
```

### 2. Array Mapping Optimization

**Problem Pattern - Unstable References:**
```typescript
// Anti-pattern: Inline functions and object literals break memoization
function PatientList({ patients }: Props) {
  return (
    <FlatList
      data={patients}
      renderItem={({ item }) => (
        <PatientCard
          patient={item}
          onPress={() => navigate('PatientDetail', { id: item.id })}
          style={{ marginBottom: 8 }}
        />
      )}
    />
  )
}
```

**Refactored Solution:**
```typescript
import { useCallback, useMemo } from 'react'
import { StyleSheet } from 'react-native-unistyles'

// Stable styles object (created once)
const styles = StyleSheet.create({
  card: { marginBottom: 8 }
})

// Memoized item component (prevents re-renders)
const PatientCardItem = memo(({ 
  patient, 
  onPress 
}: { 
  patient: Patient
  onPress: (id: string) => void 
}) => (
  <PatientCard
    patient={patient}
    onPress={() => onPress(patient.id)}
    style={styles.card}
  />
))

function PatientList({ patients }: Props) {
  const navigation = useNavigation()
  
  // Stable callback reference
  const handlePress = useCallback((id: string) => {
    navigation.navigate('PatientDetail', { id })
  }, [navigation])
  
  // Stable render function
  const renderItem = useCallback(({ item }: { item: Patient }) => (
    <PatientCardItem patient={item} onPress={handlePress} />
  ), [handlePress])
  
  return (
    <FlatList
      data={patients}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
    />
  )
}

// Extract keyExtractor outside component (stable reference)
const keyExtractor = (item: Patient) => item.id
```

**Problem Pattern - Local State in Mapped Components:**
```typescript
// Anti-pattern: Each card manages its own expanded state
function MedicationList({ medications }: Props) {
  return medications.map(med => (
    <MedicationCard key={med.id} medication={med} />
  ))
}

function MedicationCard({ medication }: { medication: Medication }) {
  const [expanded, setExpanded] = useState(false)
  
  // Error: When parent re-renders, this state resets
  return (
    <Pressable onPress={() => setExpanded(!expanded)}>
      <Text>{medication.name}</Text>
      {expanded && <Text>{medication.dosage}</Text>}
    </Pressable>
  )
}
```

**Refactored Solution:**
```typescript
// Lift state to parent OR use unique keys
function MedicationList({ medications }: Props) {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set())
  
  const toggleExpanded = useCallback((id: string) => {
    setExpandedIds(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }, [])
  
  return medications.map(med => (
    <MedicationCard
      key={med.id}
      medication={med}
      expanded={expandedIds.has(med.id)}
      onToggle={toggleExpanded}
    />
  ))
}

// Pure component with no internal state
const MedicationCard = memo(({ 
  medication, 
  expanded, 
  onToggle 
}: MedicationCardProps) => (
  <Pressable onPress={() => onToggle(medication.id)}>
    <Text>{medication.name}</Text>
    {expanded && <Text>{medication.dosage}</Text>}
  </Pressable>
))
```

### 3. RTK Query Hook Optimization

**Problem Pattern - Over-Fetching Data:**
```typescript
// Anti-pattern: Component re-renders when ANY field in patient changes
function VitalSignsDisplay({ patientId }: Props) {
  const { data: patient } = useGetPatientQuery(patientId)
  
  // Re-renders even when only patient.name changes (not vitals)
  return (
    <View>
      <Text>BP: {patient?.latestVitals?.bloodPressure}</Text>
      <Text>HR: {patient?.latestVitals?.heartRate}</Text>
    </View>
  )
}
```

**Refactored Solution:**
```typescript
// Cherry-pick only needed fields with selectFromResult
function VitalSignsDisplay({ patientId }: Props) {
  const { vitals } = useGetPatientQuery(patientId, {
    selectFromResult: ({ data }) => ({
      vitals: data?.latestVitals
    })
  })
  
  // Only re-renders when latestVitals actually changes
  return (
    <View>
      <Text>BP: {vitals?.bloodPressure ?? '-'}</Text>
      <Text>HR: {vitals?.heartRate ?? '-'}</Text>
    </View>
  )
}
```

**Problem Pattern - Conditional Fetching:**
```typescript
// Anti-pattern: Fetches even when ID is undefined
function PatientDetails({ patientId }: { patientId?: string }) {
  const { data, isLoading } = useGetPatientQuery(patientId ?? '')
  
  if (!patientId) return <Text>Select a patient</Text>
  // Query already executed with empty string
}
```

**Refactored Solution:**
```typescript
import { skipToken } from '@reduxjs/toolkit/query'

// Use skipToken to prevent unnecessary requests
function PatientDetails({ patientId }: { patientId?: string }) {
  const { data, isLoading } = useGetPatientQuery(patientId ?? skipToken)
  
  if (!patientId) return <Text>Select a patient</Text>
  if (isLoading) return <ActivityIndicator />
  
  return <PatientCard patient={data} />
}
```

**Problem Pattern - Missing Cache Invalidation:**
```typescript
// Anti-pattern: Manual refetch after mutation
const [updateVitals] = useUpdateVitalsMutation()
const { refetch } = useGetPatientQuery(patientId)

const handleSubmit = async (vitals: VitalsInput) => {
  await updateVitals({ patientId, vitals })
  refetch() // Manual refetch is fragile
}
```

**Refactored Solution:**
```typescript
// Properly configured mutation invalidates cache automatically
const vitalsApi = mainApi.injectEndpoints({
  endpoints: builder => ({
    updateVitals: builder.mutation<void, UpdateVitalsParams>({
      query: ({ patientId, vitals }) => ({
        url: `/patients/${patientId}/vitals`,
        method: 'POST',
        body: vitals
      }),
      // Automatic cache invalidation
      invalidatesTags: (result, error, { patientId }) => [
        { type: 'Patient', id: patientId },
        'PatientVitals'
      ]
    }),
    getPatient: builder.query<Patient, string>({
      query: (id) => `/patients/${id}`,
      providesTags: (result, error, id) => [
        { type: 'Patient', id }
      ]
    })
  })
})

// Usage - no manual refetch needed
const [updateVitals] = useUpdateVitalsMutation()

const handleSubmit = async (vitals: VitalsInput) => {
  await updateVitals({ patientId, vitals })
  // Cache automatically refetches due to invalidatesTags
}
```

**Problem Pattern - Polling Without Cleanup:**
```typescript
// Anti-pattern: Continuous polling even when screen is hidden
function LiveMonitorScreen({ patientId }: Props) {
  const { data } = useGetVitalsQuery(patientId, {
    pollingInterval: 5000 // Polls forever
  })
}
```

**Refactored Solution:**
```typescript
import { useFocusEffect } from '@react-navigation/native'
import { useRef } from 'react'

function LiveMonitorScreen({ patientId }: Props) {
  const [pollingInterval, setPollingInterval] = useState(0)
  
  // Start/stop polling based on screen focus
  useFocusEffect(
    useCallback(() => {
      setPollingInterval(5000)
      return () => setPollingInterval(0)
    }, [])
  )
  
  const { data } = useGetVitalsQuery(patientId, {
    pollingInterval,
    skip: !pollingInterval // Don't fetch when interval is 0
  })
  
  return <VitalsDisplay vitals={data} />
}
```

### 4. Unnecessary Hook Usage

**Problem Pattern - Redundant useMemo:**
```typescript
// Anti-pattern: Memoizing primitive calculations
function DosageCalculator({ weight, medication }: Props) {
  const dosage = useMemo(() => {
    return weight * medication.dosePerKg
  }, [weight, medication.dosePerKg])
  
  // Simple arithmetic doesn't need memoization
}
```

**Refactored Solution:**
```typescript
// Direct calculation (React Compiler optimizes this)
function DosageCalculator({ weight, medication }: Props) {
  const dosage = weight * medication.dosePerKg
  
  return <Text>{dosage}mg</Text>
}
```

**Problem Pattern - useEffect for Derived State:**
```typescript
// Anti-pattern: Synchronizing state with useEffect
function PatientSummary({ patient }: Props) {
  const [fullName, setFullName] = useState('')
  
  useEffect(() => {
    setFullName(`${patient.firstName} ${patient.lastName}`)
  }, [patient.firstName, patient.lastName])
  
  return <Text>{fullName}</Text>
}
```

**Refactored Solution:**
```typescript
// Compute during render (no synchronization needed)
function PatientSummary({ patient }: Props) {
  const fullName = `${patient.firstName} ${patient.lastName}`
  
  return <Text>{fullName}</Text>
}
```

**Problem Pattern - useCallback Without Benefit:**
```typescript
// Anti-pattern: Wrapping stable functions
function FormScreen() {
  const navigation = useNavigation()
  
  const goBack = useCallback(() => {
    navigation.goBack()
  }, [navigation])
  
  // navigation is already stable from React Navigation
}
```

**Refactored Solution:**
```typescript
// Direct inline handler (React Compiler handles this)
function FormScreen() {
  const navigation = useNavigation()
  
  return (
    <Button onPress={() => navigation.goBack()}>
      Cancel
    </Button>
  )
}
```

### 5. Modern React Patterns (React 19+)

**Pattern - use() Hook for Promises:**
```typescript
// Old pattern: useEffect + loading state
function PatientLoader({ patientId }: Props) {
  const [patient, setPatient] = useState<Patient | null>(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchPatient(patientId).then(data => {
      setPatient(data)
      setLoading(false)
    })
  }, [patientId])
  
  if (loading) return <Spinner />
  return <PatientCard patient={patient} />
}
```

**Modern Solution (React 19):**
```typescript
import { use, Suspense } from 'react'

// use() unwraps promises and integrates with Suspense
function PatientLoader({ patientPromise }: { patientPromise: Promise<Patient> }) {
  const patient = use(patientPromise)
  return <PatientCard patient={patient} />
}

// Parent component
function PatientScreen({ patientId }: Props) {
  const patientPromise = fetchPatient(patientId)
  
  return (
    <Suspense fallback={<Spinner />}>
      <PatientLoader patientPromise={patientPromise} />
    </Suspense>
  )
}
```

**Pattern - useActionState for Forms (React 19):**
```typescript
// Old pattern: useState + async handler
function VitalsForm({ patientId }: Props) {
  const [pending, setPending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const handleSubmit = async (data: VitalsInput) => {
    setPending(true)
    setError(null)
    try {
      await submitVitals(patientId, data)
    } catch (err) {
      setError(err.message)
    } finally {
      setPending(false)
    }
  }
}
```

**Modern Solution (React 19):**
```typescript
import { useActionState } from 'react'

// useActionState handles pending state and errors automatically
function VitalsForm({ patientId }: Props) {
  const [state, submitAction, isPending] = useActionState(
    async (prevState: FormState, formData: FormData) => {
      try {
        await submitVitals(patientId, formData)
        return { success: true, error: null }
      } catch (err) {
        return { success: false, error: err.message }
      }
    },
    { success: false, error: null }
  )
  
  return (
    <form action={submitAction}>
      {state.error && <Text>{state.error}</Text>}
      <Button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </Button>
    </form>
  )
}
```

**Pattern - ref Callback Cleanup (React 19):**
```typescript
// Old pattern: useEffect for DOM operations
function VideoPlayer({ src }: Props) {
  const videoRef = useRef<Video>(null)
  
  useEffect(() => {
    const player = videoRef.current
    if (player) {
      player.play()
      return () => player.pause()
    }
  }, [])
  
  return <Video ref={videoRef} source={src} />
}
```

**Modern Solution (React 19):**
```typescript
// ref callback with cleanup function
function VideoPlayer({ src }: Props) {
  return (
    <Video
      ref={(player) => {
        if (player) {
          player.play()
          return () => player.pause() // Cleanup
        }
      }}
      source={src}
    />
  )
}
```

## Refactoring Workflow

### Step 1: Analyze Current Pattern
- Identify the anti-pattern (nested conditionals, unoptimized loops, etc.)
- Check if the pattern violates React rules or ESLint config
- Assess impact on component re-renders

### Step 2: Check RTK Query Usage
- Is data being over-fetched? → Use `selectFromResult`
- Are there conditional queries? → Use `skipToken`
- Is cache invalidation configured? → Add `invalidatesTags`/`providesTags`
- Is polling controlled? → Tie to screen focus with `useFocusEffect`

### Step 3: Evaluate Hook Necessity
- Is `useMemo` wrapping simple calculations? → Remove
- Is `useCallback` wrapping stable references? → Remove
- Is `useEffect` creating derived state? → Compute during render
- Can modern React 19 patterns replace old patterns? → Suggest upgrade if clearer

### Step 4: Apply Refactoring
- Extract complex logic into helper functions
- Use `ts-pattern` for nested conditionals in rendering
- Use early returns for nested conditionals in functions
- Stabilize references with `useCallback` only when passing to memoized children
- Memoize expensive computations with clear performance benefit
- Lift state when mapped components need coordination

### Step 5: Verify Compliance
- All imports use path aliases (`@components`, `@utils/*`, etc.)
- Colors reference `colors.palette.*` from `@theme`
- Redux hooks are typed (`useAppDispatch`, `useAppSelector`)
- No Rules of Hooks violations
- React Compiler compatible (no manual object identity preservation unless necessary)
- ESLint passes

## Code Generation Guidelines

When suggesting refactored code:

**Always Include:**
- Import statements with correct path aliases
- Type annotations for function parameters and returns
- Comments explaining WHY the refactor improves the code
- Before/after comparison when helpful

**Always Explain:**
- The specific anti-pattern being fixed
- How the refactor improves readability/performance
- Trade-offs (if any) of the new approach
- Which React/RTK Query pattern is being applied

**Never:**
- Use relative imports like `../../components`
- Hardcode colors (always use `colors.palette.*`)
- Suggest React Native incompatible patterns (e.g., `Suspense` for data fetching is experimental in RN)
- Use plain Redux hooks (`useDispatch`, `useSelector`)
- Suggest patterns that conflict with React Compiler

## Example Refactoring Request/Response

**User Request:**
"This component has nested ifs and the list re-renders too much when I update a single item's state"

**Assistant Response:**
I can see two issues here. First, the nested conditionals in your render logic make it hard to understand the component's states. We can refactor this using `ts-pattern` for clearer state matching. Second, your mapped list items maintain their own expanded state, which gets lost on parent re-renders. We should lift that state to the parent component.

Let me show you the refactored version with explanations:

```typescript
import { match, P } from 'ts-pattern'
import { useCallback, useState, memo } from 'react'
import { useGetPatientsQuery } from '@reducers/patientSlice'
import { colors } from '@theme'

// Lift state to parent so it survives re-renders
function PatientList() {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set())
  const { patients, isLoading, error } = useGetPatientsQuery(undefined, {
    // Only re-render when patients array changes, not when unrelated data updates
    selectFromResult: ({ data, isLoading, error }) => ({
      patients: data?.patients ?? [],
      isLoading,
      error
    })
  })
  
  // Stable callback for toggling expansion
  const toggleExpanded = useCallback((id: string) => {
    setExpandedIds(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }, [])
  
  // Clear, readable state matching with ts-pattern
  const Content = match({ isLoading, error, patients })
    .with({ isLoading: true }, () => <ActivityIndicator />)
    .with({ error: P.not(P.nullish) }, ({ error }) => (
      <ErrorView message={error.message} />
    ))
    .with({ patients: P.when(arr => arr.length > 0) }, ({ patients }) => (
      <FlatList
        data={patients}
        renderItem={({ item }) => (
          <PatientCard
            patient={item}
            expanded={expandedIds.has(item.id)}
            onToggle={toggleExpanded}
          />
        )}
        keyExtractor={keyExtractor}
      />
    ))
    .with({ patients: P.array() }, () => (
      <EmptyState message="No patients found" />
    ))
    .otherwise(() => null)
  
  return <View style={styles.container}>{Content}</View>
}

// Memoized to prevent re-renders when other list items change
const PatientCard = memo(({ patient, expanded, onToggle }: PatientCardProps) => (
  <Pressable
    onPress={() => onToggle(patient.id)}
    style={styles.card}
  >
    <Text style={styles.name}>{patient.name}</Text>
    {expanded && (
      <Text style={styles.details}>
        Age: {patient.age} | MRN: {patient.mrn}
      </Text>
    )}
  </Pressable>
))

// Extract keyExtractor outside component for stable reference
const keyExtractor = (item: Patient) => item.id

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.palette.white
  },
  card: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: colors.palette.neutral300
  },
  name: {
    fontSize: 16,
    fontFamily: 'Manrope-SemiBold',
    color: colors.palette.neutral900
  },
  details: {
    marginTop: 8,
    fontSize: 14,
    fontFamily: 'Manrope-Regular',
    color: colors.palette.neutral600
  }
})
```

This refactor accomplishes several things:

First, the `ts-pattern` match eliminates four levels of nested ternaries, making each state (loading, error, data, empty) explicit and easy to reason about. You can now see at a glance what renders in each scenario.

Second, the expanded state now lives in the parent as a Set of IDs, which persists across re-renders and allows you to track multiple expanded items efficiently. The Set data structure gives you O(1) lookup performance when checking if an item is expanded.

Third, the RTK Query `selectFromResult` ensures this component only re-renders when the patients array actually changes, not when other fields in the API response update. This is crucial for performance in lists.

Fourth, the PatientCard is memoized and receives only the props it needs, preventing unnecessary re-renders when sibling items update their state. The stable `toggleExpanded` callback and `keyExtractor` function ensure the memoization isn't broken by new function references on each render.

The React Compiler will handle optimizing the rest, so we don't need additional memoization beyond these strategic points. Does this approach make sense for your use case?
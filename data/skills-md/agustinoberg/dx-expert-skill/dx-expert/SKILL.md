---
name: dx-expert
description: Enforce developer experience principles (SRP, hook architecture, compound component composition, UX polish) for React Native Expo projects. Use this skill proactively when writing or reviewing code that involves more than one component or more than one piece of logic.
---

# /dx-expert - Developer Experience Expert

Enforce Single Responsibility Principle, clean hook architecture, and component composition patterns in **React Native Expo** to maintain excellent developer experience without performance issues.

**Target platform:** React Native with Expo. Always prefer Expo APIs and Expo Router native features before reaching for third-party alternatives.

## When to Apply

Apply these principles **automatically** when:
- Creating or modifying more than one component
- Writing logic that spans multiple concerns
- Reviewing code that mixes state logic with rendering
- Refactoring existing code for clarity

## Core Principles

### 1. Single Responsibility Principle (SRP)

Separate **state logic** from **rendering logic**. Components render. Hooks manage state.

```typescript
// BAD - Mixed concerns
export const AppointmentCard = ({ appointmentId }: Props) => {
  const [appointment, setAppointment] = useState<Appointment | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [barber, setBarber] = useState<Barber | null>(null);

  useEffect(() => {
    fetchAppointment(appointmentId).then(setAppointment);
  }, [appointmentId]);

  useEffect(() => {
    if (appointment?.barberId) {
      fetchBarber(appointment.barberId).then(setBarber);
    }
  }, [appointment?.barberId]);

  const handleToggle = () => setIsExpanded(prev => !prev);

  return (
    <View>
      <Text>{appointment?.clientName}</Text>
      {isExpanded && <Text>{barber?.name}</Text>}
      <Pressable onPress={handleToggle}>
        <Text>Toggle</Text>
      </Pressable>
    </View>
  );
};

// GOOD - Separated concerns
export const AppointmentCard = ({ appointmentId }: AppointmentCardProps) => {
  const { appointment, barber, isExpanded, handleToggle } = useAppointmentCard({ appointmentId });

  return (
    <View>
      <Text>{appointment?.clientName}</Text>
      {isExpanded && <Text>{barber?.name}</Text>}
      <Pressable onPress={handleToggle}>
        <Text>Toggle</Text>
      </Pressable>
    </View>
  );
};
AppointmentCard.displayName = 'AppointmentCard';
```

---

### 2. Hook Architecture

#### 2a. One Hook Per File

Every hook lives in its own file. Group related hooks in folders.

```
hooks/
├── useAppointmentCard/
│   ├── index.ts
│   ├── useAppointmentCard.ts
│   ├── useExpandToggle.ts        # Small, focused sub-hook
│   └── types.ts
```

#### 2b. Small and Focused

Each hook does **one thing only**. If a hook grows beyond ~50-80 lines, split it.

```typescript
// BAD - Hook doing too many things
const useAppointmentForm = ({ appointmentId }: Args) => {
  // 200+ lines of fetching, validation, submission, formatting...
};

// GOOD - Composed small hooks
const useAppointmentForm = ({ appointmentId }: UseAppointmentFormArgs) => {
  const { appointment } = useAppointmentQuery({ appointmentId });
  const { form, handleSubmit } = useAppointmentFormState({ appointment });
  const { timeSlots } = useAvailableSlots({ barberId: appointment?.barberId });

  return { appointment, form, handleSubmit, timeSlots };
};
```

#### 2c. Single Object Argument

Hooks **always** receive a single object as argument. Never loose parameters.

```typescript
// BAD - Loose parameters
const useClientSearch = (query: string, filters: Filters, page: number) => { ... };

// GOOD - Single object argument
interface UseClientSearchArgs {
  query: string;
  filters: Filters;
  page: number;
}

const useClientSearch = ({ query, filters, page }: UseClientSearchArgs) => { ... };
```

Even with a single parameter, use an object for consistency and extensibility:

```typescript
// BAD
const useBarberDetails = (barberId: string) => { ... };

// GOOD
const useBarberDetails = ({ barberId }: UseBarberDetailsArgs) => { ... };
```

---

### 3. useEffect Rules

**Avoid useEffect whenever possible.** It is one of the main sources of memory leaks.

#### When NOT to use useEffect:
- Deriving state from props or other state (use `useMemo` or compute inline)
- Responding to user events (use event handlers)
- Transforming data for rendering (compute during render)
- Syncing with external stores (use `useSyncExternalStore`)

```typescript
// BAD - Derived state in useEffect
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// GOOD - Compute inline or with useMemo
const fullName = `${firstName} ${lastName}`;
```

#### When useEffect IS acceptable:
- Syncing with external systems (subscriptions, native modules)
- Cleanup on unmount (event listeners, timers)
- Cases where no alternative exists

#### If using useEffect:
1. Keep the dependency array **fully controlled and explicit**
2. Keep the effect body **small and focused** (< 10 lines)
3. Always include cleanup when needed
4. Never ignore exhaustive-deps warnings

```typescript
// Acceptable - External system sync
useEffect(() => {
  const subscription = eventEmitter.addListener('event', handler);
  return () => subscription.remove();
}, [handler]);
```

---

### 4. Memoization Strategy

#### useCallback: Almost Never

With React Compiler, `useCallback` loses its purpose. Do not use it.

```typescript
// BAD - Unnecessary with React Compiler
const handlePress = useCallback(() => {
  onSelect(item.id);
}, [onSelect, item.id]);

// GOOD - Just define the function
const handlePress = () => {
  onSelect(item.id);
};
```

#### useMemo: Only for Computed Constants

Use `useMemo` for expensive computations or derived constants. Do **not** memoize components or hooks. Do **not** memoize everything.

```typescript
// Valid - Expensive computation
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => a.name.localeCompare(b.name)),
  [items],
);

// Valid - Derived constant
const availableSlots = useMemo(
  () => slots.filter(slot => slot.isAvailable),
  [slots],
);

// BAD - Memoizing a component
const MemoizedCard = useMemo(() => <Card data={data} />, [data]);

// BAD - Memoizing trivial operations
const label = useMemo(() => `${firstName} ${lastName}`, [firstName, lastName]);
```

---

### 5. Component Rules

#### 5a. Small and Focused

Each component has **semantic meaning** and a clear, single purpose.

```typescript
// BAD - Component doing too much
const AppointmentScreen = () => {
  // 300 lines: header, filters, list, empty state, modals, FAB...
};

// GOOD - Composed small components
const AppointmentScreen = () => {
  return (
    <View style={styles.container}>
      <AppointmentHeader />
      <AppointmentFilters />
      <AppointmentList />
      <CreateAppointmentFAB />
    </View>
  );
};
AppointmentScreen.displayName = 'AppointmentScreen';
```

#### 5b. No Excessive Conditionals

Avoid nested ternaries and complex conditional rendering. Extract to components or use early returns.

```typescript
// BAD - Nested ternaries
return (
  <View>
    {isLoading ? (
      <Spinner />
    ) : error ? (
      <ErrorView error={error} />
    ) : data?.length ? (
      data.map(item => (
        item.type === 'premium' ? (
          <PremiumCard key={item.id} data={item} />
        ) : (
          <StandardCard key={item.id} data={item} />
        )
      ))
    ) : (
      <EmptyState />
    )}
  </View>
);

// GOOD - Clear, readable conditions
if (isLoading) return <Spinner />;
if (error) return <ErrorView error={error} />;
if (!data?.length) return <EmptyState />;

return (
  <View>
    {data.map(item => (
      <AppointmentCard key={item.id} data={item} />
    ))}
  </View>
);
```

#### 5c. Compound Component Pattern — Composition Is All You Need

This is **the preferred way** to build components and screens. Instead of monolithic components with growing lists of boolean props, use the compound component pattern (`Component.Root`, `Component.Header`, `Component.Content`, etc.) to create declarative, composable APIs that share state through context.

##### The Golden Rule

**If you have a boolean prop that determines which component tree gets rendered, you need composition instead.**

```typescript
// BAD - Boolean props that control rendering
<Composer isThread={true} isEditing={false} isForwarding={false} isDM={false} />

// GOOD - Distinct component trees that compose shared internals
<ThreadComposer />   // Renders only what threads need
<EditComposer />     // Renders only what editing needs
<ForwardComposer />  // Renders only what forwarding needs
```

Don't render or don't — there are no booleans. Want drag-and-drop? Render `<DropZone />`. Don't want it? Don't render it. No `enableDropZone={false}`.

##### The Pattern

A compound component has:
1. **A Provider** that holds the context and defines the shared interface (state + actions)
2. **Sub-components** that consume the context and render specific parts
3. **A namespace export** that groups everything under `Component.Root`, `Component.Header`, etc.

**State management:** Always use **React Context** for sharing state within compound components. External state (React Query, global stores) feeds into the provider from outside, but the delivery mechanism between provider and sub-components is always Context.

The key insight: **the provider defines the interface, but each consumer decides the implementation.** Different screens can use different state management (useState, React Query, global sync) as long as they conform to the same context interface.

##### File Organization

Flexible based on size:

**Small compound component** — everything in one file:
```
ServicePicker/
├── index.ts
├── ServicePicker.tsx     # Context, provider, and sub-components all here
├── styles.ts
└── types.ts
```

**Large compound component** — split across files in a folder:
```
AppointmentComposer/
├── index.ts
├── context.ts                          # Context + useContext hook
├── types.ts                            # Shared types
├── AppointmentComposer.Frame.tsx
├── AppointmentComposer.ClientPicker.tsx
├── AppointmentComposer.DatePicker.tsx
├── AppointmentComposer.SubmitButton.tsx
├── CommonActions.tsx                   # Co-located shared composition
└── styles.ts
```

Shared compositions like `CommonActions` are **co-located** within the compound component folder.

##### Full Example: Appointment Composer

Imagine an appointment component used in multiple places: creating, editing, and rescheduling. Each has subtle differences in UI and state.

```typescript
// -- Context Interface --

interface AppointmentComposerContextValue {
  state: {
    clientId: string | null;
    barberId: string | null;
    serviceIds: string[];
    date: Date | null;
    notes: string;
  };
  actions: {
    updateClient: (clientId: string) => void;
    updateBarber: (barberId: string) => void;
    updateServices: (serviceIds: string[]) => void;
    updateDate: (date: Date) => void;
    updateNotes: (notes: string) => void;
    submit: () => void;
  };
  meta: {
    isSubmitting: boolean;
    canSubmit: boolean;
  };
}

const AppointmentComposerContext = createContext<AppointmentComposerContextValue | null>(null);

const useAppointmentComposer = () => {
  const context = useContext(AppointmentComposerContext);
  if (!context) {
    throw new Error('Must be used within AppointmentComposer.Provider');
  }
  return context;
};

// -- Sub-components (agnostic to state implementation) --

const Frame = ({ children }: { children: ReactNode }) => (
  <View style={styles.frame}>{children}</View>
);
Frame.displayName = 'AppointmentComposer.Frame';

const ClientPicker = () => {
  const { state, actions } = useAppointmentComposer();
  return (
    <ClientSelector
      selectedId={state.clientId}
      onSelect={actions.updateClient}
    />
  );
};
ClientPicker.displayName = 'AppointmentComposer.ClientPicker';

const BarberPicker = () => {
  const { state, actions } = useAppointmentComposer();
  return (
    <BarberSelector
      selectedId={state.barberId}
      onSelect={actions.updateBarber}
    />
  );
};
BarberPicker.displayName = 'AppointmentComposer.BarberPicker';

const ServicePicker = () => {
  const { state, actions } = useAppointmentComposer();
  return (
    <ServiceMultiSelect
      selectedIds={state.serviceIds}
      onChange={actions.updateServices}
    />
  );
};
ServicePicker.displayName = 'AppointmentComposer.ServicePicker';

const DatePicker = () => {
  const { state, actions } = useAppointmentComposer();
  return <CalendarPicker selected={state.date} onSelect={actions.updateDate} />;
};
DatePicker.displayName = 'AppointmentComposer.DatePicker';

const Notes = () => {
  const { state, actions } = useAppointmentComposer();
  return (
    <TextInput
      value={state.notes}
      onChangeText={actions.updateNotes}
      placeholder="Notes..."
    />
  );
};
Notes.displayName = 'AppointmentComposer.Notes';

const SubmitButton = () => {
  const { actions, meta } = useAppointmentComposer();
  return (
    <Button
      onPress={actions.submit}
      disabled={!meta.canSubmit}
      loading={meta.isSubmitting}
    />
  );
};
SubmitButton.displayName = 'AppointmentComposer.SubmitButton';

// -- Namespace Export --

export const AppointmentComposer = {
  Context: AppointmentComposerContext,
  useContext: useAppointmentComposer,
  Frame,
  ClientPicker,
  BarberPicker,
  ServicePicker,
  DatePicker,
  Notes,
  SubmitButton,
};
```

##### Different Implementations, Same Components

**Creating an appointment** — state is local, submit creates:

```typescript
const CreateAppointmentProvider = ({ children }: { children: ReactNode }) => {
  const [state, setState] = useState(INITIAL_STATE);
  const { mutate: createAppointment, isPending } = useCreateAppointmentMutation();

  const actions = {
    updateClient: (clientId: string) => setState(prev => ({ ...prev, clientId })),
    updateBarber: (barberId: string) => setState(prev => ({ ...prev, barberId })),
    // ...other updates
    submit: () => createAppointment(state),
  };

  const meta = { isSubmitting: isPending, canSubmit: !!state.clientId && !!state.date };

  return (
    <AppointmentComposer.Context.Provider value={{ state, actions, meta }}>
      {children}
    </AppointmentComposer.Context.Provider>
  );
};

// Usage — all sub-components, full form:
const CreateAppointmentScreen = () => (
  <CreateAppointmentProvider>
    <AppointmentComposer.Frame>
      <AppointmentComposer.ClientPicker />
      <AppointmentComposer.BarberPicker />
      <AppointmentComposer.ServicePicker />
      <AppointmentComposer.DatePicker />
      <AppointmentComposer.Notes />
      <AppointmentComposer.SubmitButton />
    </AppointmentComposer.Frame>
  </CreateAppointmentProvider>
);
CreateAppointmentScreen.displayName = 'CreateAppointmentScreen';
```

**Editing an appointment** — state is pre-filled, submit updates, no client picker:

```typescript
const EditAppointmentProvider = ({ appointmentId, children }: EditProviderProps) => {
  const { data: appointment } = useAppointmentQuery({ appointmentId });
  const [state, setState] = useState(() => mapAppointmentToState(appointment));
  const { mutate: updateAppointment, isPending } = useUpdateAppointmentMutation();

  const actions = {
    // ...same interface, different implementation
    submit: () => updateAppointment({ appointmentId, ...state }),
  };

  return (
    <AppointmentComposer.Context.Provider value={{ state, actions, meta }}>
      {children}
    </AppointmentComposer.Context.Provider>
  );
};

// Usage — NO ClientPicker, NO boolean. We just don't render it.
const EditAppointmentScreen = () => (
  <EditAppointmentProvider appointmentId={id}>
    <AppointmentComposer.Frame>
      <AppointmentComposer.BarberPicker />
      <AppointmentComposer.ServicePicker />
      <AppointmentComposer.DatePicker />
      <AppointmentComposer.Notes />
      <AppointmentComposer.SubmitButton />
    </AppointmentComposer.Frame>
  </EditAppointmentProvider>
);
EditAppointmentScreen.displayName = 'EditAppointmentScreen';
```

**Rescheduling** — only date picker, submit button is OUTSIDE the frame (in a modal footer):

```typescript
// Lift the provider above the frame so external components can access state.
const RescheduleModal = () => (
  <RescheduleProvider appointmentId={id}>
    <ModalContent>
      <AppointmentComposer.Frame>
        <AppointmentComposer.DatePicker />
      </AppointmentComposer.Frame>
    </ModalContent>
    <ModalFooter>
      {/* This button is OUTSIDE the frame but INSIDE the provider.
          It can access state and actions from context. */}
      <AppointmentComposer.SubmitButton />
    </ModalFooter>
  </RescheduleProvider>
);
RescheduleModal.displayName = 'RescheduleModal';
```

##### Lifting State — The Most Powerful Technique

If a component outside your main frame needs access to the composer's state, **lift the provider higher in the tree**. The provider doesn't have to wrap only the visual component — it wraps anything that needs access.

```typescript
// BAD - Trying to pass state back up
const Modal = () => {
  const [formState, setFormState] = useState(null);
  return (
    <View>
      <Composer onFormStateChange={setFormState} />
      <Button onPress={() => submit(formState)}>Save</Button>  {/* Stale, fragile */}
    </View>
  );
};

// GOOD - Lift the provider
const Modal = () => (
  <ComposerProvider>
    <Composer />
    <SaveButton />  {/* Uses context directly, always in sync */}
  </ComposerProvider>
);
```

##### Reusable Monoliths From Compound Components

When many implementations share the same actions, create a convenience wrapper that composes the sub-components — but always allow escaping to individual pieces:

```typescript
// Convenience: shared default for most cases
const CommonActions = () => (
  <>
    <AppointmentComposer.ServicePicker />
    <AppointmentComposer.DatePicker />
    <AppointmentComposer.Notes />
  </>
);

// Most screens use CommonActions
const CreateScreen = () => (
  <CreateProvider>
    <AppointmentComposer.Frame>
      <AppointmentComposer.ClientPicker />
      <CommonActions />
      <AppointmentComposer.SubmitButton />
    </AppointmentComposer.Frame>
  </CreateProvider>
);

// But you can always escape to individual components
const EditScreen = () => (
  <EditProvider appointmentId={id}>
    <AppointmentComposer.Frame>
      {/* No ClientPicker, no CommonActions — just what we need */}
      <AppointmentComposer.DatePicker />
      <AppointmentComposer.Notes />
      <AppointmentComposer.SubmitButton />
    </AppointmentComposer.Frame>
  </EditProvider>
);
```

##### Why This Is the Best Approach

| Problem | Compound Components Solve It |
|---------|------------------------------|
| Boolean prop explosion (`isEditing`, `isThread`, `isForwarding`) | Each variant is its own component tree — no booleans |
| Prop drilling | State is shared via context, not passed through layers |
| Massive components | Each sub-component is small and focused |
| Rigid layouts | Consumer controls order and composition |
| State management coupling | Provider defines interface; implementation is swapped at the root |
| Components outside the frame needing state | Lift the provider higher in the tree |
| Testing | Sub-components can be tested in isolation with a mock provider |

##### When to Use

- **Screens**: Always. Every screen should be a Provider + composed sub-components.
- **Complex components**: Cards with header/body/footer, modals, composers, forms with sections.
- **Anything with shared state**: If 2+ sibling components need the same data, use this pattern.
- **Components with variants**: If the same concept has different implementations (create vs edit vs reschedule), use different providers with the same sub-components.

##### When NOT to Use

- Simple, self-contained components with no shared state (a `Badge`, a `Divider`)
- Components with 1-2 props that don't drill anywhere

##### Anti-Patterns

```typescript
// BAD - Boolean props controlling what renders
<Composer isEditing={true} hideClientPicker={true} showCancelButton={true} />

// BAD - God component with everything inline
const AppointmentScreen = () => {
  // 300 lines of mixed state + rendering + conditions
};

// BAD - Passing state back up to parent
<Composer onFormStateChange={setFormState} />

// BAD - Array of actions with conditions
const actions = [
  { id: 'emoji', show: !isEditing },
  { id: 'attach', show: !isEditing && !isForwarding },
  // ...nightmare
];
```

#### 5d. No renderSomething Functions

Never create `render` functions inside components. Extract to proper components.

```typescript
// BAD - render functions
const ClientList = () => {
  const renderHeader = () => <View><Text>Clients</Text></View>;
  const renderItem = (item: Client) => <View><Text>{item.name}</Text></View>;
  const renderEmpty = () => <View><Text>No clients</Text></View>;

  return (
    <View>
      {renderHeader()}
      <FlatList
        data={clients}
        renderItem={({ item }) => renderItem(item)}
        ListEmptyComponent={renderEmpty()}
      />
    </View>
  );
};

// GOOD - Proper components
const ClientListHeader = () => (
  <View><Text>Clients</Text></View>
);
ClientListHeader.displayName = 'ClientListHeader';

const ClientListItem = ({ client }: ClientListItemProps) => (
  <View><Text>{client.name}</Text></View>
);
ClientListItem.displayName = 'ClientListItem';

const ClientListEmpty = () => (
  <View><Text>No clients</Text></View>
);
ClientListEmpty.displayName = 'ClientListEmpty';

const ClientList = () => (
  <FlatList
    data={clients}
    renderItem={({ item }) => <ClientListItem client={item} />}
    ListHeaderComponent={ClientListHeader}
    ListEmptyComponent={ClientListEmpty}
  />
);
ClientList.displayName = 'ClientList';
```

#### 5e. Use Native APIs

Prefer React Native built-in components: `FlatList`, `SectionList`, `ScrollView`, `Pressable`. Avoid reinventing what the platform provides.

---

### 6. Suggest Better Libraries When Obvious

If something is clearly being reinvented when a well-known library already solves it, suggest it:

> "This could be much better using **[library]**. It would save you all these problems."

Only suggest when it's **obviously** a bad practice — don't over-suggest. Use common sense.

---

### 7. User Experience Must Be Pixel-Perfect

DX and UX go hand in hand. Every solution must consider **how the user actually experiences it**. This is non-negotiable.

#### Keyboard Handling

The keyboard must **never** cover the input the user is typing in. Ever. This is the #1 UX offense in mobile apps.

Solutions (use whichever fits):
- `KeyboardAvoidingView` (built-in React Native) for simple screens
- `react-native-keyboard-controller` for smooth native-driven animations
- `ScrollView` with `keyboardShouldPersistTaps="handled"` for scrollable forms
- Proper `contentContainerStyle` padding to account for keyboard height

```typescript
// BAD - Input hidden behind keyboard
const FormScreen = () => (
  <View style={styles.container}>
    <TextInput placeholder="Name" />
    <TextInput placeholder="Email" />
    <TextInput placeholder="Notes" />  {/* Covered by keyboard */}
  </View>
);

// GOOD - Keyboard never covers active input
const FormScreen = () => (
  <KeyboardAvoidingView behavior="padding" style={styles.container}>
    <ScrollView keyboardShouldPersistTaps="handled">
      <TextInput placeholder="Name" />
      <TextInput placeholder="Email" />
      <TextInput placeholder="Notes" />
    </ScrollView>
  </KeyboardAvoidingView>
);
```

#### General UX Principles

Always consider:

- **Loading states**: Never show a blank screen. Use skeletons, spinners, or placeholders.
- **Error states**: Every failure must be communicated clearly. No silent failures.
- **Empty states**: Lists with no data must show a meaningful empty state, not just nothing.
- **Touch targets**: Interactive elements must be large enough to tap comfortably (minimum 44x44pt).
- **Feedback**: Every user action must have visible feedback (press states, animations, haptics).
- **Scroll behavior**: Long content must scroll. Never clip or hide content without a way to reach it.
- **Safe areas**: Respect device notches, home indicators, and status bars. Use safe area insets.
- **Dismissibility**: Modals, bottom sheets, and overlays must always be dismissible (gesture or button).

These are not nice-to-haves. They are **requirements**. If a solution works technically but the UX is broken, it's not done.

---

### 8. Expo Router First

Always prefer **Expo Router native features** before reaching for manual solutions or third-party navigation libraries.

#### Use Expo Router For:

- **Navigation**: File-based routing is the default. Use `app/` directory conventions. Don't manually configure stack navigators when a file in the right folder does the same thing.
- **Layouts**: Use `_layout.tsx` files for shared layouts (tabs, stacks, drawers). Don't build layout wrappers manually.
- **Modals**: Use `modal` presentation in route config. Don't build custom modal navigation.
- **Deep linking**: Expo Router handles it automatically via file structure. Don't configure linking manually.
- **Route params**: Use `useLocalSearchParams` and `useGlobalSearchParams`. Don't pass data through context or state when it belongs in the URL.
- **Navigation hooks**: Use `useRouter`, `useSegments`, `usePathname` from `expo-router`.
- **Protected routes**: Use redirect logic in layouts, not manual navigation guards.
- **Screen options**: Configure via `<Stack.Screen options={...} />` in layouts, not imperatively.

```typescript
// BAD - Manual navigation when Expo Router handles it
import { useNavigation } from '@react-navigation/native';

const navigation = useNavigation();
navigation.navigate('ClientDetail', { clientId: '123' });

// GOOD - Expo Router
import { useRouter } from 'expo-router';

const router = useRouter();
router.push({ pathname: '/clients/[clientId]', params: { clientId: '123' } });
```

```typescript
// BAD - Manual modal management
const [showModal, setShowModal] = useState(false);

return (
  <>
    <Button onPress={() => setShowModal(true)} />
    {showModal && <CustomModal onClose={() => setShowModal(false)} />}
  </>
);

// GOOD - Expo Router modal route (when it fits)
// app/clients/[clientId]/edit.tsx with presentation: 'modal' in _layout.tsx
router.push(`/clients/${clientId}/edit`);
```

#### When Expo Router Is Not Enough

If Expo Router doesn't cover a specific need (e.g., complex nested navigators, custom transition animations), then use React Navigation APIs directly. But always check Expo Router first.

---

### 9. Basic Performance Awareness

Don't overthink performance — the React Compiler handles most re-render issues. But be aware of these basics:

- **FlatList**: Always use `keyExtractor`. Never render heavy components without `getItemLayout` for known-height items. Prefer `FlashList` for large lists.
- **Images**: Always provide explicit `width` and `height`. Use cached image libraries when loading remote images.
- **Inline objects/arrays in JSX**: Avoid creating new objects/arrays on every render as props (e.g., `style={{ flex: 1 }}`). Move them to stylesheets or constants.
- **Large context values**: If a context value changes frequently and has many consumers, consider splitting into separate contexts (one for state, one for actions) to reduce unnecessary re-renders.

---

## Decision Checklist

When writing or reviewing code, verify:

- [ ] **SRP**: Is state logic in hooks and rendering in components?
- [ ] **Hook size**: Is each hook under ~80 lines and focused on one thing?
- [ ] **Hook args**: Does every hook receive a single object argument?
- [ ] **One hook per file**: Is each hook in its own file?
- [ ] **No useEffect**: Can this be solved without useEffect?
- [ ] **No useCallback**: Is useCallback removed (React Compiler handles it)?
- [ ] **useMemo**: Only used for computed constants, not components or trivial ops?
- [ ] **Component size**: Is each component small with semantic meaning?
- [ ] **No nested ternaries**: Are conditionals flat and readable?
- [ ] **Compound components**: Are screens and complex components using the `Component.Root` / `Component.X` pattern?
- [ ] **No prop drilling**: Is state shared via context inside compound components, not drilled through props?
- [ ] **No renderX functions**: Are all render functions extracted to components?
- [ ] **Native APIs**: Are platform components used where applicable?
- [ ] **Library suggestions**: Is there a hand-rolled solution that a library already solves better?
- [ ] **Keyboard**: Does the keyboard never cover the active input?
- [ ] **Loading/Error/Empty**: Are all three states handled for every data-driven screen?
- [ ] **Touch targets**: Are interactive elements at least 44x44pt?
- [ ] **Safe areas**: Are notches, home indicators, and status bars respected?
- [ ] **Dismissibility**: Can every overlay/modal/sheet be dismissed?
- [ ] **Expo Router**: Is Expo Router used for navigation, modals, params, and layouts before manual alternatives?

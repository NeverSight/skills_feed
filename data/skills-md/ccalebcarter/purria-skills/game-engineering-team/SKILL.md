---
name: game-engineering-team
description: AAA-caliber engineering council for building production-quality games. Use when implementing game systems, writing game code, designing data architecture, building UI components, creating tutorials, optimizing performance, or any technical game development task. Covers game programming patterns, casino/card game implementation, reward systems, game UI engineering, tutorial design, code architecture, data infrastructure, security, and quality assurance. Triggers on requests for game code, system implementation, refactoring, performance optimization, data design, or technical architecture decisions.
---

# Game Engineering Team

A multidisciplinary council of AAA-caliber engineers dedicated to building production-quality game systems for Farming in Purria.

## The Engineering Council

### Core Game Engineers (6)

| Engineer | Specialization | Technical Lens |
|----------|----------------|----------------|
| **Game Systems Architect** | State machines, ECS, core loops | "How do the pieces fit together?" |
| **Casino Logic Engineer** | Probability, RNG, payout systems | "Is the math provably fair?" |
| **Card Game Specialist** | Hand evaluation, deck management | "How do cards flow through states?" |
| **Board/Grid Engineer** | Spatial algorithms, pathfinding | "How does the hex grid compute?" |
| **Progression Engineer** | XP curves, unlock systems, gating | "How does growth feel right?" |
| **Real-Time Systems Lead** | Timing, animation sync, frame budgets | "Does it feel responsive?" |

### UI/UX Engineers (5)

| Engineer | Specialization | Technical Lens |
|----------|----------------|----------------|
| **Game UI Architect** | Component systems, layout engines | "How is the UI structured?" |
| **Interaction Engineer** | Touch, gestures, accessibility | "How do players physically interact?" |
| **Animation Programmer** | Tweens, particles, juice | "Does it feel alive?" |
| **Typography Specialist** | Font rendering, readability, style | "Is text beautiful and readable?" |
| **Responsive Design Lead** | Mobile-first, cross-platform | "Does it work everywhere?" |

### Data & Infrastructure (5)

| Engineer | Specialization | Technical Lens |
|----------|----------------|----------------|
| **Data Architect** | Schema design, relationships, queries | "How is data organized?" |
| **Telemetry Engineer** | Logging, analytics, events | "What do we need to measure?" |
| **Security Engineer** | Auth, validation, anti-cheat | "Is this exploitable?" |
| **Performance Engineer** | Profiling, optimization, budgets | "Will it run on low-end devices?" |
| **DevOps Specialist** | CI/CD, deployment, monitoring | "How do we ship reliably?" |

### Quality & Craft (4)

| Engineer | Specialization | Technical Lens |
|----------|----------------|----------------|
| **Code Quality Lead** | Patterns, refactoring, reviews | "Is this maintainable?" |
| **Technical Writer** | Documentation, comments, APIs | "Can others understand this?" |
| **Test Architect** | Unit, integration, E2E strategies | "How do we verify correctness?" |
| **Tutorial Systems Engineer** | Onboarding flows, contextual help | "How do players learn this?" |

### Integration Specialists (4)

| Engineer | Specialization | Technical Lens |
|----------|----------------|----------------|
| **API Designer** | tRPC, REST, contract design | "How do client and server talk?" |
| **State Management Lead** | Zustand, persistence, sync | "Where does state live?" |
| **Plugin/Mod Architect** | Extensibility, configuration | "Can this be extended safely?" |
| **Cross-System Integrator** | System coupling, event buses | "How do systems communicate?" |

---

## Part I: Core Engineering Principles

### The Engineering Manifesto

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FARMING IN PURRIA ENGINEERING PRINCIPLES                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. PLAYER FIRST                                                            │
│     Every technical decision serves the player experience.                  │
│     60fps on mobile. Instant feedback. No jank.                            │
│                                                                             │
│  2. TYPE SAFETY END-TO-END                                                  │
│     From database to UI, types are the contract.                           │
│     If it compiles, it should work.                                        │
│                                                                             │
│  3. EXPLICIT OVER CLEVER                                                    │
│     Readable code beats clever code.                                       │
│     The next developer is you in 6 months.                                 │
│                                                                             │
│  4. SMALL, COMPOSABLE PIECES                                                │
│     Functions do one thing. Components render one thing.                   │
│     Composition over inheritance.                                          │
│                                                                             │
│  5. FAIL FAST, RECOVER GRACEFULLY                                           │
│     Validate inputs immediately. Handle errors at boundaries.              │
│     Players should never see stack traces.                                 │
│                                                                             │
│  6. MEASURE EVERYTHING                                                       │
│     If we can't measure it, we can't improve it.                           │
│     Telemetry is not optional.                                             │
│                                                                             │
│  7. OPTIMIZE LAST                                                            │
│     Make it work. Make it right. Make it fast.                             │
│     Profile before optimizing.                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Technical Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              TECH STACK                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FRONTEND                          BACKEND                                  │
│  ────────                          ───────                                  │
│  React 18+                         Hono                                     │
│  TanStack Router                   tRPC                                     │
│  Zustand                           Drizzle ORM                              │
│  Tailwind CSS                      SQLite/Turso                             │
│  shadcn/ui                         Bun runtime                              │
│  Framer Motion                     Zod validation                           │
│                                                                             │
│  TOOLING                           INFRASTRUCTURE                           │
│  ───────                           ──────────────                           │
│  TypeScript 5+                     Cloudflare Pages                         │
│  Biome (lint/format)               Cloudflare Workers                       │
│  Vitest                            GitHub Actions                           │
│  Playwright (E2E)                  PostHog analytics                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part II: Game Programming Patterns

### Pattern 1: Finite State Machines (FSM)

**When to Use:** Phase management, UI states, game mode transitions

```typescript
// Type-safe FSM with explicit transitions
type GamePhase = 'morning' | 'action' | 'resolution' | 'night';

interface PhaseTransitions {
  morning: 'action';
  action: 'resolution';
  resolution: 'night';
  night: 'morning';
}

type NextPhase<T extends GamePhase> = PhaseTransitions[T];

class GamePhaseMachine {
  private phase: GamePhase = 'morning';
  
  transition(): void {
    const transitions: Record<GamePhase, GamePhase> = {
      morning: 'action',
      action: 'resolution',
      resolution: 'night',
      night: 'morning',
    };
    
    this.phase = transitions[this.phase];
    this.onPhaseEnter(this.phase);
  }
  
  private onPhaseEnter(phase: GamePhase): void {
    // Phase-specific initialization
  }
}
```

### Pattern 2: Command Pattern (Undo/Redo)

**When to Use:** Bet placement, farm actions, any reversible operation

```typescript
interface Command {
  execute(): void;
  undo(): void;
  description: string;
}

class PlaceBetCommand implements Command {
  constructor(
    private potId: string,
    private betType: BetType,
    private amount: number,
    private gameState: GameState
  ) {}
  
  execute(): void {
    this.gameState.placeBet(this.potId, this.betType, this.amount);
  }
  
  undo(): void {
    this.gameState.removeBet(this.potId);
    this.gameState.refundCoins(this.amount);
  }
  
  get description() {
    return `Bet ${this.amount} on ${this.potId}`;
  }
}

class CommandHistory {
  private history: Command[] = [];
  private pointer = -1;
  
  execute(command: Command): void {
    // Clear redo stack
    this.history = this.history.slice(0, this.pointer + 1);
    command.execute();
    this.history.push(command);
    this.pointer++;
  }
  
  undo(): void {
    if (this.pointer >= 0) {
      this.history[this.pointer].undo();
      this.pointer--;
    }
  }
  
  redo(): void {
    if (this.pointer < this.history.length - 1) {
      this.pointer++;
      this.history[this.pointer].execute();
    }
  }
}
```

### Pattern 3: Observer Pattern (Event Bus)

**When to Use:** Cross-system communication, triggers, achievements

```typescript
type GameEvent = 
  | { type: 'POT_THRESHOLD_REACHED'; potId: string; threshold: number }
  | { type: 'TROUBLE_SPAWNED'; hexId: string; troubleType: TroubleType }
  | { type: 'SIMULIN_LEVELED'; simulinId: string; newLevel: number }
  | { type: 'TRIGGER_EARNED'; trigger: TriggerType }
  | { type: 'DAY_COMPLETED'; dayNumber: number };

type EventHandler<T extends GameEvent['type']> = (
  event: Extract<GameEvent, { type: T }>
) => void;

class GameEventBus {
  private handlers = new Map<GameEvent['type'], Set<EventHandler<any>>>();
  
  on<T extends GameEvent['type']>(type: T, handler: EventHandler<T>): () => void {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    this.handlers.get(type)!.add(handler);
    
    // Return unsubscribe function
    return () => this.handlers.get(type)?.delete(handler);
  }
  
  emit(event: GameEvent): void {
    const handlers = this.handlers.get(event.type);
    if (handlers) {
      handlers.forEach(handler => handler(event));
    }
  }
}

// Usage
const events = new GameEventBus();

// Trigger system listens for pot events
events.on('POT_THRESHOLD_REACHED', ({ potId, threshold }) => {
  if (threshold === 100) {
    checkForPerfectReadTrigger();
  }
});
```

### Pattern 4: Object Pool (Performance)

**When to Use:** Particles, projectiles, frequently created/destroyed objects

```typescript
class ObjectPool<T> {
  private pool: T[] = [];
  private activeCount = 0;
  
  constructor(
    private factory: () => T,
    private reset: (obj: T) => void,
    initialSize = 10
  ) {
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(factory());
    }
  }
  
  acquire(): T {
    if (this.activeCount >= this.pool.length) {
      this.pool.push(this.factory());
    }
    return this.pool[this.activeCount++];
  }
  
  release(obj: T): void {
    const index = this.pool.indexOf(obj);
    if (index !== -1 && index < this.activeCount) {
      this.reset(obj);
      // Swap with last active
      [this.pool[index], this.pool[this.activeCount - 1]] = 
        [this.pool[this.activeCount - 1], this.pool[index]];
      this.activeCount--;
    }
  }
  
  releaseAll(): void {
    for (let i = 0; i < this.activeCount; i++) {
      this.reset(this.pool[i]);
    }
    this.activeCount = 0;
  }
}
```

### Pattern 5: Strategy Pattern (Interchangeable Algorithms)

**When to Use:** AI behaviors, scoring algorithms, difficulty modes

```typescript
interface ScoringStrategy {
  calculateScore(results: DayResults): number;
  getName(): string;
}

class StandardScoring implements ScoringStrategy {
  calculateScore(results: DayResults): number {
    return results.potsWon * 100 + results.troubleCleared * 50;
  }
  getName() { return 'Standard'; }
}

class HarvestPhaseScoring implements ScoringStrategy {
  calculateScore(results: DayResults): number {
    // 3x multiplier during harvest phase
    return (results.potsWon * 100 + results.troubleCleared * 50) * 3;
  }
  getName() { return 'Harvest Bonus'; }
}

class GameScorer {
  constructor(private strategy: ScoringStrategy) {}
  
  setStrategy(strategy: ScoringStrategy): void {
    this.strategy = strategy;
  }
  
  score(results: DayResults): number {
    return this.strategy.calculateScore(results);
  }
}
```

---

## Part III: Casino & Card Game Implementation

### Random Number Generation

**Critical:** Use cryptographically secure, seedable RNG for fair play.

```typescript
class SeededRNG {
  private seed: number;
  
  constructor(seed: number = Date.now()) {
    this.seed = seed;
  }
  
  // Mulberry32 - fast, good distribution
  next(): number {
    let t = this.seed += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
  
  // Range helpers
  nextInt(min: number, max: number): number {
    return Math.floor(this.next() * (max - min + 1)) + min;
  }
  
  nextFloat(min: number, max: number): number {
    return this.next() * (max - min) + min;
  }
  
  // Shuffle array (Fisher-Yates)
  shuffle<T>(array: T[]): T[] {
    const result = [...array];
    for (let i = result.length - 1; i > 0; i--) {
      const j = this.nextInt(0, i);
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }
  
  // Weighted random selection
  weightedChoice<T>(items: T[], weights: number[]): T {
    const totalWeight = weights.reduce((a, b) => a + b, 0);
    let random = this.next() * totalWeight;
    
    for (let i = 0; i < items.length; i++) {
      random -= weights[i];
      if (random <= 0) return items[i];
    }
    return items[items.length - 1];
  }
}

// Usage with verifiable seed
const daySeed = hashString(`${seasonId}-day-${dayNumber}`);
const rng = new SeededRNG(daySeed);
```

### Card Deck Management

```typescript
interface Card {
  suit: 'hearts' | 'diamonds' | 'clubs' | 'spades';
  rank: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13;
}

class Deck {
  private cards: Card[] = [];
  private discardPile: Card[] = [];
  
  constructor(private rng: SeededRNG) {
    this.reset();
  }
  
  reset(): void {
    this.cards = [];
    this.discardPile = [];
    
    const suits: Card['suit'][] = ['hearts', 'diamonds', 'clubs', 'spades'];
    for (const suit of suits) {
      for (let rank = 1; rank <= 13; rank++) {
        this.cards.push({ suit, rank: rank as Card['rank'] });
      }
    }
    
    this.shuffle();
  }
  
  shuffle(): void {
    this.cards = this.rng.shuffle(this.cards);
  }
  
  draw(count = 1): Card[] {
    if (this.cards.length < count) {
      // Reshuffle discard pile into deck
      this.cards = [...this.cards, ...this.rng.shuffle(this.discardPile)];
      this.discardPile = [];
    }
    
    return this.cards.splice(0, count);
  }
  
  discard(cards: Card[]): void {
    this.discardPile.push(...cards);
  }
  
  get remaining(): number {
    return this.cards.length;
  }
  
  peek(count = 1): Card[] {
    return this.cards.slice(0, count);
  }
}
```

### Poker Hand Evaluation

```typescript
type HandRank = 
  | 'high-card'
  | 'pair'
  | 'two-pair'
  | 'three-of-a-kind'
  | 'straight'
  | 'flush'
  | 'full-house'
  | 'four-of-a-kind'
  | 'straight-flush'
  | 'royal-flush';

interface HandResult {
  rank: HandRank;
  value: number;        // For comparing same-rank hands
  cards: Card[];        // The 5 cards making the hand
  kickers: Card[];      // Remaining cards for tiebreakers
}

class PokerHandEvaluator {
  evaluate(cards: Card[]): HandResult {
    if (cards.length < 5) {
      throw new Error('Need at least 5 cards');
    }
    
    // If more than 5 cards, find best 5-card hand
    if (cards.length > 5) {
      return this.findBestHand(cards);
    }
    
    const sorted = [...cards].sort((a, b) => b.rank - a.rank);
    const isFlush = this.checkFlush(sorted);
    const straightRank = this.checkStraight(sorted);
    const groups = this.groupByRank(sorted);
    
    // Check for each hand type
    if (isFlush && straightRank === 14) {
      return { rank: 'royal-flush', value: 1000, cards: sorted, kickers: [] };
    }
    if (isFlush && straightRank > 0) {
      return { rank: 'straight-flush', value: 900 + straightRank, cards: sorted, kickers: [] };
    }
    if (groups[0].length === 4) {
      return this.buildResult('four-of-a-kind', 800, groups, sorted);
    }
    if (groups[0].length === 3 && groups[1]?.length === 2) {
      return this.buildResult('full-house', 700, groups, sorted);
    }
    if (isFlush) {
      return { rank: 'flush', value: 600 + this.highCardValue(sorted), cards: sorted, kickers: [] };
    }
    if (straightRank > 0) {
      return { rank: 'straight', value: 500 + straightRank, cards: sorted, kickers: [] };
    }
    if (groups[0].length === 3) {
      return this.buildResult('three-of-a-kind', 400, groups, sorted);
    }
    if (groups[0].length === 2 && groups[1]?.length === 2) {
      return this.buildResult('two-pair', 300, groups, sorted);
    }
    if (groups[0].length === 2) {
      return this.buildResult('pair', 200, groups, sorted);
    }
    
    return { 
      rank: 'high-card', 
      value: 100 + this.highCardValue(sorted), 
      cards: sorted, 
      kickers: sorted.slice(1) 
    };
  }
  
  private checkFlush(cards: Card[]): boolean {
    return cards.every(c => c.suit === cards[0].suit);
  }
  
  private checkStraight(cards: Card[]): number {
    const ranks = cards.map(c => c.rank).sort((a, b) => b - a);
    
    // Check for wheel (A-2-3-4-5)
    if (ranks[0] === 13 && ranks[1] === 5 && ranks[2] === 4 && 
        ranks[3] === 3 && ranks[4] === 2) {
      return 5; // Low straight
    }
    
    // Check regular straight
    for (let i = 0; i < ranks.length - 1; i++) {
      if (ranks[i] - ranks[i + 1] !== 1) return 0;
    }
    
    return ranks[0]; // High card of straight
  }
  
  private groupByRank(cards: Card[]): Card[][] {
    const groups = new Map<number, Card[]>();
    for (const card of cards) {
      if (!groups.has(card.rank)) groups.set(card.rank, []);
      groups.get(card.rank)!.push(card);
    }
    return Array.from(groups.values()).sort((a, b) => {
      if (a.length !== b.length) return b.length - a.length;
      return b[0].rank - a[0].rank;
    });
  }
  
  private highCardValue(cards: Card[]): number {
    return cards.reduce((acc, c, i) => acc + c.rank * Math.pow(15, 4 - i), 0);
  }
  
  private buildResult(
    rank: HandRank, 
    baseValue: number, 
    groups: Card[][], 
    sorted: Card[]
  ): HandResult {
    const mainCards = groups[0];
    const value = baseValue + mainCards[0].rank;
    return { rank, value, cards: sorted, kickers: groups.slice(1).flat() };
  }
  
  private findBestHand(cards: Card[]): HandResult {
    let best: HandResult | null = null;
    
    // Generate all 5-card combinations
    const combinations = this.combinations(cards, 5);
    
    for (const combo of combinations) {
      const result = this.evaluate(combo);
      if (!best || result.value > best.value) {
        best = result;
      }
    }
    
    return best!;
  }
  
  private *combinations<T>(arr: T[], k: number): Generator<T[]> {
    if (k === 0) { yield []; return; }
    if (arr.length < k) return;
    
    const [first, ...rest] = arr;
    for (const combo of this.combinations(rest, k - 1)) {
      yield [first, ...combo];
    }
    yield* this.combinations(rest, k);
  }
}
```

### Pot/Betting System

```typescript
type BetType = 'fold' | 'call' | 'raise' | 'all-in';

interface Pot {
  id: string;
  name: string;
  currentFill: number;     // 0-100
  thresholds: number[];    // [50, 80, 100]
  payoutMultipliers: Record<BetType, number[]>; // Per threshold
}

interface Bet {
  potId: string;
  betType: BetType;
  amount: number;
  placedAt: Date;
}

class BettingSystem {
  private bets: Bet[] = [];
  
  placeBet(potId: string, betType: BetType, amount: number): Bet {
    // Validate bet
    if (betType !== 'fold' && amount <= 0) {
      throw new Error('Bet amount must be positive');
    }
    
    // Check for existing bet on this pot
    const existing = this.bets.find(b => b.potId === potId);
    if (existing) {
      throw new Error('Already bet on this pot');
    }
    
    const bet: Bet = {
      potId,
      betType,
      amount: betType === 'fold' ? 0 : amount,
      placedAt: new Date(),
    };
    
    this.bets.push(bet);
    return bet;
  }
  
  resolveBets(pots: Pot[]): BetResult[] {
    const results: BetResult[] = [];
    
    for (const bet of this.bets) {
      const pot = pots.find(p => p.id === bet.potId);
      if (!pot) continue;
      
      const result = this.resolveSingleBet(bet, pot);
      results.push(result);
    }
    
    this.bets = [];
    return results;
  }
  
  private resolveSingleBet(bet: Bet, pot: Pot): BetResult {
    // Find highest threshold reached
    let thresholdIndex = -1;
    for (let i = pot.thresholds.length - 1; i >= 0; i--) {
      if (pot.currentFill >= pot.thresholds[i]) {
        thresholdIndex = i;
        break;
      }
    }
    
    // Fold always returns nothing
    if (bet.betType === 'fold') {
      return { bet, won: false, payout: 0, thresholdReached: thresholdIndex };
    }
    
    // No threshold reached = loss
    if (thresholdIndex < 0) {
      return { bet, won: false, payout: 0, thresholdReached: -1 };
    }
    
    // Calculate payout
    const multiplier = pot.payoutMultipliers[bet.betType][thresholdIndex];
    const payout = Math.floor(bet.amount * multiplier);
    
    return { 
      bet, 
      won: true, 
      payout, 
      thresholdReached: thresholdIndex,
      multiplier 
    };
  }
}

interface BetResult {
  bet: Bet;
  won: boolean;
  payout: number;
  thresholdReached: number;
  multiplier?: number;
}
```

---

## Part IV: Reward & Progression Systems

### Experience Curves

```typescript
// Common XP curve formulas
const XP_CURVES = {
  // Linear: Simple, predictable
  linear: (level: number, base: number) => base * level,
  
  // Quadratic: Steeper growth
  quadratic: (level: number, base: number) => base * level * level,
  
  // Exponential: Slow start, rapid growth
  exponential: (level: number, base: number, rate: number) => 
    base * Math.pow(rate, level),
  
  // Polynomial: Customizable curve
  polynomial: (level: number, base: number, power: number) => 
    Math.floor(base * Math.pow(level, power)),
  
  // Fibonacci-like: Natural feeling progression
  fibonacci: (level: number, base: number) => {
    if (level <= 1) return base;
    let [a, b] = [base, base * 2];
    for (let i = 2; i < level; i++) {
      [a, b] = [b, a + b];
    }
    return b;
  },
};

class ProgressionSystem {
  constructor(
    private xpForLevel: (level: number) => number,
    private maxLevel: number = 100
  ) {}
  
  getLevel(totalXP: number): number {
    let level = 1;
    let xpNeeded = 0;
    
    while (level <= this.maxLevel) {
      xpNeeded += this.xpForLevel(level);
      if (totalXP < xpNeeded) break;
      level++;
    }
    
    return Math.min(level, this.maxLevel);
  }
  
  getProgress(totalXP: number): { level: number; current: number; needed: number; percent: number } {
    const level = this.getLevel(totalXP);
    const xpForCurrent = this.getTotalXPForLevel(level);
    const xpForNext = this.xpForLevel(level + 1);
    const current = totalXP - xpForCurrent;
    
    return {
      level,
      current,
      needed: xpForNext,
      percent: Math.floor((current / xpForNext) * 100),
    };
  }
  
  private getTotalXPForLevel(level: number): number {
    let total = 0;
    for (let i = 1; i < level; i++) {
      total += this.xpForLevel(i);
    }
    return total;
  }
}

// Simulin bonding uses gentle curve
const simulinProgression = new ProgressionSystem(
  (level) => XP_CURVES.polynomial(level, 100, 1.5),
  25 // Max bond level
);
```

### Trigger & Combo System

```typescript
interface DailyTrigger {
  type: TriggerType;
  earnedAt: Date;
  dayNumber: number;
  metadata?: Record<string, any>;
}

type TriggerType = 
  | 'first_bloom'
  | 'perfect_read'
  | 'trouble_slayer'
  | 'growth_spurt'
  | 'simulin_sync';

type ComboHandType = 
  | 'pair'
  | 'two_pair'
  | 'three_of_a_kind'
  | 'straight'
  | 'full_house'
  | 'flush'
  | 'four_of_a_kind'
  | 'straight_flush'
  | 'royal_flush';

class ComboEngine {
  private readonly HAND_VALUES: Record<ComboHandType, number> = {
    'pair': 2,
    'two_pair': 3,
    'three_of_a_kind': 5,
    'straight': 10,
    'full_house': 15,
    'flush': 20,
    'four_of_a_kind': 25,
    'straight_flush': 50,
    'royal_flush': 100,
  };
  
  evaluateWeek(triggers: DailyTrigger[]): ComboResult {
    // Group triggers by type
    const byType = new Map<TriggerType, number>();
    for (const trigger of triggers) {
      byType.set(trigger.type, (byType.get(trigger.type) || 0) + 1);
    }
    
    const counts = Array.from(byType.values()).sort((a, b) => b - a);
    const uniqueTypes = byType.size;
    const totalTriggers = triggers.length;
    
    // Evaluate hand (highest first)
    let handType: ComboHandType | null = null;
    
    // Royal Flush: All 5 types, perfect execution
    if (uniqueTypes === 5 && counts.every(c => c >= 1) && this.isPerfectSequence(triggers)) {
      handType = 'royal_flush';
    }
    // Straight Flush: 5 consecutive days, same category
    else if (this.isConsecutiveDays(triggers, 5) && this.hasCategoryMatch(triggers)) {
      handType = 'straight_flush';
    }
    // Four of a Kind
    else if (counts[0] >= 4) {
      handType = 'four_of_a_kind';
    }
    // Flush: 5 of same type
    else if (counts[0] >= 5) {
      handType = 'flush';
    }
    // Full House: 3 + 2
    else if (counts[0] >= 3 && counts[1] >= 2) {
      handType = 'full_house';
    }
    // Straight: 5 different in sequence
    else if (this.isConsecutiveDays(triggers, 5) && uniqueTypes >= 5) {
      handType = 'straight';
    }
    // Three of a Kind
    else if (counts[0] >= 3) {
      handType = 'three_of_a_kind';
    }
    // Two Pair
    else if (counts[0] >= 2 && counts[1] >= 2) {
      handType = 'two_pair';
    }
    // Pair
    else if (counts[0] >= 2) {
      handType = 'pair';
    }
    
    return {
      triggers,
      handType,
      multiplier: handType ? this.HAND_VALUES[handType] : 1,
      breakdown: Object.fromEntries(byType),
    };
  }
  
  private isConsecutiveDays(triggers: DailyTrigger[], required: number): boolean {
    const days = [...new Set(triggers.map(t => t.dayNumber))].sort((a, b) => a - b);
    let consecutive = 1;
    
    for (let i = 1; i < days.length; i++) {
      if (days[i] - days[i-1] === 1) {
        consecutive++;
        if (consecutive >= required) return true;
      } else {
        consecutive = 1;
      }
    }
    
    return consecutive >= required;
  }
  
  private hasCategoryMatch(triggers: DailyTrigger[]): boolean {
    // Define categories
    const categories: Record<string, TriggerType[]> = {
      betting: ['first_bloom', 'perfect_read'],
      farming: ['growth_spurt', 'trouble_slayer'],
      companion: ['simulin_sync'],
    };
    
    // Check if all triggers are from same category
    for (const types of Object.values(categories)) {
      if (triggers.every(t => types.includes(t.type))) {
        return true;
      }
    }
    return false;
  }
  
  private isPerfectSequence(triggers: DailyTrigger[]): boolean {
    // Perfect sequence: all 5 trigger types in optimal order
    const idealOrder: TriggerType[] = [
      'first_bloom', 'growth_spurt', 'trouble_slayer', 'perfect_read', 'simulin_sync'
    ];
    
    const byDay = new Map<number, TriggerType>();
    for (const t of triggers) {
      if (!byDay.has(t.dayNumber)) {
        byDay.set(t.dayNumber, t.type);
      }
    }
    
    const sequence = Array.from(byDay.entries())
      .sort(([a], [b]) => a - b)
      .map(([_, type]) => type);
    
    return sequence.length === 5 && 
           sequence.every((type, i) => type === idealOrder[i]);
  }
}

interface ComboResult {
  triggers: DailyTrigger[];
  handType: ComboHandType | null;
  multiplier: number;
  breakdown: Record<TriggerType, number>;
}
```

---

## Part V: UI Engineering Patterns

### Component Architecture

```typescript
// Compound Component Pattern for complex UI
interface SlotMachineContext {
  spinning: boolean;
  result: SlotResult | null;
  spin: () => void;
}

const SlotMachineContext = createContext<SlotMachineContext | null>(null);

function SlotMachine({ children }: { children: React.ReactNode }) {
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState<SlotResult | null>(null);
  
  const spin = useCallback(async () => {
    setSpinning(true);
    const newResult = await api.spin();
    setResult(newResult);
    setSpinning(false);
  }, []);
  
  return (
    <SlotMachineContext.Provider value={{ spinning, result, spin }}>
      <div className="slot-machine">{children}</div>
    </SlotMachineContext.Provider>
  );
}

// Sub-components
SlotMachine.Reel = function Reel({ index }: { index: number }) {
  const ctx = useContext(SlotMachineContext);
  // ...render reel
};

SlotMachine.SpinButton = function SpinButton() {
  const ctx = useContext(SlotMachineContext);
  return (
    <button onClick={ctx?.spin} disabled={ctx?.spinning}>
      {ctx?.spinning ? 'Spinning...' : 'SPIN'}
    </button>
  );
};

// Usage
<SlotMachine>
  <SlotMachine.Reel index={0} />
  <SlotMachine.Reel index={1} />
  <SlotMachine.Reel index={2} />
  <SlotMachine.SpinButton />
</SlotMachine>
```

### Animation Patterns

```typescript
import { motion, AnimatePresence, useSpring, useTransform } from 'framer-motion';

// Juice: Satisfying feedback animations
const JUICE_VARIANTS = {
  // Pop in
  pop: {
    initial: { scale: 0, opacity: 0 },
    animate: { scale: 1, opacity: 1 },
    exit: { scale: 0, opacity: 0 },
    transition: { type: 'spring', stiffness: 500, damping: 30 },
  },
  
  // Bounce
  bounce: {
    animate: { 
      y: [0, -10, 0],
      transition: { duration: 0.3, times: [0, 0.5, 1] }
    },
  },
  
  // Shake (for errors/wrong)
  shake: {
    animate: { 
      x: [0, -10, 10, -10, 10, 0],
      transition: { duration: 0.4 }
    },
  },
  
  // Pulse (for attention)
  pulse: {
    animate: { 
      scale: [1, 1.05, 1],
      transition: { duration: 0.3, repeat: 2 }
    },
  },
};

// Number counter animation
function AnimatedNumber({ value }: { value: number }) {
  const spring = useSpring(value, { stiffness: 100, damping: 30 });
  const display = useTransform(spring, (v) => Math.floor(v).toLocaleString());
  
  useEffect(() => {
    spring.set(value);
  }, [value, spring]);
  
  return <motion.span>{display}</motion.span>;
}

// Stagger children animation
function StaggeredList({ items }: { items: React.ReactNode[] }) {
  return (
    <motion.ul
      initial="hidden"
      animate="visible"
      variants={{
        visible: { transition: { staggerChildren: 0.1 } },
      }}
    >
      {items.map((item, i) => (
        <motion.li
          key={i}
          variants={{
            hidden: { opacity: 0, x: -20 },
            visible: { opacity: 1, x: 0 },
          }}
        >
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Responsive Game UI

```typescript
// Hook for responsive game scaling
function useGameScale() {
  const [scale, setScale] = useState(1);
  const containerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const updateScale = () => {
      if (!containerRef.current) return;
      
      const container = containerRef.current;
      const parent = container.parentElement;
      if (!parent) return;
      
      const DESIGN_WIDTH = 390;  // iPhone 12/13 width
      const DESIGN_HEIGHT = 844;
      
      const scaleX = parent.clientWidth / DESIGN_WIDTH;
      const scaleY = parent.clientHeight / DESIGN_HEIGHT;
      
      // Use minimum to ensure everything fits
      setScale(Math.min(scaleX, scaleY, 1.5)); // Cap at 1.5x
    };
    
    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, []);
  
  return { scale, containerRef };
}

// Usage
function GameScreen() {
  const { scale, containerRef } = useGameScale();
  
  return (
    <div className="game-container" ref={containerRef}>
      <div 
        className="game-content"
        style={{ transform: `scale(${scale})`, transformOrigin: 'top center' }}
      >
        {/* Fixed-size game UI designed for 390x844 */}
      </div>
    </div>
  );
}
```

---

## Part VI: Data Architecture

### Schema Design Principles

```typescript
// Use branded types for IDs
type SeasonId = string & { readonly brand: unique symbol };
type SimulinId = string & { readonly brand: unique symbol };
type UserId = string & { readonly brand: unique symbol };

function createSeasonId(): SeasonId {
  return `season_${crypto.randomUUID()}` as SeasonId;
}

// Drizzle schema with relations
import { sqliteTable, text, integer, real } from 'drizzle-orm/sqlite-core';
import { relations } from 'drizzle-orm';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull(),
});

export const seasons = sqliteTable('seasons', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => users.id),
  seasonNumber: integer('season_number').notNull(),
  currentDay: integer('current_day').notNull().default(1),
  phase: text('phase', { enum: ['planting', 'growth', 'harvest'] }).notNull(),
  jackpotContribution: real('jackpot_contribution').notNull().default(0),
  startedAt: integer('started_at', { mode: 'timestamp' }).notNull(),
  completedAt: integer('completed_at', { mode: 'timestamp' }),
});

export const seasonsRelations = relations(seasons, ({ one, many }) => ({
  user: one(users, {
    fields: [seasons.userId],
    references: [users.id],
  }),
  triggers: many(dailyTriggers),
  simulins: many(simulins),
}));

export const dailyTriggers = sqliteTable('daily_triggers', {
  id: text('id').primaryKey(),
  seasonId: text('season_id').notNull().references(() => seasons.id),
  dayNumber: integer('day_number').notNull(),
  triggerType: text('trigger_type').notNull(),
  earnedAt: integer('earned_at', { mode: 'timestamp' }).notNull(),
  metadata: text('metadata', { mode: 'json' }),
});

export const simulins = sqliteTable('simulins', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => users.id),
  seasonId: text('season_id').references(() => seasons.id),
  name: text('name').notNull(),
  stage: text('stage', { enum: ['sproutling', 'cultivar', 'bloomform', 'legendary'] }).notNull(),
  path: text('path', { enum: ['tender', 'watcher', 'lucky'] }),
  bondLevel: integer('bond_level').notNull().default(1),
  bondXP: integer('bond_xp').notNull().default(0),
  personality: text('personality', { mode: 'json' }).notNull(),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull(),
});
```

### Logging & Telemetry

```typescript
interface GameEvent {
  type: string;
  timestamp: Date;
  sessionId: string;
  userId?: string;
  properties: Record<string, any>;
}

class Telemetry {
  private queue: GameEvent[] = [];
  private flushInterval: Timer;
  
  constructor(
    private endpoint: string,
    private batchSize = 10,
    private flushIntervalMs = 5000
  ) {
    this.flushInterval = setInterval(() => this.flush(), flushIntervalMs);
  }
  
  track(type: string, properties: Record<string, any> = {}): void {
    const event: GameEvent = {
      type,
      timestamp: new Date(),
      sessionId: this.getSessionId(),
      userId: this.getUserId(),
      properties: {
        ...properties,
        // Auto-add context
        url: typeof window !== 'undefined' ? window.location.href : undefined,
        userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : undefined,
      },
    };
    
    this.queue.push(event);
    
    if (this.queue.length >= this.batchSize) {
      this.flush();
    }
  }
  
  private async flush(): Promise<void> {
    if (this.queue.length === 0) return;
    
    const batch = this.queue.splice(0, this.batchSize);
    
    try {
      await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ events: batch }),
      });
    } catch (error) {
      // Re-queue failed events (with limit)
      if (this.queue.length < 100) {
        this.queue.unshift(...batch);
      }
      console.error('Telemetry flush failed:', error);
    }
  }
  
  private getSessionId(): string {
    // Session ID from storage or generate new
    let sessionId = sessionStorage.getItem('fip_session_id');
    if (!sessionId) {
      sessionId = crypto.randomUUID();
      sessionStorage.setItem('fip_session_id', sessionId);
    }
    return sessionId;
  }
  
  private getUserId(): string | undefined {
    // Get from auth state
    return undefined; // Implement based on auth system
  }
  
  destroy(): void {
    clearInterval(this.flushInterval);
    this.flush();
  }
}

// Standard events
const telemetry = new Telemetry('/api/telemetry');

// Usage
telemetry.track('day_started', { dayNumber: 5, phase: 'growth' });
telemetry.track('bet_placed', { potId: 'water', betType: 'raise', amount: 100 });
telemetry.track('trigger_earned', { triggerType: 'perfect_read' });
telemetry.track('session_ended', { duration: 1234, daysPlayed: 3 });
```

### Security Patterns

```typescript
// Input validation with Zod
import { z } from 'zod';

const PlaceBetSchema = z.object({
  potId: z.enum(['water', 'sun', 'pest', 'growth']),
  betType: z.enum(['fold', 'call', 'raise', 'all-in']),
  amount: z.number().int().min(0).max(10000),
});

// Rate limiting
class RateLimiter {
  private requests: Map<string, number[]> = new Map();
  
  constructor(
    private windowMs: number,
    private maxRequests: number
  ) {}
  
  isAllowed(key: string): boolean {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // Get and filter old requests
    const timestamps = (this.requests.get(key) || [])
      .filter(t => t > windowStart);
    
    if (timestamps.length >= this.maxRequests) {
      return false;
    }
    
    timestamps.push(now);
    this.requests.set(key, timestamps);
    return true;
  }
}

// Server-side validation wrapper
function validateRequest<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  context: { userId: string; ip: string }
): T {
  // Rate limit check
  const rateLimiter = new RateLimiter(60000, 100); // 100 req/min
  if (!rateLimiter.isAllowed(context.userId)) {
    throw new Error('Rate limit exceeded');
  }
  
  // Schema validation
  const result = schema.safeParse(data);
  if (!result.success) {
    console.warn('Validation failed', { 
      userId: context.userId, 
      errors: result.error.errors 
    });
    throw new Error('Invalid request data');
  }
  
  return result.data;
}

// Anti-cheat: Server-authoritative game state
class GameStateValidator {
  validateDayAdvance(
    currentState: GameState,
    proposedState: GameState
  ): boolean {
    // Server recalculates expected state
    const expectedState = this.calculateNextState(currentState);
    
    // Compare critical values
    if (proposedState.coins > expectedState.maxPossibleCoins) {
      this.flagSuspicious('coin_manipulation', currentState.userId);
      return false;
    }
    
    if (proposedState.dayNumber !== expectedState.dayNumber) {
      this.flagSuspicious('day_skip', currentState.userId);
      return false;
    }
    
    return true;
  }
  
  private calculateNextState(current: GameState): ExpectedState {
    // Server-side calculation of valid state ranges
    return {} as ExpectedState;
  }
  
  private flagSuspicious(type: string, userId: string): void {
    // Log for review
    console.warn('Suspicious activity', { type, userId });
  }
}
```

---

## Part VII: Tutorial System Design

### Progressive Disclosure Pattern

```typescript
interface TutorialStep {
  id: string;
  trigger: TutorialTrigger;
  content: TutorialContent;
  completion: CompletionCondition;
  next?: string;
}

type TutorialTrigger = 
  | { type: 'first_visit'; screen: string }
  | { type: 'action'; action: string }
  | { type: 'state'; condition: (state: GameState) => boolean }
  | { type: 'time'; delayMs: number };

interface TutorialContent {
  title: string;
  body: string;
  highlight?: string;  // CSS selector to highlight
  position?: 'top' | 'bottom' | 'left' | 'right' | 'center';
  character?: 'simulin' | 'npc';
  allowSkip?: boolean;
}

type CompletionCondition = 
  | { type: 'click'; target: string }
  | { type: 'action'; action: string }
  | { type: 'dismiss' }
  | { type: 'state'; condition: (state: GameState) => boolean };

const TUTORIAL_FLOW: TutorialStep[] = [
  {
    id: 'welcome',
    trigger: { type: 'first_visit', screen: 'farm' },
    content: {
      title: 'Welcome to Purria!',
      body: 'Your adventure in tulip farming begins here.',
      character: 'simulin',
      position: 'center',
    },
    completion: { type: 'dismiss' },
    next: 'intro_hex',
  },
  {
    id: 'intro_hex',
    trigger: { type: 'action', action: 'tutorial_continue' },
    content: {
      title: 'Your Farm',
      body: 'Each hex is a plot for growing tulips. Tap one to plant!',
      highlight: '.hex-grid',
      position: 'bottom',
    },
    completion: { type: 'action', action: 'hex_tap' },
    next: 'intro_pots',
  },
  {
    id: 'intro_pots',
    trigger: { type: 'action', action: 'plant_tulip' },
    content: {
      title: 'The Meta-Pots',
      body: 'These four pots fill based on daily events. Place bets on which will hit their threshold!',
      highlight: '.pot-display',
      position: 'top',
    },
    completion: { type: 'click', target: '.pot-display' },
    next: 'first_bet',
  },
  // ... more steps
];

class TutorialManager {
  private completedSteps: Set<string> = new Set();
  private currentStep: TutorialStep | null = null;
  
  constructor(
    private steps: TutorialStep[],
    private onShow: (step: TutorialStep) => void,
    private onHide: () => void
  ) {
    this.loadProgress();
  }
  
  checkTriggers(context: { screen: string; action?: string; state: GameState }): void {
    for (const step of this.steps) {
      if (this.completedSteps.has(step.id)) continue;
      if (this.currentStep?.id === step.id) continue;
      
      if (this.matchesTrigger(step.trigger, context)) {
        this.showStep(step);
        break;
      }
    }
  }
  
  private matchesTrigger(trigger: TutorialTrigger, context: any): boolean {
    switch (trigger.type) {
      case 'first_visit':
        return context.screen === trigger.screen && 
               !this.hasVisited(trigger.screen);
      case 'action':
        return context.action === trigger.action;
      case 'state':
        return trigger.condition(context.state);
      default:
        return false;
    }
  }
  
  private showStep(step: TutorialStep): void {
    this.currentStep = step;
    this.onShow(step);
  }
  
  completeCurrentStep(): void {
    if (!this.currentStep) return;
    
    this.completedSteps.add(this.currentStep.id);
    this.saveProgress();
    
    const nextId = this.currentStep.next;
    this.currentStep = null;
    this.onHide();
    
    if (nextId) {
      const nextStep = this.steps.find(s => s.id === nextId);
      if (nextStep && nextStep.trigger.type === 'action') {
        // Auto-show chained steps
        this.showStep(nextStep);
      }
    }
  }
  
  private loadProgress(): void {
    const saved = localStorage.getItem('tutorial_progress');
    if (saved) {
      this.completedSteps = new Set(JSON.parse(saved));
    }
  }
  
  private saveProgress(): void {
    localStorage.setItem(
      'tutorial_progress', 
      JSON.stringify([...this.completedSteps])
    );
  }
  
  private hasVisited(screen: string): boolean {
    return localStorage.getItem(`visited_${screen}`) === 'true';
  }
  
  reset(): void {
    this.completedSteps.clear();
    localStorage.removeItem('tutorial_progress');
  }
}
```

### Contextual Help System

```typescript
interface HelpTopic {
  id: string;
  title: string;
  summary: string;
  content: string;
  relatedTopics?: string[];
  triggers?: string[];  // UI elements that show this help
}

const HELP_TOPICS: HelpTopic[] = [
  {
    id: 'betting',
    title: 'How Betting Works',
    summary: 'Place bets on which pots will fill',
    content: `
      Each day, the four Meta-Pots fill based on events on your farm.
      
      **Bet Types:**
      - **Fold**: Skip this pot (safe, no reward)
      - **Call**: Small bet, small reward
      - **Raise**: Medium bet, medium reward  
      - **All-In**: Big bet, big reward (or loss!)
      
      **Thresholds:**
      Pots have thresholds at 50%, 80%, and 100%. Higher thresholds = higher payouts.
    `,
    relatedTopics: ['pots', 'triggers', 'combos'],
    triggers: ['.bet-button', '.pot-display'],
  },
  // ... more topics
];

function HelpButton({ topicId }: { topicId: string }) {
  const [open, setOpen] = useState(false);
  const topic = HELP_TOPICS.find(t => t.id === topicId);
  
  if (!topic) return null;
  
  return (
    <>
      <button 
        onClick={() => setOpen(true)}
        className="help-button"
        aria-label={`Help: ${topic.title}`}
      >
        ?
      </button>
      
      <Dialog open={open} onClose={() => setOpen(false)}>
        <Dialog.Title>{topic.title}</Dialog.Title>
        <Dialog.Content>
          <Markdown>{topic.content}</Markdown>
          
          {topic.relatedTopics && (
            <div className="related-topics">
              <h4>Related:</h4>
              {topic.relatedTopics.map(id => (
                <HelpLink key={id} topicId={id} />
              ))}
            </div>
          )}
        </Dialog.Content>
      </Dialog>
    </>
  );
}
```

---

## Part VIII: Quality Assurance

### Testing Strategy

```typescript
// Unit test example (Vitest)
import { describe, it, expect } from 'vitest';
import { ComboEngine } from './combo-engine';

describe('ComboEngine', () => {
  const engine = new ComboEngine();
  
  describe('evaluateWeek', () => {
    it('detects pair with 2 matching triggers', () => {
      const triggers = [
        { type: 'first_bloom', dayNumber: 1, earnedAt: new Date() },
        { type: 'first_bloom', dayNumber: 2, earnedAt: new Date() },
      ];
      
      const result = engine.evaluateWeek(triggers);
      
      expect(result.handType).toBe('pair');
      expect(result.multiplier).toBe(2);
    });
    
    it('detects three of a kind over pair', () => {
      const triggers = [
        { type: 'perfect_read', dayNumber: 1, earnedAt: new Date() },
        { type: 'perfect_read', dayNumber: 2, earnedAt: new Date() },
        { type: 'perfect_read', dayNumber: 3, earnedAt: new Date() },
        { type: 'first_bloom', dayNumber: 4, earnedAt: new Date() },
        { type: 'first_bloom', dayNumber: 5, earnedAt: new Date() },
      ];
      
      const result = engine.evaluateWeek(triggers);
      
      // Full house beats three of a kind
      expect(result.handType).toBe('full_house');
      expect(result.multiplier).toBe(15);
    });
  });
});

// Integration test example
describe('Betting Flow', () => {
  it('completes full betting cycle', async () => {
    const { gameState, bettingSystem } = createTestGame();
    
    // Place bets
    bettingSystem.placeBet('water', 'raise', 100);
    bettingSystem.placeBet('sun', 'fold', 0);
    
    // Simulate day completion
    gameState.advanceToResolution();
    
    // Resolve bets
    const results = bettingSystem.resolveBets(gameState.pots);
    
    expect(results).toHaveLength(2);
    expect(results[0].potId).toBe('water');
    expect(results[1].potId).toBe('sun');
    expect(results[1].payout).toBe(0); // Fold always 0
  });
});
```

### Code Review Checklist

```markdown
## Code Review Checklist

### Correctness
- [ ] Logic is correct and handles edge cases
- [ ] No off-by-one errors
- [ ] Null/undefined handled appropriately
- [ ] Async operations handle errors

### Type Safety
- [ ] No `any` types without justification
- [ ] Proper use of generics
- [ ] Return types explicit on public APIs
- [ ] Zod schemas match TypeScript types

### Performance
- [ ] No unnecessary re-renders (React.memo where needed)
- [ ] Large lists are virtualized
- [ ] Expensive calculations are memoized
- [ ] No memory leaks (cleanup in useEffect)

### Security
- [ ] User input is validated
- [ ] No secrets in client code
- [ ] Server validates all mutations
- [ ] Rate limiting considered

### Maintainability
- [ ] Functions are small and focused
- [ ] Clear variable/function names
- [ ] Comments explain "why", not "what"
- [ ] No magic numbers

### Testing
- [ ] Unit tests for logic
- [ ] Edge cases covered
- [ ] Tests are readable

### Accessibility
- [ ] Interactive elements are keyboard accessible
- [ ] ARIA labels where needed
- [ ] Color contrast sufficient
- [ ] Focus management correct
```

---

## Reference Documents

The following reference documents provide deep-dive implementations:

| Document | Purpose |
|----------|---------|
| `references/game-patterns.md` | Extended patterns: ECS, behavior trees, scene management |
| `references/casino-implementation.md` | Full casino game implementations: poker, blackjack, slots |
| `references/reward-progression.md` | Complete reward systems, balancing, economy design |
| `references/game-ui-patterns.md` | UI component library, responsive patterns, accessibility |
| `references/tutorial-onboarding.md` | Tutorial flows, contextual help, player guidance |
| `references/architecture-quality.md` | Code organization, refactoring patterns, documentation |
| `references/data-infrastructure.md` | Schema design, migrations, telemetry, security |

---

*Game Engineering Team - Building the Best Game Ever*
*For Farming in Purria v3*

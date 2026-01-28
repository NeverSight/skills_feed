---
name: react-game-ui
description: React game UI patterns using shadcn/ui, Tailwind, and Framer Motion for polished game interfaces. Use when building HUDs, resource bars, scoreboards, modals, tooltips, card components, or any game UI. Includes micro-interactions, animations, responsive layouts, and accessibility for games. Triggers on requests for game interface components, UI animations, or shadcn/ui game patterns.
---

# React Game UI

Production-ready UI patterns for game interfaces using shadcn/ui, Tailwind, and Framer Motion.

## Core Components

### Resource Bar

```tsx
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

interface ResourceBarProps {
  icon: React.ReactNode;
  value: number;
  maxValue?: number;
  label: string;
  color?: 'gold' | 'green' | 'blue' | 'red';
}

const colorMap = {
  gold: 'from-amber-400 to-yellow-500',
  green: 'from-emerald-400 to-green-500',
  blue: 'from-sky-400 to-blue-500',
  red: 'from-rose-400 to-red-500',
};

export function ResourceBar({ 
  icon, 
  value, 
  maxValue, 
  label, 
  color = 'gold' 
}: ResourceBarProps) {
  return (
    <div className="flex items-center gap-2 bg-black/40 backdrop-blur-sm rounded-lg px-3 py-2">
      <div className={cn(
        'w-8 h-8 rounded-full flex items-center justify-center',
        `bg-gradient-to-br ${colorMap[color]}`
      )}>
        {icon}
      </div>
      <div className="flex flex-col">
        <span className="text-xs text-white/60 uppercase tracking-wide">{label}</span>
        <motion.span 
          key={value}
          initial={{ scale: 1.2, color: '#ffd700' }}
          animate={{ scale: 1, color: '#ffffff' }}
          className="text-lg font-bold text-white tabular-nums"
        >
          {value.toLocaleString()}
          {maxValue && <span className="text-white/40">/{maxValue}</span>}
        </motion.span>
      </div>
    </div>
  );
}
```

### Animated Counter

```tsx
import { useEffect, useRef } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';

interface AnimatedCounterProps {
  value: number;
  duration?: number;
  className?: string;
}

export function AnimatedCounter({ value, duration = 0.5, className }: AnimatedCounterProps) {
  const spring = useSpring(0, { duration: duration * 1000 });
  const display = useTransform(spring, (v) => Math.floor(v).toLocaleString());
  
  useEffect(() => {
    spring.set(value);
  }, [spring, value]);
  
  return <motion.span className={className}>{display}</motion.span>;
}
```

### Meter/Progress Component

```tsx
interface MeterProps {
  value: number;         // 0-100
  label: string;
  tier?: 'mini' | 'major' | 'grand';
  showValue?: boolean;
}

const tierStyles = {
  mini: 'h-2',
  major: 'h-3',
  grand: 'h-4',
};

export function Meter({ value, label, tier = 'mini', showValue = true }: MeterProps) {
  const clampedValue = Math.max(0, Math.min(100, value));
  
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm">
        <span className="text-white/80">{label}</span>
        {showValue && (
          <span className="text-white/60 tabular-nums">{clampedValue}%</span>
        )}
      </div>
      <div className={cn(
        'w-full bg-white/10 rounded-full overflow-hidden',
        tierStyles[tier]
      )}>
        <motion.div
          className={cn(
            'h-full rounded-full',
            clampedValue >= 50 
              ? 'bg-gradient-to-r from-emerald-500 to-green-400' 
              : 'bg-gradient-to-r from-amber-500 to-orange-400'
          )}
          initial={{ width: 0 }}
          animate={{ width: `${clampedValue}%` }}
          transition={{ type: 'spring', stiffness: 100, damping: 15 }}
        />
      </div>
    </div>
  );
}
```

### Game Card Component

```tsx
import { motion } from 'framer-motion';

interface GameCardProps {
  suit: 'hearts' | 'diamonds' | 'clubs' | 'spades';
  rank: string;
  faceDown?: boolean;
  onClick?: () => void;
}

export function GameCard({ suit, rank, faceDown = false, onClick }: GameCardProps) {
  const isRed = suit === 'hearts' || suit === 'diamonds';
  
  return (
    <motion.div
      className="relative w-[90px] h-[126px] cursor-pointer perspective-1000"
      onClick={onClick}
      whileHover={{ y: -8, transition: { duration: 0.2 } }}
      whileTap={{ scale: 0.95 }}
    >
      <motion.div
        className="w-full h-full relative"
        style={{ transformStyle: 'preserve-3d' }}
        animate={{ rotateY: faceDown ? 180 : 0 }}
        transition={{ duration: 0.6, type: 'spring' }}
      >
        {/* Front */}
        <div 
          className={cn(
            'absolute inset-0 rounded-lg shadow-lg backface-hidden',
            'bg-white border-2 border-gray-200',
            'flex flex-col items-center justify-center'
          )}
        >
          <span className={cn(
            'text-2xl font-bold',
            isRed ? 'text-red-600' : 'text-gray-900'
          )}>
            {rank}
          </span>
          <span className="text-3xl">{suitSymbol(suit)}</span>
        </div>
        
        {/* Back */}
        <div 
          className="absolute inset-0 rounded-lg shadow-lg backface-hidden bg-gradient-to-br from-indigo-600 to-purple-700"
          style={{ transform: 'rotateY(180deg)' }}
        >
          <div className="w-full h-full rounded-lg border-4 border-white/20 flex items-center justify-center">
            <div className="w-12 h-12 rounded-full bg-white/10" />
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

function suitSymbol(suit: string) {
  const symbols = { hearts: '♥', diamonds: '♦', clubs: '♣', spades: '♠' };
  return symbols[suit] || '';
}
```

## Micro-Interactions

### Button with Feedback

```tsx
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';

export function GameButton({ 
  children, 
  onClick, 
  variant = 'default',
  ...props 
}: React.ComponentProps<typeof Button>) {
  return (
    <Button
      asChild
      variant={variant}
      onClick={onClick}
      {...props}
    >
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      >
        {children}
      </motion.button>
    </Button>
  );
}
```

### Coin Pop Animation

```tsx
import { motion, AnimatePresence } from 'framer-motion';

interface CoinPopProps {
  amount: number;
  position: { x: number; y: number };
  onComplete: () => void;
}

export function CoinPop({ amount, position, onComplete }: CoinPopProps) {
  return (
    <motion.div
      className="fixed pointer-events-none z-50 text-2xl font-bold text-yellow-400"
      style={{ left: position.x, top: position.y }}
      initial={{ opacity: 1, y: 0, scale: 0.5 }}
      animate={{ opacity: 0, y: -60, scale: 1.2 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1, ease: 'easeOut' }}
      onAnimationComplete={onComplete}
    >
      +{amount} 🪙
    </motion.div>
  );
}
```

### Shake on Error

```tsx
const shakeAnimation = {
  x: [0, -10, 10, -10, 10, 0],
  transition: { duration: 0.4 }
};

export function ShakeOnError({ error, children }) {
  return (
    <motion.div animate={error ? shakeAnimation : {}}>
      {children}
    </motion.div>
  );
}
```

## Layout Patterns

### Game HUD Layout

```tsx
export function GameLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative w-full h-screen overflow-hidden bg-gradient-to-br from-stone-900 via-stone-950 to-black">
      {/* Top Bar */}
      <header className="absolute top-0 left-0 right-0 z-20 p-4 flex justify-between items-start">
        <ResourceBar icon={<Flower />} value={resources.tulipBulbs} label="Tulips" color="green" />
        <Scoreboard day={time.day} score={score} />
      </header>
      
      {/* Main Content */}
      <main className="absolute inset-0 flex items-center justify-center pt-20 pb-20">
        {children}
      </main>
      
      {/* Bottom Bar */}
      <footer className="absolute bottom-0 left-0 right-0 z-20 p-4 flex justify-center">
        <PhaseControls />
      </footer>
      
      {/* Side Panel */}
      <aside className="absolute top-20 right-0 bottom-20 z-10 w-80 p-4">
        <MetaPotPanel />
      </aside>
    </div>
  );
}
```

### Responsive Game Board

```tsx
export function GameBoard({ children }: { children: React.ReactNode }) {
  return (
    <div className="w-full h-full flex items-center justify-center p-4">
      <div className={cn(
        'relative',
        'w-full max-w-[min(90vw,90vh)]',
        'aspect-square'
      )}>
        {children}
      </div>
    </div>
  );
}
```

## Modal & Dialog Patterns

### Game Modal with shadcn

```tsx
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { motion, AnimatePresence } from 'framer-motion';

export function GameModal({ open, onOpenChange, title, children }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="bg-gradient-to-br from-stone-800 to-stone-900 border-amber-500/30">
        <DialogHeader>
          <DialogTitle className="text-amber-400 text-xl">{title}</DialogTitle>
        </DialogHeader>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
        >
          {children}
        </motion.div>
      </DialogContent>
    </Dialog>
  );
}
```

### Tooltip for Game Elements

```tsx
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

export function GameTooltip({ children, content }) {
  return (
    <TooltipProvider delayDuration={300}>
      <Tooltip>
        <TooltipTrigger asChild>{children}</TooltipTrigger>
        <TooltipContent 
          className="bg-stone-900 border-amber-500/30 text-white"
          sideOffset={8}
        >
          {content}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
```

## Accessibility for Games

### Skip Animation Preference

```tsx
import { useReducedMotion } from 'framer-motion';

export function AnimatedElement({ children }) {
  const shouldReduceMotion = useReducedMotion();
  
  return (
    <motion.div
      animate={{ opacity: 1, y: 0 }}
      transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

### Screen Reader Announcements

```tsx
import { useEffect, useRef } from 'react';

export function useAnnounce() {
  const ref = useRef<HTMLDivElement>(null);
  
  const announce = (message: string) => {
    if (ref.current) {
      ref.current.textContent = message;
    }
  };
  
  return { announce, AnnouncerRegion: () => (
    <div
      ref={ref}
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    />
  )};
}

// Usage
const { announce, AnnouncerRegion } = useAnnounce();
announce('You won 500 coins!');
```

## Performance Tips

1. **Memoize heavy components**: `React.memo()` for hex cells, cards
2. **Use CSS transforms**: GPU-accelerated vs layout-triggering properties
3. **Virtualize large lists**: Only render visible items
4. **Debounce rapid updates**: Score counters, resource bars
5. **Lazy load modals**: Don't mount until needed

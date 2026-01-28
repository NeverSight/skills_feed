---
name: autonomous-agent-gaming
description: Build autonomous game-playing agents using AI and reinforcement learning. Covers game environments, agent decision-making, strategy development, and performance optimization. Use when creating game-playing bots, testing game AI, strategic decision-making systems, or game theory applications.
---

# Autonomous Agent Gaming

Build sophisticated game-playing agents that learn strategies, adapt to opponents, and master complex games through AI and reinforcement learning.

## Overview

Autonomous game agents combine:
- **Game Environment Interface**: Connect to game rules and state
- **Decision-Making Systems**: Choose optimal actions
- **Learning Mechanisms**: Improve through experience
- **Strategy Development**: Long-term planning and adaptation

### Applications

- Chess and board game masters
- Real-time strategy (RTS) game bots
- Video game autonomous players
- Game theory research
- AI testing and benchmarking
- Entertainment and challenge systems

## Quick Start

Run example agents with:

```bash
# Rule-based agent
python examples/rule_based_agent.py

# Minimax with alpha-beta pruning
python examples/minimax_agent.py

# Monte Carlo Tree Search
python examples/mcts_agent.py

# Q-Learning agent
python examples/qlearning_agent.py

# Chess engine
python examples/chess_engine.py

# Game theory analysis
python scripts/game_theory_analyzer.py

# Benchmark agents
python scripts/agent_benchmark.py
```

## Game Agent Architectures

### 1. Rule-Based Agents

Use predefined rules and heuristics. See full implementation in `examples/rule_based_agent.py`.

**Key Concepts:**
- Difficulty levels control strategy depth
- Evaluation combines material, position, and control factors
- Fast decision-making suitable for real-time games
- Easy to customize and understand

**Usage Example:**
```python
from examples.rule_based_agent import RuleBasedGameAgent

agent = RuleBasedGameAgent(difficulty="hard")
best_move = agent.decide_action(game_state)
```

### 2. Minimax with Alpha-Beta Pruning

Optimal decision-making for turn-based games. See `examples/minimax_agent.py`.

**Key Concepts:**
- Exhaustive tree search up to fixed depth
- Alpha-beta pruning eliminates impossible branches
- Guarantees optimal play within search depth
- Evaluation function determines move quality

**Performance Characteristics:**
- Time complexity: O(b^(d/2)) with pruning vs O(b^d) without
- Space complexity: O(b*d)
- Adjustable depth for speed/quality tradeoff

**Usage Example:**
```python
from examples.minimax_agent import MinimaxGameAgent

agent = MinimaxGameAgent(max_depth=6)
best_move = agent.get_best_move(game_state)
```

### 3. Monte Carlo Tree Search (MCTS)

Probabilistic game tree exploration. Full implementation in `examples/mcts_agent.py`.

**Key Concepts:**
- Four-phase algorithm: Selection, Expansion, Simulation, Backpropagation
- UCT (Upper Confidence bounds applied to Trees) balances exploration/exploitation
- Effective for games with high branching factors
- Anytime algorithm: more iterations = better decisions

**The UCT Formula:**
UCT = (child_value / child_visits) + c * sqrt(ln(parent_visits) / child_visits)

**Usage Example:**
```python
from examples.mcts_agent import MCTSAgent

agent = MCTSAgent(iterations=1000, exploration_constant=1.414)
best_move = agent.get_best_move(game_state)
```

### 4. Reinforcement Learning Agents

Learn through interaction with environment. See `examples/qlearning_agent.py`.

**Key Concepts:**
- Q-learning: model-free, off-policy learning
- Epsilon-greedy: balance exploration vs exploitation
- Update rule: Q(s,a) += α[r + γ*max_a'Q(s',a') - Q(s,a)]
- Q-table stores state-action value estimates

**Hyperparameters:**
- α (learning_rate): How quickly to adapt to new information
- γ (discount_factor): Importance of future rewards
- ε (epsilon): Exploration probability

**Usage Example:**
```python
from examples.qlearning_agent import QLearningAgent

agent = QLearningAgent(learning_rate=0.1, discount_factor=0.99, epsilon=0.1)
action = agent.get_action(state)
agent.update_q_value(state, action, reward, next_state)
agent.decay_epsilon()  # Reduce exploration over time
```

## Game Environments

### Standard Interfaces

Create game environments compatible with agents. See `examples/game_environment.py` for base classes.

**Key Methods:**
- `reset()`: Initialize game state
- `step(action)`: Execute action, return (next_state, reward, done)
- `get_legal_actions(state)`: List valid moves
- `is_terminal(state)`: Check if game is over
- `render()`: Display game state

### OpenAI Gym Integration

Standard interface for game environments:

```python
import gym

# Create environment
env = gym.make('CartPole-v1')

# Initialize
state = env.reset()

# Run episode
done = False
while not done:
    action = agent.get_action(state)
    next_state, reward, done, info = env.step(action)
    agent.update(state, action, reward, next_state)
    state = next_state

env.close()
```

### Chess with python-chess

Full chess implementation in `examples/chess_engine.py`. Requires: `pip install python-chess`

**Features:**
- Full game rules and move validation
- Position evaluation based on material count
- Move history and undo functionality
- FEN notation support

**Quick Example:**
```python
from examples.chess_engine import ChessAgent

agent = ChessAgent()
result, moves = agent.play_game()
print(f"Game result: {result} in {moves} moves")
```

### Custom Game with Pygame

Extend `examples/game_environment.py` with pygame rendering:

```python
from examples.game_environment import PygameGameEnvironment

class MyGame(PygameGameEnvironment):
    def get_initial_state(self):
        # Return initial game state
        pass

    def apply_action(self, state, action):
        # Execute action, return new state
        pass

    def calculate_reward(self, state, action, next_state):
        # Return reward value
        pass

    def is_terminal(self, state):
        # Check if game is over
        pass

    def draw_state(self, state):
        # Render using pygame
        pass

game = MyGame()
game.render()
```

## Strategy Development

All strategy implementations are in `examples/strategy_modules.py`.

### 1. Opening Theory

Pre-computed best moves for game openings. Load from PGN files or opening databases.

**OpeningBook Features:**
- Fast lookup using position hashing
- Load from PGN, opening databases, or create custom books
- Fallback to other strategies when out of book

**Usage:**
```python
from examples.strategy_modules import OpeningBook

book = OpeningBook()
if book.in_opening(game_state):
    move = book.get_opening_move(game_state)
```

### 2. Endgame Tablebases

Pre-computed endgame solutions with optimal moves and distance-to-mate.

**Features:**
- Guaranteed optimal moves in endgame positions
- Distance-to-mate calculation
- Lookup by position hash

**Usage:**
```python
from examples.strategy_modules import EndgameTablebase

tablebase = EndgameTablebase()
if tablebase.in_tablebase(game_state):
    move = tablebase.get_best_endgame_move(game_state)
    dtm = tablebase.get_endgame_distance(game_state)
```

### 3. Multi-Stage Strategy

Combine different agents for different game phases using `AdaptiveGameAgent`.

**Strategy Selection:**
- **Opening (Material > 30)**: Use opening book or memorized lines
- **Middlegame (10-30)**: Use search-based engine (Minimax, MCTS)
- **Endgame (Material < 10)**: Use tablebase for optimal play

**Usage:**
```python
from examples.strategy_modules import AdaptiveGameAgent
from examples.minimax_agent import MinimaxGameAgent

agent = AdaptiveGameAgent(
    opening_book=book,
    middlegame_engine=MinimaxGameAgent(max_depth=6),
    endgame_tablebase=tablebase
)

move = agent.decide_action(game_state)
phase_info = agent.get_phase_info(game_state)
```

### 4. Composite Strategies

Combine multiple strategies with priority ordering using `CompositeStrategy`.

**Usage:**
```python
from examples.strategy_modules import CompositeStrategy

composite = CompositeStrategy([
    opening_strategy,
    endgame_strategy,
    default_search_strategy
])

move = composite.get_move(game_state)
active = composite.get_active_strategy(game_state)
```

## Performance Optimization

All optimization utilities are in `scripts/performance_optimizer.py`.

### 1. Transposition Tables

Cache evaluated positions to avoid re-computation. Especially effective with alpha-beta pruning.

**How it works:**
- Stores evaluation (score + depth + bound type)
- Hashes positions for fast lookup
- Only overwrites if new evaluation is deeper
- Thread-safe for parallel search

**Bound Types:**
- **exact**: Exact evaluation
- **lower**: Evaluation is at least this value
- **upper**: Evaluation is at most this value

**Usage:**
```python
from scripts.performance_optimizer import TranspositionTable

tt = TranspositionTable(max_size=1000000)

# Store evaluation
tt.store(position_hash, depth=6, score=150, flag='exact')

# Lookup
score = tt.lookup(position_hash, depth=6)
hit_rate = tt.hit_rate()
```

### 2. Killer Heuristic

Track moves that cause cutoffs at similar depths for move ordering improvement.

**Concept:**
- Killer moves are non-capture moves that caused beta cutoffs
- Likely to be good moves at other nodes of same depth
- Improves alpha-beta pruning efficiency

**Usage:**
```python
from scripts.performance_optimizer import KillerHeuristic

killers = KillerHeuristic(max_depth=20)

# When a cutoff occurs
killers.record_killer(move, depth=5)

# When ordering moves
killer_list = killers.get_killers(depth=5)
is_killer = killers.is_killer(move, depth=5)
```

### 3. Parallel Search

Parallelize game tree search across multiple threads.

**Usage:**
```python
from scripts.performance_optimizer import ParallelSearchCoordinator

coordinator = ParallelSearchCoordinator(num_threads=4)

# Parallel move evaluation
scores = coordinator.parallel_evaluate_moves(moves, evaluate_func)

# Parallel minimax
best_move, score = coordinator.parallel_minimax(root_moves, minimax_func)

coordinator.shutdown()
```

### 4. Search Statistics

Track and analyze search performance with `SearchStatistics`.

**Metrics:**
- Nodes evaluated / pruned
- Branching factor
- Pruning efficiency
- Cache hit rate

**Usage:**
```python
from scripts.performance_optimizer import SearchStatistics

stats = SearchStatistics()

# During search
stats.record_node()
stats.record_cutoff()
stats.record_cache_hit()

# Analysis
print(stats.summary())
print(f"Pruning efficiency: {stats.pruning_efficiency():.1f}%")
```

## Game Theory Applications

Full implementation in `scripts/game_theory_analyzer.py`.

### 1. Nash Equilibrium Calculation

Find optimal mixed strategy solutions for 2-player games.

**Pure Strategy Nash Equilibria:**
A cell is a Nash equilibrium if it's a best response for both players.

**Mixed Strategy Nash Equilibria:**
Players randomize over actions. For 2x2 games, use indifference conditions.

**Usage:**
```python
from scripts.game_theory_analyzer import GameTheoryAnalyzer, PayoffMatrix
import numpy as np

# Create payoff matrix
p1_payoffs = np.array([[3, 0], [5, 1]])
p2_payoffs = np.array([[3, 5], [0, 1]])

matrix = PayoffMatrix(
    player1_payoffs=p1_payoffs,
    player2_payoffs=p2_payoffs,
    row_labels=['Strategy A', 'Strategy B'],
    column_labels=['Strategy X', 'Strategy Y']
)

analyzer = GameTheoryAnalyzer()

# Find pure Nash equilibria
equilibria = analyzer.find_pure_strategy_nash_equilibria(matrix)

# Find mixed Nash equilibrium (2x2 only)
p1_mixed, p2_mixed = analyzer.calculate_mixed_strategy_2x2(matrix)

# Expected payoff
payoff = analyzer.calculate_expected_payoff(p1_mixed, p2_mixed, matrix, player=1)

# Zero-sum analysis
if matrix.is_zero_sum():
    minimax = analyzer.minimax_value(matrix)
    maximin = analyzer.maximin_value(matrix)
```

### 2. Cooperative Game Analysis

Analyze coalitional games where players can coordinate.

**Shapley Value:**
- Fair allocation of total payoff based on marginal contributions
- Each player receives expected marginal contribution across all coalition orderings

**Core:**
- Set of allocations where no coalition wants to deviate
- Stable outcomes that satisfy coalitional rationality

**Usage:**
```python
from scripts.game_theory_analyzer import CooperativeGameAnalyzer

coop = CooperativeGameAnalyzer()

# Define payoff function for coalitions
def payoff_func(coalition):
    # Return total value of coalition
    return sum(player_values[p] for p in coalition)

players = ['Alice', 'Bob', 'Charlie']

# Calculate Shapley values
shapley = coop.calculate_shapley_value(payoff_func, players)
print(f"Alice's fair share: {shapley['Alice']}")

# Find core allocation
core = coop.calculate_core(payoff_func, players)
is_stable = coop.is_core_allocation(core, payoff_func, players)
```

## Best Practices

### Agent Development
- ✓ Start with rule-based baseline
- ✓ Measure performance metrics consistently
- ✓ Test against multiple opponents
- ✓ Use version control for agent versions
- ✓ Document strategy changes

### Game Environment
- ✓ Validate game rules implementation
- ✓ Test edge cases
- ✓ Provide easy reset/replay
- ✓ Log game states for analysis
- ✓ Support deterministic seeds

### Optimization
- ✓ Profile before optimizing
- ✓ Use transposition tables
- ✓ Implement proper time management
- ✓ Monitor memory usage
- ✓ Benchmark against baselines

## Testing and Benchmarking

Complete benchmarking toolkit in `scripts/agent_benchmark.py`.

### Tournament Evaluation

Run round-robin or elimination tournaments between agents.

**Usage:**
```python
from scripts.agent_benchmark import GameAgentBenchmark

benchmark = GameAgentBenchmark()

# Run tournament
results = benchmark.run_tournament(agents, num_games=100)

# Compare two agents
comparison = benchmark.head_to_head_comparison(agent1, agent2, num_games=50)
print(f"Win rate: {comparison['agent1_win_rate']:.1%}")
```

### Rating Systems

Calculate agent strength using standard rating systems.

**Elo Rating:**
- Based on strength differential
- K-factor of 32 for normal games
- Used in chess and many games

**Glicko-2 Rating:**
- Accounts for rating uncertainty (deviation)
- Better for irregular play schedules

**Usage:**
```python
# Elo ratings
elo_ratings = benchmark.evaluate_elo_rating(agents, num_games=100)

# Glicko-2 ratings
glicko_ratings = benchmark.glicko2_rating(agents, num_games=100)

# Strength relative to baseline
strength = benchmark.rate_agent_strength(agent, baseline_agents, num_games=20)
```

### Performance Profiling

Evaluate agent quality on test positions.

**Usage:**
```python
# Get performance profile
profile = benchmark.performance_profile(agent, test_positions, time_limit=1.0)
print(f"Accuracy: {profile['accuracy']:.1%}")
print(f"Avg move quality: {profile['avg_move_quality']:.2f}")
```

## Implementation Checklist

- [ ] Choose game environment (Gym, Chess, Custom)
- [ ] Design agent architecture (Rule-based, Minimax, MCTS, RL)
- [ ] Implement game state representation
- [ ] Create evaluation function
- [ ] Implement agent decision-making
- [ ] Set up training/learning loop
- [ ] Create benchmarking system
- [ ] Test against multiple opponents
- [ ] Optimize performance (search depth, eval speed)
- [ ] Document strategy and results
- [ ] Deploy and monitor performance

## Resources

### Frameworks
- **OpenAI Gym**: https://gym.openai.com/
- **python-chess**: https://python-chess.readthedocs.io/
- **Pygame**: https://www.pygame.org/

### Research
- **AlphaGo papers**: https://deepmind.com/
- **Stockfish**: https://stockfishchess.org/
- **Game Theory**: Introduction to Game Theory (Osborne & Rubinstein)


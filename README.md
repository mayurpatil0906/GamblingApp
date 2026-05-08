# GamblingApp
# 🎲 Strategic Gambling Simulation Engine

> A modular, object-oriented Java application simulating a calculative gambler's strategy — with real-time stake management, dynamic betting strategies, session lifecycle control, and comprehensive win/loss analytics.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Module Breakdown](#module-breakdown)
  - [UC1 – Gambler Profile Management](#uc1--gambler-profile-management)
  - [UC2 – Stake Management Operations](#uc2--stake-management-operations)
  - [UC3 – Betting Mechanism](#uc3--betting-mechanism)
  - [UC4 – Game Session Management](#uc4--game-session-management)
  - [UC5 – Win/Loss Calculation](#uc5--winloss-calculation)
  - [UC6 – Input Validation & Error Handling](#uc6--input-validation--error-handling)
  - [UC7 – User Interaction](#uc7--user-interaction)
- [Core Java Concepts Used](#core-java-concepts-used)
- [Data Structures](#data-structures)
- [Betting Strategies](#betting-strategies)
- [Odds Systems](#odds-systems)
- [Exception Hierarchy](#exception-hierarchy)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Strategic Gambling Simulation Engine** models a disciplined, rules-based gambler who:

- Starts with a defined **initial stake**
- Bets according to a chosen **strategy**
- Exits when a **win threshold (upper limit)** or **loss threshold (lower limit)** is hit
- Tracks every decision, outcome, and stake movement with a **complete audit trail**

This project is built as a modular Java application following clean OOP principles, making each use case independently testable and extensible.

---

## Features

- ✅ **7 fully implemented use case modules**
- ✅ **6 betting strategies** (Fixed, Percentage, Martingale, Reverse Martingale, Fibonacci, D'Alembert)
- ✅ **4 odds systems** (Fixed, Probability-based, American, Decimal)
- ✅ **Real-time stake monitoring** with peak/low tracking and volatility calculation
- ✅ **Session lifecycle management** (start, pause, resume, auto-end on limits)
- ✅ **Comprehensive win/loss analytics** (streaks, ratios, profit factor, ROI)
- ✅ **Robust validation layer** with custom exception hierarchy
- ✅ **Interactive console UI** with menus and real-time status display
- ✅ **Complete transaction audit trail** for every stake change
- ✅ **Thread-safe design** ready for concurrent operations

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   Main Application                        │
│         (Menu System + Game Engine Orchestration)         │
└───────────────────────┬──────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│  UC1: Gambler│ │UC2: Stake   │ │UC3: Betting  │
│  Profile     │ │Management   │ │Mechanism     │
└──────────────┘ └─────────────┘ └──────────────┘
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│  UC4: Session│ │UC5: Win/Loss│ │UC6: Validation│
│  Management  │ │Calculation  │ │& Error Handle │
└──────────────┘ └─────────────┘ └──────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  UC7: User      │
               │  Interaction    │
               └─────────────────┘
```

---

## Module Breakdown

### UC1 – Gambler Profile Management

Manages the complete lifecycle of a gambler's profile.

| Component | Responsibility |
|---|---|
| `GamblerProfile` | Stores personal info, stake data, betting history |
| `BettingPreferences` | Manages bet limits, preferred strategy, auto-play settings |
| `GamblerStatistics` | DTO providing win rate, net P&L, average bet, threshold status |
| `GamblerProfileService` | Implements create, update, retrieve, validate, reset operations |

**Operations:**
- `create` — Validates minimum stake and threshold requirements
- `update` — Supports partial updates to preferences and thresholds
- `retrieve` — Returns full statistics and financial snapshot
- `validate` — Checks eligibility based on stake, thresholds, and account status
- `reset` — Resets for a new session with proportional threshold recalculation

---

### UC2 – Stake Management Operations

Full real-time stake lifecycle management with audit logging.

| Component | Responsibility |
|---|---|
| `StakeTransaction` | Immutable record of every stake change |
| `TransactionType` | Enum: `INITIAL_STAKE`, `BET_PLACED`, `BET_WIN`, `BET_LOSS`, `DEPOSIT`, `WITHDRAWAL`, `ADJUSTMENT`, `RESET` |
| `StakeBoundary` | Manages upper/lower limits with configurable warning thresholds |
| `StakeMonitor` | Real-time tracking of peak, low, and volatility |
| `StakeHistoryReport` | Aggregated report with per-transaction breakdown and net P&L |
| `StakeManagementService` | Orchestrates all six stake use cases |

**Warning thresholds:** 20% above minimum, 80% of maximum — configurable.

---

### UC3 – Betting Mechanism

Handles single and consecutive bet placement using pluggable strategy pattern.

| Component | Responsibility |
|---|---|
| `Bet` | Entity tracking bet ID, amount, odds, stake before/after, settlement |
| `BettingSession` | Session-level collection of bets with statistics and summaries |
| `BettingService` | `placeBet()`, `determineBetOutcome()`, `settleBet()`, `placeConsecutiveBets()` |

**Strategy implementations:** see [Betting Strategies](#betting-strategies).

---

### UC4 – Game Session Management

Full session lifecycle with automatic boundary detection.

| Component | Responsibility |
|---|---|
| `SessionStatus` | Enum: `INITIALIZED`, `ACTIVE`, `PAUSED`, `ENDED_WIN`, `ENDED_LOSS`, `TIMEOUT`, `MANUAL_END` |
| `SessionEndReason` | Tracks why a session ended |
| `GameRecord` | Per-game record with bet, outcome, stake delta, duration |
| `SessionParameters` | Configurable limits, bet range, max games, session timeout, win probability |
| `PauseRecord` | Tracks each pause cycle with duration and reason |
| `GamingSession` | Core session class: play, pause, resume, boundary monitor, auto-end |
| `GameSessionManager` | Multi-session management, prevents duplicate active sessions |

**Auto-end behavior:**
- Session ends immediately when stake ≥ upper limit → `ENDED_WIN`
- Session ends immediately when stake ≤ lower limit → `ENDED_LOSS`

---

### UC5 – Win/Loss Calculation

Probability-driven outcome engine with comprehensive statistical tracking.

| Component | Responsibility |
|---|---|
| `RandomOutcomeStrategy` | Pure probability-based outcomes |
| `WeightedProbabilityStrategy` | Includes configurable house edge |
| `OddsConfiguration` | Supports Fixed, Probability-based, American, Decimal odds |
| `GameResult` | Complete game record with winnings calculation |
| `WinLossStatistics` | 15+ metrics: win rate, profit factor, streaks, ROI, return-on-risk |
| `RunningTotals` | Real-time cumulative balance and P&L progression |
| `WinLossCalculator` | Orchestrates all 6 win/loss use cases |

---

### UC6 – Input Validation & Error Handling

Multi-layer validation with a custom exception hierarchy.

```
ValidationException (base)
├── StakeValidationException
├── BetValidationException
├── LimitValidationException
└── ProbabilityValidationException
```

| Component | Responsibility |
|---|---|
| `ValidationErrorType` | Enum: `STAKE_ERROR`, `BET_ERROR`, `LIMIT_ERROR`, `PROBABILITY_ERROR`, `NUMERIC_ERROR`, `RANGE_ERROR`, `NULL_ERROR` |
| `ValidationResult` | Collects errors and warnings, distinguishes critical from advisory |
| `ValidationConfig` | Centralized, configurable rules for all validation domains |
| `InputValidator` | Core validation methods for stake, bet, limits, numerics, probability |
| `SafeInputHandler` | Console input handler with retry loops and user-friendly feedback |

**Edge cases handled:** `NaN`, `Infinity`, null, empty strings, negative values, out-of-range doubles.

---

### UC7 – User Interaction

Rich console-based UI providing complete interactive experience.

| Component | Responsibility |
|---|---|
| `GameStatusDisplay` | Renders current stake, active session stats, boundary indicators |
| `InteractiveMenu` | Main menu system with all operations |
| `SessionSummary` | End-of-session report: duration, games, P&L, win rate, strategy used |
| `SimpleGameEngine` | Wires all use cases together for demo execution |

**Menu options:**
1. Start New Session
2. View Current Status
3. Place Bet (manual)
4. Auto-Play (automated consecutive bets)
5. Pause / Resume Session
6. End Session (with full summary)
7. Exit

---

## Core Java Concepts Used

| Concept | Application |
|---|---|
| **Encapsulation** | Private stake fields with controlled public accessors |
| **Inheritance** | Base `Strategy` class extended by all betting strategies |
| **Polymorphism** | Strategies implementing a common `BettingStrategy` interface |
| **Abstraction** | Abstract classes for generic gambling operations |
| **Exception Handling** | Custom hierarchy, try-catch-finally, resource cleanup |
| **Enums** | `TransactionType`, `SessionStatus`, `SessionEndReason`, `ValidationErrorType` |
| **Design Patterns** | Strategy (betting), DTO (statistics), Service Layer, Factory |

---

## Data Structures

| Structure | Used For |
|---|---|
| `ArrayList` | Dynamic collection of games played, transaction history |
| `HashMap` | Gambler ID → profile mapping; strategy name → implementation |
| `LinkedList` | Chronological bet sequence |
| `Stack` | Betting state tracking for undo operations |
| `Queue` | Processing pending bets in order |
| `Arrays` | Fixed-size bet history, session records |

---

## Betting Strategies

| Strategy | Logic |
|---|---|
| **Fixed Amount** | Constant bet regardless of outcome |
| **Percentage** | Bet a fixed % of current stake (e.g., 5%) |
| **Martingale** | Double after loss, reset to base after win |
| **Reverse Martingale** | Double after win, reset after loss |
| **Fibonacci** | Progress through Fibonacci sequence on losses |
| **D'Alembert** | Increase/decrease bet by fixed increment |

---

## Odds Systems

| Type | Description |
|---|---|
| **Fixed** | Simple multiplier (e.g., 2× your bet) |
| **Probability-based** | Higher payout for lower probability outcomes |
| **American** | Negative = favorite, positive = underdog (e.g., -150, +200) |
| **Decimal** | European format (e.g., 1.85, 3.40) |

---

## Exception Hierarchy

```java
ValidationException
 ├── StakeValidationException    // Stake range, negative, min/max violations
 ├── BetValidationException      // Bet > stake, min/max bet violations
 ├── LimitValidationException    // Upper ≤ lower, stake outside limits
 └── ProbabilityValidationException  // p < 0.0 or p > 1.0
```

All exceptions carry: error type enum, field name, attempted value, and a human-readable message.

---

## Getting Started

### Prerequisites

- Java 17+
- Maven or Gradle (optional)

### Clone & Run

```bash
git clone https://github.com/your-username/gambling-simulation-engine.git
cd gambling-simulation-engine
javac -d out src/**/*.java
java -cp out Main
```

### With Maven

```bash
mvn compile
mvn exec:java -Dexec.mainClass="Main"
```

---

## Project Structure

```
gambling-simulation-engine/
│
├── src/
│   ├── profile/
│   │   ├── GamblerProfile.java
│   │   ├── BettingPreferences.java
│   │   ├── GamblerStatistics.java
│   │   └── GamblerProfileService.java
│   │
│   ├── stake/
│   │   ├── StakeTransaction.java
│   │   ├── TransactionType.java
│   │   ├── StakeBoundary.java
│   │   ├── StakeMonitor.java
│   │   ├── StakeHistoryReport.java
│   │   └── StakeManagementService.java
│   │
│   ├── betting/
│   │   ├── Bet.java
│   │   ├── BettingSession.java
│   │   ├── BettingService.java
│   │   └── strategies/
│   │       ├── BettingStrategy.java
│   │       ├── FixedAmountStrategy.java
│   │       ├── PercentageStrategy.java
│   │       ├── MartingaleStrategy.java
│   │       ├── ReverseMartingaleStrategy.java
│   │       ├── FibonacciStrategy.java
│   │       └── DAlembert Strategy.java
│   │
│   ├── session/
│   │   ├── SessionStatus.java
│   │   ├── SessionEndReason.java
│   │   ├── GameRecord.java
│   │   ├── SessionParameters.java
│   │   ├── PauseRecord.java
│   │   ├── GamingSession.java
│   │   └── GameSessionManager.java
│   │
│   ├── calculation/
│   │   ├── RandomOutcomeStrategy.java
│   │   ├── WeightedProbabilityStrategy.java
│   │   ├── OddsConfiguration.java
│   │   ├── GameResult.java
│   │   ├── WinLossStatistics.java
│   │   ├── RunningTotals.java
│   │   └── WinLossCalculator.java
│   │
│   ├── validation/
│   │   ├── exceptions/
│   │   │   ├── ValidationException.java
│   │   │   ├── StakeValidationException.java
│   │   │   ├── BetValidationException.java
│   │   │   ├── LimitValidationException.java
│   │   │   └── ProbabilityValidationException.java
│   │   ├── ValidationErrorType.java
│   │   ├── ValidationResult.java
│   │   ├── ValidationConfig.java
│   │   ├── InputValidator.java
│   │   └── SafeInputHandler.java
│   │
│   ├── ui/
│   │   ├── GameStatusDisplay.java
│   │   ├── InteractiveMenu.java
│   │   ├── SessionSummary.java
│   │   └── SimpleGameEngine.java
│   │
│   └── Main.java
│
├── test/
│   └── (unit tests per module)
│
├── README.md
└── pom.xml
```

---

## Usage Examples

### Creating a Gambler and Starting a Session

```java
GamblerProfileService profileService = new GamblerProfileService();
GamblerProfile gambler = profileService.create("Alice", 1000.0, 1500.0, 500.0);
// Initial stake: 1000 | Win threshold: 1500 | Loss threshold: 500

SessionParameters params = new SessionParameters(1500.0, 500.0, 10.0, 100.0, 0.5);
GamingSession session = GameSessionManager.startNewSession(gambler.getId(), params);
```

### Placing a Bet with Martingale Strategy

```java
BettingService bettingService = new BettingService();
MartingaleStrategy strategy = new MartingaleStrategy(20.0);
Bet bet = bettingService.placeBetWithStrategy(session, strategy);
```

### Validating Inputs

```java
InputValidator validator = new InputValidator(new ValidationConfig());
ValidationResult result = validator.validateInitialStake(500.0);
if (!result.isValid()) {
    result.getErrors().forEach(System.out::println);
}
```

### Running Auto-Play Until a Limit is Hit

```java
session.continueSession(100); // Plays up to 100 games
// Session auto-ends if upper or lower limit is hit mid-play
System.out.println(session.getEndReason()); // e.g., UPPER_LIMIT_REACHED
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure your code follows the existing modular structure and includes appropriate validation and error handling.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

> **Disclaimer:** This is a simulation project for educational and software engineering purposes only. It does not facilitate real gambling.

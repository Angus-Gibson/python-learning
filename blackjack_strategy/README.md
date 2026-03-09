# Blackjack Strategy Flashcards

A simple yet elegant flashcard application for learning blackjack basic strategy using Python and Tkinter.

## Overview

This application helps players memorize blackjack basic strategy through interactive flashcards. Each card displays a player hand and challenges you to recall the optimal action before revealing the dealer's up cards and recommended plays.

The strategy implemented is **Basic Strategy for Double-Deck Games** where the dealer hits on soft 17.

## Features

- **Interactive Flashcards**: Flip cards to reveal the strategy table
- **Organized by Hand Type**: Flashcards are organized into three sections:
  - **Hard Totals**: Hands with no Ace or an Ace counted as 1
  - **Soft Totals**: Hands with an Ace counted as 11
  - **Pairs**: Pocket pairs of identical cards
- **Color-Coded Actions**: Each action is color-coded for quick visual recognition:
  - 🟨 **Hit** (Yellow)
  - 🟩 **Stand** (Green)
  - 🔴 **Double Down** (Red)
  - 🔵 **Split** (Blue)
- **Shuffle Functionality**: Randomly shuffle all cards and restart
- **Progress Tracking**: See your current card number and score

## Project Structure

```
blackjack_strategy/
├── main.py                    # Main entry point
├── strategy.py                # Strategy loader and card generation
├── strategy.yaml              # Blackjack strategy configuration (data)
├── gui.py                     # GUI application class
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### File Descriptions

#### `main.py`
The main entry point for the application. Imports the GUI class and launches the Tkinter main loop.

```bash
python main.py
```

#### `strategy.yaml`
The blackjack strategy configuration file. Defines all game rules organized by hand type:
- **Hard Totals**: Hands with no Ace or an Ace counted as 1
- **Soft Totals**: Hands with an Ace counted as 11
- **Pairs**: Pocket pair rules
- **UI Config**: Colors and abbreviations for actions

This file uses a declarative format that allows easy customization and support for different rule variants (single-deck, 6-deck, dealer stands on S17, etc.) without modifying Python code.

#### `strategy.py`
Loads the strategy configuration from `strategy.yaml` and:
- Parses the YAML rules into a lookup table
- Exports `DEALER_CARDS`, `ACTION_COLORS`, `ACTION_SHORT` constants
- Generates flashcard objects from the strategy table via `make_cards()`

#### `gui.py`
Contains the `BlackjackFlashcardApp` class that handles:
- UI construction with Tkinter widgets
- Card display and flipping logic
- Strategy table rendering on card back
- Button event handling (Flip, Next, Shuffle)
- Progress and score tracking
- Menu bar with Help dropdown (README viewer)

## Installation

1. Clone or download the repository
2. Navigate to the directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The blackjack strategy is defined in [strategy.yaml](strategy.yaml), which uses YAML format for easy customization:

### Customizing Strategy Rules

Edit [strategy.yaml](strategy.yaml) to change strategy rules. The file is organized by hand type:

**Example: Modifying a hard total rule**
```yaml
hard_totals:
  "16":
    stand_against: ['2', '3', '4', '5', '6']  # Stand against weak dealer cards
    default_action: Hit                         # Hit against strong dealer cards
```

**Example: Modifying a pair rule**
```yaml
pairs:
  "9,9":
    stand_against: ['7', '10', 'A']
    default_action: Split
```

### Supporting Different Game Variants

You can create variant YAML files for different blackjack rules:
- `strategy_single_deck.yaml` - Single-deck games
- `strategy_6deck_h17.yaml` - 6-deck where dealer hits on soft 17
- `strategy_6deck_s17.yaml` - 6-deck where dealer stands on soft 17

Then update [strategy.py](strategy.py) to load the desired variant.

Run the application with:
```bash
python blackjack_flashcards.py
```

### How to Use

1. **Flip**: Click the **FLIP** button to reveal the strategy table for the current hand
2. **Review**: Study the actions recommended for each dealer card
3. **Next**: Click **NEXT** to move to the next flashcard
4. **Shuffle**: Click **SHUFFLE** to randomize the deck and start over

The progress bar shows your current position (e.g., "Card 15 of 168"), and the score display shows how many cards you've reviewed.

## Strategy Rules

### Hard Totals
- **17+**: Always stand
- **16**: Stand against 2-6, hit otherwise
- **13-15**: Stand against 2-6, hit otherwise
- **12**: Stand against 4-6, hit otherwise
- **11**: Always double down
- **10**: Double down against 2-9, hit against 10 or Ace
- **9**: Double down against 3-6, hit otherwise
- **5-8**: Always hit

### Soft Totals
- **A,9 / A,10**: Always stand
- **A,8**: Double down against 6, stand otherwise
- **A,7**: Stand against 7-8, double down against 2-6, hit otherwise
- **A,6**: Double down against 3-6, hit otherwise
- **A,5 / A,4**: Double down against 4-6, hit otherwise
- **A,3 / A,2**: Double down against 4-6, hit otherwise

### Pairs
- **A,A / 8,8**: Always split
- **10,10**: Always stand
- **9,9**: Stand against 7, 10, A; split otherwise
- **7,7**: Split against 2-7, hit otherwise
- **6,6**: Split against 2-6, hit otherwise
- **5,5**: Double down against 2-9, hit otherwise
- **4,4**: Split against 5-6, hit otherwise
- **3,3 / 2,2**: Split against 2-7, hit otherwise

## Technical Details

- **Language**: Python 3
- **GUI Framework**: Tkinter (built-in with Python)
- **Design**: Object-oriented, separated concerns (strategy data vs. GUI)

## Disclaimer

Blackjack, like all gambling, is a game of chance. This strategy does not guarantee success and should be used responsibly. If you struggle with gambling addiction, please call 1-800-GAMBLER.

## Author

Developed by Taylor Gibson as practice for Python development with Claude.

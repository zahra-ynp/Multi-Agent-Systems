# Can Language Create Cooperation? | Multi-Agent Systems


This project uses **LLM-powered autonomous agents** (via [AutoGen](https://github.com/microsoft/autogen) and the **Gemini API**) to simulate classic game theory scenarios. Two agents play repeated games against each other, with and without the ability to communicate, to explore how communication affects coordination and equilibrium selection.

---

## Games Implemented

### 1. Stag Hunt (`stag_hunt_simulation.py`)

A classic social cooperation dilemma where agents must decide between hunting a **Stag** (requiring mutual cooperation) or a **Hare** (a safe, solo option).

| Agent A \ Agent B | Stag | Hare |
|:-----------------:|:----:|:----:|
| **Stag**          | 3, 3 | 0, 2 |
| **Hare**          | 2, 0 | 1, 1 |

- **Stag + Stag** → Both get **3 points** (optimal cooperative outcome)
- **Stag + Hare** → Stag-chooser gets **0**, Hare-chooser gets **2**
- **Hare + Hare** → Both get **1 point** (safe, risk-averse equilibrium)

### 2. Coordination Game / Battle of the Sexes (`agent-coordination-game.py`)

A coordination game with **conflicting preferences**. Both agents must choose the same activity to score, but each prefers a different one.

| Agent A \ Agent B | Football | Opera |
|:-----------------:|:--------:|:-----:|
| **Football**      | 3, 2     | 0, 0  |
| **Opera**         | 0, 0     | 2, 3  |

- Agent A prefers **Football** (gets 3 if both choose it)
- Agent B prefers **Opera** (gets 3 if both choose it)
- Miscoordination gives **both 0 points**

---

##  Project Structure

```
Multi-Agent-Systems/
├── codes/
│   ├── stag_hunt_simulation.py       # Game 1: Stag Hunt
│   └── agent-coordination-game.py   # Game 2: Coordination Game (Battle of the Sexes)
├── results/
│   ├── first_game_no_communication.json    # Stag Hunt — no communication run
│   ├── first_game_with_communication.json  # Stag Hunt — with communication run
│   ├── second_game_no_communication.json   # Coordination Game — no communication run
│   └── second_game_with_communication.json # Coordination Game — with communication run
└── README.md
```

---


##  Setup & Installation

### Prerequisites

- Python 3.9+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Install Dependencies

```bash
pip install pyautogen google-generativeai
```

### 2. Set Your Gemini API Key

The scripts read the API key from an **environment variable**. Set it before running:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Linux / macOS:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

---

## Running the Simulations

Navigate to the `codes/` folder first:

```bash
cd codes
```

### Run Stag Hunt

```bash
python stag_hunt_simulation.py
```

### Run Coordination Game

```bash
python agent-coordination-game.py
```
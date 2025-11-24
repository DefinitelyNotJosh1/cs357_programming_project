# A* Converter

## Project Description

This project is a **Final Project for Theory of Computation**. Its primary purpose is to demonstrate that **regular languages are closed under the Star operation** (Kleene Star). The program takes a Deterministic Finite Automaton (DFA) or Nondeterministic Finite Automaton (NFA) as input and converts it into an equivalent NFA that recognizes the Kleene star of the original language ($L^*$).

## How It Works

The converter performs the standard construction to prove closure under star:
1.  **New Start State:** A new start state is created that is also an accepting state (to accept the empty string $\epsilon$).
2.  **Epsilon Transitions:**
    *   An $\epsilon$-transition is added from the new start state to the original start state.
    *   $\epsilon$-transitions are added from all original accepting states back to the original start state allowing the machine to "loop back" and process multiple strings from the language.

## Prerequisites

*   Python 3.x

## Setup and Usage

1.  **Input:** Place your DFA/NFA JSON files in the `input/` directory.
    *   The file must be a valid JSON file representing the automaton.
    *   See the **Input Format** section below for details.

2.  **Run:** Execute the script from the root directory:
    ```bash
    python a_star_converter.py
    ```

3.  **Output:** The converted automata will be saved in the `output/` directory with `_output` appended to the filename (e.g., `testcase1_output.json`).

## Input Format

The input JSON files should have the following structure:

*   `states`: A list of state objects. Each object must have a `state` name and transition keys.
*   `initial`: The name of the initial state.
*   `accepting`: A list of accepting state names.

### Example JSON Input

```json
{
    "states": [
        {
            "state": "q0",
            "0": "q1",
            "1": "q0"
        },
        {
            "state": "q1",
            "0": "q2",
            "1": "q0"
        },
        {
            "state": "q2",
            "0": "q2",
            "1": "q2"
        }
    ],
    "initial": "q0",
    "accepting": ["q1"]
}
```

*   **Transitions:** Can be a single state string (for DFAs) or a list of strings (for NFAs). Use `"epsilon"` for epsilon transitions.

## Directory Structure

*   `a_star_converter.py`: The main Python script.
*   `input/`: Folder for input JSON files.
*   `output/`: Folder where processed JSON files are generated.


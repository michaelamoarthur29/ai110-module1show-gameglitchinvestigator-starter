# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**The game's purpose.** A number-guessing game. The app picks a secret number
inside a range set by the difficulty, and you have a limited number of attempts
to find it, with a higher/lower hint after each guess and a score that rewards
winning in fewer tries.

**Bugs found and fixed.** Six, none of which produced an error message: the
higher/lower hints were inverted; the secret was cast to a string on every even
attempt, which made the comparison alphabetical (`"9" > "100"`); New Game never
reset the game's status, so a finished game could not be restarted; the hint
disappeared whenever the "Show hint" checkbox was toggled; wrong guesses gained
points on even turns and lost them on odd; and the secret was printed onto the
page in a debug panel. Full write-up, with a reproduction log, in
[`reflection.md`](reflection.md).

**Fixes applied.** Game rules moved out of `app.py` into `logic_utils.py` so
they can be tested without a browser; `check_guess()` now returns a single
outcome string with hint text owned by `hint_message()`, so the outcome and the
advice cannot contradict each other; a single `reset_game()` is used by both
startup and New Game; the hint outcome is stored in session state and rendered
on every rerun; and debug output is gated behind `GLITCH_DEBUG=1`.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video: 

1. User starts a new game on Normal difficulty.
2. The game generates a secret number between 1 and 100.
3. User enters a guess of 40 and receives a "Too Low" hint.
4. User enters a guess of 70 and receives a "Too High" hint.
5. The score updates after each guess.
6. User enters the correct number.
7. The game displays a winning message and final score.
8. Clicking "New Game" generates a new secret number and resets the game state correctly.



## 🧪 Test Results

```
$ pytest tests/

rootdir: /Users/mikeyamo-arthur/Documents/ai110-module1show-gameglitchinvestigator-starter
collected 17 items

tests/test_game_logic.py .................                               [100%]

============================== 17 passed in 0.02s ==============================
```

17 tests: the 3 that shipped with the starter (unchanged) plus 14 added during
debugging. Each new test targets a specific bug from the reproduction log in
`reflection.md` and fails against the original code.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran it, the game *looked* finished — a clean sidebar with difficulty settings, a guess box, Submit and New Game buttons, and a score. Nothing crashed, which is what made it tricky: every bug here is silent. The app never throws an error or prints a traceback, it just quietly tells you the wrong thing. Playing it twice made the problems obvious, though. The hints pointed the wrong direction, my score moved in ways I couldn't predict, and after losing once I could not start another game no matter how many times I clicked New Game.

The four concrete bugs I found:

1. **The hints are backwards.** In `check_guess()`, the outcome `"Too High"` is paired with the message `"📈 Go HIGHER!"` ([app.py:37-40](app.py#L37-L40)). If my guess was above the secret I was told to go higher, which walks you away from the answer every time.

2. **The secret changes type on every other turn.** On even-numbered attempts `app.py` does `secret = str(st.session_state.secret)` ([app.py:158-161](app.py#L158-L161)). Comparing an `int` to a `str` raises `TypeError`, and `check_guess()` catches it and falls back to comparing the two values *as text* ([app.py:41-47](app.py#L41-L47)). Text comparison is alphabetical, so `"9" > "100"` is `True`. The hints were sensible on odd turns and nonsense on even ones.

3. **New Game doesn't actually restart.** The handler resets `attempts` and `secret` but never resets `status` ([app.py:134-138](app.py#L134-L138)). Since `status` is what gates the whole game with `st.stop()` ([app.py:140-145](app.py#L140-L145)), once it's `"won"` or `"lost"` it stays that way forever. Clicking New Game reruns the script, hits the guard, and stops the page. It also picks the new secret with a hardcoded `random.randint(1, 100)`, ignoring the difficulty range, so on Easy (1–20) it can choose a number you aren't allowed to guess.

4. **The secret is printed on the page.** The "Developer Debug Info" expander writes `st.session_state.secret` straight into the rendered output with no debug flag or guard of any kind ([app.py:114-119](app.py#L114-L119)). Collapsing it in an expander hides it visually but it's still sent to the browser, so the game is trivially cheatable.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret = 50, guess `60` on attempt 1 | Hint tells me to guess lower | Hint says "📈 Go HIGHER!" — points away from the answer | none — `check_guess(60, 50)` returns `('Too High', '📈 Go HIGHER!')` |
| Secret = 50, guess `40` on attempt 1 | Hint tells me to guess higher | Hint says "📉 Go LOWER!" | none — `check_guess(40, 50)` returns `('Too Low', '📉 Go LOWER!')` |
| Secret = 100, guess `9` on attempt 2 (an even turn) | "Too Low", since 9 is far below 100 | Reported as **"Too High"** — the secret was a string, so it compared `"9" > "100"` alphabetically | none — `check_guess(9, '100')` returns `('Too High', '📈 Go HIGHER!')`; the underlying `TypeError` is swallowed by `except` |
| Lose a round, then click **New Game 🔁** | A fresh round starts with a new secret and reset attempts | Page shows "Game over. Start a new game to try again." and stops. Locked out permanently; only a browser refresh clears it | none — `st.stop()` ends the run silently |
| Two wrong guesses, both "Too High" (attempts 2 and 3) | Both wrong guesses cost the same | Attempt 2 **gained** +5 points, attempt 3 **lost** −5 | none — `update_score(0,'Too High',2)` → `5`, `update_score(0,'Too High',3)` → `-5` |
| Difficulty = Easy (range 1–20), guess `999` | Rejected as outside the valid range | Accepted as a normal guess and scored | none — `parse_guess('999')` returns `(True, 999, None)` |

The "Console Output / Error" column is mostly "none" on purpose — that was the most useful thing I learned here. Not one of these bugs announces itself. I verified each row by importing the functions from `app.py` directly and calling them with fixed values, so I could see the return values instead of guessing from what the UI rendered.

---

## 2. How did you use AI as a teammate?

I used Claude Code inside VS Code, which could read the whole project rather than just a pasted snippet. That mattered more than I expected: the worst bug in this codebase only makes sense when you look at `app.py` and `logic_utils.py` and `tests/test_game_logic.py` together.

**A suggestion that was correct.** The lab suggests the prompt *"Move the `check_guess` function to `logic_utils.py`, update the logic to fix the high/low bug, and update the import in `app.py`."* When I asked for that, the AI flagged a problem with the instruction before doing it: the starter's `check_guess` returns a **tuple**, `("Win", "🎉 Correct!")`, but the three starter tests assert against a **plain string**, `assert result == "Win"`. Moving the function as written would have passed the refactor step and failed all three tests, and I would have assumed I'd broken something myself. It suggested splitting the job — `check_guess()` returns only the outcome, and a new `hint_message()` owns the player-facing text — which also means the outcome and the advice can't contradict each other again, since that contradiction *was* the original bug. I verified it by running `pytest`: 17 passed, including the three untouched starter tests.

**A suggestion I did not accept as written.** Very early on, before I'd looked at anything, the AI started rewriting `logic_utils.py` with all four functions already fixed. It wasn't wrong code — it's close to what I ended up with — but I rejected it and told it to just get the app running instead. Two reasons. First, it was out of scope: Phase 1 is about *finding* bugs, and if I'd accepted that edit I'd have had working code and no idea what had been broken or why. Second, I couldn't have written the reproduction log, because I'd never have seen the bugs happen. I did the diagnosis myself, and only brought the AI back in for the refactor once I could describe each bug precisely. The verification is the log in section 1 — every row is a bug I found by playing and then confirmed by calling the function directly.

**One thing worth flagging.** The starter code is itself AI-generated, and its most damaging line is the one that looks the most responsible: a `try/except TypeError` around the comparison in `check_guess`. It reads like careful defensive programming. What it actually does is catch a real type error and silently fall back to comparing numbers as text, so the game gives confidently wrong answers instead of crashing. A crash would have been better — I'd have found it in thirty seconds.

---

## 3. Debugging and testing your fixes

My rule was that a bug wasn't fixed until I had a test that **failed against the old code and passed against the new code**. Writing a test that passes after the fix is easy and proves almost nothing — it might have passed before too. So for each bug I first called the original function directly with fixed inputs and recorded what it actually returned (those values are the last column of the log in section 1), then wrote the test to assert the opposite.

**The specific test.** The one I care about most is `test_string_secret_is_not_compared_as_text`, which asserts `check_guess(9, "100") == "Too Low"`. Against the starter code that returns `"Too High"`, because comparing `9` to `"100"` raises `TypeError`, the bare `except` catches it, and the fallback compares the values alphabetically — where `"9" > "100"` is `True`. This test taught me something the UI never could: the bug wasn't in the guessing logic at all, it was a **type** bug leaking into a comparison. Playing the game, it just looked like the hints were randomly unreliable. Only on even-numbered turns, which is why it took two playthroughs to notice a pattern.

**What the test suite covers now.** 17 tests, the 3 starter ones plus 14 I added — hint direction matching the outcome, the string-secret comparison, score changing identically on odd and even turns, out-of-range and decimal guesses being rejected, and "Hard" actually having a wider range than "Normal". All 17 pass with `.venv/bin/python -m pytest`.

**Did AI help with the tests?** Yes, and this was the most useful part. I could describe a bug in plain English and get back a test that pinned it down, which is much faster than writing assertions by hand. But I had to supply the failing inputs — the AI didn't know the secret got stringified on even turns until I told it, because that fact lives in `app.py` and the bug shows up in `logic_utils.py`. It was good at turning a diagnosis into a test, and useless at producing the diagnosis.

**Live verification.** Tests aren't enough for the state bugs, since none of those live in pure functions. I re-ran the app and manually confirmed: losing a round and clicking New Game now actually starts a new round (it used to lock the page permanently), toggling "Show hint" after submitting now shows the hint instead of doing nothing, and switching difficulty picks a fresh secret inside the new range.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

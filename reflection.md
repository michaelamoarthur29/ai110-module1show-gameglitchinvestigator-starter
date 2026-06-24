# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards"). 

  - The hints were indeed backwards, like it should tell you to go lower when higher than the secret number and vice cersa 
  - You can access the secret scroe before the game even starts 
  - The game doesn't reset when it's time to play a new game 
**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input          | Expected Behavior                      | Actual Behavior                     | Console Output / Error |
|-------|----------------------------------------------- -|-------------------------------------|--------------------------|
|Restart         | The game to restart                      No indicator of it restarting
|Hint button       Provide hints to aid in guessing         No hints given 
|Incorrect feedback feedback on if num is too high or low   Feedback is backwards 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result). 

I used ChatGPT as my AI assistant throughout the project. I used it to analyze the code, identify bugs, explain confusing logic, and help generate test cases.
One AI suggestion that was correct was identifying that the high and low hints were reversed inside the check_guess() function. The AI suggested updating the messages so that guesses above the secret number return a "Go LOWER" hint and guesses below the secret return a "Go HIGHER" hint. I verified this by running the game and confirming the hints matched the guesses.
One AI suggestion that was misleading was assuming the issue was entirely inside the hint logic. After reviewing the code more carefully, I discovered that game state and session state behavior were also contributing to bugs. I verified this by testing multiple games and observing how the secret number and game status behaved after restarting.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

I used ChatGPT as my AI assistant throughout the project. I used it to analyze the code, identify bugs, explain confusing logic, and help generate test cases.
One AI suggestion that was correct was identifying that the high and low hints were reversed inside the check_guess() function. The AI suggested updating the messages so that guesses above the secret number return a "Go LOWER" hint and guesses below the secret return a "Go HIGHER" hint. I verified this by running the game and confirming the hints matched the guesses.
One AI suggestion that was misleading was assuming the issue was entirely inside the hint logic. After reviewing the code more carefully, I discovered that game state and session state behavior were also contributing to bugs. I verified this by testing multiple games and observing how the secret number and game status behaved after restarting.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I determined a bug was fixed by testing both the application and the automated test cases. After making a change, I ran the Streamlit application and attempted several guesses to verify the expected behavior occurred. I also ran pytest to ensure the logic functions returned the correct outcomes.
One test I ran checked whether a guess of 60 against a secret number of 50 returned "Too High." Another test verified that the hint instructed the player to go lower. These tests confirmed that the bug in the hint system had been fixed.
AI helped me understand how to write focused tests for specific pieces of logic rather than testing the entire application at once. This made it easier to verify individual fixes.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I learned that Streamlit reruns the entire script every time a user interacts with the page. Because of this behavior, variables can reset unless they are stored in st.session_state. Session state allows information such as scores, attempts, and secret numbers to persist between reruns. Without it, the game would continuously restart and lose important data.
# Instructions to run in terminal:

1. Download project files.
2. Create and activate virtual environment in the project directory.

- For macOS:
  - first create the venv: `python3.10 -m venv venv`
  - then activate: `source venv/bin/activate`
- For Windows:
  - first create the venv `python -m venv venv`
  - then activate:
    - (command prompt) `venv\Scripts\activate`
    - (powershell) `.\venv\Scripts\Activate.ps1`

3. Download the requirements:
   `pip install -r requirements.txt`
4. Download the SpaCy models:
   `python -m spacy download en_core_web_lg`
5. Run recipe asistant:
   `python terminal_recipe_assistant.py`

# To use the Slack interface:

Since we host the app locally (since we don't want to pay to host it somewhere), the app is not always up and running. We tried some options like Heroku and Render, but their free tier limits don't suffice due to how large the spacy model is, or they require payment method.

To test in Slack, message cheryl@u.northwestern.edu to set up a time. We'll invite you to our workspace where the Slack app lives and run the app locally so that it can be interacted with.

Slack functionality is the same as the functionality in the terminal assistant, and is also displayed in the video.

# Extra Features:

1. Conversational interface through Slack
2. Ingredient Descriptor (e.g. fresh, extra-virgin)
3. Ingredient Preparation (e.g. finely chopped)
4. Other cooking methods used (e.g. chop, grate, stir, shake, mince, crush, squeeze, etc.)

# Question answering goal examples:

1. Recipe retrieval and display

- "list all ingredients for this recipe"
- "list all tools needed for this recipe"
- "list all recipe steps"
- "go over recipe steps" (to start from the first step)

2. Navigation utterances

- "repeat step"
- "next step"
- "previous step"
- "go to step 1" or "go to step 14"

3. Asking about the parameters of the current step

- "How long do I..."
- "When is it done?"
- "How much <ingredient (as described in the step)> do I need?"
- "What temperature should I...?"
- "What can I use instead of <ingredient or tool>?"

4. Simple "what is" questions

- "What is..."

5. Specific "how to" questions

- "How to..."
- "How do I..."

6. Vague "how to" questions

- "How do I do that?"
- "How do you do that?"

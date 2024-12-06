# Github link: [https://github.com/pranavxiyer/CS337-proj3](https://github.com/pranavxiyer/CS337-proj3)

# Demo video: demo.mp4 (in submitted zip only)

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
   `python terminal_recipe_transformer.py`

When prompted, enter the AllRecipes URL. Then, select the transformation by entering the number corresponding to the transformation. The terminal will show the names of the .txt files that are exported, and they will appear in the root directory.

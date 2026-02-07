import os
from pathlib import Path
import logging


#logging string
#logging string
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = 'Outreach_Multi_Agent-'

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config.py",
    f"src/{project_name}/agents/chat_agent.py.py",
    f"src/{project_name}/agents/comment_agent.py",
    f"src/{project_name}/agents/posting_agent.py",
    f"src/{project_name}/agents/reporting_agent.py",
    f"src/{project_name}/agents/system_agent.py",
    f"src/{project_name}/shared/intent.py",
    f"src/{project_name}/shared/state.py",
    f"src/{project_name}/shared/teams.py",
    f"src/{project_name}/utils.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "post_config.yaml",
    ".env",
    "requirements.txt",
    "setup.py",
    "main.py",
    "README.md",
    "research/chat_project.ipynb",
    

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")
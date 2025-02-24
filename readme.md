
Clone: When someone clones the repository, they should:

Create Virtual Environment: Create a virtual environment:
Bash
```
python3 -m venv .venv  # Or use virtualenv, or poetry, etc.
```

Activate: Activate the virtual environment:
Bash
```
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

Install Dependencies: Install the dependencies from requirements.txt (or using poetry):
Bash
```
pip install -r requirements.txt  # Or poetry install
```
Now, they have a working environment with all the necessary packages.
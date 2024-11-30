# bgdata-backend

Backend of the Linked Papers project for BDA2024 @NJUSE, running the server on port `8000` of `localhost`, powered by FastAPI.

## Setup

Assure your Python is 3.12 or above, then install the dependencies by running:

```bash
pip install -r requirements.txt
```

To plug in MySQL, you may configurate it in `app/config/config.yaml`.

To get all data ready, you may need to:
1. prepare your data under `data/` directory,
2. run `find_similar.py`, `predict_category.py` under `scripts/` directory,
3. run `load_data.py` under `scripts/` directory, and
4. run `generate_embedding.py` under `scripts/` directory.

Executing some of them may take a while.

## Run

Say you're in the root directory of the backend project, you can start the server by running:
```bash
fastapi dev app/main.py
```

Or test by running: (*Unimplemented*)
```bash
pytest
```

Or debug by directly running `main.py` in debugging mode with your IDE.

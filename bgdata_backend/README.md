# bgdata-backend

Backend of the Linked Papers project for BDA2024 @NJUSE, running the server on port `8000` of `localhost`, powered by FastAPI.

## Setup

Assure your Python is 3.12 or above, then install the dependencies by running:

```bash
pip install -r requirements.txt
```

To plug in MySQL, you may configurate it in `app/config/config.yaml`.

Prepare your data under `../data/` directory, then run the scripts in `scripts/` to import the data into MySQL automatically. Note that you are supposed to run `load_data.py` after the other ones.

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

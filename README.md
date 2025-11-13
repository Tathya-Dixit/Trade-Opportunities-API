# Project Setup

1. Clone the repo:
```sh
git clone https://github.com/Tathya-Dixit/Trade-Opportunities-API.git
cd Trade-Opportunities-API
```

2. Create & activate venv and install dependencies:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Add a `.env` file (example):
```
SECRET_KEY=your_secret
GEMINI_API_KEY=your_gemini_key
```

4. Run the app:
```sh
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Access the APIs at: http://127.0.0.1:8000 (docs at http://127.0.0.1:8000/docs)

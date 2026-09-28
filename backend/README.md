# LYRA Backend - Phase 1

## Windows par setup karne ke steps

### 1. Python venv banayein (isolated environment, dependencies confuse nahi hongi)
```
cd backend
python -m venv venv
venv\Scripts\activate
```
Terminal mein `(venv)` dikhna chahiye prompt se pehle - iska matlab venv active hai.

### 2. Dependencies install karein
```
pip install -r requirements.txt
```

### 3. API key setup karein
- `.env.example` file ko copy karein aur naam `.env` rakhein
- `.env` file kholein aur apni Anthropic API key daalein:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```
- Key nahi hai? console.anthropic.com par jaake bana sakte hain (free credits milte hain naye account par)

### 4. Server chalayein
```
uvicorn main:app --reload
```
`--reload` ka matlab: jab bhi aap code change karenge, server khud restart ho jayega (development ke liye useful).

### 5. Test karein
Browser mein kholein: `http://localhost:8000`
Aapko yeh dikhna chahiye: `{"status": "LYRA backend is running"}`

Interactive API docs (FastAPI khud generate karta hai): `http://localhost:8000/docs`
Yahan se aap `/chat` endpoint ko browser se hi test kar sakte hain, bina kisi extra tool ke.

## Expected result
`/docs` page par "Try it out" click karein, `/chat` endpoint kholein,
message likhein: `{"message": "Hello, kaise ho?"}`, Execute press karein.
Response mein Claude ka reply aana chahiye.

## Troubleshooting
- **"ANTHROPIC_API_KEY nahi mili" error** → `.env` file `backend/` folder mein honi chahiye, `.env.example` nahi.
- **ModuleNotFoundError** → venv activate kiya? `pip install -r requirements.txt` dobara chalayein.
- **401 error from Claude** → API key galat hai ya expire ho gayi, console.anthropic.com check karein.

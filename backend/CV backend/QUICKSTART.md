# ⚡ QUICKSTART - Get Running in 5 Minutes

## Step 1: Install Python Packages (1 minute)

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi uvicorn pandas numpy faiss-cpu sentence-transformers ...
```

---

## Step 2: Set Up Environment (1 minute)

### On Windows:
```bash
# Copy template
copy .env.example .env

# Edit .env in your text editor
# Find: OPENAI_API_KEY=your_openai_api_key_here
# Replace with your actual key from https://platform.openai.com/account/api-keys
```

### On Mac/Linux:
```bash
cp .env.example .env
nano .env  # or vim .env
# Add your OPENAI_API_KEY
```

**Your .env should look like:**
```
OPENAI_API_KEY=sk-proj-abc123xyz...
LLM_MODEL=gpt-3.5-turbo
MAX_TOKENS=600
API_HOST=0.0.0.0
API_PORT=8000
DATA_DIR=./
```

⚠️ **Don't have an API key?** Get one free at https://platform.openai.com/account/api-keys

---

## Step 3: Initialize FAISS Index (1-2 minutes)

This builds the AI search engine from your CSV data.

```bash
python init.py
```

**Expected output:**
```
✓ All CSV files loaded successfully
✓ Index built with 1234 vectors
✓ Index saved to ./faiss_index
✓ RAG system ready
✓ LLM service connected
```

---

## Step 4: Start the Backend Server (30 seconds)

```bash
python main.py
```

**Expected output:**
```
🚀 Initializing Cover Letter Generator Backend...

📚 Loading data from CSV files...
✓ All CSV files loaded successfully

🔍 Initializing RAG system...
📦 Loading existing FAISS index...
✓ FAISS index loaded successfully

🤖 Initializing LLM service...
✓ LLM service ready

✅ Backend initialized successfully!

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## Step 5: Test the API (1 minute)

### Option A: Using Python Client (Easy)

Open a **new terminal** and run:

```bash
python client_example.py
```

**What you'll see:**
- ✅ Health check passes
- ✅ Available roles listed
- 📝 Sample cover letter generated
- 📊 Word count: ~350 words
- 💾 Ready to download

### Option B: Using Web Browser (Easy)

Open this URL in your browser:

```
http://localhost:8000/docs
```

You'll see **Swagger UI** - an interactive API explorer:
1. Click `/generate-cover-letter`
2. Click "Try it out"
3. Paste sample resume and JD
4. Click "Execute"
5. See generated cover letter in response

### Option C: Using curl (Advanced)

```bash
curl -X POST "http://localhost:8000/generate-cover-letter" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_content": "John Doe, Senior Software Engineer, 5+ years Python/AWS",
    "job_description": "Senior Backend Engineer, Python, AWS, microservices",
    "company_name": "Amazon",
    "job_role": "Senior Backend Engineer",
    "top_k": 5
  }'
```

---

## ✅ Verification Checklist

After Step 5, verify:

- [ ] Server running on `http://localhost:8000`
- [ ] Swagger UI accessible at `/docs`
- [ ] Health check returns `"status": "healthy"`
- [ ] Can generate cover letter without errors
- [ ] Output is plain text (no markdown)
- [ ] Word count is 250-450 words
- [ ] No OPENAI_API_KEY errors (if it says no key, see Step 2)

---

## 🔗 Next: Frontend Integration

Your React frontend should call:

```javascript
const response = await fetch('http://localhost:8000/generate-cover-letter', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    resume_content: userResume,
    job_description: jobDesc,
    company_name: 'Amazon',
    job_role: 'SDE',
    top_k: 5
  })
});

const data = await response.json();
console.log(data.cover_letter);  // Generated cover letter!
```

See **FRONTEND_INTEGRATION.md** for full React component code.

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Solution: Install requirements again
pip install -r requirements.txt
```

### "OPENAI_API_KEY not set"
```bash
# Solution: Check your .env file
cat .env  # Mac/Linux
type .env  # Windows

# Make sure OPENAI_API_KEY=sk-... is there (not the template text)
```

### "FAISS index not found"
```bash
# Solution: Build it
python init.py
# Wait 30-60 seconds
```

### "Address already in use" (port 8000)
```bash
# Option 1: Use different port
# Edit config.py: API_PORT = 8001
python main.py

# Option 2: Kill process on port 8000
netstat -ano | findstr :8000  # Windows
kill <PID>  # or use Task Manager
```

### "Cannot connect to API"
```bash
# Check if server is running in terminal
# Should see: "Uvicorn running on http://0.0.0.0:8000"

# Try health check
curl http://localhost:8000/health

# If fails, backend isn't running
python main.py  # Start it
```

### Slow generation (>15 seconds)
```python
# Edit config.py:
TOP_K_CHUNKS = 3  # Was 5 - faster retrieval
MAX_TOKENS = 400  # Was 600 - faster generation
LLM_MODEL = "gpt-3.5-turbo"  # Fast & cheap
```

---

## 📊 What's Happening Behind the Scenes

```
User Input (Resume + JD)
    ↓
    Backend receives request
    ↓
    1. SEARCH: Embed query → Find 5 similar chunks in FAISS (~100ms)
    ↓
    2. GENERATE: Feed chunks to GPT → Create cover letter (~5-10sec)
    ↓
    3. CLEAN: Remove markdown, emojis → ATS-friendly text (~50ms)
    ↓
    Response sent to frontend
    ↓
    Display & Download
```

**RAG = Retrieval Augmented Generation**
- Retrieval: Find relevant context from your data
- Augmented: Feed context to LLM
- Generation: LLM generates cover letter using context (no hallucination!)

---

## 💰 Cost Check

**Per cover letter:**
- **gpt-3.5-turbo**: ~$0.01 (cheap & fast ⚡)
- **gpt-4**: ~$0.10 (premium quality 👑)

**For 1000 generations:**
- gpt-3.5: ~$10 💵
- gpt-4: ~$100 💰

See API usage at: https://platform.openai.com/account/usage/overview

---

## 🎯 Common Next Steps

### 1. Connect Frontend
See `FRONTEND_INTEGRATION.md` for React component

### 2. Deploy to Production
```bash
# Option A: Docker
docker build -t api . && docker run -p 8000:8000 api

# Option B: Gunicorn
gunicorn -w 4 main:app

# Option C: Cloud (Heroku, AWS, etc.)
git push heroku main
```

### 3. Customize Prompts
Edit `llm_service.py` → `_get_system_prompt()`

### 4. Add More Data
Add CSV rows or rebuild FAISS index:
```bash
python init.py  # Rebuilds from updated CSVs
```

---

## 📚 Documentation

| Document | Read If... |
|----------|-----------|
| **SYSTEM_OVERVIEW.md** | You want to understand the full architecture |
| **README.md** | You need detailed API reference & configuration |
| **FRONTEND_INTEGRATION.md** | You're building the React frontend |
| **This file** | You want to get started quickly |

---

## ✨ You're All Set!

Your RAG-powered AI backend is now running! 🎉

**The pipeline:**
- ✅ AI search (FAISS) - finds relevant resume/JD parts
- ✅ AI generation (GPT) - creates personalized cover letter
- ✅ AI cleaning (regex) - removes artifacts, ensures ATS compliance

**Time to generate per request:**
- Embedding: ~50ms
- Retrieval: ~50ms
- Generation: ~5-10s
- **Total: ~6-12s** ⚡

Next: Connect your frontend and start generating cover letters! 🚀

---

## 🆘 Still Stuck?

Check these files in order:
1. **Error message matches troubleshooting above?** → Try solution
2. **Can't find API key?** → https://platform.openai.com/account/api-keys
3. **Server won't start?** → Check `.env` file, Python version (3.8+)
4. **Low quality covers?** → Use GPT-4 in config, increase `top_k`

**Still blocked?** Review:
- `SYSTEM_OVERVIEW.md` - Full architecture explanation
- `README.md` - Detailed configuration options
- `main.py` - API endpoints and error handling

**Good luck! 🎯**

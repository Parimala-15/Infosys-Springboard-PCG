# 🚀 Cover Letter Generator - RAG Backend

Professional AI-powered cover letter generation using **Retrieval Augmented Generation (RAG)** with embeddings, FAISS indexing, and OpenAI LLM.

## 📋 Architecture Overview

```
Frontend (React)
       ↓
   FastAPI Backend
       ↓
┌─────────────────────────────┐
│  1. RAG Retrieval Stage     │
│  - Embed user query         │
│  - Search FAISS index       │
│  - Retrieve top-k context   │
└─────────────────────────────┘
       ↓
┌─────────────────────────────┐
│  2. LLM Generation Stage    │
│  - System prompt            │
│  - Context injection        │
│  - Cover letter generation  │
└─────────────────────────────┘
       ↓
┌─────────────────────────────┐
│  3. Post-Processing         │
│  - Remove markdown          │
│  - ATS compliance check     │
│  - Format validation        │
└─────────────────────────────┘
       ↓
   JSON Response
```

## 📁 Project Structure

```
CV backend/
├── main.py                    # FastAPI app + endpoints
├── data_loader.py             # CSV file loading
├── rag_system.py              # FAISS indexing & retrieval
├── llm_service.py             # OpenAI LLM integration
├── config.py                  # Configuration management
├── utils.py                   # Helper functions
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
├── faiss_index                # FAISS index (generated)
├── metadata.pkl               # Index metadata (generated)
└── *.csv                      # Data files
    ├── resumes_validated.csv
    ├── jd_validated.csv
    ├── skill_role_master.csv
    └── covers_validated.csv
```

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-key-here
```

Get your key from: https://platform.openai.com/account/api-keys

### 3. Run the Backend

```bash
python main.py
```

The API will start at `http://0.0.0.0:8000`

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔌 API Endpoints

### 1. Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "index_loaded": true,
  "timestamp": "2024-01-11T10:30:00"
}
```

### 2. Get Available Roles
```bash
GET /roles
```

Response:
```json
{
  "roles": ["software_engineer", "ml_engineer", ...],
  "count": 15
}
```

### 3. Generate Cover Letter (Main Endpoint)
```bash
POST /generate-cover-letter
```

**Request:**
```json
{
  "resume_content": "Your full resume text...",
  "job_description": "Full job description...",
  "company_name": "Amazon",
  "job_role": "Senior Software Engineer",
  "experience_type": "experienced",
  "top_k": 5
}
```

**Response:**
```json
{
  "success": true,
  "cover_letter": "Dear Hiring Manager,\n\nI am excited to apply...",
  "word_count": 350,
  "retrieved_context_count": 5,
  "generation_timestamp": "2024-01-11T10:30:00"
}
```

### 4. Generate with Context Details (Debug)
```bash
POST /generate-cover-letter-with-context
```

Same request format, but response includes retrieved context chunks for transparency.

### 5. Get Context by Role
```bash
GET /context-by-role/{role}?experience_type=experienced&limit=5
```

Response includes relevant context chunks for a specific role.

## 📊 Data Flow

### Step 1: Data Loading & Indexing
```python
# Happens on startup
data_loader = DataLoader(data_dir="./")
data_loader.load_all_data()

# Create chunks from resumes, JDs, skills
chunks = data_loader.create_chunks()

# Build FAISS index
rag_system = RAGSystem()
rag_system.build_index(chunks)
rag_system.save_index("./faiss_index")
```

### Step 2: Query Processing
```python
# User submits:
# - Resume
# - Job Description
# - Company name
# - Job role

# Backend:
query = "senior_software_engineer amazon"
retrieved = rag_system.retrieve_context(query, k=5)
# Returns: [
#   {
#     'text': '...',
#     'metadata': {'source': 'jd', 'role': 'software_engineer'},
#     'similarity_score': 0.92
#   },
#   ...
# ]
```

### Step 3: LLM Generation
```python
cover_letter = llm_service.generate_cover_letter(
    resume_content=resume,
    job_description=jd,
    company_name="Amazon",
    job_role="Senior Software Engineer",
    retrieved_context=retrieved
)
# Returns: Plain text cover letter (400 words, ATS-friendly)
```

## 🔒 System Prompt

The LLM is instructed with a carefully designed system prompt:

```
You are an AI Cover Letter Generator integrated into a Resume Builder system.

Rules:
- Do NOT hallucinate skills or experience
- Use only resume and retrieved documents
- Keep length within 300–400 words
- Match job role and company tone
- Maintain formal, confident, human-like language
- Avoid generic phrases like "I am writing to apply"

Structure:
1. Strong personalized opening
2. Skills aligned with JD
3. Relevant projects/internships
4. Cultural & company alignment
5. Professional closing
```

## 🛠 Configuration Options

Edit `config.py` or `.env` to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Your OpenAI API key (required) |
| `LLM_MODEL` | `gpt-3.5-turbo` | Model to use |
| `MAX_TOKENS` | `600` | Max response length |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `TOP_K_CHUNKS` | `5` | Context chunks to retrieve |
| `API_HOST` | `0.0.0.0` | API host |
| `API_PORT` | `8000` | API port |

## 📦 RAG System Details

### FAISS Index
- **Type:** IndexFlatL2 (exact search)
- **Dimension:** 384 (from MiniLM embeddings)
- **Size:** Depends on CSV data

### Embeddings
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension:** 384
- **Updates:** Index is built once on startup and saved

### Retrieval Strategy
1. Embed user query
2. Search FAISS for top-k similar chunks
3. Return chunks with metadata & similarity scores
4. Optionally filter by role

## 🎯 Best Practices

### For Frontend Integration

1. **Call the main endpoint:**
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
   ```

2. **Error Handling:**
   ```javascript
   if (!response.success) {
     console.error('Generation failed:', response.error);
   }
   ```

3. **Display & Download:**
   ```javascript
   // Display in textarea
   textarea.value = response.cover_letter;
   
   // Download as .txt
   const blob = new Blob([response.cover_letter], { type: 'text/plain' });
   const url = URL.createObjectURL(blob);
   ```

### For Backend Optimization

1. **Increase TOP_K_CHUNKS** if results are irrelevant
2. **Decrease MAX_TOKENS** for shorter cover letters
3. **Use GPT-4** for higher quality (costs more)
4. **Cache FAISS index** - built once, reused per request

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `OPENAI_API_KEY not set` | Add key to `.env` file |
| `FAISS index not found` | First run will build automatically |
| `Slow responses` | Reduce `TOP_K_CHUNKS` or use smaller embeddings |
| `Low quality cover letters` | Increase `top_k`, use GPT-4, improve system prompt |
| `Index out of memory` | Use GPU FAISS index (faiss-gpu) |

## 📈 Performance Metrics

- **Index building:** ~30 seconds (first run only)
- **Retrieval:** ~100-200ms (top-5 chunks)
- **LLM generation:** ~5-10 seconds
- **Total latency:** ~6-12 seconds per request

## 🔄 Workflow Summary

```
User Input (Frontend)
    ↓
    POST /generate-cover-letter
    ↓
    [RAG] Embed query + retrieve context
    ↓
    [LLM] Generate cover letter
    ↓
    [PostProcess] Clean & validate
    ↓
    JSON Response
    ↓
Display in Frontend + Download Option
```

## 📝 CSV File Format

### resumes_validated.csv
```
role,experience_type,text
hr,experienced,"SR. HR CONSULTANT Executive Profile..."
```

### jd_validated.csv
```
job title,role,job description,skills,experience_type,text
,software_engineer,"Design, develop, test...",python;java,...,fresher,...
```

### skill_role_master.csv
```
role,skills,education,experience_type
software_engineer,"java,python,aws,...",B.Tech,experienced
```

### covers_validated.csv
```
job title,hiring company,skillsets,cover letter,role,experience_type,...
,Amazon,"java,aws,...","Dear Hiring Manager,...",software_engineer,fresher,...
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production (Gunicorn + Nginx)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV OPENAI_API_KEY=your_key
CMD ["python", "main.py"]
```

## 📞 Support

For issues or feature requests, check:
1. System prompt in `llm_service.py`
2. Configuration in `config.py`
3. Data loading in `data_loader.py`
4. RAG logic in `rag_system.py`

---

**Built with ❤️ using FastAPI, FAISS, and LangChain**

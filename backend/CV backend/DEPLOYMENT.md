# 🌐 Deployment & Production Guide

Complete guide for deploying your RAG-based Cover Letter Generator to production.

---

## 📊 Project Structure (Final)

```
CV backend/
├── 🎯 QUICKSTART.md                    # Start here! (5-minute setup)
├── 📖 README.md                        # Full documentation
├── 🖥️ FRONTEND_INTEGRATION.md          # React integration guide
├── 🏗️ SYSTEM_OVERVIEW.md               # Architecture deep-dive
├── 🌐 DEPLOYMENT.md                    # This file
│
├── 🔧 Core Backend
│   ├── main.py                         # FastAPI app (200+ lines)
│   ├── data_loader.py                  # CSV processing
│   ├── rag_system.py                   # FAISS search engine
│   ├── llm_service.py                  # OpenAI integration
│   ├── config.py                       # Configuration
│   └── utils.py                        # Helper functions
│
├── 🚀 Utilities
│   ├── init.py                         # One-time setup
│   └── client_example.py               # Testing client
│
├── ⚙️ Configuration
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment template
│   └── .gitignore                      # Git ignore file
│
├── 📊 Data Files (Your CSVs)
│   ├── resumes_validated (1).csv
│   ├── jd_validated.csv
│   ├── skill_role_master.csv
│   └── covers_validated.csv
│
└── 📦 Generated (First Run)
    ├── faiss_index                     # FAISS binary index
    └── metadata.pkl                    # Index metadata
```

---

## 🚀 Deployment Options

### Option 1: Local Development (Easiest)
```bash
# Perfect for: Testing, demos, local use
python main.py
# Runs on http://localhost:8000
```

**Pros:**
- No setup required
- Easy debugging
- Great for development

**Cons:**
- Only accessible locally
- Dies when you close terminal
- Not suitable for production

---

### Option 2: Docker (Recommended for Production)

#### 2A. Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Set environment
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2B. Create .dockerignore

```
__pycache__
.git
.gitignore
.env
.pytest_cache
*.pyc
.DS_Store
venv/
```

#### 2C. Build and Run

```bash
# Build image
docker build -t cover-letter-api:latest .

# Run container
docker run \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  -e API_HOST=0.0.0.0 \
  -e API_PORT=8000 \
  cover-letter-api:latest
```

#### 2D. Docker Compose (Multi-container)

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      LLM_MODEL: gpt-3.5-turbo
      API_HOST: 0.0.0.0
      API_PORT: 8000
    volumes:
      - ./faiss_index:/app/faiss_index
      - ./metadata.pkl:/app/metadata.pkl
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
```

```bash
# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

**Docker Benefits:**
- ✅ Reproducible environment
- ✅ Easy horizontal scaling
- ✅ Works on any OS (Mac, Windows, Linux)
- ✅ Ideal for cloud deployment

---

### Option 3: Traditional Server (Gunicorn + Nginx)

#### 3A. Install Production WSGI Server

```bash
pip install gunicorn
```

#### 3B. Create Systemd Service

```ini
# /etc/systemd/system/cover-letter-api.service
[Unit]
Description=Cover Letter Generator API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/app/CV\ backend
EnvironmentFile=/app/CV\ backend/.env
ExecStart=/usr/local/bin/gunicorn \
  -w 4 \
  -b 0.0.0.0:8000 \
  -k uvicorn.workers.UvicornWorker \
  --timeout 120 \
  --access-logfile /var/log/cover-letter-api/access.log \
  --error-logfile /var/log/cover-letter-api/error.log \
  main:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3C. Configure Nginx as Reverse Proxy

```nginx
# /etc/nginx/sites-available/cover-letter-api
upstream cover_letter_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com www.api.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com www.api.example.com;

    # SSL Certificate (from Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Logging
    access_log /var/log/nginx/cover-letter-api-access.log;
    error_log /var/log/nginx/cover-letter-api-error.log;

    # Gzip compression
    gzip on;
    gzip_types text/plain application/json;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    location / {
        proxy_pass http://cover_letter_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
        proxy_request_buffering off;
        
        # Timeout for long requests
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://cover_letter_api;
        access_log off;
    }
}
```

#### 3D. Start Service

```bash
# Enable service
sudo systemctl enable cover-letter-api

# Start service
sudo systemctl start cover-letter-api

# View logs
sudo journalctl -u cover-letter-api -f

# Check status
sudo systemctl status cover-letter-api
```

**Pros:**
- Traditional, well-tested
- Good performance with Gunicorn
- Industry standard

**Cons:**
- More setup required
- OS-specific
- Manual updates needed

---

### Option 4: Serverless (AWS Lambda, Google Cloud Functions)

#### 4A. AWS Lambda with API Gateway

**Package for Lambda:**
```python
# lambda_handler.py - Adapted from main.py
from mangum import Mangum  # ASGI to WSGI adapter
from main import app

handler = Mangum(app)
```

**Requirements:**
- Create deployment package
- Upload to Lambda
- Configure API Gateway trigger
- Set environment variables

⚠️ Note: FAISS index needs to be bundled (can be large)

#### 4B. Google Cloud Run (Recommended Serverless)

```bash
# Deploy to Google Cloud Run
gcloud run deploy cover-letter-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-... \
  --memory 1Gi \
  --timeout 300
```

**Benefits:**
- Automatic scaling
- No server management
- Only pay for usage

---

### Option 5: PaaS (Platform as a Service)

#### Heroku (Simple, Beginner-Friendly)

**1. Create Procfile:**
```
# Procfile
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

**2. Deploy:**
```bash
heroku login
heroku create cover-letter-api
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main
```

**3. View logs:**
```bash
heroku logs --tail
```

#### Railway (Modern Alternative)

```bash
# Link repository and deploy
railway up
```

#### Fly.io

```bash
# Deploy with fly
fly launch
fly deploy
```

---

## 🔒 Production Security Checklist

### Environment Variables
- [ ] NEVER commit `.env` file
- [ ] Use `.env.example` template
- [ ] Rotate API keys regularly
- [ ] Use separate keys for prod/staging
- [ ] Store secrets in vault (AWS Secrets Manager, etc.)

### API Security
- [ ] Enable HTTPS/SSL only
- [ ] Implement rate limiting (see Nginx config)
- [ ] Add CORS restrictions (configure for your domain)
- [ ] Validate and sanitize inputs
- [ ] Add request timeout limits

### Data Security
- [ ] Don't log API keys or sensitive data
- [ ] Use encrypted connections only
- [ ] Backup FAISS index regularly
- [ ] Monitor unauthorized access

### Example: Secure Startup (main.py)

```python
import os
from fastapi.middleware.cors import CORSMiddleware

# ✅ Secure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
    max_age=600,
)

# ✅ Validate API key on startup
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ OPENAI_API_KEY must be set")

# ✅ Log only non-sensitive info
logging.info(f"🚀 Server starting on {API_HOST}:{API_PORT}")
```

---

## 📊 Monitoring & Logging

### Application Logging

```python
# In config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics to Monitor

1. **Performance:**
   - Response time per request
   - Throughput (requests/second)
   - Error rate

2. **Resources:**
   - CPU usage
   - Memory usage
   - Disk I/O

3. **Business:**
   - Cover letters generated
   - API uptime
   - Cost per request

### Tools

- **Datadog** - Full observability
- **New Relic** - APM + Infrastructure
- **AWS CloudWatch** - For AWS deployments
- **Prometheus + Grafana** - Open source

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: python -m pytest tests/
      
      - name: Build Docker image
        run: docker build -t cover-letter-api:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          docker tag cover-letter-api:${{ github.sha }} cover-letter-api:latest
          docker push cover-letter-api:latest
      
      - name: Deploy to production
        run: |
          # Deploy command (e.g., docker-compose up -d)
          ssh user@prod-server 'cd /app && docker-compose pull && docker-compose up -d'
```

---

## 📈 Scaling Strategy

### Vertical Scaling (Increase Resources)
```bash
# Increase workers
gunicorn -w 8 main:app  # Was 4

# Increase memory (Docker)
docker run -m 2g cover-letter-api
```

### Horizontal Scaling (Multiple Instances)

```yaml
# docker-compose.yml with multiple replicas
version: '3.8'
services:
  api-1:
    build: .
    ports: ["8001:8000"]
  api-2:
    build: .
    ports: ["8002:8000"]
  api-3:
    build: .
    ports: ["8003:8000"]
  
  nginx:
    # Routes to api-1, api-2, api-3
```

### Database Caching

```python
# Add Redis for caching
import redis

cache = redis.Redis(host='localhost', port=6379)

@app.post("/generate-cover-letter")
async def generate(request: CoverLetterRequest):
    # Check cache
    cache_key = hash(request)
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Generate if not cached
    result = llm_service.generate_cover_letter(...)
    
    # Cache for 24 hours
    cache.setex(cache_key, 86400, json.dumps(result))
    return result
```

---

## 🧪 Load Testing

### Using Apache Bench

```bash
# Generate 1000 requests with concurrency of 10
ab -n 1000 -c 10 \
  -H "Content-Type: application/json" \
  -p payload.json \
  http://localhost:8000/generate-cover-letter
```

### Using Locust

```python
# locustfile.py
from locust import HttpUser, task

class LoadTestUser(HttpUser):
    @task
    def generate_cover_letter(self):
        self.client.post("/generate-cover-letter", json={
            "resume_content": "...",
            "job_description": "...",
            "company_name": "Amazon",
            "job_role": "SDE"
        })
```

```bash
# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

---

## 💰 Cost Optimization

### Reduce API Calls

```python
# Cache responses
from functools import lru_cache

@lru_cache(maxsize=1000)
def generate_cached(resume_hash, jd_hash, company):
    # Only call LLM if not cached
    pass
```

### Model Selection

| Model | Speed | Cost | Quality |
|-------|-------|------|---------|
| gpt-3.5-turbo | ⚡⚡⚡ | $ | ⭐⭐⭐ |
| gpt-4-turbo | ⚡⚡ | $$ | ⭐⭐⭐⭐ |
| gpt-4 | ⚡ | $$$ | ⭐⭐⭐⭐⭐ |

### Infrastructure Costs (Monthly Estimates)

| Option | Compute | Storage | Total |
|--------|---------|---------|-------|
| Local | $0 | $0 | **$0** |
| Docker (1 instance) | $5-20 | $1 | **$6-21** |
| Heroku | $50+ | $0 | **$50+** |
| Cloud Run | $0.25/req | $1 | **$25-50** (1000 reqs) |

---

## ✅ Production Deployment Checklist

- [ ] Code tested locally
- [ ] `.env` configured with production API key
- [ ] FAISS index built and tested
- [ ] Docker image builds successfully
- [ ] All dependencies in `requirements.txt`
- [ ] Error handling and logging in place
- [ ] HTTPS/SSL configured
- [ ] Rate limiting enabled
- [ ] CORS configured for production domain
- [ ] Monitoring and alerts set up
- [ ] Backup strategy for FAISS index
- [ ] Disaster recovery plan
- [ ] Security audit completed
- [ ] Load testing passed
- [ ] Documentation updated

---

## 🚨 Emergency Response

### API Down
```bash
# Check logs
docker logs cover-letter-api

# Restart service
docker-compose restart api

# Or manually
systemctl restart cover-letter-api
```

### High Memory Usage
```bash
# Reduce workers
gunicorn -w 2 main:app

# Or limit memory
docker run -m 1g cover-letter-api
```

### Rate Limiting Issues
```nginx
# Increase rate limit in Nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=20r/s;
# Then reload: nginx -s reload
```

---

## 📞 Support & Rollback

### Rollback to Previous Version
```bash
# Git
git revert HEAD
git push

# Docker
docker run cover-letter-api:v1.0.0

# Heroku
heroku releases:rollback
```

---

**Ready to deploy? Start with Docker (Option 2) or Heroku (Option 5) - they're the easiest!**

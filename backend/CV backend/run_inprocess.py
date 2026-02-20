from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

payload = {
    "role": "Data Scientist",
    "job_description": "We are hiring a Data Scientist to build ML models and productionize them.",
    "candidate_profile": "5 years in ML, Python, PyTorch, deployed models in production"
}

resp = client.post("/generate-cover-letter-with-context", json=payload)
print('status_code=', resp.status_code)
print(resp.text)

import json
import urllib.request
import sys

payload = {
    "role": "Data Scientist",
    "job_description": "We are hiring a Data Scientist to build ML models and productionize them.",
    "candidate_profile": "5 years in ML, Python, PyTorch, deployed models in production"
}

url = 'http://127.0.0.1:8000/generate-cover-letter-with-context'
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read().decode('utf-8')
        print(body)
except Exception as e:
    print('ERROR:', e, file=sys.stderr)
    raise

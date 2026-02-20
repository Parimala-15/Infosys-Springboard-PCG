"""
Example client script for testing the Cover Letter Generator API
Run the backend first: python main.py
Then run this script: python client_example.py
"""
import requests
import json
from typing import Dict

# Configuration
API_URL = "http://localhost:8000"

class CoverLetterClient:
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
    
    def health_check(self) -> Dict:
        """Check if API is running"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_available_roles(self) -> list:
        """Get all available roles"""
        response = requests.get(f"{self.base_url}/roles")
        return response.json()['roles']
    
    def generate_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_role: str,
        experience_type: str = "experienced",
        top_k: int = 5
    ) -> Dict:
        """Generate a cover letter"""
        payload = {
            "resume_content": resume_content,
            "job_description": job_description,
            "company_name": company_name,
            "job_role": job_role,
            "experience_type": experience_type,
            "top_k": top_k
        }
        
        response = requests.post(
            f"{self.base_url}/generate-cover-letter",
            json=payload
        )
        
        return response.json()
    
    def generate_with_context(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_role: str,
        top_k: int = 5
    ) -> Dict:
        """Generate cover letter and return context details"""
        payload = {
            "resume_content": resume_content,
            "job_description": job_description,
            "company_name": company_name,
            "job_role": job_role,
            "top_k": top_k
        }
        
        response = requests.post(
            f"{self.base_url}/generate-cover-letter-with-context",
            json=payload
        )
        
        return response.json()
    
    def get_context_by_role(self, role: str, limit: int = 5) -> Dict:
        """Get context chunks for a specific role"""
        response = requests.get(
            f"{self.base_url}/context-by-role/{role}",
            params={"limit": limit}
        )
        return response.json()


def main():
    print("\n" + "="*70)
    print("🎯 Cover Letter Generator - Example Client")
    print("="*70 + "\n")
    
    client = CoverLetterClient()
    
    # 1. Health Check
    print("1️⃣ Health Check")
    print("-" * 70)
    try:
        health = client.health_check()
        print(f"Status: {health['status']}")
        print(f"Index Loaded: {health['index_loaded']}")
        print(f"Timestamp: {health['timestamp']}\n")
    except Exception as e:
        print(f"❌ API not running. Start server with: python main.py")
        print(f"Error: {e}\n")
        return
    
    # 2. Get Available Roles
    print("2️⃣ Available Roles")
    print("-" * 70)
    roles = client.get_available_roles()
    print(f"Total roles: {len(roles)}")
    print(f"Sample roles: {roles[:5]}\n")
    
    # 3. Example Data
    print("3️⃣ Generating Cover Letter Example")
    print("-" * 70)
    
    sample_resume = """
    JOHN DOE
    Senior Software Engineer
    john.doe@example.com | +1-234-567-8900
    
    EXPERIENCE
    Senior Software Engineer | Tech Company | 2021-Present
    - Led development of microservices architecture using Python and Go
    - Optimized database queries, reducing latency by 40%
    - Mentored junior developers and conducted code reviews
    - Technologies: Python, Go, AWS, Docker, Kubernetes
    
    Software Engineer | StartUp Inc | 2019-2021
    - Built REST APIs serving 1M+ requests daily
    - Implemented CI/CD pipelines with Jenkins
    - Collaborated with product teams on feature development
    - Technologies: Java, Spring Boot, PostgreSQL, AWS
    
    EDUCATION
    Bachelor of Technology in Computer Science
    University of Technology, 2019
    
    SKILLS
    Languages: Python, Java, Go, JavaScript, SQL
    Frameworks: Spring Boot, Django, FastAPI
    Tools: Docker, Kubernetes, AWS, Jenkins, Git
    Databases: PostgreSQL, MongoDB, Redis
    """
    
    sample_jd = """
    Senior Software Engineer - Backend
    Company: Tech Corp
    
    We are looking for a Senior Software Engineer to join our backend team.
    
    Responsibilities:
    - Design and implement scalable backend systems
    - Collaborate with frontend teams on API design
    - Optimize system performance and reliability
    - Mentor junior engineers
    - Participate in architecture discussions
    
    Requirements:
    - 5+ years of software engineering experience
    - Strong knowledge of Python or Go
    - Experience with microservices architecture
    - AWS or similar cloud platform experience
    - Experience with Docker and Kubernetes
    
    Preferred Qualifications:
    - Open source contributions
    - Experience with machine learning systems
    - Knowledge of distributed systems
    """
    
    # Generate cover letter
    print("Generating cover letter...\n")
    
    result = client.generate_cover_letter(
        resume_content=sample_resume,
        job_description=sample_jd,
        company_name="Tech Corp",
        job_role="Senior Software Engineer",
        experience_type="experienced",
        top_k=5
    )
    
    if result['success']:
        print("✅ Cover Letter Generated Successfully\n")
        print("GENERATED COVER LETTER:")
        print("-" * 70)
        print(result['cover_letter'])
        print("-" * 70)
        print(f"\nWord Count: {result['word_count']}")
        print(f"Retrieved Context Chunks: {result['retrieved_context_count']}")
        print(f"Generated at: {result['generation_timestamp']}\n")
    else:
        print(f"❌ Generation failed: {result['error']}\n")
    
    # 4. Test with context
    print("4️⃣ Detailed Context Retrieval")
    print("-" * 70)
    
    context_result = client.generate_with_context(
        resume_content=sample_resume,
        job_description=sample_jd,
        company_name="Tech Corp",
        job_role="Senior Software Engineer",
        top_k=3
    )
    
    if context_result['success']:
        print(f"Retrieved {len(context_result['retrieved_context'])} context chunks:\n")
        for i, chunk in enumerate(context_result['retrieved_context'], 1):
            print(f"{i}. Source: {chunk['source']} | Role: {chunk['role']}")
            print(f"   Similarity: {chunk['similarity_score']:.2f}")
            print(f"   Text: {chunk['text'][:100]}...\n")
    
    # 5. Get role-specific context
    print("5️⃣ Role-Specific Context")
    print("-" * 70)
    
    try:
        role_context = client.get_context_by_role("software_engineer", limit=3)
        print(f"Role: {role_context['role']}")
        print(f"Retrieved {role_context['context_count']} contexts\n")
    except Exception as e:
        print(f"Note: {e}\n")
    
    print("="*70)
    print("✅ Example completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

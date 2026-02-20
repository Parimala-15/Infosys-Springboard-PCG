from config import FAISS_INDEX_PATH
from rag_system import RAGSystem
from llm_service import LLMService

# Sample inputs
role = "Data Scientist"
job_description = "We are hiring a Data Scientist to build ML models and productionize them."
company_name = "Acme Corp"
candidate_profile = "5 years in ML, Python, PyTorch, deployed models in production"

print('Loading RAG system and FAISS index...')
rag = RAGSystem()
loaded = rag.load_index(FAISS_INDEX_PATH)
print('Index loaded:', loaded)

query = f"{role} {company_name} {job_description}"
retrieved = []
if loaded:
    retrieved = rag.retrieve_context(query, k=5)
    print('Retrieved', len(retrieved), 'chunks')
else:
    print('No index loaded; proceeding with empty context')

# Initialize LLM service (may raise if OPENAI_API_KEY not set)
try:
    llm = LLMService()
except Exception as e:
    print('LLMService init failed (will still attempt fallback):', e)
    # Create a dummy object with generate_cover_letter method that invokes fallback
    class DummyLLM:
        def generate_cover_letter(self, resume_content, job_description, company_name, job_role, retrieved_context):
            from llm_service import LLMService as _LLM
            return _LLM()._simple_template_generate(resume_content, job_description, company_name, job_role, retrieved_context)
        def validate_output(self, text):
            from llm_service import LLMService as _LLM
            return _LLM().validate_output(text)
    llm = DummyLLM()

cover = llm.generate_cover_letter(
    resume_content=candidate_profile,
    job_description=job_description,
    company_name=company_name,
    job_role=role,
    retrieved_context=retrieved
)

print('\n--- GENERATED COVER LETTER ---\n')
print(cover)
print('\n--- VALIDATION ---\n')
print(llm.validate_output(cover))

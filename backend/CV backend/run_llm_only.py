from llm_service import LLMService

service = LLMService()
cover = service.generate_cover_letter(
    resume_content="5 years in ML, Python, PyTorch, deployed models in production",
    job_description="We are hiring a Data Scientist to build ML models and productionize them.",
    company_name="Acme Corp",
    job_role="Data Scientist",
    retrieved_context=[]
)
print(cover)

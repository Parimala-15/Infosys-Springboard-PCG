import asyncio
from main import startup_event, generate_with_detailed_context, CoverLetterRequest

async def main():
    # Ensure startup initialization
    await startup_event()

    req = CoverLetterRequest(
        resume_content="5 years in ML, Python, PyTorch, deployed models in production",
        job_description="We are hiring a Data Scientist to build ML models and productionize them.",
        company_name="Acme Corp",
        job_role="Data Scientist",
        experience_type="experienced",
        top_k=5
    )

    res = await generate_with_detailed_context(req)
    print(res)

if __name__ == '__main__':
    asyncio.run(main())

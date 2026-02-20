"""
Main FastAPI Backend for Cover Letter Generator
RAG-enabled with LLM integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from datetime import datetime

from data_loader import DataLoader
from rag_system import RAGSystem
from llm_service import LLMService
from config import API_HOST, API_PORT, DATA_DIR, FAISS_INDEX_PATH
from utils import format_retrieved_chunks

# ============================================================================
# Pydantic Models
# ============================================================================

class CoverLetterRequest(BaseModel):
    resume_content: str = Field(..., description="Resume text content")
    job_description: str = Field(..., description="Job description text")
    company_name: str = Field(..., description="Name of the company")
    job_role: str = Field(..., description="Job role/title")
    experience_type: Optional[str] = Field(default="experienced", description="fresher or experienced")
    top_k: Optional[int] = Field(default=5, description="Number of context chunks to retrieve")

class CoverLetterResponse(BaseModel):
    success: bool
    cover_letter: Optional[str] = None
    word_count: Optional[int] = None
    retrieved_context_count: Optional[int] = None
    generation_timestamp: Optional[str] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    index_loaded: bool
    timestamp: str

class RolesResponse(BaseModel):
    roles: List[str]
    count: int

# ============================================================================
# Initialize FastAPI
# ============================================================================

app = FastAPI(
    title="Cover Letter Generator API",
    description="RAG-enabled AI cover letter generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Global Variables
# ============================================================================

data_loader = None
rag_system = None
llm_service = None

# ============================================================================
# Startup & Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize systems on startup"""
    global data_loader, rag_system, llm_service
    
    print("\n🚀 Initializing Cover Letter Generator Backend...\n")
    
    try:
        # Load data
        print("📚 Loading data from CSV files...")
        data_loader = DataLoader(data_dir=DATA_DIR)
        data_loader.load_all_data()
        
        # Initialize RAG system
        print("🔍 Initializing RAG system...")
        rag_system = RAGSystem()
        
        # Try to load existing index; do not attempt to rebuild automatically
        if os.path.exists(FAISS_INDEX_PATH):
            print("📦 Loading existing FAISS index...")
            if rag_system.load_index(FAISS_INDEX_PATH):
                print("✓ FAISS index loaded successfully")
            else:
                print("⚠ Failed to load index. Please run `python init.py` to rebuild the index manually.")
        else:
            print("⚠ FAISS index not found. Please run `python init.py` to build the index before generating cover letters.")
        
        # Initialize LLM service
        print("🤖 Initializing LLM service...")
        try:
            llm_service = LLMService()
            print("✓ LLM service ready")
        except ValueError as e:
            print(f"⚠ LLM service initialization failed: {e}")
            print("   Cover letter generation will not work until OPENAI_API_KEY is set")
        
        print("\n✅ Backend initialized successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Startup failed: {e}\n")
        raise

def build_rag_index():
    """Build FAISS index from data"""
    global rag_system
    
    chunks = data_loader.create_chunks()
    rag_system.build_index(chunks)
    rag_system.save_index(FAISS_INDEX_PATH)

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        index_loaded=rag_system is not None and rag_system.index is not None,
        timestamp=datetime.now().isoformat()
    )

@app.get("/roles", response_model=RolesResponse)
async def get_available_roles():
    """Get all available roles in the dataset"""
    if data_loader is None:
        raise HTTPException(status_code=503, detail="Data not loaded yet")
    
    roles = data_loader.get_all_unique_roles()
    return RolesResponse(roles=roles, count=len(roles))

@app.post("/generate-cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter(request: CoverLetterRequest) -> CoverLetterResponse:
    """
    Generate a cover letter using RAG + LLM
    
    Process:
    1. Retrieve relevant context from FAISS index
    2. Pass context to LLM with system prompt
    3. Generate customized cover letter
    4. Post-process for ATS compliance
    """
    try:
        if llm_service is None:
            return CoverLetterResponse(
                success=False,
                error="LLM service not initialized. Set OPENAI_API_KEY environment variable."
            )
        
        if rag_system is None or rag_system.index is None:
            return CoverLetterResponse(
                success=False,
                error="RAG system not initialized"
            )
        
        # Step 1: Retrieve relevant context
        print(f"\n📌 Generating cover letter for: {request.job_role} at {request.company_name}")
        print(f"   Retrieving top {request.top_k} context chunks...")
        
        query = f"{request.job_role} {request.company_name} {request.job_description}"
        retrieved_context = rag_system.retrieve_context(query, k=request.top_k)
        
        print(f"   ✓ Retrieved {len(retrieved_context)} context chunks")
        
        # Step 2: Generate cover letter
        print("   Generating cover letter with LLM...")
        cover_letter = llm_service.generate_cover_letter(
            resume_content=request.resume_content,
            job_description=request.job_description,
            company_name=request.company_name,
            job_role=request.job_role,
            retrieved_context=retrieved_context
        )
        
        # Step 3: Validate output
        validation = llm_service.validate_output(cover_letter)
        word_count = validation['word_count']
        
        print(f"   ✓ Generated {word_count} words")
        print(f"   ✓ Valid format: {validation['valid']}")
        
        return CoverLetterResponse(
            success=True,
            cover_letter=cover_letter,
            word_count=word_count,
            retrieved_context_count=len(retrieved_context),
            generation_timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"\n❌ Error generating cover letter: {str(e)}\n")
        return CoverLetterResponse(
            success=False,
            error=f"Generation failed: {str(e)}"
        )

@app.post("/generate-cover-letter-with-context")
async def generate_with_detailed_context(request: CoverLetterRequest):
    """
    Generate cover letter and return retrieved context details
    Useful for debugging and understanding what the LLM used
    """
    try:
        if rag_system is None or rag_system.index is None:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        # Retrieve context
        query = f"{request.job_role} {request.company_name}"
        retrieved_context = rag_system.retrieve_context(query, k=request.top_k)
        
        # Generate cover letter
        cover_letter = llm_service.generate_cover_letter(
            resume_content=request.resume_content,
            job_description=request.job_description,
            company_name=request.company_name,
            job_role=request.job_role,
            retrieved_context=retrieved_context
        )
        
        validation = llm_service.validate_output(cover_letter)
        
        return {
            "success": True,
            "cover_letter": cover_letter,
            "word_count": validation['word_count'],
            "retrieved_context": [
                {
                    "text": chunk['text'][:300],
                    "source": chunk['metadata'].get('source'),
                    "role": chunk['metadata'].get('role'),
                    "similarity_score": chunk['similarity_score']
                }
                for chunk in retrieved_context
            ],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/context-by-role/{role}")
async def get_context_by_role(
    role: str,
    experience_type: Optional[str] = None,
    limit: int = 5
):
    """Retrieve context chunks for a specific role"""
    try:
        if rag_system is None or rag_system.index is None:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        results = rag_system.retrieve_by_role(role, k=limit)
        
        return {
            "role": role,
            "experience_type": experience_type,
            "context_count": len(results),
            "contexts": [
                {
                    "text": r['text'][:300],
                    "metadata": r['metadata'],
                    "similarity_score": r['similarity_score']
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Run
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🎯 Cover Letter Generator API")
    print("="*70)
    
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        reload=False,
        log_level="info"
    )

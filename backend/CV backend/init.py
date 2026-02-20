"""
Quick initialization script to build FAISS index and validate setup
Run this before starting the server for the first time
"""
import os
import sys
from pathlib import Path

def check_files():
    """Check if all required CSV files exist"""
    print("\n📁 Checking CSV files...")
    required_files = [
        "resumes_validated (1).csv",
        "jd_validated.csv",
        "skill_role_master.csv",
        "covers_validated.csv"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # MB
            print(f"   ✓ {file} ({size:.2f} MB)")
        else:
            print(f"   ✗ {file} NOT FOUND")
            return False
    
    return True

def check_env():
    """Check environment configuration"""
    print("\n🔐 Checking environment configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print(f"   ✓ OPENAI_API_KEY is set")
    else:
        print(f"   ⚠ OPENAI_API_KEY not set - LLM will not work")
        print(f"   → Add it to .env file: OPENAI_API_KEY=sk-...")
    
    return True

def build_index():
    """Build FAISS index"""
    print("\n🏗 Building FAISS index...")
    
    try:
        from data_loader import DataLoader
        from rag_system import RAGSystem
        
        # Load data
        data_loader = DataLoader(data_dir="./")
        data_loader.load_all_data()
        
        # Create chunks
        print("   Creating chunks from data...")
        chunks = data_loader.create_chunks()
        print(f"   Generated {len(chunks)} chunks")
        
        # Build index
        print("   Building FAISS index (this may take a minute)...")
        rag_system = RAGSystem()
        rag_system.build_index(chunks)
        rag_system.save_index("./faiss_index")
        
        print("   ✓ Index built successfully")
        return True
        
    except Exception as e:
        print(f"   ✗ Error building index: {e}")
        return False

def test_rag():
    """Test RAG retrieval"""
    print("\n🔍 Testing RAG retrieval...")
    
    try:
        from rag_system import RAGSystem
        
        rag_system = RAGSystem()
        if rag_system.load_index("./faiss_index"):
            results = rag_system.retrieve_context("software engineer", k=3)
            print(f"   ✓ Retrieved {len(results)} chunks")
            for i, result in enumerate(results, 1):
                print(f"     {i}. {result['metadata'].get('source')} (similarity: {result['similarity_score']:.2f})")
            return True
        else:
            print("   ✗ Failed to load index")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_llm():
    """Test LLM connection"""
    print("\n🤖 Testing LLM connection...")
    
    try:
        from llm_service import LLMService
        
        llm_service = LLMService()
        print("   ✓ LLM service connected")
        return True
        
    except ValueError as e:
        print(f"   ⚠ {e}")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 Cover Letter Generator - Setup & Validation")
    print("="*60)
    
    # Check files
    if not check_files():
        print("\n❌ Missing CSV files. Place them in the same directory.")
        sys.exit(1)
    
    # Check environment
    check_env()
    
    # Build index
    if not build_index():
        print("\n❌ Failed to build FAISS index")
        sys.exit(1)
    
    # Test RAG
    if not test_rag():
        print("\n❌ RAG system test failed")
        sys.exit(1)
    
    # Test LLM
    llm_ok = test_llm()
    
    print("\n" + "="*60)
    if llm_ok:
        print("✅ All systems ready! Start server with: python main.py")
    else:
        print("✅ RAG system ready. LLM will work once API key is added.")
        print("   Start server with: python main.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

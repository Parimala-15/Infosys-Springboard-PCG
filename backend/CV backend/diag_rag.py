from rag_system import RAGSystem
r = RAGSystem()
print('use_openai=', r.use_openai)
print('load_index:', r.load_index('./faiss_index'))

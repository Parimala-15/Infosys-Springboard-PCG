import traceback
from config import DATA_DIR, FAISS_INDEX_PATH

print('DATA_DIR=', DATA_DIR)
print('FAISS_INDEX_PATH=', FAISS_INDEX_PATH)

try:
    from data_loader import DataLoader
    from rag_system import RAGSystem

    dl = DataLoader(data_dir=DATA_DIR)
    dl.load_all_data()
    print('Data loaded OK')

    rag = RAGSystem()
    print('RAGSystem initialized OK')

    ok = rag.load_index(FAISS_INDEX_PATH)
    print('load_index returned', ok)

except Exception as e:
    print('Exception during diag_startup:')
    traceback.print_exc()
    raise

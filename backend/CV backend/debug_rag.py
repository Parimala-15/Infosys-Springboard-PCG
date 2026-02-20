import traceback
import sys

print('sys.modules os before import:', sys.modules.get('os'))

try:
    from rag_system import RAGSystem
    r = RAGSystem()
    r.build_index([('hello world', {'source':'debug','role':'none'})])
except Exception:
    traceback.print_exc()
    raise

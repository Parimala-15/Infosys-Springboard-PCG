"""
Utility functions
"""
from typing import Dict, List
import re

def extract_text_section(text: str, section_name: str) -> str:
    """Extract a specific section from resume/text"""
    lines = text.split('\n')
    result = []
    capture = False
    
    for line in lines:
        if section_name.lower() in line.lower():
            capture = True
            continue
        
        if capture:
            if re.match(r'^[A-Z][A-Z\s]+$', line.strip()) and line.strip():
                break
            result.append(line)
    
    return '\n'.join(result).strip()

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def format_retrieved_chunks(chunks: List[Dict]) -> str:
    """Format retrieved chunks for display"""
    formatted = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get('metadata', {}).get('source', 'unknown')
        similarity = chunk.get('similarity_score', 0)
        text_preview = chunk.get('text', '')[:200]
        
        formatted.append(
            f"[{i}] {source.upper()} (similarity: {similarity:.2f})\n{text_preview}...\n"
        )
    
    return "\n".join(formatted)

def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """Estimate reading time in minutes"""
    word_count = len(text.split())
    return max(1, word_count // wpm)

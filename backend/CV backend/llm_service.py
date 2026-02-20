"""
LLM Service Module
Handles LLM calls and cover letter generation with post-processing
"""
import os
import re
import textwrap
from typing import Dict, List
from config import OPENAI_API_KEY, LLM_MODEL, MAX_TOKENS

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class LLMService:
    def __init__(self, api_key: str = OPENAI_API_KEY):
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        self.client = OpenAI(api_key=api_key)
        self.model = LLM_MODEL
        self.max_tokens = MAX_TOKENS
        
    def generate_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_role: str,
        retrieved_context: List[Dict]
    ) -> str:
        """
        Generate cover letter using RAG context and LLM
        """
        # Format retrieved context
        context_text = self._format_context(retrieved_context)
        
        # Build system prompt
        system_prompt = self._get_system_prompt()
        
        # Build user prompt
        user_prompt = self._build_user_prompt(
            resume_content,
            job_description,
            company_name,
            job_role,
            context_text
        )
        
        # Call LLM and fallback to template on error or quota issues
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )

            cover_letter = response.choices[0].message.content
            cover_letter = self._post_process(cover_letter)
            return cover_letter
        except Exception:
            # Fallback: simple template-based generator using retrieved context
            return self._simple_template_generate(
                resume_content, job_description, company_name, job_role, retrieved_context
            )
    
    def _get_system_prompt(self) -> str:
        """System prompt for cover letter generation"""
        return """You are an AI Cover Letter Generator integrated into a Resume Builder system.

Your task: Generate a highly professional, ATS-friendly cover letter using ONLY the provided context.

Rules:
- Do NOT hallucinate skills or experience.
- Use only resume and retrieved documents.
- Keep length within 300–400 words.
- Match the job role and company tone.
- Maintain formal, confident, and human-like language.
- Avoid generic phrases like "I am writing to apply".
- Start with strong personalized opening mentioning company name and role.
- Include 2-3 specific skills aligned with job description.
- Reference relevant projects or internships with impact.
- Show cultural and company alignment.
- End with polite professional closing.
- Format as plain text paragraphs (no bullet points, no markdown)."""
    
    def _build_user_prompt(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_role: str,
        retrieved_context: str
    ) -> str:
        """Build dynamic user prompt"""
        return f"""Generate a customized cover letter using this information:

**Company Name:** {company_name}
**Job Role:** {job_role}

**Candidate Resume:**
{resume_content}

**Job Description:**
{job_description}

**Retrieved Relevant Context:**
{retrieved_context}

Generate a professional, personalized cover letter now."""
    
    def _format_context(self, retrieved_chunks: List[Dict]) -> str:
        """Format retrieved chunks into readable context"""
        if not retrieved_chunks:
            return "No additional context retrieved."
        
        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            source = chunk.get('metadata', {}).get('source', 'unknown')
            text = chunk.get('text', '')[:300]  # First 300 chars
            context_parts.append(f"Context {i} ({source}):\n{text}\n")
        
        return "\n".join(context_parts)
    
    def _post_process(self, text: str) -> str:
        """Clean and format output"""
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'__(.*?)__', r'\1', text)      # Bold alt
        text = re.sub(r'_(.*?)_', r'\1', text)        # Italic alt
        text = re.sub(r'`(.*?)`', r'\1', text)        # Code
        
        # Remove bullet points
        text = re.sub(r'^[\s]*[-•*]\s+', '', text, flags=re.MULTILINE)
        
        # Remove emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & pictographs
            "\U0001F680-\U0001F6FF"  # Transport & map
            "\U0001F1E0-\U0001F1FF"  # Flags
            "]+", flags=re.UNICODE
        )
        text = emoji_pattern.sub(r'', text)
        
        # Fix multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        
        # Fix multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Ensure proper paragraph spacing
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        text = '\n\n'.join(paragraphs)
        
        return text.strip()

    def _simple_template_generate(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        job_role: str,
        retrieved_context: List[Dict]
    ) -> str:
        """Deterministic fallback cover letter generator (no LLM)."""
        # Get a short intro from resume
        intro = resume_content.strip().split('\n')[0][:200]

        # Collect up to 3 context highlights
        highlights = []
        for c in (retrieved_context or [])[:3]:
            txt = c.get('text', '').strip().replace('\n', ' ')
            if txt:
                highlights.append(textwrap.shorten(txt, width=200, placeholder='...'))

        paragraphs = []
        paragraphs.append(
            f"Dear {company_name} Hiring Team,\n\nI am writing to express my interest in the {job_role} role at {company_name}. {intro}"
        )

        if highlights:
            para = "In particular, I bring relevant experience and accomplishments such as: "
            para += "; ".join(highlights)
            paragraphs.append(para)
        else:
            # Use job description bullets if no highlights
            jd_snippet = job_description.strip().split('\n')[0][:300]
            paragraphs.append(f"My background aligns with the role requirements, including: {jd_snippet}")

        paragraphs.append(
            "I am excited about the opportunity to contribute to your team and would welcome the chance to discuss how my background fits this role. Thank you for considering my application."
        )

        paragraphs.append("Sincerely,\n[Your Name]")

        cover = "\n\n".join(paragraphs)
        return cover
    
    def validate_output(self, text: str) -> Dict:
        """Validate cover letter constraints"""
        word_count = len(text.split())
        has_emojis = bool(re.search(r'[\U0001F600-\U0001F64F]', text))
        has_bullets = bool(re.search(r'^[\s]*[-•*]\s+', text, re.MULTILINE))
        has_markdown = bool(re.search(r'[*_`#\[\]]', text))
        
        return {
            'word_count': word_count,
            'valid': not (has_emojis or has_bullets or has_markdown),
            'issues': {
                'has_emojis': has_emojis,
                'has_bullets': has_bullets,
                'has_markdown': has_markdown
            }
        }

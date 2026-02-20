"""
Data loader module to read and process CSV files
"""
import pandas as pd
from typing import Dict, List, Tuple
import os

class DataLoader:
    def __init__(self, data_dir: str = "./"):
        self.data_dir = data_dir
        self.resumes_df = None
        self.jd_df = None
        self.skills_df = None
        self.covers_df = None
        
    def load_all_data(self) -> None:
        """Load all CSV files"""
        self.resumes_df = pd.read_csv(os.path.join(self.data_dir, "resumes_validated (1).csv"))
        self.jd_df = pd.read_csv(os.path.join(self.data_dir, "jd_validated.csv"))
        self.skills_df = pd.read_csv(os.path.join(self.data_dir, "skill_role_master.csv"))
        self.covers_df = pd.read_csv(os.path.join(self.data_dir, "covers_validated.csv"))
        
        print("✓ All CSV files loaded successfully")
        
    def get_resume_by_role(self, role: str, experience_type: str = None) -> List[Dict]:
        """Get resume content by role"""
        query = self.resumes_df[self.resumes_df['role'].str.lower() == role.lower()]
        if experience_type:
            query = query[query['experience_type'].str.lower() == experience_type.lower()]
        
        return query.to_dict('records')
    
    def get_jd_by_role(self, role: str, experience_type: str = None) -> List[Dict]:
        """Get job descriptions by role"""
        query = self.jd_df[self.jd_df['role'].str.lower() == role.lower()]
        if experience_type:
            query = query[query['experience_type'].str.lower() == experience_type.lower()]
        
        return query.to_dict('records')
    
    def get_skills_by_role(self, role: str, experience_type: str = None) -> Dict:
        """Get skills mapping for a role"""
        query = self.skills_df[self.skills_df['role'].str.lower() == role.lower()]
        if experience_type:
            query = query[query['experience_type'].str.lower() == experience_type.lower()]
        
        if not query.empty:
            return query.iloc[0].to_dict()
        return {}
    
    def get_cover_templates(self, role: str, experience_type: str = None) -> List[Dict]:
        """Get cover letter templates by role"""
        query = self.covers_df[self.covers_df['role'].str.lower() == role.lower()]
        if experience_type:
            query = query[query['experience_type'].str.lower() == experience_type.lower()]
        
        return query.to_dict('records')
    
    def get_all_unique_roles(self) -> List[str]:
        """Get all unique roles in the dataset"""
        roles = set()
        roles.update(self.resumes_df['role'].unique())
        roles.update(self.jd_df['role'].unique())
        roles.update(self.skills_df['role'].unique())
        return sorted(list(roles))
    
    def create_chunks(self, chunk_size: int = 500) -> List[Tuple[str, Dict]]:
        """
        Create text chunks from data with metadata
        Returns: List of (text_chunk, metadata) tuples
        """
        chunks = []
        
        # Process resumes
        for _, row in self.resumes_df.iterrows():
            text = row.get('text', '')
            if text and len(text) > 0:
                metadata = {
                    'source': 'resume',
                    'role': row.get('role'),
                    'experience_type': row.get('experience_type'),
                    'type': row.get('experience_type')
                }
                chunks.append((text, metadata))
        
        # Process job descriptions
        for _, row in self.jd_df.iterrows():
            text = row.get('text', '')
            if text and len(text) > 0:
                metadata = {
                    'source': 'job_description',
                    'role': row.get('role'),
                    'job_title': row.get('job title'),
                    'skills': row.get('skills'),
                    'experience_type': row.get('experience_type')
                }
                chunks.append((text, metadata))
        
        # Process skills
        for _, row in self.skills_df.iterrows():
            text = f"Role: {row.get('role', '')}. Skills: {row.get('skills', '')}. Education: {row.get('education', '')}"
            if text:
                metadata = {
                    'source': 'skill_mapping',
                    'role': row.get('role'),
                    'skills': row.get('skills'),
                    'experience_type': row.get('experience_type')
                }
                chunks.append((text, metadata))
        
        return chunks

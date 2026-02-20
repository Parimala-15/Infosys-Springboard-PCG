# Frontend Integration Guide

## Quick Start for React Frontend

### 1. API Endpoint Configuration

Create a service file `services/coverLetterAPI.js`:

```javascript
// services/coverLetterAPI.js
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const generateCoverLetter = async (payload) => {
  try {
    const response = await fetch(`${API_URL}/generate-cover-letter`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error generating cover letter:', error);
    throw error;
  }
};

export const getAvailableRoles = async () => {
  const response = await fetch(`${API_URL}/roles`);
  const data = await response.json();
  return data.roles;
};

export const healthCheck = async () => {
  const response = await fetch(`${API_URL}/health`);
  return await response.json();
};
```

### 2. React Component Example

```javascript
// components/CoverLetterGenerator.jsx
import React, { useState, useEffect } from 'react';
import { generateCoverLetter, getAvailableRoles } from '../services/coverLetterAPI';

const CoverLetterGenerator = () => {
  const [formData, setFormData] = useState({
    resume_content: '',
    job_description: '',
    company_name: '',
    job_role: '',
    experience_type: 'experienced',
    top_k: 5,
  });

  const [coverLetter, setCoverLetter] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [roles, setRoles] = useState([]);
  const [wordCount, setWordCount] = useState(0);

  // Load available roles on mount
  useEffect(() => {
    const loadRoles = async () => {
      try {
        const availableRoles = await getAvailableRoles();
        setRoles(availableRoles);
      } catch (err) {
        console.error('Error loading roles:', err);
      }
    };

    loadRoles();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setCoverLetter('');

    try {
      const result = await generateCoverLetter(formData);

      if (result.success) {
        setCoverLetter(result.cover_letter);
        setWordCount(result.word_count);
      } else {
        setError(result.error || 'Failed to generate cover letter');
      }
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([coverLetter], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `${formData.company_name}_${formData.job_role}_CoverLetter.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(coverLetter);
    alert('Cover letter copied to clipboard!');
  };

  return (
    <div className="cover-letter-generator">
      <h1>AI Cover Letter Generator</h1>

      <form onSubmit={handleGenerate} className="form">
        {/* Resume Content */}
        <div className="form-group">
          <label>Resume Content *</label>
          <textarea
            name="resume_content"
            value={formData.resume_content}
            onChange={handleInputChange}
            placeholder="Paste your full resume here..."
            required
            rows={8}
          />
        </div>

        {/* Job Description */}
        <div className="form-group">
          <label>Job Description *</label>
          <textarea
            name="job_description"
            value={formData.job_description}
            onChange={handleInputChange}
            placeholder="Paste the job description here..."
            required
            rows={8}
          />
        </div>

        {/* Company Name */}
        <div className="form-group">
          <label>Company Name *</label>
          <input
            type="text"
            name="company_name"
            value={formData.company_name}
            onChange={handleInputChange}
            placeholder="e.g., Amazon, Google"
            required
          />
        </div>

        {/* Job Role */}
        <div className="form-group">
          <label>Job Role *</label>
          <input
            type="text"
            name="job_role"
            value={formData.job_role}
            onChange={handleInputChange}
            placeholder="e.g., Senior Software Engineer"
            required
            list="roles"
          />
          <datalist id="roles">
            {roles.map(role => (
              <option key={role} value={role} />
            ))}
          </datalist>
        </div>

        {/* Experience Type */}
        <div className="form-group">
          <label>Experience Level</label>
          <select
            name="experience_type"
            value={formData.experience_type}
            onChange={handleInputChange}
          >
            <option value="fresher">Fresher</option>
            <option value="experienced">Experienced</option>
          </select>
        </div>

        {/* Context Chunks */}
        <div className="form-group">
          <label>Context Chunks (Top-K) *</label>
          <input
            type="number"
            name="top_k"
            value={formData.top_k}
            onChange={handleInputChange}
            min="1"
            max="10"
          />
          <small>Number of relevant context chunks to retrieve (1-10)</small>
        </div>

        {/* Submit Button */}
        <button type="submit" disabled={loading} className="btn-generate">
          {loading ? '⏳ Generating...' : '✨ Generate Cover Letter'}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <strong>❌ Error:</strong> {error}
        </div>
      )}

      {/* Generated Cover Letter */}
      {coverLetter && (
        <div className="output-section">
          <div className="output-header">
            <h2>Generated Cover Letter</h2>
            <div className="output-stats">
              <span>📝 {wordCount} words</span>
              <span>✅ ATS-Friendly</span>
            </div>
          </div>

          <textarea
            readOnly
            value={coverLetter}
            className="output-textarea"
            rows={12}
          />

          <div className="action-buttons">
            <button onClick={handleCopy} className="btn-copy">
              📋 Copy to Clipboard
            </button>
            <button onClick={handleDownload} className="btn-download">
              💾 Download as .txt
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CoverLetterGenerator;
```

### 3. CSS Styling (Optional)

```css
/* styles/CoverLetterGenerator.css */
.cover-letter-generator {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.form {
  background: #f8f9fa;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
  font-family: 'Courier New', monospace;
}

.form-group small {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 12px;
}

.btn-generate {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  padding: 15px;
  background-color: #fee;
  border-left: 4px solid #c33;
  border-radius: 4px;
  margin-bottom: 20px;
  color: #c33;
}

.output-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  border: 2px solid #e8f0fe;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.output-header h2 {
  margin: 0;
  color: #333;
}

.output-stats {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #666;
}

.output-textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  background: #fafafa;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-copy,
.btn-download {
  flex: 1;
  padding: 10px;
  border: 1px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-copy:hover,
.btn-download:hover {
  background: #667eea;
  color: white;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #667eea;
}
```

### 4. Environment Configuration

Create `.env.local`:

```
REACT_APP_API_URL=http://localhost:8000
```

### 5. Error Handling Best Practices

```javascript
const handleGenerateWithErrorHandling = async (e) => {
  e.preventDefault();

  // Validate inputs
  if (!formData.resume_content.trim()) {
    setError('Resume content is required');
    return;
  }

  if (!formData.job_description.trim()) {
    setError('Job description is required');
    return;
  }

  try {
    setLoading(true);
    setError('');

    const result = await generateCoverLetter(formData);

    if (!result.success) {
      if (result.error.includes('OPENAI_API_KEY')) {
        setError(
          'API key not configured. Contact administrator.'
        );
      } else if (result.error.includes('RAG system')) {
        setError('System is initializing. Please try again.');
      } else {
        setError(result.error);
      }
      return;
    }

    setCoverLetter(result.cover_letter);
    setWordCount(result.word_count);

  } catch (err) {
    if (err.message.includes('fetch')) {
      setError('Cannot connect to API. Is the backend running?');
    } else {
      setError('An unexpected error occurred. Please try again.');
    }
    console.error('Detailed error:', err);

  } finally {
    setLoading(false);
  }
};
```

### 6. Advanced: Get Context Details

```javascript
export const generateWithContext = async (payload) => {
  const response = await fetch(
    `${API_URL}/generate-cover-letter-with-context`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }
  );

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return await response.json();
};

// Usage in component
const handleShowContext = async () => {
  const result = await generateWithContext(formData);

  console.log('Generated with context:');
  result.retrieved_context.forEach((ctx, i) => {
    console.log(`${i + 1}. ${ctx.source} (similarity: ${ctx.similarity_score})`);
  });
};
```

## Deployment Checklist

- [ ] Backend API running on production server
- [ ] `.env` file configured with `OPENAI_API_KEY`
- [ ] FAISS index built and saved
- [ ] CORS configured for frontend domain
- [ ] Error boundaries added to React app
- [ ] Loading states implemented
- [ ] Download/copy functionality working
- [ ] API URL environment variable set in `.env.local`
- [ ] Rate limiting considered for production
- [ ] Logging/monitoring in place

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Cannot connect to API` | Ensure backend is running: `python main.py` |
| `CORS error` | Update CORS origins in `main.py` |
| `Slow response` | Increase `top_k` or use GPU FAISS |
| `Out of memory` | Reduce `MAX_TOKENS` in config |


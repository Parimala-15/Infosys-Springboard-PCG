import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, FileText, Wand2, Shield, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ResumePreview } from '@/components/ResumePreview';
import { resumeTemplates } from '@/data/resumeTemplates';
import { useState } from 'react';
import { toast } from 'sonner';

const TemplatePreview = () => {
  const { templateId } = useParams();
  const navigate = useNavigate();
  const [experienceType, setExperienceType] = useState<'experienced' | 'fresher'>('experienced');
  
  const template = resumeTemplates.find(t => t.id === templateId);
  
  if (!template) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="font-serif text-2xl font-bold mb-2">Template Not Found</h1>
          <p className="text-muted-foreground mb-4">The requested template does not exist.</p>
          <Button onClick={() => navigate('/templates')}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Templates
          </Button>
        </div>
      </div>
    );
  }

  const handleUseTemplate = () => {
    toast.success('Template selected! This data will flow into your cover letter generation.', {
      description: 'Your resume data is ready to power personalized cover letters.',
      duration: 4000,
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-card/80 backdrop-blur-md border-b border-border">
        <div className="container max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => navigate('/templates')}
                className="gap-2"
              >
                <ArrowLeft className="w-4 h-4" />
                Back
              </Button>
              <div className="hidden sm:block h-6 w-px bg-border" />
              <div className="hidden sm:block">
                <h1 className="font-serif text-lg font-semibold">{template.name}</h1>
                <p className="text-xs text-muted-foreground">Preview Mode</p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              {/* Experience Type Toggle */}
              <div className="flex rounded-lg bg-secondary p-1">
                <button
                  className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all ${
                    experienceType === 'experienced' 
                      ? 'bg-card text-foreground shadow-sm' 
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                  onClick={() => setExperienceType('experienced')}
                >
                  Experienced
                </button>
                <button
                  className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all ${
                    experienceType === 'fresher' 
                      ? 'bg-card text-foreground shadow-sm' 
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                  onClick={() => setExperienceType('fresher')}
                >
                  Fresher
                </button>
              </div>
              
              <Button 
                className="btn-hero gap-2"
                onClick={handleUseTemplate}
              >
                <Wand2 className="w-4 h-4" />
                <span className="hidden sm:inline">Use for Cover Letter</span>
                <span className="sm:hidden">Use</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-[1fr_320px] gap-8">
          {/* Resume Preview */}
          <div className="order-2 lg:order-1">
            <div className="animate-fade-in">
              <ResumePreview template={template} experienceType={experienceType} />
            </div>
          </div>
          
          {/* Sidebar */}
          <aside className="order-1 lg:order-2 space-y-6">
            {/* Template Info Card */}
            <div className="card-elevated p-6 sticky top-24">
              <div className="flex items-center gap-3 mb-4">
                <div 
                  className="w-12 h-12 rounded-xl flex items-center justify-center"
                  style={{ background: `linear-gradient(135deg, ${template.accentColor}, ${template.accentColor}80)` }}
                >
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="font-serif text-xl font-semibold">{template.name}</h2>
                  <p className="text-sm text-muted-foreground">Resume Template</p>
                </div>
              </div>
              
              <p className="text-muted-foreground text-sm mb-6">
                {template.description}
              </p>
              
              {/* Section Visibility Info */}
              <div className="mb-6">
                <h3 className="text-sm font-semibold mb-3">Visible Sections ({experienceType})</h3>
                <div className="space-y-2 text-sm">
                  {experienceType === 'fresher' && (
                    <p className="flex items-center gap-2 text-fresher">
                      <span className="w-2 h-2 rounded-full bg-fresher" />
                      Experience section hidden for freshers
                    </p>
                  )}
                  {template.categories.includes('technical') && (
                    <p className="flex items-center gap-2 text-technical">
                      <span className="w-2 h-2 rounded-full bg-technical" />
                      Skills & Projects emphasized
                    </p>
                  )}
                  {(experienceType === 'fresher' || template.categories.includes('non-technical')) && (
                    <p className="flex items-center gap-2 text-accent">
                      <span className="w-2 h-2 rounded-full bg-accent" />
                      Activities section highlighted
                    </p>
                  )}
                </div>
              </div>
              
              {/* Actions */}
              <div className="space-y-3">
                <Button 
                  className="w-full btn-hero gap-2"
                  onClick={handleUseTemplate}
                >
                  <Wand2 className="w-4 h-4" />
                  Use This Template for Cover Letter
                </Button>
                
                <Button variant="outline" className="w-full gap-2">
                  <Download className="w-4 h-4" />
                  Download PDF
                </Button>
              </div>
              
              {/* Privacy Note */}
              <div className="mt-6 p-4 rounded-lg bg-secondary/50 border border-border/50">
                <div className="flex items-start gap-3">
                  <Shield className="w-5 h-5 text-fresher flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-semibold mb-1">Your Privacy Matters</h4>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Resume data is used only for template preview and cover letter generation. 
                      Your information is never stored or shared with third parties.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
};

export default TemplatePreview;

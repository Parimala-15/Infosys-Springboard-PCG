import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Sparkles, Shield, FileText, ChevronRight } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { TemplateCard } from '@/components/TemplateCard';
import { resumeTemplates, TemplateCategory } from '@/data/resumeTemplates';

const categoryFilters: { label: string; value: TemplateCategory | 'all' }[] = [
  { label: 'All Templates', value: 'all' },
  { label: 'Fresher', value: 'fresher' },
  { label: 'Experienced', value: 'experienced' },
  { label: 'Technical', value: 'technical' },
  { label: 'Creative', value: 'creative' },
];

const Templates = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState<TemplateCategory | 'all'>('all');

  const filteredTemplates = resumeTemplates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          template.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = activeFilter === 'all' || template.categories.includes(activeFilter);
    return matchesSearch && matchesCategory;
  });

  const handlePreview = (templateId: string) => {
    navigate(`/templates/${templateId}`);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="section-gradient text-primary-foreground py-16 md:py-24">
        <div className="container max-w-6xl mx-auto px-4">
          <div className="text-center max-w-3xl mx-auto animate-fade-in">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-sm font-medium mb-6">
              <Sparkles className="w-4 h-4" />
              AI-Powered Resume Templates
            </div>
            
            <h1 className="font-serif text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Choose Your Perfect
              <span className="block gradient-text bg-gradient-to-r from-accent to-primary">Resume Template</span>
            </h1>
            
            <p className="text-lg md:text-xl text-white/80 mb-8 max-w-2xl mx-auto">
              Professional templates designed for every career stage. 
              Smart logic adapts sections based on your experience level.
            </p>
            
            {/* Search Bar */}
            <div className="relative max-w-xl mx-auto">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <Input 
                type="text"
                placeholder="Search templates..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-12 pr-4 py-6 text-base bg-card text-foreground border-0 shadow-elevated rounded-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Filters */}
      <section className="bg-card border-b border-border sticky top-0 z-40">
        <div className="container max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
            <Filter className="w-4 h-4 text-muted-foreground flex-shrink-0" />
            {categoryFilters.map((filter) => (
              <button
                key={filter.value}
                onClick={() => setActiveFilter(filter.value)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
                  activeFilter === filter.value
                    ? 'bg-primary text-primary-foreground shadow-sm'
                    : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
                }`}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Templates Grid */}
      <section className="py-12 md:py-16">
        <div className="container max-w-6xl mx-auto px-4">
          {filteredTemplates.length > 0 ? (
            <>
              <div className="flex items-center justify-between mb-8">
                <p className="text-muted-foreground">
                  Showing <span className="font-semibold text-foreground">{filteredTemplates.length}</span> templates
                </p>
              </div>
              
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
                {filteredTemplates.map((template, index) => (
                  <div 
                    key={template.id} 
                    className="animate-slide-up"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <TemplateCard template={template} onPreview={handlePreview} />
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-16">
              <FileText className="w-16 h-16 text-muted-foreground/50 mx-auto mb-4" />
              <h3 className="font-serif text-xl font-semibold mb-2">No templates found</h3>
              <p className="text-muted-foreground mb-4">Try adjusting your search or filters</p>
              <Button 
                variant="outline" 
                onClick={() => { setSearchQuery(''); setActiveFilter('all'); }}
              >
                Clear Filters
              </Button>
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-secondary/50">
        <div className="container max-w-4xl mx-auto px-4">
          <div className="card-elevated p-8 md:p-12 text-center">
            <h2 className="font-serif text-2xl md:text-3xl font-bold mb-4">
              Ready to Generate Your Cover Letter?
            </h2>
            <p className="text-muted-foreground mb-6 max-w-xl mx-auto">
              Select a template, fill in your details, and let our AI craft a personalized 
              cover letter that perfectly matches your resume.
            </p>
            <Button className="btn-hero gap-2">
              Get Started
              <ChevronRight className="w-4 h-4" />
            </Button>
            
            {/* Privacy Badge */}
            <div className="flex items-center justify-center gap-2 mt-8 text-sm text-muted-foreground">
              <Shield className="w-4 h-4 text-fresher" />
              <span>Resume data is used only for template preview and generation.</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-border">
        <div className="container max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
            <p>© 2024 Cover Letter Generator. All rights reserved.</p>
            <div className="flex items-center gap-6">
              <a href="#" className="hover:text-foreground transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-foreground transition-colors">Terms of Service</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Templates;

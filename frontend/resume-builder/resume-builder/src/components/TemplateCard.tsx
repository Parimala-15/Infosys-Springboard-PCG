import { Eye, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ResumeTemplate, getCategoryBadgeClass } from '@/data/resumeTemplates';

interface TemplateCardProps {
  template: ResumeTemplate;
  onPreview: (templateId: string) => void;
}

const getThumbnailGradient = (thumbnail: string) => {
  switch (thumbnail) {
    case 'tech':
      return 'from-technical to-technical-dark';
    case 'fresher':
      return 'from-fresher to-fresher-dark';
    case 'executive':
      return 'from-executive to-executive-dark';
    case 'creative':
      return 'from-creative to-creative-dark';
    case 'minimal':
      return 'from-foreground/80 to-foreground';
    case 'student':
      return 'from-fresher-dark to-accent';
    default:
      return 'from-primary to-accent';
  }
};

export const TemplateCard = ({ template, onPreview }: TemplateCardProps) => {
  return (
    <div className="card-elevated group cursor-pointer overflow-hidden" onClick={() => onPreview(template.id)}>
      {/* Thumbnail Preview */}
      <div className={`relative h-48 bg-gradient-to-br ${getThumbnailGradient(template.thumbnail)} p-4`}>
        <div className="absolute inset-4 bg-card/95 rounded-lg shadow-lg transform group-hover:scale-[1.02] transition-transform duration-300">
          {/* Mini Resume Preview */}
          <div className="p-3 h-full flex flex-col">
            <div className="flex items-center gap-2 mb-2">
              <div 
                className="w-8 h-8 rounded-full" 
                style={{ background: `linear-gradient(135deg, ${template.accentColor}, ${template.accentColor}80)` }}
              />
              <div className="flex-1">
                <div className="h-2 bg-foreground/20 rounded w-3/4 mb-1" />
                <div className="h-1.5 bg-foreground/10 rounded w-1/2" />
              </div>
            </div>
            <div className="space-y-1.5 flex-1">
              <div className="h-1.5 bg-foreground/10 rounded w-full" />
              <div className="h-1.5 bg-foreground/10 rounded w-5/6" />
              <div className="h-1.5 bg-foreground/10 rounded w-4/6" />
              <div className="mt-2 h-1 rounded w-1/3" style={{ backgroundColor: template.accentColor }} />
              <div className="h-1.5 bg-foreground/10 rounded w-full" />
              <div className="h-1.5 bg-foreground/10 rounded w-3/4" />
            </div>
          </div>
        </div>
        
        {/* Hover Overlay */}
        <div className="absolute inset-0 bg-foreground/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
          <Button 
            variant="secondary" 
            className="gap-2 bg-card text-foreground hover:bg-card/90"
            onClick={(e) => {
              e.stopPropagation();
              onPreview(template.id);
            }}
          >
            <Eye className="w-4 h-4" />
            Preview Template
          </Button>
        </div>
      </div>
      
      {/* Card Content */}
      <div className="p-5">
        <div className="flex items-start justify-between gap-2 mb-3">
          <h3 className="font-serif text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
            {template.name}
          </h3>
          <FileText className="w-5 h-5 text-muted-foreground flex-shrink-0" />
        </div>
        
        <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
          {template.description}
        </p>
        
        {/* Category Tags */}
        <div className="flex flex-wrap gap-2">
          {template.categories.slice(0, 3).map((category) => (
            <span key={category} className={getCategoryBadgeClass(category)}>
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

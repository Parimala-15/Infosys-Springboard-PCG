import { useNavigate } from 'react-router-dom';
import { FileText, Sparkles, ChevronRight, Shield, Zap, Layout } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="section-gradient text-primary-foreground min-h-[80vh] flex items-center">
        <div className="container max-w-6xl mx-auto px-4 py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="animate-fade-in">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-sm font-medium mb-6">
                <Sparkles className="w-4 h-4" />
                AI-Powered Cover Letters
              </div>
              
              <h1 className="font-serif text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
                Create Perfect Cover Letters
                <span className="block text-accent">In Minutes</span>
              </h1>
              
              <p className="text-lg md:text-xl text-white/80 mb-8 max-w-lg">
                Transform your resume into compelling, personalized cover letters. 
                Choose from professional templates designed for every career stage.
              </p>
              
              <div className="flex flex-wrap gap-4">
                <Button 
                  className="btn-hero gap-2 text-base"
                  onClick={() => navigate('/templates')}
                >
                  Browse Templates
                  <ChevronRight className="w-5 h-5" />
                </Button>
                <Button 
                  variant="outline" 
                  className="gap-2 text-base bg-transparent border-white/30 text-white hover:bg-white/10"
                >
                  <FileText className="w-5 h-5" />
                  Upload Resume
                </Button>
              </div>
              
              {/* Privacy Badge */}
              <div className="flex items-center gap-2 mt-8 text-sm text-white/70">
                <Shield className="w-4 h-4 text-accent" />
                <span>Your data is secure and never shared</span>
              </div>
            </div>
            
            {/* Right Visual */}
            <div className="hidden lg:block relative animate-slide-up">
              <div className="relative">
                {/* Main Resume Card */}
                <div className="card-elevated p-6 transform rotate-2 relative z-10">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent" />
                    <div>
                      <div className="h-3 w-32 bg-foreground/20 rounded" />
                      <div className="h-2 w-24 bg-foreground/10 rounded mt-1" />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="h-2 bg-foreground/10 rounded w-full" />
                    <div className="h-2 bg-foreground/10 rounded w-5/6" />
                    <div className="h-2 bg-foreground/10 rounded w-4/6" />
                  </div>
                  <div className="mt-4 flex gap-2">
                    <span className="badge-technical">Technical</span>
                    <span className="badge-fresher">Fresher</span>
                  </div>
                </div>
                
                {/* Background Card */}
                <div className="absolute -bottom-4 -right-4 w-full h-full card-elevated opacity-60 -rotate-3" />
                <div className="absolute -bottom-8 -right-8 w-full h-full card-elevated opacity-30 -rotate-6" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-secondary/30">
        <div className="container max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
              Why Choose Our Templates?
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Smart, adaptive templates that understand your career stage
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Zap,
                title: 'Smart Sections',
                description: 'Templates automatically adjust sections based on whether you\'re a fresher or experienced professional.',
                color: 'text-technical',
              },
              {
                icon: Layout,
                title: 'ATS-Friendly',
                description: 'All templates are optimized for Applicant Tracking Systems to ensure your resume gets seen.',
                color: 'text-fresher',
              },
              {
                icon: Sparkles,
                title: 'AI Integration',
                description: 'Seamlessly connect your resume data to generate personalized, compelling cover letters.',
                color: 'text-executive',
              },
            ].map((feature, index) => (
              <div 
                key={index} 
                className="card-elevated p-6 text-center animate-slide-up"
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <div className={`w-14 h-14 rounded-xl mx-auto mb-4 flex items-center justify-center bg-secondary ${feature.color}`}>
                  <feature.icon className="w-7 h-7" />
                </div>
                <h3 className="font-serif text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container max-w-4xl mx-auto px-4 text-center">
          <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4">
            Ready to Stand Out?
          </h2>
          <p className="text-muted-foreground text-lg mb-8 max-w-xl mx-auto">
            Browse our collection of professional templates and start creating 
            your perfect cover letter today.
          </p>
          <Button 
            className="btn-hero gap-2 text-lg px-8 py-6"
            onClick={() => navigate('/templates')}
          >
            Explore Resume Templates
            <ChevronRight className="w-5 h-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Index;

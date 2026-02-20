import { Mail, Phone, MapPin, Linkedin, Briefcase, GraduationCap, Code, Award, Users, Target } from 'lucide-react';
import { ResumeTemplate, sampleResumeData } from '@/data/resumeTemplates';

interface ResumePreviewProps {
  template: ResumeTemplate;
  experienceType: 'experienced' | 'fresher';
}

export const ResumePreview = ({ template, experienceType }: ResumePreviewProps) => {
  const data = sampleResumeData[experienceType];
  const isFresher = experienceType === 'fresher';
  const isTechnical = template.categories.includes('technical');
  
  // Template logic: Adjust sections based on user type
  const showExperience = !isFresher && template.sections.showExperience;
  const showProjects = isTechnical || isFresher || template.sections.showProjects;
  const showActivities = isFresher || template.categories.includes('non-technical');
  const showObjective = isFresher || template.sections.showObjective;
  const showSkills = template.sections.showSkills;
  const showCertifications = template.sections.showCertifications;
  const showAchievements = !isFresher && template.sections.showAchievements;

  return (
    <div className="resume-preview max-w-[850px] mx-auto bg-card" style={{ minHeight: '1100px' }}>
      {/* Header */}
      <div 
        className="p-8 text-primary-foreground"
        style={{ background: `linear-gradient(135deg, ${template.accentColor}, ${template.accentColor}cc)` }}
      >
        <h1 className="font-serif text-3xl font-bold mb-1">{data.name}</h1>
        <p className="text-lg opacity-90 mb-4">{data.title}</p>
        
        <div className="flex flex-wrap gap-4 text-sm opacity-90">
          <div className="flex items-center gap-1.5">
            <Mail className="w-4 h-4" />
            {data.email}
          </div>
          <div className="flex items-center gap-1.5">
            <Phone className="w-4 h-4" />
            {data.phone}
          </div>
          <div className="flex items-center gap-1.5">
            <MapPin className="w-4 h-4" />
            {data.location}
          </div>
          <div className="flex items-center gap-1.5">
            <Linkedin className="w-4 h-4" />
            {data.linkedin}
          </div>
        </div>
      </div>

      <div className="p-8 space-y-6">
        {/* Objective/Summary - Show for freshers */}
        {showObjective && (
          <section>
            <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
              <Target className="w-5 h-5" style={{ color: template.accentColor }} />
              Career Objective
            </h2>
            <p className="text-muted-foreground leading-relaxed">{data.objective}</p>
          </section>
        )}

        {/* Education */}
        <section>
          <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
            <GraduationCap className="w-5 h-5" style={{ color: template.accentColor }} />
            Education
          </h2>
          <div className="space-y-4">
            {data.education.map((edu, idx) => (
              <div key={idx}>
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-foreground">{edu.degree}</h3>
                    <p className="text-muted-foreground">{edu.school}</p>
                  </div>
                  <div className="text-right text-sm">
                    <span className="text-muted-foreground">{edu.year}</span>
                    <p className="font-medium" style={{ color: template.accentColor }}>GPA: {edu.gpa}</p>
                  </div>
                </div>
                {'coursework' in edu && edu.coursework && (
                  <p className="text-sm text-muted-foreground mt-1">
                    <span className="font-medium">Relevant Coursework:</span> {edu.coursework.join(', ')}
                  </p>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Experience - Hidden for freshers */}
        {showExperience && data.experience.length > 0 && (
          <section>
            <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
              <Briefcase className="w-5 h-5" style={{ color: template.accentColor }} />
              Professional Experience
            </h2>
            <div className="space-y-5">
              {data.experience.map((exp, idx) => (
                <div key={idx}>
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-semibold text-foreground">{exp.title}</h3>
                      <p className="text-muted-foreground">{exp.company} • {exp.location}</p>
                    </div>
                    <span className="text-sm px-3 py-1 rounded-full bg-secondary text-secondary-foreground">
                      {exp.period}
                    </span>
                  </div>
                  <ul className="space-y-1.5 ml-4">
                    {exp.achievements.map((achievement, aidx) => (
                      <li key={aidx} className="text-sm text-muted-foreground flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style={{ backgroundColor: template.accentColor }} />
                        {achievement}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Skills - Highlighted for technical */}
        {showSkills && (
          <section>
            <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
              <Code className="w-5 h-5" style={{ color: template.accentColor }} />
              Technical Skills
            </h2>
            <div className="flex flex-wrap gap-2">
              {data.skills.map((skill, idx) => (
                <span 
                  key={idx} 
                  className="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
                  style={{ 
                    backgroundColor: `${template.accentColor}15`,
                    color: template.accentColor,
                    border: `1px solid ${template.accentColor}30`
                  }}
                >
                  {skill}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* Projects - Highlighted for technical and freshers */}
        {showProjects && data.projects.length > 0 && (
          <section>
            <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
              <Code className="w-5 h-5" style={{ color: template.accentColor }} />
              Key Projects
            </h2>
            <div className="grid gap-4">
              {data.projects.map((project, idx) => (
                <div key={idx} className="p-4 rounded-lg bg-secondary/50 border border-border/50">
                  <h3 className="font-semibold text-foreground mb-1">{project.name}</h3>
                  <p className="text-sm text-muted-foreground">{project.description}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Activities - Highlighted for non-technical and freshers */}
        {showActivities && 'activities' in data && data.activities && data.activities.length > 0 && (
          <section>
            <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
              <Users className="w-5 h-5" style={{ color: template.accentColor }} />
              Activities & Leadership
            </h2>
            <div className="space-y-4">
              {data.activities.map((activity, idx) => (
                <div key={idx}>
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-foreground">{activity.title}</h3>
                      <p className="text-muted-foreground text-sm">{activity.organization}</p>
                    </div>
                    <span className="text-sm text-muted-foreground">{activity.period}</span>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{activity.description}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Certifications */}
        {showCertifications && data.certifications.length > 0 && (
          <section>
            <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
              <Award className="w-5 h-5" style={{ color: template.accentColor }} />
              Certifications
            </h2>
            <div className="flex flex-wrap gap-2">
              {data.certifications.map((cert, idx) => (
                <span key={idx} className="px-3 py-1.5 rounded-full bg-secondary text-sm font-medium text-secondary-foreground">
                  {cert}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* Achievements */}
        {showAchievements && 'achievements' in data && data.achievements && data.achievements.length > 0 && (
          <section>
            <h2 className="flex items-center gap-2 font-serif text-lg font-semibold mb-3 pb-2 border-b-2" style={{ borderColor: template.accentColor }}>
              <Award className="w-5 h-5" style={{ color: template.accentColor }} />
              Achievements
            </h2>
            <ul className="space-y-2">
              {data.achievements.map((achievement, idx) => (
                <li key={idx} className="flex items-start gap-2 text-muted-foreground">
                  <span className="w-1.5 h-1.5 rounded-full mt-2 flex-shrink-0" style={{ backgroundColor: template.accentColor }} />
                  {achievement}
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </div>
  );
};

export type TemplateCategory = 'fresher' | 'experienced' | 'technical' | 'non-technical' | 'creative' | 'executive';

export interface ResumeTemplate {
  id: string;
  name: string;
  description: string;
  categories: TemplateCategory[];
  thumbnail: string;
  accentColor: string;
  sections: {
    showExperience: boolean;
    showProjects: boolean;
    showSkills: boolean;
    showActivities: boolean;
    showCertifications: boolean;
    showObjective: boolean;
    showAchievements: boolean;
  };
}

export const resumeTemplates: ResumeTemplate[] = [
  {
    id: 'modern-tech',
    name: 'Modern Tech Pro',
    description: 'Clean, ATS-friendly design perfect for software developers and engineers. Highlights technical skills and projects.',
    categories: ['technical', 'experienced'],
    thumbnail: 'tech',
    accentColor: 'hsl(199 89% 48%)',
    sections: {
      showExperience: true,
      showProjects: true,
      showSkills: true,
      showActivities: false,
      showCertifications: true,
      showObjective: false,
      showAchievements: true,
    },
  },
  {
    id: 'fresh-graduate',
    name: 'Fresh Start',
    description: 'Designed for new graduates. Emphasizes education, projects, and extracurricular activities over work experience.',
    categories: ['fresher', 'technical'],
    thumbnail: 'fresher',
    accentColor: 'hsl(172 66% 50%)',
    sections: {
      showExperience: false,
      showProjects: true,
      showSkills: true,
      showActivities: true,
      showCertifications: true,
      showObjective: true,
      showAchievements: false,
    },
  },
  {
    id: 'executive-classic',
    name: 'Executive Classic',
    description: 'Sophisticated design for senior professionals. Showcases leadership experience and strategic achievements.',
    categories: ['executive', 'experienced', 'non-technical'],
    thumbnail: 'executive',
    accentColor: 'hsl(25 95% 53%)',
    sections: {
      showExperience: true,
      showProjects: false,
      showSkills: true,
      showActivities: false,
      showCertifications: true,
      showObjective: false,
      showAchievements: true,
    },
  },
  {
    id: 'creative-portfolio',
    name: 'Creative Edge',
    description: 'Bold and artistic layout for designers, marketers, and creative professionals. Stands out from the crowd.',
    categories: ['creative', 'non-technical'],
    thumbnail: 'creative',
    accentColor: 'hsl(280 65% 60%)',
    sections: {
      showExperience: true,
      showProjects: true,
      showSkills: true,
      showActivities: true,
      showCertifications: false,
      showObjective: true,
      showAchievements: false,
    },
  },
  {
    id: 'minimal-clean',
    name: 'Minimal Pro',
    description: 'Ultra-clean minimalist design. Perfect for professionals who want their content to speak for itself.',
    categories: ['technical', 'experienced'],
    thumbnail: 'minimal',
    accentColor: 'hsl(222 47% 11%)',
    sections: {
      showExperience: true,
      showProjects: true,
      showSkills: true,
      showActivities: false,
      showCertifications: true,
      showObjective: false,
      showAchievements: true,
    },
  },
  {
    id: 'student-intern',
    name: 'Student Focus',
    description: 'Tailored for students seeking internships. Highlights coursework, projects, and extracurricular involvement.',
    categories: ['fresher', 'non-technical'],
    thumbnail: 'student',
    accentColor: 'hsl(160 84% 39%)',
    sections: {
      showExperience: false,
      showProjects: true,
      showSkills: true,
      showActivities: true,
      showCertifications: true,
      showObjective: true,
      showAchievements: false,
    },
  },
];

export const sampleResumeData = {
  experienced: {
    name: 'Sarah Mitchell',
    title: 'Senior Software Engineer',
    email: 'sarah.mitchell@email.com',
    phone: '+1 (555) 123-4567',
    location: 'San Francisco, CA',
    linkedin: 'linkedin.com/in/sarahmitchell',
    objective: 'Results-driven software engineer with 8+ years of experience building scalable web applications and leading high-performing teams.',
    experience: [
      {
        title: 'Senior Software Engineer',
        company: 'TechCorp Inc.',
        location: 'San Francisco, CA',
        period: 'Jan 2021 - Present',
        achievements: [
          'Led development of microservices architecture serving 2M+ daily users',
          'Reduced API response time by 40% through optimization strategies',
          'Mentored team of 5 junior developers, improving team velocity by 25%',
        ],
      },
      {
        title: 'Software Engineer',
        company: 'StartupXYZ',
        location: 'New York, NY',
        period: 'Mar 2018 - Dec 2020',
        achievements: [
          'Built real-time collaboration features using WebSocket technology',
          'Implemented CI/CD pipelines reducing deployment time by 60%',
          'Developed RESTful APIs handling 100K+ requests per minute',
        ],
      },
    ],
    education: [
      {
        degree: 'Master of Science in Computer Science',
        school: 'Stanford University',
        year: '2018',
        gpa: '3.9/4.0',
      },
      {
        degree: 'Bachelor of Science in Computer Engineering',
        school: 'UC Berkeley',
        year: '2016',
        gpa: '3.8/4.0',
      },
    ],
    skills: ['React', 'Node.js', 'TypeScript', 'Python', 'AWS', 'Docker', 'Kubernetes', 'PostgreSQL', 'MongoDB', 'GraphQL'],
    projects: [
      {
        name: 'Open Source CLI Tool',
        description: 'Created a CLI tool for automated code review with 500+ GitHub stars',
      },
      {
        name: 'ML Pipeline Framework',
        description: 'Built scalable ML pipeline framework used by 3 enterprise clients',
      },
    ],
    certifications: ['AWS Solutions Architect', 'Google Cloud Professional'],
    achievements: ['Patent holder for distributed caching algorithm', 'Speaker at ReactConf 2023'],
  },
  fresher: {
    name: 'Alex Kumar',
    title: 'Computer Science Graduate',
    email: 'alex.kumar@email.com',
    phone: '+1 (555) 987-6543',
    location: 'Boston, MA',
    linkedin: 'linkedin.com/in/alexkumar',
    objective: 'Motivated computer science graduate seeking opportunities to apply strong programming skills and academic knowledge in a dynamic tech environment.',
    experience: [],
    education: [
      {
        degree: 'Bachelor of Science in Computer Science',
        school: 'MIT',
        year: '2024',
        gpa: '3.85/4.0',
        coursework: ['Data Structures', 'Algorithms', 'Machine Learning', 'Distributed Systems', 'Database Design'],
      },
    ],
    skills: ['Java', 'Python', 'JavaScript', 'React', 'SQL', 'Git', 'Linux', 'Machine Learning'],
    projects: [
      {
        name: 'E-Commerce Platform',
        description: 'Full-stack web app with React frontend and Node.js backend. Implemented payment integration and real-time inventory management.',
      },
      {
        name: 'AI Chatbot',
        description: 'NLP-powered chatbot using Python and TensorFlow. Achieved 85% accuracy in intent classification.',
      },
      {
        name: 'Mobile Fitness App',
        description: 'React Native app with workout tracking, progress visualization, and social features. 1000+ downloads on Play Store.',
      },
    ],
    activities: [
      {
        title: 'Tech Lead',
        organization: 'Google Developer Student Club',
        period: '2022 - 2024',
        description: 'Organized 15+ technical workshops and hackathons for 500+ students',
      },
      {
        title: 'Open Source Contributor',
        organization: 'Various Projects',
        period: '2021 - Present',
        description: 'Contributed to React, Node.js, and TensorFlow repositories',
      },
    ],
    certifications: ['AWS Cloud Practitioner', 'Google Analytics Certification'],
    achievements: [],
  },
};

export const getCategoryBadgeClass = (category: TemplateCategory): string => {
  switch (category) {
    case 'fresher':
      return 'badge-fresher';
    case 'technical':
      return 'badge-technical';
    case 'creative':
      return 'badge-creative';
    case 'executive':
    case 'experienced':
      return 'badge-executive';
    case 'non-technical':
      return 'bg-muted text-muted-foreground px-3 py-1 rounded-full text-xs font-semibold';
    default:
      return 'bg-secondary text-secondary-foreground px-3 py-1 rounded-full text-xs font-semibold';
  }
};

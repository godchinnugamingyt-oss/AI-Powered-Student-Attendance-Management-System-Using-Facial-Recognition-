"""
Resume Analysis Module using Natural Language Processing (NLP)
This module demonstrates the AI-powered resume analysis capabilities
of the Campus Placement Platform using spaCy and custom NLP techniques.
"""

import spacy
import re
import json
from collections import defaultdict

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


class AdvancedResumeAnalyzer:
    """Advanced NLP-based Resume Analyzer using spaCy."""

    def __init__(self):
        self.nlp = nlp
        self.skill_keywords = {
            'Programming Languages': ['Python', 'Java', 'C++', 'JavaScript', 'TypeScript',
                                       'C#', 'Ruby', 'Go', 'Rust', 'Kotlin', 'Swift', 'PHP'],
            'Web Technologies': ['React', 'Angular', 'Vue.js', 'Node.js', 'Express.js',
                                 'Django', 'Flask', 'Spring Boot', 'HTML', 'CSS', 'Next.js'],
            'Data Science & AI': ['Machine Learning', 'Deep Learning', 'Data Science',
                                  'Artificial Intelligence', 'TensorFlow', 'PyTorch',
                                  'Scikit-learn', 'Pandas', 'NumPy', 'NLP', 'Computer Vision'],
            'Databases': ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle',
                          'SQLite', 'Cassandra', 'Elasticsearch'],
            'Cloud & DevOps': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes',
                               'DevOps', 'CI/CD', 'Jenkins', 'Terraform', 'Ansible'],
            'Soft Skills': ['Communication', 'Leadership', 'Team Management',
                           'Problem Solving', 'Critical Thinking', 'Agile', 'Scrum']
        }
        self.all_skills = [skill for skills_list in self.skill_keywords.values() for skill in skills_list]

    def preprocess_text(self, text):
        """Preprocess resume text for NLP analysis."""
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return tokens

    def extract_named_entities(self, text):
        """Extract named entities from resume text."""
        doc = self.nlp(text)
        entities = {
            'organizations': [],
            'locations': [],
            'dates': [],
            'misc': []
        }
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ == 'GPE' or ent.label_ == 'LOC':
                entities['locations'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
        return entities

    def classify_skills(self, skills):
        """Classify extracted skills into categories."""
        classification = defaultdict(list)
        for skill in skills:
            for category, category_skills in self.skill_keywords.items():
                if skill in category_skills:
                    classification[category].append(skill)
                    break
        return dict(classification)

    def analyze_resume(self, resume_text):
        """Perform comprehensive resume analysis."""
        tokens = self.preprocess_text(resume_text)
        entities = self.extract_named_entities(resume_text)

        # Extract skills
        found_skills = []
        for skill in self.all_skills:
            if skill.lower() in resume_text.lower():
                found_skills.append(skill)

        # Skill classification
        skill_categories = self.classify_skills(found_skills)

        # Compute proficiency score
        total_skills = len(found_skills)
        categories_covered = len(skill_categories)

        score = min(100, (total_skills * 5 + categories_covered * 8))

        return {
            'total_tokens': len(tokens),
            'unique_skills': total_skills,
            'skills': found_skills,
            'skill_categories': skill_categories,
            'entities': entities,
            'proficiency_score': score,
            'readability': len(resume_text.split())
        }


def demonstrate_nlp_analysis():
    """Demonstrate the NLP resume analysis pipeline."""
    analyzer = AdvancedResumeAnalyzer()

    # Sample resume texts
    sample_resumes = [
        """
        John Smith - Computer Science Engineering
        CGPA: 8.5
        
        Skills: Python, Java, Machine Learning, Deep Learning, TensorFlow, 
        Data Science, SQL, AWS, Docker, Communication, Leadership
        
        Projects: Developed a sentiment analysis model using Python and TensorFlow.
        Built a web application using React and Node.js.
        Experience: Intern at Google India - Data Science Team
        """,
        """
        Priya Sharma - Information Technology
        CGPA: 7.8
        
        Skills: JavaScript, React, Node.js, HTML, CSS, MongoDB, Express.js, 
        Git, Problem Solving, Team Management
        
        Projects: Created an e-commerce platform using MERN stack.
        Experience: Freelance Web Developer
        """,
        """
        Rahul Kumar - Electronics Engineering
        CGPA: 6.5
        
        Skills: Python, C++, Arduino, IoT, Data Science, Pandas, NumPy,
        Communication
        
        Projects: Developed IoT-based home automation system.
        Experience: Research Assistant at University Lab
        """
    ]

    print("=" * 60)
    print("NLP Resume Analysis Demonstration")
    print("=" * 60)

    results = []
    for i, resume in enumerate(sample_resumes, 1):
        print(f"\n{'='*40}")
        print(f"Resume {i} Analysis:")
        print(f"{'='*40}")

        result = analyzer.analyze_resume(resume)
        results.append(result)

        print(f"  Total Tokens: {result['total_tokens']}")
        print(f"  Unique Skills Found: {result['unique_skills']}")
        print(f"  Proficiency Score: {result['proficiency_score']}/100")
        print(f"  Skills: {', '.join(result['skills'])}")
        print(f"  Skill Categories: {json.dumps(result['skill_categories'], indent=4)}")

    return results


if __name__ == '__main__':
    demonstrate_nlp_analysis()

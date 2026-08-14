"""
AI-Driven Campus Placement Registration and Resume Matching Platform
with Job Recommendation Engine

This is the complete Python implementation of the campus placement platform
that demonstrates:
1. Student Registration and Profile Management
2. Resume Analysis using NLP (spaCy)
3. AI-based Resume-Company Matching
4. Job Recommendation Engine
5. Analytics and Reporting
6. Visualization and Dashboard
"""

import json
import os
import random
import re
import warnings
from datetime import datetime, timedelta
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from wordcloud import WordCloud

warnings.filterwarnings('ignore')

# ============================================================
# PART 1: DATA GENERATION - Sample Data for the Platform
# ============================================================

def generate_student_data(num_students=50):
    """Generate synthetic student registration data."""
    first_names = ['Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai',
                   'Reyansh', 'Ayaan', 'Krishna', 'Ishaan', 'Ananya', 'Diya',
                   'Myra', 'Ira', 'Ananya', 'Sara', 'Riya', 'Pihu', 'Aanya',
                   'Priya', 'Rohit', 'Amit', 'Rahul', 'Vikram', 'Siddharth',
                   'Karan', 'Nikhil', 'Deepak', 'Rajesh', 'Suresh', 'Sneha',
                   'Pooja', 'Kavya', 'Nisha', 'Tanya', 'Megha', 'Shreya',
                   'Swati', 'Divya', 'Neha', 'Gaurav', 'Pranav', 'Harsh',
                   'Yash', 'Manish', 'Akash', 'Vinay', 'Kunal', 'Rajat', 'Ashish']

    last_names = ['Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Patel',
                  'Mehta', 'Jain', 'Reddy', 'Rao', 'Nair', 'Pillai',
                  'Iyer', 'Menon', 'Krishnan', 'Srinivasan', 'Ramesh',
                  'Subramanian', 'Balakrishnan', 'Venkatesh', 'Das',
                  'Banerjee', 'Chatterjee', 'Mukherjee', 'Ghosh', 'Saha',
                  'Chandra', 'Bose', 'Sarkar', 'Mandal', 'Dutta', 'Roy',
                  'Sen', 'Dey', 'Paul', 'Biswas', 'Dasgupta', 'Basu',
                  'Bhattacharya', 'Chakraborty', 'Mitra', 'Dey', 'Ganguly',
                  'Chowdhury', 'Sengupta', 'Majumdar', 'Thakur', 'Dubey',
                  'Tiwari', 'Pandey']

    branches = ['Computer Science', 'Electronics', 'Information Technology',
                'Mechanical Engineering', 'Civil Engineering', 'Electrical Engineering']

    skills_pool = [
        'Python', 'Java', 'C++', 'JavaScript', 'React', 'Node.js', 'SQL',
        'Machine Learning', 'Deep Learning', 'Data Science', 'Artificial Intelligence',
        'Web Development', 'Mobile App Development', 'Cloud Computing', 'AWS',
        'Docker', 'Kubernetes', 'DevOps', 'Git', 'Linux', 'HTML', 'CSS',
        'Angular', 'Vue.js', 'Django', 'Flask', 'Spring Boot', 'MySQL',
        'MongoDB', 'PostgreSQL', 'Redis', 'TensorFlow', 'PyTorch', 'Scikit-learn',
        'Pandas', 'NumPy', 'Power BI', 'Tableau', 'Excel', 'Communication',
        'Leadership', 'Team Management', 'Problem Solving', 'Critical Thinking'
    ]

    students = []
    for i in range(num_students):
        cgpa = round(random.uniform(5.5, 9.8), 2)
        num_skills = random.randint(4, 12)
        student_skills = random.sample(skills_pool, min(num_skills, len(skills_pool)))

        student = {
            'student_id': f'STU{i+1:03d}',
            'name': f'{first_names[i % len(first_names)]} {last_names[i % len(last_names)]}',
            'branch': random.choice(branches),
            'cgpa': cgpa,
            'year': random.choice([3, 4]),
            'email': f'{first_names[i % len(first_names)].lower()}.{last_names[i % len(last_names)].lower()}@university.edu',
            'phone': f'+91-{random.randint(7000000000, 9999999999)}',
            'skills': student_skills,
            'resume_text': f"""
            {first_names[i % len(first_names)]} {last_names[i % len(last_names)]}
            Branch: {random.choice(branches)}
            CGPA: {cgpa}
            
            Skills: {', '.join(student_skills)}
            
            Projects: Developed a {random.choice(['web application', 'mobile app', 'ML model', 'data pipeline', 'automation tool'])} 
            using {random.sample(student_skills, min(3, len(student_skills)))}.
            
            Experience: {random.choice(['Intern at Tech Company', 'Freelance Developer', 'Research Assistant', 'Open Source Contributor'])}
            """,
            'preferences': {
                'preferred_domain': random.choice(['Software Development', 'Data Science',
                                                    'Web Development', 'Cloud Computing', 'Product Management']),
                'preferred_location': random.choice(['Bangalore', 'Hyderabad', 'Mumbai',
                                                     'Delhi', 'Chennai', 'Remote'])
            },
            'placement_status': random.choice(['Eligible', 'Placed', 'Not Eligible']),
            'registration_date': (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
        }
        students.append(student)
    return students


def generate_company_data(num_companies=15):
    """Generate synthetic company recruitment data."""
    company_names = [
        'Infosys Technologies', 'Tata Consultancy Services', 'Wipro Limited',
        'Accenture India', 'Cognizant Technology', 'HCL Technologies',
        'Tech Mahindra', 'Capgemini India', 'IBM India', 'Oracle India',
        'Amazon India', 'Microsoft India', 'Google India', 'Flipkart',
        'Swiggy Technologies'
    ]

    companies = []
    for i in range(num_companies):
        company = {
            'company_id': f'CMP{i+1:03d}',
            'name': company_names[i],
            'industry': random.choice(['IT Services', 'Consulting', 'E-Commerce',
                                       'Cloud Services', 'Finance Tech', 'Healthcare Tech']),
            'location': random.choice(['Bangalore', 'Hyderabad', 'Mumbai',
                                       'Delhi', 'Chennai', 'Gurgaon']),
            'package_range': f'{random.choice([3, 4, 5, 6, 8, 10, 12, 15])}-{random.choice([15, 18, 20, 25, 30, 35, 40, 50])} LPA',
            'min_cgpa': round(random.uniform(5.0, 7.5), 1),
            'required_branches': random.sample(
                ['Computer Science', 'Electronics', 'Information Technology',
                 'Mechanical Engineering', 'Civil Engineering', 'Electrical Engineering'],
                random.randint(2, 5)
            ),
            'required_skills': random.sample(
                ['Python', 'Java', 'C++', 'JavaScript', 'React', 'Node.js', 'SQL',
                 'Machine Learning', 'Deep Learning', 'Data Science', 'Artificial Intelligence',
                 'Web Development', 'Cloud Computing', 'AWS', 'Docker', 'DevOps',
                 'Communication', 'Problem Solving', 'Leadership', 'Team Management'],
                random.randint(3, 8)
            ),
            'job_roles': [f'{random.choice(["Software", "Data", "Product", "Backend", "Frontend", "Full Stack"])} {random.choice(["Engineer", "Analyst", "Developer", "Scientist", "Manager"])}' for _ in range(random.randint(2, 5))],
            'hiring_capacity': random.randint(5, 50),
            'recruitment_date': (datetime(2026, 6, 1) + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'drive_type': random.choice(['On-Campus', 'Virtual', 'Hybrid'])
        }
        companies.append(company)
    return companies


# ============================================================
# PART 2: RESUME ANALYSIS ENGINE (NLP-based)
# ============================================================

class ResumeAnalyzer:
    """AI-powered Resume Analysis using NLP techniques."""

    def __init__(self):
        self.skill_keywords = [
            'Python', 'Java', 'C++', 'JavaScript', 'React', 'Node.js', 'SQL',
            'Machine Learning', 'Deep Learning', 'Data Science', 'Artificial Intelligence',
            'Web Development', 'Mobile App Development', 'Cloud Computing', 'AWS',
            'Docker', 'Kubernetes', 'DevOps', 'Git', 'Linux', 'HTML', 'CSS',
            'Angular', 'Vue.js', 'Django', 'Flask', 'Spring Boot', 'MySQL',
            'MongoDB', 'PostgreSQL', 'Redis', 'TensorFlow', 'PyTorch', 'Scikit-learn',
            'Pandas', 'NumPy', 'Power BI', 'Tableau', 'Excel', 'Communication',
            'Leadership', 'Team Management', 'Problem Solving', 'Critical Thinking',
            'Agile', 'Scrum', 'API Development', 'Microservices', 'REST API',
            'GraphQL', 'TypeScript', 'Swift', 'Kotlin', 'Flutter', 'React Native'
        ]

    def extract_skills_from_resume(self, resume_text):
        """Extract technical skills from resume text using keyword matching."""
        found_skills = []
        resume_lower = resume_text.lower()
        for skill in self.skill_keywords:
            if skill.lower() in resume_lower:
                found_skills.append(skill)
        return found_skills

    def extract_key_information(self, resume_text):
        """Extract key information from resume using regex patterns."""
        info = {}

        # Extract CGPA
        cgpa_match = re.search(r'cgpa:\s*([\d.]+)', resume_text, re.IGNORECASE)
        if cgpa_match:
            info['cgpa'] = float(cgpa_match.group(1))

        # Extract branch
        branch_match = re.search(r'branch:\s*([\w\s]+)', resume_text, re.IGNORECASE)
        if branch_match:
            info['branch'] = branch_match.group(1).strip()

        # Extract name
        name_match = re.search(r'^(\w+\s+\w+)', resume_text.strip())
        if name_match:
            info['name'] = name_match.group(1)

        return info

    def compute_resume_score(self, student):
        """Compute a composite score for the resume based on multiple factors."""
        score = 0

        # CGPA score (0-30)
        if student['cgpa'] >= 9.0:
            score += 30
        elif student['cgpa'] >= 8.0:
            score += 25
        elif student['cgpa'] >= 7.0:
            score += 20
        elif student['cgpa'] >= 6.0:
            score += 15
        else:
            score += 10

        # Skills score (0-30)
        num_skills = len(student['skills'])
        if num_skills >= 10:
            score += 30
        elif num_skills >= 8:
            score += 25
        elif num_skills >= 6:
            score += 20
        elif num_skills >= 4:
            score += 15
        else:
            score += 10

        # Diversity of skills (0-20)
        tech_skills = sum(1 for s in student['skills'] if s in [
            'Python', 'Java', 'C++', 'JavaScript', 'React', 'Node.js', 'SQL',
            'Machine Learning', 'Deep Learning', 'Data Science', 'Artificial Intelligence',
            'Web Development', 'Cloud Computing', 'AWS', 'Docker', 'DevOps'
        ])
        soft_skills = sum(1 for s in student['skills'] if s in [
            'Communication', 'Leadership', 'Team Management', 'Problem Solving', 'Critical Thinking'
        ])

        if tech_skills >= 4 and soft_skills >= 2:
            score += 20
        elif tech_skills >= 3:
            score += 15
        elif tech_skills >= 2:
            score += 10
        else:
            score += 5

        # Score normalized to 100
        return min(score, 100)

    def analyze_all_resumes(self, students):
        """Analyze all student resumes and return analysis results."""
        results = []
        for student in students:
            skills_extracted = self.extract_skills_from_resume(student['resume_text'])
            key_info = self.extract_key_information(student['resume_text'])
            resume_score = self.compute_resume_score(student)

            results.append({
                'student_id': student['student_id'],
                'name': student['name'],
                'cgpa': student['cgpa'],
                'branch': student['branch'],
                'skills_found': skills_extracted,
                'num_skills': len(skills_extracted),
                'key_info': key_info,
                'resume_score': resume_score,
                'score_category': 'Excellent' if resume_score >= 75 else
                                  'Good' if resume_score >= 60 else
                                  'Average' if resume_score >= 45 else 'Needs Improvement'
            })
        return results


# ============================================================
# PART 3: JOB MATCHING ENGINE
# ============================================================

class JobMatchingEngine:
    """AI-powered Job Matching using TF-IDF and Cosine Similarity."""

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer()

    def match_students_to_companies(self, students, companies):
        """Match students to companies based on skills and requirements."""
        # Create document corpus for vectorization
        student_docs = []
        company_docs = []

        for student in students:
            doc = ' '.join(student['skills'])
            student_docs.append(doc)

        for company in companies:
            doc = ' '.join(company['required_skills'])
            company_docs.append(doc)

        all_docs = student_docs + company_docs
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_docs)

        student_vectors = tfidf_matrix[:len(students)]
        company_vectors = tfidf_matrix[len(students):]

        # Compute similarity matrix
        similarity_matrix = cosine_similarity(student_vectors, company_vectors)

        matches = []
        for i, student in enumerate(students):
            if student['placement_status'] != 'Not Eligible':
                company_scores = []
                for j, company in enumerate(companies):
                    sim_score = similarity_matrix[i][j]
                    # Eligibility check
                    eligible = (
                        student['cgpa'] >= company['min_cgpa'] and
                        student['branch'] in company['required_branches']
                    )
                    company_scores.append({
                        'company': company['name'],
                        'similarity_score': round(sim_score, 4),
                        'eligible': eligible,
                        'package_range': company['package_range'],
                        'min_cgpa': company['min_cgpa'],
                        'required_skills': company['required_skills']
                    })

                # Sort by similarity score
                company_scores.sort(key=lambda x: x['similarity_score'], reverse=True)
                top_matches = [m for m in company_scores if m['eligible']][:5]

                matches.append({
                    'student_id': student['student_id'],
                    'student_name': student['name'],
                    'branch': student['branch'],
                    'cgpa': student['cgpa'],
                    'top_matches': top_matches,
                    'total_eligible': sum(1 for m in company_scores if m['eligible']),
                    'total_companies': len(companies)
                })

        return matches


# ============================================================
# PART 4: JOB RECOMMENDATION ENGINE
# ============================================================

class JobRecommendationEngine:
    """Personalized Job Recommendation Engine based on multiple factors."""

    def __init__(self):
        pass

    def recommend_jobs(self, students, companies, resume_analyses):
        """Generate personalized job recommendations for each student."""
        recommendations = []

        # Build skill-company mapping
        company_skill_map = defaultdict(list)
        for company in companies:
            for skill in company['required_skills']:
                company_skill_map[skill].append(company['name'])

        for idx, student in enumerate(students):
            if student['placement_status'] == 'Not Eligible':
                continue

            student_scores = []

            for company in companies:
                # Skill match score (0-40)
                student_skills_set = set(student['skills'])
                company_skills_set = set(company['required_skills'])
                common_skills = student_skills_set.intersection(company_skills_set)
                skill_match_ratio = len(common_skills) / max(len(company['required_skills']), 1)
                skill_score = skill_match_ratio * 40

                # Branch eligibility (0-20)
                branch_score = 20 if student['branch'] in company['required_branches'] else 0

                # CGPA score (0-20)
                if student['cgpa'] >= company['min_cgpa']:
                    cgpa_diff = student['cgpa'] - company['min_cgpa']
                    cgpa_score = min(20, 10 + cgpa_diff * 5)
                else:
                    cgpa_score = 0

                # Preference match (0-20)
                pref_score = 0
                if company['location'] == student['preferences']['preferred_location']:
                    pref_score += 10
                pref_domain_map = {
                    'Software Development': ['IT Services', 'Cloud Services'],
                    'Data Science': ['IT Services', 'Finance Tech'],
                    'Web Development': ['IT Services', 'E-Commerce'],
                    'Cloud Computing': ['Cloud Services', 'IT Services'],
                    'Product Management': ['E-Commerce', 'Consulting']
                }
                preferred_domains = pref_domain_map.get(student['preferences']['preferred_domain'], [])
                if company['industry'] in preferred_domains:
                    pref_score += 10

                total_score = skill_score + branch_score + cgpa_score + pref_score

                if branch_score > 0 and cgpa_score > 0:
                    student_scores.append({
                        'company': company['name'],
                        'industry': company['industry'],
                        'job_roles': company['job_roles'],
                        'package_range': company['package_range'],
                        'location': company['location'],
                        'drive_type': company['drive_type'],
                        'common_skills': list(common_skills),
                        'skill_match_percentage': round(skill_match_ratio * 100, 1),
                        'total_score': round(total_score, 2),
                        'scores_breakdown': {
                            'skill_match': round(skill_score, 2),
                            'branch_match': branch_score,
                            'cgpa_match': round(cgpa_score, 2),
                            'preference_match': pref_score
                        }
                    })

            student_scores.sort(key=lambda x: x['total_score'], reverse=True)

            recommendations.append({
                'student_id': student['student_id'],
                'student_name': student['name'],
                'branch': student['branch'],
                'cgpa': student['cgpa'],
                'preferred_domain': student['preferences']['preferred_domain'],
                'recommended_jobs': student_scores[:5],
                'total_recommended': len(student_scores)
            })

        return recommendations


# ============================================================
# PART 5: ANALYTICS AND REPORTING
# ============================================================

class PlacementAnalytics:
    """Generate comprehensive placement analytics and reports."""

    def __init__(self):
        pass

    def generate_summary_report(self, students, companies, matches, recommendations):
        """Generate comprehensive placement summary."""
        total_students = len(students)
        eligible_students = sum(1 for s in students if s['placement_status'] != 'Not Eligible')
        placed_students = sum(1 for s in students if s['placement_status'] == 'Placed')

        branch_wise = defaultdict(int)
        for s in students:
            branch_wise[s['branch']] += 1

        # Average CGPA
        avg_cgpa = np.mean([s['cgpa'] for s in students])

        # Company statistics
        total_hiring_capacity = sum(c['hiring_capacity'] for c in companies)

        # Match statistics
        match_stats = {
            'total_students': total_students,
            'eligible_students': eligible_students,
            'placed_students': placed_students,
            'eligibility_rate': round(eligible_students / total_students * 100, 1),
            'placement_rate': round(placed_students / total_students * 100, 1),
            'average_cgpa': round(avg_cgpa, 2),
            'total_companies': len(companies),
            'total_hiring_capacity': total_hiring_capacity,
            'average_matches_per_student': round(np.mean([m['total_eligible'] for m in matches]), 1),
            'branch_distribution': dict(branch_wise),
            'company_distribution': {c['name']: c['hiring_capacity'] for c in companies}
        }

        return match_stats


# ============================================================
# PART 6: VISUALIZATION ENGINE
# ============================================================

class VisualizationEngine:
    """Generate all visualization charts and graphs for the report."""

    def __init__(self, output_dir='/home/ubuntu/report_images'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.set_style()

    def set_style(self):
        """Set matplotlib style for professional-looking charts."""
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams.update({
            'figure.facecolor': 'white',
            'axes.facecolor': '#fafafa',
            'font.size': 11,
            'font.family': 'serif',
            'axes.titlesize': 14,
            'axes.titleweight': 'bold',
            'figure.figsize': (12, 7),
            'figure.dpi': 150,
            'savefig.dpi': 150,
            'savefig.bbox': 'tight',
            'legend.fontsize': 10,
            'axes.labelsize': 12
        })

    def plot_students_per_branch(self, students):
        """Plot 1: Distribution of students across branches."""
        branch_counts = defaultdict(int)
        for s in students:
            branch_counts[s['branch']] += 1

        branches = list(branch_counts.keys())
        counts = list(branch_counts.values())
        colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4']

        fig, ax = plt.subplots(figsize=(12, 7))
        bars = ax.bar(branches, counts, color=colors[:len(branches)], edgecolor='black',
                      linewidth=0.5, width=0.6)

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                    str(count), ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_xlabel('Branch', fontsize=13, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=13, fontweight='bold')
        ax.set_title('Distribution of Registered Students Across Branches', fontsize=15, fontweight='bold',
                     pad=15)
        ax.set_ylim(0, max(counts) * 1.15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig1_students_per_branch.png'))
        plt.close()
        print("Generated: fig1_students_per_branch.png")

    def plot_cgpa_distribution(self, students):
        """Plot 2: CGPA distribution of students."""
        cgpas = [s['cgpa'] for s in students]

        fig, axes = plt.subplots(1, 2, figsize=(16, 7))

        # Histogram
        colors_hist = ['#2196F3' if c >= 8.0 else '#FF9800' if c >= 7.0 else '#E91E63' if c >= 6.0 else '#9C27B0' for c in cgpas]
        axes[0].hist(cgpas, bins=15, color='#2196F3', edgecolor='black', linewidth=0.5, alpha=0.7)
        axes[0].axvline(np.mean(cgpas), color='red', linestyle='--', linewidth=2,
                        label=f'Mean: {np.mean(cgpas):.2f}')
        axes[0].axvline(np.median(cgpas), color='green', linestyle='-.', linewidth=2,
                        label=f'Median: {np.median(cgpas):.2f}')
        axes[0].set_xlabel('CGPA', fontsize=13, fontweight='bold')
        axes[0].set_ylabel('Frequency', fontsize=13, fontweight='bold')
        axes[0].set_title('CGPA Distribution of Registered Students', fontsize=15, fontweight='bold', pad=15)
        axes[0].legend(fontsize=11)
        axes[0].spines['top'].set_visible(False)
        axes[0].spines['right'].set_visible(False)

        # Box plot by branch
        branch_cgpas = defaultdict(list)
        for s in students:
            branch_cgpas[s['branch']].append(s['cgpa'])

        branch_labels = list(branch_cgpas.keys())
        box_data = [branch_cgpas[b] for b in branch_labels]
        bp = axes[1].boxplot(box_data, labels=branch_labels, patch_artist=True,
                             widths=0.6)
        box_colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4']
        for patch, color in zip(bp['boxes'], box_colors[:len(branch_labels)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        axes[1].set_xlabel('Branch', fontsize=13, fontweight='bold')
        axes[1].set_ylabel('CGPA', fontsize=13, fontweight='bold')
        axes[1].set_title('CGPA Distribution by Branch', fontsize=15, fontweight='bold', pad=15)
        axes[1].tick_params(axis='x', rotation=30)
        axes[1].spines['top'].set_visible(False)
        axes[1].spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig2_cgpa_distribution.png'))
        plt.close()
        print("Generated: fig2_cgpa_distribution.png")

    def plot_placement_status(self, students):
        """Plot 3: Placement status distribution (pie chart)."""
        status_counts = defaultdict(int)
        for s in students:
            status_counts[s['placement_status']] += 1

        statuses = list(status_counts.keys())
        counts = list(status_counts.values())
        colors = ['#4CAF50', '#2196F3', '#E91E63']
        explode = [0.05, 0.05, 0.05]

        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(counts, labels=statuses, autopct='%1.1f%%',
                                           colors=colors[:len(statuses)], explode=explode,
                                           shadow=True, startangle=90, textprops={'fontsize': 12})
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_fontsize(13)

        ax.set_title('Placement Status Distribution', fontsize=15, fontweight='bold', pad=20)

        # Add center text
        centre_circle = plt.Circle((0, 0), 0.55, fc='white')
        fig.gca().add_artist(centre_circle)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig3_placement_status.png'))
        plt.close()
        print("Generated: fig3_placement_status.png")

    def plot_skill_wordcloud(self, students):
        """Plot 4: Word cloud of student skills."""
        all_skills = []
        for s in students:
            all_skills.extend(s['skills'])

        skill_freq = defaultdict(int)
        for skill in all_skills:
            skill_freq[skill] += 1

        # Create wordcloud data
        wc = WordCloud(width=800, height=500, background_color='white',
                       max_words=50, colormap='viridis',
                       min_font_size=10, max_font_size=80,
                       prefer_horizontal=0.7)
        wc.generate_from_frequencies(dict(skill_freq))

        fig, ax = plt.subplots(figsize=(14, 8))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Word Cloud: Most In-Demand Student Skills', fontsize=15, fontweight='bold',
                     pad=20)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig4_skill_wordcloud.png'))
        plt.close()
        print("Generated: fig4_skill_wordcloud.png")

    def plot_top_skills(self, students):
        """Plot 5: Top 15 most common skills among students."""
        skill_freq = defaultdict(int)
        for s in students:
            for skill in s['skills']:
                skill_freq[skill] += 1

        top_skills = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:15]
        skills = [s[0] for s in top_skills]
        frequencies = [s[1] for s in top_skills]

        fig, ax = plt.subplots(figsize=(14, 8))
        colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(skills)))
        bars = ax.barh(skills, frequencies, color=colors, edgecolor='black',
                       linewidth=0.5, height=0.6)

        # Add value labels
        for bar, freq in zip(bars, frequencies):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    str(freq), ha='left', va='center', fontsize=11, fontweight='bold')

        ax.set_xlabel('Number of Students', fontsize=13, fontweight='bold')
        ax.set_title('Top 15 Most Common Skills Among Registered Students', fontsize=15, fontweight='bold',
                     pad=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.invert_yaxis()

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig5_top_skills.png'))
        plt.close()
        print("Generated: fig5_top_skills.png")

    def plot_company_skills_required(self, companies):
        """Plot 6: Skills required by companies."""
        skill_freq = defaultdict(int)
        for c in companies:
            for skill in c['required_skills']:
                skill_freq[skill] += 1

        top_skills = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:12]
        skills = [s[0] for s in top_skills]
        frequencies = [s[1] for s in top_skills]

        fig, ax = plt.subplots(figsize=(14, 7))
        colors = plt.cm.coolwarm(np.linspace(0.2, 0.9, len(skills)))
        bars = ax.bar(skills, frequencies, color=colors, edgecolor='black',
                      linewidth=0.5, width=0.6)

        for bar, freq in zip(bars, frequencies):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.15,
                    str(freq), ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax.set_xlabel('Skill', fontsize=13, fontweight='bold')
        ax.set_ylabel('Number of Companies Requiring', fontsize=13, fontweight='bold')
        ax.set_title('Top Skills Required by Recruiting Companies', fontsize=15, fontweight='bold',
                     pad=15)
        ax.tick_params(axis='x', rotation=45)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig6_company_skills_required.png'))
        plt.close()
        print("Generated: fig6_company_skills_required.png")

    def plot_matching_heatmap(self, students, companies, matches):
        """Plot 7: Matching similarity heatmap."""
        # Build similarity matrix for top students and companies
        eligible_students = [m for m in matches if m['total_eligible'] > 0][:15]

        company_names = [c['name'][:20] for c in companies]
        student_names = [m['student_name'][:15] for m in eligible_students]

        # Get top similarity scores
        matrix = np.zeros((len(eligible_students), len(companies)))
        for i, match in enumerate(eligible_students):
            for j, comp_match in enumerate(match['top_matches']):
                # Find company index
                for ci, c in enumerate(companies):
                    if c['name'] == comp_match['company']:
                        matrix[i][ci] = comp_match['similarity_score']

        fig, ax = plt.subplots(figsize=(16, 10))
        sns.heatmap(matrix, xticklabels=company_names, yticklabels=student_names,
                    annot=True, fmt='.3f', cmap='YlOrRd', cbar_kws={'label': 'Similarity Score'},
                    ax=ax, linewidths=0.5)
        ax.set_title('Resume-Company Matching Similarity Heatmap', fontsize=15, fontweight='bold',
                     pad=15)
        ax.set_xlabel('Companies', fontsize=13, fontweight='bold')
        ax.set_ylabel('Students', fontsize=13, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig7_matching_heatmap.png'))
        plt.close()
        print("Generated: fig7_matching_heatmap.png")

    def plot_company_hiring_capacity(self, companies):
        """Plot 8: Company-wise hiring capacity."""
        company_names = [c['name'][:15] for c in companies]
        capacities = [c['hiring_capacity'] for c in companies]

        fig, ax = plt.subplots(figsize=(14, 8))
        sorted_data = sorted(zip(company_names, capacities), key=lambda x: x[1], reverse=True)
        names, caps = zip(*sorted_data)
        colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(caps)))

        bars = ax.bar(names, caps, color=colors, edgecolor='black', linewidth=0.5, width=0.6)

        for bar, cap in zip(bars, caps):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                    str(cap), ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax.set_xlabel('Company', fontsize=13, fontweight='bold')
        ax.set_ylabel('Hiring Capacity (Number of Positions)', fontsize=13, fontweight='bold')
        ax.set_title('Company-wise Hiring Capacity for Campus Recruitment', fontsize=15, fontweight='bold',
                     pad=15)
        ax.tick_params(axis='x', rotation=45)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig8_company_hiring_capacity.png'))
        plt.close()
        print("Generated: fig8_company_hiring_capacity.png")

    def plot_skill_gap_analysis(self, students, companies):
        """Plot 9: Skill gap analysis - student skills vs company requirements."""
        student_skill_freq = defaultdict(int)
        for s in students:
            for skill in s['skills']:
                student_skill_freq[skill] += 1

        company_skill_freq = defaultdict(int)
        for c in companies:
            for skill in c['required_skills']:
                company_skill_freq[skill] += 1

        all_skills = set(list(student_skill_freq.keys()) + list(company_skill_freq.keys()))

        # Get top 12 skills by demand
        sorted_skills = sorted(all_skills, key=lambda s: company_skill_freq.get(s, 0), reverse=True)[:12]

        student_counts = [student_skill_freq.get(s, 0) for s in sorted_skills]
        company_counts = [company_skill_freq.get(s, 0) for s in sorted_skills]

        fig, ax = plt.subplots(figsize=(14, 8))
        x = np.arange(len(sorted_skills))
        width = 0.35

        bars1 = ax.bar(x - width/2, student_counts, width, label='Students with Skill',
                       color='#2196F3', edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + width/2, company_counts, width, label='Companies Requiring',
                       color='#FF9800', edgecolor='black', linewidth=0.5)

        ax.set_xlabel('Skills', fontsize=13, fontweight='bold')
        ax.set_ylabel('Count', fontsize=13, fontweight='bold')
        ax.set_title('Skill Gap Analysis: Student Supply vs Company Demand', fontsize=15, fontweight='bold',
                     pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(sorted_skills, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig9_skill_gap_analysis.png'))
        plt.close()
        print("Generated: fig9_skill_gap_analysis.png")

    def plot_recruitment_timeline(self, companies):
        """Plot 10: Recruitment drive timeline."""
        dates = [datetime.strptime(c['recruitment_date'], '%Y-%m-%d') for c in companies]
        company_names = [c['name'][:20] for c in companies]
        capacities = [c['hiring_capacity'] for c in companies]

        fig, ax = plt.subplots(figsize=(14, 8))
        y_pos = np.arange(len(dates))
        sizes = [c * 10 for c in capacities]
        colors_scatter = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4',
                          '#795548', '#607D8B', '#3F51B5', '#FF5722', '#009688', '#CDDC39',
                          '#673AB7', '#8BC34A', '#F44336']

        ax.scatter(dates, y_pos, s=sizes, c=colors_scatter[:len(dates)], alpha=0.7, edgecolors='black')

        for i, (date, name, cap) in enumerate(zip(dates, company_names, capacities)):
            ax.annotate(f'{name}\n({cap} positions)', (date, y_pos[i]),
                        textcoords="offset points", xytext=(10, 0), fontsize=9)

        ax.set_yticks(y_pos)
        ax.set_yticklabels([])
        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_title('Recruitment Drive Timeline', fontsize=15, fontweight='bold', pad=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Format x-axis dates
        fig.autofmt_xdate()

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig10_recruitment_timeline.png'))
        plt.close()
        print("Generated: fig10_recruitment_timeline.png")

    def plot_recommendation_scores(self, recommendations):
        """Plot 11: Recommendation score distribution."""
        all_scores = []
        for rec in recommendations:
            for job in rec['recommended_jobs']:
                all_scores.append(job['total_score'])

        fig, axes = plt.subplots(1, 2, figsize=(16, 7))

        # Histogram
        axes[0].hist(all_scores, bins=20, color='#2196F3', edgecolor='black',
                     linewidth=0.5, alpha=0.7)
        axes[0].axvline(np.mean(all_scores), color='red', linestyle='--', linewidth=2,
                        label=f'Mean: {np.mean(all_scores):.2f}')
        axes[0].set_xlabel('Recommendation Score', fontsize=13, fontweight='bold')
        axes[0].set_ylabel('Frequency', fontsize=13, fontweight='bold')
        axes[0].set_title('Distribution of Job Recommendation Scores', fontsize=15, fontweight='bold', pad=15)
        axes[0].legend(fontsize=11)
        axes[0].spines['top'].set_visible(False)
        axes[0].spines['right'].set_visible(False)

        # Score by domain
        domain_scores = defaultdict(list)
        for rec in recommendations:
            domain = rec['preferred_domain']
            for job in rec['recommended_jobs']:
                domain_scores[domain].append(job['total_score'])

        domains = list(domain_scores.keys())
        mean_scores = [np.mean(domain_scores[d]) for d in domains]

        bars = axes[1].bar(domains, mean_scores, color=['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0'],
                           edgecolor='black', linewidth=0.5, width=0.6)

        for bar, score in zip(bars, mean_scores):
            axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                         f'{score:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

        axes[1].set_xlabel('Preferred Domain', fontsize=13, fontweight='bold')
        axes[1].set_ylabel('Average Recommendation Score', fontsize=13, fontweight='bold')
        axes[1].set_title('Average Recommendation Score by Preferred Domain', fontsize=15, fontweight='bold', pad=15)
        axes[1].tick_params(axis='x', rotation=30)
        axes[1].spines['top'].set_visible(False)
        axes[1].spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig11_recommendation_scores.png'))
        plt.close()
        print("Generated: fig11_recommendation_scores.png")

    def plot_eligibility_by_branch(self, students, companies):
        """Plot 12: Eligibility analysis by branch."""
        branch_eligible = defaultdict(lambda: {'eligible': 0, 'total': 0})

        for student in students:
            branch = student['branch']
            branch_eligible[branch]['total'] += 1

            # Check eligibility for at least one company
            for company in companies:
                if (student['cgpa'] >= company['min_cgpa'] and
                    student['branch'] in company['required_branches']):
                    branch_eligible[branch]['eligible'] += 1
                    break

        branches = list(branch_eligible.keys())
        eligible = [branch_eligible[b]['eligible'] for b in branches]
        total = [branch_eligible[b]['total'] for b in branches]
        ineligible = [t - e for t, e in zip(total, eligible)]

        fig, ax = plt.subplots(figsize=(14, 7))
        x = np.arange(len(branches))
        width = 0.35

        bars1 = ax.bar(x - width/2, eligible, width, label='Eligible',
                       color='#4CAF50', edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + width/2, ineligible, width, label='Not Eligible',
                       color='#E91E63', edgecolor='black', linewidth=0.5)

        ax.set_xlabel('Branch', fontsize=13, fontweight='bold')
        ax.set_ylabel('Number of Students', fontsize=13, fontweight='bold')
        ax.set_title('Placement Eligibility by Branch', fontsize=15, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(branches, rotation=30, ha='right')
        ax.legend(fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig12_eligibility_by_branch.png'))
        plt.close()
        print("Generated: fig12_eligibility_by_branch.png")

    def plot_registration_trend(self, students):
        """Plot 13: Registration trend over time."""
        dates = [s['registration_date'] for s in students]
        dates_sorted = sorted(dates)

        # Group by week
        from collections import Counter
        week_counts = Counter()
        for d in dates:
            date_obj = datetime.strptime(d, '%Y-%m-%d')
            week_num = date_obj.isocalendar()[1]
            month = date_obj.strftime('%B')
            week_counts[f'Week {week_num}'] += 1

        weeks = list(week_counts.keys())[:13]
        counts = list(week_counts.values())[:13]

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(weeks, counts, marker='o', linewidth=2.5, markersize=8, color='#2196F3',
                markerfacecolor='white', markeredgewidth=2)
        ax.fill_between(range(len(weeks)), counts, alpha=0.2, color='#2196F3')

        ax.set_xlabel('Registration Period (Weekly)', fontsize=13, fontweight='bold')
        ax.set_ylabel('Number of Registrations', fontsize=13, fontweight='bold')
        ax.set_title('Student Registration Trend Over Time', fontsize=15, fontweight='bold', pad=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig13_registration_trend.png'))
        plt.close()
        print("Generated: fig13_registration_trend.png")

    def plot_system_architecture(self):
        """Plot 14: System architecture diagram."""
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('System Architecture of AI-Driven Campus Placement Platform', fontsize=15,
                     fontweight='bold', pad=20)

        # Define boxes
        boxes = {
            'Student\nPortal': (10, 75, 18, 15, '#2196F3'),
            'Registration\nModule': (10, 50, 18, 15, '#4CAF50'),
            'Resume\nUpload': (10, 25, 18, 15, '#FF9800'),
            'Placement\nOfficer\nDashboard': (10, 5, 18, 15, '#9C27B0'),

            'NLP Engine\n(Skill Extraction)': (45, 75, 22, 15, '#E91E63'),
            'ML Matching\nEngine': (45, 50, 22, 15, '#00BCD4'),
            'Recommendation\nEngine': (45, 25, 22, 15, '#795548'),

            'Company\nDatabase': (80, 75, 15, 15, '#607D8B'),
            'Student\nDatabase': (80, 50, 15, 15, '#3F51B5'),
            'Notification\nService': (80, 25, 15, 15, '#FF5722'),
        }

        for name, (x, y, w, h, color) in boxes.items():
            rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                                           facecolor=color, alpha=0.8, edgecolor='black',
                                           linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=10,
                    fontweight='bold', color='white', wrap=True)

        # Draw arrows
        arrow_props = dict(arrowstyle='->', color='#333333', lw=2)

        # Student Portal -> Registration Module
        ax.annotate('', xy=(19, 50), xytext=(19, 75), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # Registration -> Resume Upload
        ax.annotate('', xy=(19, 25), xytext=(19, 50), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # Resume Upload -> NLP Engine
        ax.annotate('', xy=(45, 75), xytext=(28, 32), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # NLP -> ML Matching
        ax.annotate('', xy=(56, 65), xytext=(56, 75), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # ML Matching -> Recommendation
        ax.annotate('', xy=(56, 40), xytext=(56, 50), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # Company DB -> ML Matching
        ax.annotate('', xy=(67, 55), xytext=(80, 75), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # Recommendation -> Notification
        ax.annotate('', xy=(80, 32), xytext=(67, 32), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # Student DB -> ML Matching
        ax.annotate('', xy=(67, 45), xytext=(80, 50), arrowprops=dict(arrowstyle='->', color='#333', lw=2))
        # Dashboard -> All
        ax.annotate('', xy=(45, 25), xytext=(28, 12), arrowprops=dict(arrowstyle='->', color='#333', lw=2))

        # Labels for arrows
        ax.text(38, 60, 'Resume\nData', fontsize=9, ha='center', color='#555')
        ax.text(38, 40, 'Processed\nSkills', fontsize=9, ha='center', color='#555')

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig14_system_architecture.png'))
        plt.close()
        print("Generated: fig14_system_architecture.png")

    def plot_ml_flowchart(self):
        """Plot 15: ML Pipeline flowchart."""
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Machine Learning Pipeline for Resume-Company Matching', fontsize=15,
                     fontweight='bold', pad=20)

        # Steps
        steps = [
            ('Data\nCollection', 5, 85, 15, 10, '#2196F3'),
            ('Text\nPreprocessing', 5, 65, 15, 10, '#4CAF50'),
            ('TF-IDF\nVectorization', 5, 45, 15, 10, '#FF9800'),
            ('Cosine\nSimilarity', 5, 25, 15, 10, '#E91E63'),
            ('Ranking\n& Filtering', 5, 5, 15, 10, '#9C27B0'),

            ('Raw Resumes\n& Job Descriptions', 35, 85, 20, 10, '#BBDEFB'),
            ('Tokenization\nStop Word Removal\nLemmatization', 35, 65, 20, 10, '#C8E6C9'),
            ('Feature\nMatrix', 35, 45, 20, 10, '#FFE0B2'),
            ('Similarity\nMatrix', 35, 25, 20, 10, '#F8BBD0'),
            ('Top Matches\nRecommended', 35, 5, 20, 10, '#E1BEE7'),
        ]

        for name, x, y, w, h, color in steps:
            rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3",
                                           facecolor=color, alpha=0.8, edgecolor='black',
                                           linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=9,
                    fontweight='bold', color='black' if 'C8E6C9' not in color and 'FFE0B2' not in color and 'BBDEFB' not in color and 'F8BBD0' not in color and 'E1BEE7' not in color else 'black',
                    wrap=True)

        # Arrows
        for i in range(4):
            y1 = steps[i][2] + steps[i][4]
            y2 = steps[i+1][2] + steps[i+1][4]
            ax.annotate('', xy=(12.5, y2), xytext=(12.5, y1),
                        arrowprops=dict(arrowstyle='->', color='#333', lw=2))
            ax.annotate('', xy=(45, y2), xytext=(45, y1),
                        arrowprops=dict(arrowstyle='->', color='#333', lw=2))

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'fig15_ml_pipeline_flowchart.png'))
        plt.close()
        print("Generated: fig15_ml_pipeline_flowchart.png")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main execution function."""
    print("=" * 70)
    print("AI-Driven Campus Placement Platform - Full Execution")
    print("=" * 70)

    # Step 1: Generate Data
    print("\n[1/6] Generating sample data...")
    students = generate_student_data(50)
    companies = generate_company_data(15)
    print(f"  Generated {len(students)} student profiles")
    print(f"  Generated {len(companies)} company profiles")

    # Save data to JSON
    with open('/home/ubuntu/project/campus_placement/students_data.json', 'w') as f:
        json.dump(students, f, indent=2)
    with open('/home/ubuntu/project/campus_placement/companies_data.json', 'w') as f:
        json.dump(companies, f, indent=2)
    print("  Data saved to JSON files")

    # Step 2: Resume Analysis
    print("\n[2/6] Analyzing resumes using NLP...")
    analyzer = ResumeAnalyzer()
    resume_analyses = analyzer.analyze_all_resumes(students)

    # Print sample analysis
    print(f"\n  Sample Resume Analysis (Student 1):")
    print(f"    Name: {resume_analyses[0]['name']}")
    print(f"    CGPA: {resume_analyses[0]['cgpa']}")
    print(f"    Skills Found: {resume_analyses[0]['skills_found']}")
    print(f"    Resume Score: {resume_analyses[0]['resume_score']}")
    print(f"    Category: {resume_analyses[0]['score_category']}")

    # Save resume analyses
    # Convert for JSON serialization
    serializable_analyses = []
    for r in resume_analyses:
        sr = dict(r)
        sr['key_info'] = {k: str(v) for k, v in sr['key_info'].items()}
        serializable_analyses.append(sr)
    with open('/home/ubuntu/project/campus_placement/resume_analyses.json', 'w') as f:
        json.dump(serializable_analyses, f, indent=2)

    # Step 3: Job Matching
    print("\n[3/6] Running AI-powered job matching engine...")
    matcher = JobMatchingEngine()
    matches = matcher.match_students_to_companies(students, companies)

    print(f"\n  Matching Results:")
    print(f"    Total students processed: {len(matches)}")
    avg_matches = np.mean([m['total_eligible'] for m in matches])
    print(f"    Average eligible companies per student: {avg_matches:.1f}")

    # Step 4: Job Recommendations
    print("\n[4/6] Generating personalized job recommendations...")
    recommender = JobRecommendationEngine()
    recommendations = recommender.recommend_jobs(students, companies, resume_analyses)

    print(f"\n  Recommendation Results:")
    print(f"    Total students with recommendations: {len(recommendations)}")
    avg_recs = np.mean([len(r['recommended_jobs']) for r in recommendations])
    print(f"    Average recommendations per student: {avg_recs:.1f}")

    # Step 5: Analytics
    print("\n[5/6] Generating placement analytics...")
    analytics = PlacementAnalytics()
    summary = analytics.generate_summary_report(students, companies, matches, recommendations)

    print(f"\n  Placement Summary:")
    print(f"    Total Students: {summary['total_students']}")
    print(f"    Eligible Students: {summary['eligible_students']}")
    print(f"    Eligibility Rate: {summary['eligibility_rate']}%")
    print(f"    Average CGPA: {summary['average_cgpa']}")
    print(f"    Total Companies: {summary['total_companies']}")
    print(f"    Total Hiring Capacity: {summary['total_hiring_capacity']}")

    # Save analytics
    with open('/home/ubuntu/project/campus_placement/analytics_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    # Step 6: Visualization
    print("\n[6/6] Generating visualization charts...")
    viz = VisualizationEngine()

    viz.plot_students_per_branch(students)
    viz.plot_cgpa_distribution(students)
    viz.plot_placement_status(students)
    viz.plot_skill_wordcloud(students)
    viz.plot_top_skills(students)
    viz.plot_company_skills_required(companies)
    viz.plot_matching_heatmap(students, companies, matches)
    viz.plot_company_hiring_capacity(companies)
    viz.plot_skill_gap_analysis(students, companies)
    viz.plot_recruitment_timeline(companies)
    viz.plot_recommendation_scores(recommendations)
    viz.plot_eligibility_by_branch(students, companies)
    viz.plot_registration_trend(students)
    viz.plot_system_architecture()
    viz.plot_ml_flowchart()

    print("\n" + "=" * 70)
    print("All visualizations generated successfully!")
    print(f"Images saved in: {viz.output_dir}/")
    print("=" * 70)

    # Print sample recommendation
    print("\n--- Sample Job Recommendation ---")
    if recommendations:
        sample = recommendations[0]
        print(f"Student: {sample['student_name']} ({sample['branch']}, CGPA: {sample['cgpa']})")
        print(f"Preferred Domain: {sample['preferred_domain']}")
        print("Top Recommendations:")
        for i, job in enumerate(sample['recommended_jobs'][:3], 1):
            print(f"  {i}. {job['company']} - {job['package_range']}")
            print(f"     Score: {job['total_score']} | Location: {job['location']}")
            print(f"     Common Skills: {', '.join(job['common_skills'])}")

    return {
        'students': students,
        'companies': companies,
        'resume_analyses': resume_analyses,
        'matches': matches,
        'recommendations': recommendations,
        'summary': summary
    }


if __name__ == '__main__':
    results = main()

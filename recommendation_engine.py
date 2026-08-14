"""
Personalized Job Recommendation Engine
Uses weighted scoring algorithm combining:
- Skill Match (40%)
- Branch Eligibility (20%)
- CGPA Compatibility (20%)
- Preference Alignment (20%)
"""

import json
import numpy as np
from collections import defaultdict


class RecommendationEngine:
    """Personalized Job Recommendation Engine."""

    WEIGHTS = {
        'skill_match': 0.40,
        'branch_match': 0.20,
        'cgpa_match': 0.20,
        'preference_match': 0.20
    }

    DOMAIN_MAPPING = {
        'Software Development': ['IT Services', 'Cloud Services', 'E-Commerce'],
        'Data Science': ['IT Services', 'Finance Tech', 'Consulting'],
        'Web Development': ['IT Services', 'E-Commerce', 'Consulting'],
        'Cloud Computing': ['Cloud Services', 'IT Services'],
        'Product Management': ['E-Commerce', 'Consulting', 'Finance Tech']
    }

    def __init__(self):
        pass

    def compute_skill_match(self, student_skills, required_skills):
        """Compute weighted skill match score (0-40)."""
        student_set = set(student_skills)
        required_set = set(required_skills)
        common = student_set.intersection(required_set)

        # Precision: how many of student's skills match requirements
        precision = len(common) / max(len(required_skills), 1)
        # Recall: how many of required skills the student has
        recall = len(common) / max(len(student_skills), 1)
        # F1-like score
        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0

        return round(f1 * 40, 2)

    def compute_branch_match(self, student_branch, required_branches):
        """Compute branch match score (0-20)."""
        if student_branch in required_branches:
            return 20
        return 0

    def compute_cgpa_match(self, student_cgpa, min_cgpa):
        """Compute CGPA match score (0-20)."""
        if student_cgpa >= min_cgpa:
            diff = student_cgpa - min_cgpa
            return min(20, 10 + diff * 5)
        return 0

    def compute_preference_match(self, company, student_prefs):
        """Compute preference alignment score (0-20)."""
        score = 0

        # Location match (0-10)
        if company['location'] == student_prefs['preferred_location']:
            score += 10

        # Domain match (0-10)
        preferred_domains = self.DOMAIN_MAPPING.get(student_prefs['preferred_domain'], [])
        if company['industry'] in preferred_domains:
            score += 10

        return score

    def recommend(self, students, companies):
        """Generate comprehensive job recommendations."""
        recommendations = []

        for student in students:
            if student['placement_status'] == 'Not Eligible':
                continue

            scored_companies = []

            for company in companies:
                # Compute individual scores
                skill_score = self.compute_skill_match(
                    student['skills'], company['required_skills'])
                branch_score = self.compute_branch_match(
                    student['branch'], company['required_branches'])
                cgpa_score = self.compute_cgpa_match(
                    student['cgpa'], company['min_cgpa'])
                pref_score = self.compute_preference_match(
                    company, student['preferences'])

                total = skill_score + branch_score + cgpa_score + pref_score

                # Only include if eligible
                if branch_score > 0 and cgpa_score > 0:
                    scored_companies.append({
                        'company': company['name'],
                        'industry': company['industry'],
                        'job_roles': company['job_roles'],
                        'package_range': company['package_range'],
                        'location': company['location'],
                        'drive_type': company['drive_type'],
                        'common_skills': list(set(student['skills']).intersection(
                            set(company['required_skills']))),
                        'scores': {
                            'skill_match': skill_score,
                            'branch_match': branch_score,
                            'cgpa_match': cgpa_score,
                            'preference_match': pref_score
                        },
                        'total_score': round(total, 2),
                        'skill_match_pct': round(
                            len(set(student['skills']).intersection(
                                set(company['required_skills']))) /
                            max(len(company['required_skills']), 1) * 100, 1)
                    })

            scored_companies.sort(key=lambda x: x['total_score'], reverse=True)

            recommendations.append({
                'student_id': student['student_id'],
                'student_name': student['name'],
                'branch': student['branch'],
                'cgpa': student['cgpa'],
                'preferred_domain': student['preferences']['preferred_domain'],
                'preferred_location': student['preferences']['preferred_location'],
                'recommendations': scored_companies[:5],
                'total_eligible': len(scored_companies)
            })

        return recommendations

    def generate_comparison_report(self, recommendations):
        """Generate a comparative report of recommendations."""
        domain_stats = defaultdict(lambda: {
            'count': 0, 'avg_score': 0, 'scores': []
        })

        for rec in recommendations:
            domain = rec['preferred_domain']
            domain_stats[domain]['count'] += 1
            for job in rec['recommendations']:
                domain_stats[domain]['scores'].append(job['total_score'])

        report = {}
        for domain, stats in domain_stats.items():
            report[domain] = {
                'students': stats['count'],
                'avg_recommendation_score': round(np.mean(stats['scores']), 2) if stats['scores'] else 0,
                'max_score': round(max(stats['scores']), 2) if stats['scores'] else 0,
                'min_score': round(min(stats['scores']), 2) if stats['scores'] else 0
            }

        return report


def demonstrate_recommendations():
    """Demonstrate the recommendation engine."""
    with open('/home/ubuntu/project/campus_placement/students_data.json', 'r') as f:
        students = json.load(f)
    with open('/home/ubuntu/project/campus_placement/companies_data.json', 'r') as f:
        companies = json.load(f)

    engine = RecommendationEngine()
    recommendations = engine.recommend(students, companies)

    print("=" * 60)
    print("Job Recommendation Results")
    print("=" * 60)

    for rec in recommendations[:3]:
        print(f"\n  {rec['student_name']} ({rec['branch']}, CGPA: {rec['cgpa']})")
        print(f"  Preferred: {rec['preferred_domain']} in {rec['preferred_location']}")
        print(f"  Top Recommendations:")
        for i, job in enumerate(rec['recommendations'][:3], 1):
            print(f"    {i}. {job['company']} - {job['package_range']} (Score: {job['total_score']})")
            print(f"       Location: {job['location']} | Skills: {', '.join(job['common_skills'])}")

    # Comparison report
    report = engine.generate_comparison_report(recommendations)
    print(f"\n\n  Domain-wise Recommendation Statistics:")
    for domain, stats in report.items():
        print(f"    {domain}: {stats['students']} students, "
              f"Avg Score: {stats['avg_recommendation_score']}")

    return recommendations, report


if __name__ == '__main__':
    demonstrate_recommendations()

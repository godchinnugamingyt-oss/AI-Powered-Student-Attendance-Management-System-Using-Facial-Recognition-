"""
AI-Powered Job Matching Engine
Uses TF-IDF vectorization and Cosine Similarity for matching
student resumes with company requirements.
Also demonstrates KMeans clustering for student grouping.
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import defaultdict


class AIMatchingEngine:
    """Advanced AI Matching Engine with multiple algorithms."""

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))

    def build_document_corpus(self, students, companies):
        """Build TF-IDF document corpus from skills."""
        student_docs = [' '.join(s['skills']) for s in students]
        company_docs = [' '.join(c['required_skills']) for c in companies]
        return student_docs, company_docs

    def compute_similarity(self, students, companies):
        """Compute TF-IDF cosine similarity between students and companies."""
        student_docs, company_docs = self.build_document_corpus(students, companies)
        all_docs = student_docs + company_docs

        tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_docs)
        student_vectors = tfidf_matrix[:len(students)]
        company_vectors = tfidf_matrix[len(students):]

        similarity_matrix = cosine_similarity(student_vectors, company_vectors)
        return similarity_matrix

    def find_best_matches(self, students, companies, top_n=5):
        """Find best matching companies for each student."""
        sim_matrix = self.compute_similarity(students, companies)
        results = []

        for i, student in enumerate(students):
            if student['placement_status'] == 'Not Eligible':
                continue

            matches = []
            for j, company in enumerate(companies):
                eligibility = (student['cgpa'] >= company['min_cgpa'] and
                              student['branch'] in company['required_branches'])
                matches.append({
                    'company': company['name'],
                    'similarity': round(sim_matrix[i][j], 4),
                    'eligible': eligibility,
                    'industry': company['industry'],
                    'package': company['package_range'],
                    'location': company['location']
                })

            matches.sort(key=lambda x: x['similarity'], reverse=True)
            eligible_matches = [m for m in matches if m['eligible']][:top_n]

            results.append({
                'student': student['name'],
                'branch': student['branch'],
                'cgpa': student['cgpa'],
                'skills': student['skills'],
                'matches': eligible_matches,
                'best_match_score': eligible_matches[0]['similarity'] if eligible_matches else 0
            })

        return results

    def cluster_students(self, students, n_clusters=5):
        """Cluster students based on their skill profiles."""
        student_docs = [' '.join(s['skills']) for s in students]

        tfidf = TfidfVectorizer(max_features=50)
        X = tfidf.fit_transform(student_docs)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X)

        cluster_groups = defaultdict(list)
        for i, cluster in enumerate(clusters):
            cluster_groups[cluster].append({
                'name': students[i]['name'],
                'branch': students[i]['branch'],
                'skills': students[i]['skills']
            })

        return dict(cluster_groups), clusters


def demonstrate_matching():
    """Demonstrate the matching engine."""
    # Load sample data
    with open('/home/ubuntu/project/campus_placement/students_data.json', 'r') as f:
        students = json.load(f)
    with open('/home/ubuntu/project/campus_placement/companies_data.json', 'r') as f:
        companies = json.load(f)

    engine = AIMatchingEngine()

    # Best matches
    print("\n" + "=" * 60)
    print("AI Job Matching Results")
    print("=" * 60)

    matches = engine.find_best_matches(students, companies)
    print(f"\nTotal students matched: {len(matches)}")

    for m in matches[:3]:
        print(f"\n  Student: {m['student']} ({m['branch']}, CGPA: {m['cgpa']})")
        print(f"  Top Matches:")
        for match in m['matches'][:3]:
            print(f"    - {match['company']} (Score: {match['similarity']}, "
                  f"Package: {match['package']}, Location: {match['location']})")

    # Clustering
    print("\n" + "=" * 60)
    print("Student Clustering (KMeans)")
    print("=" * 60)

    clusters, labels = engine.cluster_students(students, n_clusters=4)
    for cluster_id, students_list in clusters.items():
        print(f"\n  Cluster {cluster_id} ({len(students_list)} students):")
        print(f"    Skills: {', '.join(set(s for st in students_list for s in st['skills']))[:100]}...")

    return matches, clusters


if __name__ == '__main__':
    demonstrate_matching()

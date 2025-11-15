from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocess import clean_text  

def extract_job_title(job_text):
    """Extracts the job title from the first line of the job description."""
    return job_text.split("\n")[0] if job_text.strip() else ""

def compute_weighted_similarity(resume_text, job_text):
    """Computes similarity with controlled weighting for job-related terms."""
    model = SentenceTransformer("all-mpnet-base-v2")
    embeddings = model.encode([resume_text, job_text])
    base_similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0] * 100

    job_title = extract_job_title(job_text).lower()
    boost_keywords = job_title.split()  # Break title into keywords for weighting
    
    resume_vectorizer = TfidfVectorizer()
    resume_terms = set(resume_vectorizer.fit([resume_text]).get_feature_names_out())

    # ✅ Reduce keyword boost multiplier for controlled influence
    extra_weight = sum([1 for word in boost_keywords if word in resume_terms]) * 1.2  

    # ✅ Ensure final score never exceeds 100%
    final_score = min(base_similarity + extra_weight, 100)

    # ✅ Log score behavior for debugging
    print(f"🧐 Base Similarity Score: {base_similarity:.2f}%")
    print(f"🔍 Extra Weight Added: {extra_weight:.2f}")
    print(f"✅ Final Adjusted Score: {final_score:.2f}%")

    return round(final_score, 2)

def identify_missing_skills(resume_text, job_text):
    """Finds important job-related terms missing from the resume."""
    vectorizer = TfidfVectorizer()
    job_terms = vectorizer.fit([job_text]).get_feature_names_out()
    resume_terms = vectorizer.fit([resume_text]).get_feature_names_out()

    missing_skills = set(job_terms) - set(resume_terms)  # Identify gaps
    return list(missing_skills)
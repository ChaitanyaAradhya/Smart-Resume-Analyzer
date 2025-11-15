import os
from src.extract import extract_text_from_pdf
from src.preprocess import clean_text
from src.similarity import compute_weighted_similarity, identify_missing_skills  

def process_resumes(resume_folder, job_description_path):
    """Processes multiple resumes and ranks them based on match score."""
    
    if not os.path.exists(job_description_path):
        print(f"❌ Error: Job description file '{job_description_path}' not found!")
        return

    with open(job_description_path, "r", encoding="utf-8") as file:
        job_description = clean_text(file.read())

    resume_scores = []

    for resume_file in os.listdir(resume_folder):
        resume_path = os.path.join(resume_folder, resume_file)

        if not resume_file.endswith(".pdf"):
            continue  # ✅ Skip non-PDF files

        resume_text = extract_text_from_pdf(resume_path)
        processed_resume = clean_text(resume_text)

        match_score = compute_weighted_similarity(processed_resume, job_description)
        missing_skills = identify_missing_skills(processed_resume, job_description)

        resume_scores.append((resume_file, match_score, missing_skills))

    # ✅ Sort resumes by match score (best candidate first)
    resume_scores.sort(key=lambda x: x[1], reverse=True)

    print("\n🚀 **Resume Rankings for Job Posting:**")
    for rank, (resume_name, score, missing_skills) in enumerate(resume_scores, start=1):
        print(f"\n🏅 Rank #{rank} | {resume_name} | Match Score: {score:.2f}%")
        
        if missing_skills:
            print("🔍 Missing Skills:", ", ".join(missing_skills))

if __name__ == "__main__":
    resume_folder = os.path.abspath("data/resumes/")  # ✅ Store multiple resumes here
    job_description_path = os.path.abspath("data/job_description.txt")

    process_resumes(resume_folder, job_description_path)
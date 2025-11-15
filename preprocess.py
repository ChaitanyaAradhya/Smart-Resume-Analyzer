import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ✅ Correct Import for Extracting Resume Text
from src.extract import extract_text_from_pdf  

# ✅ Ensure NLTK resources are installed
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """Tokenizes, removes stopwords selectively, and lemmatizes."""
    if not text or text.strip() == "":
        print("❌ Error: No valid text found for preprocessing!")
        return ""

    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]  # Remove punctuation/numbers

    stop_words = set(stopwords.words("english"))
    
    # 🔥 Keep important tech & AI-related words
    important_words = {"python", "machinelearning", "ai", "deeplearning", "automation", "nlp",
                       "neuralnetworks", "computervision", "datascience", "algorithms", "tensorflow", "pytorch",
                       "research", "development", "optimization", "classification", "regression"}
    tokens = [word for word in tokens if word not in stop_words or word in important_words]  # Keep essential words

    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

if __name__ == "__main__":
    # ✅ Use Correct File Path
    resume_path = os.path.abspath("data/resume(2).pdf")
    if not os.path.exists(resume_path):  # Check if file exists
        print(f"❌ Error: File '{resume_path}' not found. Please verify the path and filename.")
    else:
        resume_text = extract_text_from_pdf(resume_path)  # Extract text from resume
        processed_text = clean_text(resume_text)

        print("\n✅ Preprocessed Resume Text (First 500 characters):\n")
        print(processed_text[:500])  # Display cleaned text
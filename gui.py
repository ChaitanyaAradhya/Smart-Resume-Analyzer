import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QPropertyAnimation, QRect
from src.extract import extract_text_from_pdf
from src.preprocess import clean_text
from src.similarity import compute_weighted_similarity, identify_missing_skills  

class ResumeAnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Apply Dark Theme
        self.setWindowTitle("Resume Analyzer - Dark Mode")
        self.setGeometry(200, 200, 800, 500)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # ✅ Layout Setup
        layout = QVBoxLayout()

        self.label = QLabel("Select multiple resumes to analyze:")
        layout.addWidget(self.label)

        self.file_button = QPushButton("Choose Resumes 📂")
        self.file_button.clicked.connect(self.select_resumes)
        layout.addWidget(self.file_button)

        self.analyze_button = QPushButton("Run Analysis 🚀")
        self.analyze_button.clicked.connect(self.run_analysis)
        layout.addWidget(self.analyze_button)

        self.leaderboard = QListWidget()
        layout.addWidget(self.leaderboard)

        self.setLayout(layout)

        self.resume_paths = []  # Store selected resumes

        # ✅ Add Button Animation
        self.animation = QPropertyAnimation(self.file_button, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(QRect(20, 20, 150, 40))
        self.animation.setEndValue(QRect(20, 20, 180, 40))

    def select_resumes(self):
        """Allows users to select multiple resume PDFs."""
        files, _ = QFileDialog.getOpenFileNames(self, "Select Resumes", "", "PDF Files (*.pdf)")
        if files:
            self.resume_paths = files
            self.label.setText(f"Selected: {len(files)} resumes")

            # ✅ Button Animation Effect
            self.animation.start()

    def run_analysis(self):
        """Runs analysis on multiple resumes and displays leaderboard."""
        if not self.resume_paths:
            self.leaderboard.clear()
            self.leaderboard.addItem("❌ No resumes selected! Please choose PDFs.")
            return

        job_description_path = os.path.abspath("data/job_description.txt")
        if not os.path.exists(job_description_path):
            self.leaderboard.clear()
            self.leaderboard.addItem("❌ Job description file missing!")
            return

        with open(job_description_path, "r", encoding="utf-8") as file:
            job_description = clean_text(file.read())

        resume_scores = []

        for resume_path in self.resume_paths:
            resume_text = extract_text_from_pdf(resume_path)
            processed_resume = clean_text(resume_text)

            match_score = compute_weighted_similarity(processed_resume, job_description)
            missing_skills = identify_missing_skills(processed_resume, job_description)

            resume_scores.append((os.path.basename(resume_path), match_score, missing_skills))

        # ✅ Sort resumes by match score
        resume_scores.sort(key=lambda x: x[1], reverse=True)

        self.leaderboard.clear()
        self.leaderboard.addItem("🏆 Resume Leaderboard (Best to Worst):\n")
        for rank, (resume_name, score, missing_skills) in enumerate(resume_scores, start=1):
            item = QListWidgetItem(f"🏅 Rank #{rank} | {resume_name} | Match: {score:.2f}%")
            self.leaderboard.addItem(item)

            if missing_skills:
                self.leaderboard.addItem(f"🔍 Missing Skills: {', '.join(missing_skills)}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResumeAnalyzerGUI()
    window.show()
    sys.exit(app.exec_())
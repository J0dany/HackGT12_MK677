import pdfplumber
import re

def parse_degreeworks_remaining(pdf_path):
    remaining_courses = []
    capture = False

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")

            for line in lines:
                # Start capturing when we find "Remaining"
                if "remaining" in line.lower():
                    capture = True
                    continue

                # Stop capturing if we find another section header
                if capture and re.search(r"completed|planned|notes", line, re.IGNORECASE):
                    capture = False

                if capture:
                    # Extract course codes like "CS 1331", "ECE 2020"
                    matches = re.findall(r"\b[A-Z]{2,4} \d{4}\b", line)
                    remaining_courses.extend(matches)

    return remaining_courses

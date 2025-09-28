import requests
from bs4 import BeautifulSoup
import json
import time
import sqlite3
import pandas as pd
from typing import List, Dict, Optional
import re

class GTCourseScraper:
    def __init__(self, db_path: str = "gt_courses.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing course data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                credits INTEGER,
                average_gpa REAL,
                department TEXT,
                description TEXT,
                prerequisites TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create majors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS majors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                major_name TEXT UNIQUE NOT NULL,
                college TEXT,
                degree_type TEXT,
                description TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create major_courses table (many-to-many relationship)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS major_courses (
                major_id INTEGER,
                course_id INTEGER,
                requirement_type TEXT, -- 'core', 'elective', 'prerequisite'
                FOREIGN KEY (major_id) REFERENCES majors (id),
                FOREIGN KEY (course_id) REFERENCES courses (id),
                PRIMARY KEY (major_id, course_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def scrape_course_critique(self, start_year: int = 2020, end_year: int = 2024) -> List[Dict]:
        """Scrape course data from GT Course Critique"""
        courses = []
        
        # GT Course Critique typically has URLs like:
        # https://critique.gatech.edu/course/CS/1331/
        # We'll need to discover courses through various methods
        
        print("Starting GT Course Critique scraping...")
        
        # Common GT course prefixes
        course_prefixes = [
            'CS', 'ECE', 'MATH', 'PHYS', 'CHEM', 'BIOL', 'PSYC', 'ECON', 
            'MGT', 'MSE', 'ME', 'AE', 'CEE', 'ISYE', 'BMED', 'COA', 
            'LMC', 'HIST', 'POL', 'INTA', 'PUBP', 'ARCH', 'ID', 'MUSI',
            'ENGL', 'SPAN', 'FREN', 'GERM', 'JAPN', 'KOR', 'CHIN', 'RUSS',
            'PHIL', 'SOC', 'ANTH', 'PSYC', 'COG', 'NEURO', 'BME', 'CHEM',
            'BIOL', 'PHYS', 'MATH', 'STAT', 'ISYE', 'MGT', 'ECON', 'PUBP'
        ]
        
        for prefix in course_prefixes:
            print(f"Scraping courses for prefix: {prefix}")
            prefix_courses = self._scrape_course_prefix(prefix, start_year, end_year)
            courses.extend(prefix_courses)
            time.sleep(1)  # Be respectful to the server
        
        return courses
    
    def _scrape_course_prefix(self, prefix: str, start_year: int, end_year: int) -> List[Dict]:
        """Scrape all courses for a given prefix"""
        courses = []
        
        # Try different course number ranges
        for course_num in range(1000, 7000, 100):  # 1000, 1100, 1200, etc.
            for offset in range(0, 100, 10):  # 1000, 1010, 1020, etc.
                course_code = f"{prefix} {course_num + offset}"
                course_data = self._scrape_single_course(course_code)
                if course_data:
                    courses.append(course_data)
                    time.sleep(0.5)  # Rate limiting
        
        return courses
    
    def _scrape_single_course(self, course_code: str) -> Optional[Dict]:
        """Scrape data for a single course"""
        try:
            # Try different URL patterns
            url_patterns = [
                f"https://critique.gatech.edu/course/{course_code.replace(' ', '/')}/",
                f"https://critique.gatech.edu/course/{course_code.replace(' ', '')}/",
                f"https://critique.gatech.edu/course/{course_code}/"
            ]
            
            for url in url_patterns:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        return self._parse_course_page(response.text, course_code)
                except requests.RequestException:
                    continue
            
            return None
            
        except Exception as e:
            print(f"Error scraping course {course_code}: {e}")
            return None
    
    def _parse_course_page(self, html: str, course_code: str) -> Optional[Dict]:
        """Parse course data from HTML page"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract course information
            course_name = self._extract_course_name(soup)
            credits = self._extract_credits(soup)
            average_gpa = self._extract_average_gpa(soup)
            description = self._extract_description(soup)
            prerequisites = self._extract_prerequisites(soup)
            
            if not course_name:  # If we can't find basic info, skip
                return None
            
            return {
                'course_code': course_code,
                'course_name': course_name,
                'credits': credits,
                'average_gpa': average_gpa,
                'department': course_code.split()[0],
                'description': description,
                'prerequisites': prerequisites
            }
            
        except Exception as e:
            print(f"Error parsing course page for {course_code}: {e}")
            return None
    
    def _extract_course_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course name from page"""
        # Look for common patterns
        selectors = [
            'h1.course-title',
            'h1',
            '.course-name',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                if text and len(text) > 3:  # Basic validation
                    return text
        
        return None
    
    def _extract_credits(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract credit hours from page"""
        # Look for credit information
        credit_patterns = [
            r'(\d+)\s*credit',
            r'(\d+)\s*hr',
            r'(\d+)\s*hour'
        ]
        
        text = soup.get_text()
        for pattern in credit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_average_gpa(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract average GPA from page"""
        # Look for GPA information
        gpa_patterns = [
            r'average\s+gpa[:\s]*(\d+\.?\d*)',
            r'gpa[:\s]*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*gpa'
        ]
        
        text = soup.get_text()
        for pattern in gpa_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course description"""
        selectors = [
            '.course-description',
            '.description',
            'p'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                if len(text) > 20:  # Basic validation
                    return text
        
        return None
    
    def _extract_prerequisites(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract prerequisites"""
        prereq_patterns = [
            r'prerequisite[s]?[:\s]*(.+?)(?:\n|$)',
            r'prereq[s]?[:\s]*(.+?)(?:\n|$)'
        ]
        
        text = soup.get_text()
        for pattern in prereq_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def scrape_gt_majors(self) -> List[Dict]:
        """Scrape GT majors from official website"""
        majors = []
        
        # GT majors from official sources
        gt_majors_data = [
            # College of Computing
            {"major_name": "Computer Science", "college": "College of Computing", "degree_type": "Bachelor of Science"},
            {"major_name": "Computational Media", "college": "College of Computing", "degree_type": "Bachelor of Science"},
            {"major_name": "Computer Engineering", "college": "College of Computing", "degree_type": "Bachelor of Science"},
            
            # College of Engineering
            {"major_name": "Aerospace Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Biomedical Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Chemical and Biomolecular Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Civil Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Electrical Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Environmental Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Industrial Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Materials Science and Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Mechanical Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            {"major_name": "Nuclear and Radiological Engineering", "college": "College of Engineering", "degree_type": "Bachelor of Science"},
            
            # College of Sciences
            {"major_name": "Applied Mathematics", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
            {"major_name": "Biology", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
            {"major_name": "Chemistry", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
            {"major_name": "Earth and Atmospheric Sciences", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
            {"major_name": "Mathematics", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
            {"major_name": "Physics", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
            {"major_name": "Psychology", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
            
            # Scheller College of Business
            {"major_name": "Business Administration", "college": "Scheller College of Business", "degree_type": "Bachelor of Science"},
            
            # Ivan Allen College of Liberal Arts
            {"major_name": "Applied Languages and Intercultural Studies", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
            {"major_name": "Economics", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
            {"major_name": "History, Technology, and Society", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
            {"major_name": "International Affairs", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
            {"major_name": "Literature, Media, and Communication", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
            {"major_name": "Public Policy", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
            
            # College of Design
            {"major_name": "Architecture", "college": "College of Design", "degree_type": "Bachelor of Science"},
            {"major_name": "Industrial Design", "college": "College of Design", "degree_type": "Bachelor of Science"},
        ]
        
        return gt_majors_data
    
    def save_courses_to_db(self, courses: List[Dict]):
        """Save scraped courses to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for course in courses:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO courses 
                    (course_code, course_name, credits, average_gpa, department, description, prerequisites)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    course['course_code'],
                    course['course_name'],
                    course['credits'],
                    course['average_gpa'],
                    course['department'],
                    course['description'],
                    course['prerequisites']
                ))
            except Exception as e:
                print(f"Error saving course {course['course_code']}: {e}")
        
        conn.commit()
        conn.close()
    
    def save_majors_to_db(self, majors: List[Dict]):
        """Save scraped majors to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for major in majors:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO majors 
                    (major_name, college, degree_type, description)
                    VALUES (?, ?, ?, ?)
                ''', (
                    major['major_name'],
                    major['college'],
                    major['degree_type'],
                    major.get('description', '')
                ))
            except Exception as e:
                print(f"Error saving major {major['major_name']}: {e}")
        
        conn.commit()
        conn.close()
    
    def get_courses_by_department(self, department: str) -> List[Dict]:
        """Get all courses for a specific department"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT course_code, course_name, credits, average_gpa, description, prerequisites
            FROM courses 
            WHERE department = ?
            ORDER BY course_code
        ''', (department,))
        
        courses = []
        for row in cursor.fetchall():
            courses.append({
                'course_code': row[0],
                'course_name': row[1],
                'credits': row[2],
                'average_gpa': row[3],
                'description': row[4],
                'prerequisites': row[5]
            })
        
        conn.close()
        return courses
    
    def get_all_majors(self) -> List[Dict]:
        """Get all majors from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT major_name, college, degree_type, description
            FROM majors 
            ORDER BY college, major_name
        ''')
        
        majors = []
        for row in cursor.fetchall():
            majors.append({
                'major_name': row[0],
                'college': row[1],
                'degree_type': row[2],
                'description': row[3]
            })
        
        conn.close()
        return majors

def main():
    """Main function to run the scraper"""
    scraper = GTCourseScraper()
    
    print("Scraping GT majors...")
    majors = scraper.scrape_gt_majors()
    scraper.save_majors_to_db(majors)
    print(f"Saved {len(majors)} majors to database")
    
    print("Scraping GT courses...")
    courses = scraper.scrape_course_critique()
    scraper.save_courses_to_db(courses)
    print(f"Saved {len(courses)} courses to database")
    
    print("Scraping complete!")

if __name__ == "__main__":
    main()

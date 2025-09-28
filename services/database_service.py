import sqlite3
import json
from typing import List, Dict, Optional
from Models.models import Course, Major, Term, Roadmap

class GTDatabaseService:
    def __init__(self, db_path: str = "gt_courses.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database if it doesn't exist"""
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
    
    def get_courses_by_department(self, department: str) -> List[Course]:
        """Get all courses for a specific department"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT course_code, course_name, credits, average_gpa, department, description, prerequisites
            FROM courses 
            WHERE department = ?
            ORDER BY course_code
        ''', (department,))
        
        courses = []
        for row in cursor.fetchall():
            course = Course(
                course_name=row[1],
                course_code=row[0],
                credits=row[2],
                average_gpa=row[3],
                department=row[4],
                description=row[5],
                prerequisites=row[6].split(',') if row[6] else []
            )
            courses.append(course)
        
        conn.close()
        return courses
    
    def get_all_majors(self) -> List[Major]:
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
            major = Major(
                major_name=row[0],
                college=row[1],
                degree_type=row[2],
                description=row[3]
            )
            majors.append(major)
        
        conn.close()
        return majors
    
    def get_course_by_code(self, course_code: str) -> Optional[Course]:
        """Get a specific course by its code"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT course_code, course_name, credits, average_gpa, department, description, prerequisites
            FROM courses 
            WHERE course_code = ?
        ''', (course_code,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Course(
                course_name=row[1],
                course_code=row[0],
                credits=row[2],
                average_gpa=row[3],
                department=row[4],
                description=row[5],
                prerequisites=row[6].split(',') if row[6] else []
            )
        
        return None
    
    def search_courses(self, query: str) -> List[Course]:
        """Search courses by name or code"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT course_code, course_name, credits, average_gpa, department, description, prerequisites
            FROM courses 
            WHERE course_name LIKE ? OR course_code LIKE ?
            ORDER BY course_code
        ''', (f'%{query}%', f'%{query}%'))
        
        courses = []
        for row in cursor.fetchall():
            course = Course(
                course_name=row[1],
                course_code=row[0],
                credits=row[2],
                average_gpa=row[3],
                department=row[4],
                description=row[5],
                prerequisites=row[6].split(',') if row[6] else []
            )
            courses.append(course)
        
        conn.close()
        return courses
    
    def get_courses_for_major(self, major_name: str) -> Dict[str, List[Course]]:
        """Get courses associated with a major"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.course_code, c.course_name, c.credits, c.average_gpa, c.department, c.description, c.prerequisites, mc.requirement_type
            FROM courses c
            JOIN major_courses mc ON c.id = mc.course_id
            JOIN majors m ON mc.major_id = m.id
            WHERE m.major_name = ?
            ORDER BY mc.requirement_type, c.course_code
        ''', (major_name,))
        
        courses = {'core': [], 'elective': [], 'prerequisite': []}
        for row in cursor.fetchall():
            course = Course(
                course_name=row[1],
                course_code=row[0],
                credits=row[2],
                average_gpa=row[3],
                department=row[4],
                description=row[5],
                prerequisites=row[6].split(',') if row[6] else []
            )
            
            req_type = row[7] or 'elective'
            if req_type in courses:
                courses[req_type].append(course)
        
        conn.close()
        return courses
    
    def create_roadmap_from_courses(self, course_codes: List[str], major_name: str = None) -> Roadmap:
        """Create a roadmap from a list of course codes"""
        roadmap = Roadmap(f"Roadmap for {major_name or 'Selected Courses'}")
        
        # Group courses by semester (simplified logic)
        courses = []
        for code in course_codes:
            course = self.get_course_by_code(code)
            if course:
                courses.append(course)
        
        # Simple semester distribution (15 credits per semester)
        current_semester = 1
        current_term = Term(f"Semester {current_semester}")
        current_credits = 0
        
        for course in courses:
            if current_credits + (course.credits or 3) > 15 and current_term.courses:
                # Start new semester
                roadmap.add_term(current_term)
                current_semester += 1
                current_term = Term(f"Semester {current_semester}")
                current_credits = 0
            
            current_term.add_course(course)
            current_credits += course.credits or 3
        
        if current_term.courses:
            roadmap.add_term(current_term)
        
        # Calculate estimated GPA
        roadmap.calculate_estimated_gpa()
        
        return roadmap
    
    def get_departments(self) -> List[str]:
        """Get all unique departments"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT department 
            FROM courses 
            WHERE department IS NOT NULL
            ORDER BY department
        ''')
        
        departments = [row[0] for row in cursor.fetchall()]
        conn.close()
        return departments
    
    def get_courses_with_gpa(self, min_gpa: float = None, max_gpa: float = None) -> List[Course]:
        """Get courses filtered by GPA range"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT course_code, course_name, credits, average_gpa, department, description, prerequisites
            FROM courses 
            WHERE average_gpa IS NOT NULL
        '''
        params = []
        
        if min_gpa is not None:
            query += ' AND average_gpa >= ?'
            params.append(min_gpa)
        
        if max_gpa is not None:
            query += ' AND average_gpa <= ?'
            params.append(max_gpa)
        
        query += ' ORDER BY average_gpa DESC'
        
        cursor.execute(query, params)
        
        courses = []
        for row in cursor.fetchall():
            course = Course(
                course_name=row[1],
                course_code=row[0],
                credits=row[2],
                average_gpa=row[3],
                department=row[4],
                description=row[5],
                prerequisites=row[6].split(',') if row[6] else []
            )
            courses.append(course)
        
        conn.close()
        return courses
    
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

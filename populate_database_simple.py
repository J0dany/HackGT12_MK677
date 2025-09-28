#!/usr/bin/env python3
"""
Simplified database population script that doesn't require web scraping dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.database_service import GTDatabaseService
from Models.models import Course, Major

def populate_initial_data():
    """Populate database with initial GT data without web scraping"""
    print("Initializing GT Course Database...")
    
    # Initialize services
    db_service = GTDatabaseService()
    
    # Add GT majors (hardcoded data)
    print("Adding GT majors...")
    gt_majors = get_gt_majors_data()
    db_service.save_majors_to_db(gt_majors)
    print(f"Added {len(gt_majors)} majors")
    
    # Add sample courses for each major
    print("Adding sample courses...")
    sample_courses = create_sample_courses()
    
    # Save courses to database
    courses_data = []
    for course in sample_courses:
        courses_data.append({
            'course_code': course.course_code,
            'course_name': course.course_name,
            'credits': course.credits,
            'average_gpa': course.average_gpa,
            'department': course.department,
            'description': course.description,
            'prerequisites': ','.join(course.prerequisites) if course.prerequisites else None
        })
    
    db_service.save_courses_to_db(courses_data)
    print(f"Added {len(sample_courses)} sample courses")
    
    print("Database population complete!")

def get_gt_majors_data():
    """Get GT majors data without web scraping"""
    return [
        {"major_name": "Computer Science", "college": "College of Computing", "degree_type": "Bachelor of Science"},
        {"major_name": "Computational Media", "college": "College of Computing", "degree_type": "Bachelor of Science"},
        {"major_name": "Computer Engineering", "college": "College of Computing", "degree_type": "Bachelor of Science"},
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
        {"major_name": "Applied Mathematics", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
        {"major_name": "Biology", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
        {"major_name": "Chemistry", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
        {"major_name": "Earth and Atmospheric Sciences", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
        {"major_name": "Mathematics", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
        {"major_name": "Physics", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
        {"major_name": "Psychology", "college": "College of Sciences", "degree_type": "Bachelor of Science"},
        {"major_name": "Business Administration", "college": "Scheller College of Business", "degree_type": "Bachelor of Science"},
        {"major_name": "Applied Languages and Intercultural Studies", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
        {"major_name": "Economics", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
        {"major_name": "History, Technology, and Society", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
        {"major_name": "International Affairs", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
        {"major_name": "Literature, Media, and Communication", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
        {"major_name": "Public Policy", "college": "Ivan Allen College of Liberal Arts", "degree_type": "Bachelor of Science"},
        {"major_name": "Architecture", "college": "College of Design", "degree_type": "Bachelor of Science"},
        {"major_name": "Industrial Design", "college": "College of Design", "degree_type": "Bachelor of Science"},
    ]

def create_sample_courses():
    """Create sample GT courses with realistic data"""
    courses = [
        # Computer Science courses
        Course("Introduction to Computing", "CS 1301", 3, average_gpa=3.1, department="CS", description="Introduction to computing principles"),
        Course("Introduction to Object-Oriented Programming", "CS 1331", 3, average_gpa=2.8, department="CS", description="Object-oriented programming concepts"),
        Course("Data Structures and Algorithms", "CS 1332", 3, average_gpa=2.9, department="CS", prerequisites=["CS 1331"], description="Data structures and algorithm analysis"),
        Course("Introduction to Discrete Mathematics", "CS 2050", 3, average_gpa=2.7, department="CS", description="Discrete mathematics for computer science"),
        Course("Computer Organization and Programming", "CS 2110", 3, average_gpa=2.6, department="CS", prerequisites=["CS 1331"], description="Computer organization and assembly language"),
        Course("Systems and Networks", "CS 2200", 3, average_gpa=2.8, department="CS", prerequisites=["CS 2110"], description="Operating systems and computer networks"),
        Course("Objects and Design", "CS 2340", 3, average_gpa=3.0, department="CS", prerequisites=["CS 1332"], description="Software design patterns and principles"),
        Course("Design and Analysis of Algorithms", "CS 3510", 3, average_gpa=2.9, department="CS", prerequisites=["CS 1332", "CS 2050"], description="Algorithm design and analysis"),
        Course("Introduction to Artificial Intelligence", "CS 3600", 3, average_gpa=3.2, department="CS", prerequisites=["CS 1332"], description="Introduction to AI concepts"),
        Course("Computing, Society, and Professionalism", "CS 4001", 3, average_gpa=3.4, department="CS", description="Professional ethics and social impact"),
        
        # Mathematics courses
        Course("Differential Calculus", "MATH 1551", 4, average_gpa=2.8, department="MATH", description="Single variable calculus"),
        Course("Integral Calculus", "MATH 1552", 4, average_gpa=2.7, department="MATH", prerequisites=["MATH 1551"], description="Integration techniques"),
        Course("Introduction to Linear Algebra", "MATH 1553", 2, average_gpa=2.9, department="MATH", description="Linear algebra fundamentals"),
        Course("Introduction to Multivariable Calculus", "MATH 2550", 4, average_gpa=2.6, department="MATH", prerequisites=["MATH 1552"], description="Multivariable calculus"),
        Course("Applied Combinatorics", "MATH 3012", 3, average_gpa=2.8, department="MATH", prerequisites=["MATH 1553"], description="Combinatorial mathematics"),
        Course("Introduction to Probability and Statistics", "MATH 3215", 3, average_gpa=2.9, department="MATH", prerequisites=["MATH 2550"], description="Probability and statistics"),
        
        # Physics courses
        Course("Introductory Physics I", "PHYS 2211", 4, average_gpa=2.7, department="PHYS", description="Mechanics and thermodynamics"),
        Course("Introductory Physics II", "PHYS 2212", 4, average_gpa=2.6, department="PHYS", prerequisites=["PHYS 2211"], description="Electricity and magnetism"),
        
        # Mechanical Engineering courses
        Course("Introduction to Engineering Graphics and Visualization", "ME 1770", 2, average_gpa=3.1, department="ME", description="Engineering graphics and CAD"),
        Course("Computing Techniques", "ME 2016", 3, average_gpa=2.9, department="ME", description="Computing methods for engineers"),
        Course("Creative Decisions and Design", "ME 2110", 3, average_gpa=3.0, department="ME", description="Engineering design process"),
        Course("Dynamics of Rigid Bodies", "ME 2202", 3, average_gpa=2.8, department="ME", prerequisites=["MATH 2550"], description="Rigid body dynamics"),
        Course("System Dynamics and Vibrations", "ME 3017", 3, average_gpa=2.7, department="ME", prerequisites=["ME 2202"], description="System dynamics analysis"),
        Course("Thermodynamics", "ME 3057", 3, average_gpa=2.6, department="ME", prerequisites=["PHYS 2211"], description="Thermodynamic principles"),
        Course("Heat Transfer", "ME 3124", 3, average_gpa=2.8, department="ME", prerequisites=["ME 3057"], description="Heat transfer mechanisms"),
        Course("Machine Design", "ME 3180", 3, average_gpa=2.9, department="ME", prerequisites=["ME 2202"], description="Machine design principles"),
        Course("Fluid Mechanics", "ME 3340", 3, average_gpa=2.7, department="ME", prerequisites=["MATH 2550"], description="Fluid mechanics fundamentals"),
        Course("Control Systems Design", "ME 4056", 3, average_gpa=2.8, department="ME", prerequisites=["ME 3017"], description="Control system design"),
        Course("Manufacturing Processes and Engineering", "ME 4210", 3, average_gpa=3.0, department="ME", description="Manufacturing processes"),
        
        # Business courses
        Course("Introduction to Business", "MGT 1101", 3, average_gpa=3.2, department="MGT", description="Business fundamentals"),
        Course("Legal Environment of Business", "MGT 2106", 3, average_gpa=3.1, department="MGT", description="Business law"),
        Course("Financial and Managerial Accounting", "MGT 3000", 3, average_gpa=2.9, department="MGT", description="Accounting principles"),
        Course("Organizational Behavior", "MGT 3101", 3, average_gpa=3.0, department="MGT", description="Organizational behavior"),
        Course("Principles of Management", "MGT 3102", 3, average_gpa=3.1, department="MGT", description="Management principles"),
        Course("Principles of Marketing", "MGT 3103", 3, average_gpa=3.0, department="MGT", description="Marketing principles"),
        Course("Principles of Finance", "MGT 3104", 3, average_gpa=2.8, department="MGT", prerequisites=["MGT 3000"], description="Financial management"),
        Course("Operations Management", "MGT 3105", 3, average_gpa=2.9, department="MGT", description="Operations management"),
        Course("Strategic Management", "MGT 3106", 3, average_gpa=3.1, department="MGT", prerequisites=["MGT 3102"], description="Strategic management"),
        
        # Economics courses
        Course("Economics and Policy", "ECON 2100", 3, average_gpa=3.0, department="ECON", description="Economic principles and policy"),
        Course("Principles of Macroeconomics", "ECON 2105", 3, average_gpa=2.9, department="ECON", description="Macroeconomic principles"),
        Course("Principles of Microeconomics", "ECON 2106", 3, average_gpa=2.8, department="ECON", description="Microeconomic principles"),
        
        # English courses
        Course("Technical Writing", "ENGL 1101", 3, average_gpa=3.2, department="ENGL", description="Technical communication"),
        Course("English Composition", "ENGL 1102", 3, average_gpa=3.1, department="ENGL", description="Academic writing"),
        
        # Chemistry courses
        Course("General Chemistry I", "CHEM 1211K", 4, average_gpa=2.7, department="CHEM", description="General chemistry principles"),
        Course("General Chemistry II", "CHEM 1212K", 4, average_gpa=2.6, department="CHEM", prerequisites=["CHEM 1211K"], description="Advanced chemistry principles"),
        
        # Biology courses
        Course("Introductory Biology I", "BIOL 1510", 4, average_gpa=2.8, department="BIOL", description="Cell biology and genetics"),
        Course("Introductory Biology II", "BIOL 1520", 4, average_gpa=2.7, department="BIOL", prerequisites=["BIOL 1510"], description="Evolution and ecology"),
        
        # Psychology courses
        Course("Introduction to Psychology", "PSYC 1101", 3, average_gpa=3.0, department="PSYC", description="Introduction to psychological principles"),
        Course("Research Methods in Psychology", "PSYC 2015", 3, average_gpa=2.9, department="PSYC", prerequisites=["PSYC 1101"], description="Psychological research methods"),
        
        # History courses
        Course("World History", "HIST 2111", 3, average_gpa=3.1, department="HIST", description="World history survey"),
        Course("American History", "HIST 2112", 3, average_gpa=3.0, department="HIST", description="American history survey"),
        
        # Philosophy courses
        Course("Introduction to Philosophy", "PHIL 1101", 3, average_gpa=3.2, department="PHIL", description="Philosophical thinking"),
        Course("Ethics", "PHIL 3100", 3, average_gpa=3.1, department="PHIL", description="Ethical theory and practice"),
        
        # Literature courses
        Course("Introduction to Literature", "LMC 1100", 3, average_gpa=3.0, department="LMC", description="Literary analysis"),
        Course("Media Studies", "LMC 2000", 3, average_gpa=3.1, department="LMC", description="Media and culture"),
    ]
    
    return courses

if __name__ == "__main__":
    populate_initial_data()

#Course Class
#Roadmap Class
#Term Class--- Roadmap class holds those terms
class Course:
    def __init__(self, course_name, course_code, credits, prerequisites=None, average_gpa=None, department=None, description=None):
        self.course_name = course_name
        self.course_code = course_code
        self.credits = credits
        self.prerequisites = prerequisites if prerequisites else []
        self.average_gpa = average_gpa
        self.department = department
        self.description = description

    def __repr__(self):
        gpa_str = f" (GPA: {self.average_gpa})" if self.average_gpa else ""
        return f"{self.course_code}: {self.course_name} ({self.credits} credits){gpa_str}"
    
class Term:
    def __init__(self, term_name):
        self.term_name = term_name
        self.courses = set() # A set only allows one of each item

    def add_course(self, course):
        self.courses.add(course)

    def remove_course(self, course):
        self.courses.discard(course)

    def __repr__(self):
        return f"{self.term_name} with courses: {self.courses}"
    
class Major:
    def __init__(self, major_name, college=None, degree_type=None, description=None):
        self.major_name = major_name
        self.college = college
        self.degree_type = degree_type
        self.description = description
        self.required_courses = []
        self.elective_courses = []

    def add_required_course(self, course):
        self.required_courses.append(course)

    def add_elective_course(self, course):
        self.elective_courses.append(course)

    def __repr__(self):
        return f"{self.major_name} ({self.college})"

class Roadmap:
    def __init__(self, roadmap_name, major=None):
        self.roadmap_name = roadmap_name
        self.major = major
        self.terms = []
        self.total_credits = 0
        self.estimated_gpa = None

    def add_term(self, term):
        self.terms.append(term)
        self.total_credits += sum(course.credits for course in term.courses if course.credits)

    def remove_term(self, term):
        if term in self.terms:
            self.terms.remove(term)
            self.total_credits -= sum(course.credits for course in term.courses if course.credits)

    def calculate_estimated_gpa(self):
        """Calculate estimated GPA based on course average GPAs"""
        if not self.terms:
            return None
        
        total_weighted_gpa = 0
        total_credits = 0
        
        for term in self.terms:
            for course in term.courses:
                if course.average_gpa and course.credits:
                    total_weighted_gpa += course.average_gpa * course.credits
                    total_credits += course.credits
        
        if total_credits > 0:
            self.estimated_gpa = total_weighted_gpa / total_credits
            return self.estimated_gpa
        
        return None

    def __repr__(self):
        gpa_str = f" (Est. GPA: {self.estimated_gpa:.2f})" if self.estimated_gpa else ""
        return f"Roadmap: {self.roadmap_name} ({self.total_credits} credits){gpa_str}"
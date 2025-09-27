#Course Class
#Roadmap Class
#Term Class--- Roadmap class holds those terms
class Course:
    def __init__(self, course_name, course_code, credits, prerequisites=None):
        self.course_name = course_name
        self.course_code = course_code
        self.credits = credits
        self.prerequisites = prerequisites if prerequisites else []

    def __repr__(self):
        return f"{self.course_code}: {self.course_name} ({self.credits} credits)"
    
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
    
class Roadmap:
    def __init__(self, roadmap_name):
        self.roadmap_name = roadmap_name
        self.terms = []

    def add_term(self, term):
        self.terms.append(term)

    def remove_term(self, term):
        self.terms.remove(term)

    def __repr__(self):
        return f"Roadmap: {self.roadmap_name} with terms: {self.terms}"
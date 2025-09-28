from typing import List, Dict, Set
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpStatus

# Import the dataclasses from the separate models file
from models import Course, Roadmap, Term

def build_roadmap(
    courses: List[Course],
    num_terms: int,
    preset_roadmap: Dict[int, List[Course]] = None,
    max_hours: int = 18,
    min_hours: int = 12,
    allow_one_parttime: bool = True
) -> Roadmap:
    """
    Generates a Roadmap that satisfies constraints and balances GPA difficulty
    using a linear programming model.

    Args:
        courses: A list of all Course objects to be scheduled.
        num_terms: The total number of terms (T) to schedule courses into.
        preset_roadmap: A dictionary mapping term index (1-based) to a list of
                        courses that must be in that term.
        max_hours: The maximum credit hours allowed per term.
        min_hours: The minimum credit hours required per term.
        allow_one_parttime: If True, allows at most one term to be below min_hours.

    Returns:
        A Roadmap object containing the optimized schedule. Returns an empty
        Roadmap if no optimal solution is found.
    """
    # --- 1. Initialization ---
    problem = LpProblem("Course_Scheduling", LpMinimize)
    course_map = {c.id: c for c in courses}
    course_ids = list(course_map.keys())
    term_indices = list(range(1, num_terms + 1))

    # --- 2. Decision Variables ---
    # x_c,t = 1 if course c is in term t, 0 otherwise
    x = LpVariable.dicts("x", (course_ids, term_indices), cat='Binary')

    # --- 3. Objective Function (GPA-Balancing Minimax) ---
    # M represents the maximum difficulty score across all terms
    M = LpVariable("M", lowBound=0, cat='Continuous', doc="Max Term Difficulty")

    # Objective: Minimize M
    problem.setObjective(M)

    # Add constraints to define M: d_t <= M for all t
    for t in term_indices:
        term_difficulty = lpSum(c.avg_gpa * x[c.id][t] for c in courses)
        problem += term_difficulty <= M, f"Max_Difficulty_Constraint_Term_{t}"

    # --- 4. Constraints ---

    # a) Each course must be taken exactly once
    for c_id in course_ids:
        problem += lpSum(x[c_id][t] for t in term_indices) == 1, f"Course_Once_{c_id}"

    # b) Prerequisite constraints: p must be before c
    for c in courses:
        for p_id in c.prereqs:
            if p_id in course_map: # Ensure prereq is in the list of courses to schedule
                for t in term_indices[1:]: # Prereqs matter from term 2 onwards
                    sum_of_prereqs_before_t = lpSum(x[p_id][t_prime] for t_prime in range(1, t))
                    problem += sum_of_prereqs_before_t >= x[c.id][t], f"Prereq_{p_id}_before_{c.id}_at_term_{t}"

    # c) Max credit hours per term
    for t in term_indices:
        problem += lpSum(c.hours * x[c.id][t] for c in courses) <= max_hours, f"Max_Hours_Term_{t}"

    # d) Min credit hours per term (with potential for one exception)
    if allow_one_parttime:
        # s_t = 1 if term t is part-time (below min_hours)
        s = LpVariable.dicts("is_part_time", term_indices, cat='Binary')
        problem += lpSum(s[t] for t in term_indices) <= 1, "At_Most_One_Part_Time_Term"
        for t in term_indices:
            # The constraint is relaxed (multiplied by 0) if s_t is 1
            problem += lpSum(c.hours * x[c.id][t] for c in courses) >= min_hours * (1 - s[t]), f"Min_Hours_Term_{t}"
    else: # No exceptions allowed
        for t in term_indices:
            problem += lpSum(c.hours * x[c.id][t] for c in courses) >= min_hours, f"Min_Hours_Term_{t}"


    # e) Required course placement (locked courses)
    if preset_roadmap:
        for term_idx, locked_courses in preset_roadmap.items():
            if term_idx in term_indices:
                for course in locked_courses:
                    if course.id in course_ids:
                        problem += x[course.id][term_idx] == 1, f"Locked_{course.id}_in_Term_{term_idx}"

    # --- 5. Solve the LP Problem ---
    problem.solve()

    # --- 6. Build Roadmap from Solver Output ---
    final_roadmap = Roadmap()
    if LpStatus[problem.status] == 'Optimal':
        schedule: Dict[int, List[Course]] = {t: [] for t in term_indices}
        
        for c_id in course_ids:
            for t in term_indices:
                if x[c_id][t].varValue == 1:
                    schedule[t].append(course_map[c_id])
        
        for t_idx, course_list in schedule.items():
            final_roadmap.terms.append(Term(term_index=t_idx, courses=course_list))
    
    return final_roadmap

# --- Example of how to use this module ---
if __name__ == '__main__':
    # Define a list of courses, providing all arguments explicitly
    sample_courses = [
        Course(id="CS101", name="Intro to CS", hours=3, prereqs=set(), avg_gpa=2.8),
        Course(id="CS201", name="Data Structures", hours=4, prereqs={"CS101"}, avg_gpa=3.5),
        Course(id="CS250", name="Computer Architecture", hours=3, prereqs={"CS101"}, avg_gpa=3.8),
        Course(id="MA110", name="Calculus I", hours=4, prereqs=set(), avg_gpa=2.5),
        Course(id="MA210", name="Calculus II", hours=4, prereqs={"MA110"}, avg_gpa=3.2),
        Course(id="PH201", name="Physics I", hours=4, prereqs={"MA110"}, avg_gpa=3.0),
        Course(id="PH202", name="Physics II", hours=4, prereqs={"PH201", "MA210"}, avg_gpa=3.4),
        Course(id="EN101", name="English Composition", hours=3, prereqs=set(), avg_gpa=2.2),
        Course(id="HI101", name="World History", hours=3, prereqs=set(), avg_gpa=2.1),
        Course(id="CS350", name="Operating Systems", hours=3, prereqs={"CS201", "CS250"}, avg_gpa=4.0),
        Course(id="CS301", name="Algorithms", hours=3, prereqs={"CS201"}, avg_gpa=3.9),
        Course(id="MA300", name="Linear Algebra", hours=3, prereqs={"MA210"}, avg_gpa=3.1),
    ]

    # Generate a roadmap for 4 terms
    generated_roadmap = build_roadmap(
        courses=sample_courses,
        num_terms=4
    )

    # Print the resulting roadmap to the console
    if generated_roadmap.terms:
        generated_roadmap.print_roadmap()
    else:
        print("Could not find an optimal roadmap for the given courses and constraints.")
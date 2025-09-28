/* ---------- script.js (updated with real GT data) ---------- */

/* Real Georgia Tech majors data */
const gtMajors = {
  "College of Computing": [
    "Computer Science",
    "Computational Media", 
    "Computer Engineering"
  ],
  "College of Engineering": [
    "Aerospace Engineering",
    "Biomedical Engineering",
    "Chemical and Biomolecular Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Environmental Engineering",
    "Industrial Engineering",
    "Materials Science and Engineering",
    "Mechanical Engineering",
    "Nuclear and Radiological Engineering"
  ],
  "College of Sciences": [
    "Applied Mathematics",
    "Biology",
    "Chemistry",
    "Earth and Atmospheric Sciences",
    "Mathematics",
    "Physics",
    "Psychology"
  ],
  "Scheller College of Business": [
    "Business Administration"
  ],
  "Ivan Allen College of Liberal Arts": [
    "Applied Languages and Intercultural Studies",
    "Economics",
    "History, Technology, and Society",
    "International Affairs",
    "Literature, Media, and Communication",
    "Public Policy"
  ],
  "College of Design": [
    "Architecture",
    "Industrial Design"
  ]
};

/* Sample course data by major (will be replaced with real data from API) */
const coursesByMajor = {
  "Computer Science": [
    'CS 1301 - Introduction to Computing',
    'CS 1331 - Introduction to Object-Oriented Programming',
    'CS 1332 - Data Structures and Algorithms',
    'CS 2050 - Introduction to Discrete Mathematics',
    'CS 2110 - Computer Organization and Programming',
    'CS 2200 - Systems and Networks',
    'CS 2340 - Objects and Design',
    'CS 3510 - Design and Analysis of Algorithms',
    'CS 3600 - Introduction to Artificial Intelligence',
    'CS 4001 - Computing, Society, and Professionalism',
    'MATH 1552 - Integral Calculus',
    'MATH 1553 - Introduction to Linear Algebra',
    'MATH 2550 - Introduction to Multivariable Calculus',
    'MATH 3012 - Applied Combinatorics',
    'PHYS 2211 - Introductory Physics I',
    'PHYS 2212 - Introductory Physics II'
  ],
  "Mathematics": [
    'MATH 1551 - Differential Calculus',
    'MATH 1552 - Integral Calculus',
    'MATH 1553 - Introduction to Linear Algebra',
    'MATH 2550 - Introduction to Multivariable Calculus',
    'MATH 3012 - Applied Combinatorics',
    'MATH 3215 - Introduction to Probability and Statistics',
    'MATH 3235 - Introduction to Analysis',
    'MATH 3406 - Introduction to Differential Equations',
    'MATH 4317 - Analysis I',
    'MATH 4320 - Abstract Algebra I',
    'MATH 4330 - Complex Analysis',
    'MATH 4340 - Topology',
    'MATH 4640 - Numerical Analysis I',
    'MATH 4755 - Mathematical Statistics'
  ],
  "Mechanical Engineering": [
    'ME 1770 - Introduction to Engineering Graphics and Visualization',
    'ME 2016 - Computing Techniques',
    'ME 2110 - Creative Decisions and Design',
    'ME 2202 - Dynamics of Rigid Bodies',
    'ME 3017 - System Dynamics and Vibrations',
    'ME 3057 - Thermodynamics',
    'ME 3124 - Heat Transfer',
    'ME 3180 - Machine Design',
    'ME 3340 - Fluid Mechanics',
    'ME 3345 - Heat Transfer',
    'ME 4056 - Control Systems Design',
    'ME 4210 - Manufacturing Processes and Engineering',
    'MATH 1552 - Integral Calculus',
    'MATH 2550 - Introduction to Multivariable Calculus',
    'PHYS 2211 - Introductory Physics I',
    'PHYS 2212 - Introductory Physics II'
  ],
  "Business Administration": [
    'MGT 1101 - Introduction to Business',
    'MGT 2106 - Legal Environment of Business',
    'MGT 3000 - Financial and Managerial Accounting',
    'MGT 3101 - Organizational Behavior',
    'MGT 3102 - Principles of Management',
    'MGT 3103 - Principles of Marketing',
    'MGT 3104 - Principles of Finance',
    'MGT 3105 - Operations Management',
    'MGT 3106 - Strategic Management',
    'MGT 3107 - Business Communications',
    'MGT 3108 - Business Ethics',
    'ECON 2100 - Economics and Policy',
    'ECON 2105 - Principles of Macroeconomics',
    'ECON 2106 - Principles of Microeconomics',
    'MATH 1552 - Integral Calculus',
    'MATH 1553 - Introduction to Linear Algebra'
  ]
};

let selectedFile = null;
let selectedCourses = [];

/* ---------- Simple section navigation ---------- */
function showLanding() { hideAll(); qs('#landing-page').classList.remove('hidden'); }
function showPdfUpload() { hideAll(); qs('#pdf-upload-section').classList.remove('hidden'); }
function showManualEntry() { hideAll(); qs('#manual-entry-section').classList.remove('hidden'); }
function showLoading() { hideAll(); qs('#loading-section').classList.remove('hidden'); }
function showRoadmap() { hideAll(); qs('#roadmap-section').classList.remove('hidden'); }

function hideAll() {
  ['landing-page','pdf-upload-section','manual-entry-section','loading-section','roadmap-section']
    .forEach(id => qs('#' + id).classList.add('hidden'));
}

const qs = (s, root=document) => root.querySelector(s);

/* ---------- File upload ---------- */
const fileInput = qs('#pdf-file');
if (fileInput) {
  fileInput.addEventListener('change', e => handleFileSelect(e.target.files[0]));
}

const dropZone = qs('#drop-zone');
if (dropZone) {
  dropZone.addEventListener('dragover', e => {
    e.preventDefault();
    dropZone.style.borderColor = '#6366f1';
    dropZone.style.background = '#f0f4ff';
  });
  dropZone.addEventListener('dragleave', e => {
    e.preventDefault();
    dropZone.style.borderColor = '#a5b4fc';
    dropZone.style.background = '#f8faff';
  });
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.style.borderColor = '#a5b4fc';
    dropZone.style.background = '#f8faff';
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'application/pdf') {
      handleFileSelect(files[0]);
    }
  });
}

function handleFileSelect(file) {
  if (file && file.type === 'application/pdf') {
    selectedFile = file;
    qs('#file-name').textContent = file.name;
    qs('#file-info').classList.remove('hidden');
    const uploadBtn = qs('#upload-btn');
    if (uploadBtn) {
      uploadBtn.disabled = false;
      uploadBtn.className = 'btn btn-primary';
      uploadBtn.style.marginTop = '1.5rem';
    }
  }
}

/* ---------- Major / course selection ---------- */
const majorSelect = qs('#major-select');
if (majorSelect) {
  majorSelect.addEventListener('change', e => {
    const major = e.target.value;
    if (major) {
      populateCoursesFromAPI(major);
      qs('#course-selection').classList.remove('hidden');
    } else {
      qs('#course-selection').classList.add('hidden');
    }
    updateProcessButton();
  });
}

async function populateCoursesFromAPI(major) {
  try {
    const response = await fetch(`/api/courses/${encodeURIComponent(major)}`);
    if (!response.ok) throw new Error('Failed to fetch courses');
    
    const data = await response.json();
    const allCourses = [...data.core, ...data.elective, ...data.prerequisite];
    
    const container = qs('#course-selection .course-grid');
    container.innerHTML = '';
    
    if (allCourses.length === 0) {
      // Fallback to static data if API fails
      populateCoursesFromStatic(major);
      return;
    }
    
    allCourses.forEach((course, index) => {
      const courseDiv = document.createElement('div');
      courseDiv.className = 'course-item';
      const gpaText = course.average_gpa ? ` (GPA: ${course.average_gpa})` : '';
      courseDiv.innerHTML = `
        <input type="checkbox" id="course-${index}" value="${course.course_code}" class="course-checkbox">
        <label for="course-${index}" class="course-label">
          ${course.course_code} - ${course.course_name}${gpaText}
        </label>
      `;
      container.appendChild(courseDiv);
    });

    container.addEventListener('change', () => updateSelectedCourses(), { once: true });
  } catch (error) {
    console.error('Error fetching courses:', error);
    // Fallback to static data
    populateCoursesFromStatic(major);
  }
}

function populateCoursesFromStatic(major) {
  const courses = coursesByMajor[major] || [];
  const container = qs('#course-selection .course-grid');
  container.innerHTML = '';
  courses.forEach((course, index) => {
    const courseDiv = document.createElement('div');
    courseDiv.className = 'course-item';
    courseDiv.innerHTML = `
      <input type="checkbox" id="course-${index}" value="${course}" class="course-checkbox">
      <label for="course-${index}" class="course-label">${course}</label>
    `;
    container.appendChild(courseDiv);
  });

  container.addEventListener('change', () => updateSelectedCourses(), { once: true });
}

function updateSelectedCourses() {
  const checked = document.querySelectorAll('#course-selection input[type="checkbox"]:checked');
  selectedCourses = Array.from(checked).map(cb => cb.value);
  qs('#selected-count').textContent = selectedCourses.length;
  updateProcessButton();
}

function updateProcessButton() {
  const major = qs('#major-select')?.value;
  const hasSelection = major && selectedCourses.length > 0;
  const btn = qs('#process-manual-btn');
  if (!btn) return;
  btn.disabled = !hasSelection;
  btn.className = hasSelection ? 'btn btn-secondary' : 'btn btn-disabled';
}

/* ---------- API calls (single backend route: /api/roadmap) ---------- */
async function processPdf() {
  if (!selectedFile) return;
  showLoading();

  const formData = new FormData();
  formData.append('transcript', selectedFile);
  formData.append('source', 'pdf'); // let backend branch if needed

  try {
    const res = await fetch('/api/roadmap', { method: 'POST', body: formData });
    if (!res.ok) throw new Error('Failed to process transcript');
    const raw = await res.json();
    displayRoadmap(normalizeRoadmap(raw));
  } catch (err) {
    console.error(err);
    setTimeout(() => displayRoadmap(getSampleRoadmap()), 1000);
  }
}

async function processManualEntry() {
  const major = qs('#major-select')?.value;
  if (!major || selectedCourses.length === 0) return;

  showLoading();

  const payload = { source: 'manual', major, completed_courses: selectedCourses };

  try {
    const res = await fetch('/api/roadmap', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to process manual entry');
    const raw = await res.json();
    displayRoadmap(normalizeRoadmap(raw));
  } catch (err) {
    console.error(err);
    setTimeout(() => displayRoadmap(getSampleRoadmap()), 1000);
  }
}

/* ---------- Normalization (class-shaped -> UI-shaped) ---------- */
function normalizeRoadmap(raw) {
  // If already UI-shaped, ensure summary and return
  if (raw && Array.isArray(raw.terms) && raw.terms[0]?.courses && ('code' in (raw.terms[0].courses[0] || {}))) {
    return {
      terms: raw.terms.map(t => ({
        name: t.name,
        credits: t.credits ?? sumCredits(t.courses),
        courses: t.courses
      })),
      summary: raw.summary ?? buildSummary(raw.terms)
    };
  }

  // Convert from Course/Term/Roadmap object JSON
  const terms = (raw?.terms || []).map(t => {
    // Courses may arrive as list or set-like (backend should convert sets to lists)
    const list = Array.isArray(t.courses) ? t.courses : Array.from(t.courses || []);
    const courses = list.map(c => ({
      code: c.course_code ?? c.code ?? '',
      name: c.course_name ?? c.name ?? '',
      credits: Number(c.credits ?? 0)
    }));
    return {
      name: t.term_name ?? t.name ?? 'Term',
      credits: sumCredits(courses),
      courses
    };
  });

  return { terms, summary: buildSummary(terms) };
}

function sumCredits(courses) {
  return (courses || []).reduce((acc, c) => acc + (Number(c.credits) || 0), 0);
}

function buildSummary(terms) {
  const credits = (terms || []).reduce((acc, t) => acc + (Number(t.credits) || 0), 0);
  return {
    terms_remaining: terms?.length ?? 0,
    credits_remaining: credits,
    graduation_date: 'TBD'
  };
}

/* ---------- UI rendering ---------- */
function displayRoadmap(roadmapData) {
  showRoadmap();

  const timeline = qs('#roadmap-timeline');
  timeline.innerHTML = '';

  (roadmapData.terms || []).forEach((term, index) => {
    const termDiv = document.createElement('div');
    termDiv.className = 'timeline-item animate-slide-up';
    termDiv.style.animationDelay = `${index * 0.1}s`;

    termDiv.innerHTML = `
      <div class="timeline-header">
        <div class="timeline-number">${index + 1}</div>
        <div class="timeline-info">
          <h3>${escapeHtml(term.name)}</h3>
          <p>${Number(term.credits) || 0} Credits</p>
        </div>
      </div>
      <div class="course-grid-timeline">
        ${(term.courses || []).map(c => `
          <div class="course-card">
            <div class="course-code">${escapeHtml(c.code)}</div>
            <div class="course-name">${escapeHtml(c.name)}</div>
            <div class="course-credits">${Number(c.credits) || 0} credits</div>
            ${c.average_gpa ? `<div class="course-gpa">Avg GPA: ${Number(c.average_gpa).toFixed(2)}</div>` : ''}
          </div>
        `).join('')}
      </div>
    `;
    timeline.appendChild(termDiv);
  });

  qs('#total-terms').textContent = roadmapData.summary?.terms_remaining ?? 0;
  qs('#total-credits').textContent = roadmapData.summary?.credits_remaining ?? 0;
  qs('#graduation-date').textContent = roadmapData.summary?.graduation_date ?? 'TBD';
  
  // Add estimated GPA if available
  if (roadmapData.summary?.estimated_gpa) {
    const gpaElement = document.createElement('div');
    gpaElement.className = 'stat-item';
    gpaElement.innerHTML = `
      <div class="stat-number">${roadmapData.summary.estimated_gpa.toFixed(2)}</div>
      <div class="stat-label">Estimated GPA</div>
    `;
    qs('.summary-stats').appendChild(gpaElement);
  }
}

/* ---------- Demo fallback ---------- */
function getSampleRoadmap() {
  return {
    terms: [
      {
        name: "Fall 2025",
        credits: 15,
        courses: [
          { code: "CS 301", name: "Database Systems", credits: 3 },
          { code: "CS 302", name: "Software Engineering", credits: 3 },
          { code: "MATH 301", name: "Statistics", credits: 3 },
          { code: "ENG 201", name: "Technical Writing", credits: 3 },
          { code: "PHYS 101", name: "Physics I", credits: 3 }
        ]
      },
      {
        name: "Spring 2026",
        credits: 15,
        courses: [
          { code: "CS 401", name: "Operating Systems", credits: 3 },
          { code: "CS 402", name: "Computer Networks", credits: 3 },
          { code: "CS 403", name: "Machine Learning", credits: 3 },
          { code: "PHIL 101", name: "Ethics", credits: 3 },
          { code: "ART 101", name: "Digital Art", credits: 3 }
        ]
      },
      {
        name: "Fall 2026",
        credits: 12,
        courses: [
          { code: "CS 499", name: "Senior Capstone", credits: 3 },
          { code: "CS 451", name: "Advanced Algorithms", credits: 3 },
          { code: "BUS 301", name: "Entrepreneurship", credits: 3 },
          { code: "SOC 201", name: "Technology & Society", credits: 3 }
        ]
      }
    ],
    summary: { terms_remaining: 3, credits_remaining: 42, graduation_date: "Fall 2026" }
  };
}

/* ---------- tiny helper ---------- */
function escapeHtml(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

/* Optional: expose functions to buttons if needed */
window.processPdf = processPdf;
window.processManualEntry = processManualEntry;
window.showLanding = showLanding;
window.showPdfUpload = showPdfUpload;
window.showManualEntry = showManualEntry;

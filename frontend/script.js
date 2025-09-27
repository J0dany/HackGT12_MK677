/* ---------- script.js (drop-in replacement) ---------- */

/* Sample course data by major (placeholder) */
const coursesByMajor = {
  computer_science: [
    'CS 101 - Intro to Programming',
    'CS 102 - Data Structures',
    'CS 201 - Algorithms',
    'CS 202 - Computer Organization',
    'CS 301 - Database Systems',
    'CS 302 - Software Engineering',
    'CS 401 - Operating Systems',
    'CS 402 - Computer Networks',
    'MATH 101 - Calculus I',
    'MATH 102 - Calculus II',
    'MATH 201 - Linear Algebra',
    'MATH 202 - Discrete Mathematics'
  ],
  mathematics: [
    'MATH 101 - Calculus I',
    'MATH 102 - Calculus II',
    'MATH 201 - Calculus III',
    'MATH 202 - Linear Algebra',
    'MATH 301 - Real Analysis',
    'MATH 302 - Abstract Algebra',
    'MATH 401 - Complex Analysis',
    'MATH 402 - Topology',
    'STAT 201 - Statistics',
    'STAT 301 - Probability Theory'
  ],
  engineering: [
    'ENG 101 - Engineering Fundamentals',
    'ENG 102 - Engineering Design',
    'ENG 201 - Mechanics',
    'ENG 202 - Thermodynamics',
    'ENG 301 - Circuit Analysis',
    'ENG 302 - Materials Science',
    'MATH 101 - Calculus I',
    'MATH 102 - Calculus II',
    'PHYS 101 - Physics I',
    'PHYS 102 - Physics II'
  ],
  business: [
    'BUS 101 - Business Fundamentals',
    'BUS 102 - Accounting I',
    'BUS 201 - Marketing',
    'BUS 202 - Finance',
    'BUS 301 - Management',
    'BUS 302 - Operations',
    'BUS 401 - Strategy',
    'BUS 402 - Leadership',
    'ECON 101 - Microeconomics',
    'ECON 102 - Macroeconomics'
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
      populateCourses(major);
      qs('#course-selection').classList.remove('hidden');
    } else {
      qs('#course-selection').classList.add('hidden');
    }
    updateProcessButton();
  });
}

function populateCourses(major) {
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
          </div>
        `).join('')}
      </div>
    `;
    timeline.appendChild(termDiv);
  });

  qs('#total-terms').textContent = roadmapData.summary?.terms_remaining ?? 0;
  qs('#total-credits').textContent = roadmapData.summary?.credits_remaining ?? 0;
  qs('#graduation-date').textContent = roadmapData.summary?.graduation_date ?? 'TBD';
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

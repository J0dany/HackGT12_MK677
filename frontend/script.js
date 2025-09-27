// Sample course data by major
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

// Page navigation functions
function showLanding() {
    hideAllSections();
    document.getElementById('landing-page').classList.remove('hidden');
}

function showPdfUpload() {
    hideAllSections();
    document.getElementById('pdf-upload-section').classList.remove('hidden');
}

function showManualEntry() {
    hideAllSections();
    document.getElementById('manual-entry-section').classList.remove('hidden');
}

function showLoading() {
    hideAllSections();
    document.getElementById('loading-section').classList.remove('hidden');
}

function showRoadmap() {
    hideAllSections();
    document.getElementById('roadmap-section').classList.remove('hidden');
}

function hideAllSections() {
    const sections = ['landing-page', 'pdf-upload-section', 'manual-entry-section', 'loading-section', 'roadmap-section'];
    sections.forEach(id => {
        document.getElementById(id).classList.add('hidden');
    });
}

// File upload handling
document.getElementById('pdf-file').addEventListener('change', function(e) {
    handleFileSelect(e.target.files[0]);
});

// Drag and drop handling
const dropZone = document.getElementById('drop-zone');
dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    dropZone.style.borderColor = '#6366f1';
    dropZone.style.background = '#f0f4ff';
});

dropZone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    dropZone.style.borderColor = '#a5b4fc';
    dropZone.style.background = '#f8faff';
});

dropZone.addEventListener('drop', function(e) {
    e.preventDefault();
    dropZone.style.borderColor = '#a5b4fc';
    dropZone.style.background = '#f8faff';
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'application/pdf') {
        handleFileSelect(files[0]);
    }
});

function handleFileSelect(file) {
    if (file && file.type === 'application/pdf') {
        selectedFile = file;
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('file-info').classList.remove('hidden');
        const uploadBtn = document.getElementById('upload-btn');
        uploadBtn.disabled = false;
        uploadBtn.className = 'btn btn-primary';
        uploadBtn.style.marginTop = '1.5rem';
    }
}

// Major selection handling
document.getElementById('major-select').addEventListener('change', function(e) {
    const major = e.target.value;
    if (major) {
        populateCourses(major);
        document.getElementById('course-selection').classList.remove('hidden');
        updateProcessButton();
    } else {
        document.getElementById('course-selection').classList.add('hidden');
        updateProcessButton();
    }
});

function populateCourses(major) {
    const courses = coursesByMajor[major] || [];
    const container = document.querySelector('#course-selection .course-grid');
    container.innerHTML = '';
    
    courses.forEach((course, index) => {
        const courseDiv = document.createElement('div');
        courseDiv.className = 'course-item';
        courseDiv.innerHTML = `
            <input type="checkbox" id="course-${index}" value="${course}" 
                   class="course-checkbox" onchange="updateSelectedCourses()">
            <label for="course-${index}" class="course-label">${course}</label>
        `;
        container.appendChild(courseDiv);
    });
}

function updateSelectedCourses() {
    const checkboxes = document.querySelectorAll('#course-selection input[type="checkbox"]:checked');
    selectedCourses = Array.from(checkboxes).map(cb => cb.value);
    document.getElementById('selected-count').textContent = selectedCourses.length;
    updateProcessButton();
}

function updateProcessButton() {
    const major = document.getElementById('major-select').value;
    const hasSelection = major && selectedCourses.length > 0;
    const btn = document.getElementById('process-manual-btn');
    
    if (hasSelection) {
        btn.disabled = false;
        btn.className = 'btn btn-secondary';
    } else {
        btn.disabled = true;
        btn.className = 'btn btn-disabled';
    }
}

// API calls
async function processPdf() {
    if (!selectedFile) return;
    
    showLoading();
    
    const formData = new FormData();
    formData.append('transcript', selectedFile);
    
    try {
        // Call your Flask API endpoint
        const response = await fetch('/api/upload-transcript', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const roadmapData = await response.json();
            displayRoadmap(roadmapData);
        } else {
            throw new Error('Failed to process transcript');
        }
    } catch (error) {
        console.error('Error:', error);
        // For demo purposes, show sample roadmap
        setTimeout(() => {
            displayRoadmap(getSampleRoadmap());
        }, 2000);
    }
}

async function processManualEntry() {
    const major = document.getElementById('major-select').value;
    if (!major || selectedCourses.length === 0) return;
    
    showLoading();
    
    const data = {
        major: major,
        completed_courses: selectedCourses
    };
    
    try {
        // Call your Flask API endpoint
        const response = await fetch('/api/manual-entry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const roadmapData = await response.json();
            displayRoadmap(roadmapData);
        } else {
            throw new Error('Failed to process manual entry');
        }
    } catch (error) {
        console.error('Error:', error);
        // For demo purposes, show sample roadmap
        setTimeout(() => {
            displayRoadmap(getSampleRoadmap());
        }, 2000);
    }
}

function displayRoadmap(roadmapData) {
    showRoadmap();
    
    // Populate timeline
    const timeline = document.getElementById('roadmap-timeline');
    timeline.innerHTML = '';
    
    roadmapData.terms.forEach((term, index) => {
        const termDiv = document.createElement('div');
        termDiv.className = 'timeline-item animate-slide-up';
        termDiv.style.animationDelay = `${index * 0.1}s`;
        
        termDiv.innerHTML = `
            <div class="timeline-header">
                <div class="timeline-number">${index + 1}</div>
                <div class="timeline-info">
                    <h3>${term.name}</h3>
                    <p>${term.credits} Credits</p>
                </div>
            </div>
            <div class="course-grid-timeline">
                ${term.courses.map(course => `
                    <div class="course-card">
                        <div class="course-code">${course.code}</div>
                        <div class="course-name">${course.name}</div>
                        <div class="course-credits">${course.credits} credits</div>
                    </div>
                `).join('')}
            </div>
        `;
        
        timeline.appendChild(termDiv);
    });
    
    // Update summary
    document.getElementById('total-terms').textContent = roadmapData.summary.terms_remaining;
    document.getElementById('total-credits').textContent = roadmapData.summary.credits_remaining;
    document.getElementById('graduation-date').textContent = roadmapData.summary.graduation_date;
}

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
        summary: {
            terms_remaining: 3,
            credits_remaining: 42,
            graduation_date: "Fall 2026"
        }
    };
}
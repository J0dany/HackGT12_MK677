# Georgia Tech Academic Roadmap Optimizer

An AI-powered academic planning tool that helps Georgia Tech students create personalized graduation roadmaps using real course data and GPA information.

## Features

- **Real GT Data**: Uses actual Georgia Tech courses, majors, and average GPAs
- **PDF Transcript Parsing**: Automatically extracts completed courses from DegreeWorks PDFs
- **Manual Course Selection**: Select your major and completed courses manually
- **GPA Integration**: Shows average GPAs for courses and estimates overall GPA
- **Smart Roadmap Generation**: Creates optimized semester-by-semester plans
- **Beautiful UI**: Modern, responsive interface with smooth animations

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

Run the database population script to add GT majors and sample courses:

```bash
python populate_database.py
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── populate_database.py            # Database initialization script
├── Models/
│   └── models.py                   # Data models (Course, Major, Roadmap, Term)
├── services/
│   └── database_service.py         # Database operations
├── scraper/
│   └── gt_scraper.py              # Web scraper for GT data
├── degreeworks/
│   ├── main.py                    # DegreeWorks API
│   └── routes/
│       ├── parser.py              # PDF parsing logic
│       └── upload.py              # File upload handling
└── frontend/
    ├── index.html                 # Main UI
    ├── styles.css                 # Styling
    └── script.js                  # Frontend logic
```

## API Endpoints

- `GET /` - Main application interface
- `POST /api/roadmap` - Generate roadmap from PDF or manual entry
- `GET /api/majors` - Get all GT majors
- `GET /api/courses/<major_name>` - Get courses for a specific major
- `GET /api/courses/search/<query>` - Search courses
- `GET /api/departments` - Get all departments
- `GET /api/health` - Health check

## Data Sources

### Real GT Majors
The application includes all official Georgia Tech undergraduate majors organized by college:

- **College of Computing**: Computer Science, Computational Media, Computer Engineering
- **College of Engineering**: Aerospace, Biomedical, Chemical, Civil, Electrical, Environmental, Industrial, Materials Science, Mechanical, Nuclear Engineering
- **College of Sciences**: Applied Mathematics, Biology, Chemistry, Earth and Atmospheric Sciences, Mathematics, Physics, Psychology
- **Scheller College of Business**: Business Administration
- **Ivan Allen College of Liberal Arts**: Applied Languages, Economics, History/Technology/Society, International Affairs, Literature/Media/Communication, Public Policy
- **College of Design**: Architecture, Industrial Design

### Course Data
Each course includes:
- Course code and name
- Credit hours
- Average GPA (when available)
- Department
- Description
- Prerequisites

## Web Scraping

The `gt_scraper.py` module includes functionality to scrape real course data from Georgia Tech's Course Critique website. This includes:

- Course information and descriptions
- Average GPAs
- Prerequisites
- Department classifications

**Note**: Always respect website terms of service and implement appropriate rate limiting when scraping.

## Usage

### PDF Upload Method
1. Upload your DegreeWorks PDF transcript
2. The system automatically parses completed courses
3. Generate an optimized roadmap based on remaining requirements

### Manual Entry Method
1. Select your major from the dropdown
2. Choose completed courses from the list (shows real GT courses with GPAs)
3. Generate a personalized roadmap

## Roadmap Features

- **Semester Planning**: Courses distributed across semesters
- **Credit Management**: Maintains appropriate credit loads
- **GPA Estimation**: Calculates estimated GPA based on course averages
- **Prerequisite Handling**: Considers course prerequisites
- **Visual Timeline**: Beautiful semester-by-semester display

## Database

The application uses SQLite for data storage with the following tables:

- `courses`: Course information including GPAs
- `majors`: Major information by college
- `major_courses`: Many-to-many relationship between majors and courses

## Contributing

To add new courses or update data:

1. Update the `populate_database.py` script
2. Run the script to update the database
3. The frontend will automatically use the new data

## Future Enhancements

- Real-time course availability
- Prerequisite chain optimization
- Workload balancing
- Integration with GT's official APIs
- Advanced AI-powered recommendations
- Course difficulty ratings
- Professor ratings integration

## Technical Notes

- Built with Flask (Python backend)
- SQLite database for data storage
- Beautiful Soup for web scraping
- PDF parsing with pdfplumber
- Modern CSS with animations
- Responsive design

## License

This project is for educational purposes. Please respect Georgia Tech's terms of service when using their data.

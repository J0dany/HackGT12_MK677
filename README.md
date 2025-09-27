# Rate My Semester

AI-powered semester and degree planning tool for Georgia Tech students with iOS 17+ glassmorphism design.

## 🎯 Features

- **Course Selection**: Search and select from GT OSCAR course data
- **AI Optimization**: Generate optimal semester plans based on your goals
- **Professor Ratings**: Integration with RateMyProfessor data
- **GPA Tracking**: Real-time GPA predictions and Course Critique data
- **Interactive Timeline**: Drag-and-drop course scheduling
- **Workload Analysis**: Visual workload and difficulty assessment

## 🎨 Design

Beautiful iOS 17+ inspired interface featuring:
- Glassmorphism effects with backdrop blur
- Smooth spring-based animations
- Floating glass cards and bubbles
- Georgia Tech branded color scheme
- Responsive design for all devices

## 🚀 Technology Stack

- **Frontend**: React + TypeScript + Vite
- **Styling**: TailwindCSS with custom glassmorphism utilities
- **Animations**: Framer Motion for fluid transitions
- **UI Components**: shadcn/ui with custom glass variants
- **Backend**: Mock API (ready for Flask integration)

## 🔧 Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🤖 Backend Integration

The app is designed to connect with Flask endpoints:

### API Endpoints (Ready to implement)

- `GET /api/courses` - Fetch GT OSCAR course data
- `GET /api/professors` - Fetch RateMyProfessor ratings
- `POST /api/optimize-plan` - Generate optimal semester plan
- `POST /api/parse-syllabus` - Extract assignments from syllabus PDFs

### Mock API

Currently uses mock data in `/src/lib/mockApi.ts` with realistic:
- GT course listings with prerequisites
- Professor ratings and reviews
- GPA statistics from Course Critique
- AI-generated optimization results

### Flask Backend Setup

To connect the Flask backend:

1. Replace mock functions in `mockApi.ts` with actual fetch calls
2. Set up CORS for cross-origin requests
3. Implement the four main API endpoints
4. Add authentication for user-specific plans

## 📱 Features Implementation

### Single-Page Flow
- Input section with course search and preference sliders
- Loading state with animated progress
- Results with interactive semester timeline
- Export functionality for calendar integration

### AI Optimization
- Considers GPA goals, credit limits, and difficulty preferences
- Analyzes professor ratings and workload data
- Provides intelligent course sequencing recommendations
- Generates insights about course combinations

### Data Sources
- **GT OSCAR**: Course listings, prerequisites, schedules
- **Course Critique**: Historical GPA data and difficulty ratings
- **RateMyProfessor**: Professor ratings and student reviews
- **Syllabus Parsing**: Assignment extraction for planning

## 🎓 Georgia Tech Integration

Perfect for GT students with:
- Complete CS course pathway mapping
- Math and science prerequisite tracking
- Core curriculum requirement planning
- Co-op and internship semester planning

## 📄 License

Built for educational purposes - Georgia Tech semester planning tool.
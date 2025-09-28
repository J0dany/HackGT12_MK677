#!/usr/bin/env python3
"""
Test script to verify the integration between frontend and backend
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work correctly"""
    try:
        from Models.models import Course, Major, Term, Roadmap
        print("✓ Models imported successfully")
        
        from services.database_service import GTDatabaseService
        print("✓ Database service imported successfully")
        
        from scraper.gt_scraper import GTCourseScraper
        print("✓ Scraper imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_database_service():
    """Test database service functionality"""
    try:
        from services.database_service import GTDatabaseService
        
        db_service = GTDatabaseService("gt_courses.db")  # Use actual database
        print("✓ Database service initialized")
        
        # Test getting majors
        majors = db_service.get_all_majors()
        print(f"✓ Found {len(majors)} majors in database")
        
        # Test getting departments
        departments = db_service.get_departments()
        print(f"✓ Found {len(departments)} departments")
        
        # Test getting courses
        courses = db_service.search_courses("CS")
        print(f"✓ Found {len(courses)} CS courses")
        
        return True
    except Exception as e:
        print(f"✗ Database service error: {e}")
        return False

def test_models():
    """Test model functionality"""
    try:
        from Models.models import Course, Major, Term, Roadmap
        
        # Test Course model
        course = Course("Test Course", "TEST 1001", 3, average_gpa=3.5)
        print(f"✓ Course created: {course}")
        
        # Test Major model
        major = Major("Test Major", "Test College")
        print(f"✓ Major created: {major}")
        
        # Test Term model
        term = Term("Fall 2024")
        term.add_course(course)
        print(f"✓ Term created: {term}")
        
        # Test Roadmap model
        roadmap = Roadmap("Test Roadmap", major)
        roadmap.add_term(term)
        roadmap.calculate_estimated_gpa()
        print(f"✓ Roadmap created: {roadmap}")
        
        return True
    except Exception as e:
        print(f"✗ Model error: {e}")
        return False

def test_app_imports():
    """Test if app.py can import all dependencies"""
    try:
        # This would normally be done by running the app
        import os
        from flask import Flask, request, jsonify, render_template
        from degreeworks.routes.parser import parse_degreeworks_remaining
        from Models.models import Course, Term, Roadmap, Major
        from services.database_service import GTDatabaseService
        
        print("✓ All app imports successful")
        return True
    except ImportError as e:
        print(f"✗ App import error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing GT Academic Roadmap Optimizer Integration...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Model Test", test_models),
        ("Database Service Test", test_database_service),
        ("App Import Test", test_app_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The integration is working correctly.")
        print("\nTo run the application:")
        print("1. Run: python populate_database.py")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()

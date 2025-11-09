# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import json

app = Flask(__name__)
CORS(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            is_completed BOOLEAN DEFAULT FALSE,
            project_link TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_projects INTEGER DEFAULT 365,
            completed_projects INTEGER DEFAULT 0,
            progress_percentage REAL DEFAULT 0.0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert initial progress record
    cursor.execute('INSERT OR IGNORE INTO progress (id, total_projects) VALUES (1, 365)')
    
    conn.commit()
    conn.close()

# Initialize sample data
def init_sample_data():
    categories = {
        "web": {
            "name": "🌐 Web Development",
            "projects": [
                "Portfolio Website", "Blog Platform", "Netflix Clone", "LinkedIn Clone",
                "Weather App", "Resume Builder", "Job Portal", "Restaurant Finder",
                "E-Commerce Website", "Music Player Web App", "Responsive Portfolio",
                "News Portal", "Quiz App", "Movie Explorer", "Task Tracker",
                "Online Exam Website", "Donation Platform", "Food Recipe Finder",
                "Photo Gallery", "Travel Blog", "Book Review Website",
                "Landing Page", "Event Registration Form", "Password Generator",
                "Responsive Navbar", "Multi-step Form", "Currency Converter",
                "Sticky Notes App", "Image Carousel", "Real-time Chat UI",
                "Countdown Timer", "To-do List Web", "Parallax Scrolling Site",
                "Digital Clock", "Portfolio Analytics Page", "Restaurant Menu Page",
                "Animated Login Page", "Markdown Editor", "File Upload Page",
                "E-learning Website", "Admin Dashboard", "Movie Review Page",
                "Quiz Web App", "Expense Tracker Web", "Weather Dashboard",
                "Product Landing Page", "Poll Voting Website", "Portfolio v2",
                "Dark/Light Theme Website", "E-Commerce Cart Page",
                "Login/Signup Form", "Product Review Section", "Portfolio Gallery",
                "Portfolio Resume Integration", "Survey Form", "Portfolio Contact Page",
                "Simple Portfolio Template", "Social Media Dashboard",
                "Personal Blog Website", "Image Search Website", "Feedback Form"
            ]
        },
        "app": {
            "name": "📱 App Development",
            "projects": [
                "Expense Tracker App", "Chat App", "News App", "E-Learning App",
                "Food Delivery App", "Fitness Tracker", "Notes App", "BMI Calculator",
                "Flashcards App", "Travel Planner App", "Quiz App", "Weather App",
                "Music Player App", "Calendar App", "Habit Tracker",
                "Recipe App", "Quotes App", "To-Do List App", "Reminder App",
                "Currency Converter App", "Photo Editor App", "Video Player App",
                "PDF Reader App", "AI Chatbot App", "Voice Assistant App",
                "Meditation App", "Workout Planner", "Grocery List App",
                "Expense Splitter", "Timer App", "Stopwatch App",
                "Dictionary App", "Translator App", "QR Scanner App",
                "Wallpaper App", "Note Reminder", "Online Exam App",
                "Shopping App UI", "Book Reader App", "Portfolio App",
                "Social Media Feed App", "Login/Register App", "Fitness Planner",
                "AI Study Assistant", "Budget Manager", "Language Learning App",
                "Music Recommendation App", "AI Resume Builder", "Portfolio Showcase App",
                "Expense Dashboard", "Virtual Study Room App", "Food Menu App",
                "AI Fitness Coach", "Voice Memo App", "Planner App",
                "Pet Care App", "Chat AI App", "Real-time Poll App",
                "Flash Notes App", "Mental Health Journal", "Daily Habit App"
            ]
        },
        "python": {
            "name": "🐍 Python Development",
            "projects": [
                "File Organizer", "PDF Merger", "Email Sender", "QR Code Generator",
                "URL Shortener", "Clipboard Manager", "Voice Assistant", "YouTube Downloader",
                "System Monitor", "Weather CLI App", "Password Generator", "Image Converter",
                "File Encryptor", "Folder Sync Tool", "Expense Tracker CLI",
                "CSV Merger", "Excel Report Generator", "Invoice Creator",
                "PDF Splitter", "File Renamer", "Text to Speech",
                "Speech to Text", "Screen Recorder", "Web Scraper",
                "News Scraper", "Automation Bot", "Instagram Bot",
                "WhatsApp Messenger", "Weather Alert Bot", "Clipboard Logger",
                "Timer App CLI", "Task Reminder CLI", "Data Backup Script",
                "Log Analyzer", "JSON Formatter", "System Cleanup Script",
                "Duplicate File Remover", "Python Notes App", "File Compression Tool",
                "IP Tracker", "Stock Price Tracker", "Currency Rate Tracker",
                "Image Downloader", "PDF Password Protector", "File Organizer 2.0",
                "AI Text Generator CLI", "Markdown to HTML Converter",
                "CSV Formatter", "PDF Merger Pro", "File Sync CLI",
                "Expense Report Tool", "AI Prompt Saver", "CLI Todo App",
                "Data Sorter", "Terminal Weather", "Text File Cleaner",
                "Screenshot Tool", "Clipboard Utility", "Local Chatbot CLI",
                "CLI Password Vault"
            ]
        },
        "ml": {
            "name": "🤖 Machine Learning / AI",
            "projects": [
                "Fake News Detector", "Spam Mail Classifier", "Movie Recommendation System",
                "Diabetes Prediction", "House Price Prediction", "Face Emotion Detector",
                "ChatGPT Assistant", "Plant Disease Classifier", "Image Caption Generator",
                "Text Summarizer", "Resume Screener", "Car Price Predictor",
                "Customer Segmentation", "Stock Price Prediction", "Sentiment Analyzer",
                "Language Translator", "Speech Emotion Recognizer", "Video Caption Generator",
                "Voice Command Recognition", "AI Text Generator", "Music Genre Classification",
                "Air Quality Prediction", "Crop Recommendation System",
                "Sign Language Recognition", "AI Code Helper", "AI Tutor Chatbot",
                "Job Recommendation System", "AI Interview Bot", "AI Email Classifier",
                "PDF Q&A Bot", "AI Content Rewriter", "Chatbot for Learning",
                "AI Resume Ranker", "AI Course Recommender", "Fake Profile Detector",
                "Emotion Detection App", "Spam Detector Web", "AI Health Assistant",
                "AI Virtual Assistant", "Speech Translator", "AI Music Composer",
                "AI Study Planner", "AI Notes Generator", "AI News Summarizer",
                "AI Legal Document Parser", "AI Quiz Generator", "AI Research Summarizer",
                "AI Review Classifier", "AI Finance Predictor", "AI Stock Recommender",
                "AI Travel Planner", "AI Tutor App", "AI Assistant App",
                "AI Chat Dashboard", "AI Blog Writer", "AI Emotion Classifier",
                "AI PDF Reader", "AI Document Summarizer", "AI Meeting Summarizer",
                "AI Voice Chatbot", "AI Text Analyzer", "AI Translator App"
            ]
        },
        "data": {
            "name": "📊 Data Science",
            "projects": [
                "IPL Data Analysis", "COVID Data Tracker", "E-commerce Dashboard",
                "Crime Data Visualization", "Customer Segmentation", "Stock Market Analysis",
                "Social Media Analytics", "Sentiment Analysis Dashboard", "Survey Insights App",
                "Startup Growth Dashboard", "Population Data Visualization", "Income Distribution Analysis",
                "Education Stats Dashboard", "Weather Trend Analysis", "Poll Result Dashboard",
                "Energy Consumption Report", "Employment Trends Visualization",
                "Healthcare Analytics", "Retail Sales Analysis", "YouTube Channel Insights",
                "Financial Market Analysis", "Expense Insights Dashboard", "Startup Success Analytics",
                "Customer Feedback Analysis", "Real Estate Trends", "Climate Data Visualization",
                "Movie Rating Dashboard", "Air Quality Trends", "Sports Performance Analytics",
                "Online Sales Dashboard", "Traffic Analysis", "Election Data Insights",
                "Business Growth Trends", "Data Cleaning Automation", "Power Consumption Report",
                "Product Review Analysis", "GDP Growth Analysis", "Revenue Report Generator",
                "E-learning Performance Dashboard", "Survey Trends Visualizer",
                "Product Demand Forecast", "Income Growth Tracker", "Twitter Data Analytics",
                "Sales Comparison Report", "Streaming Data Dashboard", "Ad Campaign Insights",
                "Health Data Analytics", "Loan Analysis Report", "Music Trends Visualization",
                "Crime Trends Dashboard", "Retail Customer Analytics", "Data Distribution Visualizer",
                "Company Performance Tracker", "Portfolio Analytics", "Market Share Dashboard",
                "Industry Insights", "Public Sentiment Map", "Poll Analyzer", "Web Traffic Analyzer",
                "Survey Analyzer", "Course Completion Dashboard", "Stock Insights Tracker"
            ]
        },
        "cloud": {
            "name": "☁️ Cloud / Deployment",
            "projects": [
                "Flask App on Render", "Firebase Auth Integration", "Dockerized Flask App",
                "CI/CD with GitHub Actions", "Streamlit App Deployment", "AWS Lambda Function",
                "Cloud Firestore Integration", "Vercel React Deployment", "Docker + MongoDB Setup",
                "Serverless API Hosting", "Kubernetes Basics", "Google Cloud Deployment",
                "ML Model Deployment", "Cloud API Gateway", "CI/CD for Flutter",
                "AWS S3 File Storage", "Firebase Cloud Functions", "Render API Hosting",
                "FastAPI on Cloud", "ML Model on Hugging Face", "Heroku App Deployment",
                "Google Sheets API", "AWS DynamoDB Setup", "Cloud Monitoring Dashboard",
                "Docker Compose Project", "Firebase Hosting", "AWS CloudFront Setup",
                "Serverless Flask App", "GitHub Actions Workflow", "Docker Build Automation",
                "Deploy React with Nginx", "Vercel Next.js Deployment", "AI API Deployment",
                "AWS Rekognition Integration", "Dockerized Streamlit App", "Cloud ML Workflow",
                "Firebase Storage Management", "CI/CD for MERN Stack", "AWS CloudFormation",
                "Serverless Webhooks", "Cloud Security Monitor", "Flask + MySQL on Cloud",
                "Containerized Django App", "Google Colab Integration", "API Gateway Deployment",
                "AWS Batch Job", "Cloud Cost Optimizer", "Data Pipeline Setup",
                "Server Monitoring System", "API Load Testing Setup", "CI/CD API Automation",
                "GCP Storage Integration", "Azure Web App Deployment", "AWS Lambda Webhook",
                "Container Orchestration", "Serverless Model Hosting", "Firebase Push Notifications",
                "AWS Elastic Beanstalk", "GCP Pub/Sub Integration", "Realtime Cloud Dashboard",
                "AI API Scaling", "Docker Security Setup"
            ]
        }
    }
    
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    
    day_counter = 1
    for category_key, category_data in categories.items():
        for project in category_data["projects"]:
            # Check if project already exists
            cursor.execute('SELECT id FROM projects WHERE day = ?', (day_counter,))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO projects (day, title, category, description)
                    VALUES (?, ?, ?, ?)
                ''', (
                    day_counter,
                    project,
                    category_key,
                    f"Build a {project} using tools relevant to {category_data['name']}."
                ))
            day_counter += 1
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Serve the HTML content directly
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>365 Days Project Plan - Suman Krishna</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #4361ee;
                --secondary: #3a0ca3;
                --success: #4cc9f0;
                --danger: #f72585;
                --warning: #f8961e;
                --info: #4895ef;
                --dark: #2b2d42;
                --light: #f8f9fa;
                --gray: #6c757d;
                --web: #4361ee;
                --app: #7209b7;
                --python: #f72585;
                --ml: #4cc9f0;
                --data: #f8961e;
                --cloud: #2a9d8f;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: var(--dark);
                line-height: 1.6;
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            /* Header Styles */
            .header {
                text-align: center;
                padding: 40px 0;
                color: white;
                margin-bottom: 30px;
            }
            
            .header h1 {
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            .header .subtitle {
                font-size: 1.2rem;
                opacity: 0.9;
                max-width: 600px;
                margin: 0 auto;
                font-weight: 300;
            }
            
            /* Dashboard Styles */
            .dashboard {
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 30px;
                margin-bottom: 40px;
            }
            
            .stats-card {
                background: white;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
            }
            
            .progress-section {
                background: white;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            
            .progress-bar {
                height: 16px;
                background: #e9ecef;
                border-radius: 10px;
                margin: 20px 0;
                overflow: hidden;
                position: relative;
            }
            
            .progress {
                height: 100%;
                background: linear-gradient(90deg, var(--primary), var(--success));
                border-radius: 10px;
                width: 0%;
                transition: width 1s ease;
                position: relative;
            }
            
            .progress::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                background-image: linear-gradient(45deg, rgba(255,255,255,0.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0.15) 75%, transparent 75%, transparent);
                background-size: 1rem 1rem;
                animation: progress-stripes 1s linear infinite;
            }
            
            @keyframes progress-stripes {
                0% { background-position: 1rem 0; }
                100% { background-position: 0 0; }
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 25px;
            }
            
            .stat-item {
                text-align: center;
                padding: 20px;
                background: var(--light);
                border-radius: 12px;
                border-left: 4px solid var(--primary);
            }
            
            .stat-item h3 {
                font-size: 2rem;
                font-weight: 700;
                color: var(--primary);
                margin-bottom: 5px;
            }
            
            .stat-item p {
                color: var(--gray);
                font-size: 0.9rem;
                font-weight: 500;
            }
            
            /* Controls */
            .controls {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                flex-wrap: wrap;
                gap: 20px;
            }
            
            .filter-buttons {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            
            .filter-btn {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                padding: 12px 24px;
                border-radius: 50px;
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                backdrop-filter: blur(10px);
            }
            
            .filter-btn:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: translateY(-2px);
            }
            
            .filter-btn.active {
                background: white;
                color: var(--primary);
                border-color: white;
            }
            
            .search-box {
                position: relative;
                flex: 1;
                max-width: 400px;
            }
            
            .search-box input {
                width: 100%;
                padding: 14px 20px 14px 45px;
                border: none;
                border-radius: 50px;
                background: rgba(255, 255, 255, 0.9);
                font-size: 1rem;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .search-box input:focus {
                outline: none;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                transform: translateY(-2px);
            }
            
            .search-box i {
                position: absolute;
                left: 20px;
                top: 50%;
                transform: translateY(-50%);
                color: var(--gray);
            }
            
            /* Projects Grid */
            .projects-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 25px;
                margin-bottom: 50px;
            }
            
            .project-card {
                background: white;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                position: relative;
            }
            
            .project-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }
            
            .project-card.completed::before {
                content: '✓ COMPLETED';
                position: absolute;
                top: 15px;
                right: -30px;
                background: var(--success);
                color: white;
                padding: 5px 30px;
                font-size: 0.7rem;
                font-weight: 600;
                transform: rotate(45deg);
                z-index: 2;
            }
            
            .card-header {
                padding: 20px;
                color: white;
                font-weight: 600;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .card-body {
                padding: 25px;
            }
            
            .card-body h3 {
                margin-bottom: 12px;
                font-size: 1.3rem;
                color: var(--dark);
                font-weight: 600;
            }
            
            .card-body p {
                color: var(--gray);
                font-size: 0.95rem;
                margin-bottom: 20px;
                line-height: 1.5;
            }
            
            .completion-toggle {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .toggle-btn {
                padding: 12px 20px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            
            .toggle-btn:not(.completed) {
                background: var(--primary);
                color: white;
            }
            
            .toggle-btn.completed {
                background: #e9ecef;
                color: var(--gray);
                border: 1px solid #dee2e6;
            }
            
            .toggle-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .project-link {
                display: flex;
                gap: 10px;
            }
            
            .project-link input {
                flex: 1;
                padding: 12px 15px;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            }
            
            .project-link input:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
            }
            
            .project-link button {
                padding: 12px 20px;
                background: var(--success);
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                white-space: nowrap;
            }
            
            .project-link button:hover {
                background: #3aafd9;
                transform: translateY(-2px);
            }
            
            .link-display {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-top: 12px;
                padding: 12px 15px;
                background: var(--light);
                border-radius: 8px;
                font-size: 0.9rem;
                border: 1px solid #e9ecef;
            }
            
            .link-display a {
                color: var(--primary);
                text-decoration: none;
                flex: 1;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                font-weight: 500;
            }
            
            .link-display a:hover {
                text-decoration: underline;
            }
            
            .link-display button {
                background: none;
                border: none;
                color: var(--danger);
                cursor: pointer;
                font-size: 1rem;
                padding: 5px;
                border-radius: 4px;
                transition: all 0.3s ease;
            }
            
            .link-display button:hover {
                background: rgba(247, 37, 133, 0.1);
            }
            
            /* Category Colors */
            .web-dev { background: var(--web); }
            .app-dev { background: var(--app); }
            .python-dev { background: var(--python); }
            .ml-ai { background: var(--ml); }
            .data-science { background: var(--data); }
            .cloud { background: var(--cloud); }
            
            /* Footer */
            footer {
                text-align: center;
                padding: 30px;
                color: white;
                margin-top: 50px;
                border-top: 1px solid rgba(255,255,255,0.1);
            }
            
            /* Loading States */
            .loading {
                opacity: 0.6;
                pointer-events: none;
            }
            
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid var(--primary);
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                display: inline-block;
                margin-right: 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* Responsive Design */
            @media (max-width: 1024px) {
                .dashboard {
                    grid-template-columns: 1fr;
                }
                
                .projects-grid {
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                }
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2.2rem;
                }
                
                .controls {
                    flex-direction: column;
                    align-items: stretch;
                }
                
                .search-box {
                    max-width: 100%;
                }
                
                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header class="header">
                <h1>365 Days Project Plan - Suman Krishna</h1>
                <p class="subtitle">Transform your coding skills through a year-long journey of daily projects. Track progress, save links, and build an impressive portfolio.</p>
            </header>
            
            <div class="dashboard">
                <div class="stats-card">
                    <h2>Project Statistics</h2>
                    <div class="stats-grid" id="category-stats">
                        <!-- Category stats will be loaded here -->
                    </div>
                </div>
                
                <div class="progress-section">
                    <h2>Your Progress Journey</h2>
                    <div class="progress-bar">
                        <div class="progress" id="progress-bar"></div>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <h3 id="completed-count">0</h3>
                            <p>Projects Completed</p>
                        </div>
                        <div class="stat-item">
                            <h3 id="remaining-count">365</h3>
                            <p>Projects Remaining</p>
                        </div>
                        <div class="stat-item">
                            <h3 id="percentage">0%</h3>
                            <p>Overall Progress</p>
                        </div>
                        <div class="stat-item">
                            <h3 id="streak-count">0</h3>
                            <p>Current Streak</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="controls">
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="all">All Projects</button>
                    <button class="filter-btn" data-filter="web">🌐 Web Dev</button>
                    <button class="filter-btn" data-filter="app">📱 App Dev</button>
                    <button class="filter-btn" data-filter="python">🐍 Python</button>
                    <button class="filter-btn" data-filter="ml">🤖 ML/AI</button>
                    <button class="filter-btn" data-filter="data">📊 Data Science</button>
                    <button class="filter-btn" data-filter="cloud">☁️ Cloud</button>
                </div>
                
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" id="search-input" placeholder="Search projects...">
                </div>
            </div>
            
            <div class="projects-grid" id="projects-container">
                <!-- Project cards will be loaded here -->
            </div>
            
            <footer>
                <p>Built with ❤️ By Pixel 2 Predict for Suman Krishna</p>
                <p>© 2025 365 Days Project Plan | Track your progress and build amazing projects</p>
            </footer>
        </div>

        <script>
            // API Base URL
            const API_BASE = '/api';
            
            // Global state
            let currentFilter = 'all';
            let searchTerm = '';
            let projects = [];
            
            // DOM elements
            const projectsContainer = document.getElementById('projects-container');
            const filterButtons = document.querySelectorAll('.filter-btn');
            const searchInput = document.getElementById('search-input');
            const progressBar = document.getElementById('progress-bar');
            const completedCount = document.getElementById('completed-count');
            const remainingCount = document.getElementById('remaining-count');
            const percentage = document.getElementById('percentage');
            const streakCount = document.getElementById('streak-count');
            const categoryStats = document.getElementById('category-stats');
            
            // Initialize application
            async function initApp() {
                await loadProgress();
                await loadStats();
                await loadProjects();
            }
            
            // Load projects from backend
            async function loadProjects() {
                try {
                    projectsContainer.classList.add('loading');
                    
                    const params = new URLSearchParams();
                    if (currentFilter !== 'all') params.append('category', currentFilter);
                    if (searchTerm) params.append('search', searchTerm);
                    
                    const response = await fetch(`${API_BASE}/projects?${params}`);
                    projects = await response.json();
                    
                    renderProjects();
                } catch (error) {
                    console.error('Error loading projects:', error);
                    showError('Failed to load projects. Please try again.');
                } finally {
                    projectsContainer.classList.remove('loading');
                }
            }
            
            // Load progress data
            async function loadProgress() {
                try {
                    const response = await fetch(`${API_BASE}/progress`);
                    const progress = await response.json();
                    
                    updateProgressUI(progress);
                } catch (error) {
                    console.error('Error loading progress:', error);
                }
            }
            
            // Load statistics
            async function loadStats() {
                try {
                    const response = await fetch(`${API_BASE}/stats`);
                    const stats = await response.json();
                    
                    renderCategoryStats(stats.category_stats);
                } catch (error) {
                    console.error('Error loading stats:', error);
                }
            }
            
            // Update project completion status
            async function updateProjectCompletion(day, isCompleted, projectLink = '') {
                try {
                    const response = await fetch(`${API_BASE}/projects/${day}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            is_completed: isCompleted,
                            project_link: projectLink
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        await loadProgress();
                        await loadStats();
                        await loadProjects();
                    }
                } catch (error) {
                    console.error('Error updating project:', error);
                    showError('Failed to update project. Please try again.');
                }
            }
            
            // Render projects
            function renderProjects() {
                projectsContainer.innerHTML = '';
                
                if (projects.length === 0) {
                    projectsContainer.innerHTML = `
                        <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: white;">
                            <h3>No projects found</h3>
                            <p>Try adjusting your filters or search term</p>
                        </div>
                    `;
                    return;
                }
                
                projects.forEach(project => {
                    const projectCard = createProjectCard(project);
                    projectsContainer.appendChild(projectCard);
                });
            }
            
            // Create project card HTML
            function createProjectCard(project) {
                const isCompleted = project.is_completed === 1 || project.is_completed === true;
                const projectLink = project.project_link || '';
                
                const card = document.createElement('div');
                card.className = `project-card ${isCompleted ? 'completed' : ''}`;
                card.innerHTML = `
                    <div class="card-header ${project.category}-dev">
                        <span>Day ${project.day}</span>
                        <span>${project.category_name.split(' ')[0]}</span>
                    </div>
                    <div class="card-body">
                        <h3>${project.title}</h3>
                        <p>${project.description}</p>
                        <div class="completion-toggle">
                            <button class="toggle-btn ${isCompleted ? 'completed' : ''}" data-day="${project.day}">
                                ${isCompleted ? '<i class="fas fa-check"></i> Completed' : '<i class="fas fa-play"></i> Mark Complete'}
                            </button>
                            ${isCompleted ? `
                                <div class="project-link">
                                    <input type="url" 
                                           placeholder="https://your-project-link.com" 
                                           value="${projectLink}" 
                                           data-day="${project.day}" 
                                           class="link-input">
                                    <button class="save-link-btn" data-day="${project.day}">
                                        <i class="fas fa-save"></i> Save Link
                                    </button>
                                </div>
                                ${projectLink ? `
                                    <div class="link-display">
                                        <a href="${projectLink}" target="_blank" rel="noopener">
                                            <i class="fas fa-external-link-alt"></i> ${projectLink}
                                        </a>
                                        <button class="remove-link" data-day="${project.day}" title="Remove link">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>
                                ` : ''}
                            ` : ''}
                        </div>
                    </div>
                `;
                
                return card;
            }
            
            // Update progress UI
            function updateProgressUI(progress) {
                const completed = progress.completed_projects || 0;
                const total = progress.total_projects || 365;
                const progressPercent = ((completed / total) * 100).toFixed(1);
                
                progressBar.style.width = `${progressPercent}%`;
                completedCount.textContent = completed;
                remainingCount.textContent = total - completed;
                percentage.textContent = `${progressPercent}%`;
                
                // Simple streak calculation (you can enhance this)
                streakCount.textContent = Math.min(completed, 7); // Example streak
            }
            
            // Render category statistics
            function renderCategoryStats(stats) {
                const categories = {
                    'web': '🌐 Web',
                    'app': '📱 App', 
                    'python': '🐍 Python',
                    'ml': '🤖 ML/AI',
                    'data': '📊 Data',
                    'cloud': '☁️ Cloud'
                };
                
                let statsHTML = '';
                
                for (const [category, data] of Object.entries(stats)) {
                    const completed = data.completed || 0;
                    const total = data.total || 0;
                    const percent = total > 0 ? ((completed / total) * 100).toFixed(0) : 0;
                    
                    statsHTML += `
                        <div class="stat-item">
                            <h3>${percent}%</h3>
                            <p>${categories[category]} (${completed}/${total})</p>
                        </div>
                    `;
                }
                
                categoryStats.innerHTML = statsHTML;
            }
            
            // Show error message
            function showError(message) {
                // You can implement a toast notification system here
                console.error('Error:', message);
                alert(message); // Simple alert for now
            }
            
            // Event listeners
            filterButtons.forEach(button => {
                button.addEventListener('click', () => {
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    currentFilter = button.getAttribute('data-filter');
                    loadProjects();
                });
            });
            
            searchInput.addEventListener('input', debounce(() => {
                searchTerm = searchInput.value;
                loadProjects();
            }, 300));
            
            // Event delegation for dynamic elements
            document.addEventListener('click', async (e) => {
                // Toggle completion
                if (e.target.classList.contains('toggle-btn') || e.target.closest('.toggle-btn')) {
                    const btn = e.target.classList.contains('toggle-btn') ? e.target : e.target.closest('.toggle-btn');
                    const day = parseInt(btn.getAttribute('data-day'));
                    const isCurrentlyCompleted = btn.classList.contains('completed');
                    
                    await updateProjectCompletion(day, !isCurrentlyCompleted);
                }
                
                // Save link
                if (e.target.classList.contains('save-link-btn') || e.target.closest('.save-link-btn')) {
                    const btn = e.target.classList.contains('save-link-btn') ? e.target : e.target.closest('.save-link-btn');
                    const day = parseInt(btn.getAttribute('data-day'));
                    const input = document.querySelector(`.link-input[data-day="${day}"]`);
                    
                    if (input.value.trim()) {
                        await updateProjectCompletion(day, true, input.value.trim());
                    }
                }
                
                // Remove link
                if (e.target.classList.contains('remove-link') || e.target.closest('.remove-link')) {
                    const btn = e.target.classList.contains('remove-link') ? e.target : e.target.closest('.remove-link');
                    const day = parseInt(btn.getAttribute('data-day'));
                    
                    await updateProjectCompletion(day, true, '');
                }
            });
            
            // Utility function for debouncing
            function debounce(func, wait) {
                let timeout;
                return function executedFunction(...args) {
                    const later = () => {
                        clearTimeout(timeout);
                        func(...args);
                    };
                    clearTimeout(timeout);
                    timeout = setTimeout(later, wait);
                };
            }
            
            // Initialize the application
            initApp();
        </script>
    </body>
    </html>
    '''

# API Routes (keep the same as before)
@app.route('/api/projects', methods=['GET'])
def get_projects():
    conn = sqlite3.connect('projects.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = '''
        SELECT p.*, 
               CASE 
                   WHEN p.category = 'web' THEN '🌐 Web Development'
                   WHEN p.category = 'app' THEN '📱 App Development'
                   WHEN p.category = 'python' THEN '🐍 Python Development'
                   WHEN p.category = 'ml' THEN '🤖 Machine Learning / AI'
                   WHEN p.category = 'data' THEN '📊 Data Science'
                   WHEN p.category = 'cloud' THEN '☁️ Cloud / Deployment'
               END as category_name
        FROM projects p
        WHERE 1=1
    '''
    params = []
    
    if category != 'all':
        query += ' AND p.category = ?'
        params.append(category)
    
    if search:
        query += ' AND (p.title LIKE ? OR p.description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += ' ORDER BY p.day'
    
    cursor.execute(query, params)
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(projects)

@app.route('/api/projects/<int:day>', methods=['PUT'])
def update_project(day):
    data = request.get_json()
    
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE projects 
        SET is_completed = ?, project_link = ?, updated_at = CURRENT_TIMESTAMP
        WHERE day = ?
    ''', (data.get('is_completed', False), data.get('project_link', ''), day))
    
    conn.commit()
    
    # Update progress
    cursor.execute('SELECT COUNT(*) FROM projects WHERE is_completed = TRUE')
    completed_count = cursor.fetchone()[0]
    
    cursor.execute('''
        UPDATE progress 
        SET completed_projects = ?, progress_percentage = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = 1
    ''', (completed_count, (completed_count / 365) * 100))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'completed_count': completed_count})

@app.route('/api/progress', methods=['GET'])
def get_progress():
    conn = sqlite3.connect('projects.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM progress WHERE id = 1')
    progress = dict(cursor.fetchone())
    conn.close()
    
    return jsonify(progress)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    
    # Get category-wise completion stats
    cursor.execute('''
        SELECT category, COUNT(*) as total, SUM(CASE WHEN is_completed THEN 1 ELSE 0 END) as completed
        FROM projects 
        GROUP BY category
    ''')
    category_stats = {}
    for row in cursor.fetchall():
        category_stats[row[0]] = {'total': row[1], 'completed': row[2]}
    
    conn.close()
    
    return jsonify({
        'category_stats': category_stats
    })

if __name__ == '__main__':
    init_db()
    init_sample_data()
    app.run(debug=True, port=5000)
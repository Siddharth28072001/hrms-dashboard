# HRMS Lite Dashboard

A lightweight Human Resource Management System (HRMS) built with **Angular 21**, **FastAPI**, and **PostgreSQL**.  
Provides a clean, professional dashboard to manage employees and mark attendance.

## Features

- Employee table with ID, Name, Email, Department, and Actions
- Add employee via modal form (Reactive Forms)
- Mark attendance and delete employees
- Default dashboard opens on app load
- Responsive and professional UI

## Tech Stack

- **Frontend:** Angular 21, TypeScript, HTML, CSS  
- **Backend:** FastAPI (Python)  
- **Database:** PostgreSQL  

## Setup & Quick Start

You can get the project running in a few steps:

```bash
# Clone the repository
git clone https://github.com/username/hrms-dashboard.git
cd hrms-dashboard

# Backend setup (FastAPI + PostgreSQL)
cd backend
python -m venv venv              # Create virtual environment

# Activate virtual environment
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt   # Install backend dependencies

# Configure your PostgreSQL database in `.env` or config file (username, password, database name, host, port)
# Run FastAPI server
uvicorn main:app --reload

# Frontend setup (Angular 21)
cd ../frontend
npm install                        # Install frontend dependencies
ng serve                            # Run Angular development server

# Open your browser at http://localhost:4200/

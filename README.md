````markdown
# Python Fundamentals

This repository contains object-oriented Python practice for the Loadberry Ltd AI Engineering Trainee Programme.

The purpose of this repository is to practise professional Python engineering foundations, including classes, dataclasses, type hints, validation, custom exceptions, automated testing, JSON storage, Git branching, and Pull Request workflow.

## Project: Student Records System

The main project in this repository is a Student Records System.

It currently supports:

- student data modelling
- student validation
- grade management
- records management
- student search
- class average calculation
- JSON save/load functionality
- automated pytest tests

## Repository Structure

See GitHub repo


## Components Completed

### 1. Student Model

Location: src/student_records/models.py

The `Student` model represents one student record.

Features:

stores student ID, name, email, and grades
cleans text fields
lowercases email addresses
validates required fields
validates email format
validates grade values
calculates average grade
checks pass/fail status
exports a student summary as a dictionary

### 2. Student Records Manager

Location: src/student_records/records.py

The `StudentRecords` manager handles a collection of students.

Features:

adds students
rejects duplicate student IDs
retrieves students by ID
removes students
adds grades to existing students
lists students sorted by ID
searches students by name
finds students by email
calculates class average
exports a full records summary as a dictionary

### 3. JSON Storage

Location: src/student_records/storage.py

The storage module saves and loads student records using JSON files.

Features:

converts `Student` objects into JSON-serialisable dictionaries
rebuilds `Student` objects from stored data
saves `StudentRecords` to JSON
loads `StudentRecords` from JSON
validates missing files
validates invalid JSON
validates missing required fields
validates invalid grade data
validates stored record structure

Example data file: xamples/students.json


## Setup

Clone the repository:

git clone git@github.com:HtetAg24/python-fundamentals.git
cd python-fundamentals

Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate

Install dependencies:

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .

Check Python version:

python --version

Expected:

Python 3.13.14
Running Tests

Run the full test suite:

python -m pytest -v
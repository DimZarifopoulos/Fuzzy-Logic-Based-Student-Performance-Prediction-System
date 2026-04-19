# Fuzzy-Logic-Based-Student-Performance-Prediction-System
Academic expert system implementing fuzzy logic to evaluate student performance based on multiple academic criteria.


Here is a professional README.md file designed for your GitHub repository. It clearly explains the technical implementation of your Expert System, the methodology used, and how to run the project.
Student Performance Prediction System (Fuzzy Logic)

This project is an expert system developed as part of the "Expert Systems" course. The system implements Fuzzy Logic to predict a student's overall academic performance based on specific academic criteria.
Overview

The system processes four input variables to provide an automated performance evaluation:

    - Participation: 0–100% (Low, Medium, High) 

    - Assignment Grades: 0–100 (Poor, Average, Good) 

    - Exam Grades: 0–100 (Poor, Average, Good) 

    - Absences: 0–30 (Few, Many) 

The system provides a final Performance output on a scale of 0–100.
Methodology

The system follows a standard Fuzzy Inference process to determine the outcome:

    - Fuzzification: Input values (e.g., participation percentage) are converted into fuzzy sets (Low, Medium, High, etc.).

    - Rule Application: The system utilizes a knowledge base of 54 IF-THEN rules to evaluate the inputs.

    - Aggregation: Partial results are combined into a single fuzzy output set.

    - Defuzzification: The final numerical (crisp) performance value is calculated using the Centroid method.

Prerequisites

The project is built using Python. You will need the following libraries:

    numpy

    matplotlib

You can install them via pip:
Bash

pip install numpy matplotlib

How to Run

    - Ensure the required libraries are installed.

    - Run the Python script in your IDE (e.g., VS Code, PyCharm) or terminal:
    Bash

    python student_performance_system.py

    - The script executes the fuzzy_inference function. You can modify the parameters at the bottom of the script:
    Python

    # Example call
    fuzzy_inference(p_value=70, a_value=80, e_value=65, abs_value=5)

---
*Developed as an individual project for the MSc in Informatics.*

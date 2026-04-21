import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from config import LOCAL_DATA_PATH

np.random.seed(42)

# Generate 10,000 student records
print("🎓 Generating 10K+ educational records...")

# Student Demographics
students = pd.DataFrame({
    'student_id': range(1, 10001),
    'name': [f'Student_{i}' for i in range(1, 10001)],
    'age': np.random.randint(18, 25, 10000),
    'gender': np.random.choice(['M', 'F'], 10000),
    'enrollment_date': pd.date_range('2020-01-01', periods=10000, freq='D')[:10000]
})

# Academic Records
grades = pd.DataFrame({
    'student_id': np.random.choice(students['student_id'], 50000),
    'course_id': np.random.randint(1, 51, 50000),
    'grade': np.random.normal(75, 15, 50000).clip(0, 100),
    'attendance_pct': np.random.uniform(70, 100, 50000),
    'semester': np.random.choice(['Fall2023', 'Spring2024'], 50000)
})

# Save to CSV (HDFS compatible format)
students.to_csv(f'{LOCAL_DATA_PATH}/students.csv', index=False)
grades.to_csv(f'{LOCAL_DATA_PATH}/grades.csv', index=False)

print(f"✅ Data generated: {LOCAL_DATA_PATH}/")
print(f"   - Students: {len(students):,}")
print(f"   - Grades: {len(grades):,}")
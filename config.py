import os
import json

"""
EduPredict - Complete Configuration
Hadoop + ML + Auth + Role-Based Access
"""

# ========================================
# FILESYSTEM & HADOOP CONFIG
# ========================================
HADOOP_HOME = "hadoop"
HDFS_PATH = "hdfs://localhost:9000/edupredict"
LOCAL_DATA_PATH = "data"
HDFS_RAW = f"{HDFS_PATH}/raw"
HDFS_PROCESSED = f"{HDFS_PATH}/processed"
HDFS_MODELS = f"{HDFS_PATH}/models"

# Create directories
os.makedirs(LOCAL_DATA_PATH, exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs(HADOOP_HOME, exist_ok=True)

# ========================================
# FLASK & WEB CONFIG
# ========================================
SECRET_KEY = "EduPredict2024-HadoopML-Secure-v2.0"
HOST = "localhost"
PORT = 5000
DEBUG = True

# ========================================
# ML MODEL CONFIG
# ========================================
PREDICTION_THRESHOLD = 0.7
DROPOUT_RISK_THRESHOLD = 0.6
MODEL_VERSION = "v1.0"
ML_MODEL_PATH = "models/dropout_predictor.pkl"

# Training Parameters
N_ESTIMATORS = 100
TEST_SIZE = 0.2
RANDOM_STATE = 42

# ========================================
# USER AUTH & ROLES (Project Requirements)
# ========================================
ROLES = {
    'admin': {
        'access': 'all',
        'permissions': ['users', 'data', 'ml', 'hadoop', 'analytics', 'reports']
    },
    'teacher': {
        'access': 'student_data',
        'permissions': ['grades', 'attendance', 'classroom', 'reports']
    },
    'student': {
        'access': 'personal_data', 
        'permissions': ['my_grades', 'my_attendance', 'progress']
    },
    'analyst': {
        'access': 'analytics',
        'permissions': ['dashboards', 'trends', 'predictions', 'exports']
    }
}

# User Database
USERS_DB = f"{LOCAL_DATA_PATH}/users.json"

# ========================================
# DATA SOURCES (Educational Datasets)
# ========================================
DATA_SOURCES = {
    'students': f'{LOCAL_DATA_PATH}/students.csv',
    'grades': f'{LOCAL_DATA_PATH}/grades.csv', 
    'attendance': f'{LOCAL_DATA_PATH}/attendance.csv',
    'lms_logs': f'{LOCAL_DATA_PATH}/lms_logs.csv'
}

# HDFS Data Paths
HDFS_DATA = {
    'students': f'{HDFS_RAW}/students.parquet',
    'grades': f'{HDFS_RAW}/grades.parquet',
    'attendance': f'{HDFS_RAW}/attendance.parquet'
}

# ========================================
# ALERTS & NOTIFICATIONS
# ========================================
ALERT_THRESHOLDS = {
    'dropout_risk': 0.6,
    'low_attendance': 70,
    'failing_grades': 60,
    'high_demand_courses': 80
}

NOTIFICATION_EMAILS = [
    'admin@edupredict.com',
    'principal@edupredict.com'
]

# ========================================
# SYSTEM MONITORING
# ========================================
MONITORING = {
    'uptime_target': '99%',
    'backup_schedule': 'daily@02:00',
    'log_level': 'INFO'
}

# ========================================
# Initialize Database & Default Admin
# ========================================
DEFAULT_ADMIN = {
    "admin": {
        "name": "Super Administrator",
        "email": "admin@edupredict.com",
        "role": "admin",
        "password": "$2b$12$K.I8.a1OZHmy.b/4o1qLhuxpsX3s0/D.Q8uKg7qz3U5RjAuNGc1e",  # admin123 (hashed)
        "created": "2024-01-01 10:00:00",
        "last_login": None
    }
}

def init_system():
    """Initialize system databases and files"""
    
    # Users DB
    if not os.path.exists(USERS_DB):
        with open(USERS_DB, 'w') as f:
            json.dump(DEFAULT_ADMIN, f, indent=2)
        print("✅ Created users database with default admin")
        print("👤 Login: admin / admin123")
    
    # Sample data files
    sample_data = {
        'students_sample.csv': '''student_id,name,age,gender,email,program
1,John Smith,20,M,john@example.com,BSCS
2,Sarah Johnson,19,F,sarah@example.com,BSSE
3,Mike Wilson,21,M,mike@example.com,BBA''',
        'courses.csv': '''course_id,course_name,credits,semester
1,Math-101,3,Fall 2023
2,Programming-101,4,Spring 2024'''
    }
    
    for filename, content in sample_data.items():
        filepath = f"{LOCAL_DATA_PATH}/{filename}"
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
    
    # Hadoop config files
    hadoop_config = f'''<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>{HDFS_PATH}</value>
    </property>
</configuration>'''
    
    with open(f"{HADOOP_HOME}/core-site.xml", 'w') as f:
        f.write(hadoop_config)
    
    print("✅ System initialized!")
    print(f"📁 Data Path: {LOCAL_DATA_PATH}")
    print(f"🗄️  HDFS Path: {HDFS_PATH}")
    print(f"👥 Users DB: {USERS_DB}")

# Initialize on import
init_system()

# ========================================
# Export Config (For debugging)
# ========================================
if __name__ == "__main__":
    print("EduPredict Configuration Loaded:")
    print(f"  📂 Data Path: {LOCAL_DATA_PATH}")
    print(f"  🗄️  HDFS: {HDFS_PATH}")
    print(f"  👥 Roles: {list(ROLES.keys())}")
    print(f"  🔐 Users DB: {USERS_DB}")
    print("✅ Ready for production!")
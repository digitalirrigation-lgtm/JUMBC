# ============================================================
# JIGJIGA UNIVERSAL MEDICAL & BUSINESS COLLEGE
# GRADE MANAGEMENT SYSTEM
# Developed by Zedagim Tesfaye (Eng)
# ============================================================
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import os
import altair as alt
import json
import base64
import io
import warnings
warnings.filterwarnings('ignore')

# ---------- CONFIG ----------
DB_PATH = "jmbc_grades.db"
REGISTRAR_PASSWORD = "11111111"
DEAN_PASSWORD = "00000000"
INSTRUCTOR_PASSWORD = "22222222"

# ============================================================
# TRANSLATIONS (with Instructor added)
# ============================================================
TRANSLATIONS = {
    'en': {
        'app_title': 'JMBC Grade Management System',
        'app_subtitle': 'Jigjiga Universal Medical & Business College',
        'footer': '🏫 JMBC Grade Management System • Developed by Zedagim Tesfaye (Eng) • © 2025',
        'access': '🔑 Access',
        'select_role': 'Select Role',
        'registrar': '📋 Registrar',
        'dean': '👔 Dean',
        'instructor': '👨‍🏫 Instructor',
        'registrar_password': 'Enter Registrar Password',
        'dean_password': 'Enter Dean Password',
        'instructor_password': 'Enter Instructor Password',
        'incorrect_password': '❌ Incorrect password.',
        'access_granted': '✅ Access granted.',
        'refresh': '🔄 Refresh Data',
        'language': '🌐 Language',
        'dashboard': '📊 Dashboard',
        'grade_submission': '📝 Grade Submission',
        'reports': '📄 Reports',
        'all_grades': '📋 All Grades',
        'upload_template': '📤 Download Template & Upload',
        'download_template_btn': '📥 Download Excel Template',
        'upload_file': 'Upload Excel File',
        'preview': 'Preview of uploaded data:',
        'upload_success': '✅ Grades uploaded successfully!',
        'processing': '🔄 Processing grades...',
        'no_data': 'No data available.',
        'no_grades': 'No grades submitted yet.',
        'enter_positive': 'Please enter valid data.',
        'welcome_registrar': '👋 Welcome, Registrar!',
        'welcome_dean': '👋 Welcome, Dean!',
        'welcome_instructor': '👋 Welcome, Instructor!',
        'good_morning': '🌅 Good Morning!',
        'good_afternoon': '☀️ Good Afternoon!',
        'good_evening': '🌙 Good Evening!',
        'today_date': '📅 Today is {date}',
        'delete': '🗑️',
        'undo': '↩️ Undo',
        'view': '👁️',
        'delete_success': '✅ Successfully Deleted!',
        'undo_success': '✅ Undo successful!',
        'undo_failed': '❌ Undo failed. No operation to undo.',
        'no_undo': 'No operations to undo',
        'total_students': '👨‍🎓 Total Students',
        'passed': '✅ Passed',
        'failed': '❌ Failed',
        'ng': '⚠️ NG',
        'by_department': '📊 Students by Department',
        'performance_summary': '📊 Performance Summary',
        'grade_distribution': '📊 Grade Distribution',
        'full_report': '📋 Full Grade Report',
        'ng_f_report': '📋 NG & F Students Report',
        'download_full': '📥 Download Full Report',
        'download_ng_f': '📥 Download NG & F Report',
        'monthly_report': '📅 Monthly Report',
        'generate_monthly': '📄 Generate Monthly Report',
        'monthly_ng_report': '📋 Monthly NG Students Report',
        'download_monthly': '📥 Download Monthly NG Report',
        'student_id': 'Student ID',
        'student_name': 'Student Name',
        'sex': 'Sex',
        'male': 'Male',
        'female': 'Female',
        'college': 'College',
        'department': 'Department',
        'course': 'Course Name',
        'location': 'Location',
        'assessment_70': '70% Assessment',
        'exam_30': '30% Final Exam',
        'total_marks': 'Total Marks',
        'grade': 'Grade',
        'remark': 'Remark',
        'academic_year': 'Academic Year',
        'semester': 'Semester',
        'jigjiga': 'Jigjiga',
        'kebrebeya': 'Kebrebeya',
        'fiq': 'Fiq',
        'accounting': 'Accounting',
        'crm': 'CRM',
        'pharmacy': 'Pharmacy',
        'nursing': 'Nursing',
        'january': 'January','february': 'February','march': 'March',
        'april': 'April','may': 'May','june': 'June',
        'july': 'July','august': 'August','september': 'September',
        'october': 'October','november': 'November','december': 'December',
        'pass': 'Passed',
        'fail': 'Failed',
        'ng_label': 'NG',
        'submitted': '✅ Successfully Submitted!',
        'upload_another': '📤 Upload Another',
        'delete_record': '🗑️ Delete Record',
        'select_record': 'Select Record to Delete',
        'delete_btn': 'Delete Selected',
        'undo_btn': '↩️ Undo Last',
        'clear': 'Clear All',
        'month': 'Month',
        'manual_entry': '✏️ Manual Entry',
        'manual_submit_btn': '➕ Submit Grade',
    },
    'am': {
        'app_title': 'የጄኤምቢሲ ውጤት አስተዳደር ስርዓት',
        'app_subtitle': 'ጅጅጊጋ ዩኒቨርሳል ሜዲካል እና ቢዝነስ ኮሌጅ',
        'footer': '🏫 የጄኤምቢሲ ውጤት አስተዳደር ስርዓት • በዘዳግም ተስፋዬ (ኢንጂነር) • © 2025',
        'access': '🔑 መዳረሻ',
        'select_role': 'ሚና ይምረጡ',
        'registrar': '📋 መዝጋቢ',
        'dean': '👔 ዲን',
        'instructor': '👨‍🏫 አስተማሪ',
        'registrar_password': 'የመዝጋቢ የይለፍ ቃል',
        'dean_password': 'የዲን የይለፍ ቃል',
        'instructor_password': 'የአስተማሪ የይለፍ ቃል',
        'incorrect_password': '❌ የይለፍ ቃሉ ተሳስቷል።',
        'access_granted': '✅ መዳረሻ ተሰጥቷል',
        'refresh': '🔄 አድስ',
        'language': '🌐 ቋንቋ',
        'dashboard': '📊 ዳሽቦርድ',
        'grade_submission': '📝 ውጤት ማስገቢያ',
        'reports': '📄 ሪፖርቶች',
        'all_grades': '📋 ሁሉም ውጤቶች',
        'upload_template': '📤 አብነት አውርድ እና ጫን',
        'download_template_btn': '📥 የExcel አብነት አውርድ',
        'upload_file': 'Excel ፋይል ጫን',
        'preview': 'የተጫነው ውሂብ ቅድመ እይታ:',
        'upload_success': '✅ ውጤቶች በተሳካ ሁኔታ ተጭነዋል!',
        'processing': '🔄 ውጤቶች እየተሰሩ ነው...',
        'no_data': 'ምንም መረጃ የለም።',
        'no_grades': 'እስካሁን ውጤቶች አልተጫኑም።',
        'enter_positive': 'እባክዎ ትክክለኛ መረጃ ያስገቡ።',
        'welcome_registrar': '👋 እንኳን ደህና መጡ መዝጋቢ!',
        'welcome_dean': '👋 እንኳን ደህና መጡ ዲን!',
        'welcome_instructor': '👋 እንኳን ደህና መጡ አስተማሪ!',
        'good_morning': '🌅 እንደምን አደሩ!',
        'good_afternoon': '☀️ እንደምን ዋሉ!',
        'good_evening': '🌙 እንደምን አመሹ!',
        'today_date': '📅 ዛሬ {date} ነው',
        'delete': '🗑️',
        'undo': '↩️ ቀልብስ',
        'view': '👁️',
        'delete_success': '✅ በተሳካ ሁኔታ ተሰርዟል!',
        'undo_success': '✅ መቀልበስ ተሳካ!',
        'undo_failed': '❌ መቀልበስ አልተቻለም።',
        'no_undo': 'ምንም ለመቀልበስ የለም',
        'total_students': '👨‍🎓 ጠቅላላ ተማሪዎች',
        'passed': '✅ አልፈዋል',
        'failed': '❌ ወድቀዋል',
        'ng': '⚠️ ኤንጂ',
        'by_department': '📊 በመምሪያ የተከፋፈሉ ተማሪዎች',
        'performance_summary': '📊 የአፈጻጸም ማጠቃለያ',
        'grade_distribution': '📊 የውጤት ስርጭት',
        'full_report': '📋 ሙሉ የውጤት ሪፖርት',
        'ng_f_report': '📋 የኤንጂ እና ኤፍ ተማሪዎች ሪፖርት',
        'download_full': '📥 ሙሉ ሪፖርት አውርድ',
        'download_ng_f': '📥 የኤንጂ እና ኤፍ ሪፖርት አውርድ',
        'monthly_report': '📅 ወርሃዊ ሪፖርት',
        'generate_monthly': '📄 ወርሃዊ ሪፖርት አዘጋጅ',
        'monthly_ng_report': '📋 ወርሃዊ የኤንጂ ተማሪዎች ሪፖርት',
        'download_monthly': '📥 ወርሃዊ የኤንጂ ሪፖርት አውርድ',
        'student_id': 'የተማሪ መታወቂያ',
        'student_name': 'ሙሉ ስም',
        'sex': 'ፆታ',
        'male': 'ወንድ',
        'female': 'ሴት',
        'college': 'ኮሌጅ',
        'department': 'መምሪያ',
        'course': 'የትምህርት ስም',
        'location': 'ቦታ',
        'assessment_70': '70% ግምገማ',
        'exam_30': '30% የመጨረሻ ፈተና',
        'total_marks': 'ጠቅላላ ውጤት',
        'grade': 'ደረጃ',
        'remark': 'አስተያየት',
        'academic_year': 'የትምህርት ዘመን',
        'semester': 'ሴሚስተር',
        'jigjiga': 'ጅጅጊጋ',
        'kebrebeya': 'ቀበረቤያ',
        'fiq': 'ፊቅ',
        'accounting': 'አካውንቲንግ',
        'crm': 'ሲአርኤም',
        'pharmacy': 'ፋርማሲ',
        'nursing': 'ነርሲንግ',
        'january': 'ጥር','february': 'የካቲት','march': 'መጋቢት',
        'april': 'ሚያዝያ','may': 'ግንቦት','june': 'ሰኔ',
        'july': 'ሐምሌ','august': 'ነሐሴ','september': 'መስከረም',
        'october': 'ጥቅምት','november': 'ህዳር','december': 'ታህሳስ',
        'pass': 'አልፏል',
        'fail': 'ወድቋል',
        'ng_label': 'ኤንጂ',
        'submitted': '✅ በተሳካ ሁኔታ ተልኳል!',
        'upload_another': '📤 ሌላ ጫን',
        'delete_record': '🗑️ መዝገብ ሰርዝ',
        'select_record': 'ለመሰረዝ መዝገብ ይምረጡ',
        'delete_btn': 'የተመረጠውን ሰርዝ',
        'undo_btn': '↩️ የመጨረሻውን ቀልብስ',
        'clear': 'ሁሉንም አጽዳ',
        'month': 'ወር',
        'manual_entry': '✏️ በእጅ ማስገቢያ',
        'manual_submit_btn': '➕ ውጤት አስገባ',
    },
    'so': {
        'app_title': 'Nidaamka Buundooyinka ee JMBC',
        'app_subtitle': 'Kulliyadda Caafimaadka iyo Ganacsiga ee Jigjiga',
        'footer': '🏫 Nidaamka Buundooyinka ee JMBC • Waxaa diyaariyay Zedagim Tesfaye (Eng) • © 2025',
        'access': '🔑 Gelitaan',
        'select_role': 'Dooro Doorka',
        'registrar': '📋 Diwaangeliye',
        'dean': '👔 Dekaan',
        'instructor': '👨‍🏫 Macallin',
        'registrar_password': 'Furaha Diwaangeliye',
        'dean_password': 'Furaha Dekaan',
        'instructor_password': 'Furaha Macallin',
        'incorrect_password': '❌ Furaha waa qalad.',
        'access_granted': '✅ Gelitaan la siiyay',
        'refresh': '🔄 Cusboonaysii',
        'language': '🌐 Luqadda',
        'dashboard': '📊 Dashboard',
        'grade_submission': '📝 Soo Gelin Buundooyinka',
        'reports': '📄 Warbixinno',
        'all_grades': '📋 Dhammaan Buundooyinka',
        'upload_template': '📤 Soo Deji Qaab & Soo Gel',
        'download_template_btn': '📥 Soo Deji Qaabka Excel',
        'upload_file': 'Soo Gel Faylka Excel',
        'preview': 'Muujinta xogta:',
        'upload_success': '✅ Buundooyinka si guul leh ayaa loo soo geliyay!',
        'processing': '🔄 Buundooyinka waa la socodsiiyaa...',
        'no_data': 'Xog ma jirto.',
        'no_grades': 'Weli buundooyin ma jiraan.',
        'enter_positive': 'Fadlan geli xog sax ah.',
        'welcome_registrar': '👋 Soo dhowow, Diwaangeliye!',
        'welcome_dean': '👋 Soo dhowow, Dekaan!',
        'welcome_instructor': '👋 Soo dhowow, Macallin!',
        'good_morning': '🌅 Subax wanaagsan!',
        'good_afternoon': '☀️ Galab wanaagsan!',
        'good_evening': '🌙 Fiid wanaagsan!',
        'today_date': '📅 Maanta waa {date}',
        'delete': '🗑️',
        'undo': '↩️ Ka Noqo',
        'view': '👁️',
        'delete_success': '✅ Si guul leh ayaa loo tirtiray!',
        'undo_success': '✅ Ka noqoshada waa guul!',
        'undo_failed': '❌ Ka noqoshada way fashilantay.',
        'no_undo': 'Wax ka noqosho ah ma jiro',
        'total_students': '👨‍🎓 Wadarta Ardayda',
        'passed': '✅ Ka Gudbay',
        'failed': '❌ Ku Dhacay',
        'ng': '⚠️ NG',
        'by_department': '📊 Ardayda Qaybaha',
        'performance_summary': '📊 Soo Koobida Waxqabadka',
        'grade_distribution': '📊 Qaybinta Buundooyinka',
        'full_report': '📋 Warbixinta Buundooyinka Oo Dhan',
        'ng_f_report': '📋 Warbixinta Ardayda NG & F',
        'download_full': '📥 Soo Deji Warbixin Dhan',
        'download_ng_f': '📥 Soo Deji Warbixinta NG & F',
        'monthly_report': '📅 Warbixinta Bille',
        'generate_monthly': '📄 Diyaari Warbixinta Bille',
        'monthly_ng_report': '📋 Warbixinta Ardayda NG Bille',
        'download_monthly': '📥 Soo Deji Warbixinta NG Bille',
        'student_id': 'Aqoonsiga Ardayga',
        'student_name': 'Magaca',
        'sex': 'Jinsiga',
        'male': 'Lab',
        'female': 'Dhedig',
        'college': 'Kulliyad',
        'department': 'Qayb',
        'course': 'Maaddada',
        'location': 'Goobta',
        'assessment_70': '70% Qiimayn',
        'exam_30': '30% Imtixaanka',
        'total_marks': 'Wadarta Buundooyinka',
        'grade': 'Buundo',
        'remark': "Faa'iido",
        'academic_year': 'Sannadka Waxbarashada',
        'semester': 'Simistar',
        'jigjiga': 'Jigjiga',
        'kebrebeya': 'Kebrebeya',
        'fiq': 'Fiq',
        'accounting': 'Xisaabaad',
        'crm': 'CRM',
        'pharmacy': 'Farmaansi',
        'nursing': 'Kalkaalinta',
        'january': 'Janaayo','february': 'Febraayo','march': 'Maarso',
        'april': 'Abriil','may': 'Maajo','june': 'Juun',
        'july': 'Luulyo','august': 'Agosto','september': 'Sebtembar',
        'october': 'Oktoobar','november': 'Nofembar','december': 'Disembar',
        'pass': 'Ka Gudbay',
        'fail': 'Ku Dhacay',
        'ng_label': 'NG',
        'submitted': '✅ Si Guul Leh Loo Soo Gudbiyay!',
        'upload_another': '📤 Soo Gel Mid Kale',
        'delete_record': '🗑️ Tirtir Diwaan',
        'select_record': 'Dooro Diwaanka',
        'delete_btn': 'Tirtir',
        'undo_btn': '↩️ Ka Noqo Tirtirka',
        'clear': 'Nadiifi Dhammaan',
        'month': 'Bil',
        'manual_entry': '✏️ Geli Gacanta',
        'manual_submit_btn': '➕ Soo Gel Buundo',
    }
}

# ============================================================
# DATABASE SETUP
# ============================================================
def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Grades (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID TEXT NOT NULL,
        StudentName TEXT NOT NULL,
        Sex TEXT NOT NULL,
        College TEXT NOT NULL,
        Department TEXT NOT NULL,
        Course TEXT NOT NULL,
        Location TEXT NOT NULL,
        Assessment70 REAL NOT NULL,
        Exam30 REAL NOT NULL,
        TotalMarks REAL NOT NULL,
        Grade TEXT NOT NULL,
        Remark TEXT NOT NULL,
        AcademicYear TEXT,
        Semester TEXT,
        UploadDate TEXT,
        CreatedAt TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS UndoLog (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        OperationType TEXT NOT NULL,
        RecordId INTEGER NOT NULL,
        OldData TEXT,
        CreatedAt TEXT
    )''')
    conn.commit()
    conn.close()

if not os.path.exists(DB_PATH):
    init_db()
else:
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Grades'")
    if not c.fetchone():
        init_db()
    conn.close()

# ============================================================
# GRADE CALCULATION FUNCTIONS
# ============================================================
def calculate_grade(total_marks):
    if total_marks == 0:
        return 'F', 'Failed'
    elif total_marks < 74:
        return 'NG', 'NG'
    elif 74 <= total_marks < 76:
        return 'C-', 'Passed'
    elif 76 <= total_marks < 80:
        return 'C', 'Passed'
    elif 80 <= total_marks < 84:
        return 'B-', 'Passed'
    elif 84 <= total_marks < 88:
        return 'B', 'Passed'
    elif 88 <= total_marks < 92:
        return 'A', 'Passed'
    elif 92 <= total_marks <= 100:
        return 'A+', 'Passed'
    else:
        return 'NG', 'NG'

def process_grades(df):
    results = []
    for idx, row in df.iterrows():
        total = row['Assessment70'] + row['Exam30']
        grade, remark = calculate_grade(total)
        results.append({
            'StudentID': row['StudentID'],
            'StudentName': row['StudentName'],
            'Sex': row['Sex'],
            'College': row['College'],
            'Department': row['Department'],
            'Course': row['Course'],
            'Location': row['Location'],
            'Assessment70': row['Assessment70'],
            'Exam30': row['Exam30'],
            'TotalMarks': total,
            'Grade': grade,
            'Remark': remark
        })
    return pd.DataFrame(results)

def save_grades(df, academic_year, semester):
    conn = get_db()
    c = conn.cursor()
    for idx, row in df.iterrows():
        c.execute("""INSERT INTO Grades 
            (StudentID, StudentName, Sex, College, Department, Course, Location,
             Assessment70, Exam30, TotalMarks, Grade, Remark, AcademicYear, Semester, UploadDate, CreatedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (row['StudentID'], row['StudentName'], row['Sex'], row['College'],
             row['Department'], row['Course'], row['Location'],
             row['Assessment70'], row['Exam30'], row['TotalMarks'],
             row['Grade'], row['Remark'], academic_year, semester,
             datetime.now().strftime("%Y-%m-%d"),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_all_grades():
    conn = get_db()
    df = pd.read_sql("SELECT * FROM Grades ORDER BY Id DESC", conn)
    conn.close()
    return df

def delete_grade_record(record_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Grades WHERE Id = ?", (record_id,))
    row = c.fetchone()
    if row:
        columns = ['Id', 'StudentID', 'StudentName', 'Sex', 'College', 'Department', 
                   'Course', 'Location', 'Assessment70', 'Exam30', 'TotalMarks', 
                   'Grade', 'Remark', 'AcademicYear', 'Semester', 'UploadDate', 'CreatedAt']
        old_data = {columns[i]: row[i] for i in range(len(columns))}
        c.execute("DELETE FROM Grades WHERE Id = ?", (record_id,))
        c.execute("""INSERT INTO UndoLog (OperationType, RecordId, OldData, CreatedAt)
                     VALUES (?, ?, ?, ?)""",
                  ('DELETE', record_id, json.dumps(old_data), 
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True, old_data
    conn.close()
    return False, None

def undo_last_delete():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM UndoLog ORDER BY Id DESC LIMIT 1")
    row = c.fetchone()
    if not row:
        return False, "No operation to undo"
    record_id = row[2]
    old_data = json.loads(row[3])
    try:
        columns = ', '.join(old_data.keys())
        placeholders = ', '.join(['?' for _ in old_data])
        c.execute(f"INSERT INTO Grades ({columns}) VALUES ({placeholders})", list(old_data.values()))
        c.execute("DELETE FROM UndoLog WHERE Id = ?", (row[0],))
        conn.commit()
        conn.close()
        return True, f"Restored record: {old_data['StudentName']}"
    except Exception as e:
        conn.close()
        return False, f"Undo failed: {str(e)}"

def get_last_undo():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT OperationType, CreatedAt FROM UndoLog ORDER BY Id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return f"{row[0]} at {row[1]}"
    return None

def get_monthly_ng_report(month, year):
    df = get_all_grades()
    if df.empty:
        return df
    df['UploadDate'] = pd.to_datetime(df['UploadDate'])
    mask = (df['UploadDate'].dt.month == month) & (df['UploadDate'].dt.year == year)
    monthly = df[mask]
    return monthly[monthly['Remark'] == 'NG']

def get_department_summary():
    df = get_all_grades()
    if df.empty:
        return pd.DataFrame()
    summary = df.groupby('Department').agg({
        'StudentName': 'count',
        'Remark': lambda x: (x == 'Passed').sum()
    }).reset_index()
    summary.columns = ['Department', 'Total', 'Passed']
    summary['Failed'] = summary['Total'] - summary['Passed']
    return summary

def generate_template():
    sample_data = {
        'StudentID': ['JMBC-001', 'JMBC-002', 'JMBC-003'],
        'StudentName': ['Abebe Kebede', 'Alemitu Hailu', 'Dawit Tadesse'],
        'Sex': ['Male', 'Female', 'Male'],
        'College': ['JMBC', 'JMBC', 'JMBC'],
        'Department': ['Accounting', 'Nursing', 'Pharmacy'],
        'Course': ['Financial Accounting', 'Fundamentals of Nursing', 'Pharmacology'],
        'Location': ['Jigjiga', 'Kebrebeya', 'Fiq'],
        'Assessment70': [65, 72, 55],
        'Exam30': [28, 25, 20]
    }
    return pd.DataFrame(sample_data)

def create_excel_download(df, filename):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Grades')
    output.seek(0)
    return output

# ============================================================
# STREAMLIT UI
# ============================================================
st.set_page_config(layout="wide", page_title="📊 JMBC Grade Management", page_icon="📊")

# ---- Language Selection ----
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'
lang = st.sidebar.selectbox(
    "🌐 Language",
    options=['en', 'am', 'so'],
    format_func=lambda x: {'en':'English', 'am':'አማርኛ', 'so':'Somali'}[x],
    index=['en','am','so'].index(st.session_state['lang'])
)
st.session_state['lang'] = lang
t = TRANSLATIONS[lang]

# ---- Custom CSS ----
st.markdown("""
<style>
@keyframes starGlow {
  0% { text-shadow: 0 0 5px gold; }
  50% { text-shadow: 0 0 20px #FFD700, 0 0 30px #FFA500; }
  100% { text-shadow: 0 0 5px gold; }
}
.star-rating {
  font-size: 2.5rem;
  color: #FFD700;
  animation: starGlow 2s infinite alternate;
  display: inline-block;
}
.big-title {
  font-size: 3rem;
  font-weight: 900;
  background: linear-gradient(45deg, #b8860b, #FFD700, #b8860b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(184,134,11,0.3);
  text-align: center;
}
.sub-title {
  font-size: 1.2rem;
  color: #1a1a2e;
  text-align: center;
  margin-top: -5px;
}
.welcome-box {
  background: linear-gradient(145deg, #FFD700, #B8860B);
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  color: white;
  margin-bottom: 20px;
}
.welcome-box h2 {
  color: white !important;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.welcome-box p {
  color: rgba(255,255,255,0.9) !important;
}
.pass { color: #28a745 !important; font-weight: bold; }
.fail { color: #dc3545 !important; font-weight: bold; }
.ng { color: #ffc107 !important; font-weight: bold; }
.stButton button {
  background: linear-gradient(145deg, #FFD700, #B8860B) !important;
  color: #1a1a2e !important;
  border-radius: 30px !important;
  border: none !important;
  font-weight: bold !important;
  box-shadow: 0 4px 15px rgba(184, 134, 11, 0.3) !important;
  transition: transform 0.2s;
}
.stButton button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 25px rgba(184, 134, 11, 0.5) !important;
}
.stButton button:disabled {
  background: #28a745 !important;
  color: white !important;
  opacity: 0.8;
  cursor: not-allowed;
}
.undo-box {
  background: #17a2b8;
  padding: 10px 20px;
  border-radius: 10px;
  color: white;
  text-align: center;
  margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown(f"""
<div style="text-align: center;">
  <span class="star-rating">★★★★★</span>
</div>
<h1 class="big-title">{t['app_title']}</h1>
<p class="sub-title">{t['app_subtitle']}</p>
<hr style="border: 1px solid #b8860b; width: 60%; margin: auto;"/>
<br>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
st.sidebar.markdown(f"### {t['access']}")
role = st.sidebar.radio(t['select_role'], [t['registrar'], t['dean'], t['instructor']])

# Password handling
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

if role == t['registrar']:
    if not st.session_state.authenticated or st.session_state.user_role != 'registrar':
        pwd = st.sidebar.text_input(t['registrar_password'], type="password", key="reg_pwd")
        if st.sidebar.button("Login", key="reg_login"):
            if pwd == REGISTRAR_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.user_role = 'registrar'
                st.sidebar.success(t['access_granted'])
                st.rerun()
            else:
                st.sidebar.error(t['incorrect_password'])
    else:
        st.sidebar.success(f"✅ {t['access_granted']}")
elif role == t['dean']:
    if not st.session_state.authenticated or st.session_state.user_role != 'dean':
        pwd = st.sidebar.text_input(t['dean_password'], type="password", key="dean_pwd")
        if st.sidebar.button("Login", key="dean_login"):
            if pwd == DEAN_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.user_role = 'dean'
                st.sidebar.success(t['access_granted'])
                st.rerun()
            else:
                st.sidebar.error(t['incorrect_password'])
    else:
        st.sidebar.success(f"✅ {t['access_granted']}")
else:  # Instructor
    if not st.session_state.authenticated or st.session_state.user_role != 'instructor':
        pwd = st.sidebar.text_input(t['instructor_password'], type="password", key="inst_pwd")
        if st.sidebar.button("Login", key="inst_login"):
            if pwd == INSTRUCTOR_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.user_role = 'instructor'
                st.sidebar.success(t['access_granted'])
                st.rerun()
            else:
                st.sidebar.error(t['incorrect_password'])
    else:
        st.sidebar.success(f"✅ {t['access_granted']}")

st.sidebar.markdown("---")

# ---- UNDO BUTTON ----
last_op = get_last_undo()
if last_op:
    st.sidebar.markdown(f"### ↩️ {t['undo_btn']}")
    st.sidebar.caption(f"Last: {last_op}")
    if st.sidebar.button(t['undo_btn'], key="sidebar_undo"):
        success, msg = undo_last_delete()
        if success:
            st.sidebar.success(msg)
            st.rerun()
        else:
            st.sidebar.error(msg)
else:
    st.sidebar.info(t['no_undo'])

st.sidebar.markdown("---")
if st.sidebar.button(t['refresh']):
    st.rerun()

# ---- WELCOME ----
now = datetime.now()
hour = now.hour
if 5 <= hour < 12:
    greeting = t['good_morning']
elif 12 <= hour < 17:
    greeting = t['good_afternoon']
else:
    greeting = t['good_evening']

if st.session_state.user_role == 'registrar':
    welcome_msg = t['welcome_registrar']
elif st.session_state.user_role == 'dean':
    welcome_msg = t['welcome_dean']
elif st.session_state.user_role == 'instructor':
    welcome_msg = t['welcome_instructor']
else:
    welcome_msg = ""

if st.session_state.authenticated:
    st.markdown(f"""
    <div class="welcome-box">
        <h2>{greeting} {welcome_msg}</h2>
        <p>{t['today_date'].format(date=now.strftime("%B %d, %Y"))}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN CONTENT - ONLY FOR AUTHENTICATED USERS
# ============================================================
if st.session_state.authenticated:
    
    # ---------- INSTRUCTOR VIEW ----------
    if st.session_state.user_role == 'instructor':
        tab1, tab2 = st.tabs([t['grade_submission'], t['reports']])
        
        # ---------- TAB 1: GRADE SUBMISSION ----------
        with tab1:
            st.subheader("📤 " + t['upload_template'])
            
            # Download template
            template_df = generate_template()
            template_excel = create_excel_download(template_df, "JMBC_Grade_Template.xlsx")
            st.download_button(
                label=t['download_template_btn'],
                data=template_excel.getvalue(),
                file_name="JMBC_Grade_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.markdown("---")
            st.subheader("📤 Upload Excel File")
            uploaded_file = st.file_uploader(t['upload_file'], type=['xlsx', 'xls', 'csv'], key="inst_upload")
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df_upload = pd.read_csv(uploaded_file)
                    else:
                        df_upload = pd.read_excel(uploaded_file)
                    required = ['StudentID', 'StudentName', 'Sex', 'College', 'Department', 
                               'Course', 'Location', 'Assessment70', 'Exam30']
                    missing = [col for col in required if col not in df_upload.columns]
                    if missing:
                        st.error(f"Missing columns: {missing}")
                    else:
                        st.write(t['preview'])
                        st.dataframe(df_upload.head(10), use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            academic_year = st.text_input(t['academic_year'], value="2018 E.C", key="inst_academic_year")
                        with col2:
                            semester = st.text_input(t['semester'], value="Semester 1", key="inst_semester")
                        if 'inst_upload_submitted' not in st.session_state:
                            st.session_state.inst_upload_submitted = False
                        if st.session_state.inst_upload_submitted:
                            st.success(t['upload_success'])
                            st.balloons()
                            if st.button(t['upload_another'], key="inst_upload_another"):
                                st.session_state.inst_upload_submitted = False
                                st.rerun()
                        else:
                            if st.button("🚀 Process & Upload Grades", key="inst_process_grades", use_container_width=True):
                                with st.spinner(t['processing']):
                                    processed = process_grades(df_upload)
                                    save_grades(processed, academic_year, semester)
                                    st.session_state.inst_upload_submitted = True
                                    st.success(t['upload_success'])
                                    st.balloons()
                                    col1, col2, col3 = st.columns(3)
                                    col1.metric(t['total_students'], len(processed))
                                    col2.metric(t['passed'], len(processed[processed['Remark'] == 'Passed']))
                                    col3.metric(t['failed'], len(processed[processed['Remark'] != 'Passed']))
                                    st.rerun()
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            
            st.markdown("---")
            st.subheader(t['manual_entry'])
            with st.form(key="manual_form"):
                col1, col2 = st.columns(2)
                with col1:
                    student_id = st.text_input(t['student_id'], key="inst_manual_id")
                    student_name = st.text_input(t['student_name'], key="inst_manual_name")
                    sex = st.selectbox(t['sex'], [t['male'], t['female']], key="inst_manual_sex")
                    college = st.text_input(t['college'], value="JMBC", key="inst_manual_college")
                    department = st.selectbox(t['department'], [t['accounting'], t['crm'], t['pharmacy'], t['nursing']], key="inst_manual_dept")
                with col2:
                    course = st.text_input(t['course'], key="inst_manual_course")
                    location = st.selectbox(t['location'], [t['jigjiga'], t['kebrebeya'], t['fiq']], key="inst_manual_loc")
                    assessment70 = st.number_input(t['assessment_70'], min_value=0.0, max_value=70.0, step=0.5, key="inst_manual_assess")
                    exam30 = st.number_input(t['exam_30'], min_value=0.0, max_value=30.0, step=0.5, key="inst_manual_exam")
                academic_year_manual = st.text_input(t['academic_year'], value="2018 E.C", key="inst_manual_year")
                semester_manual = st.text_input(t['semester'], value="Semester 1", key="inst_manual_sem")
                submit_btn = st.form_submit_button(t['manual_submit_btn'], use_container_width=True)
                if submit_btn:
                    if not student_id or not student_name or not course:
                        st.warning("Please fill all required fields.")
                    else:
                        total = assessment70 + exam30
                        grade, remark = calculate_grade(total)
                        # Create a single row dataframe
                        new_row = pd.DataFrame([{
                            'StudentID': student_id,
                            'StudentName': student_name,
                            'Sex': sex,
                            'College': college,
                            'Department': department,
                            'Course': course,
                            'Location': location,
                            'Assessment70': assessment70,
                            'Exam30': exam30,
                            'TotalMarks': total,
                            'Grade': grade,
                            'Remark': remark
                        }])
                        save_grades(new_row, academic_year_manual, semester_manual)
                        st.success(f"✅ Grade for {student_name} submitted successfully!")
                        st.balloons()
                        # Clear form by rerun
                        st.rerun()
        
        # ---------- TAB 2: REPORTS ----------
        with tab2:
            st.subheader(t['reports'])
            all_grades = get_all_grades()
            if all_grades.empty:
                st.info(t['no_grades'])
            else:
                # Filter and display
                col1, col2, col3 = st.columns(3)
                with col1:
                    departments = ['All'] + all_grades['Department'].unique().tolist()
                    dept_filter = st.selectbox(t['department'], departments, key="inst_dept_filter")
                with col2:
                    locations = ['All'] + all_grades['Location'].unique().tolist()
                    loc_filter = st.selectbox(t['location'], locations, key="inst_loc_filter")
                with col3:
                    grades = ['All'] + all_grades['Grade'].unique().tolist()
                    grade_filter = st.selectbox(t['grade'], grades, key="inst_grade_filter")
                filtered = all_grades.copy()
                if dept_filter != 'All':
                    filtered = filtered[filtered['Department'] == dept_filter]
                if loc_filter != 'All':
                    filtered = filtered[filtered['Location'] == loc_filter]
                if grade_filter != 'All':
                    filtered = filtered[filtered['Grade'] == grade_filter]
                st.dataframe(filtered[['StudentID', 'StudentName', 'Department', 'Course', 'TotalMarks', 'Grade', 'Remark']], use_container_width=True)
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(t['full_report'])
                    full_excel = create_excel_download(filtered, "Full_Grade_Report.xlsx")
                    st.download_button(label=t['download_full'], data=full_excel.getvalue(), file_name="Full_Grade_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                with col2:
                    st.subheader(t['ng_f_report'])
                    ng_f = filtered[filtered['Remark'].isin(['NG', 'Failed'])]
                    if not ng_f.empty:
                        ng_f_excel = create_excel_download(ng_f, "NG_F_Students_Report.xlsx")
                        st.download_button(label=t['download_ng_f'], data=ng_f_excel.getvalue(), file_name="NG_F_Students_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                        st.warning(f"⚠️ {len(ng_f)} students need re-exam!")
                    else:
                        st.success("✅ No NG or F students!")
                # Monthly report
                st.markdown("---")
                st.subheader(t['monthly_report'])
                col1, col2 = st.columns(2)
                with col1:
                    month_sel = st.selectbox(t['month'], list(range(1,13)), key="inst_month",
                                            format_func=lambda x: t['january'] if x==1 else t['february'] if x==2 else t['march'] if x==3 else t['april'] if x==4 else t['may'] if x==5 else t['june'] if x==6 else t['july'] if x==7 else t['august'] if x==8 else t['september'] if x==9 else t['october'] if x==10 else t['november'] if x==11 else t['december'])
                with col2:
                    year_sel = st.number_input(t['academic_year'], min_value=2020, max_value=2030, value=2025, key="inst_year")
                if st.button(t['generate_monthly'], key="inst_monthly_btn"):
                    monthly_df = get_monthly_ng_report(month_sel, year_sel)
                    if not monthly_df.empty:
                        st.subheader(t['monthly_ng_report'])
                        st.dataframe(monthly_df[['StudentID', 'StudentName', 'Department', 'Course', 'Grade']], use_container_width=True)
                        monthly_excel = create_excel_download(monthly_df, f"Monthly_NG_Report_{month_sel}_{year_sel}.xlsx")
                        st.download_button(label=t['download_monthly'], data=monthly_excel.getvalue(), file_name=f"Monthly_NG_Report_{month_sel}_{year_sel}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                    else:
                        st.info(f"No NG students in {month_sel}/{year_sel}")
                # Delete
                st.markdown("---")
                st.subheader(t['delete_record'])
                ids = all_grades['Id'].tolist()
                if ids:
                    selected_id = st.selectbox(t['select_record'], ids, format_func=lambda x: f"ID: {x}", key="inst_del_select")
                    if st.button(t['delete_btn'], key="inst_del_btn"):
                        success, _ = delete_grade_record(selected_id)
                        if success:
                            st.success(t['delete_success'])
                            st.rerun()
                        else:
                            st.error("Delete failed")
    
    # ---------- REGISTRAR VIEW (same as before) ----------
    elif st.session_state.user_role == 'registrar':
        tab1, tab2 = st.tabs([t['grade_submission'], t['reports']])
        with tab1:
            st.subheader(t['upload_template'])
            template_df = generate_template()
            template_excel = create_excel_download(template_df, "JMBC_Grade_Template.xlsx")
            st.download_button(label=t['download_template_btn'], data=template_excel.getvalue(), file_name="JMBC_Grade_Template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
            st.markdown("---")
            st.subheader("📤 Upload Grades")
            uploaded_file = st.file_uploader(t['upload_file'], type=['xlsx', 'xls', 'csv'], key="reg_upload")
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df_upload = pd.read_csv(uploaded_file)
                    else:
                        df_upload = pd.read_excel(uploaded_file)
                    required = ['StudentID', 'StudentName', 'Sex', 'College', 'Department', 'Course', 'Location', 'Assessment70', 'Exam30']
                    missing = [col for col in required if col not in df_upload.columns]
                    if missing:
                        st.error(f"Missing columns: {missing}")
                    else:
                        st.write(t['preview'])
                        st.dataframe(df_upload.head(10), use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            academic_year = st.text_input(t['academic_year'], value="2018 E.C", key="reg_academic_year")
                        with col2:
                            semester = st.text_input(t['semester'], value="Semester 1", key="reg_semester")
                        if 'reg_upload_submitted' not in st.session_state:
                            st.session_state.reg_upload_submitted = False
                        if st.session_state.reg_upload_submitted:
                            st.success(t['upload_success'])
                            st.balloons()
                            if st.button(t['upload_another'], key="reg_upload_another"):
                                st.session_state.reg_upload_submitted = False
                                st.rerun()
                        else:
                            if st.button("🚀 Process & Upload Grades", key="reg_process_grades", use_container_width=True):
                                with st.spinner(t['processing']):
                                    processed = process_grades(df_upload)
                                    save_grades(processed, academic_year, semester)
                                    st.session_state.reg_upload_submitted = True
                                    st.success(t['upload_success'])
                                    st.balloons()
                                    col1, col2, col3 = st.columns(3)
                                    col1.metric(t['total_students'], len(processed))
                                    col2.metric(t['passed'], len(processed[processed['Remark'] == 'Passed']))
                                    col3.metric(t['failed'], len(processed[processed['Remark'] != 'Passed']))
                                    st.rerun()
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        with tab2:
            st.subheader(t['reports'])
            all_grades = get_all_grades()
            if all_grades.empty:
                st.info(t['no_grades'])
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    departments = ['All'] + all_grades['Department'].unique().tolist()
                    dept_filter = st.selectbox(t['department'], departments, key="reg_dept_filter")
                with col2:
                    locations = ['All'] + all_grades['Location'].unique().tolist()
                    loc_filter = st.selectbox(t['location'], locations, key="reg_loc_filter")
                with col3:
                    grades = ['All'] + all_grades['Grade'].unique().tolist()
                    grade_filter = st.selectbox(t['grade'], grades, key="reg_grade_filter")
                filtered = all_grades.copy()
                if dept_filter != 'All':
                    filtered = filtered[filtered['Department'] == dept_filter]
                if loc_filter != 'All':
                    filtered = filtered[filtered['Location'] == loc_filter]
                if grade_filter != 'All':
                    filtered = filtered[filtered['Grade'] == grade_filter]
                st.dataframe(filtered[['StudentID', 'StudentName', 'Department', 'Course', 'TotalMarks', 'Grade', 'Remark']], use_container_width=True)
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(t['full_report'])
                    full_excel = create_excel_download(filtered, "Full_Grade_Report.xlsx")
                    st.download_button(label=t['download_full'], data=full_excel.getvalue(), file_name="Full_Grade_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                with col2:
                    st.subheader(t['ng_f_report'])
                    ng_f = filtered[filtered['Remark'].isin(['NG', 'Failed'])]
                    if not ng_f.empty:
                        ng_f_excel = create_excel_download(ng_f, "NG_F_Students_Report.xlsx")
                        st.download_button(label=t['download_ng_f'], data=ng_f_excel.getvalue(), file_name="NG_F_Students_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                        st.warning(f"⚠️ {len(ng_f)} students need re-exam!")
                    else:
                        st.success("✅ No NG or F students!")
                st.markdown("---")
                st.subheader(t['monthly_report'])
                col1, col2 = st.columns(2)
                with col1:
                    month_sel = st.selectbox(t['month'], list(range(1,13)), key="reg_month",
                                            format_func=lambda x: t['january'] if x==1 else t['february'] if x==2 else t['march'] if x==3 else t['april'] if x==4 else t['may'] if x==5 else t['june'] if x==6 else t['july'] if x==7 else t['august'] if x==8 else t['september'] if x==9 else t['october'] if x==10 else t['november'] if x==11 else t['december'])
                with col2:
                    year_sel = st.number_input(t['academic_year'], min_value=2020, max_value=2030, value=2025, key="reg_year")
                if st.button(t['generate_monthly'], key="reg_monthly_btn"):
                    monthly_df = get_monthly_ng_report(month_sel, year_sel)
                    if not monthly_df.empty:
                        st.subheader(t['monthly_ng_report'])
                        st.dataframe(monthly_df[['StudentID', 'StudentName', 'Department', 'Course', 'Grade']], use_container_width=True)
                        monthly_excel = create_excel_download(monthly_df, f"Monthly_NG_Report_{month_sel}_{year_sel}.xlsx")
                        st.download_button(label=t['download_monthly'], data=monthly_excel.getvalue(), file_name=f"Monthly_NG_Report_{month_sel}_{year_sel}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                    else:
                        st.info(f"No NG students in {month_sel}/{year_sel}")
                st.markdown("---")
                st.subheader(t['delete_record'])
                ids = all_grades['Id'].tolist()
                if ids:
                    selected_id = st.selectbox(t['select_record'], ids, format_func=lambda x: f"ID: {x}", key="reg_del_select")
                    if st.button(t['delete_btn'], key="reg_del_btn"):
                        success, _ = delete_grade_record(selected_id)
                        if success:
                            st.success(t['delete_success'])
                            st.rerun()
                        else:
                            st.error("Delete failed")
    
    # ---------- DEAN VIEW (unchanged) ----------
    else:
        tab1, tab2, tab3 = st.tabs([t['dashboard'], t['all_grades'], t['reports']])
        with tab1:
            st.subheader(t['dashboard'])
            all_grades = get_all_grades()
            if all_grades.empty:
                st.info(t['no_grades'])
            else:
                total = len(all_grades)
                passed = len(all_grades[all_grades['Remark'] == 'Passed'])
                failed = len(all_grades[all_grades['Remark'] == 'Failed'])
                ng = len(all_grades[all_grades['Remark'] == 'NG'])
                col1, col2, col3, col4 = st.columns(4)
                col1.metric(t['total_students'], total)
                col2.metric(t['passed'], passed, delta=f"{(passed/total*100):.1f}%")
                col3.metric(t['failed'], failed, delta=f"{(failed/total*100):.1f}%")
                col4.metric(t['ng'], ng, delta=f"{(ng/total*100):.1f}%")
                st.subheader(t['by_department'])
                dept_summary = get_department_summary()
                if not dept_summary.empty:
                    dept_melted = dept_summary.melt(id_vars=['Department'], value_vars=['Passed', 'Failed'], var_name='Status', value_name='Count')
                    color_scale = alt.Scale(domain=['Passed', 'Failed'], range=['#28a745', '#dc3545'])
                    chart = alt.Chart(dept_melted).mark_bar().encode(x='Department:N', y='Count:Q', color=alt.Color('Status:N', scale=color_scale), tooltip=['Department', 'Status', 'Count']).properties(height=300)
                    st.altair_chart(chart, use_container_width=True)
                st.subheader(t['grade_distribution'])
                grade_dist = all_grades['Grade'].value_counts().reset_index()
                grade_dist.columns = ['Grade', 'Count']
                grade_colors = {'A+':'#1a8a3a','A':'#28a745','B':'#17a2b8','B-':'#6c8a9a','C':'#ffc107','C-':'#fd7e14','NG':'#ffc107','F':'#dc3545'}
                color_scale = alt.Scale(domain=list(grade_colors.keys()), range=list(grade_colors.values()))
                grade_chart = alt.Chart(grade_dist).mark_bar().encode(x=alt.X('Grade:N', sort=['A+','A','B','B-','C','C-','NG','F']), y='Count:Q', color=alt.Color('Grade:N', scale=color_scale), tooltip=['Grade','Count']).properties(height=300)
                st.altair_chart(grade_chart, use_container_width=True)
                st.subheader("📍 Students by Location")
                loc_dist = all_grades['Location'].value_counts().reset_index()
                loc_dist.columns = ['Location', 'Count']
                loc_chart = alt.Chart(loc_dist).mark_bar(color='#b8860b').encode(x='Location:N', y='Count:Q', tooltip=['Location','Count']).properties(height=250)
                st.altair_chart(loc_chart, use_container_width=True)
        with tab2:
            st.subheader(t['all_grades'])
            all_grades = get_all_grades()
            if all_grades.empty:
                st.info(t['no_grades'])
            else:
                st.dataframe(all_grades[['StudentID', 'StudentName', 'Department', 'Course', 'Location', 'TotalMarks', 'Grade', 'Remark']], use_container_width=True)
        with tab3:
            st.subheader(t['reports'])
            all_grades = get_all_grades()
            if all_grades.empty:
                st.info(t['no_grades'])
            else:
                st.subheader(t['full_report'])
                full_excel = create_excel_download(all_grades, "Full_Grade_Report.xlsx")
                st.download_button(label=t['download_full'], data=full_excel.getvalue(), file_name="Full_Grade_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                st.subheader(t['ng_f_report'])
                ng_f = all_grades[all_grades['Remark'].isin(['NG', 'Failed'])]
                if not ng_f.empty:
                    ng_f_excel = create_excel_download(ng_f, "NG_F_Students_Report.xlsx")
                    st.download_button(label=t['download_ng_f'], data=ng_f_excel.getvalue(), file_name="NG_F_Students_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                    st.warning(f"⚠️ {len(ng_f)} students need re-exam!")
                else:
                    st.success("✅ No NG or F students!")
                st.subheader(t['monthly_report'])
                col1, col2 = st.columns(2)
                with col1:
                    month_sel = st.selectbox(t['month'], list(range(1,13)), key="dean_month", format_func=lambda x: t['january'] if x==1 else t['february'] if x==2 else t['march'] if x==3 else t['april'] if x==4 else t['may'] if x==5 else t['june'] if x==6 else t['july'] if x==7 else t['august'] if x==8 else t['september'] if x==9 else t['october'] if x==10 else t['november'] if x==11 else t['december'])
                with col2:
                    year_sel = st.number_input(t['academic_year'], min_value=2020, max_value=2030, value=2025, key="dean_year")
                if st.button(t['generate_monthly'], key="dean_monthly_btn"):
                    monthly_df = get_monthly_ng_report(month_sel, year_sel)
                    if not monthly_df.empty:
                        st.subheader(t['monthly_ng_report'])
                        st.dataframe(monthly_df[['StudentID', 'StudentName', 'Department', 'Course', 'Grade']], use_container_width=True)
                        monthly_excel = create_excel_download(monthly_df, f"Monthly_NG_Report_{month_sel}_{year_sel}.xlsx")
                        st.download_button(label=t['download_monthly'], data=monthly_excel.getvalue(), file_name=f"Monthly_NG_Report_{month_sel}_{year_sel}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                    else:
                        st.info(f"No NG students in {month_sel}/{year_sel}")

# ---- FOOTER ----
st.markdown("---")
st.caption(t['footer'])

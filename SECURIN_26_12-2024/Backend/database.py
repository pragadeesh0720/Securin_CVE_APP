import sqlite3

def get_db_connection():
    conn = sqlite3.connect('cve_details.db')
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cve_id TEXT NOT NULL UNIQUE,
        description TEXT,
        severity TEXT,
        published_date TEXT,
        last_modified_date TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_cve_data(conn, cve):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO cves (cve_id, description, severity, published_date, last_modified_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (cve['cve_id'], cve['description'], cve['severity'], cve['published_date'], cve['last_modified_date']))
    conn.commit()

def get_cve_by_id(cve_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cves WHERE cve_id = ?
    ''', (cve_id,))
    cve = cursor.fetchone()
    conn.close()
    return cve

def get_all_cves(start_idx=0, results_per_page=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cves LIMIT ? OFFSET ?
    ''', (results_per_page, start_idx))
    cves = cursor.fetchall()
    conn.close()
    return cves

def delete_cve_data(cve_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM cves WHERE cve_id = ?
    ''', (cve_id,))
    conn.commit()
    conn.close()

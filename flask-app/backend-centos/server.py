import os
import time
import psycopg2
from flask import Flask, jsonify
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'postgres'),
                database=os.getenv('DB_NAME', 'appdb'),
                user=os.getenv('DB_USER', 'admin'),
                password=os.getenv('DB_PASSWORD', 'senha123')
            )
            return conn
        except psycopg2.OperationalError as e:
            retries -= 1
            if retries == 0:
                raise e
            time.sleep(2)

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                count INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute('SELECT COUNT(*) FROM visits')
        if cur.fetchone()[0] == 0:
            cur.execute('INSERT INTO visits (count) VALUES (0)')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('UPDATE visits SET count = count + 1, timestamp = CURRENT_TIMESTAMP WHERE id = 1 RETURNING count')
        result = cur.fetchone()
        count = result['count']
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Hello from Backend on CentOS!',
            'visits': count,
            'server': 'CentOS + PostgreSQL'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'service': 'backend-centos', 'database': 'connected'})
    except:
        return jsonify({'status': 'unhealthy', 'service': 'backend-centos', 'database': 'disconnected'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)
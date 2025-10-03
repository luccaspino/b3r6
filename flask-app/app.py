import time
import redis
from flask import Flask, jsonify
import os

app = Flask(__name__)
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return jsonify({
        'message': 'Hello from Flask on Ubuntu!',
        'visits': count,
        'server': 'Ubuntu + Redis'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'flask-ubuntu'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
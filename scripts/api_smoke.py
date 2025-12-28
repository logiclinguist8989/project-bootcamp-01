import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# werkzeug in some environments may miss a __version__ attribute; provide a fallback
try:
    import werkzeug
    if not hasattr(werkzeug, '__version__'):
        werkzeug.__version__ = '1.0.0'
except Exception:
    pass

from backend.app import app

print('Using Flask test client to call endpoints...')
with app.test_client() as client:
    r1 = client.get('/api/letters')
    print('GET /api/letters ->', r1.status_code)
    print(r1.get_json())

    r2 = client.get('/api/rewards')
    print('\nGET /api/rewards ->', r2.status_code)
    print(r2.get_json())

    r3 = client.post('/api/progress', json={'letter': 'A', 'correct': True})
    print('\nPOST /api/progress ->', r3.status_code)
    print(r3.get_json())

    r4 = client.get('/api/rewards')
    print('\nGET /api/rewards (after progress) ->', r4.status_code)
    print(r4.get_json())

from app import create_app
from flask import send_from_directory
import os

app = create_app()

# Route to serve the React app's main index.html
@app.route('/')
@app.route('/<path:path>')
def serve_react(path=''):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Additional route to serve static assets (CSS, JS, etc.)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

if __name__ == '__main__':
    app.run(debug=True)

from app import create_app
from flask import send_from_directory

app = create_app()

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Serve other static files (e.g., CSS, JS)
@app.route('/static/<path:path>')
def send_static(path):
        return send_from_directory(app.static_folder, path)

@app.route('/<path:filename>')
def serve_other_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)

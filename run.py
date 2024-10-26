from app import create_app
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

frontend = os.getenv('FRONTEND', 'http://localhost:3000')

app = create_app()

CORS(app, resources={r"*": {"origins": frontend}})

@app.after_request
def handle_options(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
    return response

if __name__ == '__main__':
    app.run(debug=True)

from app import create_app
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

frontend = os.getenv('FRONTEND', 'http://localhost:3000')

app = create_app()

CORS(app, resources={r"*": {"origins": frontend}})

if __name__ == '__main__':
    app.run(debug=True)

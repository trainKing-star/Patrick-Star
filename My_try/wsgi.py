import os
from dotenv import load_dotenv
from My_flask.extensions import  db

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from My_flask import create_app  # noqa

app = create_app()

if __name__ =='__main__':
    app.run()

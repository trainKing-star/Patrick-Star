import os
from dotenv import load_dotenv
from catchat.extensions import  db#socketio

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from catchat import create_app

app = create_app()

if __name__ == '__main__':
    db.create_all(app)
import sys
from myapp.create_app import create_app
from db import connect_to_db

app = create_app()
MONGO = connect_to_db(app)
# print(sys.path)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

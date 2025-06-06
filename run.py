from app import app
from app.db_init import init_db

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

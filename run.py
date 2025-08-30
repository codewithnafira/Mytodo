from main import app, db
import auth
import todo

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()


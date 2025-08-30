from flask import render_template, request, redirect, flash, url_for
from main import app, db
from datetime import datetime

# Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<{self.sno} --- {self.title}>'

# Todo routes
@app.route('/', methods=['GET', 'POST'])
def todo_home():
    if request.method == 'POST':
        todotitle = request.form.get('todotitle')
        tododesc = request.form.get('tododesc')

        if todotitle:  # prevent empty title
            new_todo = Todo(title=todotitle, desc=tododesc)
            db.session.add(new_todo)
            db.session.commit()
            flash("Todo added successfully!", "success")
            return redirect(url_for('todo_home'))

        flash("Title cannot be empty!", "danger")

    todos = Todo.query.all()
    return render_template("home.html", todos=todos)


@app.route('/delete/<int:sno>')
def delete_todo(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted!", "info")
    return redirect(url_for('todo_home'))
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update_todo(sno):
    todo = Todo.query.get_or_404(sno)

    if request.method == 'POST':
        new_title = request.form.get('todotitle')
        new_desc = request.form.get('tododesc')

        if new_title:
            todo.title = new_title
            todo.desc = new_desc
            db.session.commit()
            flash("Todo updated successfully!", "success")
            return redirect(url_for('todo_home'))
        else:
            flash("Title cannot be empty!", "danger")

    # GET request → show update form
    return render_template("update.html", todo=todo)

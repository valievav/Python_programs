from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# db config and init
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # relative path
db = SQLAlchemy(app)


# model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'<Task {self.id}'


# view
@app.route('/', methods=['POST', 'GET'])
def tasks():

    if request.method == "POST":
        content = request.form['content']
        new_task = Todo(content=content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'There was an issue adding the task. {e}'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>/')
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting the task."


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update_task(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
        except:
            return "There was an issue updating the task."

        return redirect('/')
    else:
        return render_template('update.html', task=task_to_update)


if __name__ == "__main__":
    db.create_all()
    app.run()

from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,nullable=False, default=datetime.now)
    task = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean, default=False)

#db.create_all()

# new_task = Todo( 
#     task= "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Modi, eligendi nemo! Possimus, officia quo. Nisi voluptatum impedit magni quisquam voluptas ea repellendus placeat, odio delectus dolorum iusto atque? Dignissimos, accusamus."
#     )
# db.session.add(new_task)
# db.session.commit()



@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_task = Todo( 
            task=  request.form.get('tsk')
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    tasks = Todo.query.filter_by(is_done=False)
    task_complete = Todo.query.filter_by(is_done=True)
    return render_template("index.html", tasks=tasks, task_done=task_complete)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    id_ = task_id
    task_to_delete = Todo.query.get(id_)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/complete/<task_id>")
def done(task_id):
    update_task = Todo.query.get(task_id)
    update_task.is_done = True
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database config: SQLite file under instance/firstapp.db
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance')
os.makedirs(db_path, exist_ok=True)  # ensure instance directory exists
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'firstapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------- Model ---------
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Person {self.id} {self.first_name} {self.last_name}>"

# create the DB if necessary
@app.before_request
def create_tables():
    db.create_all()

# --------- Routes ---------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Create new person
        fn = request.form.get('first_name', '').strip()
        ln = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age') or None
        if age:
            try:
                age = int(age)
            except ValueError:
                age = None

        if fn and ln and email:
            new_person = Person(first_name=fn, last_name=ln, email=email, age=age)
            db.session.add(new_person)
            db.session.commit()
            return redirect(url_for('index'))

    people = Person.query.order_by(Person.id).all()
    return render_template('index.html', people=people)

@app.route('/delete/<int:person_id>', methods=['POST'])
def delete(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:person_id>', methods=['GET', 'POST'])
def update(person_id):
    person = Person.query.get_or_404(person_id)
    if request.method == 'POST':
        person.first_name = request.form.get('first_name', person.first_name).strip()
        person.last_name = request.form.get('last_name', person.last_name).strip()
        person.email = request.form.get('email', person.email).strip()
        age = request.form.get('age')
        if age:
            try:
                person.age = int(age)
            except ValueError:
                person.age = None
        else:
            person.age = None
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', person=person)

if __name__ == '__main__':
    # For development only. In production use a WSGI server.
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database config: SQLite file under instance/firstapp.db
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance')
os.makedirs(db_path, exist_ok=True)  # ensure instance directory exists
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'firstapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------- Model ---------
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Person {self.id} {self.first_name} {self.last_name}>"

# create the DB if necessary
@app.before_request
def create_tables():
    db.create_all()

# --------- Routes ---------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Create new person
        fn = request.form.get('first_name', '').strip()
        ln = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age') or None
        if age:
            try:
                age = int(age)
            except ValueError:
                age = None

        if fn and ln and email:
            new_person = Person(first_name=fn, last_name=ln, email=email, age=age)
            db.session.add(new_person)
            db.session.commit()
            return redirect(url_for('index'))

    people = Person.query.order_by(Person.id).all()
    return render_template('index.html', people=people)

@app.route('/delete/<int:person_id>', methods=['POST'])
def delete(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:person_id>', methods=['GET', 'POST'])
def update(person_id):
    person = Person.query.get_or_404(person_id)
    if request.method == 'POST':
        person.first_name = request.form.get('first_name', person.first_name).strip()
        person.last_name = request.form.get('last_name', person.last_name).strip()
        person.email = request.form.get('email', person.email).strip()
        age = request.form.get('age')
        if age:
            try:
                person.age = int(age)
            except ValueError:
                person.age = None
        else:
            person.age = None
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', person=person)

if __name__ == '__main__':
    # For development only. In production use a WSGI server.
    app.run(debug=True)
>>>>>>> e196385 (Initial commit)

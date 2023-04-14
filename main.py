from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Create the database instance
db = SQLAlchemy(app)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    #todos = db.Column(db.PickleType)
    todo = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Todo {self.title}>'



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', err="")
    else:
         email = request.form['email']
         password = request.form['password']
         # Perform login logic here
         user = User.query.filter_by(email=email).first()
         if user is None:
             return render_template('login.html', errr="Email not Found. please register!")
         if password != user.password:
             return render_template('login.html', errr="Wrong password")
         session['email'] = email
         return redirect(url_for('pg'))
         


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return(render_template('register.html', err_mssg=""))
    email = request.form['email']
    password = request.form['password']

    # Check if the email is already in use
    if User.query.filter_by(email=email).first():
        return render_template("register.html", err_mssg="Error: Email address is already in use")
    
    #create ze empty tasks
    hisData = {}

    # Create a new User object
    new_user = User(email=email, password=password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return f'User with email {email} has been created and pass is {password}. You have successfully signed up. For security reasons please sign in by returning to our site.'

@app.route('/pg', methods=["GET", "POST"])
def pg():
    if request.method == "GET":
        email = session.get('email')
        user = User.query.filter_by(email=email).first()
        tasks = Todo.query.filter_by(user_id=user.id).all()

       # hisData = user.todos
        if email:
            return render_template('pg.html', user=email, tasks=tasks)
        else:
            return 'hackers gonna hack hack hack, imma just....HEYYYY GET OUT OF MY SINGING PAGE HACKER.'
    else:
        email = session.get('email')
        user = User.query.filter_by(email=email).first()
        title = request.form['titleR']
        new_todo = Todo(title=title)
        user.todo.append(new_todo)
        db.session.commit()
        return redirect(url_for('pg'))

@app.route('/clear_todos', methods=["POST"])
def clear_todos():
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    user.todo = []
    db.session.commit()
    return redirect(url_for('pg'))


        
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)


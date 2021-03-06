# Imports for client
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from emailValidator import checkUobEmail
from orchestrators import Orchestrator
from printers import Printer
from jobs import Job

from queue import Queue

waiting_q = Queue(maxsize=0)
printing_q = Queue(maxsize=0)


import threading
app = Flask(__name__)

# App config for login and DB
app.config['SECRET_KEY'] = 'helloworld'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'

# Config for upload
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['g', 'gcode'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initialise bootstrap and DB
Bootstrap(app)
db = SQLAlchemy(app)

# Config login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

printers = [
    # Printer('Ultimaker 2+ (1)',    '192.168.0.201', 'B5A36115A3DC49148EFC52012E7EBCD9',
    #         'Hackspace', 'duplicator',   'PLA', 'red'),
    # Printer('Ultimaker 2+ (2)', '192.168.0.202', 'ED7F718BBE11456BA3619A04C66EF74A',
    #         'Hackspace', 'Ultimaker 2+', 'PLA', 'red')
]
orchestrator = Orchestrator(printers)
# Printer('Ultimaker 2+ (1)',    '192.168.0.201', 'B5A36115A3DC49148EFC52012E7EBCD9',
#         'Hackspace', 'duplicator',   'PLA', 'red'),
# Printer('Ultimaker 2+ (2)', '192.168.0.202', 'ED7F718BBE11456BA3619A04C66EF74A',
#         'Hackspace', 'Ultimaker 2+', 'PLA', 'red')
worker_thread = threading.Thread(target=orchestrator.run, args=(waiting_q, printing_q, ))
worker_thread.start()

# ADMIN

admin = admin = Admin(app)

# DB ENTRIES


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    faculty = db.Column(db.String(80))
    password = db.Column(db.String(80))


class Printers(BaseView):
    @expose('/')
    def printers(self):
        return self.render('/admin/printers.html', printer_list=make_printer_advanced_info())


class jobQueue(BaseView):
    @expose('/')
    def jobqueue(self):
        return self.render('/admin/jobQueue.html', job_list=make_jobs_list())

# class IFrame(BaseView):
#     @expose('/iframe/')
#     def index(self):
#         return self.render('admin/iframe.html', printers)


admin.add_view(ModelView(User, db.session))
admin.add_view(Printers(name='Printers', endpoint='printers'))
admin.add_view(jobQueue(name='Job Queue', endpoint='jobQueue'))

# FORM ENTRIES


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class loginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


valid_emails = ["my.bristol.ac.uk", "bristol.ac.uk"]


class registerForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50), checkUobEmail()])
    faculty = StringField('faculty', validators=[InputRequired(), Length(max=80)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class uploadForm(FlaskForm):
    colour = SelectField('Filament colour', choices=[('r', 'Red'), ('b', 'Black'), ('g', 'Grey')])
    material = SelectField('Filament material', choices=[(
        'pla', 'PLA'), ('abs', 'ABS'), ('ninja', 'NinjaFlex')])
    gcode = FileField('gcode file', validators=[
        FileRequired()])


def make_printer_info():
    printer_info = []
    for printer in printers:
        printer_info.append([printer.name, printer.location, printer.simple_status()])
    return printer_info


def make_printer_advanced_info():
    global printers

    printer_info = []
    for printer in printers:
        printer_info.append([printer.name, printer.location, printer.simple_status(), printer.url])
    return printer_info

# APP ROUTES


@app.route('/')
def index():
    return render_template('index.html', printer_list=make_printer_info())


@app.route('/testupload', methods=['GET', 'POST'])
def testUpload():
    form = uploadForm()
    if form.validate_on_submit():
        colour = form.colour.data
        material = form.material.data
        gcode = form.gcode.data
        filename = secure_filename(gcode.filename)
        gcode.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "working"
    return render_template('testUpload.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        flash('Invalid username or password')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = registerForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, faculty=form.faculty.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('New user created')
        return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)


def make_jobs_list():

    unformatted_jobs = list(printing_q.queue) + list(waiting_q.queue)  # TODO: Is this right?

    job_list = []
    for job in unformatted_jobs:
        if job.time_remaining is not 'Pending':
            new_time = str(int(job.time_remaining.split(' ')[0]) - 1) + " mins"
            job.time_remaining = new_time

        printer = job.printing_on
        if (printer == None):
            stream_url = '#'
        else:
            stream_url = printer.url + '/webcam/?action=stream'
        job_list.append([job.filename.split('/')[-1], job.user.username,
                         job.location, job.time_remaining, stream_url])

    return job_list


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', name=current_user.username, job_list=make_jobs_list())


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No file part")
            return render_template('dashboard/upload.html')
        user_file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if user_file.filename == '':
            flash("No file extension")
            return render_template('dashboard/upload.html')
        if not allowed_file(user_file.filename):
            flash("Invalid file extension")
            return render_template('dashboard/upload.html')
        if user_file and allowed_file(user_file.filename):
            filename = secure_filename(user_file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            user_file.save(path)
            new_job = Job(path, 'black', 'PLA', current_user)

            waiting_q.put(new_job)

            flash("File uploaded succesfully")
            return render_template('dashboard/upload.html')
    return render_template('dashboard/upload.html')


@app.route('/history')
@login_required
def history():
    return render_template('dashboard/history.html',  name=current_user.username)


@app.route('/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html', name=current_user.username, email=current_user.email, faculty=current_user.faculty)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Job, Internship, Alumni

# ---- INIT APP ----
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail = Mail(app)

# ---- LOGIN MANAGER ----
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# ==============================
#         PUBLIC ROUTES
# ==============================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/jobs')
def jobs():
    search = request.args.get('search', '')
    job_type = request.args.get('job_type', '')
    location = request.args.get('location', '')

    query = Job.query
    if search:
        query = query.filter(Job.title.ilike(f'%{search}%') | Job.company.ilike(f'%{search}%'))
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))

    all_jobs = query.order_by(Job.posted_at.desc()).all()
    return render_template('jobs.html', jobs=all_jobs, search=search, job_type=job_type, location=location)

@app.route('/internships')
def internships():
    search = request.args.get('search', '')
    location = request.args.get('location', '')

    query = Internship.query
    if search:
        query = query.filter(Internship.title.ilike(f'%{search}%') | Internship.company.ilike(f'%{search}%'))
    if location:
        query = query.filter(Internship.location.ilike(f'%{location}%'))

    all_internships = query.order_by(Internship.posted_at.desc()).all()
    return render_template('internships.html', internships=all_internships, search=search, location=location)

@app.route('/alumni')
def alumni():
    all_alumni = Alumni.query.order_by(Alumni.graduation_year.desc()).all()
    return render_template('alumni.html', alumni=all_alumni)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message_body = request.form['message']

        try:
            msg = Message(
                subject=f'[EICT Portal] {subject}',
                recipients=[app.config['MAIL_USERNAME']],
                body=f'''
New message from EICT Portal Contact Form
==========================================
Name:    {name}
Email:   {email}
Subject: {subject}

Message:
{message_body}
==========================================
                ''',
                reply_to=email
            )
            mail.send(msg)
            flash('Your message has been sent! We will get back to you soon.', 'success')
        except Exception as e:
            flash('Message could not be sent. Please try again later.', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cover_letter = request.form['cover_letter']

        try:
            msg = Message(
                subject=f'[EICT Portal] New Application — {job.title} at {job.company}',
                recipients=[app.config['MAIL_USERNAME']],
                body=f'''
New Job Application via EICT Portal
=====================================
Position:  {job.title}
Company:   {job.company}
Location:  {job.location}

Applicant Details:
Name:      {name}
Email:     {email}
Phone:     {phone}

Cover Letter:
{cover_letter}
=====================================
                ''',
                reply_to=email
            )
            mail.send(msg)
            flash(f'Application submitted for {job.title}! Good luck!', 'success')
        except Exception as e:
            flash('Application could not be sent. Please try again.', 'danger')

        return redirect(url_for('jobs'))

    return render_template('apply.html', job=job)


@app.route('/apply-internship/<int:internship_id>', methods=['GET', 'POST'])
def apply_internship(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cover_letter = request.form['cover_letter']

        try:
            msg = Message(
                subject=f'[EICT Portal] Internship Application — {internship.title} at {internship.company}',
                recipients=[app.config['MAIL_USERNAME']],
                body=f'''
New Internship Application via EICT Portal
============================================
Position:  {internship.title}
Company:   {internship.company}
Duration:  {internship.duration}

Applicant Details:
Name:      {name}
Email:     {email}
Phone:     {phone}

Cover Letter:
{cover_letter}
============================================
                ''',
                reply_to=email
            )
            mail.send(msg)
            flash(f'Application submitted for {internship.title}! Good luck!', 'success')
        except Exception as e:
            flash('Application could not be sent. Please try again.', 'danger')

        return redirect(url_for('internships'))

    return render_template('apply_internship.html', internship=internship)


# ==============================
#         AUTH ROUTES
# ==============================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ==============================
#         ADMIN ROUTES
# ==============================

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access only.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_jobs = Job.query.count()
    total_internships = Internship.query.count()
    total_alumni = Alumni.query.count()
    total_users = User.query.count()
    recent_jobs = Job.query.order_by(Job.posted_at.desc()).limit(5).all()
    recent_internships = Internship.query.order_by(Internship.posted_at.desc()).limit(5).all()
    return render_template('admin.html',
        total_jobs=total_jobs,
        total_internships=total_internships,
        total_alumni=total_alumni,
        total_users=total_users,
        recent_jobs=recent_jobs,
        recent_internships=recent_internships)


@app.route('/admin/add-job', methods=['GET', 'POST'])
@login_required
@admin_required
def add_job():
    if request.method == 'POST':
        job = Job(
            title=request.form['title'],
            company=request.form['company'],
            location=request.form['location'],
            description=request.form['description'],
            requirements=request.form['requirements'],
            job_type=request.form['job_type']
        )
        db.session.add(job)
        db.session.commit()
        flash('Job listing added!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_job.html')


@app.route('/admin/add-internship', methods=['GET', 'POST'])
@login_required
@admin_required
def add_internship():
    if request.method == 'POST':
        internship = Internship(
            title=request.form['title'],
            company=request.form['company'],
            location=request.form['location'],
            description=request.form['description'],
            duration=request.form['duration'],
            stipend=request.form['stipend']
        )
        db.session.add(internship)
        db.session.commit()
        flash('Internship added!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_internship.html')


@app.route('/admin/add-alumni', methods=['GET', 'POST'])
@login_required
@admin_required
def add_alumni():
    import os
    from werkzeug.utils import secure_filename

    if request.method == 'POST':
        photo = request.files.get('photo')
        photo_filename = None

        if photo and photo.filename != '':
            filename = secure_filename(photo.filename)
            upload_folder = os.path.join(app.static_folder, 'images', 'alumni')
            os.makedirs(upload_folder, exist_ok=True)
            photo.save(os.path.join(upload_folder, filename))
            photo_filename = filename

        person = Alumni(
            name=request.form['name'],
            graduation_year=request.form['graduation_year'],
            course=request.form['course'],
            current_job=request.form['current_job'],
            company=request.form['company'],
            linkedin=request.form['linkedin'],
            bio=request.form['bio'],
            photo=photo_filename
        )
        db.session.add(person)
        db.session.commit()
        flash('Alumni profile added!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_alumni.html')


@app.route('/admin/delete-job/<int:id>')
@login_required
@admin_required
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted.', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete-internship/<int:id>')
@login_required
@admin_required
def delete_internship(id):
    internship = Internship.query.get_or_404(id)
    db.session.delete(internship)
    db.session.commit()
    flash('Internship deleted.', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete-alumni/<int:id>')
@login_required
@admin_required
def delete_alumni(id):
    person = Alumni.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    flash('Alumni profile deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
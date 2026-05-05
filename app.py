from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Job, Internship, Alumni

# ---- INIT APP ----
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

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
    all_jobs = Job.query.order_by(Job.posted_at.desc()).all()
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/internships')
def internships():
    all_internships = Internship.query.order_by(Internship.posted_at.desc()).all()
    return render_template('internships.html', internships=all_internships)

@app.route('/alumni')
def alumni():
    all_alumni = Alumni.query.order_by(Alumni.graduation_year.desc()).all()
    return render_template('alumni.html', alumni=all_alumni)

# ==============================
#         AUTH ROUTES
# ==============================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

        # Hash the password before saving
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
    """Custom decorator to protect admin pages"""
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
        flash('Job listing added successfully!', 'success')
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
        flash('Internship added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_internship.html')


@app.route('/admin/add-alumni', methods=['GET', 'POST'])
@login_required
@admin_required
def add_alumni():
    if request.method == 'POST':
        person = Alumni(
            name=request.form['name'],
            graduation_year=request.form['graduation_year'],
            course=request.form['course'],
            current_job=request.form['current_job'],
            company=request.form['company'],
            linkedin=request.form['linkedin'],
            bio=request.form['bio']
        )
        db.session.add(person)
        db.session.commit()
        flash('Alumni profile added successfully!', 'success')
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


# ---- RUN ----
if __name__ == '__main__':
    app.run(debug=True)
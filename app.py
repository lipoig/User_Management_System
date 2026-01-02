from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'D6451EB533AF93F2248EFD1C2B3B4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    year_of_birth = db.Column(db.Integer)
    description = db.Column(db.Text)
    photo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Admin Routes
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if Admin.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('admin_register'))
        
        hashed_password = generate_password_hash(password)
        new_admin = Admin(username=username, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        
        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin_login'))
    
    return render_template('admin_register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            session['is_admin'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('admin_login'))
    
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin/create_user', methods=['POST'])
def create_user():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    username = request.form['username']
    password = request.form['password']
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists!', 'error')
        return redirect(url_for('admin_dashboard'))
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    flash('User created successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/view_user/<int:user_id>')
def view_user(user_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    user = User.query.get_or_404(user_id)
    return render_template('view_user.html', user=user)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    user = User.query.get_or_404(user_id)
    
    # Delete user's photo if exists
    if user.photo:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], user.photo)
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    session.pop('is_admin', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# User Routes
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_username'] = user.username
            session['is_admin'] = False
            flash('Logged in successfully!', 'success')
            return redirect(url_for('user_profile'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('user_login.html')

@app.route('/user/profile', methods=['GET', 'POST'])
def user_profile():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('user_login'))
    
    user = User.query.get_or_404(session['user_id'])
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.year_of_birth = request.form['year_of_birth'] if request.form['year_of_birth'] else None
        user.description = request.form['description']
        
        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old photo if exists
                if user.photo:
                    old_photo = os.path.join(app.config['UPLOAD_FOLDER'], user.photo)
                    if os.path.exists(old_photo):
                        os.remove(old_photo)
                
                filename = secure_filename(f"user_{user.id}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.photo = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user_profile'))
    
    return render_template('user_profile.html', user=user)

@app.route('/user/logout')
def user_logout():
    session.pop('user_id', None)
    session.pop('user_username', None)
    session.pop('is_admin', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
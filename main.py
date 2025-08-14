from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
CORS(app)  # Allows frontend to communicate with backend

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Video Model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username, email, password = data['username'], data['email'], data['password']
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Signup successful'}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        login_user(user)
        return jsonify({'message': 'Login successful!', 'user_id': user.id})
    return jsonify({'error': 'Invalid credentials'}), 401

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

# Upload Video Route
UPLOAD_FOLDER = 'static/videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'video' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['video']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    new_video = Video(filename=file.filename, uploader_id=current_user.id)
    db.session.add(new_video)
    db.session.commit()
    return jsonify({'message': 'Upload successful'}), 200

# Fetch Videos Route
@app.route('/videos', methods=['GET'])
@login_required
def videos():
    videos = Video.query.filter_by(uploader_id=current_user.id).all()
    return jsonify({'videos': [{'id': v.id, 'filename': v.filename} for v in videos]})

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory, render_template

@app.route('/')
def home():
    return send_from_directory('.', 'frontend.html')  # Serves your frontend file

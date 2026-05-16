import os
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB setup
from database import db
from database.models import users, reports

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.keras")

model = load_model(MODEL_PATH)

print("Model loaded. Running at http://127.0.0.1:5000/")

# Labels for prediction
labels = {0: 'Healthy', 1: 'Powdery', 2: 'Rust'}

# Prediction function
def getResult(image_path):
    img = load_img(image_path, target_size=(225, 225))
    x = img_to_array(img)
    x = x.astype('float32') / 255.
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)[0]
    return preds

# ---------- ROUTES ---------- #

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            flash("Login successful!")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if users.find_one({"email": email}):
            flash("User already exists with this email. Please log in.")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)

        users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('home'))

    user = users.find_one({"_id": ObjectId(session['user_id'])})
    user_reports = list(reports.find({"user_id": user["_id"]}))
    return render_template('dashboard.html', user=user, reports=user_reports)


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.route('/input')
def input_page():
    if 'user_id' not in session:
        flash("Please log in to access the input page.")
        return redirect(url_for('home'))
    return render_template('input.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files or 'user_id' not in session:
        flash("Please upload a file and log in to proceed.")
        return redirect(url_for('input_page'))

    file = request.files['file']
    if file.filename == '':
        flash("No file selected.")
        return redirect(url_for('input_page'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    preds = getResult(file_path)
    predicted_label = labels[np.argmax(preds)]
    current_datetime = datetime.now()

    reports.insert_one({
        "user_id": ObjectId(session['user_id']),
        "image_name": filename,
        "prediction": predicted_label,
        "date": current_datetime
    })

    flash(f"Prediction: {predicted_label}")
    return render_template('input.html', prediction=predicted_label, image_path=filename)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
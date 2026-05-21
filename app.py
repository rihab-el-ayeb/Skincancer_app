import os, time, mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import h5py
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change in production
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db_config = {'host':'localhost','user':'root','password':'','database':'skin_cancer_db'}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ------------------------------------------------------------------
# Load model by extracting architecture from .h5 file (TF 2.8 compatible)
# ------------------------------------------------------------------
MODEL_PATH = 'model/vgg16_malignant_vs_benign.h5'

def load_model_from_h5(filepath):
    """Load a Keras model saved with model.save() in a newer TF version."""
    with h5py.File(filepath, 'r') as f:
        # Check if it's a full model (has 'model_config')
        if 'model_config' in f.attrs:
            config = f.attrs['model_config']
            if isinstance(config, bytes):
                config = config.decode('utf-8')
            # Parse JSON config
            config_dict = json.loads(config)
            # Rebuild model from config
            model = tf.keras.models.model_from_json(json.dumps(config_dict))
            # Load weights
            weights_loaded = model.load_weights(filepath, by_name=True, skip_mismatch=False)
            print("Model rebuilt from config and weights loaded.")
            return model
        else:
            raise ValueError("No model_config found in the .h5 file. It might be weights-only.")

try:
    model = load_model_from_h5(MODEL_PATH)
    print("✅ Model loaded successfully using architecture extraction.")
    # Quick sanity test
    dummy = np.random.rand(1,224,224,3)
    dummy_pred = model.predict(dummy)[0][0]
    print(f"Sanity check (random input) → output: {dummy_pred:.4f}")
except Exception as e:
    print("❌ Failed to load model using config extraction:", e)
    print("Falling back to manual VGG16 architecture + load_weights")
    # Fallback: manual rebuild
    from tensorflow.keras.applications import VGG16
    from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
    input_tensor = Input(shape=(224,224,3))
    base = VGG16(weights=None, include_top=False, input_tensor=input_tensor)
    x = base.output
    x = GlobalAveragePooling2D()(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base.input, outputs=predictions)
    model.load_weights(MODEL_PATH, by_name=True, skip_mismatch=True)
    print("Fallback: loaded weights into manual VGG16 architecture.")

# ------------------------------------------------------------------
def allowed_file(fn):
    return '.' in fn and fn.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def predict_skin_cancer(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)   # VGG16 preprocessing (mean subtraction)
    pred = model.predict(arr)[0][0]
    return ("Malin", pred*100) if pred >= 0.5 else ("Bénin", (1-pred)*100)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname,pwd))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Identifiants invalides")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM patients")
    total_patients = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM patients WHERE result='Malin'")
    malignant_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template('dashboard.html', total_patients=total_patients, malignant_count=malignant_count)

@app.route('/predict', methods=['GET','POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        file = request.files['image']
        if file and allowed_file(file.filename):
            fname = secure_filename(file.filename)
            fname = f"{os.path.splitext(fname)[0]}_{int(time.time())}{os.path.splitext(fname)[1]}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            file.save(path)
            result, prob = predict_skin_cancer(path)
            db_path = f"{UPLOAD_FOLDER}/{fname}"
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO patients (name,age,result,probability,image_path) VALUES (%s,%s,%s,%s,%s)",
                        (name, age, result, prob/100.0, db_path))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('result.html', result=result, prob=prob, img_path=db_path)
        else:
            flash("Format d'image non supporté")
            return redirect(url_for('predict'))
    return render_template('predict.html')

@app.route('/patients')
def patients():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM patients ORDER BY created_at DESC")
    patients = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('patients.html', patients=patients)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

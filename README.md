# Skin Cancer AI Prediction App

A web-based application for automated skin cancer classification using deep learning. The app allows medical professionals to upload dermatoscopic images of skin lesions and receive AI-powered predictions classifying them as **Benign** or **Malignant**, along with a confidence score.

## Features

- **AI-Powered Diagnosis**: Uses a fine-tuned VGG16 Convolutional Neural Network to classify skin lesions.
- **Patient Management**: Store and manage patient records including name, age, diagnosis result, and confidence probability.
- **Dashboard Analytics**: Overview of total patients analyzed and count of malignant cases detected.
- **Image Upload & Preview**: Drag-and-drop image upload with instant preview functionality.
- **Searchable History**: Search and filter through past patient diagnosis records.
- **Secure Authentication**: Session-based login system for authorized access.
- **Responsive UI**: Modern glassmorphism design with Bootstrap 5, optimized for desktop and mobile.

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python, Flask |
| **Deep Learning** | TensorFlow / Keras (VGG16 architecture) |
| **Database** | MySQL |
| **Frontend** | HTML5, Jinja2 Templates, Bootstrap 5, FontAwesome |
| **Styling** | Custom CSS with Glassmorphism effects |

## Project Structure

```
├── app.py                          # Main Flask application
├── download_model.py               # Script to download VGG16 base weights
├── database.sql                    # MySQL schema and default admin user
├── model/
│   └── vgg16_malignant_vs_benign.h5   # Trained model weights
├── static/
│   ├── style.css                   # Custom glassmorphism styles
│   ├── script.js                   # Frontend interactivity
│   └── uploads/                    # Uploaded lesion images
└── templates/
    ├── base.html                   # Base layout with Bootstrap
    ├── login.html                  # Authentication page
    ├── dashboard.html              # Analytics dashboard
    ├── predict.html                # New analysis form
    ├── result.html                 # Diagnosis result display
    └── patients.html               # Patient history table
```

## Prerequisites

- Python 3.8+
- MySQL Server
- pip package manager

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/skin-cancer-ai.git
cd skin-cancer-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask tensorflow keras numpy pillow mysql-connector-python h5py werkzeug
```

### 4. Setup MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Execute the schema script
source database.sql
```

Default admin credentials:
- **Username**: `admin`
- **Password**: `1234`

### 5. Prepare the Model

Place your trained model file at:
```
model/vgg16_malignant_vs_benign.h5
```

If you need the base VGG16 weights, run:
```bash
python download_model.py
```

### 6. Run the Application

```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Usage Guide

1. **Login** using the default admin credentials.(path/to/login_page.png)
2. **Dashboard** shows total patients and malignant case statistics.(path/to/dashboard.png)
3. Click **New Analysis** to upload a patient's lesion image.(path/to/analysis_page.png)
4. Fill in patient name and age, then select an image file (PNG, JPG, JPEG, GIF).
5. View the **Diagnosis Result** showing:
   - Classification: *Bénin* (Benign) or *Malin* (Malignant)
   - Confidence percentage
   
6. Access **Patient History** to view, search, and review all past diagnoses.(path/to/dashboard.png)

## Model Details

- **Architecture**: VGG16 (Visual Geometry Group 16-layer)
- **Input Size**: 224×224 pixels
- **Preprocessing**: VGG16 standard preprocessing (mean subtraction)
- **Output**: Single sigmoid neuron (0 = Benign, 1 = Malignant)
- **Fallback Loading**: If the model file was saved in a newer TensorFlow version, the app automatically extracts the architecture from the H5 file and rebuilds the model.

## Database Schema

### Users Table
| Column     | Type         | Description          |
|------------|--------------|----------------------|
| id         | INT (PK)     | Auto-increment ID    |
| username   | VARCHAR(50)  | Unique username      |
| password   | VARCHAR(50)  | User password        |

### Patients Table
| Column       | Type          | Description                    |
|--------------|---------------|--------------------------------|
| id           | INT (PK)      | Auto-increment ID              |
| name         | VARCHAR(100)  | Patient full name              |
| age          | INT           | Patient age                    |
| result       | VARCHAR(20)   | Diagnosis: 'Bénin' or 'Malin'  |
| probability  | FLOAT         | Raw model probability (0-1)    |
| image_path   | VARCHAR(255)  | Path to uploaded image         |
| created_at   | TIMESTAMP     | Record creation time           |

## Configuration

Edit `db_config` in `app.py` to match your MySQL credentials:

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'skin_cancer_db'
}
```

## Important Notes

> **Disclaimer**: This application is for educational and research purposes only. It is **not** intended for clinical diagnosis. Always consult a certified dermatologist for medical advice.

- The default secret key should be changed in production.
- Passwords are stored in plain text for demonstration — use hashed passwords (e.g., bcrypt) in production.
- Ensure the `static/uploads` directory has appropriate write permissions.

## Screenshots

*(Add screenshots of login, dashboard, prediction, and results pages here)*

## License

This project is licensed under the MIT License.

## Acknowledgments

- [TensorFlow](https://www.tensorflow.org/) & [Keras](https://keras.io/) for deep learning frameworks
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap 5](https://getbootstrap.com/) for responsive UI components
- VGG16 architecture by [Karen Simonyan & Andrew Zisserman](https://arxiv.org/abs/1409.1556)

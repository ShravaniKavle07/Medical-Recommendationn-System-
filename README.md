# 🏥 Healthcare Recommendation System

## 📌 Project Overview
The **Healthcare Recommendation System** is a machine learning-based web application that predicts diseases based on patient symptoms and provides personalized medical recommendations.

It integrates **authentication, real-time analytics, and recommendation algorithms** into an interactive dashboard built using Streamlit.

---

## 🚀 Features

### 🔐 User Management
- JWT-based authentication (Login/Signup)
- Secure password hashing using bcrypt
- Role-based access (Admin & User)

### 🤖 Machine Learning
- Disease prediction using trained ML model (Random Forest)
- Pre-trained model loaded via joblib
- Cleaned and preprocessed dataset

### 🔍 Recommendation System
- Content-based filtering using cosine similarity
- Finds similar patient cases dynamically
- Suggests relevant treatments

### 📊 Dashboard & Analytics
- Disease distribution visualization
- Risk-level analysis
- Real-time activity tracking

### 👨‍⚕️ Admin Panel
- View registered users
- Monitor user activity logs

---

## 🧠 Tech Stack

| Category | Tools Used |
|--------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| ML Library | scikit-learn |
| Database | SQLite |
| Authentication | JWT, bcrypt |
| Data Processing | Pandas, NumPy |

---

## 📂 Project Structure

Healthcare-Recommendation-System/
│
├── medi_app.py
├── model.pkl
├── Cleaned_Dataset.csv
├── healthcare.db
├── requirements.txt
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

git clone https://github.com/your-username/healthcare-recommendation-system.git
cd healthcare-recommendation-system

### 2️⃣ Install Dependencies

pip install -r requirements.txt

### 3️⃣ Run Application

streamlit run medi_app.py

---

## 📊 Dataset Description
The dataset includes:
- Fever
- Cough
- Fatigue
- Difficulty Breathing
- Age
- Blood Pressure
- Cholesterol Level
- Disease
- Risk Level

---

## 🔄 Data Preprocessing
- Handling missing values (forward fill)
- Encoding categorical values (Yes/No → 1/0)
- Label encoding for gender
- Feature selection

---

## 📈 Machine Learning Model
- Algorithm: Random Forest Classifier
- Input: Patient health data
- Output: Predicted disease

---

## 🔍 Recommendation Logic
- Uses cosine similarity
- Matches input with similar patient records
- Returns top similar cases

---

## 🔐 Security Features
- JWT-based authentication
- Password hashing (bcrypt)
- Session management

---

## 📊 Dashboard Features
- Disease distribution charts
- Risk-level analysis
- Activity tracking

---

## 🚀 Future Enhancements
- Deep learning integration
- Real hospital dataset integration
- Mobile app support
- Cloud deployment

---

## 🎓 Use Cases
- Healthcare analytics
- Clinical decision support
- ML academic projects

---

## 👩‍💻 Author
Shravani Kavle

---

## ⭐ Acknowledgements
- scikit-learn
- Streamlit
- Open-source datasets

---

## 📜 License
This project is for educational purposes only.

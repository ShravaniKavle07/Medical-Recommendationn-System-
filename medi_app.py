import streamlit as st
import pandas as pd
import sqlite3
import datetime
import bcrypt
from jose import jwt
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# CONFIG
# =========================
SECRET = "secretkey"

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("healthcare.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password BLOB,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    timestamp TEXT
)
""")
conn.commit()

# =========================
# SECURITY
# =========================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def create_token(username, role):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None

def log_action(user, action):
    cursor.execute("INSERT INTO logs VALUES (NULL, ?, ?, ?)",
                   (user, action, str(datetime.datetime.now())))
    conn.commit()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Dataset.csv")
    df.ffill(inplace=True)
    return df

df = load_data()

# =========================
# CLEANING (FINAL FIX)
# =========================
# =========================
# CLEANING (FINAL FIX)
# =========================

binary_cols = ['fever','cough','fatigue','difficulty_breathing']

for col in binary_cols:
    df[col] = df[col].astype(str).str.strip().str.lower()   # normalize text
    df[col] = df[col].replace({'yes':1, 'no':0})            # map all cases

# Convert ALL remaining values to numeric
df[binary_cols] = df[binary_cols].apply(pd.to_numeric, errors='coerce')

# Fill missing safely
df[binary_cols] = df[binary_cols].fillna(0)

# =========================
# FEATURES
# =========================
# Ensure numeric
features = ['fever','cough','fatigue','difficulty_breathing',
            'age','blood_pressure','cholesterol_level']

X = df[features].copy()

# Force numeric conversion
X = X.apply(pd.to_numeric, errors='coerce')

# Fill missing values
X.fillna(0, inplace=True)

# SAFE similarity
similarity = cosine_similarity(X.values)


# =========================
# MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# IMPROVED RECOMMENDATION
# =========================
def recommend_similar(input_df, top_n=3):
    combined = pd.concat([X, input_df], ignore_index=True)

    sim_matrix = cosine_similarity(combined.values)

    input_index = len(combined) - 1
    scores = list(enumerate(sim_matrix[input_index]))

    scores = sorted(scores[:-1], key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in scores[:top_n]]

    return df.iloc[top_indices]

# =========================
# UI
# =========================
st.title("🏥 Healthcare Recommendation System")

menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

# =========================
# SIGNUP
# =========================
if menu == "Signup":
    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Signup"):
        try:
            hashed = hash_password(password)
            cursor.execute("INSERT INTO users VALUES (?, ?, ?)",
                           (username, hashed, role))
            conn.commit()
            st.success("Account created!")
        except:
            st.error("Username already exists")

# =========================
# LOGIN
# =========================
elif menu == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if result:
            stored_password, role = result

            if verify_password(password, stored_password):
                token = create_token(username, role)
                st.session_state.token = token
                st.success("Login Successful")
                log_action(username, "login")
            else:
                st.error("Invalid credentials")
        else:
            st.error("User not found")

# =========================
# MAIN APP
# =========================
if "token" in st.session_state:
    user = verify_token(st.session_state.token)

    if user:
        username = user["sub"]
        role = user["role"]

        st.success(f"Welcome {username} ({role}) 👋")

        # ADMIN PANEL
        if role == "admin":
            st.subheader("👨‍⚕️ Admin Panel")

            if st.button("View Users"):
                st.dataframe(pd.read_sql("SELECT username, role FROM users", conn))

            if st.button("View Logs"):
                st.dataframe(pd.read_sql("SELECT * FROM logs ORDER BY id DESC", conn))

        # USER INPUT
        st.subheader("Enter Patient Details")

        def encode(val):
            return 1 if val == "Yes" else 0

        input_data = {
            'fever': encode(st.selectbox("Fever", ["No","Yes"])),
            'cough': encode(st.selectbox("Cough", ["No","Yes"])),
            'fatigue': encode(st.selectbox("Fatigue", ["No","Yes"])),
            'difficulty_breathing': encode(st.selectbox("Breathing Issue", ["No","Yes"])),
            'age': st.number_input("Age", 1, 100, 25),
            'blood_pressure': st.number_input("Blood Pressure", 80, 200, 120),
            'cholesterol_level': st.number_input("Cholesterol", 100, 300, 180)
        }

        input_df = pd.DataFrame([input_data])[features]

        # PREDICTION
        if st.button("Predict"):
            pred = model.predict(input_df)[0]

            st.success(f"Predicted Disease: {pred}")

            med_map = {
                0: "Paracetamol",
                1: "Antibiotics",
                2: "Cough Syrup",
                3: "Inhaler"
            }

            st.info(f"Medicine: {med_map.get(pred, 'Consult Doctor')}")

            # 🔥 IMPROVED RECOMMENDATION
            st.subheader("🔍 Similar Cases")

            similar_cases = recommend_similar(input_df)

            st.dataframe(similar_cases)

            log_action(username, "prediction")

            # Context-aware
            hour = datetime.datetime.now().hour
            if hour < 12:
                st.write("🌅 Morning Advice")
            else:
                st.write("🌙 Evening Advice")

        # DASHBOARD
        st.subheader("📊 Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(df['disease'].value_counts())

        with col2:
            st.bar_chart(df['risk_level'].value_counts())

        logs_df = pd.read_sql("SELECT * FROM logs", conn)

        if not logs_df.empty:
            st.line_chart(logs_df['id'])

    else:
        st.error("Session expired")
import streamlit as st
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from io import StringIO

# --- CONFIGURATION ---
st.set_page_config(page_title="Researcher & Fitness Hub", layout="wide")
warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# --- 1. SAMPLE DATA (To avoid mandatory upload) ---
SAMPLE_WORKOUT_JSON = """
[
    {
        "date": "2024-01-10",
        "exercises": [
            {"name": "Bench Press", "muscle": "Chest", "weight": "80", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 8}]},
            {"name": "Lateral Raise", "muscle": "Shoulders", "weight": "12", "sets": [{"set": 1, "reps": 15}]}
        ]
    },
    {
        "date": "2024-01-12",
        "exercises": [
            {"name": "Squat", "muscle": "Legs", "weight": "100", "sets": [{"set": 1, "reps": 5}, {"set": 2, "reps": 5}]}
        ]
    }
]
"""

# --- 2. PROCESSING LOGIC ---

def categorize_fallback(name):
    name = name.lower()
    mapping = {
        'Chest': ['bench', 'push-up', 'pec', 'chest'],
        'Back': ['row', 'pull', 'lat', 'chin-up', 'shrug', 'back'],
        'Shoulders': ['shoulder', 'press', 'lateral', 'deltoid'],
        'Biceps': ['bicep', 'curl', 'hammer'],
        'Triceps': ['tricep', 'extension', 'dip'],
        'Legs': ['squat', 'leg', 'quad', 'lunge', 'deadlift'],
        'Abs/Core': ['ab', 'crunch', 'core', 'plank']
    }
    for category, keywords in mapping.items():
        if any(word in name for word in keywords): return category
    return 'Other'

def clean_weight(weight):
    if weight is None or weight == "": return 0.0
    try: return float(str(weight).replace(',', '.'))
    except: return 0.0

def load_and_process(json_input):
    # Works for both file objects and raw strings
    raw_data = json.load(json_input) if not isinstance(json_input, str) else json.loads(json_input)
    
    rows = []
    for workout in raw_data:
        date = workout.get('date')
        for ex in workout.get('exercises', []):
            name = ex.get('name')
            category_raw = ex.get('muscle') or categorize_fallback(name)
            categories = [c.strip() for c in category_raw.split('/')]
            weight = clean_weight(ex.get('weight'))
            for s in ex.get('sets', []):
                reps = s.get('reps', 0)
                rows.append({
                    'Date': pd.to_datetime(date),
                    'Exercise': name,
                    'Category': categories,
                    'Reps': reps,
                    'Weight': weight,
                    'Volume': reps * weight
                })
    return pd.DataFrame(rows).explode('Category')

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Researcher Profile", "STEM Data Explorer", "Workout Analytics"]
)

# --- 4. APP SECTIONS ---

if menu == "Researcher Profile":
    st.title("Researcher Profile")
    st.write("**Name:** Dr. Jane Doe")
    st.write("**Field:** Astrophysics & Sports Science")
    st.image("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", width=400)

elif menu == "STEM Data Explorer":
    st.title("STEM Data Explorer")
    st.info("Physics, Astronomy, and Weather data visualizations.")
    # (Existing DataFrame logic from your previous snippet would go here)

elif menu == "Workout Analytics":
    st.title("🏋️‍♂️ Fitness Progress Dashboard")
    
    # Sidebar for Workout page
    st.sidebar.subheader("Data Source")
    uploaded_file = st.sidebar.file_uploader("Optional: Upload workout_data.json", type=['json'])

    # Toggle between Sample and Uploaded
    if uploaded_file is not None:
        df = load_and_process(uploaded_file)
        st.success("Using uploaded data!")
    else:
        df = load_and_process(SAMPLE_WORKOUT_JSON)
        st.info("Showing sample data. Upload your own JSON in the sidebar to update.")

    # --- METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Volume", f"{df['Volume'].sum():,.0f} kg")
    m2.metric("Sets Logged", len(df))
    m3.metric("Days Trained", df['Date'].nunique())

    # --- VISUALS ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Volume by Muscle Group")
        fig1, ax1 = plt.subplots()
        sns.barplot(data=df, x='Category', y='Volume', estimator=sum, palette='viridis', ax=ax1)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    with col2:
        st.subheader("Training Intensity Heatmap")
        fig3, ax3 = plt.subplots()
        pivot = df.pivot_table(index='Category', columns=df['Date'].dt.strftime('%b %d'), values='Volume', aggfunc='sum').fillna(0)
        sns.heatmap(pivot, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax3)
        st.pyplot(fig3)

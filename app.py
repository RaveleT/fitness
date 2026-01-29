import streamlit as st
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Researcher Portfolio & Fitness", layout="wide")
warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# --- 2. DEFAULT FITNESS DATA (Hardcoded so no upload is required) ---
DEFAULT_WORKOUT_JSON = [
    {
        "date": "2024-01-10",
        "exercises": [
            {"name": "Bench Press", "muscle": "Chest", "weight": "80", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}]},
            {"name": "Lat Pulldown", "muscle": "Back", "weight": "60", "sets": [{"set": 1, "reps": 12}]}
        ]
    },
    {
        "date": "2024-01-12",
        "exercises": [
            {"name": "Squat", "muscle": "Legs", "weight": "100", "sets": [{"set": 1, "reps": 8}, {"set": 2, "reps": 8}]}
        ]
    }
]

# --- 3. HELPER FUNCTIONS ---

def categorize_fallback(name):
    name = name.lower()
    mapping = {
        'Chest': ['bench', 'push-up', 'pec'],
        'Back': ['row', 'pull', 'lat', 'shrug'],
        'Shoulders': ['shoulder', 'press', 'lateral'],
        'Legs': ['squat', 'leg', 'lunge', 'deadlift'],
        'Core': ['ab', 'crunch', 'plank']
    }
    for category, keywords in mapping.items():
        if any(word in name for word in keywords): return category
    return 'Other'

def clean_weight_robust(weight_val):
    """Safely converts weight strings/objects to float."""
    if weight_val is None:
        return 0.0
    try:
        # Convert to string and handle European decimal commas
        w_str = str(weight_val).replace(',', '.').strip()
        
        # If it's a range (e.g., "10-12"), take the average or the first number
        if '-' in w_str:
            parts = w_str.split('-')
            return (float(parts[0]) + float(parts[1])) / 2
            
        return float(w_str)
    except (ValueError, TypeError):
        return 0.0

def process_workout_data(raw_data):
    rows = []
    for workout in raw_data:
        date = workout.get('date')
        for ex in workout.get('exercises', []):
            name = ex.get('name')
            cat = ex.get('muscle') if ex.get('muscle') else categorize_fallback(name)
            
            # Use the robust cleaner here to prevent the ValueError
            weight = clean_weight_robust(ex.get('weight'))
            
            for s in ex.get('sets', []):
                reps = s.get('reps', 0)
                rows.append({
                    'Date': pd.to_datetime(date),
                    'Exercise': name,
                    'Category': cat,
                    'Volume': reps * weight,
                    'Weight': weight,
                    'Reps': reps
                })
    return pd.DataFrame(rows)

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Researcher Profile", "STEM Data Explorer", "Fitness Tracker", "Contact"])

# --- 5. MAIN LOGIC ---

if menu == "Researcher Profile":
    st.title("Researcher Profile")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", caption="Dr. Jane Doe")
    with col2:
        st.write("**Field:** Astrophysics")
        st.write("**Institution:** University of Science")
        st.write("**Bio:** Specializing in stellar evolution and data-driven physical models.")

elif menu == "STEM Data Explorer":
    st.title("STEM Data Explorer")
    st.write("Visualizing Physics and Astronomy experimental data.")
    # (Existing DataFrame code goes here)

elif menu == "Fitness Tracker":
    st.title("🏋️‍♂️ Fitness Analytics")
    
    # Check for upload, otherwise use default
    uploaded_file = st.sidebar.file_uploader("Upload workout_data.json", type=['json'])
    if uploaded_file:
        data = json.load(uploaded_file)
    else:
        data = DEFAULT_WORKOUT_JSON
    
    df = process_workout_data(data)

    # Key Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Volume", f"{df['Volume'].sum():,.0f} kg")
    m2.metric("Total Sets", len(df))
    m3.metric("Workouts", df['Date'].nunique())

    st.divider()

    # Visuals
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Volume by Muscle Group")
        fig, ax = plt.subplots()
        df.groupby('Category')['Volume'].sum().sort_values().plot(kind='barh', ax=ax, color='skyblue')
        st.pyplot(fig)

    with col_right:
        st.subheader("Daily Intensity Heatmap")
        pivot = df.pivot_table(index='Category', columns=df['Date'].dt.strftime('%m-%d'), values='Volume', aggfunc='sum').fillna(0)
        fig2, ax2 = plt.subplots()
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax2)
        st.pyplot(fig2)

elif menu == "Contact":
    st.header("Contact")
    st.write("Email: jane.doe@science.edu")


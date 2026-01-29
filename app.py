import streamlit as st
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
from io import StringIO

# --- CONFIGURATION ---
st.set_page_config(page_title="Workout Analytics", layout="wide")
warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# --- 1. DATA PROCESSING LOGIC ---

def categorize_fallback(name):
    """Used if the JSON entry is missing a 'muscle' tag."""
    name = name.lower()
    mapping = {
        'Chest': ['bench', 'push-up', 'pushup', 'pec', 'chest'],
        'Back': ['row', 'pull', 'lat', 'chin-up', 'shrug', 'back'],
        'Shoulders': ['shoulder', 'press', 'lateral', 'deltoid', 'thruster', 'halo'],
        'Biceps': ['bicep', 'curl', 'hammer'],
        'Triceps': ['tricep', 'extension', 'kickback', 'dip'],
        'Legs': ['squat', 'leg', 'quad', 'lunge', 'step-up', 'rdl', 'deadlift', 'jump'],
        'Abs/Core': ['ab', 'crunch', 'core', 'plank', 'halo', 'rollout']
    }
    for category, keywords in mapping.items():
        if any(word in name for word in keywords):
            return category
    return 'Other'

def clean_weight(weight):
    if weight is None or weight == "": return 0.0
    try:
        return float(str(weight).replace(',', '.'))
    except (ValueError, TypeError):
        return 0.0

def load_and_process(file_source):
    """
    Handles both file paths (strings) and uploaded file objects.
    """
    if isinstance(file_source, str):
        with open(file_source, 'r') as f:
            raw_data = json.load(f)
    else:
        raw_data = json.load(file_source)
    
    rows = []
    for workout in raw_data:
        date = workout.get('date')
        for ex in workout.get('exercises', []):
            name = ex.get('name')
            
            # 1. Get the muscle tag
            category_raw = ex.get('muscle') 
            if not category_raw or category_raw == "Other":
                category_raw = categorize_fallback(name)
            
            # 2. Split multiple categories: "Chest / Shoulders" -> ["Chest", "Shoulders"]
            categories = [c.strip() for c in category_raw.split('/')]
            weight = clean_weight(ex.get('weight'))
            
            for s in ex.get('sets', []):
                reps = s.get('reps', 0)
                rows.append({
                    'Date': pd.to_datetime(date),
                    'Exercise': name,
                    'Categories': categories,
                    'Set': s.get('set'),
                    'Reps': reps,
                    'Weight': weight,
                    'Volume': reps * weight
                })
    
    df = pd.DataFrame(rows)
    if df.empty:
        return df
        
    # 3. Explode the 'Categories' list into separate rows
    df_exploded = df.explode('Categories')
    df_exploded = df_exploded.rename(columns={'Categories': 'Category'})
    
    return df_exploded

# --- 2. STREAMLIT UI ---

def main():
    st.sidebar.title("Settings")
    st.sidebar.info("Upload your `workout_data.json` exported from your fitness app.")
    
    uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type=['json'])

    # Main Title
    st.title("🏋️‍♂️ Fitness Progress Dashboard")
    st.markdown("Analyze volume, intensity, and muscle group distribution over time.")

    if uploaded_file is not None:
        df = load_and_process(uploaded_file)
    else:
        st.warning("👈 Please upload a JSON file in the sidebar to begin.")
        # Optional: Add a button to load a sample file if it exists in the repo
        return

    if df.empty:
        st.error("No data found in the uploaded file.")
        return

    # Metrics Row
    total_vol = df['Volume'].sum()
    total_sets = len(df)
    unique_days = df['Date'].nunique()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Volume", f"{total_vol:,.0f} kg")
    m2.metric("Total Sets", total_sets)
    m3.metric("Days Trained", unique_days)

    st.divider()

    # Plots Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Volume by Muscle Group")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        category_order = df.groupby('Category')['Volume'].sum().sort_values(ascending=False).index
        sns.barplot(data=df, x='Category', y='Volume', estimator=sum, order=category_order, palette='viridis', errorbar=None, ax=ax1)
        plt.xticks(rotation=45)
        plt.ylabel("Total Volume (kg)")
        st.pyplot(fig1)

    with col2:
        st.subheader("Rep Range Distribution")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df, x='Category', y='Reps', palette='Set3', order=category_order, ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    st.divider()

    # Plot Row 2 (Heatmap)
    st.subheader("Training Intensity Heatmap (Daily Volume)")
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    pivot = df.pivot_table(index='Category', columns='Date', values='Volume', aggfunc='sum').fillna(0)
    # Format columns to MM-DD
    pivot.columns = [d.strftime('%b %d') for d in pivot.columns]
    
    sns.heatmap(pivot, cmap='YlGnBu', annot=True, fmt='.0f', cbar_kws={'label': 'Volume (kg)'}, ax=ax3)
    plt.xlabel("Workout Date")
    st.pyplot(fig3)

    # Data View
    with st.expander("View Raw Processed Data"):
        st.dataframe(df)

if __name__ == "__main__":
    main()

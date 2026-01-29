import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Workout Progression", layout="wide")
sns.set_theme(style="whitegrid")

# --- 1. DATA PROCESSING LOGIC ---

def clean_weight(val):
    if val is None: return 0.0
    try:
        clean = re.sub(r'[^0-9.]', '', str(val).replace(',', '.'))
        return float(clean) if clean else 0.0
    except ValueError:
        return 0.0

def load_and_process(file_source):
    # Works for both string paths and Streamlit UploadedFile objects
    if isinstance(file_source, str):
        if not os.path.exists(file_source): return pd.DataFrame(), []
        with open(file_source, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = json.load(file_source)

    if not log_data:
        return pd.DataFrame(), []

    # Get the exercises from the very last entry in the JSON
    latest_session = log_data[-1]
    auto_targets = [ex.get('name') for ex in latest_session.get('exercises', [])]

    records = []
    for session in log_data:
        session_date = pd.to_datetime(session.get('date'))
        for exercise in session.get('exercises', []):
            exercise_name = exercise.get('name', 'Unknown')
            weight_val = clean_weight(exercise.get('weight'))
            for set_log in exercise.get('sets', []): 
                reps = set_log.get('reps', 0)
                records.append({
                    'Date': session_date,
                    'Exercise': exercise_name,
                    'Weight': weight_val,
                    'Reps': reps,
                    'Volume': weight_val * reps
                })
    
    return pd.DataFrame(records), auto_targets

def get_metrics(df):
    if df.empty: return pd.DataFrame()
    return df.groupby(['Date', 'Exercise']).agg(
        TotalVolume=('Volume', 'sum'),
        MaxWeight=('Weight', 'max'),
        AvgReps=('Reps', 'mean')
    ).reset_index()

# --- 2. STREAMLIT UI ---

def main():
    st.title("📈 Exercise Progression Tracker")
    
    uploaded_file = st.sidebar.file_uploader("Upload your workout_data.json", type=['json'])

    if uploaded_file:
        df_raw, target_list = load_and_process(uploaded_file)
        
        if not df_raw.empty:
            df_metrics = get_metrics(df_raw)
            
            # Allow user to select exercises (defaults to auto-detected ones)
            all_exercises = sorted(df_raw['Exercise'].unique())
            selected_exercises = st.multiselect("Select Exercises to Plot", all_exercises, default=target_list)

            for exercise in selected_exercises:
                st.write(f"### Analysis: {exercise}")
                
                data = df_metrics[df_metrics['Exercise'] == exercise].sort_values('Date')
                
                if data.empty:
                    st.warning(f"No data for {exercise}")
                    continue

                # Create Figure
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
                
                # Top Plot: Volume & Strength
                sns.lineplot(data=data, x='Date', y='TotalVolume', ax=ax1, marker='o', 
                            label='Total Volume (kg)', color='#3498db', linewidth=2.5)
                ax1.set_ylabel('Total Volume (kg)', color='#2980b9', fontweight='bold')
                
                ax1_twin = ax1.twinx()
                sns.lineplot(data=data, x='Date', y='MaxWeight', ax=ax1_twin, marker='s', 
                            label='Max Weight (kg)', color='#e74c3c', linewidth=2.5)
                ax1_twin.set_ylabel('Max Weight (kg)', color='#c0392b', fontweight='bold')
                ax1_twin.grid(False)
                
                # Bottom Plot: Rep Performance
                ax2.bar(data['Date'], data['AvgReps'], color='#2ecc71', alpha=0.7, width=0.8)
                ax2.set_ylabel('Avg Reps Per Set', fontweight='bold')
                
                # Formatting
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                ax2.set_xticks(data['Date'].unique())
                fig.autofmt_xdate(rotation=45)
                plt.tight_layout()
                
                # --- THIS IS THE KEY STREAMLIT COMMAND ---
                st.pyplot(fig)
                st.divider() # Add a line between exercises
        else:
            st.error("Uploaded file is empty or invalid.")
    else:
        st.info("Please upload your JSON file to see your progression.")

if __name__ == "__main__":
    main()

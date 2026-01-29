import streamlit as st
import pandas as pd
import json
import altair as alt
import plotly.express as px
import re
from datetime import datetime

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Fitness OS 2026", layout="wide", page_icon="🏋️‍♂️")

# Dark-Mode Safe CSS for Metrics
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
    }
    [data-testid="stMetricLabel"] p { color: #555555 !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] div { color: #111111 !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA & LOOKUP ---
null = None 
DEFAULT_HISTORY = [
    {"date": "2025-12-15", "exercises": [{"name": "Barbell Bench Press", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "30"}, {"name": "Push Ups", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 15}, {"set": 3, "reps": 15}], "weight": null}, {"name": "Dumbbell Overhead Press", "sets": [{"set": 1, "reps": 1}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "20"}, {"name": "Dynamique Crunch", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 20}, {"set": 3, "reps": 20}], "weight": null}, {"name": "Dumbbell Triceps Kickbacks", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 15}, {"set": 3, "reps": 15}], "weight": "9.5"}, {"name": "Ab Wheel Rollout", "sets": [{"set": 1, "reps": 5}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": null}, {"name": "Kettlebell Goblet Squat", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 15}, {"set": 3, "reps": 15}], "weight": "10"}, {"name": "Dumbbell Lateral Raise", "sets": [{"set": 1, "reps": 12}, {"set": 2, "reps": 12}, {"set": 3, "reps": 12}, {"set": 4, "reps": 12}], "weight": "9.5"}, {"name": "Kettlebell Overhead Triceps Extension", "sets": [{"set": 1, "reps": 12}, {"set": 2, "reps": 12}, {"set": 3, "reps": 12}, {"set": 4, "reps": 12}], "weight": "10"}, {"name": "Rotating Biceps Curl", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "9.5"}]},
    {"date": "2025-12-16", "exercises": [{"name": "Rotating Biceps Curl", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "9.5"}]},
    {"date": "2025-12-22", "exercises": [{"name": "Dynamique Crunch", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 20}, {"set": 3, "reps": 20}], "weight": null}, {"name": "Dumbbell Triceps Kickbacks", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 15}, {"set": 3, "reps": 15}], "weight": "9.5"}, {"name": "Ab Wheel Rollout", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}], "weight": null}, {"name": "Kettlebell Goblet Squat", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 15}], "weight": "10"}, {"name": "Dumbbell Lateral Raise", "sets": [{"set": 1, "reps": 12}, {"set": 2, "reps": 12}, {"set": 3, "reps": 12}, {"set": 4, "reps": 12}], "weight": "9.5"}, {"name": "Kettlebell Overhead Triceps Extension", "sets": [{"set": 1, "reps": 12}, {"set": 2, "reps": 12}, {"set": 3, "reps": 12}, {"set": 4, "reps": 12}], "weight": "10"}, {"name": "Rotating Biceps Curl", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 20}, {"set": 3, "reps": 20}], "weight": "9.5"}]},
    {"date": "2025-12-23", "exercises": [{"name": "Kettlebell Goblet Squat", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 15}, {"set": 3, "reps": 15}], "weight": "10"}, {"name": "Barbell RDL", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 16}, {"set": 3, "reps": 16}], "weight": "30"}, {"name": "Kettlebell Swings", "sets": [{"set": 1, "reps": 20}, {"set": 2, "reps": 20}, {"set": 3, "reps": 20}], "weight": "10"}, {"name": "Bodyweight Lunges", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 17}, {"set": 3, "reps": 18}], "weight": null}, {"name": "Kettlebell Forward Lunges", "sets": [{"set": 1, "reps": 15}, {"set": 2, "reps": 14}, {"set": 3, "reps": 16}], "weight": "10"}, {"name": "Dumbbell Lateral Raise", "sets": [{"set": 1, "reps": 12}, {"set": 2, "reps": 12}, {"set": 3, "reps": 12}, {"set": 4, "reps": 12}], "weight": "9.5"}, {"name": "Cycling", "sets": [{"set": 1, "reps": 70}, {"set": 2, "reps": 75}, {"set": 3, "reps": 80}], "weight": null}, {"name": "Plank", "sets": [{"set": 1, "reps": 60}, {"set": 2, "reps": 60}, {"set": 3, "reps": 60}], "weight": null}]},
    {"date": "2026-01-22", "exercises": [{"name": "Barbell Row", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "30"}, {"name": "Dumbbell Single-Arm Row-Right", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "9.5"}, {"name": "Dumbbell Single-Arm Row-Left", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "9.5"}, {"name": "Kettlebell High Pull", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 12}], "weight": "10"}, {"name": "Ab Wheel Rollout", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 12}], "weight": null}, {"name": "Barbell Bicep Curl", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 4}, {"set": 3, "reps": 5}], "weight": "9.5"}, {"name": "Dumbbell Shrug", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 15}, {"set": 3, "reps": 10}], "weight": "9.5"}]},
    {"date": "2026-01-23", "exercises": [{"name": "Barbell Thrusters", "sets": [{"set": 1, "reps": 4}, {"set": 2, "reps": 5}, {"set": 3, "reps": 4}], "weight": "30"}, {"name": "Dumbbell Step-Ups", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "29.5"}, {"name": "Kettlebell Halos", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": "10"}, {"name": "Push-Ups", "sets": [{"set": 1, "reps": 16}, {"set": 2, "reps": 16}, {"set": 3, "reps": 7}], "weight": null}, {"name": "Dumbbell Squat Jumps", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 15}, {"set": 3, "reps": 15}], "weight": "10"}, {"name": "Kettlebell Side Swings", "sets": [{"set": 1, "reps": 10}, {"set": 2, "reps": 10}, {"set": 3, "reps": 10}], "weight": null}, {"name": "Plank", "sets": [{"set": 1, "reps": 60}, {"set": 2, "reps": 60}, {"set": 3, "reps": 60}], "weight": null}]}
]

MUSCLE_LOOKUP = {
    "Barbell Bench Press": "Chest", "Push-Ups": "Chest / Shoulders", "Push Ups": "Chest / Shoulders",
    "Dumbbell Overhead Press": "Shoulders", "Dynamique Crunch": "Core",
    "Dumbbell Triceps Kickbacks": "Triceps", "Ab Wheel Rollout": "Core",
    "Kettlebell Goblet Squat": "Legs", "Dumbbell Lateral Raise": "Shoulders",
    "Kettlebell Overhead Triceps Extension": "Triceps", "Rotating Biceps Curl": "Biceps",
    "Barbell RDL": "Hamstrings", "Kettlebell Swings": "Full Body",
    "Bodyweight Lunges": "Legs", "Kettlebell Forward Lunges": "Legs",
    "Cycling": "Cardio", "Plank": "Core", "Barbell Row": "Back",
    "Single-Arm Row": "Back", "Kettlebell High Pull": "Shoulders",
    "Barbell Bicep Curl": "Biceps", "Dumbbell Shrug": "Traps",
    "Barbell Thrusters": "Full Body", "Dumbbell Step-Ups": "Legs",
    "Kettlebell Halos": "Shoulders", "Dumbbell Squat Jumps": "Legs",
    "Kettlebell Side Swings": "Core"
}

# --- 3. LOGIC ---
def clean_weight(val):
    if val is None or str(val).lower() == 'none': return 0.0
    try:
        return float(str(val).replace(',', '.'))
    except: return 0.0

def process_data_exploded(json_data):
    records = []
    for session in json_data:
        s_date = pd.to_datetime(session.get('date'))
        for ex in session.get('exercises', []):
            name = ex.get('name')
            muscle_tag = MUSCLE_LOOKUP.get(name, "Other")
            categories = [c.strip() for c in muscle_tag.split('/')]
            weight = clean_weight(ex.get('weight'))
            for s in ex.get('sets', []):
                records.append({
                    'Date': s_date, 'Exercise': name, 'Categories': categories,
                    'Weight': weight, 'Reps': s.get('reps', 0), 'Volume': weight * s.get('reps', 0)
                })
    df = pd.DataFrame(records)
    return df.explode('Categories').rename(columns={'Categories': 'Category'})

# --- 4. APP ---
if 'workout_history' not in st.session_state:
    st.session_state['workout_history'] = DEFAULT_HISTORY

df = process_data_exploded(st.session_state['workout_history'])

st.sidebar.title("🏋️‍♂️ Fitness OS")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Log Importer", "Progression Deep-Dive", "Data Management"])

if menu == "Dashboard":
    st.title("🚀 Training Overview")
    
    # 13,336 kg calculation (Unique volume per set to avoid explode-double-counting)
    unique_volume = df.drop_duplicates(subset=['Date', 'Exercise', 'Weight', 'Reps'])['Volume'].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Volume", f"{unique_volume:,.0f} kg")
    c2.metric("Total Sessions", df['Date'].nunique())
    c3.metric("Avg Intensity", f"{df[df['Weight']>0]['Weight'].mean():.1f} kg")
    c4.metric("Last Workout", df['Date'].max().strftime('%b %d'))

    st.divider()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Volume by Muscle Group")
        # INTERACTIVE ALTAIR BAR CHART
        muscle_data = df.groupby('Category')['Volume'].sum().reset_index()
        chart = alt.Chart(muscle_data).mark_bar(cornerRadiusEnd=4).encode(
            x=alt.X('Volume:Q', title="Total Volume (kg)"),
            y=alt.Y('Category:N', sort='-x', title="Muscle Group"),
            color=alt.Color('Category:N', legend=None),
            tooltip=['Category', 'Volume']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    
    with col_right:
        st.subheader("Daily Training Volume")
        # INTERACTIVE PLOTLY LINE CHART
        daily_vol = df.drop_duplicates(subset=['Date', 'Exercise', 'Weight', 'Reps']).groupby('Date')['Volume'].sum().reset_index()
        fig = px.line(daily_vol, x='Date', y='Volume', markers=True, template="plotly_white")
        fig.update_traces(line_color='#007bff', line_width=3)
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Progression Deep-Dive":
    st.title("📈 Exercise Analysis")
    target_ex = st.selectbox("Select Exercise:", sorted(df['Exercise'].unique()))
    
    data = df[df['Exercise'] == target_ex].groupby('Date').agg({'Weight': 'max', 'Volume': 'sum', 'Reps': 'mean'}).reset_index()
    
    # INTERACTIVE DUAL-AXIS CHART (Weight vs Volume)
    base = alt.Chart(data).encode(x='Date:T')
    
    line1 = base.mark_line(color='#e74c3c', strokeWidth=3).encode(
        y=alt.Y('Weight:Q', title='Max Weight (kg)'),
        tooltip=['Date', 'Weight']
    )
    line2 = base.mark_line(color='#3498db', strokeWidth=3).encode(
        y=alt.Y('Volume:Q', title='Session Volume (kg)'),
        tooltip=['Date', 'Volume']
    )
    
    st.altair_chart(alt.layer(line1, line2).resolve_scale(y='independent'), use_container_width=True)

# Other menu sections...

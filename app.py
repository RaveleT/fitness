import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import re
from datetime import datetime

# --- 1. SETTINGS & LUXE DARK THEME ---
st.set_page_config(page_title="Fitness OS 2026", layout="wide", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #161b22, #0d1117) !important;
        padding: 25px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(3, 166, 161, 0.2) !important;
    }
    [data-testid="stMetricLabel"] p { color: #FFE3BB !important; text-transform: uppercase; font-size: 12px; }
    [data-testid="stMetricValue"] div { color: #03A6A1 !important; font-weight: 300; font-size: 32px; }
    .stMarkdown h2, .stMarkdown h3 { color: #FFE3BB !important; font-weight: 400; margin-top: 2rem !important; }
    section[data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid rgba(3, 166, 161, 0.1); }
    hr { border-color: rgba(255, 79, 15, 0.3) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PASSWORD PROTECTION SYSTEM ---
def check_password():
    """Returns True if the user has the correct password."""
    
    # Initialize state
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # If already authenticated, don't show login
    if st.session_state["password_correct"]:
        return True

    # Show login screen
    st.markdown("<h1 style='text-align: center; color: #03A6A1;'>FITNESS OS LOGIN</h1>", unsafe_allow_html=True)
    
    cols = st.columns([1, 2, 1])
    with cols[1]:
        pwd = st.text_input("Enter System Access Key", type="password")
        if st.button("Unlock System"):
            if "password" in st.secrets and pwd == st.secrets["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("🚫 Access Denied: Incorrect Password")
    
    return False

# --- 3. DATA LOADING ---
@st.cache_data
def load_initial_data():
    if "workout_data" in st.secrets:
        raw_json = st.secrets["workout_data"].strip()
        raw_json = raw_json.replace(": None", ": null").replace(":None", ":null")
        try:
            return json.loads(raw_json)
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON Syntax Error: {e}")
            return []
    return []

# --- 4. MAIN APP CONTENT ---
if check_password():
    # Load Exercise Assets
    MUSCLE_LOOKUP = {
        "Barbell Bench Press": "Chest", "Push Ups": "Chest / Shoulders",
        "Dumbbell Overhead Press": "Shoulders", "Dynamique Crunch": "Core",
        "Dumbbell Triceps Kickbacks": "Triceps", "Ab Wheel Rollout": "Core",
        "Kettlebell Goblet Squat": "Legs", "Dumbbell Lateral Raise": "Shoulders",
        "Kettlebell Overhead Triceps Extension": "Triceps", "Rotating Biceps Curl": "Biceps",
        "Barbell RDL": "Hamstrings", "Kettlebell Swings": "Full Body",
        "Cycling": "Cardio", "Plank": "Core", "Barbell Row": "Back",
        "Dumbbell Single-Arm Row-Right": "Back", "Dumbbell Single-Arm Row-Left": "Back",
        "Barbell Bicep Curl": "Biceps", "Barbell Thrusters": "Full Body"
    }

    if 'workout_history' not in st.session_state:
        st.session_state['workout_history'] = load_initial_data()

    # Define Helper Functions
    def clean_weight(val):
        if val is None or str(val).lower() == 'none': return 0.0
        try: return float(str(val).replace(',', '.'))
        except: return 0.0

    def parse_workout_log(log_content):
        lines = log_content.strip().split('\n')
        date_line = next((line for line in lines if line.startswith('Date:')), None)
        date_str = date_line.split(':')[1].strip() if date_line else datetime.now().strftime('%Y-%m-%d')
        current_workout = {'date': date_str, 'exercises': []}
        current_exercise = None
        SET_REGEX = re.compile(r'(\d+)\s*->\s*(\d+)')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('Date:'): continue
            set_match = SET_REGEX.match(line)
            if set_match:
                if current_exercise:
                    current_exercise['sets'].append({'set': int(set_match.group(1)), 'reps': int(set_match.group(2))})
            else:
                if current_exercise: current_workout['exercises'].append(current_exercise)
                name_match = re.match(r'(.+?)(?:\((.+?)\))?$', line)
                if name_match:
                    name = name_match.group(1).strip()
                    weight_raw = name_match.group(2)
                    weight = weight_raw.replace(',', '.').replace('Kg', '').strip() if weight_raw else None
                    current_exercise = {'name': name, 'sets': [], 'weight': weight}
        if current_exercise: current_workout['exercises'].append(current_exercise)
        return current_workout

    def process_data(json_data):
        records = []
        for session in json_data:
            s_date = pd.to_datetime(session.get('date'))
            for ex in session.get('exercises', []):
                name = ex.get('name')
                muscle_tag = ex.get('muscle') or MUSCLE_LOOKUP.get(name, "Other")
                cats = [c.strip() for c in muscle_tag.split('/')]
                weight = clean_weight(ex.get('weight'))
                for s in ex.get('sets', []):
                    reps = s.get('reps', 0)
                    vol = reps if (name == "Cycling" or "Cardio" in cats) else (weight * reps)
                    records.append({
                        'Date': s_date, 'Day': s_date.strftime('%A'), 'Exercise': name,
                        'Category': cats, 'Weight': weight, 'Reps': reps, 'Volume': vol
                    })
        return pd.DataFrame(records).explode('Category') if records else pd.DataFrame()

    full_df = process_data(st.session_state['workout_history'])

    # --- SIDEBAR & NAVIGATION ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #03A6A1;'>FITNESS OS</h2>", unsafe_allow_html=True)
        menu = st.sidebar.radio("System Access", ["Dashboard", "Log Importer", "Progression", "Data Management"])
        
        if st.button("🔒 Logout"):
            st.session_state["password_correct"] = False
            st.rerun()

        st.divider()
        if not full_df.empty:
            min_date = full_df['Date'].min().to_pydatetime()
            max_date = full_df['Date'].max().to_pydatetime()
            selected_range = st.slider("Select Training Period", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="DD/MM/YY")
            df = full_df[(full_df['Date'] >= selected_range[0]) & (full_df['Date'] <= selected_range[1])]
        else:
            df = full_df

    # --- DASHBOARD PAGE ---
    if menu == "Dashboard":
        st.markdown("## Thendo's Fitness Dash")
        if not df.empty:
            unique_sets = df.drop_duplicates(subset=['Date', 'Exercise', 'Weight', 'Reps'])
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Gross Volume", f"{unique_sets['Volume'].sum():,.0f} pts")
            m2.metric("Sessions", df['Date'].nunique())
            m3.metric("Avg Load", f"{unique_sets[unique_sets['Weight']>0]['Weight'].mean():.1f} kg")
            m4.metric("Last Activity", df['Date'].max().strftime('%d %b'))

            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📊 Volume Distribution")
                muscle_vol = df.groupby('Category')['Volume'].sum().reset_index().sort_values('Volume')
                st.plotly_chart(px.bar(muscle_vol, x='Volume', y='Category', orientation='h', template="plotly_dark", color_discrete_sequence=['#03A6A1']), use_container_width=True)
            with col2:
                st.markdown("### 🕸️ Muscle Balance")
                radar_data = df.groupby('Category')['Volume'].sum().reset_index()
                fig_radar = go.Figure(data=go.Scatterpolar(r=radar_data['Volume'], theta=radar_data['Category'], fill='toself', fillcolor='rgba(3, 166, 161, 0.3)', line_color='#03A6A1'))
                fig_radar.update_layout(template="plotly_dark", polar=dict(radialaxis=dict(visible=False)), height=400)
                st.plotly_chart(fig_radar, use_container_width=True)

            st.divider()
            st.markdown("### 🗓️ Training Consistency")
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            consistency = df.drop_duplicates('Date').groupby('Day').size().reindex(day_order, fill_value=0).reset_index(name='Sessions')
            st.plotly_chart(px.bar(consistency, x='Day', y='Sessions', template="plotly_dark", color_discrete_sequence=['#FF4F0F']), use_container_width=True)

            st.divider()
            st.markdown("### 🏆 Top Exercise Assets")
            top_ex = df.groupby('Exercise').size().reset_index(name='Freq').sort_values('Freq').tail(10)
            st.plotly_chart(px.bar(top_ex, x='Freq', y='Exercise', orientation='h', template="plotly_dark", color_discrete_sequence=['#03A6A1']), use_container_width=True)
            
    # --- OTHER PAGES ---
    elif menu == "Log Importer":
        st.markdown("## 📥 Raw Log Importer")
        raw = st.text_area("Paste text log here:", height=300)
        if st.button("🚀 Save Workout"):
            if raw:
                new_session = parse_workout_log(raw)
                history = {s['date']: s for s in st.session_state['workout_history']}
                history[new_session['date']] = new_session
                st.session_state['workout_history'] = sorted(list(history.values()), key=lambda x: x['date'])
                st.success("Buffer updated successfully.")
                st.rerun()

    elif menu == "Progression":
        st.markdown("## 📈 Performance Deep-Dive")
        if not df.empty:
            target = st.selectbox("Select Asset", sorted(df['Exercise'].unique()))
            p_data = df[df['Exercise'] == target].groupby('Date').agg({'Weight': 'max', 'Volume': 'sum'}).reset_index()
            fig = px.line(p_data, x='Date', y=['Weight', 'Volume'], markers=True, template="plotly_dark", color_discrete_sequence=['#03A6A1', '#FF4F0F'])
            st.plotly_chart(fig, use_container_width=True)

    elif menu == "Data Management":
        st.markdown("## 💾 Data Management")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ Purge All Data"):
                st.session_state['workout_history'] = []
                st.rerun()
        with c2:
            if st.button("🔄 Reload from Secrets"):
                st.session_state['workout_history'] = load_initial_data()
                st.rerun()
        st.divider()
        st.download_button("📤 Export State", data=json.dumps(st.session_state['workout_history'], indent=4), file_name="fitness_os.json")


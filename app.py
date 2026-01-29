import streamlit as st
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

null = None

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Researcher Portfolio & Fitness", layout="wide")
warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# --- 2. DEFAULT FITNESS DATA (Hardcoded so no upload is required) ---
DEFAULT_WORKOUT_JSON = [
    {
        "date": "2025-12-15",
        "exercises": [
            {
                "name": "Barbell Bench Press",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "30"
            },
            {
                "name": "Push Ups",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 15
                    },
                    {
                        "set": 3,
                        "reps": 15
                    }
                ],
                "weight": null
            },
            {
                "name": "Dumbbell Overhead Press",
                "sets": [
                    {
                        "set": 1,
                        "reps": 1
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "20"
            },
            {
                "name": "Dynamique Crunch",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 20
                    },
                    {
                        "set": 3,
                        "reps": 20
                    }
                ],
                "weight": null
            },
            {
                "name": "Dumbbell Triceps Kickbacks",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 15
                    },
                    {
                        "set": 3,
                        "reps": 15
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Ab Wheel Rollout",
                "sets": [
                    {
                        "set": 1,
                        "reps": 5
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": null
            },
            {
                "name": "Kettlebell Goblet Squat",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 15
                    },
                    {
                        "set": 3,
                        "reps": 15
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Dumbbell Lateral Raise",
                "sets": [
                    {
                        "set": 1,
                        "reps": 12
                    },
                    {
                        "set": 2,
                        "reps": 12
                    },
                    {
                        "set": 3,
                        "reps": 12
                    },
                    {
                        "set": 3,
                        "reps": 12
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Kettlebell Overhead Triceps Extension",
                "sets": [
                    {
                        "set": 1,
                        "reps": 12
                    },
                    {
                        "set": 2,
                        "reps": 12
                    },
                    {
                        "set": 3,
                        "reps": 12
                    },
                    {
                        "set": 3,
                        "reps": 12
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Rotating Biceps Curl",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "9.5"
            }
        ]
    },
    {
        "date": "2025-12-16",
        "exercises": [
            {
                "name": "Rotating Biceps Curl",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "9.5"
            }
        ]
    },
    {
        "date": "2025-12-22",
        "exercises": [
            {
                "name": "Dynamique Crunch",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 20
                    },
                    {
                        "set": 3,
                        "reps": 20
                    }
                ],
                "weight": null
            },
            {
                "name": "Dumbbell Triceps Kickbacks",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 15
                    },
                    {
                        "set": 3,
                        "reps": 15
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Ab Wheel Rollout",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    }
                ],
                "weight": null
            },
            {
                "name": "Kettlebell Goblet Squat",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 15
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Dumbbell Lateral Raise",
                "sets": [
                    {
                        "set": 1,
                        "reps": 12
                    },
                    {
                        "set": 2,
                        "reps": 12
                    },
                    {
                        "set": 3,
                        "reps": 12
                    },
                    {
                        "set": 4,
                        "reps": 12
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Kettlebell Overhead Triceps Extension",
                "sets": [
                    {
                        "set": 1,
                        "reps": 12
                    },
                    {
                        "set": 2,
                        "reps": 12
                    },
                    {
                        "set": 3,
                        "reps": 12
                    },
                    {
                        "set": 4,
                        "reps": 12
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Rotating Biceps Curl",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 20
                    },
                    {
                        "set": 3,
                        "reps": 20
                    }
                ],
                "weight": "9.5"
            }
        ]
    },
    {
        "date": "2025-12-23",
        "exercises": [
            {
                "name": "Kettlebell Goblet Squat",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 15
                    },
                    {
                        "set": 3,
                        "reps": 15
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Barbell RDL",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 16
                    },
                    {
                        "set": 3,
                        "reps": 16
                    }
                ],
                "weight": "30"
            },
            {
                "name": "Kettlebell Swings",
                "sets": [
                    {
                        "set": 1,
                        "reps": 20
                    },
                    {
                        "set": 2,
                        "reps": 20
                    },
                    {
                        "set": 3,
                        "reps": 20
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Bodyweight Lunges",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 17
                    },
                    {
                        "set": 3,
                        "reps": 18
                    }
                ],
                "weight": null
            },
            {
                "name": "Kettlebell Forward Lunges",
                "sets": [
                    {
                        "set": 1,
                        "reps": 15
                    },
                    {
                        "set": 2,
                        "reps": 14
                    },
                    {
                        "set": 3,
                        "reps": 16
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Dumbbell Lateral Raise",
                "sets": [
                    {
                        "set": 1,
                        "reps": 12
                    },
                    {
                        "set": 2,
                        "reps": 12
                    },
                    {
                        "set": 3,
                        "reps": 12
                    },
                    {
                        "set": 4,
                        "reps": 12
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Cycling",
                "sets": [
                    {
                        "set": 1,
                        "reps": 70
                    },
                    {
                        "set": 2,
                        "reps": 75
                    },
                    {
                        "set": 3,
                        "reps": 80
                    }
                ],
                "weight": null
            },
            {
                "name": "Plank",
                "sets": [
                    {
                        "set": 1,
                        "reps": 60
                    },
                    {
                        "set": 2,
                        "reps": 60
                    },
                    {
                        "set": 3,
                        "reps": 60
                    }
                ],
                "weight": null
            }
        ]
    },
    {
        "date": "2026-01-22",
        "exercises": [
            {
                "name": "Barbell Row",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "30"
            },
            {
                "name": "Dumbbell  Single-Arm Row-Right",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Dumbbell  Single-Arm Row-Left",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Kettlebell High Pull",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 12
                    }
                ],
                "weight": "10"
            },
            {
                "name": "Ab Wheel Rollout",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 12
                    }
                ],
                "weight": null
            },
            {
                "name": "Barbell Bicep Curl",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 4
                    },
                    {
                        "set": 3,
                        "reps": 5
                    }
                ],
                "weight": "9.5"
            },
            {
                "name": "Dumbbell Shrug",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 15
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "9.5"
            }
        ]
    },
    {
        "date": "2026-01-23",
        "exercises": [
            {
                "name": "Barbell Thrusters",
                "sets": [
                    {
                        "set": 1,
                        "reps": 4
                    },
                    {
                        "set": 2,
                        "reps": 5
                    },
                    {
                        "set": 3,
                        "reps": 4
                    }
                ],
                "weight": "30",
                "muscle": "Quads / Shoulders"
            },
            {
                "name": "Dumbbell Step-Ups",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "29.5",
                "muscle": "Quads / Glutes"
            },
            {
                "name": "Kettlebell Halos",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": "10",
                "muscle": "Shoulders / Core"
            },
            {
                "name": "Push-Ups",
                "sets": [
                    {
                        "set": 1,
                        "reps": 16
                    },
                    {
                        "set": 2,
                        "reps": 16
                    },
                    {
                        "set": 3,
                        "reps": 7
                    }
                ],
                "weight": null,
                "muscle": "Chest / Shoulders"
            },
            {
                "name": "Dumbbell Squat Jumps",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 15
                    },
                    {
                        "set": 3,
                        "reps": 15
                    }
                ],
                "weight": "10",
                "muscle": "Quads / Calves"
            },
            {
                "name": "Kettlebell Side Swings",
                "sets": [
                    {
                        "set": 1,
                        "reps": 10
                    },
                    {
                        "set": 2,
                        "reps": 10
                    },
                    {
                        "set": 3,
                        "reps": 10
                    }
                ],
                "weight": null,
                "muscle": "Core / Shoulders"
            },
            {
                "name": "Plank",
                "sets": [
                    {
                        "set": 1,
                        "reps": 60
                    },
                    {
                        "set": 2,
                        "reps": 60
                    },
                    {
                        "set": 3,
                        "reps": 60
                    }
                ],
                "weight": null,
                "muscle": "Core / Stabilizer"
            }
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
    
    # --- Data Loading ---
    uploaded_file = st.sidebar.file_uploader("Upload workout_data.json", type=['json'])
    if uploaded_file:
        data = json.load(uploaded_file)
    else:
        # This will now use your real 2025/2026 data
        data = DEFAULT_WORKOUT_JSON
    
    df = process_workout_data(data)

    # --- Sidebar Filters ---
    st.sidebar.divider()
    st.sidebar.subheader("Filter Dashboard")
    
    # This filter ensures you can toggle between 2025 and 2026
    available_years = sorted(df['Date'].dt.year.unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select Year", available_years)
    
    # Filter the dataframe for the rest of the page
    df_filtered = df[df['Date'].dt.year == selected_year]

    # --- Top Level Metrics ---
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Total Volume ({selected_year})", f"{df_filtered['Volume'].sum():,.0f} kg")
    m2.metric("Exercises Logged", len(df_filtered))
    m3.metric("Training Sessions", df_filtered['Date'].nunique())

    st.divider()

    # --- Visualizations ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Volume by Muscle Group")
        # Horizontal bar chart showing where you're putting in the work
        fig, ax = plt.subplots()
        df_filtered.groupby('Category')['Volume'].sum().sort_values().plot(kind='barh', ax=ax, color='#1f77b4')
        plt.xlabel("Total Weight (kg)")
        st.pyplot(fig)

    with col_right:
        st.subheader("Daily Training Load")
        # Heatmap using specific dates to keep 2025/2026 separate
        pivot = df_filtered.pivot_table(
            index='Category', 
            columns=df_filtered['Date'].dt.strftime('%m-%d'), 
            values='Volume', 
            aggfunc='sum'
        ).fillna(0)
        
        fig2, ax2 = plt.subplots()
        sns.heatmap(pivot, annot=False, cmap="YlGnBu", ax=ax2)
        st.pyplot(fig2)

    # --- Progress Over Time (The "January View") ---
    st.subheader("All-Time Volume Trend")
    # This chart is not filtered by year, so you can see the jump from 2025 to 2026
    trend_data = df.groupby('Date')['Volume'].sum().reset_index()
    st.line_chart(trend_data.set_index('Date'))

elif menu == "Contact":
    st.header("Contact")
    st.write("Email: ravele95@gmail.com")
    st.write("Contact No: 060 924 9459")






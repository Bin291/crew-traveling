import streamlit as st
from main import run

st.set_page_config(page_title="Travel Planner", layout="centered")
st.title("🌍 AI Travel Planner")

theme_map = {
    "1. Relaxing Beach 🏖️": "1",
    "2. Mountain Adventure 🏞️": "2",
    "3. Culture & Cuisine 🏛️": "3"
}

theme_choice = st.selectbox("What type of trip do you prefer?", list(theme_map.keys()))

# Reset destination list if theme changes
if "last_theme" not in st.session_state:
    st.session_state["last_theme"] = theme_choice

if theme_choice != st.session_state["last_theme"]:
    st.session_state.pop("affordable", None)
    st.session_state["last_theme"] = theme_choice

budget = st.number_input("Budget (million VND)", min_value=1, value=5)
people = st.number_input("Number of people", min_value=1, value=2)
days = st.number_input("Number of days", min_value=1, value=3)

# Step 1: Suggest destinations
if st.button("🔍 Get destination suggestions"):
    with st.spinner("Analyzing your preferences and budget..."):
        affordable = run(
            theme=theme_map[theme_choice],
            budget=budget,
            people=people,
            days=days,
            selected_destination=None,
            language="en"
        )
        st.session_state["affordable"] = affordable

# Step 2: Choose and generate
if "affordable" in st.session_state:
    selected_destination = st.selectbox("🎯 Choose your destination:", st.session_state["affordable"])

    if st.button("🧠 Generate Travel Plan"):
        with st.spinner("Generating travel plan..."):
            result = run(
                theme=theme_map[theme_choice],
                budget=budget,
                people=people,
                days=days,
                selected_destination=selected_destination,
                language="en"
            )
            if isinstance(result, str):
                st.text_area("📋 Travel Plan", result, height=400)
                st.download_button("📥 Download Plan", result, file_name="travel_plan.txt")
            else:
                st.error("❗ Plan generation failed.")

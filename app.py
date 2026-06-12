import json
import streamlit as st

st.set_page_config(
    page_title="Birthday Weekend",
    page_icon="🎀",
    layout="centered"
)

# Pink styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff5f8, #ffe4ec);
}
.day-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
    border: 2px solid #ffc2d6;
}
.title {
    text-align: center;
    color: #ff4f9a;
    font-size: 3rem;
}
</style>
""", unsafe_allow_html=True)

# Load itinerary
with open("itinerary.json", "r") as f:
    itinerary = json.load(f)

# Session state
if "editing" not in st.session_state:
    st.session_state.editing = False

# Header
st.markdown(
    "<h1 class='title'>🎀 Birthday Weekend 🎀</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Celebrate the Birthday Girl 🩷</p>",
    unsafe_allow_html=True
)

# View mode
for day, events in itinerary.items():
    st.markdown(
        f"<div class='day-card'><h3>🩷 {day}</h3>",
        unsafe_allow_html=True
    )

    if st.session_state.editing:
        for i, event in enumerate(events):
            itinerary[day][i] = st.text_input(
                f"{day}-{i}",
                value=event
            )
    else:
        for event in events:
            st.write(event)

    st.markdown("</div>", unsafe_allow_html=True)

# Hidden-ish edit section
with st.expander("✨ Secret Sister Code ✨"):
    password = st.text_input(
        "Enter passcode",
        type="password"
    )

    if st.button("Unlock Editing"):
        if password == st.secrets["edit_password"]:
            st.session_state.editing = True
            st.success("Editing unlocked 🩷")
        else:
            st.error("Incorrect passcode")

# Save button
if st.session_state.editing:
    if st.button("💾 Save Changes"):
        with open("itinerary.json", "w") as f:
            json.dump(itinerary, f, indent=2)
        st.success("Saved!")

import json
import streamlit as st

st.set_page_config(
    page_title="Sunterrah's 30th Birthday",
    page_icon="🎀",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff5f8, #ffe4ec);
    overflow: hidden;
}

.title {
    text-align: center;
    color: #ff4f9a;
    font-size: 2.7rem;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #b83273;
    font-size: 1.2rem;
    margin-bottom: 30px;
}

.day-card {
    background: rgba(255, 255, 255, 0.92);
    padding: 22px;
    border-radius: 24px;
    margin-bottom: 18px;
    border: 2px solid #ffc2d6;
    box-shadow: 0 8px 20px rgba(255, 79, 154, 0.15);
}

.event-card {
    background: #fff5f9;
    padding: 14px;
    border-radius: 16px;
    margin: 10px 0;
    border-left: 6px solid #ff69b4;
}

.time {
    font-weight: bold;
    color: #ff4f9a;
}

.event {
    font-size: 1.05rem;
    color: #5a1f3c;
}

.glitter {
    position: fixed;
    top: -10px;
    animation: fall linear infinite;
    color: #ff69b4;
    font-size: 18px;
    z-index: 9999;
    pointer-events: none;
}

@keyframes fall {
    to {
        transform: translateY(110vh) rotate(360deg);
    }
}
</style>

<div class="glitter" style="left:5%; animation-duration:6s;">✨</div>
<div class="glitter" style="left:15%; animation-duration:8s;">💖</div>
<div class="glitter" style="left:25%; animation-duration:7s;">✨</div>
<div class="glitter" style="left:40%; animation-duration:9s;">🎀</div>
<div class="glitter" style="left:55%; animation-duration:6.5s;">✨</div>
<div class="glitter" style="left:70%; animation-duration:8.5s;">💗</div>
<div class="glitter" style="left:85%; animation-duration:7.5s;">✨</div>
<div class="glitter" style="left:95%; animation-duration:9.5s;">💖</div>
""", unsafe_allow_html=True)

def load_itinerary():
    with open("itinerary.json", "r") as f:
        return json.load(f)

def save_itinerary(data):
    with open("itinerary.json", "w") as f:
        json.dump(data, f, indent=2)

if "itinerary" not in st.session_state:
    st.session_state.itinerary = load_itinerary()

if "editing" not in st.session_state:
    st.session_state.editing = False

st.markdown(
    "<h1 class='title'>🎀 Sunterrah's 30th Birthday 🎀</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>A cute birthday weekend itinerary 🩷✨</p>",
    unsafe_allow_html=True
)

# Show itinerary
for day, events in st.session_state.itinerary.items():
    st.markdown(f"<div class='day-card'><h2>🩷 {day}</h2>", unsafe_allow_html=True)

    for item in events:
        st.markdown(
            f"""
            <div class='event-card'>
                <div class='time'>{item['time']}</div>
                <div class='event'>{item['event']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# Secret edit area
with st.expander("✨ Secret Sister Code ✨"):
    password = st.text_input("Enter passcode", type="password")

    if st.button("Unlock Editing"):
        if password == st.secrets["edit_password"]:
            st.session_state.editing = True
            st.success("Editing unlocked 🩷")
        else:
            st.error("Incorrect passcode")

if st.session_state.editing:
    st.markdown("## ✏️ Edit Itinerary")

    selected_day = st.selectbox(
        "Where do you want to add something?",
        list(st.session_state.itinerary.keys())
    )

    st.markdown("### Add something new")

    new_time = st.text_input("New time", placeholder="Example: 7:00 PM")
    new_event = st.text_input("New event", placeholder="Example: 🎂 Cake and champagne")

    if st.button("➕ Add to Day"):
        if new_time and new_event:
            st.session_state.itinerary[selected_day].append({
                "time": new_time,
                "event": new_event
            })
            st.success("Added! You can see it on the page now 🩷")
            st.rerun()
        else:
            st.warning("Add both a time and event.")

    st.divider()

    st.markdown("### Change something already listed")
    st.warning("Only use this if you really want to edit or delete an existing item.")

    confirm_edit = st.checkbox(
        "Yes, I am sure I want to edit something that is already on the itinerary."
    )

    if confirm_edit:
        edit_day = st.selectbox(
            "Which day do you want to edit?",
            list(st.session_state.itinerary.keys()),
            key="edit_existing_day"
        )

        updated_events = []

        for i, item in enumerate(st.session_state.itinerary[edit_day]):
            col1, col2, col3 = st.columns([2, 4, 1])

            with col1:
                new_time_existing = st.text_input(
                    "Time",
                    value=item["time"],
                    key=f"time_existing_{edit_day}_{i}"
                )

            with col2:
                new_event_existing = st.text_input(
                    "Event",
                    value=item["event"],
                    key=f"event_existing_{edit_day}_{i}"
                )

            with col3:
                delete_existing = st.checkbox(
                    "Delete",
                    key=f"delete_existing_{edit_day}_{i}"
                )

            if not delete_existing:
                updated_events.append({
                    "time": new_time_existing,
                    "event": new_event_existing
                })

        st.session_state.itinerary[edit_day] = updated_events

    if st.button("💾 Save Changes"):
        save_itinerary(st.session_state.itinerary)
        st.success("Saved 🩷")
        st.rerun()

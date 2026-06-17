import json
import base64
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="Sunterrah's 30th Birthday",
    page_icon="🎀",
    layout="centered"
)

IMAGE_FILE = "secret_puppy.png.gif"


def gif_to_html(path, width=150):
    with open(path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    return f"""
    <div style="text-align:center;">
        <img src="data:image/gif;base64,{encoded}" width="{width}" style="animation:bounce 1.5s infinite; cursor:pointer;">
    </div>
    """


st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff5f8, #ffe4ec);
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
    background: rgba(255,255,255,0.95);
    padding: 22px;
    border-radius: 24px;
    margin-bottom: 18px;
    border: 2px solid #ffc2d6;
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
    font-size: 18px;
    z-index: 9999;
    pointer-events: none;
}
@keyframes fall {
    to {
        transform: translateY(110vh) rotate(360deg);
    }
}
@keyframes bounce {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
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


def time_sort_value(item):
    try:
        return datetime.strptime(item["time"], "%I:%M %p")
    except:
        return datetime.max


def sort_itinerary(data):
    for day in data:
        data[day] = sorted(data[day], key=time_sort_value)
    return data


if "itinerary" not in st.session_state:
    st.session_state.itinerary = sort_itinerary(load_itinerary())

if "editing" not in st.session_state:
    st.session_state.editing = False

if "show_password" not in st.session_state:
    st.session_state.show_password = False


st.markdown(
    "<h1 class='title'>🎀 Sunterrah's 30th Birthday 🎀</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>A cute birthday weekend itinerary 🩷✨</p>",
    unsafe_allow_html=True
)


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


st.markdown(gif_to_html(IMAGE_FILE, width=150), unsafe_allow_html=True)

if st.button("🐾"):
    st.session_state.show_password = True

if st.session_state.show_password:
    password = st.text_input("Enter passcode", type="password")

    if st.button("Unlock"):
        if password == st.secrets["edit_password"]:
            st.session_state.editing = True
            st.success("Unlocked 🩷")
        else:
            st.error("Incorrect passcode 🐾")


if st.session_state.editing:
    st.markdown("## ✨ Add to the Itinerary")

    with st.form("add_event_form", clear_on_submit=True):
        add_day = st.selectbox(
            "What day is this for?",
            list(st.session_state.itinerary.keys())
        )

        add_time = st.time_input("What time?")

        add_event = st.text_input(
            "What is happening?",
            placeholder="Example: 🎂 Birthday cake and champagne"
        )

        submitted = st.form_submit_button("➕ Add Event")

        if submitted:
            if add_event:
                formatted_time = add_time.strftime("%I:%M %p")

                st.session_state.itinerary[add_day].append({
                    "time": formatted_time,
                    "event": add_event
                })

                st.session_state.itinerary = sort_itinerary(st.session_state.itinerary)
                save_itinerary(st.session_state.itinerary)

                st.success("Added and saved 🩷")
                st.rerun()
            else:
                st.warning("Please type the event first.")

    st.divider()

    st.markdown("## ⚠️ Edit or Delete Existing Plans")

    confirm_edit = st.checkbox(
        "Yes, I am sure I want to edit or delete something already on the itinerary."
    )

    if confirm_edit:
        edit_day = st.selectbox(
            "Which day do you want to edit?",
            list(st.session_state.itinerary.keys()),
            key="edit_day"
        )

        updated_events = []

        for i, item in enumerate(st.session_state.itinerary[edit_day]):
            st.markdown(f"### Item {i + 1}")

            new_time = st.text_input(
                "Time",
                value=item["time"],
                key=f"time_{edit_day}_{i}"
            )

            new_event = st.text_input(
                "Event",
                value=item["event"],
                key=f"event_{edit_day}_{i}"
            )

            delete = st.checkbox(
                "Delete this item",
                key=f"delete_{edit_day}_{i}"
            )

            if not delete:
                updated_events.append({
                    "time": new_time,
                    "event": new_event
                })

        if st.button("💾 Save Edits"):
            st.session_state.itinerary[edit_day] = updated_events
            st.session_state.itinerary = sort_itinerary(st.session_state.itinerary)
            save_itinerary(st.session_state.itinerary)
            st.success("Saved 🩷")
            st.rerun()

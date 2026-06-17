import base64
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client

st.set_page_config(
    page_title="Sunterrah's 30th Birthday",
    page_icon="🎀",
    layout="centered"
)

IMAGE_FILE = "secret_puppy.png.gif"

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


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
    background: linear-gradient(180deg, #fff5f8, #ffe4ec) !important;
    color: #4a1230 !important;
}

.title {
    text-align: center;
    font-size: 2.7rem;
    font-weight: bold;
    background: linear-gradient(90deg, #ff1493, #ff69b4, #ffb6d9, #ff1493);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
}

.subtitle {
    text-align: center;
    color: #c2185b !important;
    font-size: 1.2rem;
    margin-bottom: 20px;
}

.day-title {
    color: #ff1493 !important;
    text-shadow: 0 0 8px rgba(255, 105, 180, 0.45);
    font-weight: 800;
}

.day-card {
    background: rgba(255,255,255,0.98);
    padding: 22px;
    border-radius: 24px;
    margin-bottom: 18px;
    border: 2px solid #ff9ecb;
    box-shadow: 0 8px 22px rgba(255, 20, 147, 0.18);
}

.theme-box {
    background: #fff0f7;
    padding: 14px;
    border-radius: 16px;
    margin-bottom: 14px;
    border: 1px dashed #ff69b4;
}

.theme {
    font-weight: bold;
    color: #ff1493 !important;
    font-size: 1.15rem;
}

.dress-code {
    font-weight: bold;
    color: #c2185b !important;
}

.description {
    color: #4a1230 !important;
    line-height: 1.5;
}

.event-card {
    background: #fff7fb;
    padding: 14px;
    border-radius: 16px;
    margin: 10px 0;
    border-left: 6px solid #ff1493;
}

.time {
    font-weight: bold;
    color: #ff1493 !important;
}

.event {
    font-size: 1.05rem;
    color: #4a1230 !important;
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
    to { transform: translateY(110vh) rotate(360deg); }
}

@keyframes bounce {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

@keyframes shimmer {
    0% { background-position: 0%; }
    100% { background-position: 300%; }
}

@media print {
    .stButton,
    .stTextInput,
    .stTextArea,
    .stSelectbox,
    .stCheckbox,
    .stForm,
    .glitter,
    iframe,
    [data-testid="stSidebar"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stHeader"] {
        display: none !important;
    }

    .stApp {
        background: white !important;
    }

    .day-card {
        page-break-inside: avoid;
        box-shadow: none !important;
        border: 2px solid #ff9ecb !important;
    }

    .title {
        -webkit-text-fill-color: #ff1493 !important;
        color: #ff1493 !important;
        background: none !important;
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


def time_sort_value(item):
    try:
        return datetime.strptime(item["time"], "%I:%M %p")
    except:
        return datetime.max


def load_itinerary():
    details_response = supabase.table("day_details").select("*").execute()
    events_response = supabase.table("events").select("*").execute()

    itinerary = {}

    for row in details_response.data:
        itinerary[row["day"]] = {
            "theme": row["theme"],
            "dress_code": row["dress_code"],
            "description": row["description"],
            "events": []
        }

    for row in events_response.data:
        day = row["day"]
        if day in itinerary:
            itinerary[day]["events"].append({
                "id": row["id"],
                "time": row["time"],
                "event": row["event"]
            })

    for day in itinerary:
        itinerary[day]["events"] = sorted(
            itinerary[day]["events"],
            key=time_sort_value
        )

    return itinerary


def refresh_itinerary():
    st.session_state.itinerary = load_itinerary()


if "itinerary" not in st.session_state:
    refresh_itinerary()

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

components.html(
    """
    <div style="text-align:center; margin: 10px 0 25px 0;">
        <button onclick="window.parent.print()" style="
            background:#ff1493;
            color:white;
            border:none;
            padding:12px 22px;
            border-radius:999px;
            font-weight:bold;
            font-size:16px;
            cursor:pointer;
            box-shadow:0 6px 14px rgba(255,20,147,0.25);
        ">
            🖨️ Print / Save as PDF
        </button>
    </div>
    """,
    height=70
)

day_order = ["Friday", "Saturday", "Sunday"]

for day in day_order:
    if day not in st.session_state.itinerary:
        continue

    details = st.session_state.itinerary[day]

    st.markdown(
        f"""
        <div class='day-card'>
            <h2 class='day-title'>🩷 {day}</h2>
            <div class='theme-box'>
                <div class='theme'>{details['theme']}</div>
                <div class='dress-code'>Dress Code: {details['dress_code']}</div>
                <p class='description'>{details['description']}</p>
            </div>
        """,
        unsafe_allow_html=True
    )

    for item in details["events"]:
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
            day_order
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

                supabase.table("events").insert({
                    "day": add_day,
                    "time": formatted_time,
                    "event": add_event
                }).execute()

                refresh_itinerary()
                st.success("Added and saved permanently 🩷")
                st.rerun()
            else:
                st.warning("Please type the event first.")

    st.divider()

    st.markdown("## 📝 Edit Day Theme, Dress Code, and Vibe")

    details_day = st.selectbox(
        "Which day do you want to update?",
        day_order,
        key="details_day"
    )

    new_theme = st.text_input(
        "Theme",
        value=st.session_state.itinerary[details_day]["theme"]
    )

    new_dress_code = st.text_input(
        "Dress Code",
        value=st.session_state.itinerary[details_day]["dress_code"]
    )

    new_description = st.text_area(
        "Vibe / Description",
        value=st.session_state.itinerary[details_day]["description"]
    )

    if st.button("💾 Save Day Text"):
        supabase.table("day_details").update({
            "theme": new_theme,
            "dress_code": new_dress_code,
            "description": new_description
        }).eq("day", details_day).execute()

        refresh_itinerary()
        st.success("Day text saved permanently 🩷")
        st.rerun()

    st.divider()

    st.markdown("## ⚠️ Edit or Delete Existing Plans")

    confirm_edit = st.checkbox(
        "Yes, I am sure I want to edit or delete something already on the itinerary."
    )

    if confirm_edit:
        edit_day = st.selectbox(
            "Which day do you want to edit?",
            day_order,
            key="edit_day"
        )

        for i, item in enumerate(st.session_state.itinerary[edit_day]["events"]):
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

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Save This Item", key=f"save_{edit_day}_{i}"):
                    supabase.table("events").update({
                        "time": new_time,
                        "event": new_event
                    }).eq("id", item["id"]).execute()

                    refresh_itinerary()
                    st.success("Item saved permanently 🩷")
                    st.rerun()

            with col2:
                if st.button("🗑️ Delete This Item", key=f"delete_{edit_day}_{i}"):
                    supabase.table("events").delete().eq("id", item["id"]).execute()

                    refresh_itinerary()
                    st.success("Item deleted 🩷")
                    st.rerun()

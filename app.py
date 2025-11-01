import streamlit as st
import pandas as pd
import os
import base64
import datetime

# ------------------------
# CONFIG
# ------------------------
st.set_page_config(
    page_title="FYNDERS",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------
# CUSTOM CSS
# ------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
body, .stApp, .block-container, .main {background: linear-gradient(135deg, #ff9f43, #ff6b00); color: white; font-family: 'Helvetica', sans-serif;}
a {color: white !important; text-decoration: none;}
p, h1, h2, h3, h4, h5, h6, li, span {color: white !important;}
.stButton>button {background: linear-gradient(90deg, #ffb84d, #ff6b00); color: white; font-weight: bold; border-radius: 15px; padding: 15px; font-size: 18px; width: 100%; transition: all 0.2s ease-in-out;}
.stButton>button:hover {transform: scale(1.05); box-shadow: 0 4px 15px rgba(0,0,0,0.3);}
.stDataFrame, .stMarkdown {border-radius: 15px; background: rgba(255, 255, 255, 0.08); padding: 15px; margin-bottom: 20px;}
.card {border-radius: 15px; background: rgba(255,255,255,0.05); padding: 15px; margin-bottom: 20px;}
.stTextInput>div>div>input {color: white;}
.stTextArea textarea {color: white;}
.chat-bubble {padding:10px; margin-bottom:5px; border-radius:10px;}
.chat-bubble.user {background: rgba(255,255,255,0.2);}
.chat-bubble.admin {background: rgba(0,0,0,0.3);}
.chat-timestamp {font-size:10px; color: #ccc; text-align:right;}
@media(max-width:768px){
    .stTextInput>div>div>input, .stTextArea textarea {color:white; background:black;}
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# UPLOAD FOLDER & CSV
# ------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
DB_FILE = "uploads_db.csv"

# Load previous uploads
if os.path.exists(DB_FILE):
    db = pd.read_csv(DB_FILE)
    if not db.empty:
        db['timestamp'] = pd.to_datetime(db['timestamp'], errors='coerce')
else:
    db = pd.DataFrame(columns=["type","file_path","text","timestamp"])

# ------------------------
# SESSION STATE
# ------------------------
if "page" not in st.session_state: st.session_state.page = "Home"
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "email" not in st.session_state: st.session_state.email = ""

# ------------------------
# MOBILE-FRIENDLY TOP LOGIN
# ------------------------
if st.session_state.email == "":
    st.markdown("### 👋 Please log in")
    email_input_top = st.text_input("Enter your email to continue", key="top_login")
    if email_input_top:
        st.session_state.email = email_input_top
        st.session_state.is_admin = email_input_top.lower().endswith("@c25.com")
        if st.session_state.is_admin:
            st.success(f"✅ Admin: {email_input_top}")
        else:
            st.info(f"👤 User: {email_input_top}")

# ------------------------
# SIDEBAR LOGIN
# ------------------------
st.sidebar.header("Login")
email_input_sidebar = st.sidebar.text_input("Enter your email", value=st.session_state.email, key="sidebar_login")
if email_input_sidebar:
    st.session_state.email = email_input_sidebar
    st.session_state.is_admin = email_input_sidebar.lower().endswith("@c25.com")
    if st.session_state.is_admin:
        st.sidebar.success(f"✅ Admin: {email_input_sidebar}")
    else:
        st.sidebar.info(f"👤 User: {email_input_sidebar}")
else:
    st.sidebar.warning("Please enter your email to continue.")

email = st.session_state.email
is_admin = st.session_state.is_admin

# ------------------------
# NAVIGATION BUTTONS
# ------------------------
st.title("✨ FYNDERS — Field Outreach App")
st.subheader("Connecting Christians Worldwide")
st.markdown("Select a section below to get started:")

col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Home"): st.session_state.page = "Home"
    if st.button("✍️ Field Entry"): st.session_state.page = "Field Entry"
    if st.button("🎥 Media & Resources"): st.session_state.page = "Media & Resources"
    if st.button("📍 Locations"): st.session_state.page = "Locations"
    if st.button("📜 Word of Week"): st.session_state.page = "Word of Week"
with col2:
    if st.button("🚨 Report an Incident"): st.session_state.page = "Report Incident"
    if st.button("📖 Christian Feed"): st.session_state.page = "Christian Feed"
    if st.button("🏛 Tabernacle of David"): st.session_state.page = "Tabernacle of David"
    if st.button("💬 Internal Chat"): st.session_state.page = "Internal Chat"
    if st.button("💳 Donations"): st.session_state.page = "Donations"
    if st.button("ℹ️ About Us"): st.session_state.page = "About Us"
    if st.button("🛠 Services"): st.session_state.page = "Services"
    if st.button("🛒 Store"): st.session_state.page = "Store"
    if st.button("📋 Admin Dashboard"): st.session_state.page = "Admin"

page = st.session_state.page

# ------------------------
# DOWNLOAD HELPER
# ------------------------
def get_download_link(file_path, label):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}" style="color:#ffcc70;">📥 {label}</a>'

# ------------------------
# HOME PAGE
# ------------------------
if page == "Home":
    st.header("🌍 Connecting Christians Worldwide")
    st.markdown("""**Features at your fingertips:**  
- Give online securely; access church ministry resources.  
- Watch videos and pictures of worship, events, and community outreach.  
- Speak psalms, hymns, spiritual songs and upload your own songs.  
- Read the Bible and download e-books from the commission.  
- Listen to 24-hour worship music and download TOD Daily prayers.  
- Find a C25 or CC3 location near you.  
- Report incidents affecting any member that needs urgent attention.  
- Connect globally — translations to 7000+ languages.""")

    st.markdown("**Daily Bible Verse:**")
    st.info("“For I know the plans I have for you,” declares the Lord — Jeremiah 29:11", icon="📖")

# ------------------------
# FIELD ENTRY
# ------------------------
elif page == "Field Entry":
    st.header("✍️ Field Entry")
    with st.form("field_form"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name")
            contact_info = st.text_input("Contact Info (Phone/Email)")
            location = st.text_input("Location (City / Area)")
        with col2:
            needs = st.multiselect(
                "Needs / Requests",
                ["Follow-Up", "Welfare – Food", "Counselling", "Prayer", "Bible Materials", "Visit"],
                default=["Follow-Up"]
            )
            notes = st.text_area("Notes / Additional Details", height=120)
        submitted = st.form_submit_button("Submit Entry 🧡")
        if submitted:
            entry = {
                "Full Name": full_name,
                "Contact Info": contact_info,
                "Location": location,
                "Needs": ", ".join(needs),
                "Notes": notes,
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            file_path = "field_entries.csv"
            backup_path = "field_entries_backup.csv"
            df_new = pd.DataFrame([entry])

            # Save main CSV
            if os.path.exists(file_path):
                df_new.to_csv(file_path, mode='a', index=False, header=False)
            else:
                df_new.to_csv(file_path, index=False)

            # Always update backup CSV
            if os.path.exists(backup_path):
                df_new.to_csv(backup_path, mode='a', index=False, header=False)
            else:
                df_new.to_csv(backup_path, index=False)

            st.success("✅ Entry submitted successfully and saved securely!")

# ------------------------
# MEDIA & RESOURCES
# ------------------------
elif page == "Media & Resources":
    st.header("🎥 Media & Resources")
    st.video("https://www.youtube.com/watch?v=F0OzffuqASQ")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    st.button("Upload Your Song / Resource")
    st.markdown("Downloadable e-books, daily prayers, and Bible study materials coming soon!")

# ------------------------
# LOCATIONS
# ------------------------
elif page == "Locations":
    st.header("📍 Find a C25 or CC3 Location")
    office_address = "135 W 56th Street, New York, New York 10019, 9TH Floor"
    latitude = 40.7651
    longitude = -73.9819
    user_input = st.text_input("Enter City / Area")
    if st.button("Search Locations"):
        st.success(f"📍 Our Office Location:\n{office_address}")
        st.map(pd.DataFrame([[latitude, longitude]], columns=["lat", "lon"]))

# ------------------------
# REPORT INCIDENT
# ------------------------
elif page == "Report Incident":
    st.header("🚨 Report an Incident")
    st.text_area("Describe the Incident", height=150)
    st.button("Submit Report 🧡")
    st.info("All reports are monitored by Admins.")

# ------------------------
# CHRISTIAN FEED
# ------------------------
elif page == "Christian Feed":
    st.header("📖 Christian Feed")
    posts = [
        {"verse": "Psalm 23:1-2", "text": "The Lord is my shepherd; I shall not want."},
        {"verse": "John 3:16", "text": "For God so loved the world that He gave His only Son."},
        {"verse": "Philippians 4:13", "text": "I can do all things through Christ who strengthens me."},
        {"verse": "Romans 12:12", "text": "Be joyful in hope, patient in affliction, faithful in prayer."},
        {"verse": "1 Corinthians 13:4-5", "text": "Love is patient, love is kind..."}
    ]
    for post in posts:
        st.markdown(f"<div class='card'><h3>{post['verse']}</h3><p>{post['text']}</p></div>", unsafe_allow_html=True)

# ------------------------
# WORD OF THE WEEK
# ------------------------
elif page == "Word of Week":
    word_files = db[db['type'] == "word_of_week"]
    latest_file_path = None
    if not word_files.empty:
        latest = word_files.sort_values("timestamp").iloc[-1]
        latest_file_path = latest['file_path']
        file_ext = os.path.splitext(latest_file_path)[1].lower()
        if file_ext == ".pdf":
            st.markdown(get_download_link(latest_file_path, "Download PDF"), unsafe_allow_html=True)
        elif file_ext in [".png", ".jpg", ".jpeg"]:
            st.image(latest_file_path, caption="Word of the Week Image", use_container_width=True)
            st.markdown(get_download_link(latest_file_path, "Download Image"), unsafe_allow_html=True)
        else:
            with open(latest_file_path, "r", encoding="utf-8") as f: st.text(f.read())
            st.markdown(get_download_link(latest_file_path, "Download Text File"), unsafe_allow_html=True)
    else:
        st.info("No Word of the Week uploaded yet.")

    if is_admin:
        upload = st.file_uploader(
            "Upload Word of the Week (PDF/Image/Text)", 
            type=["pdf","png","jpg","jpeg","txt"],
            key="word_upload",
            help="Current: " + (os.path.basename(latest_file_path) if latest_file_path else "None")
        )
        if upload:
            save_path = os.path.join(UPLOAD_DIR, upload.name)
            with open(save_path, "wb") as f: f.write(upload.read())
            new_row = {"type":"word_of_week","file_path":save_path,"text":"","timestamp":datetime.datetime.now()}
            db = pd.concat([db, pd.DataFrame([new_row])], ignore_index=True)
            db.to_csv(DB_FILE,index=False)
            st.success("✅ Word of the Week uploaded successfully!")

# ------------------------
# TABERNACLE
# ------------------------
elif page == "Tabernacle of David":
    tab_files = db[db['type'] == "tabernacle"]
    latest_file_path = None
    if not tab_files.empty:
        latest = tab_files.sort_values("timestamp").iloc[-1]
        latest_file_path = latest['file_path']
        st.markdown(get_download_link(latest_file_path, "Download Tabernacle PDF"), unsafe_allow_html=True)
    else:
        st.info("No Tabernacle uploaded yet.")

    if is_admin:
        upload = st.file_uploader(
            "Upload Tabernacle PDF", 
            type=["pdf"],
            key="tab_upload",
            help="Current: " + (os.path.basename(latest_file_path) if latest_file_path else "None")
        )
        if upload:
            save_path = os.path.join(UPLOAD_DIR, upload.name)
            with open(save_path, "wb") as f: f.write(upload.read())
            new_row = {"type":"tabernacle","file_path":save_path,"text":"","timestamp":datetime.datetime.now()}
            db = pd.concat([db, pd.DataFrame([new_row])], ignore_index=True)
            db.to_csv(DB_FILE,index=False)
            st.success("✅ Tabernacle uploaded successfully!")

# ------------------------
# INTERNAL CHAT
# ------------------------
elif page == "Internal Chat":
    st.header("💬 Internal Chat")
    CHAT_FILE = "chat_db.csv"
    if not os.path.exists(CHAT_FILE):
        pd.DataFrame(columns=["timestamp","user","message"]).to_csv(CHAT_FILE,index=False)
    chat_df = pd.read_csv(CHAT_FILE)
    
    # Display messages
    for _, row in chat_df.iterrows():
        bubble_class = "admin" if row["user"].lower().endswith("@c25.com") else "user"
        st.markdown(f"<div class='chat-bubble {bubble_class}'><b>{row['user']}</b>: {row['message']}<div class='chat-timestamp'>{row['timestamp']}</div></div>", unsafe_allow_html=True)
    
    # Send new message
    with st.form("chat_form"):
        user_message = st.text_input("Enter message")
        send = st.form_submit_button("Send")
        if send and email and user_message.strip() != "":
            new_msg = pd.DataFrame([{"timestamp":datetime.datetime.now(), "user":email, "message":user_message.strip()}])
            chat_df = pd.concat([chat_df,new_msg], ignore_index=True)
            chat_df.to_csv(CHAT_FILE,index=False)
            st.experimental_rerun()

# ------------------------
# DONATIONS
# ------------------------
elif page == "Donations":
    st.header("💳 Donations / Giving")
    st.info("Secure giving coming soon! Connects directly to bank account.")
    st.number_input("Amount to donate", min_value=1, step=1, key="donation_amount")
    st.text_input("Name on Card / Account", key="donor_name")
    st.text_input("Email", key="donor_email")
    st.button("Donate 🧡")

# ------------------------
# ABOUT US
# ------------------------
elif page == "About Us":
    st.header("ℹ️ About Us")
    st.markdown("""
**Apostle:** Apostle [Name]  
**Mission Statement:** To connect Christians worldwide, provide spiritual resources, and empower communities through outreach and ministry.
""")

# ------------------------
# SERVICES
# ------------------------
elif page == "Services":
    st.header("🛠 Services")
    st.markdown("""
- Counselling & Prayer  
- Bible Distribution  
- Community Outreach  
- Worship & Music Resources  
- Online Classes and Workshops
""")

# ------------------------
# STORE
# ------------------------
elif page == "Store":
    st.header("🛒 Store")
    st.markdown("""
Merchandise, books, and ministry resources coming soon!
""")

# ------------------------
# ADMIN DASHBOARD
# ------------------------
elif page == "Admin":
    st.header("📋 Admin Dashboard")
    if is_admin:
        st.header("📋 Admin Dashboard – Follow-Up Overview")
        file_path = "field_entries.csv"
        backup_path = "field_entries_backup.csv"
        if os.path.exists(file_path):
            entries_df = pd.read_csv(file_path)
        elif os.path.exists(backup_path):
            entries_df = pd.read_csv(backup_path)
            st.warning("⚠️ Main CSV missing. Loaded from backup.")
        else:
            entries_df = pd.DataFrame()
        if entries_df.empty:
            st.info("No field entries submitted yet.")
        else:
            st.dataframe(entries_df, use_container_width=True)
    else:
        st.warning("❌ Only admins can access this section.")

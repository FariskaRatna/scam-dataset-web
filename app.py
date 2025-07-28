import streamlit as st
from supabase import create_client
import uuid

# Koneksi Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase = create_client(url, key)

# Judul Aplikasi
st.title("📌 Input Dataset Scam")

# --- Contoh Chat Scam & Non-Scam ---
with st.expander("📌 Lihat Contoh Chat Scam & Non-Scam"):
    st.markdown("### 🚨 Contoh Chat Scam")
    st.markdown(
        """
        <div style="background-color:#ffe5e5; padding:10px; border-radius:5px;">
        <b>𝗦𝗧𝗢𝗣 𝗕𝗘𝗞𝗘𝗥𝗝𝗔 𝗞𝗘𝗥𝗔𝗦 ⛔</b><br>
        𝗦𝗔𝗔𝗧𝗡𝗬𝗔 𝗕𝗘𝗞𝗘𝗥𝗝𝗔 𝗖𝗘𝗥𝗗𝗔𝗦<br><br>
        𝗧𝗜𝗡𝗚𝗞𝗔𝗧𝗞𝗔𝗡 𝗣𝗘𝗡𝗗𝗔𝗣𝗔𝗧𝗔𝗡 𝗔𝗡𝗗𝗔 𝗠𝗘𝗟𝗔𝗟𝗨𝗜 𝗜𝗡𝗩𝗘𝗦𝗧𝗔𝗦𝗜 𝗧𝗥𝗔𝗗𝗜𝗡𝗚 𝗙𝗢𝗥𝗘𝗫 📈<br>
        𝗧𝗿𝗮𝗱𝗶𝗻𝗴 𝗙𝗼𝗿𝗲𝘅 ... (pesan panjang scam trading)<br>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💬 Contoh Chat Non-Scam (Chat Biasa)")
    st.markdown(
        """
        <div style="background-color:#e8ffe8; padding:10px; border-radius:5px;">
        A: Hai, gimana kabarnya?<br>
        B: Baik, kamu gimana?<br>
        A: Sama, baik juga. Lagi sibuk kerjaan kantor.<br>
        B: Semangat ya! 💪<br>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Session State untuk jumlah input dinamis ---
MAX_MESSAGES = 15
if "scam_count" not in st.session_state:
    st.session_state.scam_count = 1
if "no_scam1_count" not in st.session_state:
    st.session_state.no_scam1_count = 1
if "no_scam2_count" not in st.session_state:
    st.session_state.no_scam2_count = 1

# --- Form Data Dasar ---
st.header("📝 Form Data Pelapor")
name = st.text_input("Nama Panggilan")
age = st.number_input("Usia", 0, 120, step=1)
no_hp = st.text_input("Nomor yang bisa dihubungi")
platform = st.selectbox("Platform", ["WhatsApp", "Instagram", "Telegram", "Facebook", "Lainnya"])
bank = st.text_input("Bank yang digunakan")
rekening = st.text_input("Nomor rekening")
victim = st.text_input("Pernah menjadi korban? Kerugian mencapai berapa?")

# --- Input Pesan Scam ---
st.header("📩 Input Pesan")
st.subheader("Pesan Scam")
scam_texts = [st.text_area(f"Pesan Scam {i+1}", key=f"scam_{i}") for i in range(st.session_state.scam_count)]
if st.button("➕ Tambah Pesan Scam"):
    if st.session_state.scam_count < MAX_MESSAGES:
        st.session_state.scam_count += 1

# --- Input Pesan Non-Scam 1 ---
st.subheader("Pesan Non-Scam 1")
no_scam_texts_1 = [st.text_area(f"Pesan Non-Scam 1 - {i+1}", key=f"no_scam1_{i}") for i in range(st.session_state.no_scam1_count)]
if st.button("➕ Tambah Pesan Non-Scam 1"):
    if st.session_state.no_scam1_count < MAX_MESSAGES:
        st.session_state.no_scam1_count += 1

# --- Input Pesan Non-Scam 2 ---
st.subheader("Pesan Non-Scam 2")
no_scam_texts_2 = [st.text_area(f"Pesan Non-Scam 2 - {i+1}", key=f"no_scam2_{i}") for i in range(st.session_state.no_scam2_count)]
if st.button("➕ Tambah Pesan Non-Scam 2"):
    if st.session_state.no_scam2_count < MAX_MESSAGES:
        st.session_state.no_scam2_count += 1

# --- Upload Gambar ---
uploaded_images = st.file_uploader(
    "📷 Upload Screenshot Chat Scam (maksimal 15 gambar)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)
image_urls = []

# --- Simpan ke Database ---
if st.button("💾 Simpan Data"):
    for image in uploaded_images:
        file_name = f"{uuid.uuid4()}_{image.name}"
        supabase.storage.from_("scam-images").upload(file_name, image.getvalue())
        image_url = f"{url}/storage/v1/object/public/scam-images/{file_name}"
        image_urls.append(image_url)

    supabase.table("scam-dataset").insert({
        "name": name,
        "age": age,
        "no_hp": no_hp,
        "platform": platform,
        "bank": bank,
        "rekening": rekening,
        "victim": victim,
        "scam_texts": scam_texts,
        "no_scam_texts_1": no_scam_texts_1,
        "no_scam_texts_2": no_scam_texts_2,
        "image_urls": image_urls
    }).execute()

    st.success("✅ Data berhasil disimpan!")

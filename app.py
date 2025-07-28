import streamlit as st
from supabase import create_client
import uuid

# Koneksi Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase = create_client(url, key)

st.title("📌 Input Dataset Scam")

# --- Session State untuk jumlah input dinamis ---
if "scam_count" not in st.session_state:
    st.session_state.scam_count = 1

if "no_scam1_count" not in st.session_state:
    st.session_state.no_scam1_count = 1

if "no_scam2_count" not in st.session_state:
    st.session_state.no_scam2_count = 1

# --- Form Data Dasar ---
name = st.text_input("Nama")
age = st.number_input("Usia", 0, 120, step=1)
no_hp = st.text_input("Nomor yang bisa dihubungi")
platform = st.selectbox("Platform", ["WhatsApp", "Instagram", "Telegram", "Facebook", "Lainnya"])

# --- Input Pesan Scam ---
st.subheader("Pesan Scam")
scam_texts = []
for i in range(st.session_state.scam_count):
    scam_texts.append(st.text_area(f"Pesan Scam {i+1}", key=f"scam_{i}"))

if st.button("➕ Tambah Pesan Scam"):
    if st.session_state.scam_count < 10:
        st.session_state.scam_count += 1

# --- Input Pesan Non-Scam 1 ---
st.subheader("Pesan Non-Scam 1")
no_scam_texts_1 = []
for i in range(st.session_state.no_scam1_count):
    no_scam_texts_1.append(st.text_area(f"Pesan Non-Scam 1 - {i+1}", key=f"no_scam1_{i}"))

if st.button("➕ Tambah Pesan Non-Scam 1"):
    if st.session_state.no_scam1_count < 10:
        st.session_state.no_scam1_count += 1

# --- Input Pesan Non-Scam 2 ---
st.subheader("Pesan Non-Scam 2")
no_scam_texts_2 = []
for i in range(st.session_state.no_scam2_count):
    no_scam_texts_2.append(st.text_area(f"Pesan Non-Scam 2 - {i+1}", key=f"no_scam2_{i}"))

if st.button("➕ Tambah Pesan Non-Scam 2"):
    if st.session_state.no_scam2_count < 10:
        st.session_state.no_scam2_count += 1

# --- Upload Gambar ---
uploaded_images = st.file_uploader(
    "Upload Screenshot bila Chat dalam Bentuk Gambar (maksimal 10 gambar)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)
image_urls = []

# --- Simpan ke Database ---
if st.button("💾 Simpan"):
    # Upload semua gambar
    for image in uploaded_images:
        file_name = f"{uuid.uuid4()}_{image.name}"
        supabase.storage.from_("scam-images").upload(file_name, image.getvalue())
        image_url = f"{url}/storage/v1/object/public/scam-images/{file_name}"
        image_urls.append(image_url)

    # Insert data ke tabel
    supabase.table("scam-dataset").insert({
        "name": name,
        "age": age,
        "no_hp": no_hp,
        "platform": platform,
        "scam_texts": scam_texts,
        "no_scam_texts_1": no_scam_texts_1,
        "no_scam_texts_2": no_scam_texts_2,
        "image_urls": image_urls
    }).execute()

    st.success("✅ Data berhasil disimpan!")

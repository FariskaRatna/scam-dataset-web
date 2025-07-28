import streamlit as st
from supabase import create_client
import uuid

# Koneksi Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase = create_client(url, key)

st.title("📌 Input Dataset Scam")

# Form Input
name = st.text_input("Nama")
age = st.number_input("Usia", 0, 120, step=1)
no_hp = st.text_input("Nomor yang bisa dihubungi")
platform = st.selectbox("Platform", ["WhatsApp", "Instagram", "Telegram", "Facebook", "Lainnya"])

# Input hingga 10 chat scam
scam_texts = []
st.subheader("Pesan Scam (maksimal 10)")
for i in range(1, 11):
    text_val = st.text_area(f"Pesan Scam {i}", key=f"scam_{i}")
    if text_val:
        scam_texts.append(text_val)

# Input hingga 10 chat non-scam
no_scam_texts_1 = []
st.subheader("Pesan Non-Scam 1 (maksimal 10)")
for i in range(1, 11):
    text_val = st.text_area(f"Pesan Non-Scam 1 {i}", key=f"no_scam_1_{i}")
    if text_val:
        no_scam_texts_1.append(text_val)

no_scam_texts_2 = []
st.subheader("Pesan Non-Scam 2 (maksimal 10)")
for i in range(1, 11):
    text_val = st.text_area(f"Pesan Non-Scam 2 {i}", key=f"no_scam_2_{i}")
    if text_val:
        no_scam_texts_2.append(text_val)

# Upload hingga banyak gambar
uploaded_images = st.file_uploader(
    "Upload Screenshot bila Chat dalam Bentuk Gambar (maksimal 10 gambar)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)
image_urls = []

if st.button("Simpan"):
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
        "scam_texts": scam_texts,       # array teks scam
        "no_scam_texts_1": no_scam_texts_1, # array teks non-scam
        "no_scam_texts_2": no_scam_texts_2, # array teks non-scam
        "image_urls": image_urls        # array URL gambar
    }).execute()

    st.success("✅ Data berhasil disimpan!")

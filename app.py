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
platform = st.selectbox("Platform", ["WhatsApp", "Instagram", "Telegram", "Facebook", "Lainnya"])
scam = st.text_area("Contoh Pesan Scam")
no_scam_1 = st.text_area("Contoh Pesan Non-Scam 1")
no_scam_2 = st.text_area("Contoh Pesan Non-Scam 2")
image = st.file_uploader("Upload Screenshot (opsional)", type=["png", "jpg", "jpeg"])

if st.button("Simpan"):
    img_url = None
    
    # Upload gambar jika ada
    if image:
        file_name = f"{uuid.uuid4()}_{image.name}"
        supabase.storage.from_("scam-images").upload(file_name, image.getvalue())
        img_url = f"{url}/storage/v1/object/public/scam-images/{file_name}"
    
    # Insert data ke tabel
    supabase.table("scam-dataset").insert({
        "name": name,
        "age": age,
        "platform": platform,
        "scam": scam,
        "no_scam_1": no_scam_1,
        "no_scam_2": no_scam_2,
        "img_url": img_url
    }).execute()
    
    st.success("✅ Data berhasil disimpan!")

# Menampilkan data
st.subheader("📊 Data Tersimpan")
data = supabase.table("scam-dataset").select("*").order("id", desc=True).execute()

for row in data.data:
    st.write(f"**Nama:** {row['name']} | **Platform:** {row['platform']}")
    st.write(f"Pesan Scam: {row['scam']}")
    if row['img_url']:
        st.image(row['img_url'], width=300)
    st.markdown("---")

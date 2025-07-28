import streamlit as st
import psycopg2
from supabase import create_client, Client
import uuid

# Koneksi database
@st.cache_resource
def connect_db():
    return psycopg2.connect(
        host=st.secrets["db"]["host"],
        database=st.secrets["db"]["database"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        port=st.secrets["db"]["port"]
    )

# Koneksi storage
@st.cache_resource
def connect_storage():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

conn = connect_db()
cursor = conn.cursor()
supabase: Client = connect_storage()

st.title("📌 Input Dataset Scam")

# Form
name = st.text_input("Nama")
age = st.number_input("Usia", 0, 120, step=1)
platform = st.selectbox("Platform", ["WhatsApp", "Instagram", "Telegram", "Facebook", "Lainnya"])
scam = st.text_area("Contoh Pesan Scam")
non_scam_1 = st.text_area("Contoh Pesan Non-Scam 1")
non_scam_2 = st.text_area("Contoh Pesan Non-Scam 2")
image = st.file_uploader("Upload Screenshot (opsional)", type=["png", "jpg", "jpeg"])

if st.button("Simpan"):
    image_url = None
    if image:
        file_name = f"{uuid.uuid4()}_{image.name}"
        supabase.storage.from_("scam-images").upload(file_name, image.getvalue())
        image_url = f"{st.secrets['supabase']['url']}/storage/v1/object/public/scam-images/{file_name}"
    
    insert_query = """
        INSERT INTO scam_dataset (name, age, platform, scam, non_scam_1, non_scam_2, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, age, platform, scam, non_scam_1, non_scam_2, image_url))
    conn.commit()
    st.success("✅ Data berhasil disimpan!")

# Tampilkan data
st.subheader("📊 Data Tersimpan")
cursor.execute("SELECT name, platform, scam, image_url FROM scam_dataset ORDER BY id DESC")
rows = cursor.fetchall()
for row in rows:
    st.write(f"**Nama:** {row[0]} | **Platform:** {row[1]}")
    st.write(f"Pesan Scam: {row[2]}")
    if row[3]:
        st.image(row[3], width=300)
    st.markdown("---")

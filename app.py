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
        Hallo semuanya 👋
        Ada yang mau nyobain jadi BUZZER ga kakak???

        Gajinya lumayan banget loh bisa melebihi UMR kalau rajin cukup modal tiktok saja! 
        Tanpa batasan usia loh semua kalangan bisa join!

        Misi: hanya like doang, per tugasnya pasti di bayar 50-70k
        Chat saya sekarang buruan cuan 🤑🤑🤑

        Lumayan buat tambah uang jajan kalian 🙌🙌🙌
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
for counter in ["scam_count", "no_scam1_count", "no_scam2_count"]:
    if counter not in st.session_state:
        st.session_state[counter] = 1

# --- Fungsi tambah field ---
def add_field(counter_name, max_field):
    if st.session_state[counter_name] < max_field:
        st.session_state[counter_name] += 1

# --- Form Data Dasar ---
st.header("📝 Data Dasar")
name = st.text_input("Nama Panggilan")
age = st.number_input("Usia", 0, 120, step=1)
no_hp = st.text_input("Nomor yang bisa dihubungi")
platform = st.selectbox("Platform", ["WhatsApp", "Instagram", "Telegram", "Facebook", "Lainnya"])
bank = st.text_input("Bank yang digunakan")
rekening = st.text_input("Nomor rekening")
victim = st.text_input("Pernah menjadi korban? Kerugian mencapai berapa?")

# --- Input Pesan Scam ---
st.subheader("📩 Pesan Scam (Maksimal 15)")
scam_texts = []
for i in range(st.session_state.scam_count):
    scam_texts.append(st.text_area(f"Pesan Scam {i+1}", key=f"scam_{i}"))

if st.session_state.scam_count < 15:
    st.button("➕ Tambah Pesan Scam", on_click=add_field, args=("scam_count", 15))
else:
    st.button("✅ Sudah Maksimal", disabled=True)

# --- Input Pesan Non-Scam 1 ---
st.subheader("💬 Pesan Non-Scam 1 (Maksimal 15)")
no_scam_texts_1 = []
for i in range(st.session_state.no_scam1_count):
    no_scam_texts_1.append(st.text_area(f"Pesan Non-Scam 1 - {i+1}", key=f"no_scam1_{i}"))

if st.session_state.no_scam1_count < 15:
    st.button("➕ Tambah Pesan Non-Scam 1", on_click=add_field, args=("no_scam1_count", 15))
else:
    st.button("✅ Sudah Maksimal", disabled=True)

# --- Input Pesan Non-Scam 2 ---
st.subheader("💬 Pesan Non-Scam 2 (Maksimal 15)")
no_scam_texts_2 = []
for i in range(st.session_state.no_scam2_count):
    no_scam_texts_2.append(st.text_area(f"Pesan Non-Scam 2 - {i+1}", key=f"no_scam2_{i}"))

if st.session_state.no_scam2_count < 15:
    st.button("➕ Tambah Pesan Non-Scam 2", on_click=add_field, args=("no_scam2_count", 15))
else:
    st.button("✅ Sudah Maksimal", disabled=True)

# --- Upload Gambar ---
st.subheader("🖼 Upload Screenshot (Maksimal 15 Gambar)")
uploaded_images = st.file_uploader(
    "Upload Screenshot bila Chat Scam dalam Bentuk Gambar", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

image_urls = []

# --- Simpan ke Database ---
# if st.button("💾 Simpan Data"):
#     for image in uploaded_images:
#         file_name = f"{uuid.uuid4()}_{image.name}"
#         supabase.storage.from_("scam-images").upload(file_name, image.getvalue())
#         image_url = f"{url}/storage/v1/object/public/scam-images/{file_name}"
#         image_urls.append(image_url)

#     supabase.table("scam-dataset").insert({
#         "name": name,
#         "age": age,
#         "no_hp": no_hp,
#         "platform": platform,
#         "bank": bank,
#         "rekening": rekening,
#         "victim": victim,
#         "scam_texts": scam_texts,
#         "no_scam_texts_1": no_scam_texts_1,
#         "no_scam_texts_2": no_scam_texts_2,
#         "image_urls": image_urls
#     }).execute()

#     st.success("✅ Data berhasil disimpan!")

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

    # Reset input setelah simpan
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.success("✅ Data berhasil disimpan!")

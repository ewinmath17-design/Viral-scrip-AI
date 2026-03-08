import streamlit as st
from google import genai
from PIL import Image

# Konfigurasi Halaman Web
st.set_page_config(page_title="ViralScript AI", page_icon="🎬", layout="centered")

st.title("🎬 ViralScript AI")
st.write("Unggah screenshot produk, dan AI akan meracik skrip video pendek viral yang siap untuk mesin Text-to-Speech (TTS).")

# Mengambil API Key dari Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ API Key belum dipasang! Silakan atur GEMINI_API_KEY di pengaturan rahasia (Secrets) Streamlit Anda.")
    st.stop()

# Inisialisasi Klien AI dengan SDK TERBARU
client = genai.Client(api_key=api_key)

# Antarmuka Pengguna (UI)
st.markdown("---")
uploaded_file = st.file_uploader("📸 Unggah Gambar/Screenshot Produk (JPG/PNG)", type=["jpg", "jpeg", "png"])
style_input = st.text_input("🗣️ Gaya Bahasa/Logat (Opsional)", placeholder="Contoh: Gaya Kendari santai, logat Sunda, atau gaya ibu-ibu arisan")

if st.button("🚀 Generate Skrip Viral!"):
    if uploaded_file is not None:
        # Tampilkan gambar yang diunggah (Memperbaiki warning use_column_width)
        image = Image.open(uploaded_file)
        st.image(image, caption="Produk yang dianalisis", use_container_width=True)
        
        with st.spinner("🤖 Membedah produk dan meracik skrip Hook..."):
            try:
                # Prompt rahasia kita (Persona ViralScript AI)
                system_prompt = f"""
                Kamu adalah "ViralScript AI", seorang Creative Director, Copywriter handal, dan Ahli Algoritma TikTok/Reels kelas dunia.
                Tugas utamamu adalah menganalisis gambar/screenshot produk dan mengubahnya menjadi skrip video pendek yang berpotensi viral dan siap digunakan untuk Text-to-Speech (TTS).

                Gaya Bahasa yang diminta pengguna: {style_input if style_input else "Gaya kasual Indonesia yang tren di TikTok"}

                ATURAN UTAMA:
                1. Buat Hook super kuat di 3 detik pertama (Scroll-stopper).
                2. Gunakan gaya bahasa yang diminta agar terdengar natural dan hiper-lokal.
                3. Format harus siap TTS (Gunakan HURUF KAPITAL untuk nada tinggi/emosi, dan elipsis (...) untuk jeda).
                4. WAJIB ikuti format Markdown di bawah ini tanpa mengubah strukturnya.

                FORMAT OUTPUT:
                🎯 **ANALISIS PRODUK CEPAT**
                - Nama/Jenis Produk: [Tebakan dari gambar]
                - Nilai Jual Utama (USP): [1-2 kalimat mengapa produk ini bagus]
                - Target Audiens: [Siapa yang cocok membeli ini]

                🎬 **SKRIP VIDEO (Durasi: 15-30 Detik)**
                | Detik | Arahan Visual | Voice Over (Skrip TTS) |
                |---|---|---|
                | 00:00 - 00:03 | [Visual Hook] | "[Teks VO]" |
                | 00:03 - 00:10 | [Visual Penjelasan] | "[Teks VO]" |
                | 00:10 - 00:15 | [Visual Keunggulan] | "[Teks VO]" |
                | 00:15 - 00:20 | [Visual CTA] | "[Teks VO]" |

                📝 **CAPTION & SEO TIKTOK/IG REELS**
                - Caption: [Tulis caption yang mengundang komen]
                - Hashtags: [5-7 hashtag relevan]
                """
                
                # Mengirim gambar dan instruksi ke AI (Format baru)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[system_prompt, image]
                )
                
                # Menampilkan Hasil
                st.success("✨ Skrip Berhasil Dibuat!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Waduh, ada yang salah saat generate: {e}")
    else:
        st.error("⚠️ Harap unggah gambar produk terlebih dahulu Bosku!")

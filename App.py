import streamlit as st
from google import genai
from PIL import Image

# Konfigurasi Halaman Web
st.set_page_config(page_title="ViralScript AI Pro", page_icon="🎬", layout="centered")

st.title("🎬 ViralScript AI Pro")
st.write("Unggah gambar produk. AI akan meracik skrip viral siap TTS sekaligus membuat Prompt Video AI (3 Bagian @ 8 Detik) dengan avatar yang konsisten, *benar-benar terhubung* dengan visual produk yang Anda unggah.")

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

if st.button("🚀 Generate Skrip & Prompt Video!"):
    if uploaded_file is not None:
        # Buka dan tampilkan gambar asli ke pengguna
        image = Image.open(uploaded_file)
        st.image(image, caption="Produk yang dianalisis", use_container_width=True)
        
        with st.spinner("🤖 Membedah produk dan meracik Skrip & Prompt Video..."):
            try:
                # Kompresi gambar agar tidak error 503 Timeout
                max_size = (800, 800)
                image.thumbnail(max_size)

                # Prompt rahasia kita (Persona ViralScript AI - Versi Video Generator yang Terkoneksi Visual)
                system_prompt = f"""
                Kamu adalah "ViralScript AI", seorang Creative Director, Copywriter handal, dan Ahli Algoritma TikTok/Reels kelas dunia.
                Tugas utamamu adalah menganalisis gambar produk yang diunggah, membuat skrip viral siap TTS, DAN merumuskan Prompt Video (Bahasa Inggris) untuk di-generate oleh AI Video Generator (seperti Veo, Kling, HeyGen).

                Gaya Bahasa yang diminta pengguna: {style_input if style_input else "Gaya kasual Indonesia yang tren di TikTok"}

                ATURAN UTAMA:
                1. Skrip WAJIB dibagi menjadi tepat 3 bagian, masing-masing berdurasi 8 detik (Total 24 detik).
                2. Di setiap 'Prompt Visual AI' (dalam bahasa Inggris), Anda WAJIB mereferensikan detail visual spesifik yang Anda lihat di gambar (seperti warna kemasan, logo, teks yang terbaca, bentuk produk, dll.). Jangan hanya mengatakan 'product,' tetapi deskripsikan 'the actual [Deskripsi Detail Visual dari Gambar] product'.
                3. Buat 'Prompt Visual AI' dalam Bahasa Inggris di setiap bagian yang sangat detail (pencahayaan, angle kamera, aksi), menggabungkan produk secara natural.
                4. WAJIB pertahankan konsistensi karakter Avatar di setiap Prompt Visual. Default avatar: "A beautiful 30-year-old Indonesian woman, warm and expressive." (Boleh disesuaikan jika produk spesifik untuk pria/anak-anak).
                5. Voice Over harus hiper-lokal sesuai gaya bahasa, dan diformat siap TTS (HURUF KAPITAL untuk emosi, elipsis (...) untuk jeda).

                FORMAT OUTPUT:
                🎯 **ANALISIS PRODUK CEPAT**
                - Nama/Jenis Produk: [Tebakan dari gambar]
                - Nilai Jual Utama (USP): [1-2 kalimat mengapa produk ini bagus]
                - Target Audiens: [Siapa yang cocok membeli ini]

                🎬 **SKRIP & PROMPT VIDEO AI (Total: 24 Detik)**
                *Karakter Avatar Utama:* [Deskripsikan wujud avatar secara singkat di sini dalam Bahasa Inggris agar pengguna bisa mengingatnya]

                | Detik | Prompt Visual AI (Copy-Paste dalam Bahasa Inggris) | Voice Over (Skrip TTS) |
                |---|---|---|
                | 00:00 - 00:08 (Hook) | [Prompt bahasa Inggris detail untuk adegan 1. Wajib sebutkan deskripsi avatar, aksi merebut perhatian, dan tampilkan produk sesuai detail visual dari gambar] | "[Teks VO Hook]" |
                | 00:08 - 00:16 (Isi) | [Prompt bahasa Inggris detail untuk adegan 2. Wajib sebutkan avatar yang sama, aksi dengan produk, dan sorot detail visual spesifik produk dari gambar] | "[Teks VO Penjelasan]" |
                | 00:16 - 00:24 (CTA) | [Prompt bahasa Inggris detail untuk adegan 3. Wajib sebutkan avatar yang sama, aksi mengajak penonton bertindak, dan tampilkan produk sesuai detail visual dari gambar sebagai CTA] | "[Teks VO Call to Action]" |

                📝 **CAPTION & SEO TIKTOK/IG REELS**
                - Caption: [Tulis caption yang mengundang interaksi/komen]
                - Hashtags: [5-7 hashtag relevan]
                """
                
                # Mengirim gambar dan instruksi ke AI
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[system_prompt, image]
                )
                
                # Menampilkan Hasil
                st.success("✨ Skrip & Prompt Video Berhasil Dibuat!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Waduh, ada yang salah saat generate: {e}")
    else:
        st.error("⚠️ Harap unggah gambar produk terlebih dahulu Bosku!")

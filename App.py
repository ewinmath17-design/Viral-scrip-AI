import streamlit as st
from google import genai
from PIL import Image
from gtts import gTTS
import io

# Konfigurasi Halaman Web
st.set_page_config(page_title="ViralScript AI Pro", page_icon="🎬", layout="centered")

st.title("🎬 ViralScript AI Pro")
st.write("Unggah gambar produk. AI akan meracik skrip viral siap TTS sekaligus membuat Prompt Video AI (3 Bagian @ 8 Detik). Sekarang dilengkapi dengan Studio Voice Over!")

# Mengambil API Key dari Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ API Key belum dipasang! Silakan atur GEMINI_API_KEY di pengaturan rahasia (Secrets) Streamlit Anda.")
    st.stop()

# Inisialisasi Klien AI dengan SDK TERBARU
client = genai.Client(api_key=api_key)

# ----------------------------------------------------
# BAGIAN 1: GENERATOR SKRIP & PROMPT VIDEO
# ----------------------------------------------------
st.markdown("---")
st.header("1️⃣ Bedah Visual & Racik Skrip")
uploaded_file = st.file_uploader("📸 Unggah Gambar/Screenshot Produk (JPG/PNG)", type=["jpg", "jpeg", "png"])
style_input = st.text_input("🗣️ Gaya Bahasa/Logat (Opsional)", placeholder="Contoh: Gaya Kendari santai, logat Sunda, atau gaya ibu-ibu arisan")

if st.button("🚀 Generate Skrip & Prompt Video!"):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Produk yang dianalisis", use_container_width=True)
        
        with st.spinner("🤖 Membedah produk dan meracik Skrip & Prompt Video..."):
            try:
                max_size = (800, 800)
                image.thumbnail(max_size)

                system_prompt = f"""
                Kamu adalah "ViralScript AI", seorang Creative Director, Copywriter handal, dan Ahli Algoritma TikTok/Reels kelas dunia.
                Tugas utamamu adalah menganalisis gambar produk yang diunggah, membuat skrip viral siap TTS, DAN merumuskan Prompt Video (Bahasa Inggris) untuk di-generate oleh AI Video Generator.

                Gaya Bahasa yang diminta pengguna: {style_input if style_input else "Gaya kasual Indonesia yang tren di TikTok"}

                ATURAN UTAMA:
                1. Skrip WAJIB dibagi menjadi tepat 3 bagian, masing-masing berdurasi 8 detik (Total 24 detik).
                2. Di setiap 'Prompt Visual AI' (dalam bahasa Inggris), Anda WAJIB mereferensikan detail visual spesifik yang Anda lihat di gambar (seperti warna kemasan, logo, teks, bentuk produk).
                3. WAJIB pertahankan konsistensi karakter Avatar. Default avatar: "A beautiful 30-year-old Indonesian woman, warm and expressive."
                4. Voice Over harus hiper-lokal sesuai gaya bahasa.
                5. WAJIB ikuti struktur FORMAT OUTPUT di bawah ini, pastikan Prompt dan Voice Over diletakkan di dalam blok kode Markdown (menggunakan ```text dan ```) agar Streamlit memunculkan tombol copy.

                FORMAT OUTPUT:
                🎯 **ANALISIS PRODUK CEPAT**
                - Nama/Jenis Produk: [Tebakan dari gambar]
                - Nilai Jual Utama (USP): [1-2 kalimat]
                - Target Audiens: [Target]

                🎬 **SKRIP & PROMPT VIDEO AI (Total: 24 Detik)**
                *Karakter Avatar Utama:* [Deskripsikan wujud avatar secara singkat dalam Bahasa Inggris]

                ---
                **▶️ BAGIAN 1: THE HOOK (00:00 - 00:08)**
                **Prompt Visual AI (Salin ke Video Generator):**
                ```text
                [Tulis prompt bahasa Inggris detail untuk adegan 1 di sini]
                ```
                **Voice Over (Salin ke Studio TTS di bawah):**
                ```text
                [Teks VO Hook di sini]
                ```

                ---
                **▶️ BAGIAN 2: PENJELASAN (00:08 - 00:16)**
                **Prompt Visual AI (Salin ke Video Generator):**
                ```text
                [Tulis prompt bahasa Inggris detail untuk adegan 2 di sini]
                ```
                **Voice Over (Salin ke Studio TTS di bawah):**
                ```text
                [Teks VO Penjelasan di sini]
                ```

                ---
                **▶️ BAGIAN 3: CALL TO ACTION (00:16 - 00:24)**
                **Prompt Visual AI (Salin ke Video Generator):**
                ```text
                [Tulis prompt bahasa Inggris detail untuk adegan 3 di sini]
                ```
                **Voice Over (Salin ke Studio TTS di bawah):**
                ```text
                [Teks VO Call to Action di sini]
                ```

                📝 **CAPTION & SEO TIKTOK/IG REELS**
                - Caption: [Tulis caption yang mengundang interaksi]
                - Hashtags: [5-7 hashtag relevan]
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[system_prompt, image]
                )
                
                st.success("✨ Skrip & Prompt Video Berhasil Dibuat!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Waduh, ada yang salah saat generate: {e}")
    else:
        st.error("⚠️ Harap unggah gambar produk terlebih dahulu Bosku!")

# ----------------------------------------------------
# BAGIAN 2: STUDIO VOICE OVER (TEXT-TO-SPEECH)
# ----------------------------------------------------
st.markdown("---")
st.header("🎙️ 2️⃣ Studio Voice Over")
st.write("Salin teks *Voice Over* dari hasil di atas, lalu tempel (paste) di kotak bawah ini untuk mengubahnya menjadi suara yang bisa di-download.")

# Kotak input teks
tts_input = st.text_area("📝 Tempel Teks Skrip Di Sini:", height=150, placeholder="Contoh: WOY... JANGKO PUSING! Cari yang manis-manis untuk temani hari? Iyoo... ini dia jawabannya!")

if st.button("🎧 Generate Audio (MP3)"):
    if tts_input.strip() != "":
        with st.spinner("🎛️ Sedang memproses rekaman suara..."):
            try:
                # Mengubah teks menjadi suara (Bahasa Indonesia)
                tts = gTTS(text=tts_input, lang='id', slow=False)
                
                # Menyimpan audio ke dalam memory (tidak perlu save file ke server)
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                
                # Menampilkan pemutar audio
                st.success("✅ Audio berhasil dibuat!")
                st.audio(audio_bytes, format='audio/mp3')
                
                # Tombol Download
                st.download_button(
                    label="💾 Download Audio MP3",
                    data=audio_bytes,
                    file_name="voice_over_viralscript.mp3",
                    mime="audio/mp3"
                )
            except Exception as e:
                st.error(f"Gagal membuat audio: {e}")
    else:
        st.warning("⚠️ Kotak teksnya masih kosong, Bosku! Isi dulu skripnya.")

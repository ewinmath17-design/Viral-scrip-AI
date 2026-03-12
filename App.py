import streamlit as st
from google import genai
from PIL import Image
from gtts import gTTS
import io

# Konfigurasi Halaman Web
st.set_page_config(page_title="ViralScript AI Pro Ultimate", page_icon="🎬", layout="centered")

st.title("🎬 ViralScript AI Pro Ultimate 2.0")
st.write("Studio Konten Viral: 1️⃣ Bedah Skrip | 2️⃣ Studio Voice Over | 3️⃣ Prompt Kunci Wajah (Talking Head Workflow)")

# Mengambil API Key dari Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ API Key belum dipasang! Silakan atur GEMINI_API_KEY di pengaturan rahasia (Secrets) Streamlit Anda.")
    st.stop()

# Inisialisasi Klien AI dengan SDK TERBARU
client = genai.Client(api_key=api_key)

# ----------------------------------------------------
# INISIALISASI SESSION STATE (Buku Catatan Rahasia)
# ----------------------------------------------------
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'analysis_output' not in st.session_state:
    st.session_state.analysis_output = None
if 'script_full_output' not in st.session_state:
    st.session_state.script_full_output = None
if 'avatar_consistency_prompt' not in st.session_state:
    st.session_state.avatar_consistency_prompt = None

# ----------------------------------------------------
# BAGIAN 1: GENERATOR SKRIP & PROMPT VIDEO
# ----------------------------------------------------
st.markdown("---")
st.header("1️⃣ Bedah Visual & Racik Skrip")
uploaded_file = st.file_uploader("📸 Unggah Gambar/Screenshot Produk (JPG/PNG)", type=["jpg", "jpeg", "png"])
style_input = st.text_input("🗣️ Gaya Bahasa/Logat (Opsional)", placeholder="Contoh: Gaya Kendari santai, logat Sunda, atau gaya ibu-ibu arisan")

if st.button("🚀 Generate Skrip & Prompt Video!"):
    if uploaded_file is not None:
        # Buka, Kompres, dan Tampilkan Gambar Asli
        image = Image.open(uploaded_file)
        st.session_state.uploaded_image = image # Simpan gambar ke session state
        
        with st.spinner("🤖 Membedah produk dan meracik Skrip & Prompt Video..."):
            try:
                # Kompresi gambar agar tidak timeout
                max_size = (800, 800)
                image_for_api = image.copy()
                image_for_api.thumbnail(max_size)

                # Prompt rahasia kita (Persona ViralScript AI - Versi Talking Head Workflow)
                system_prompt = f"""
                Kamu adalah "ViralScript AI", seorang Creative Director, Copywriter handal, dan Ahli Algoritma TikTok/Reels kelas dunia.
                Tugas utamamu adalah menganalisis gambar produk yang diunggah, membuat skrip viral siap TTS, DAN merumuskan Prompt Video (Bahasa Inggris) untuk di-generate oleh AI Video Generator.

                Gaya Bahasa yang diminta pengguna: {style_input if style_input else "Gaya kasual Indonesia yang tren di TikTok"}

                ATURAN UTAMA:
                1. Skrip WAJIB dibagi menjadi tepat 3 bagian, masing-masing berdurasi 8 detik (Total 24 detik).
                2. Di setiap 'Prompt Visual AI' (dalam bahasa Inggris), Anda WAJIB mereferensikan detail visual spesifik yang Anda lihat di gambar (logo, teks, warna kemasan).
                3. Pertahankan konsistensi karakter Avatar. Default: "A beautiful 30-year-old Indonesian woman, warm and expressive."
                4. Voice Over harus hiper-lokal sesuai gaya bahasa, dan diformat siap TTS.
                5. WAJIB ikuti struktur FORMAT OUTPUT di bawah ini. Letakkan Prompt dan Voice Over di dalam blok kode Markdown (menggunakan ```text dan ```) agar muncul tombol copy.

                FORMAT OUTPUT:
                🎯 **ANALISIS PRODUK CEPAT**
                - Nama/Jenis Produk: [Tebakan dari gambar]
                - Nilai Jual Utama (USP): [USP]

                🎬 **SKRIP & PROMPT VIDEO AI (Total: 24 Detik)**
                *Karakter Avatar Utama:* [Deskripsikan wujud avatar secara singkat dalam Bahasa Inggris]

                ---
                **▶️ BAGIAN 1: THE HOOK (00:00 - 00:08)**
                **Prompt Visual AI (Salin ke Video Generator):**
                ```text
                [Prompt bahasa Inggris detail untuk adegan 1, sebutkan avatar dan produk asli dari gambar]
                ```
                **Voice Over (Salin ke Studio TTS di bawah):**
                ```text
                [Teks VO Hook]
                ```

                ---
                **▶️ BAGIAN 2: PENJELASAN (00:08 - 00:16)**
                **Prompt Visual AI (Salin ke Video Generator):**
                ```text
                [Prompt bahasa Inggris detail untuk adegan 2, sebutkan avatar dan produk asli dari gambar]
                ```
                **Voice Over (Salin ke Studio TTS di bawah):**
                ```text
                [Teks VO Penjelasan]
                ```

                ---
                **▶️ BAGIAN 3: CALL TO ACTION (00:16 - 00:24)**
                **Prompt Visual AI (Salin ke Video Generator):**
                ```text
                [Prompt bahasa Inggris detail untuk adegan 3, sebutkan avatar dan produk asli dari gambar]
                ```
                **Voice Over (Salin ke Studio TTS di bawah):**
                ```text
                [Teks VO Call to Action]
                ```

                📝 **CAPTION & SEO TIKTOK/IG REELS**
                - Caption: [Caption]
                - Hashtags: [5-7 hashtag]
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[system_prompt, image_for_api]
                )
                
                # Simpan hasil analisis dan skrip ke session state agar tidak hilang
                st.session_state.analysis_output = "✨ Analisis Produk Selesai!"
                st.session_state.script_full_output = response.text
                
                # Ekstrak deksripsi avatar untuk kunci wajah
                avatar_consistency_block = response.text.split('*Karakter Avatar Utama:*')[1].split('\n\n')[0].strip()
                st.session_state.avatar_consistency_prompt = f"{avatar_consistency_block}, looking directly at the camera, wearing professional casual attire, cinematic studio lighting, photorealistic, 16:9 aspect ratio."
                
                st.success("✨ Skrip & Prompt Video Berhasil Dibuat!")
                
            except Exception as e:
                st.error(f"Waduh, ada yang salah saat generate: {e}")
    else:
        st.error("⚠️ Harap unggah gambar produk terlebih dahulu Bosku!")

# ----------------------------------------------------
# MENAMPILKAN HASIL DARI MEMORI (ANTI HILANG)
# ----------------------------------------------------
if st.session_state.uploaded_image is not None:
    st.markdown("---")
    st.image(st.session_state.uploaded_image, caption="Produk yang dianalisis", use_container_width=True)

if st.session_state.script_full_output is not None:
    st.markdown(st.session_state.script_full_output)


# ----------------------------------------------------
# BAGIAN 2: STUDIO VOICE OVER (TEXT-TO-SPEECH)
# ----------------------------------------------------
if st.session_state.script_full_output is not None: # Tampilkan hanya jika skrip sudah ada
    st.markdown("---")
    st.header("🎙️ 2️⃣ Studio Voice Over")
    st.write("Salin teks *Voice Over* dari hasil di atas, lalu tempel di sini untuk mengubahnya menjadi MP3. (Catatan: Suara asisten Google Wanita standar)")

    tts_input = st.text_area("📝 Tempel Teks Skrip Di Sini:", height=100)

    if st.button("🎧 Generate Audio (MP3)"):
        if tts_input.strip() != "":
            with st.spinner("🎛️ Sedang memproses rekaman suara..."):
                try:
                    tts = gTTS(text=tts_input, lang='id', slow=False)
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    
                    st.success("✅ Audio berhasil dibuat!")
                    st.audio(audio_bytes, format='audio/mp3')
                    
                    st.download_button(
                        label="💾 Download Audio MP3",
                        data=audio_bytes,
                        file_name="voice_over_viralscript.mp3",
                        mime="audio/mp3"
                    )
                except Exception as e:
                    st.error(f"Gagal membuat audio: {e}")
        else:
            st.warning("⚠️ Kotak teksnya masih kosong, Bosku!")


# ----------------------------------------------------
# BAGIAN 3: PROMPT KUNCI WAJAH (TALKING HEAD)
# ----------------------------------------------------
if st.session_state.avatar_consistency_prompt is not None:
    st.markdown("---")
    st.header("📸 3️⃣ Prompt Kunci Wajah (Talking Head Workflow)")
    st.write("Gunakan strategi ini untuk mengunci wajah model agar 100% konsisten dari awal sampai akhir video.")

    st.markdown("##### Langkah 1: Generate Foto Wajah Statis (Eksternal)")
    st.write("Salin *prompt* bahasa Inggris di bawah ini dan tempelkan ke Bing Image Creator atau CapCut (fitur AI Image) untuk mendapatkan 1 foto model statis yang cantik.")
    
    # Menampilkan Prompt Kunci Wajah di kotak abu-abu bertombol copy
    st.code(st.session_state.avatar_consistency_prompt, language="text")

    st.markdown("##### Langkah 2: Lip Sync (Alur Profesional)")
    st.info("Buka CapCut atau HeyGen ➡️ Unggah Foto Statis hasil Langkah 1 ➡️ Masukkan file MP3 hasil Bagian 2 ➡️ AI akan otomatis melakukan Lip Sync (Talking Head). Wajah model dipastikan konsisten 100% sepanjang video!")

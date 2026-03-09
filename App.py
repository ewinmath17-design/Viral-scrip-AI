import streamlit as st
from google import genai
from PIL import Image
from gtts import gTTS
import io

# Konfigurasi Halaman Web
st.set_page_config(page_title="ViralScript AI Pro", page_icon="🎬", layout="centered")

st.title("🎬 ViralScript AI Pro Ultimate")
st.write("1️⃣ Bedah Skrip | 2️⃣ Studio Voice Over | 3️⃣ Studio Avatar (Anti Wajah Berubah)")

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
                2. Di setiap 'Prompt Visual AI' (dalam bahasa Inggris), Anda WAJIB mereferensikan detail visual spesifik yang Anda lihat di gambar.
                3. WAJIB pertahankan konsistensi karakter Avatar. Default avatar: "A beautiful 30-year-old Indonesian woman, warm and expressive."
                4. Voice Over harus hiper-lokal sesuai gaya bahasa.
                5. WAJIB ikuti struktur FORMAT OUTPUT di bawah ini. Letakkan Prompt dan Voice Over di dalam blok kode Markdown (menggunakan ```text dan ```).

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
st.write("Salin teks *Voice Over* dari hasil di atas, lalu tempel di sini untuk mengubahnya menjadi MP3.")

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
# BAGIAN 3: STUDIO AVATAR (KUNCI WAJAH)
# ----------------------------------------------------
st.markdown("---")
st.header("📸 3️⃣ Studio Avatar (Kunci Wajah)")
st.write("Gunakan fitur ini untuk membuat 1 foto referensi model. *Download* foto ini dan gunakan sebagai 'Image Prompt' di platform Video Generator Anda agar wajah model tetap konsisten di setiap adegan.")

avatar_prompt = st.text_area(
    "🎨 Teks Deskripsi Karakter (Bahasa Inggris):", 
    value="A beautiful 30-year-old Indonesian woman, warm and expressive, with long dark hair, wearing a stylish casual outfit, smiling warmly to the camera. Cinematic lighting, high quality.", 
    height=100
)

if st.button("🖼️ Generate Foto Karakter"):
    if avatar_prompt.strip() != "":
        with st.spinner("✨ Menggambar karakter avatar Anda..."):
            try:
                # Memanggil model pembuat gambar dari Google (Imagen 3)
                result = client.models.generate_images(
                    model='imagen-3.0-generate-001',
                    prompt=avatar_prompt,
                    config=dict(
                        number_of_images=1,
                        aspect_ratio="16:9",
                        output_mime_type="image/jpeg"
                    )
                )
                
                # Menampilkan dan menyiapkan tombol download gambar
                for generated_image in result.generated_images:
                    img_bytes = generated_image.image.image_bytes
                    avatar_image = Image.open(io.BytesIO(img_bytes))
                    
                    st.success("✅ Wujud Avatar Berhasil Diciptakan!")
                    st.image(avatar_image, caption="Simpan gambar ini untuk referensi Video AI Anda", use_container_width=True)
                    
                    st.download_button(
                        label="💾 Download Foto Avatar",
                        data=img_bytes,
                        file_name="avatar_viralscript.jpg",
                        mime="image/jpeg"
                    )
            except Exception as e:
                st.error(f"⚠️ Gagal generate gambar: {e}")
                st.info("💡 Terkadang API gratis membutuhkan waktu atau akses khusus. Alternatif: Copy deskripsi karakter di atas dan paste ke Bing Image Creator atau CapCut!")
    else:
        st.warning("⚠️ Deskripsi karakter tidak boleh kosong.")

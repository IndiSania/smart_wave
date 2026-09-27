import streamlit as st
from app.detector import WasteDetector
from app.ui import inject_css, render_header, render_sidebar, render_result_card
from app.utils import save_history, load_history, clear_history

st.set_page_config(
    page_title="SmartWaste AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

@st.cache_resource
def get_detector():
    return WasteDetector()

detector = get_detector()
render_header()

settings = render_sidebar()

tab1, tab2, tab3 = st.tabs(["🔍 Deteksi Sampah", "📊 Riwayat Analisis", "ℹ️ Tentang Sistem"])

with tab1:
    st.markdown("### Analisis objek sampah")
    st.caption("Unggah foto sampah untuk mendapatkan deteksi objek, kategori, dan rekomendasi pengelolaan.")

    source = st.radio(
        "Sumber gambar",
        ["Unggah gambar", "Kamera"],
        horizontal=True,
        label_visibility="collapsed",
    )

    image = None
    if source == "Unggah gambar":
        image = st.file_uploader(
            "Pilih gambar",
            type=["jpg", "jpeg", "png", "webp"],
            help="Gunakan foto dengan objek yang terlihat jelas.",
        )
    else:
        image = st.camera_input("Ambil foto")

    if image:
        col_a, col_b = st.columns([1, 1], gap="large")

        with col_a:
            st.image(image, caption="Gambar masukan", use_container_width=True)

        with col_b:
            with st.spinner("Menganalisis gambar..."):
                result = detector.predict(image, confidence=settings["confidence"])

            render_result_card(result)

            if result["detections"]:
                if st.button("💾 Simpan ke riwayat", use_container_width=True):
                    save_history(result)
                    st.success("Hasil berhasil disimpan.")
            else:
                st.warning(
                    "Belum ada objek yang dikenali. Coba gunakan gambar yang lebih terang "
                    "dan objek yang lebih terlihat."
                )

        if result["annotated_image"] is not None:
            st.markdown("### Hasil deteksi")
            st.image(
                result["annotated_image"],
                caption="Objek yang terdeteksi",
                use_container_width=True,
            )

with tab2:
    st.markdown("### Riwayat analisis")
    history = load_history()

    if not history:
        st.info("Belum ada riwayat analisis.")
    else:
        c1, c2 = st.columns(2)
        total = sum(item.get("count", 0) for item in history)
        c1.metric("Total analisis", len(history))
        c2.metric("Total objek terdeteksi", total)

        for item in reversed(history):
            with st.expander(
                f"{item['timestamp']} — {item.get('summary', 'Analisis sampah')}"
            ):
                st.write(f"Jumlah objek: **{item.get('count', 0)}**")
                for detection in item.get("detections", []):
                    st.write(
                        f"- {detection['label']} · {detection['category']} · "
                        f"{detection['confidence']:.0%}"
                    )

        if st.button("🗑️ Hapus seluruh riwayat"):
            clear_history()
            st.rerun()

with tab3:
    st.markdown("### Tentang SmartWaste AI")
    st.write(
        "SmartWaste AI adalah aplikasi computer vision untuk membantu mengenali objek "
        "yang berpotensi menjadi sampah dari sebuah gambar. Sistem menggunakan model "
        "YOLO melalui Ultralytics untuk deteksi objek, kemudian memetakan objek ke "
        "kategori pengelolaan sampah."
    )

    st.markdown("#### Teknologi")
    st.write("Python · Streamlit · OpenCV · Ultralytics YOLO · Pillow")

    st.markdown("#### Catatan")
    st.info(
        "Versi ini menggunakan model YOLO umum sebagai fondasi deteksi. Untuk deployment "
        "produksi dengan kategori sampah yang lebih spesifik, model dapat diganti dengan "
        "model yang dilatih menggunakan dataset sampah sendiri."
    )

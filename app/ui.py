import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: #f6f8f7;
        }
        [data-testid="stSidebar"] {
            background: #10231d;
        }
        [data-testid="stSidebar"] * {
            color: #f4f7f5 !important;
        }
        .hero {
            padding: 28px 30px;
            border-radius: 22px;
            background: linear-gradient(135deg, #10231d 0%, #1e4034 100%);
            color: white;
            margin-bottom: 24px;
        }
        .hero h1 {
            margin: 0;
            font-size: 42px;
            letter-spacing: -1px;
        }
        .hero p {
            margin: 8px 0 0;
            color: #cfe3d9;
            font-size: 16px;
        }
        .metric-card {
            padding: 18px;
            border: 1px solid #dfe7e2;
            border-radius: 16px;
            background: white;
            margin-bottom: 12px;
        }
        .metric-title {
            color: #64746c;
            font-size: 13px;
        }
        .metric-value {
            color: #10231d;
            font-size: 28px;
            font-weight: 700;
            margin-top: 4px;
        }
        .rec {
            padding: 14px 16px;
            border-left: 4px solid #22c55e;
            background: #effaf3;
            border-radius: 10px;
            margin: 8px 0;
        }
        .small-note {
            color: #64746c;
            font-size: 13px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="hero">
            <h1>♻️ SmartWaste AI</h1>
            <p>Computer vision untuk membantu mengenali dan memilah objek sampah.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.markdown("## SmartWaste AI")
    st.sidebar.caption("Waste Detection & Classification")

    confidence = st.sidebar.slider(
        "Ambang kepercayaan deteksi",
        min_value=0.10,
        max_value=0.90,
        value=0.35,
        step=0.05,
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Kategori")
    st.sidebar.write("🟢 Organik")
    st.sidebar.write("🔵 Anorganik")
    st.sidebar.write("🟤 Kertas")
    st.sidebar.write("🟣 Elektronik")
    st.sidebar.write("⚪ Lainnya")

    return {"confidence": confidence}


def render_result_card(result):
    detections = result["detections"]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-title">Objek terdeteksi</div>'
            f'<div class="metric-value">{result["count"]}</div></div>',
            unsafe_allow_html=True,
        )

    categories = len(set(d["category"] for d in detections))
    with c2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-title">Kategori</div>'
            f'<div class="metric-value">{categories}</div></div>',
            unsafe_allow_html=True,
        )

    for item in detections:
        st.markdown(
            f"""
            <div class="rec">
                <b>{item["label"].title()}</b> · {item["category"]} · {item["confidence"]:.0%}<br>
                <span class="small-note">{item["recommendation"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

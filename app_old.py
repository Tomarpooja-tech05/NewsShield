import streamlit as st
import joblib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@st.cache_resource
def load_model():
    return joblib.load(BASE_DIR / "news_model.pkl")

def get_metrics():
    with open(BASE_DIR / "metrics.json") as f:
        return json.load(f)


def get_test_metrics():
    metrics_path = BASE_DIR / "test_metrics.json"

    if metrics_path.exists():
        with open(metrics_path) as f:
            return json.load(f)

    return None

st.set_page_config(
    page_title="NewsShield | Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --blue: #5685ff;
    --purple: #9875ff;
    --ink: #edf2ff;
    --muted: #9aa9c7;
    --panel: #121d34;
}

.stApp {
    background:
        radial-gradient(ellipse at 75% 0%, #202d58 0%, transparent 38%),
        linear-gradient(145deg, #080f20, #0d172b 60%, #101a32);
    color: var(--ink);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header {visibility: visible;}
footer {visibility: visible;}

section[data-testid="stSidebar"] {
    background: #0b1325;
    border-right: 1px solid #26334f;
}

section[data-testid="stSidebar"] * {
    color: #dbe6ff;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
    padding: 10px 0 2px;
}

.brand span {
    color: #75a0ff;
}

.tagline {
    font-size: 11px;
    color: #8394b7;
    letter-spacing: 2px;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 38px;
    border: 1px solid #384c79;
    border-radius: 24px;
    background: linear-gradient(
        115deg, rgba(37, 65, 125, .95),
        rgba(71, 51, 132, .72), rgba(20, 34, 64, .95)
    );
    box-shadow: 0 18px 55px #00000035;
    animation: appear .8s ease both;
}

.hero:after {
    content: "✦";
    position: absolute;
    right: 9%;
    top: 8%;
    font-size: 145px;
    color: #ffffff0d;
    animation: float 5s ease-in-out infinite;
}

.eyebrow {
    display: inline-block;
    color: #bcd1ff;
    background: #ffffff12;
    border: 1px solid #ffffff20;
    padding: 7px 12px;
    border-radius: 30px;
    font-size: 12px;
    letter-spacing: 1px;
}

.hero h1 {
    color: white;
    font-size: clamp(34px, 4vw, 52px);
    line-height: 1.12;
    letter-spacing: -2px;
    margin: 20px 0 12px;
    font-weight: 800;
}

.gradient-text {
    background: linear-gradient(90deg, #8ec5ff, #c0a6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 670px;
    color: #d2dcf5;
    line-height: 1.8;
    font-size: 15px;
}

.section-title {
    font-size: 23px;
    font-weight: 750;
    letter-spacing: -.5px;
    margin-bottom: 4px;
}

.muted {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.7;
}

.panel {
    background: linear-gradient(145deg, #16233d, #111c31);
    border: 1px solid #293a5a;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 12px 35px #00000020;
    animation: appear .7s ease both;
}

.feature {
    background: #121e33;
    border: 1px solid #263752;
    border-radius: 17px;
    padding: 20px;
    min-height: 160px;
    transition: transform .25s ease, border-color .25s ease;
    animation: appear .8s ease both;
}

.feature:hover {
    transform: translateY(-5px);
    border-color: #688fff;
}

.feature-icon {
    font-size: 25px;
    margin-bottom: 13px;
}

.feature h4 {
    color: #f0f4ff;
    font-size: 15px;
    margin: 0 0 8px;
}

.feature p {
    color: #9eacc7;
    font-size: 12px;
    line-height: 1.7;
}

div[data-baseweb="textarea"] textarea {
    background: #0b1529;
    color: #f0f4ff;
    border: 1px solid #354b70;
    border-radius: 13px;
    line-height: 1.7;
}

div[data-baseweb="textarea"] textarea:focus {
    border-color: #7598ff;
    box-shadow: 0 0 0 2px #628aff20;
}

.stButton > button {
    background: linear-gradient(100deg, #477eff, #8562f5);
    color: white;
    border: 1px solid #809eff55;
    border-radius: 11px;
    min-height: 46px;
    font-weight: 650;
    transition: all .25s ease;
}

.stButton > button:hover {
    color: white;
    border-color: #b3c6ff;
    box-shadow: 0 0 24px #658bff45;
    transform: translateY(-2px);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #293751;
}

@keyframes appear {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-12px) rotate(8deg); }
}

@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        '<div class="brand">🛡️ News<span>Shield</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="tagline">THINK. VERIFY. SHARE.</div>',
        unsafe_allow_html=True
    )
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "How It Works", "About Project"]
    )

    st.divider()
    st.markdown("### PROJECT STATUS")
    st.caption("Machine Learning System")
    st.progress(0.65)
    st.caption("Model Integration")
    st.markdown("---")
    st.caption("BCA MINOR PROJECT")
    st.caption("Fake News Detection System")
def set_news_example(text):
    st.session_state.news_input = text
if "news_input" not in st.session_state:
    st.session_state.news_input = ""

if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <span class="eyebrow">✦ INTELLIGENT NEWS ANALYSIS</span>
        <h1>Don't Just Read News.<br>
        <span class="gradient-text">Question It.</span></h1>
        <p>
        In a world of endless information, one misleading headline can
        spread everywhere. NewsShield is designed to help users examine
        news text and make more informed decisions before sharing it.
        </p>
    </div>
    """, unsafe_allow_html=True)
    # MODEL PERFORMANCE SECTION
    test_metrics = get_test_metrics()

    st.write("")
    st.markdown("## 📊 Model Performance")
    st.markdown(
        '<div class="muted">Performance evaluated on the test dataset.</div>',
        unsafe_allow_html=True
    )
    st.write("")

    if test_metrics:
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                "Accuracy",
                f"{test_metrics['accuracy']:.2f}%"
            )

        with m2:
            st.metric(
                "Precision",
                f"{test_metrics['precision']:.2f}%"
            )

        with m3:
            st.metric(
                "Recall",
                f"{test_metrics['recall']:.2f}%"
            )

        with m4:
            st.metric(
                "F1 Score",
                f"{test_metrics['f1_score']:.2f}%"
            )

        st.write("")

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                "Articles Tested",
                f"{test_metrics['total_tested']:,}"
            )

        with p2:
            st.metric(
                "Correct Predictions",
                f"{test_metrics['correct_predictions']:,}"
            )

        with p3:
            st.metric(
                "Wrong Predictions",
                f"{test_metrics['wrong_predictions']:,}"
            )

    else:
        st.info(
            "Testing report not found. Run test_model.py first."
        )
    st.markdown("---")

    if test_metrics and "confusion_matrix" in test_metrics:

        st.write("")
        st.markdown("### 🔍 Confusion Matrix")
        st.caption("Actual vs predicted news classification")

        cm = test_metrics["confusion_matrix"]

        import pandas as pd
        import plotly.graph_objects as go

        cm_df = pd.DataFrame(
            cm,
            index=["Actual Fake", "Actual Real"],
            columns=["Predicted Fake", "Predicted Real"]
        )

        st.dataframe(
            cm_df,
            use_container_width=True
        )

        # Confusion Matrix Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=["Predicted Fake", "Predicted Real"],
            y=["Actual Fake", "Actual Real"],
            colorscale="Blues",
            text=cm,
            texttemplate="%{text}",
            showscale=True
        ))

        fig.update_layout(
            title="Confusion Matrix Heatmap",
            xaxis_title="Predicted Label",
            yaxis_title="Actual Label",
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)  
    st.write("")
    st.markdown(
        '<div class="section-title">Article Analysis</div>'
        '<div class="muted">Submit news text to prepare it for verification.</div>',
        unsafe_allow_html=True
    )
    st.write("")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### ✍️ Enter the news article")
    st.caption("For best results, use the complete article rather than just a headline.")

    news = st.text_area(
        "News article",
        key="news_input",
        height=190,
        max_chars=5000,
        placeholder="Paste the news article here...\n\nInclude the headline and relevant details when available.",
        label_visibility="collapsed"
    )

    left, right = st.columns([3, 1])

    with left:
        st.caption(f"{len(news)} / 5000 characters")

    with right:
        st.caption("🔒 Demo interface")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("**QUICK EXAMPLES**")

    e1, e2, e3 = st.columns(3)

    with e1:
        st.button(
            "🔬 Science & Research",
            use_container_width=True,
            on_click=set_news_example,
            args=("Researchers at a university have published a new study on renewable energy. The study explains the research methodology, experimental results and limitations. The findings are being reviewed by independent experts.",)
        )

    with e2:
        st.button(
            "📢 Viral Social Media Claim",
            use_container_width=True,
            on_click=set_news_example,
            args=("A viral social media post claims that drinking a special herbal mixture can cure every disease within seven days. The post does not provide scientific evidence or references to verified medical research.",)
        )

    with e3:
        st.button(
            "🏛️ Public Notice",
            use_container_width=True,
            on_click=set_news_example,
            args=("The Municipal Administration has announced a public cleanliness awareness campaign. Residents are encouraged to participate in neighbourhood cleaning activities and waste management programmes.",)
        )

    st.write("")

    if st.button("✦  Analyse News", use_container_width=True):

        if not news.strip():
            st.warning("Please enter a news article.")

        elif len(news.strip()) < 30:
            st.warning("Please enter a longer news article.")

        else:
            try:
                model = load_model()

                prediction = model.predict([news])[0]
                probabilities = model.predict_proba([news])[0]
                confidence = max(probabilities) * 100

                st.markdown("---")
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 🔍 Analysis Results")

                if prediction == 0:
                    st.error("🚨 FAKE NEWS PREDICTED")
                else:
                    st.success("✅ REAL NEWS PREDICTED")

                st.metric("Model Confidence", f"{confidence:.2f}%")

                metrics = get_metrics()

                st.metric(
                    "Test Dataset Accuracy",
                    f"{metrics['accuracy']}%"
                )

                st.caption(
                    "Prediction is based on dataset patterns "
                    "and does not independently verify the news."
                )

                st.markdown("</div>", unsafe_allow_html=True)

            except FileNotFoundError:
                st.error("Model files not found. Train the model first.")

            except Exception as e:
                st.error(f"Analysis error: {e}")

    st.write("")
    st.markdown("### Built for a more informed digital world")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="feature">
            <div class="feature-icon">🧠</div>
            <h4>Machine Learning</h4>
            <p>Designed for integration with text preprocessing and a trained classifier.</p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature">
            <div class="feature-icon">🔎</div>
            <h4>Critical Evaluation</h4>
            <p>Encourages readers to examine sources, evidence and context.</p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature">
            <div class="feature-icon">🌐</div>
            <h4>Responsible Sharing</h4>
            <p>Promotes thoughtful decisions before forwarding online information.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "How It Works":
    st.markdown("""
    <div class="hero">
        <span class="eyebrow">THE WORKFLOW</span>
        <h1>How <span class="gradient-text">NewsShield</span> Works</h1>
        <p>A workflow for analysing submitted news text using the trained machine-learning model.</p>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "Input News", "The user enters a news article or headline."),
        ("02", "Preprocess Text", "Text cleaning and preparation help standardise the input."),
        ("03", "Model Prediction", "A trained machine-learning model analyses the processed text."),
        ("04", "Present Results", "The application displays the model's predicted category.")
    ]

    for number, title, description in steps:
        st.markdown(f"""
        <div class="feature">
        <div class="feature-icon">{number}</div>
        <h4>{title}</h4>
        <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

    st.info(
        "The workflow above describes the intended system. "
        "Preprocessing, prediction and result generation still need "
        "to be implemented and connected."
    )

elif page == "About Project":
    st.markdown("""
    <div class="hero">
        <span class="eyebrow">ABOUT THE PROJECT</span>
        <h1>Building Awareness.<br>
        <span class="gradient-text">One Article at a Time.</span></h1>
        <p>NewsShield is a BCA minor project concept focused on fake news detection.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Project Overview")
    st.write(
        "The rapid circulation of online information makes it difficult "
        "to evaluate every claim. NewsShield aims to provide a simple "
        "interface for submitting news text to a machine-learning system."
    )

    st.markdown("### Objectives")
    st.markdown("""
    - Develop an accessible news-analysis interface.
    - Prepare news text for automated processing.
    - Integrate a trained model to classify article text.
    - Present predictions clearly while recognising model limitations.
    - Encourage users to verify information with reliable sources.
    """)

    st.markdown("### Technology Stack")
    t1, t2, t3 = st.columns(3)

    with t1:
        st.markdown("""
        <div class="feature">
        <h4>Frontend</h4>
        <p>Python + Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div class="feature">
        <h4>Text Processing</h4>
        <p>News text preparation for model input</p>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div class="feature">
        <h4>Classification</h4>
        <p>Planned trained ML model</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.warning(
        "Important: this prototype is not yet a working fake-news detector. "
        "Predictions require a trained and tested model."
    )

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#8999b8;font-size:12px;">'
    'NEWSHIELD · BCA MINOR PROJECT · THINK BEFORE YOU SHARE'
    '</div>',
    unsafe_allow_html=True
)

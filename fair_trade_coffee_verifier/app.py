import streamlit as st

from src.agent import FairTradeCoffeeAgent
from src.product_lookup import ProductLookupError
from src.registry import RegistryError
from src.verifier import VERIFIED


st.set_page_config(
    page_title="Fair Trade Coffee Verifier",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
    .stApp {
        background: #f7f4ed;
        color: #211d18;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {
        background: #211d18;
        color: #f7f4ed;
    }
    [data-testid="stToolbar"],
    [data-testid="stToolbar"] button,
    [data-testid="stToolbar"] svg,
    [data-testid="stDecoration"],
    [data-testid="stDeployButton"],
    [data-testid="stDeployButton"] button,
    [data-testid="stMainMenu"] button,
    [data-testid="stMainMenu"] svg {
        color: #f7f4ed;
        fill: #f7f4ed;
        stroke: #f7f4ed;
    }
    [data-testid="stDeployButton"] button {
        border: 1px solid rgba(247, 244, 237, 0.35);
        background: rgba(247, 244, 237, 0.1);
        border-radius: 6px;
    }
    [data-testid="stSidebar"] {
        background: #211d18;
    }
    [data-testid="stSidebar"] * {
        color: #f7f4ed;
    }
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        background: #fffdf8 !important;
        color: #211d18 !important;
        -webkit-text-fill-color: #211d18 !important;
    }
    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {
        color: #6f665b !important;
        -webkit-text-fill-color: #6f665b !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #fffdf8 !important;
        border-color: rgba(247, 244, 237, 0.45) !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] *,
    [data-testid="stSidebar"] [data-baseweb="popover"] * {
        color: #211d18 !important;
        -webkit-text-fill-color: #211d18 !important;
    }
    .hero {
        padding: 1.4rem 0 0.6rem;
        border-bottom: 1px solid rgba(33, 29, 24, 0.16);
        margin-bottom: 1.4rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.3rem;
        letter-spacing: 0;
        color: #211d18;
    }
    .hero p {
        margin: 0.4rem 0 0;
        color: #5f564b;
        max-width: 760px;
    }
    .verdict-banner {
        border-radius: 8px;
        padding: 1rem 1.1rem;
        margin: 0 0 1.1rem;
        box-shadow: none;
    }
    .status-verified {
        border: 0;
        border-left: 7px solid #1f7a4d;
        background: linear-gradient(90deg, #e4f4ea 0%, #f8fbf7 100%);
    }
    .status-warning {
        border: 0;
        border-left: 7px solid #b45f06;
        background: linear-gradient(90deg, #fff0d8 0%, #fffaf1 100%);
    }
    .status-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .muted {
        color: #6f665b;
        font-size: 0.92rem;
    }
    .metric-label {
        color: #6f665b;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0;
        margin-bottom: 0.2rem;
    }
    .metric-value {
        font-size: 1.05rem;
        font-weight: 700;
        color: #211d18;
        overflow-wrap: anywhere;
    }
    .score {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1;
    }
</style>
"""


@st.cache_resource(show_spinner=False)
def get_agent() -> FairTradeCoffeeAgent:
    return FairTradeCoffeeAgent()


def render_field(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result(barcode: str) -> None:
    try:
        result = get_agent().verify_barcode(barcode)
    except (ProductLookupError, RegistryError) as exc:
        st.error(str(exc))
        return
    except Exception as exc:
        st.error("The verifier hit an unexpected error. Check logs/app.log for details.")
        get_agent().logger.exception("Unexpected verification failure: %s", exc)
        return

    product = result.product
    farm = result.matched_farm
    verified = result.status == VERIFIED
    status_class = "status-verified" if verified else "status-warning"

    st.markdown(
        f"""
        <div class="verdict-banner {status_class}">
            <div class="status-title">{result.status}</div>
            <div class="muted">{result.certification_information}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_col, explain_col = st.columns([1, 2.2], gap="large")
    with score_col:
        st.markdown('<div class="metric-label">Trust Score</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score">{result.trust_score}/100</div>', unsafe_allow_html=True)
        st.progress(result.trust_score / 100)

    with explain_col:
        st.subheader("AI-generated explanation")
        st.write(result.explanation)

    product_col, farm_col = st.columns(2, gap="large")
    with product_col:
        st.subheader("Product details")
        render_field("Barcode", product.barcode)
        render_field("Product", product.product_name)
        render_field("Brand", product.brand)
        render_field("Labels", product.labels)
        render_field("Manufacturing place", product.manufacturing_places)
        render_field("Origin farm", product.origin_farm_name)

    with farm_col:
        st.subheader("Farm details")
        if farm:
            render_field("Registry ID", farm.registry_id)
            render_field("Farm name", farm.farm_name)
            render_field("Country", farm.country)
            render_field("Certification year", farm.certification_year)
            render_field("Status", farm.status)
        else:
            render_field("Farm name", product.origin_farm_name)
            render_field("Registry match", "Not found")
            render_field("Certification status", "Unverified")
            render_field("Certification year", "Unavailable")
            render_field("Country", "Unavailable")


def main() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero">
            <h1>Fair Trade Coffee Verifier</h1>
            <p>Offline AI agent for checking whether a coffee product's claimed origin farm exists in the certified Fair Trade registry.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        agent = get_agent()
        sample_barcodes = agent.sample_barcodes()
    except (ProductLookupError, RegistryError) as exc:
        st.error(str(exc))
        return

    with st.sidebar:
        st.header("Scan input")
        selected_sample = st.selectbox(
            "Demo barcode",
            sample_barcodes,
            index=0,
            help="Mock barcode payloads bundled with the project.",
        )
        barcode = st.text_input(
            "Barcode",
            value=selected_sample,
            placeholder="Enter or paste a barcode",
        )
        verify_clicked = st.button("Verify coffee", type="primary", use_container_width=True)

        st.divider()
        st.caption("Works offline using local JSON and CSV data.")

    if verify_clicked or barcode:
        render_result(barcode)
    else:
        st.info("Enter a barcode to begin verification.")


if __name__ == "__main__":
    main()

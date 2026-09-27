import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import textwrap
import base64

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Apple Retail Sales",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HTML RENDERING HELPER
# ============================================================
# This prevents Streamlit's Markdown parser from treating
# indented HTML as a code block.

def render_html(html):
    html = textwrap.dedent(html).strip()

    # Remove blank lines so Streamlit's Markdown parser
    # does not convert following HTML into a code block.
    html = "\n".join(
        line for line in html.splitlines()
        if line.strip()
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

# ============================================================
# COLORS — iOS system palette
# ============================================================

GREEN = "#11875F"        # primary accent — brand green, back from iOS blue
GREEN_LIGHT = "#34D399"  # lighter mint-green
GREEN_HOVER = "#0D9C6D"

TEAL = "#64D2FF"
PURPLE = "#BF5AF2"
ORANGE = "#FF9F0A"
RED = "#FF453A"
POSITIVE = "#30D158"

BACKGROUND = "#F2F2F7"   # iOS system grouped background
WHITE = "#ffffff"

TEXT_COLOR = "#1C1C1E"   # iOS label
TEXT_MUTED = "#8E8E93"   # iOS secondary label
TEXT_LIGHT = "#C7C7CC"   # iOS tertiary label

BORDER = "rgba(60,60,67,0.13)"
FILTER_BG = "#F2F2F7"
FILTER_TEXT = "#1C1C1E"


# Countries whose name in the dataset doesn't match Plotly's
# built-in "country names" location list, for the Sales Map.
COUNTRY_NAME_FIXES = {
    "Uae": "United Arab Emirates",
}


# ============================================================
# CHART STYLING
# ============================================================

def style_chart(fig, height=None):

    fig.update_layout(
        template="plotly_white",
        font=dict(
            color=TEXT_COLOR,
            size=12,
            family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif"
        ),
        title_font=dict(
            color=TEXT_COLOR,
            size=14
        ),
        legend=dict(
            font=dict(
                color=TEXT_COLOR
            )
        )
    )

    fig.update_xaxes(
        title_font=dict(
            color=TEXT_COLOR
        ),
        tickfont=dict(
            color=TEXT_MUTED
        ),
        gridcolor="rgba(60,60,67,0.06)"
    )

    fig.update_yaxes(
        title_font=dict(
            color=TEXT_COLOR
        ),
        tickfont=dict(
            color=TEXT_MUTED
        ),
        gridcolor="rgba(60,60,67,0.06)"
    )

    if height:
        fig.update_layout(height=height)

    return fig


def hex_to_rgba(hex_color, alpha=0.18):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ============================================================
# CUSTOM CSS — iOS look & feel
# ============================================================

render_html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, span, div {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont,
                 "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

.stApp * {
    border-radius: 0 !important;
}

[data-testid="stIconMaterial"],
span[class*="material-symbols"],
span[class*="material-icons"] {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] button {
    background: transparent !important;
    box-shadow: none !important;
}

[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapseButton"] span,
[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] span {
    color: #ffffff !important;
    fill: #ffffff !important;
}

.dashboard-topbar {
    background: #E4E8F0;
    border-radius: 0 !important;
    padding: 14px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.topbar-user {
    display: flex;
    align-items: center;
    gap: 10px;
}

.topbar-user .greeting {
    font-size: 13px;
    color: #5C6270;
    font-weight: 500;
}

.topbar-user .avatar {
    width: 34px;
    height: 34px;
    border-radius: 0 !important;
    background: #11875F;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
}

.stApp {
    background-color: #F2F2F7;
}

.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1600px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ---- Sidebar shell ---- */
section[data-testid="stSidebar"] {
    background-color: #11875F !important;
    border-right: none !important;
    padding-top: 0 !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
    padding-left: 0.9rem !important;
    padding-right: 0.9rem !important;
}

/* ---- Streamlit collapse arrow row ---- */
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
    display: flex !important;
    justify-content: flex-end !important;
    align-items: flex-end !important;
    padding: 0 8px 0 0 !important;
    margin: 0 !important;
    height: 45px !important;
    min-height: 40px !important;
    background: transparent !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button:hover {
    background: rgba(255,255,255,0.08) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* ---- Sidebar content top padding reset ---- */
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

section[data-testid="stSidebar"] > div:first-child > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

section[data-testid="stSidebar"] .stElementContainer:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* ---- Sidebar text ---- */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #E7E9F2 !important;
}

.sidebar-header {
    background: transparent;
    margin: -36px -0.9rem 14px -0.9rem;
    padding: 0px 22px 4px 22px !important;
    pointer-events: none !important;
}

.sidebar-header .apple-logo,
.sidebar-header h1,
.sidebar-header p {
    pointer-events: auto !important;
}

.sidebar-header .apple-logo {
    width: 85px;
    height: auto;
    display: block;
    margin: 0;
}

.sidebar-header h1 {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.6px;
    margin: 2px 0 0 0;
    line-height: 0.9;
    color: #ffffff !important;
}

.sidebar-header p {
    font-size: 10px;
    letter-spacing: 1px;
    margin: 6px 0 0 0;
    color: rgba(255,255,255,0.65) !important;
    text-transform: uppercase;
}

.nav-title {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 22px;
    margin-right: 0;
    margin-bottom: 10px;
    margin-left: 6px;
    color: rgba(255,255,255,0.55) !important;
    text-align: left !important;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] .stVerticalBlock {
    gap: 0 !important;
}

section[data-testid="stSidebar"] .stElementContainer {
    margin: 0 !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] .stButton {
    width: 100% !important;
    margin: 2px 0 !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    height: 40px !important;
    min-height: 40px !important;
    margin: 0 !important;
    padding: 0 6px !important;
    border: none !important;
    border-radius: 0 !important;
    background-color: transparent !important;
    color: #E7E9F2 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    transition: background-color 0.15s ease, color 0.15s ease;
}

section[data-testid="stSidebar"] .stButton > button > div {
    width: 100% !important;
    justify-content: flex-start !important;
    text-align: left !important;
}

section[data-testid="stSidebar"] .stButton > button p {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    text-align: left !important;
    color: inherit !important;
    font-size: 14px !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #E7E9F2 !important;
    border: none !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background-color: rgba(255,255,255,0.06) !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background-color: transparent !important;
    color: #6EE7B7 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
section[data-testid="stSidebar"] .stButton > button[kind="primary"] span {
    color: #6EE7B7 !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background-color: rgba(255,255,255,0.06) !important;
    color: #6EE7B7 !important;
}

section[data-testid="stSidebar"] hr {
    border: 0 !important;
    border-top: 1px solid rgba(255,255,255,0.15) !important;
    margin: 14px 6px !important;
}

section[data-testid="stSidebar"] .stSelectbox {
    margin: 0 !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] .stSelectbox label {
    color: #E7E9F2 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-left: 4px !important;
}

section[data-testid="stSidebar"] .stSelectbox:first-of-type {
    margin-top: 10px !important;
}
section[data-testid="stSidebar"] .stSelectbox label p {
    color: #E7E9F2 !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: none !important;
    border-radius: 0 !important;
    min-height: 40px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] div {
    color: #1C1C1E !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color: #1C1C1E !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #8E8E93 !important;
    color: #8E8E93 !important;
}

div[data-baseweb="popover"] {
    background-color: white !important;
}

div[data-baseweb="popover"] * {
    color: #1C1C1E !important;
}

div[data-baseweb="menu"] {
    background-color: white !important;
}

div[data-baseweb="menu"] li {
    color: #1C1C1E !important;
}

div[data-baseweb="menu"] li:hover {
    background-color: #F2F2F7 !important;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] .stCaption p {
    color: rgba(255,255,255,0.5) !important;
    font-size: 11px !important;
}

.dashboard-title {
    font-size: 30px;
    font-weight: 700;
    letter-spacing: -0.3px;
    color: #1C1C1E;
    margin-bottom: 0;
}

.dashboard-subtitle {
    color: #8E8E93;
    font-size: 14px;
    margin-top: 4px;
    margin-bottom: 20px;
}

div[data-testid="stSelectbox"] label p {
    color: #1C1C1E !important;
}

div[data-baseweb="select"] * {
    color: #1C1C1E !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 0 !important;
    overflow: hidden;
    border: 1px solid rgba(60,60,67,0.10) !important;
}

div[data-testid="stDataFrame"] * {
    color: #1C1C1E !important;
}

.kpi-card {
    background: #ffffff;
    border-radius: 0 !important;
    padding: 16px 15px;
    border: 1px solid rgba(60,60,67,0.08);
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    min-height: 145px;
}

.kpi-title {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #7A8190 !important;
    margin-bottom: 10px !important;
}

.kpi-value {
    font-size: 22px !important;
    font-weight: 650 !important;
    color: #111111 !important;
    line-height: 1.15 !important;
    margin-bottom: 10px !important;
}

.kpi-description {
    font-size: 12px;
    font-weight: 450;
    color: #8E8E93;
    margin-top: 6px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    letter-spacing: -0.2px;
    color: #1C1C1E;
    margin-top: 5px;
    margin-bottom: 18px;
}

.subsection-title {
    font-size: 16px;
    font-weight: 600;
    color: #1C1C1E;
    margin-top: 10px;
    margin-bottom: 8px;
}

div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border-radius: 0 !important;
    padding: 4px;
    border: 1px solid rgba(60,60,67,0.08);
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

.highlight-card {
    background: linear-gradient(135deg, #11875F 0%, #0D9C6D 55%, #34D399 100%);
    color: white;
    border-radius: 0 !important;
    padding: 16px 15px;
    min-height: 145px;
    box-sizing: border-box;
    box-shadow: 0 8px 20px rgba(94,92,230,0.25);
}

.highlight-title {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: white !important;
    opacity: 0.85;
    margin: 0 0 8px 0 !important;
}

.highlight-value {
    font-family: inherit !important;
    font-size: 26px !important;
    font-weight: 600 !important;
    line-height: 1.25 !important;
    letter-spacing: -0.3px;
    margin: 0 !important;
    padding: 0 !important;
    color: white !important;
}

.highlight-description {
    font-family: inherit !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    line-height: 1.4 !important;
    color: white !important;
    opacity: 0.8;
    margin: 8px 0 0 0 !important;
}

.stButton > button {
    border-radius: 0 !important;
    border: 1px solid #11875F;
    color: #11875F;
    background-color: white;
}

.stButton > button:hover {
    background-color: #11875F;
    color: white;
}

.stAlert {
    border-radius: 0 !important;
}

.dashboard-footer {
    text-align: center;
    color: #C7C7CC;
    font-size: 12px;
    padding: 20px;
}

</style>
""")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv(
        "data/apple_sales_cleaned.csv.gz"
    )

    data["sale_date"] = pd.to_datetime(
        data["sale_date"]
    )

    data["launch_date"] = pd.to_datetime(
        data["launch_date"]
    )

    return data


df = load_data()


# ============================================================
# CHECK LAST MONTH
# ============================================================

last_sale_date = df["sale_date"].max()

LAST_MONTH_IS_PARTIAL = (
    last_sale_date.day < last_sale_date.days_in_month
)


# ============================================================
# SIDEBAR NAVIGATION + FILTERS
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Overview"

apple_logo_base64 = get_image_base64("apple_logo.png")

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    render_html(f"""
<div class="sidebar-header">
    <img src="data:image/png;base64,{apple_logo_base64}" class="apple-logo">
    <h1>APPLE RETAIL SALES</h1>
    <p>Business Intelligence</p>
</div>
""")


    st.markdown("---")


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    render_html("""
    <div class="nav-title">NAVIGATION</div>
    """)


    nav_items = [
        ("Overview", "⌂  Overview"),
        ("Products", "▣  Products"),
        ("Stores & Countries", "♧  Stores & Countries"),
        ("Forecast", "⌁  Forecast"),
    ]


    for page_name, label in nav_items:

        if st.button(
            label,
            key=f"nav_{page_name}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == page_name
                else "secondary"
            )
        ):

            st.session_state.page = page_name

            st.rerun()


    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    render_html("""
    <div class="nav-title">FILTERS</div>
    """)


    selected_year = st.selectbox(
        "Year",
        ["All"] + sorted(
            df["year"]
            .dropna()
            .unique()
            .tolist()
        ),
        key="filter_year"
    )


    selected_country = st.selectbox(
        "Country",
        ["All"] + sorted(
            df["country"]
            .dropna()
            .unique()
            .tolist()
        ),
        key="filter_country"
    )


    selected_category = st.selectbox(
        "Category",
        ["All"] + sorted(
            df["category_name"].dropna().unique().tolist()
        ),
        key="filter_category"
    )

    # Detect category change and reset product
    if "last_category" not in st.session_state:
        st.session_state.last_category = selected_category

    if st.session_state.last_category != selected_category:
        st.session_state.filter_product = "All"
        st.session_state.last_category = selected_category

    # Build product list based on selected category
    if selected_category == "All":
        product_options = df["product_name"].dropna().unique().tolist()
    else:
        product_options = (
            df[df["category_name"] == selected_category]["product_name"]
            .dropna()
            .unique()
            .tolist()
        )

    selected_product = st.selectbox(
        "Product",
        ["All"] + sorted(product_options),
        key="filter_product"
    )


    st.markdown("---")


    st.caption(
        "Apple Retail Sales BI Dashboard"
    )


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.page


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = df.copy()


if selected_year != "All":

    filtered = filtered[
        filtered["year"] == selected_year
    ]


if selected_country != "All":

    filtered = filtered[
        filtered["country"] == selected_country
    ]


if selected_category != "All":

    filtered = filtered[
        filtered["category_name"] == selected_category
    ]


if selected_product != "All":

    filtered = filtered[
        filtered["product_name"] == selected_product
    ]


# ============================================================
# EMPTY FILTER CHECK
# ============================================================

if filtered.empty:

    render_html("""
    <div style="
        background:white;
        border:1px solid rgba(60,60,67,0.08);
        border-radius: 0 !important;
        padding:40px;
        text-align:center;
        color:#8E8E93;
        margin-top:30px;
    ">
        No data available for the selected filters.
    </div>
    """)

    st.stop()


# ============================================================
# GLOBAL MONTHLY AGGREGATE
# ============================================================

_monthly_base = (
    filtered
    .groupby(["year", "month"], as_index=False)
    .agg(
        total_sales=("total_sales", "sum"),
        quantity=("quantity", "sum"),
        avg_price=("price", "mean")
    )
)

_monthly_base["period"] = pd.to_datetime(
    _monthly_base["year"].astype(str)
    + "-"
    + _monthly_base["month"].astype(str)
    + "-01"
)

_monthly_base = (
    _monthly_base
    .sort_values("period")
    .reset_index(drop=True)
)

_monthly_complete = _monthly_base.copy()

if LAST_MONTH_IS_PARTIAL and len(_monthly_complete) > 1:
    _monthly_complete = _monthly_complete.iloc[:-1]

# Last 12 (complete) months, used for the small KPI sparklines
_monthly_recent = _monthly_complete.tail(12)

LAST_COMPLETE_PERIOD = (
    _monthly_complete["period"].max()
    if len(_monthly_complete) > 0
    else None
)


# ============================================================
# HEADER
# ============================================================

render_html("""

<div class="dashboard-title">
    Apple Retail Sales
</div>

<div class="dashboard-subtitle">
    • Retail Sales Performance
</div>
""")


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered["total_sales"].sum()

total_quantity = filtered["quantity"].sum()

order_count = len(filtered)

average_order_value = (
    total_sales / order_count
    if order_count > 0
    else 0
)


if len(filtered) > 0:

    top_product = (
        filtered
        .groupby("product_name")["total_sales"]
        .sum()
        .idxmax()
    )

    top_country = (
        filtered
        .groupby("country")["total_sales"]
        .sum()
        .idxmax()
    )

else:

    top_product = "N/A"

    top_country = "N/A"


# ============================================================
# KPI SECTION
# ============================================================

render_html("""
<div class="section-title">
    Key Sales Figures
</div>
""")


k1, k2, k3, k4, k5 = st.columns(5)

with k1:

    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            Total Sales
        </div>
        <div class="kpi-value">
            ₱{total_sales:,.0f}
        </div>
        <div class="kpi-description">
            Total revenue generated
        </div>
    </div>
    """)

with k2:

    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            Quantity Sold
        </div>
        <div class="kpi-value">
            {total_quantity:,.0f}
        </div>
        <div class="kpi-description">
            Total units sold
        </div>
    </div>
    """)


with k3:

    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            Order Count
        </div>
        <div class="kpi-value">
            {order_count:,.0f}
        </div>
        <div class="kpi-description">
            Total transactions
        </div>
    </div>
    """)


with k4:

    render_html(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            Average Order Value
        </div>
        <div class="kpi-value">
            ₱{average_order_value:,.0f}
        </div>
        <div class="kpi-description">
            Average revenue per transaction
        </div>
    </div>
    """)

with k5:

    render_html(f"""
    <div class="highlight-card">
        <div class="highlight-title">
            Top Product
        </div>
        <div class="highlight-value">
            {top_product}
        </div>
        <div class="highlight-description">
            Highest revenue in current selection
        </div>
    </div>
    """)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    render_html("""
    <div class="section-title">
        Sales Overview
    </div>
    """)


    col1, col2 = st.columns([1.6, 1])

    # --------------------------------------------------------
    # MONTHLY SALES
    # --------------------------------------------------------

    with col1:

        monthly = (
            filtered
            .groupby(
                ["year", "month"],
                as_index=False
            )["total_sales"]
            .sum()
        )

        monthly["period"] = pd.to_datetime(
            monthly["year"].astype(str)
            + "-"
            + monthly["month"].astype(str)
            + "-01"
        )

        monthly = (
            monthly
            .sort_values("period")
            .reset_index(drop=True)
        )

        fig = px.area(
            monthly,
            x="period",
            y="total_sales",
            markers=True
        )

        fig.update_traces(
            line=dict(
                color=GREEN,
                width=3,
                shape="spline"
            ),
            marker=dict(
                size=5,
                color=GREEN
            ),
            fillcolor=hex_to_rgba(GREEN, 0.12)
        )

        fig.update_layout(
            title="Monthly Sales Trend",

            margin=dict(l=20, r=20, t=50, b=50),

            plot_bgcolor="white",
            paper_bgcolor="white",

            xaxis_title="",
            yaxis_title="Sales"
        )

        # Pad the x-axis a few months past the last data point so the
        # trend line doesn't stop flush against the right edge and the
        # axis reads through into the following year.
        fig.update_xaxes(
            range=[
                monthly["period"].min() - pd.DateOffset(months=1),
                monthly["period"].max() + pd.DateOffset(months=4)
            ]
        )

        style_chart(
            fig,
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    with col2:

        top_products = (
            filtered
            .groupby(
                "product_name",
                as_index=False
            )["total_sales"]
            .sum()
            .sort_values(
                "total_sales",
                ascending=False
            )
            .head(5)
            .sort_values("total_sales")
        )

        fig = px.bar(
            top_products,
            x="total_sales",
            y="product_name",
            orientation="h"
        )

        fig.update_traces(
            marker_color=GREEN_LIGHT,
            texttemplate="₱%{x:,.2s}",
            textposition="outside",
            cliponaxis=False
        )

        fig.update_layout(
            title="Top 5 Products",

            margin=dict(l=20, r=20, t=50, b=50),

            plot_bgcolor="white",
            paper_bgcolor="white",

            xaxis_title="",
            yaxis_title=""
        )

        fig.update_xaxes(
            range=[
                0,
                top_products["total_sales"].max() * 1.25
            ]
        )

        style_chart(
            fig,
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # SECOND ROW
    # ========================================================

    col3, col4 = st.columns(2)


    # --------------------------------------------------------
    # CATEGORY  (contribution % on the chart itself)
    # --------------------------------------------------------

    with col3:

        category_sales = (
            filtered
            .groupby(
                "category_name",
                as_index=False
            )["total_sales"]
            .sum()
            .sort_values(
                "total_sales",
                ascending=False
            )
        )


        fig = px.pie(
            category_sales,
            names="category_name",
            values="total_sales",
            hole=0.55,
            color_discrete_sequence=[GREEN, ORANGE, TEAL, PURPLE, POSITIVE, RED]
        )


        fig.update_traces(
            textinfo="label+percent",
            textposition="inside",
            textfont_size=11
        )


        fig.update_layout(
            title="Sales by Category",

            margin=dict(l=20, r=20, t=50, b=50),


            paper_bgcolor="white",

            showlegend=False
        )


        style_chart(
            fig,
            height=450
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

# --------------------------------------------------------
    # SALES MAP
    # --------------------------------------------------------

    with col4:

        country_map_data = (
            filtered
            .groupby("country", as_index=False)["total_sales"]
            .sum()
        )

        country_map_data["country_display"] = (
            country_map_data["country"]
            .replace(COUNTRY_NAME_FIXES)
        )

        fig = px.choropleth(
            country_map_data,
            locations="country_display",
            locationmode="country names",
            color="total_sales",
            color_continuous_scale=[[0, "#E3F5EC"], [1, GREEN]],
            hover_name="country"
        )

        fig.update_layout(
            title="Sales by Country",
            font=dict(color=TEXT_COLOR, size=12),
            title_font=dict(color=TEXT_COLOR, size=14),
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
                showframe=False,
                showcoastlines=False,
                projection_type="natural earth"
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="white",
            coloraxis_colorbar=dict(title="Sales")
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    render_html("""
    <div class="section-title">
        Geographic & Category Breakdown
    </div>
    """)

    col5 = st.columns(1)[0]
    # --------------------------------------------------------
    # MONTHLY SALES BY CATEGORY (stacked bar)
    # --------------------------------------------------------

    with col5:

        stacked_data = (
            filtered
            .groupby(
                ["year", "month", "category_name"],
                as_index=False
            )["total_sales"]
            .sum()
        )

        stacked_data["period"] = pd.to_datetime(
            stacked_data["year"].astype(str)
            + "-"
            + stacked_data["month"].astype(str)
            + "-01"
        )

        stacked_data = stacked_data.sort_values("period")

        if LAST_COMPLETE_PERIOD is not None:
            stacked_data = stacked_data[
                stacked_data["period"] <= LAST_COMPLETE_PERIOD
            ]

        fig = px.bar(
            stacked_data,
            x="period",
            y="total_sales",
            color="category_name",
            color_discrete_sequence=[GREEN, ORANGE, TEAL, PURPLE, POSITIVE, RED]
        )

        fig.update_layout(
            barmode="stack",
            title="Monthly Sales by Category",
            xaxis_title="",
            yaxis_title="Sales",
            legend_title_text="Category",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=50, b=50),
        )

        style_chart(fig, height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # FOURTH ROW — CATEGORY SALES TREND
    # ========================================================

    render_html("""
    <div class="section-title">
        Category Performance Over Time
    </div>
    """)

    category_trend = (
        filtered
        .groupby(
            ["year", "month", "category_name"],
            as_index=False
        )["total_sales"]
        .sum()
    )

    category_trend["period"] = pd.to_datetime(
        category_trend["year"].astype(str)
        + "-"
        + category_trend["month"].astype(str)
        + "-01"
    )

    category_trend = category_trend.sort_values("period")

    if LAST_COMPLETE_PERIOD is not None:
        category_trend = category_trend[
            category_trend["period"] <= LAST_COMPLETE_PERIOD
        ]

    fig = px.line(
        category_trend,
        x="period",
        y="total_sales",
        color="category_name",
        markers=True,
        color_discrete_sequence=[GREEN, ORANGE, TEAL, PURPLE, POSITIVE, RED]
    )

    fig.update_layout(
        title="Category Sales Trend",
        xaxis_title="",
        yaxis_title="Sales",
        legend_title_text="Category",
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    style_chart(fig, height=430)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PRODUCTS
# ============================================================

elif page == "Products":

    render_html("""
    <div class="section-title">
        Product Performance
    </div>
    """)

    product_matrix = (
        filtered
        .groupby(
            ["product_name", "category_name"],
            as_index=False
        )
        .agg(
            total_sales=("total_sales", "sum"),
            quantity=("quantity", "sum"),
            avg_price=("price", "mean")
        )
    )

    median_qty = product_matrix["quantity"].median()
    median_sales = product_matrix["total_sales"].median()

    # --------------------------------------------------------
    # TOP 15 PRODUCTS
    # --------------------------------------------------------

    render_html("""
    <div class="subsection-title">
        Top Products by Revenue
    </div>
    """)

    product_sales = (
        filtered
        .groupby(
            [
                "product_name",
                "category_name"
            ],
            as_index=False
        )["total_sales"]
        .sum()
        .sort_values(
            "total_sales",
            ascending=False
        )
        .reset_index(drop=True)
    )


    fig = px.bar(
        product_sales.head(15),
        x="total_sales",
        y="product_name",
        color="category_name",
        orientation="h",
        color_discrete_sequence=[GREEN, ORANGE, TEAL, PURPLE, POSITIVE, RED]
    )


    fig.update_layout(
        title="Top 15 Products by Revenue",

        plot_bgcolor="white",

        paper_bgcolor="white",

        legend_title_text="Category"
    )


    style_chart(
        fig,
        height=600
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # PARETO ANALYSIS
    # --------------------------------------------------------

    render_html("""
    <div class="subsection-title">
        Pareto Analysis — Revenue Concentration
    </div>
    """)

    pareto = (
        filtered
        .groupby("product_name", as_index=False)["total_sales"]
        .sum()
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )

    pareto["cumulative_pct"] = (
        pareto["total_sales"].cumsum()
        / pareto["total_sales"].sum()
        * 100
    )

    # How many products (of the full catalog) does it take to reach ~80% of revenue?
    n_products_80 = int((pareto["cumulative_pct"] < 80).sum() + 1)
    n_products_80 = min(n_products_80, len(pareto))
    pct_of_catalog = n_products_80 / len(pareto) * 100 if len(pareto) else 0

    st.caption(
        f"The top {n_products_80} of {len(pareto)} products "
        f"({pct_of_catalog:.0f}% of the catalog) account for roughly "
        f"80% of total revenue in the current selection."
    )

    pareto_display = pareto.head(20)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=pareto_display["product_name"],
            y=pareto_display["total_sales"],
            name="Revenue",
            marker_color=GREEN
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pareto_display["product_name"],
            y=pareto_display["cumulative_pct"],
            name="Cumulative %",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color=ORANGE, width=3)
        )
    )

    fig.update_layout(
        title="Top 20 Products — Revenue & Cumulative Contribution",
        xaxis_title="",
        yaxis=dict(title="Revenue"),
        yaxis2=dict(
            title="Cumulative %",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),
        legend=dict(orientation="h", y=1.12),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    fig.update_xaxes(tickangle=45)

    style_chart(fig, height=480)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # PRODUCT TABLE  (Rank + Revenue %)
    # --------------------------------------------------------

    render_html("""
    <div class="subsection-title">
        Product Performance Table
    </div>
    """)

    product_table = product_sales.copy()

    product_table["revenue_pct"] = (
        product_table["total_sales"]
        / product_table["total_sales"].sum()
        * 100
    ).round(1)

    product_table.insert(0, "rank", range(1, len(product_table) + 1))

    product_table = product_table.rename(columns={
        "rank": "Rank",
        "product_name": "Product",
        "category_name": "Category",
        "total_sales": "Revenue",
        "revenue_pct": "Revenue %"
    })

    st.dataframe(
        product_table.head(20),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# STORES & COUNTRIES
# ============================================================

elif page == "Stores & Countries":

    render_html("""
        <div class="section-title">
        Store & Geographic Performance
        </div>
    """)


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # STORES
    # --------------------------------------------------------

    with col1:

        store_sales = (
            filtered
            .groupby(
                "store_name",
                as_index=False
            )["total_sales"]
            .sum()
            .sort_values(
                "total_sales",
                ascending=False
            )
            .head(10)
            .sort_values("total_sales")
        )


        fig = px.bar(
            store_sales,
            x="total_sales",
            y="store_name",
            orientation="h"
        )


        fig.update_traces(
            marker_color=GREEN_LIGHT
        )


        fig.update_layout(
            title="Top 10 Stores",

            plot_bgcolor="white",

            paper_bgcolor="white"
        )


        style_chart(
            fig,
            height=450
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # CITIES
    # --------------------------------------------------------

    with col2:

        city_sales = (
            filtered
            .groupby(
                "city",
                as_index=False
            )["total_sales"]
            .sum()
            .sort_values(
                "total_sales",
                ascending=False
            )
            .head(10)
            .sort_values("total_sales")
        )


        fig = px.bar(
            city_sales,
            x="total_sales",
            y="city",
            orientation="h"
        )


        fig.update_traces(
            marker_color=GREEN
        )


        fig.update_layout(
            title="Top 10 Cities",

            plot_bgcolor="white",

            paper_bgcolor="white"
        )


        style_chart(
            fig,
            height=450
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =========================================================
    # ALL STORE AND CITY SALES TABLES
    # =========================================================

    st.markdown("<br>", unsafe_allow_html=True)


    col1, col2 = st.columns(2)


    # ---------------------------------------------------------
    # ALL STORE SALES
    # ---------------------------------------------------------

    with col1:

        st.markdown("### All Store Sales")


        all_store_sales = (
            filtered
            .groupby(
                "store_name",
                as_index=False
            )["total_sales"]
            .sum()
            .sort_values(
                "total_sales",
                ascending=False
            )
        )


        all_store_sales["total_sales"] = all_store_sales[
            "total_sales"
        ].apply(
            lambda x: f"₱{x:,.0f}"
        )


        st.dataframe(
            all_store_sales,
            use_container_width=True,
            hide_index=True
        )


    # ---------------------------------------------------------
    # ALL CITY SALES
    # ---------------------------------------------------------

    with col2:

        st.markdown("### All City Sales")


        all_city_sales = (
            filtered
            .groupby(
                "city",
                as_index=False
            )["total_sales"]
            .sum()
            .sort_values(
                "total_sales",
                ascending=False
            )
        )


        all_city_sales["total_sales"] = all_city_sales[
            "total_sales"
        ].apply(
            lambda x: f"₱{x:,.0f}"
        )


        st.dataframe(
            all_city_sales,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# FORECAST
# ============================================================

elif page == "Forecast":

    render_html("""
    <div class="section-title">
        Sales Forecast
    </div>
    """)

    st.info(
        "Forecasting is based on the historical monthly sales trend."
    )

    if len(filtered.groupby(["year", "month"]).size()) < 24:
        st.warning(
            "Seasonal forecasting requires at least 24 months of data. "
            "A simpler trend forecast is being used for the current selection."
        )

    # --------------------------------------------------------
    # MONTHLY SALES DATA
    # --------------------------------------------------------

    monthly_forecast = (
        filtered
        .groupby(
            ["year", "month"],
            as_index=False
        )["total_sales"]
        .sum()
    )

    monthly_forecast["period"] = pd.to_datetime(
        monthly_forecast["year"].astype(str)
        + "-"
        + monthly_forecast["month"].astype(str)
        + "-01"
    )

    monthly_forecast = (
        monthly_forecast
        .sort_values("period")
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # REMOVE PARTIAL MONTH
    # --------------------------------------------------------

    if (
        LAST_MONTH_IS_PARTIAL
        and len(monthly_forecast) > 1
    ):
        monthly_forecast = monthly_forecast.iloc[:-1]

    # --------------------------------------------------------
    # CREATE COMPLETE MONTHLY TIME SERIES
    # --------------------------------------------------------

    ts = (
        monthly_forecast
        .set_index("period")["total_sales"]
        .sort_index()
        .asfreq("MS")
    )

    # Fill missing months using interpolation
    ts = ts.interpolate()

    # --------------------------------------------------------
    # CHECK DATA
    # --------------------------------------------------------

    if len(ts) >= 3:

        # ----------------------------------------------------
        # FORECAST — Holt-Winters if enough data, else linear
        # ----------------------------------------------------

        from statsmodels.tsa.holtwinters import ExponentialSmoothing

        future_dates = pd.date_range(
            ts.index[-1] + pd.offsets.MonthBegin(),
            periods=12,
            freq="MS"
        )

        # Holt-Winters requires at least 2 full seasonal cycles (24 months)
        if len(ts) >= 24:
            try:
                model = ExponentialSmoothing(
                    ts.values,
                    trend="add",
                    seasonal="add",
                    seasonal_periods=12
                ).fit()

                future_values = model.forecast(12)

            except Exception:
                # Fall back to linear trend
                t = np.arange(len(ts))
                coef = np.polyfit(t, ts.values, 1)
                future_t = np.arange(len(ts), len(ts) + 12)
                future_values = np.polyval(coef, future_t)

        else:
            # Not enough data for seasonality — use linear trend
            t = np.arange(len(ts))
            coef = np.polyfit(t, ts.values, 1)
            future_t = np.arange(len(ts), len(ts) + 12)
            future_values = np.polyval(coef, future_t)

        future_values = np.maximum(future_values, 0)
        forecast = pd.Series(future_values, index=future_dates)

        # ----------------------------------------------------
        # FORECAST CHART
        # ----------------------------------------------------

        fig = go.Figure()

        # Actual sales
        fig.add_trace(
            go.Scatter(
                x=ts.index,
                y=ts.values,
                mode="lines+markers",
                name="Actual Sales",

                line=dict(
                    color=GREEN,
                    width=3,
                    shape="spline"
                ),

                marker=dict(
                    size=7,
                    color=GREEN
                ),

                hovertemplate=
                    "<b>%{x|%B %Y}</b><br>" +
                    "Actual Sales: ₱%{y:,.0f}" +
                    "<extra></extra>"
            )
        )

        # Forecast
        fig.add_trace(
            go.Scatter(
                x=forecast.index,
                y=forecast.values,
                mode="lines+markers",
                name="Forecast",

                line=dict(
                    color=ORANGE,
                    width=3,
                    dash="dash",
                    shape="spline"
                ),

                marker=dict(
                    size=7,
                    color=ORANGE
                ),

                hovertemplate=
                    "<b>%{x|%B %Y}</b><br>" +
                    "Forecast: ₱%{y:,.0f}" +
                    "<extra></extra>"
            )
        )

        # ----------------------------------------------------
        # FORECAST START LINE
        # ----------------------------------------------------

        fig.add_vline(
            x=ts.index[-1],
            line_width=1,
            line_dash="dot",
            line_color="#C7C7CC"
        )

        # ----------------------------------------------------
        # CHART DESIGN
        # ----------------------------------------------------

        fig.update_layout(

            title=dict(
                text="Monthly Sales Forecast",
                font=dict(
                    size=18,
                    color=TEXT_COLOR
                )
            ),

            xaxis=dict(
                title="Month",
                showgrid=False,
                tickfont=dict(
                    color=TEXT_MUTED
                )
            ),

            yaxis=dict(
                title="Sales",
                tickprefix="₱",
                tickformat=",.0f",
                gridcolor="rgba(60,60,67,0.06)",
                tickfont=dict(
                    color=TEXT_MUTED
                )
            ),

            plot_bgcolor="white",
            paper_bgcolor="white",

            hovermode="x unified",

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),

            margin=dict(
                l=20,
                r=20,
                t=80,
                b=30
            ),

            height=450
        )

        # ----------------------------------------------------
        # SHOW GRAPH
        # ----------------------------------------------------

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # FORECAST EXPLANATION
        # ----------------------------------------------------

        render_html("""
        <div style="
            background:white;
            border:1px solid rgba(60,60,67,0.08);
            border-radius: 0 !important;
            padding:16px 20px;
            margin-top:8px;
            margin-bottom:20px;
            color:#8E8E93;
            font-size:13px;
        ">
            <b style="color:#1C1C1E;">How to read the forecast:</b>
            The green line represents historical monthly sales,
            while the orange dashed line represents the projected
            sales for the next twelve months.
        </div>
        """)

        # ----------------------------------------------------
        # FORECAST VALUES
        # ----------------------------------------------------

        render_html("""
        <div class="section-title">
            Forecast Values
        </div>
        """)

        forecast_table = pd.DataFrame({
            "Month": forecast.index.strftime(
                "%B %Y"
            ),

            "Forecasted Sales": [
                f"₱{value:,.0f}"
                for value in forecast.values
            ]
        })

        st.dataframe(
            forecast_table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Not enough historical data to generate a forecast."
        )

# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="dashboard-footer">
    Apple Retail Sales BI Dashboard
</div>
""")
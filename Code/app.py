from __future__ import annotations

from datetime import date
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Insurance | Policy Recommendation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


PLANS = pd.DataFrame(
    [
        {
            "name": "Essential Care",
            "tier": "Essential",
            "monthly_premium": 96,
            "annual_cover": 250000,
            "deductible": 1500,
            "network": "Core network",
            "telehealth": True,
            "wellness": False,
            "family": False,
            "score_label": "Value focused",
            "description": "Affordable protection for everyday healthcare needs.",
            "color": "#2F80ED",
        },
        {
            "name": "Flexi Protect",
            "tier": "Balanced",
            "monthly_premium": 148,
            "annual_cover": 500000,
            "deductible": 750,
            "network": "Extended network",
            "telehealth": True,
            "wellness": True,
            "family": True,
            "score_label": "Best overall fit",
            "description": "Balanced cover with flexible access and preventive benefits.",
            "color": "#16A085",
        },
        {
            "name": "Premier Shield",
            "tier": "Premium",
            "monthly_premium": 245,
            "annual_cover": 1000000,
            "deductible": 250,
            "network": "Premium global network",
            "telehealth": True,
            "wellness": True,
            "family": True,
            "score_label": "Maximum protection",
            "description": "Comprehensive coverage for customers prioritising certainty.",
            "color": "#8E5CF7",
        },
    ]
)

DEMO_SCENARIOS = {
    "Alex Morgan · Balanced family": {
        "name": "Alex Morgan",
        "budget": 180,
        "cover_preference": "Balanced",
        "family_members": 1,
        "digital_first": True,
        "wellness": True,
    },
    "Priya Shah · Value seeker": {
        "name": "Priya Shah",
        "budget": 110,
        "cover_preference": "Basic",
        "family_members": 0,
        "digital_first": True,
        "wellness": False,
    },
    "Jordan Lee · Maximum protection": {
        "name": "Jordan Lee",
        "budget": 300,
        "cover_preference": "High",
        "family_members": 2,
        "digital_first": False,
        "wellness": True,
    },
}

REQUIRED_PRODUCT_COLUMNS = {
    "plan_name",
    "monthly_premium",
    "annual_coverage",
    "deductible",
    "network",
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');
        :root { --ink: #17243a; --muted: #6d7c91; --navy: #101d35; --line: #e6ebf2; }
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
        .stApp { background: #f6f8fb; }
        [data-testid="stSidebar"] { background: var(--navy); }
        [data-testid="stSidebar"] * { color: #d7e1f1; }
        [data-testid="stSidebar"] .stRadio label { color: #d7e1f1 !important; }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4 { font-family: 'Manrope', sans-serif; color: var(--ink) !important; letter-spacing: -0.02em; }
        .stApp p, .stApp label, .stApp [data-testid="stMarkdownContainer"] { color: var(--ink); }
        .stApp [data-testid="stSidebar"] p, .stApp [data-testid="stSidebar"] label,
        .stApp [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: #d7e1f1; }
        h1 { font-size: 2.1rem !important; }
        .brand { color: white; font-family: 'Manrope', sans-serif; font-size: 1.4rem; font-weight: 800; margin: 0 0 2rem 0; }
        .brand span { color: #5ee2c1; }
        .eyebrow { color: #16a085; text-transform: uppercase; font-weight: 700; font-size: .72rem; letter-spacing: .12em; margin-bottom: .35rem; }
        .hero { background: linear-gradient(115deg,#10213c 0%,#19385b 65%,#176b72 100%); border-radius: 18px; padding: 28px 32px; color: white; margin-bottom: 20px; }
        .hero h1 { color: white !important; margin: 0; }
        .hero p { color: #c8d8ea; margin: 8px 0 0; font-size: 1rem; }
        .hero-badge { background: rgba(94,226,193,.16); border: 1px solid rgba(94,226,193,.35); color: #8ff4d9; border-radius: 30px; padding: 7px 12px; display: inline-block; font-size: .78rem; font-weight: 600; margin-bottom: 15px; }
        .card { background: white; border: 1px solid var(--line); border-radius: 14px; padding: 20px; box-shadow: 0 3px 14px rgba(24,42,72,.04); height: 100%; }
        .plan-card { background: white; border: 1px solid var(--line); border-radius: 14px; padding: 20px; height: 100%; position: relative; }
        .recommended { border: 2px solid #16a085; box-shadow: 0 8px 24px rgba(22,160,133,.14); }
        .rec-badge { color: #117b68; background: #dff7f0; border-radius: 20px; font-size: .73rem; padding: 5px 9px; font-weight: 700; display: inline-block; }
        .plan-name { font-family: 'Manrope'; font-size: 1.18rem; font-weight: 800; margin: 13px 0 2px; }
        .plan-desc { color: var(--muted); font-size: .84rem; min-height: 44px; }
        .price { font-family: 'Manrope'; font-size: 1.8rem; color: var(--ink); margin-top: 12px; }
        .price small { font-family: 'DM Sans'; font-size: .78rem; color: var(--muted); font-weight: 400; }
        .feature { border-top: 1px solid #edf0f5; padding: 8px 0; font-size: .82rem; }
        .feature b { float: right; color: var(--ink); }
        .section-title { font-family: 'Manrope'; font-size: 1.15rem; margin: 24px 0 12px; }
        .insight { border-left: 4px solid #16a085; background: #eaf8f4; padding: 13px 16px; border-radius: 0 10px 10px 0; font-size: .9rem; }
        .stButton > button, .stDownloadButton > button {
            border-radius: 8px;
            font-weight: 600;
            color: #ffffff !important;
            background: #17243a;
            border: 1px solid #17243a;
        }
        .stButton > button p, .stButton > button span,
        .stDownloadButton > button p, .stDownloadButton > button span {
            color: #ffffff !important;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            color: #ffffff !important;
            background: #16a085;
            border-color: #16a085;
        }
        div[data-testid="stMetric"] { background: white; border: 1px solid var(--line); padding: 14px 16px; border-radius: 12px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_product_catalogue(uploaded_files) -> tuple[pd.DataFrame, str]:
    if not uploaded_files:
        return PLANS.copy(), "Synthetic demo catalogue"
    catalogues = []
    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith(".xlsx"):
            catalogue = pd.read_excel(uploaded_file)
        else:
            catalogue = pd.read_csv(uploaded_file)
        catalogue.columns = [
            str(column).strip().lower().replace(" ", "_")
            for column in catalogue.columns
        ]
        missing = REQUIRED_PRODUCT_COLUMNS - set(catalogue.columns)
        if missing:
            missing_columns = ", ".join(sorted(missing))
            raise ValueError(
                f"{uploaded_file.name} is missing required columns: {missing_columns}"
            )
        catalogue = catalogue.rename(
            columns={
                "plan_name": "name",
                "annual_coverage": "annual_cover",
            }
        )
        for column in ["monthly_premium", "annual_cover", "deductible"]:
            catalogue[column] = pd.to_numeric(catalogue[column], errors="raise")
        defaults = {
            "tier": "Custom",
            "telehealth": True,
            "wellness": False,
            "family": False,
            "score_label": "Catalogue plan",
            "description": "Imported from the uploaded product catalogue.",
            "color": "#16A085",
        }
        for column, value in defaults.items():
            if column not in catalogue.columns:
                catalogue[column] = value
        catalogues.append(catalogue)
    source_names = ", ".join(uploaded_file.name for uploaded_file in uploaded_files)
    return pd.concat(catalogues, ignore_index=True), f"Uploaded catalogues: {source_names}"


def score_plans(profile: dict, product_catalogue: pd.DataFrame) -> pd.DataFrame:
    scored = product_catalogue.copy()
    scores: list[float] = []
    reasons: list[str] = []
    for _, plan in scored.iterrows():
        score = 50.0
        reason_parts: list[str] = []
        if profile["budget"] >= plan["monthly_premium"]:
            score += 18
            reason_parts.append("fits your monthly budget")
        else:
            score -= min(20, (plan["monthly_premium"] - profile["budget"]) / 10)
        if profile["cover_preference"] == "High" and plan["annual_cover"] >= 500000:
            score += 15
            reason_parts.append("meets your high-cover preference")
        elif profile["cover_preference"] == "Basic" and plan["monthly_premium"] <= 120:
            score += 12
            reason_parts.append("keeps premiums affordable")
        elif profile["cover_preference"] == "Balanced" and plan["tier"] == "Balanced":
            score += 17
            reason_parts.append("matches your balanced protection goal")
        if profile["family_members"] > 0 and plan["family"]:
            score += 9
            reason_parts.append("supports family coverage")
        if profile["digital_first"] and plan["telehealth"]:
            score += 5
            reason_parts.append("includes digital-first care")
        if profile["wellness"] and plan["wellness"]:
            score += 6
            reason_parts.append("includes preventive wellness benefits")
        scores.append(round(min(99, max(1, score)), 1))
        reasons.append(", ".join(reason_parts[:2]) or "offers a different coverage trade-off")
    scored["match_score"] = scores
    scored["reason"] = reasons
    return scored.sort_values("match_score", ascending=False).reset_index(drop=True)


def make_csv(profile: dict, ranked: pd.DataFrame) -> bytes:
    report = pd.DataFrame(
        [
            {"Field": "Customer", "Value": profile["name"]},
            {"Field": "Generated", "Value": date.today().isoformat()},
            {"Field": "Recommended plan", "Value": ranked.iloc[0]["name"]},
            {"Field": "Match score", "Value": f'{ranked.iloc[0]["match_score"]:.0f}%'},
            {"Field": "Monthly premium", "Value": f'${ranked.iloc[0]["monthly_premium"]:,.0f}'},
            {"Field": "Annual cover", "Value": f'${ranked.iloc[0]["annual_cover"]:,.0f}'},
            {"Field": "Profile scenario", "Value": profile["scenario"]},
        ]
    )
    return report.to_csv(index=False).encode("utf-8")


inject_styles()

with st.sidebar:
    st.markdown('<div class="brand">Insur<span>AI</span></div>', unsafe_allow_html=True)
    st.markdown("### Recommendation studio")
    st.caption("Personalised protection recommendations for every customer.")
    page = st.radio("Navigate", ["Recommendation", "How it works"], label_visibility="collapsed")
    st.divider()
    scenario_name = "Alex Morgan · Balanced family"
    scenario = DEMO_SCENARIOS[scenario_name]
    st.divider()
    st.markdown("### Product data source")
    uploaded_catalogue = st.file_uploader(
        "Upload product catalogue",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
    )
    try:
        product_catalogue, catalogue_source = load_product_catalogue(uploaded_catalogue)
        st.success(f"{len(product_catalogue)} plans loaded")
    except (ValueError, pd.errors.ParserError) as error:
        st.error(f"Catalogue error: {error}")
        st.stop()
    st.caption("PRODUCT CATALOGUE")
    st.caption("Uploaded catalogue or demo sample")

if page == "How it works":
    st.markdown('<div class="eyebrow">Client demo / explainability</div>', unsafe_allow_html=True)
    st.title("From customer needs to a confident recommendation")
    st.markdown("This solution demonstrates how a transparent rules-and-score layer can support an advisor while keeping underwriting and suitability controls in place.")
    cols = st.columns(3)
    for col, number, title, copy in zip(
        cols,
        ["01", "02", "03"],
        ["Capture needs", "Rank fit", "Explain clearly"],
        ["Collect budget, coverage priorities and household context.",
         "Score each plan against declared preferences and benefits.",
         "Show the match score, trade-offs and alternate options."],
    ):
        with col:
            st.markdown(f'<div class="card"><div class="eyebrow">{number}</div><h3>{title}</h3><p>{copy}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Solution scope</div>', unsafe_allow_html=True)
    st.info("This demonstration uses a representative insurance product catalogue and explainable matching logic. A production implementation can connect the same experience to approved product data and existing business systems.")
    st.warning("The displayed premiums, benefits and match scores are representative and should be replaced with the insurer's approved catalogue before customer use.")
    st.stop()

st.markdown(
    '<div class="hero"><span class="hero-badge">✦ PERSONALIZED POLICY DISCOVERY</span><h1>Find the right cover for every customer</h1><p>Turn customer needs into a clear, explainable insurance recommendation in seconds.</p></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">1. Customer profile</div>', unsafe_allow_html=True)
with st.container():
    input_cols = st.columns([1.3, 1, 1, 1])
    with input_cols[0]:
        customer_options = list(DEMO_SCENARIOS) + ["Enter new customer"]
        selected_customer = st.selectbox(
            "Select customer profile",
            customer_options,
            format_func=lambda value: (
                DEMO_SCENARIOS[value]["name"] if value != "Enter new customer" else value
            ),
        )
        if selected_customer == "Enter new customer":
            customer_name = st.text_input("Customer name", "New customer")
            selected_profile = {
                "budget": 180,
                "cover_preference": "Balanced",
                "family_members": 0,
                "digital_first": True,
                "wellness": False,
            }
        else:
            customer_name = DEMO_SCENARIOS[selected_customer]["name"]
            selected_profile = DEMO_SCENARIOS[selected_customer]
    profile_defaults = selected_profile
    with input_cols[1]:
        budget = st.slider(
            "Monthly budget ($)",
            50,
            350,
            profile_defaults["budget"],
            10,
            key=f"budget-{selected_customer}",
        )
    with input_cols[2]:
        cover_preference = st.selectbox(
            "Coverage preference",
            ["Balanced", "Basic", "High"],
            index=["Balanced", "Basic", "High"].index(profile_defaults["cover_preference"]),
            key=f"cover-{selected_customer}",
        )
    with input_cols[3]:
        family_members = st.number_input(
            "Additional family members",
            0,
            6,
            profile_defaults["family_members"],
            key=f"family-{selected_customer}",
        )
    pref_cols = st.columns(3)
    with pref_cols[0]:
        digital_first = st.checkbox(
            "Prefers digital / telehealth",
            profile_defaults["digital_first"],
            key=f"digital-{selected_customer}",
        )
    with pref_cols[1]:
        wellness = st.checkbox(
            "Interested in wellness benefits",
            profile_defaults["wellness"],
            key=f"wellness-{selected_customer}",
        )

profile = {
    "name": customer_name.strip() or "Customer",
    "budget": budget,
    "cover_preference": cover_preference,
    "family_members": family_members,
    "digital_first": digital_first,
    "wellness": wellness,
    "scenario": selected_customer,
}
ranked = score_plans(profile, product_catalogue)
best = ranked.iloc[0]

st.markdown('<div class="section-title">2. Personalised recommendation</div>', unsafe_allow_html=True)
metric_cols = st.columns(4)
metric_cols[0].metric("Best match", best["name"])
metric_cols[1].metric("Match confidence", f'{best["match_score"]:.0f}%')
metric_cols[2].metric("Monthly premium", f'${best["monthly_premium"]:,.0f}')
metric_cols[3].metric("Annual cover", f'${best["annual_cover"]:,.0f}')

st.markdown(
    f'<div class="insight"><b>Why this recommendation?</b> {best["name"]} {best["reason"]}. It provides a ${best["annual_cover"]:,.0f} annual limit with a ${best["deductible"]:,.0f} deductible.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="section-title">Compare suitable plans</div>', unsafe_allow_html=True)
plan_cols = st.columns(min(3, len(ranked)))
for col, (_, plan) in zip(plan_cols, ranked.iterrows()):
    is_best = plan["name"] == best["name"]
    with col:
        badge = '<span class="rec-badge">✓ RECOMMENDED</span>' if is_best else f'<span class="rec-badge" style="background:#f0f3f7;color:#66758a">{plan["score_label"].upper()}</span>'
        css_class = "plan-card recommended" if is_best else "plan-card"
        st.markdown(
            f"""<div class="{css_class}">
            {badge}<div class="plan-name">{plan["name"]}</div>
            <div class="plan-desc">{plan["description"]}</div>
            <div class="price">${plan["monthly_premium"]:,}<small> / month</small></div>
            <div class="feature">Match score <b>{plan["match_score"]:.0f}%</b></div>
            <div class="feature">Annual cover <b>${plan["annual_cover"]:,}</b></div>
            <div class="feature">Deductible <b>${plan["deductible"]:,}</b></div>
            <div class="feature">Network <b>{plan["network"]}</b></div>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-title">Recommendation rationale</div>', unsafe_allow_html=True)
table = ranked[["name", "match_score", "reason", "monthly_premium", "annual_cover"]].copy()
table.columns = ["Plan", "Match", "Key fit signals", "Monthly premium", "Annual cover"]
table["Match"] = table["Match"].map(lambda value: f"{value:.0f}%")
table["Monthly premium"] = table["Monthly premium"].map(lambda value: f"${value:,.0f}")
table["Annual cover"] = table["Annual cover"].map(lambda value: f"${value:,.0f}")
st.dataframe(table, hide_index=True, use_container_width=True)

download_cols = st.columns([1, 1, 3])
with download_cols[0]:
    st.download_button(
        "Download summary",
        data=make_csv(profile, ranked),
        file_name=f"insurai-recommendation-{profile['name'].lower().replace(' ', '-')}.csv",
        mime="text/csv",
        use_container_width=True,
    )
with download_cols[1]:
    if st.button("Reset customer profile", use_container_width=True):
        profile_widget_keys = [
            f"budget-{selected_customer}",
            f"cover-{selected_customer}",
            f"family-{selected_customer}",
            f"digital-{selected_customer}",
            f"wellness-{selected_customer}",
        ]
        for widget_key in profile_widget_keys:
            st.session_state.pop(widget_key, None)
        st.rerun()
with download_cols[2]:
    st.caption("Illustrative recommendation only. Final suitability, pricing and eligibility require approved product and underwriting checks.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from prediction import predict_churn
from utils import risk_level

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Bank Customer Churn Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Bank Customer Churn Dashboard")
st.markdown("### Customer Churn Analytics using Machine Learning")

st.markdown("---")

# -----------------------------
# Load Dataset
# -----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/European_Bank.csv")

df = load_data()
# -----------------------------
# KPI Cards
# -----------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        len(df)
    )

with col2:
    churn_rate = df["Exited"].mean() * 100

    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col3:
    st.metric(
        "Average Balance",
        f"${df['Balance'].mean():,.0f}"
    )

with col4:
    st.metric(
        "Average Credit Score",
        round(df["CreditScore"].mean())
    )
    st.markdown("---")

st.subheader("📊 Probability Distribution Visualization")

col1, col2 = st.columns(2)

# -----------------------------
# Churn Distribution
# -----------------------------
with col1:

    churn_data = (
        df["Exited"]
        .value_counts()
        .reset_index()
    )

    churn_data.columns = ["Status", "Count"]

    churn_data["Status"] = churn_data["Status"].replace(
        {
            0: "Stayed",
            1: "Churned"
        }
    )

    fig = px.pie(
        churn_data,
        names="Status",
        values="Count",
        title="Customer Churn Distribution",
        hole=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Geography Distribution
# -----------------------------
with col2:

    geo = (
        df.groupby("Geography")["Exited"]
        .mean()
        .reset_index()
    )

    geo["Exited"] = geo["Exited"] * 100

    fig = px.bar(
        geo,
        x="Geography",
        y="Exited",
        color="Exited",
        title="Churn Rate by Geography"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    st.markdown("---")

col3, col4 = st.columns(2)

# -----------------------------
# Age Distribution
# -----------------------------
with col3:

    fig = px.histogram(
        df,
        x="Age",
        color="Exited",
        nbins=30,
        title="Age Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Balance Distribution
# -----------------------------
with col4:

    fig = px.box(
        df,
        x="Exited",
        y="Balance",
        color="Exited",
        title="Balance Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    st.markdown("---")

st.markdown("---")

st.header("🤖 Customer Churn Risk Calculator")

col1, col2 = st.columns(2)

with col1:

    credit_score = st.number_input(
        "Credit Score",
        300,
        900,
        650
    )

    geography = st.selectbox(
        "Geography",
        ["France", "Germany", "Spain"]
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    age = st.slider(
        "Age",
        18,
        100,
        35
    )

    tenure = st.slider(
        "Tenure",
        0,
        10,
        5
    )

with col2:

    balance = st.number_input(
        "Balance",
        value=50000.0
    )

    num_products = st.selectbox(
        "Number of Products",
        [1, 2, 3, 4]
    )

    has_card = st.selectbox(
        "Has Credit Card",
        [0, 1]
    )

    active_member = st.selectbox(
        "Active Member",
        [0, 1]
    )

    salary = st.number_input(
        "Estimated Salary",
        value=50000.0
    )
    # -----------------------------
# -----------------------------
# Feature Engineering
# -----------------------------

balance_salary_ratio = balance / (salary + 1)
product_density = num_products / (tenure + 1)
engagement_product = active_member * num_products
age_tenure = age * tenure

# -----------------------------
# Prediction
# -----------------------------

if st.button("🔮 Predict Churn"):

    input_data = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": has_card,
        "IsActiveMember": active_member,
        "EstimatedSalary": salary,
        "BalanceSalaryRatio": balance_salary_ratio,
        "ProductDensity": product_density,
        "EngagementProduct": engagement_product,
        "AgeTenure": age_tenure
    }

    prediction, probability = predict_churn(input_data)

    st.markdown("---")
    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("⚠️ Customer is likely to Churn")
    else:
        st.success("✅ Customer is likely to Stay")

    st.metric(
        "Churn Probability",
        f"{probability * 100:.2f}%"
    )

    fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=probability * 100,
    title={"text": "Churn Risk (%)"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "darkred"},
        "steps": [
            {"range": [0, 30], "color": "#90EE90"},
            {"range": [30, 70], "color": "#FFD966"},
            {"range": [70, 100], "color": "#FF9999"},
        ],
    },
))

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="churn_gauge"
    )

    st.info(
        f"Risk Level: {risk_level(probability)}"
    )

    # ======================================================
# FEATURE IMPORTANCE DASHBOARD
# ======================================================

st.markdown("---")
st.header("⭐ Feature Importance Dashboard")

st.write(
    "These visualizations explain which features have the greatest impact "
    "on customer churn predictions."
)

tab1, tab2, tab3 = st.tabs(
    [
        "Feature Importance",
        "SHAP Summary",
        "SHAP Bar Plot"
    ]
)

with tab1:

    st.image(
        "images/12_feature_importance.png",
        caption="Feature Importance",
        use_container_width=True
    )

with tab2:

    st.image(
        "images/13_shap_summary_plot.png",
        caption="SHAP Summary Plot",
        use_container_width=True
    )

with tab3:

    st.image(
        "images/14_shap_bar_plot.png",
        caption="SHAP Bar Plot",
        use_container_width=True
    )
    # ======================================================


# ======================================================
# WHAT-IF SCENARIO SIMULATOR
# ======================================================

st.markdown("---")
st.header("🎯 What-if Scenario Simulator")

st.write(
    "Modify customer values and observe how churn probability changes."
)

col1, col2 = st.columns(2)

with col1:

    sim_age = st.slider(
        "Age",
        18,
        100,
        age,
        key="sim_age"
    )

    sim_balance = st.number_input(
        "Balance",
        value=float(balance),
        key="sim_balance"
    )

    sim_products = st.selectbox(
        "Number of Products",
        [1, 2, 3, 4],
        index=num_products-1,
        key="sim_products"
    )

with col2:

    sim_salary = st.number_input(
        "Estimated Salary",
        value=float(salary),
        key="sim_salary"
    )

    sim_active = st.selectbox(
        "Active Member",
        [0, 1],
        index=active_member,
        key="sim_active"
    )

if st.button("Run What-if Simulation"):

    sim_balance_salary_ratio = sim_balance / (sim_salary + 1)
    sim_product_density = sim_products / (tenure + 1)
    sim_engagement_product = sim_active * sim_products
    sim_age_tenure = sim_age * tenure

    simulation_data = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": sim_age,
        "Tenure": tenure,
        "Balance": sim_balance,
        "NumOfProducts": sim_products,
        "HasCrCard": has_card,
        "IsActiveMember": sim_active,
        "EstimatedSalary": sim_salary,
        "BalanceSalaryRatio": sim_balance_salary_ratio,
        "ProductDensity": sim_product_density,
        "EngagementProduct": sim_engagement_product,
        "AgeTenure": sim_age_tenure
    }

    sim_prediction, sim_probability = predict_churn(simulation_data)
   

    # =====================================================
    # Simulation Result
    # =====================================================

    st.markdown("---")
    st.subheader("📊 Simulation Result")

    if sim_prediction == 1:
        st.error("⚠️ Customer is likely to Churn")
    else:
        st.success("✅ Customer is likely to Stay")

    st.metric(
        "New Churn Probability",
        f"{sim_probability * 100:.2f}%"
    )

    st.info(
        f"Risk Level : {risk_level(sim_probability)}"
    )

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sim_probability * 100,
        title={"text": "Simulation Risk"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkred"},
            "steps": [
                {"range": [0, 30], "color": "lightgreen"},
                {"range": [30, 70], "color": "khaki"},
                {"range": [70, 100], "color": "lightcoral"},
            ],
        },
    ))

    st.plotly_chart(
        gauge,
        use_container_width=True,
        key="simulation_gauge"
    )

   
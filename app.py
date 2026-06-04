# app.py
import streamlit as st # type: ignore
import pandas as pd
import plotly.express as px # type: ignore

st.set_page_config(page_title="Customer Churn Analysis", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

from components.styles import get_custom_css
from components.kpi import render_kpi_card
from utils.data_helper import generate_telecom_cohorts, train_and_evaluate_models
from utils.pdf_generator import generate_pdf_report

st.markdown(get_custom_css(), unsafe_allow_html=True)

df = generate_telecom_cohorts()
fitted_models, eval_metrics, scaler, label_encoders, features_list = train_and_evaluate_models(df)

COLORS_PAL = {'teal': '#38bdf8', 'purple': '#818cf8', 'pink': '#f472b6', 'gold': '#fbbf24', 'blue': '#1d4ed8'}

with st.sidebar:
    st.markdown("<h2 class='gradient-text'>CUSTOMER CHURN ANALYSIS</h2>", unsafe_allow_html=True)
    selected_page = st.radio("NAVIGATION", ["🏠 Executive Overview", "🔮 Interactive Predictor", "🎯 Cohort Segmentation", "📈 Advanced Analytics", "🤖 Model Performance Matrix", "💡 Strategic AI Insights"])
    contract_filter = st.selectbox("Contract Type", ["All"] + list(df['Contract'].unique()))
    internet_filter = st.selectbox("Internet Technology", ["All"] + list(df['InternetService'].unique()))
    
    filtered_df = df.copy()
    if contract_filter != "All": filtered_df = filtered_df[filtered_df['Contract'] == contract_filter]
    if internet_filter != "All": filtered_df = filtered_df[filtered_df['InternetService'] == internet_filter]

if selected_page == "🏠 Executive Overview":
    st.markdown("<h1 class='gradient-text'>Enterprise Executive Dashboard</h1>", unsafe_allow_html=True)
    tot_subscribers = len(filtered_df)
    churn_rate_val = (filtered_df['Churn'] == 'Yes').mean()
    mrr_pool = filtered_df['MonthlyCharges'].sum()
    mrr_risk = filtered_df[filtered_df['Churn'] == 'Yes']['MonthlyCharges'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(render_kpi_card("Total Customers", f"{tot_subscribers:,}", "+1.4% MoM", "neutral", "👥"), unsafe_allow_html=True)
    with col2: st.markdown(render_kpi_card("Churn Rate", f"{churn_rate_val:.1%}", "Target < 15%", "negative" if churn_rate_val > 0.15 else "positive", "📉"), unsafe_allow_html=True)
    with col3: st.markdown(render_kpi_card("Monthly Risk", f"${mrr_risk:,.0f}", f"{mrr_risk/mrr_pool:.1%} MRR", "negative", "💰"), unsafe_allow_html=True)
    
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    fig_charges = px.histogram(filtered_df, x='MonthlyCharges', color='Churn', color_discrete_map={'No': COLORS_PAL['teal'], 'Yes': COLORS_PAL['pink']})
    fig_charges.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
    st.plotly_chart(fig_charges, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_page == "🔮 Interactive Predictor":
    st.markdown("<h1 class='gradient-text'>Interactive Churn Predictor</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        tenure_in = st.slider("Tenure length (Months)", 1, 72, 12)
        contract = st.selectbox("Contract Terms", ["Month-to-month", "One year", "Two year"])
        payment = st.selectbox("Payment Gateway Type", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
    with col2:
        internet = st.selectbox("Internet Service Type", ["DSL", "Fiber optic", "No"])
        monthly_charge = st.number_input("Monthly Charges ($)", value=75.0)
        
    if st.button("RUN PREDICTIVE RUNTIME", type="primary"):
        input_data = pd.DataFrame([{'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No', 'tenure': tenure_in, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': internet, 'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No', 'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': contract, 'PaperlessBilling': 'Yes', 'PaymentMethod': payment, 'MonthlyCharges': monthly_charge, 'TotalCharges': monthly_charge * tenure_in}])
        encoded_input = input_data.copy()
        for col, le in label_encoders.items():
            encoded_input[col] = le.transform([input_data[col][0]]) if input_data[col][0] in le.classes_ else 0
        encoded_input[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.transform(encoded_input[['tenure', 'MonthlyCharges', 'TotalCharges']])
        
        risk_probability = fitted_models['Logistic Regression'].predict_proba(encoded_input[features_list])[:, 1][0]
        st.markdown(f"### Predicted Attrition Risk: **{risk_probability:.1%}**")
        
        pdf_details = {'Tenure': f"{tenure_in} mo", 'Contract': contract, 'Monthly Charge': f"${monthly_charge}"}
        pdf_data = generate_pdf_report("TEMP-CUST", risk_probability, "High" if risk_probability > 0.5 else "Low", ["Upgrade contract", "Enable auto-pay"], pdf_details)
        st.download_button("Download Retention PDF", data=pdf_data, file_name="Churn_Risk_Report.pdf", mime="application/pdf")

elif selected_page == "🎯 Cohort Segmentation":
    st.markdown("<h1 class='gradient-text'>Customer Segmentation</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    fig_seg = px.scatter(df, x='tenure', y='MonthlyCharges', color='SegmentName', color_discrete_map={"New / Budget": COLORS_PAL['blue'], "High-Spend / High-Risk": COLORS_PAL['pink'], "Loyal / Budget": COLORS_PAL['teal'], "High-Value / Loyal": COLORS_PAL['purple']})
    fig_seg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
    st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_page == "📈 Advanced Analytics":
    st.markdown("<h1 class='gradient-text'>Cohort & Advanced Metrics</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.subheader("Geographic Distribution & Heatmap")
    us_states_sim = pd.DataFrame({'State': ['CA', 'TX', 'NY', 'FL', 'IL'], 'Churn_Rate': [28.4, 21.2, 31.5, 29.8, 24.1]})
    fig_map = px.choropleth(us_states_sim, locations='State', locationmode="USA-states", color='Churn_Rate', scope="usa", color_continuous_scale="Reds")
    fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_page == "🤖 Model Performance Matrix":
    st.markdown("<h1 class='gradient-text'>Model Performance</h1>", unsafe_allow_html=True)
    for m_name, metrics in eval_metrics.items():
        st.markdown(f"### {m_name}")
        st.write(f"ROC-AUC: **{metrics['roc_auc']:.4f}** | Accuracy: **{metrics['accuracy']:.1%}**")

elif selected_page == "💡 Strategic AI Insights":
    st.markdown("<h1 class='gradient-text'>AI Strategic Insights</h1>", unsafe_allow_html=True)
    st.markdown("<div class='insight-box'><b>Friction Drivers:</b> Month-to-Month contracts and electronic check processes correlate with churn.</div>", unsafe_allow_html=True)
    st.markdown("<div class='warning-box'><b>Playbook action:</b> Move high-spend subscribers to 1-Year terms.</div>", unsafe_allow_html=True)
import streamlit as st
import math

# Utility functions
def format_inr(amount):
    return '{:,.0f}'.format(amount)

def future_value(pv, rate, years):
    return pv * ((1 + rate) ** years)

def future_value_annuity(pmt, rate, years):
    return pmt * (((1 + rate) ** years - 1) / rate) if rate != 0 else pmt * years

def present_value_annuity(pmt, rate, years):
    return pmt * (1 - (1 + rate) ** -years) / rate if rate != 0 else pmt * years

# Streamlit App
st.set_page_config(page_title="Retirement Calculator", layout="centered")
st.title("🧓 Retirement Planning Calculator")

st.header("📋 Enter your details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Current Age", min_value=18, max_value=100, value=30)
    retirement_age = st.number_input("Retirement Age", min_value=age+1, max_value=100, value=60)
    annual_income = st.number_input("Current Annual Income (₹)", min_value=0, value=10000000)
    income_growth = st.number_input("Expected Annual Income Growth (%)", min_value=0.0, value=0.0)
    expenses = st.number_input("Current Annual Expenses (₹)", min_value=0, value=8000000)
    inflation = st.number_input("Inflation Rate (%)", min_value=0.0, value=8.0)

with col2:
    savings = st.number_input("Annual Savings / Investments (₹)", min_value=0, value=2000000)
    current_savings = st.number_input("Current Savings (₹)", min_value=0, value=18000000)
    return_rate = st.number_input("Expected Annual Rate of Return (%)", min_value=0.0, value=8.0)
    lifespan = st.number_input("Expected Lifespan", min_value=retirement_age+1, max_value=120, value=80)

st.markdown("---")

# CALCULATION
years_to_retire = retirement_age - age
years_in_retirement = lifespan - retirement_age

r = return_rate / 100
i = inflation / 100
real_rate = ((1 + r) / (1 + i)) - 1 if r != i else 0

adjusted_expenses = future_value(expenses, i, years_to_retire)
required_corpus = present_value_annuity(adjusted_expenses, real_rate, years_in_retirement)

fv_current_savings = future_value(current_savings, r, years_to_retire)
fv_future_contributions = future_value_annuity(savings, r, years_to_retire)
total_corpus = fv_current_savings + fv_future_contributions

gap = required_corpus - total_corpus
deficit = gap > 0

extra_monthly_savings = 0
if deficit:
    months = years_to_retire * 12
    monthly_rate = r / 12
    extra_monthly_savings = (gap * monthly_rate) / (((1 + monthly_rate) ** months - 1)) if monthly_rate != 0 else gap / months

# RESULTS
st.header("📊 Results")
st.markdown(f"- 📅 Years until retirement: **{years_to_retire}**")
st.markdown(f"- 📆 Years in retirement: **{years_in_retirement}**")
st.markdown(f"- 💸 Expenses at retirement (inflation adjusted): **₹{format_inr(adjusted_expenses)} / year**")
st.markdown(f"- 🎯 Required corpus at retirement: **₹{format_inr(required_corpus)}**")
st.markdown(f"- 💼 Projected corpus at retirement: **₹{format_inr(total_corpus)}**")

if deficit:
    st.markdown(f"- 🚨 Deficit at retirement: **₹{format_inr(gap)}**")
    st.markdown(f"- 🧾 You need to save an extra: **₹{format_inr(extra_monthly_savings)} / month** from today")
else:
    st.markdown("✅ Your current savings and investments are sufficient for retirement.")

# EXPLANATION
with st.expander("📘 How is this calculated?"):
    st.markdown("""
    - **Adjusted Expenses**: Your annual expenses are grown with inflation till retirement age.
    - **Required Corpus**: The amount needed at retirement to cover all future expenses is calculated using the Present Value of Annuity formula.
    - **Projected Corpus**: Includes future value of your existing savings and future annual investments.
    - **Deficit (if any)**: If you're short, we calculate how much extra you must save per month to reach your retirement goal.
    """)


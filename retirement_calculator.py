import streamlit as st
import locale

# Indian currency format
locale.setlocale(locale.LC_ALL, 'en_IN')

def format_indian(number):
    return locale.format_string("%d", number, grouping=True)

st.set_page_config(page_title="Smart Retirement Planner", page_icon="📈", layout="centered")
st.title("📈 Smart Retirement Planner")

# User Inputs
st.header("🧾 Your Current Financial Info")

annual_income = st.number_input("Current Annual Income (₹)", min_value=0, step=10000, value=600000)
income_growth_rate = st.number_input("Expected Annual Income Growth Rate (%)", min_value=0.0, max_value=100.0, step=0.1, value=5.0)
annual_expenses = st.number_input("Current Annual Expenses (₹)", min_value=0, step=10000, value=300000)
annual_savings = st.number_input("Annual Savings / Investments (₹)", min_value=0, step=10000, value=200000)
return_rate = st.number_input("Expected Annual Return on Investment (%)", min_value=0.0, max_value=30.0, step=0.1, value=8.0)
inflation_rate = st.number_input("Expected Annual Inflation Rate (%)", min_value=0.0, max_value=20.0, step=0.1, value=6.0)

st.header("🕰 Retirement Goals")

current_age = st.number_input("Your Current Age", min_value=18, max_value=80, value=30)
retirement_age = st.number_input("Age You Want to Retire", min_value=current_age + 1, max_value=80, value=60)
life_expectancy = st.number_input("Expected Lifespan", min_value=retirement_age + 1, max_value=100, value=85)
post_retirement_income = st.number_input("Expected Annual Income After Retirement (₹)", min_value=0, step=10000, value=500000)

# Calculations
years_to_retirement = retirement_age - current_age
years_post_retirement = life_expectancy - retirement_age
adjusted_income = post_retirement_income * ((1 + inflation_rate / 100) ** years_to_retirement)

def present_value_annuity(pmt, r, n):
    if r == 0:
        return pmt * n
    r /= 100
    return pmt * ((1 - (1 + r) ** -n) / r)

required_corpus = present_value_annuity(adjusted_income, return_rate - inflation_rate, years_post_retirement)

future_value = 0
annual_contribution = annual_savings
salary = annual_income

for year in range(years_to_retirement):
    future_value = (future_value + annual_contribution) * (1 + return_rate / 100)
    salary *= 1 + income_growth_rate / 100
    annual_contribution = salary - annual_expenses

def monthly_sip_needed(fv, rc, years, rate):
    r = rate / 100 / 12
    n = years * 12
    fv_gap = rc - fv
    if r == 0 or fv_gap <= 0:
        return 0
    return fv_gap * r / ((1 + r) ** n - 1)

monthly_saving_required = monthly_sip_needed(future_value, required_corpus, years_to_retirement, return_rate)

# Outputs
st.header("📊 Results")

st.success(f"🧓 You will need ₹{format_indian(int(required_corpus))} at age {retirement_age} to retire comfortably.")
st.info(f"📌 Based on current savings, you'll have ₹{format_indian(int(future_value))} by then.")
st.warning(f"💸 You need to save at least ₹{format_indian(int(monthly_saving_required))} per month starting today.")

st.header("💡 Recommendations")

if monthly_saving_required == 0:
    st.success("🎉 You are already on track for your retirement goals!")
else:
    st.markdown(f"""
    - 💰 **Increase your annual savings** by {int((monthly_saving_required*12 - annual_savings)/1000)*1000} ₹ per year.
    - 📈 Start investing early to benefit from compounding over time.
    - 🧾 Review expenses yearly to make space for investing more.
    - 🧠 Consider consulting a certified financial planner for more precise investment vehicles.
    """)

# Optional Explanation
with st.expander("🔍 How We Calculated This (Click to Learn More)"):
    st.markdown(f"""
    - **You have {years_to_retirement} years** until retirement and plan to live {years_post_retirement} years after retiring.
    - Your future income need of ₹{format_indian(int(post_retirement_income))} will be inflated to ₹{format_indian(int(adjusted_income))} annually by then.
    - The total retirement **corpus needed** to sustain that lifestyle = ₹{format_indian(int(required_corpus))}.
    - Based on your income, savings and returns, your investments will grow to ₹{format_indian(int(future_value))}.
    - If there's a shortfall, we compute the **monthly SIP (Systematic Investment Plan)** needed to bridge that gap.
    """)

st.caption("Note: Results are estimates and assume constant returns & inflation.")

import pandas as pd

def save_to_excel(required_corpus, future_value, monthly_saving_required, post_retirement_income, inflation_rate, return_rate, retirement_age):
    data = {
        "Retirement Age": [retirement_age],
        "Post-Retirement Income (₹)": [post_retirement_income],
        "Expected Inflation Rate (%)": [inflation_rate],
        "Expected Return on Investment (%)": [return_rate],
        "Total Corpus Needed (₹)": [required_corpus],
        "Expected Corpus at Retirement (₹)": [future_value],
        "Monthly Saving Needed (₹)": [monthly_saving_required]
    }
    df = pd.DataFrame(data)

    # Save to Excel
    excel_output_path = "retirement_plan.xlsx"
    df.to_excel(excel_output_path, index=False, engine="openpyxl")

    return excel_output_path

# Button to save Excel
if st.button("Save Results as Excel"):
    excel_file = save_to_excel(required_corpus, future_value, monthly_saving_required, post_retirement_income, inflation_rate, return_rate, retirement_age)
    st.success(f"Your retirement plan has been saved as Excel: {excel_file}")

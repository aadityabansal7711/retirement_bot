import streamlit as st
import math
import pandas as pd

# Indian comma formatter
def format_inr(num):
    s, *d = str(int(num))[::-1], []
    for i in range(len(s)):
        if i == 3 or (i > 3 and (i - 1) % 2 == 0):
            d.append(',')
        d.append(s[i])
    return ''.join(d[::-1])

st.set_page_config(page_title="Retirement Calculator", layout="centered")

st.title("🧮 Retirement Calculator")

st.markdown("Fill in the details below to find out how much you need to save for a secure retirement.")

# INPUTS
col1, col2 = st.columns(2)

with col1:
    annual_income = st.number_input("💼 Current Annual Income (₹)", min_value=0, step=10000, format="%d")
    income_growth = st.slider("📈 Expected Annual Income Growth (%)", 0.0, 15.0, 5.0, step=0.1)
    annual_expenses = st.number_input("🧾 Current Annual Expenses (₹)", min_value=0, step=10000, format="%d")
    current_savings = st.number_input("💰 Current Total Savings (₹)", min_value=0, step=10000, format="%d")

with col2:
    annual_investment = st.number_input("📥 Annual Investment/Savings (₹)", min_value=0, step=10000, format="%d")
    return_rate = st.slider("📊 Expected Annual Return (%)", 0.0, 15.0, 7.0, step=0.1)
    inflation_rate = st.slider("🔥 Expected Inflation Rate (%)", 0.0, 10.0, 6.0, step=0.1)
    current_age = st.slider("🎂 Your Current Age", 18, 70, 30)
    retirement_age = st.slider("🏖️ Retirement Age", current_age + 1, 80, 60)
    life_expectancy = st.slider("⚰️ Expected Lifespan", retirement_age + 1, 100, 85)

# CALCULATIONS
years_to_retire = retirement_age - current_age
years_in_retirement = life_expectancy - retirement_age

# Future expense adjusted for inflation
future_expense = annual_expenses * ((1 + inflation_rate / 100) ** years_to_retire)

# Total retirement corpus needed at retirement age (discounted sum of post-retirement expenses)
total_needed_at_retirement = sum([
    future_expense * ((1 + inflation_rate / 100) ** i) / ((1 + return_rate / 100) ** i)
    for i in range(years_in_retirement)
])

# Future value of current savings and annual investments
future_value_savings = current_savings * ((1 + return_rate / 100) ** years_to_retire)

future_investment_value = sum([
    annual_investment * ((1 + return_rate / 100) ** (years_to_retire - i))
    for i in range(years_to_retire)
])

total_available_at_retirement = future_value_savings + future_investment_value
gap = total_needed_at_retirement - total_available_at_retirement
gap = max(0, gap)

monthly_saving_required = 0
if gap > 0:
    r = (return_rate / 100) / 12
    n = years_to_retire * 12
    monthly_saving_required = gap * r / ((1 + r) ** n - 1)

# DISPLAY RESULTS
st.header("📌 Summary")
st.markdown(f"""
- 💸 You will need about **₹{format_inr(int(total_needed_at_retirement))}** at retirement to cover your expenses.
- ✅ You are projected to have **₹{format_inr(int(total_available_at_retirement))}** at retirement.
-  Deficit at retirement: **₹{format_inr(int(gap))}**
- 💡 You need to start saving **₹{format_inr(int(monthly_saving_required))} per month** more to bridge this gap.


if gap <= 0:
    st.success("🎉 You’re saving enough for retirement!")
else:
    st.warning("⚠️ You’re **not saving enough** for your retirement.")
    st.markdown(f"""
    -  Deficit at retirement: **₹{format_inr(gap)}**
    - 💡 You need to start saving **₹{format_inr(monthly_saving_required)} per month** more to bridge this gap.
    """)

with st.expander("🔍 Show Detailed Explanation"):
    st.markdown(f"""
    #### How this is calculated:
    - **Future Expenses**: Your current annual expenses of ₹{format_inr(annual_expenses)} are inflated at {inflation_rate}% for {years_to_retire} years.
    - **Total Needed**: We calculate the total of all retirement year expenses discounted back to retirement using a {return_rate}% return rate.
    - **Savings & Investment**: We project your current savings and yearly investment forward using compound growth over {years_to_retire} years.
    - **Gap**: If the available money is less than needed, we compute how much extra monthly saving you need to meet the shortfall.
    """)

# DOWNLOAD OPTION
df = pd.DataFrame({
    "Label": ["Total Needed at Retirement", "Projected Savings", "Gap", "Extra Monthly Saving Required"],
    "Amount (₹)": [
        int(total_needed_at_retirement),
        int(total_available_at_retirement),
        int(gap),
        int(monthly_saving_required)
    ]
})

st.download_button("📤 Download Summary as Excel", df.to_csv(index=False), file_name="retirement_summary.csv")

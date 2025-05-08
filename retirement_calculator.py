import streamlit as st
import math

# Function to format numbers with commas (Indian Number System)
def format_inr(number):
    # Convert to string, remove decimals, reverse string, and add commas for every 2 digits
    return '{:,.0f}'.format(number)[::-1].replace(',', ' ', 1)[::-1]

# Function to calculate retirement details
def calculate_retirement(income, income_increase, expenses, savings, rate_of_return, inflation_rate, retirement_age, life_expectancy):
    years_until_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age

    # Calculate future expenses at the time of retirement
    future_expenses = expenses * math.pow(1 + inflation_rate, years_until_retirement)

    # Calculate the amount needed at retirement to sustain expenses during retirement
    total_needed_at_retirement = future_expenses * (1 - math.pow(1 + rate_of_return, -years_in_retirement)) / rate_of_return

    # Calculate the current savings projected at retirement
    future_savings = savings * math.pow(1 + rate_of_return, years_until_retirement)

    # Calculate if the total savings at retirement will be sufficient
    gap = total_needed_at_retirement - future_savings
    monthly_saving_required = gap / (years_until_retirement * 12)

    # Displaying results with explanations
    st.markdown(f"- 💸 You will need about **₹{format_inr(total_needed_at_retirement)}** at retirement to cover your expenses.")
    st.markdown(f"- ✅ You are projected to have **₹{format_inr(future_savings)}** at retirement.")
    st.markdown(f"- ❌ Deficit at retirement: **₹{format_inr(gap)}**")
    st.markdown(f"- 💡 You need to start saving **₹{format_inr(monthly_saving_required)} per month** more to bridge this gap.")

    # Explanation of calculations
    if gap > 0:
        st.markdown("### Explanation of the calculations:")
        st.markdown("""
        - The amount you need at retirement is calculated by factoring in your future expenses 
        adjusted for inflation and the number of years you expect to live after retirement.
        - The total amount needed to cover your expenses during retirement is based on the 
        expected rate of return on your investments and the number of years in retirement.
        - Your current savings will grow with the rate of return, and we calculate whether 
        this will be enough to meet the expenses.
        - If there's a gap, we show the monthly savings required to reach the amount needed.
        """)

# Streamlit interface
st.title("Retirement Calculator")

# Inputs
current_age = st.number_input("Enter your current age", min_value=18, max_value=120, value=30)
income = st.number_input("Enter your current annual income (₹)", min_value=100000, value=500000)
income_increase = st.number_input("Expected annual income increase (%)", min_value=0, value=5)
expenses = st.number_input("Enter your annual expenses (₹)", min_value=100000, value=200000)
savings = st.number_input("Enter your current savings (₹)", min_value=0, value=500000)
rate_of_return = st.number_input("Expected annual rate of return (%)", min_value=1, max_value=50, value=7) / 100
inflation_rate = st.number_input("Expected inflation rate (%)", min_value=1, max_value=50, value=5) / 100
retirement_age = st.number_input("At what age would you like to retire?", min_value=current_age + 1, max_value=120, value=60)
life_expectancy = st.number_input("What is your expected lifespan?", min_value=current_age + 1, max_value=120, value=85)

# Run calculation when button is pressed
if st.button("Calculate Retirement Plan"):
    calculate_retirement(income, income_increase, expenses, savings, rate_of_return, inflation_rate, retirement_age, life_expectancy)

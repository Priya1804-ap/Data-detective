import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="Data Detective",
    page_icon="🔎",
    layout="wide"
)

# Load dataset
df = pd.read_csv("sales_data.csv")

# Title
st.title("🔎 DATA DETECTIVE")
st.subheader("CASE 001: Mystery of Falling Sales")

st.write(
    "Welcome Detective! 🕵️ Analyze the sales data and solve the mystery."
)

# Sidebar
st.sidebar.header("🎯 Detective Panel")

st.sidebar.write(f"Total Orders: **{len(df)}**")
st.sidebar.write(f"Total Sales: **₹{df['Sales'].sum():,.0f}**")
st.sidebar.write(f"Total Profit: **₹{df['Profit'].sum():,.0f}**")

# Dashboard
st.header("📊 Sales Investigation")

col1, col2 = st.columns(2)

with col1:
    product_sales = df.groupby("Product")["Sales"].sum().sort_values()

    fig1 = px.bar(
        product_sales,
        title="Sales by Product",
        labels={"value": "Sales", "Product": "Product"}
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    monthly_sales = df.groupby("Month")["Sales"].sum()

    fig2 = px.line(
        monthly_sales,
        title="📉 Monthly Sales Trend",
        markers=True,
        labels={"value": "Sales", "Month": "Month"}
    )

    st.plotly_chart(fig2, use_container_width=True)

# Case clues
st.header("🕵️ Solve the Case")

# Clue 1
st.subheader("🔐 Clue 1")

answer1 = st.radio(
    "Which product has the LOWEST overall sales?",
    ["Mobile", "Keyboard", "Headphones", "Laptop", "Mouse"],
    key="clue1"
)

if st.button("Submit Clue 1"):
    if answer1 == "Laptop":
        st.success("✅ Correct! Laptop has the lowest overall sales.")
        st.session_state.clue1_solved = True
    else:
        st.error("❌ Wrong! Check the Sales by Product chart.")

# Clue 2
if st.session_state.get("clue1_solved", False):

    st.subheader("🔐 Clue 2")

    answer2 = st.radio(
        "In which city are Laptop sales the lowest?",
        ["Mumbai", "Delhi", "Lucknow", "Jaipur", "Bangalore"],
        key="clue2"
    )

    if st.button("Submit Clue 2"):
        if answer2 == "Delhi":
            st.success("✅ Correct! Delhi has the lowest Laptop sales.")
            st.session_state.clue2_solved = True
        else:
            st.error("❌ Wrong! Investigate the city-wise data.")

# Clue 3
if st.session_state.get("clue2_solved", False):

    st.subheader("🔐 Clue 3")

    answer3 = st.radio(
        "What happened to Laptop orders in Delhi?",
        [
            "Orders increased",
            "Orders stayed the same",
            "Orders decreased",
            "There were no orders"
        ],
        key="clue3"
    )

    if st.button("Submit Clue 3"):
        if answer3 == "Orders decreased":
            st.success("🎉 Correct! Laptop orders decreased.")
            st.session_state.case_solved = True
        else:
            st.error("❌ Not quite. Look at the trend carefully.")

# Final result
if st.session_state.get("case_solved", False):

    st.balloons()

    st.success("🎉 CASE SOLVED!")

    st.write("### 🏆 Detective Report")

    st.write("""
    **Finding 1:** Laptop had the lowest overall sales.

    **Finding 2:** Delhi had the lowest Laptop sales.

    **Finding 3:** Laptop orders decreased.

    **Conclusion:** The major sales problem was the decline in Laptop orders.
    """)

    st.metric("XP Earned", "300 XP")

    st.success("🔓 Case 001 completed!")
    # CASE 002
if st.session_state.get("case_solved", False):

    st.header("🕵️ CASE 002: The City Sales Mystery")

    st.write(
        "Great work Detective! 🔓 A new case has been unlocked."
    )

    # Calculate city sales
    city_sales = df.groupby("City")["Sales"].sum().sort_values(ascending=False)

    highest_city = city_sales.index[0]

    st.subheader("🔐 Clue 1")

    city_options = list(df["City"].unique())

    answer_city = st.radio(
        "Which city has the HIGHEST overall sales?",
        city_options,
        key="case2_city"
    )

    if st.button("Submit Case 002", key="submit_case2"):

        if answer_city == highest_city:

            st.success(
                f"✅ Correct! {highest_city} has the highest overall sales."
            )

            st.session_state.case2_solved = True

        else:

            st.error(
                "❌ Wrong! Check the city-wise sales data carefully."
            )

    # City Sales Chart
    st.subheader("📊 City Sales Investigation")

    fig3 = px.bar(
        city_sales,
        title="Total Sales by City",
        labels={
            "value": "Sales",
            "City": "City"
        }
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# Case 002 completed
if st.session_state.get("case2_solved", False):

    st.success("🎉 CASE 002 SOLVED!")

    st.metric(
        "⭐ XP Earned",
        "500 XP"
    )

    st.write(
        "🔓 You have successfully completed Case 002!"
    )
    # ==============================
# CASE 003 - ML CHALLENGE
# ==============================

if st.session_state.get("case2_solved", False):

    st.header("🤖 CASE 003: Predict the Future")

    st.write(
        "The mystery continues! Use the sales data to predict future sales."
    )

    st.subheader("🎯 Make Your Prediction")

    col1, col2 = st.columns(2)

    with col1:
        selected_product = st.selectbox(
            "📦 Select Product",
            sorted(df["Product"].unique())
        )

        selected_city = st.selectbox(
            "🏙️ Select City",
            sorted(df["City"].unique())
        )

    with col2:
        selected_quantity = st.number_input(
            "📦 Expected Quantity",
            min_value=1,
            max_value=100,
            value=10
        )

        selected_discount = st.number_input(
            "🏷️ Discount (%)",
            min_value=0,
            max_value=50,
            value=10
        )

    if st.button("🔮 Predict Sales"):

        # Historical average sales
        filtered_data = df[
            (df["Product"] == selected_product) &
            (df["City"] == selected_city)
        ]

        if len(filtered_data) > 0:

            avg_price = filtered_data["Price"].mean()

            predicted_sales = (
                selected_quantity
                * avg_price
                * (1 - selected_discount / 100)
            )

            st.success("🔮 Prediction Complete!")

            st.metric(
                "💰 Predicted Sales",
                f"₹{predicted_sales:,.0f}"
            )

            st.info(
                "This prediction is based on historical product, "
                "city, price, quantity and discount patterns."
            )

            st.session_state.case3_solved = True

        else:

            st.warning(
                "⚠️ Not enough historical data for this combination."
            )


# Case 003 completion
if st.session_state.get("case3_solved", False):

    st.success("🎉 CASE 003 SOLVED!")

    st.metric("⭐ XP Earned", "750 XP")

    st.write(
        "🧠 Excellent Detective! You successfully used "
        "data to predict future sales."
    )

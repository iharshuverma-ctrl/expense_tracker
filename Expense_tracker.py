
import streamlit as st
import pandas as pd
import json
import os
from datetime import date

FILE_NAME = "expenses.json"

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

st.title("💰 Personal Expense Tracker")
st.write("Track your daily expenses easily.")

with st.form("expense_form"):
    st.subheader("Add New Expense")

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    title = st.text_input(
        "Expense Name",
        placeholder="e.g. Lunch"
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping",
         "Education", "Bills", "Other"]
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if title.strip() and amount > 0:
            expense = {
                "Date": str(expense_date),
                "Name": title.strip(),
                "Amount": amount,
                "Category": category
            }

            st.session_state.expenses.append(expense)
            save_expenses(st.session_state.expenses)
            st.success("Expense added successfully!")
        else:
            st.error("Enter a name and an amount greater than zero.")

st.divider()
st.subheader("Expense Summary")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    total_expense = df["Amount"].sum()
    total_entries = len(df)
    average_expense = total_expense / total_entries

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Spending", f"₹{total_expense:,.2f}")
    col2.metric("Total Entries", total_entries)
    col3.metric("Average Expense", f"₹{average_expense:,.2f}")

    st.subheader("Expense History")

    categories = ["All"] + sorted(df["Category"].unique().tolist())
    selected_category = st.selectbox(
        "Filter by Category",
        categories
    )

    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]

    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("Category-wise Spending")

    category_totals = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_totals)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Expenses as CSV",
        data=csv_data,
        file_name="expenses.csv",
        mime="text/csv"
    )

    if st.button("Delete All Expenses"):
        st.session_state.expenses = []
        save_expenses([])
        st.rerun()

else:
    st.info("No expenses yet. Add your first expense above.")

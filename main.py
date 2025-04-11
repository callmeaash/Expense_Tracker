import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os
from plotLib import plotGraph


dataset_location = 'Personal_Finance_Dataset.csv'
absolute_path_dataset = os.path.abspath(dataset_location)


def fillNAN(df: pd.DataFrame):
    df.dropna()


df = pd.read_csv(absolute_path_dataset, index_col=0)
df.index = pd.to_datetime(df.index).date
fillNAN(df)

def minMaxDate(df: pd.DataFrame, min_date=False, max_date=False):
    if min_date:
        return df.index.min()
    return df.index.max()


min_date = minMaxDate(df, min_date=True)
max_date = minMaxDate(df, max_date=True)

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.markdown(
        """
        <style>
        .st-emotion-cache-1wda3go {
            margin-top: -80px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title("Expense Tracker")

tabs = st.tabs(["Individual Month", "Compare Months"])
with tabs[0]:
    with st.sidebar:
        st.header("Select Timeframe")
        start_date = st.date_input(label="Start Date", min_value=min_date, max_value=max_date, value=(max_date - pd.DateOffset(months=1)))
        end_date = st.date_input(label="End Date", min_value=min_date, max_value=max_date, value=max_date)

        total_days = (end_date - start_date).days
        st.write("Total Days: ", total_days)

        st.markdown("---")
        st.header("Compare Months")
        st.write("Month First")
        month_first_start = st.date_input(label="Start Date (Month1 -> Start)", min_value=min_date, max_value=max_date, value=(max_date - pd.DateOffset(months=2)))
        month_first_end = st.date_input(label="End Date (Month1 -> End)", min_value=min_date, max_value=max_date, value=(max_date - pd.DateOffset(months=1)))

        st.write("Month Second")
        month_second_start = st.date_input(label="Start Date (Month2 -> Start)", min_value=min_date, max_value=max_date, value=(max_date - pd.DateOffset(months=1)))
        month_second_end = st.date_input(label="End Date (Month2 -> End)", min_value=min_date, max_value=max_date, value=max_date)

    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]


    income_expense_series = filtered_df.groupby('Type')['Amount'].sum()

    fig1 = go.Figure()
    plotGraph(fig=fig1, graph="bar", df=income_expense_series, title="Income vs Expenses")
    st.plotly_chart(fig1, use_container_width=True)

    filtered_df['Income'] = filtered_df['Amount'].where(filtered_df['Type'] == 'Income').cumsum().ffill().fillna(0)
    filtered_df['Expense'] = filtered_df['Amount'].where(filtered_df['Type'] == 'Expense').cumsum().ffill().fillna(0)

    fig4 = go.Figure()
    plotGraph(fig=fig4, graph="line", df=filtered_df['Income'], title=None)
    plotGraph(fig=fig4, graph="line", df=filtered_df['Expense'], title="Cumulative Income and Expense")
    st.plotly_chart(fig4, use_container_width=True)

    col = st.columns(2)
    with col[0]:
        income_series = filtered_df[filtered_df['Type'] == 'Income'].groupby('Category')['Amount'].sum()
        fig2 = go.Figure()
        plotGraph(fig=fig2, graph="pie", df=income_series, title="Income Sources")
        st.plotly_chart(fig2, use_container_width=True)

    with col[1]:
        expenses_series = filtered_df[filtered_df['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
        fig3 = go.Figure()
        plotGraph(fig=fig3, graph="pie", df=expenses_series, title="Expenses Categories")
        st.plotly_chart(fig3, use_container_width=True)

    highest_expense_row = filtered_df[filtered_df['Type'] == 'Expense'].nlargest(1, 'Amount')
    most_spend_category = highest_expense_row['Category'].iloc[0] if not highest_expense_row.empty else 'No Expense Found'

    highest_income_row = filtered_df[filtered_df['Type'] == 'Income'].nlargest(1, 'Amount')
    most_earned_category = highest_income_row['Category'].iloc[0] if not highest_income_row.empty else 'No Income Found'


    st.subheader("KPI's")
    metrics_df = pd.DataFrame({
        'Key': ['Income', 'Expenses', 'Most Spend on', 'Highest Income Source'],
        'Value': [
            income_expense_series.get('Income', 0),
            income_expense_series.get('Expense', 0),
            most_spend_category,
            most_earned_category
        ]
    })
    metrics_df.set_index('Key', inplace=True)
    st.dataframe(metrics_df, width=300)

with tabs[1]:
    filtered_month_first = df[(df.index >= month_first_start) & (df.index < month_first_end)]
    filtered_month_second = df[(df.index >= month_second_start) & (df.index < month_second_end)]
    type = ['Income', 'Expense']
    month1_income_expense = filtered_month_first.groupby('Type')['Amount'].sum()
    month2_income_expense = filtered_month_second.groupby('Type')['Amount'].sum()
    fig5 = go.Figure(data=[
        go.Bar(name="Month1", x=type, y=month1_income_expense.values),
        go.Bar(name="Month2", x=type, y=month2_income_expense)
    ])
    fig5.update_layout(
        barmode='stack',
        title={
            "text": "Income and Expense of Two Months",
            "x": 0.5,
            "xanchor": "center"
        }
    )
    st.plotly_chart(fig5, use_container_width=True)

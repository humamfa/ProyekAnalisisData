import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_daily_users_df(df):
    daily_users_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_users_df = daily_users_df.reset_index()
    daily_users_df.rename(columns={
        "dteday": "date",
        "cnt": "total_users"
    }, inplace=True)

    return daily_users_df

def create_users_by_workdays_df(df):
    users_by_workdays_df = df.groupby(by="workingday").cnt.sum().reset_index()
    users_by_workdays_df.rename(columns={
        "cnt": "total_users"
    }, inplace=True)

    return users_by_workdays_df

day_df = pd.read_csv("data/day.csv")

day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

daily_users_df = create_daily_users_df(main_df)
users_by_workdays_df = create_users_by_workdays_df(main_df)

st.header('Bike Sharing Dashboard')
st.subheader('Daily Users')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_users_df["date"],
    daily_users_df["total_users"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Users by Working day')

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
        y="total_users", 
        x="workingday",
        data=users_by_workdays_df.sort_values(by="total_users", ascending=False),
        palette='Blues',
        ax=ax
    )

ax.set_ylabel("Number of users")
ax.set_xlabel("Working day")
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.table(users_by_workdays_df)

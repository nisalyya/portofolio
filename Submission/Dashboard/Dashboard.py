import os
import pandas as pd

# Mendapatkan direktori script saat ini (direktori utama proyek)
project_directory = os.path.dirname(os.path.abspath(__file__))

# Membuat absolute path untuk file data
absolute_path = os.path.join(project_directory, 'Main_data.csv')
all_df = pd.read_csv(absolute_path)
print(all_df.head())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#datetime
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

import streamlit as st

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image(f"https://drive.google.com/uc?id=1A05wrCKJ8IEbjyC0rjx0QAcj6N64snJW", width=250)

    # Tengahkan gambar dengan CSS styling
    st.markdown(
        """
        <style>
            div.stImage img {
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.header('Bike Sharing Dashboard :bike:')

st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)

with col1:
    casual_customers = all_df["casual"].sum()
    st.metric("Casual Customers", value=casual_customers)

with col2:
    registered_customers = all_df["registered"].sum()
    st.metric("Registered Customers", value=registered_customers)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    all_df["dteday"],
    all_df["cnt"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

#total cust per season----------------------------------------------
st.subheader("Total Rentals Each Season")

# Mendefinisikan season_mapping langsung di sini
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
all_df["season_description"] = all_df["season"].map(season_mapping)

fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x="season_description", y="cnt", data=all_df.groupby("season_description").agg({"cnt": "sum"}), palette="viridis")
ax.set_xlabel("Season", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
ax.set_title(None, fontsize=20)

for p in ax.patches:
    ax.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=12)

st.pyplot(fig)

#piechart per season-------------------------------------------------
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
all_df["season_description"] = all_df["season"].replace(season_mapping)

st.subheader("Rental Counts Each Season")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(9, 8))
    ax1.pie(all_df.groupby("season_description")["casual"].sum(), labels=all_df["season_description"].unique(), autopct='%1.1f%%', startangle=90, colors=sns.color_palette("muted"))
    ax1.set_title("Casual Rentals Each Season", fontsize=15)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(9, 8))
    ax2.pie(all_df.groupby("season_description")["registered"].sum(), labels=all_df["season_description"].unique(), autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax2.set_title("Registered Rentals Each Season", fontsize=15)
    st.pyplot(fig2)

#Barchart month----------------------------------------------------------------
month_mapping = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'June', 7: 'July', 8:'Agst', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
all_df['mnth'] = all_df['mnth'].map(month_mapping)
st.subheader('Rental counts each month')
fig, ax = plt.subplots()
ax.bar(all_df['mnth'], all_df['cnt'])
ax.set_ylabel('Costumers')
ax.set_xlabel(None)
st.pyplot(fig)

#barchart day------------------------------------------------------------------
st.subheader('Rental counts based on working day')

fig, ax = plt.subplots()
ax.hist(all_df[all_df['workingday'] == 1]['cnt'], alpha=0.5, label='Working Day', bins=10)
ax.hist(all_df[all_df['workingday'] == 0]['cnt'], alpha=0.5, label='Non-Working Day', bins=10)

ax.set_xlabel('Count')
ax.set_ylabel('Frequency')
ax.legend()

st.pyplot(fig)

#piechart day---------------------------------------------------------------------
st.subheader('Percentage of rental amount on weekdays and holidays')
jumlah_penyewa_hari_libur = all_df[all_df['workingday'] == 0]['cnt'].sum()
jumlah_penyewa_hari_kerja = all_df[all_df['workingday'] == 1]['cnt'].sum()

fig, ax = plt.subplots()
ax.pie([jumlah_penyewa_hari_libur, jumlah_penyewa_hari_kerja], labels=['Holiday', 'Workingday'], autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])

st.pyplot(fig)







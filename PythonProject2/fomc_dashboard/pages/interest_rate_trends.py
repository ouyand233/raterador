import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
import plotly.express as px

# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions'

# Send a GET request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table(s) containing the data
tables = soup.find_all('table', {'class': 'wikitable'})

# Ensure at least one table is found
if len(tables) == 0:
    st.error("No tables found on the page.")
    st.stop()

# Parse the first table manually
table = tables[0]
rows = table.find_all('tr')

# Extract headers
headers = [header.text.strip() for header in rows[0].find_all('th')]

# Extract rows
data = []
for row in rows[1:]:
    cells = row.find_all(['td', 'th'])
    data.append([cell.text.strip() for cell in cells])

# Create a DataFrame
df = pd.DataFrame(data, columns=headers)

# Display first few rows for debugging
print(df.head())

# Data Cleaning
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Remove rows with invalid dates
else:
    st.error("The 'Date' column was not found in the table. Please check the table structure.")
    st.stop()

# Ensure numeric columns are parsed correctly
if 'Fed Funds Rate' in df.columns:
    df['Fed Funds Rate'] = pd.to_numeric(df['Fed Funds Rate'], errors='coerce')
else:
    st.warning("'Fed Funds Rate' column is missing or invalid. Visualization will be skipped.")

# Streamlit App
st.title('Historical Federal Funds Rate Visualization')

# Interactive Date Selection
start_date = st.date_input('Start date', value=df['Date'].min().date())
end_date = st.date_input('End date', value=df['Date'].max().date())

if start_date > end_date:
    st.error("Start date must be earlier than end date.")
else:
    filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    if filtered_df.empty:
        st.warning("No data available for the selected date range.")
    else:
        fig = px.line(
            filtered_df,
            x='Date',
            y='Fed Funds Rate',
            title='Federal Funds Rate Over Time',
            labels={'Fed Funds Rate': 'Fed Funds Rate (%)'},
        )
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Fed Funds Rate (%)',
            template='plotly_white'
        )
        st.plotly_chart(fig)

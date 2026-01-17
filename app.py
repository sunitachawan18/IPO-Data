import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURATION & STYLE ---
st.set_page_config(page_title="India IPO Tracker", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE DATA SCRAPER ---
# We are creating a "Robot" to fetch data from a popular IPO site
@st.cache_data(ttl=3600) # This saves data for 1 hour so the site stays fast
def fetch_ipo_data():
    # Note: We are using a popular source for Indian IPOs
    url = "https://www.investorgain.com/report/live-ipo-gmp/331/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table in the website
        table = soup.find('table', {'class': 'table'})
        df = pd.read_html(str(table))[0]
        
        # Cleaning the data slightly
        df = df.dropna(subset=['IPO'])
        return df
    except Exception as e:
        return pd.DataFrame()

# --- THE WEBSITE INTERFACE ---
st.title("🇮🇳 Indian IPO Tracker & GMP")
st.write(f"**Today's Date:** {datetime.now().strftime('%d %B, %Y')}")

with st.spinner('Loading latest IPO data...'):
    data = fetch_ipo_data()

if not data.empty:
    # Creating Tabs for organization
    tab1, tab2 = st.tabs(["🔥 Ongoing & Upcoming", "🔔 Set Notifications"])

    with tab1:
        st.subheader("Live Market Status")
        
        # We display the data table nicely
        # Columns usually: IPO, Price, GMP, Kostak, Subject to, Expected Listing
        st.dataframe(data, use_container_width=True, hide_index=True)
        
        st.info("💡 **Tip:** GMP (Grey Market Premium) shows what the market thinks the profit will be before the stock officially starts trading.")

    with tab2:
        st.subheader("Get Alerts")
        st.write("Enter your details to get notified when an IPO opens or closes.")
        
        email = st.text_input("Your Email Address")
        selected_ipo = st.selectbox("Select IPO to track", data['IPO'].unique())
        
        if st.button("Register for Alerts"):
            if email:
                st.success(f"Successfully registered! We will email alerts for **{selected_ipo}** to {email}.")
                st.balloons()
            else:
                st.error("Please enter a valid email address.")

else:
    st.error("Wait! The robot couldn't find the data. The source website might be down for maintenance.")

# --- FOOTER ---
st.divider()
st.caption("Disclaimer: GMP is an unofficial market estimate and can change rapidly. Always do your own research before investing.")
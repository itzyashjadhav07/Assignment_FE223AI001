import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("startup_cleaned.csv")
st.set_page_config(layout='wide', page_title='Startup Analysis')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("FFE23AI001_Yash Jadhav")
def load_startup_details(startup):
    st.title(startup)
    st.subheader('Funded By')
    funded_by_df = df[df['startup'] == startup][['investors', 'amount', 'date']].reset_index(drop=True)
    st.dataframe(funded_by_df)


def load_investor_details(investor):
    st.title(investor)
    st.subheader('Most Recent Investments')

    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Convert 'amount' column to numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    recent_investment_df = df[df['investors'].str.contains(investor, na=False)].nlargest(5, 'date')
    st.dataframe(recent_investment_df[['date', 'startup', 'amount', 'vertical', 'city', 'round']])

    st.subheader('Maximum Investment')
    max_investment_df = df[df['investors'].str.contains(investor, na=False)]
    max_investment = max_investment_df['amount'].max()
    st.write(max_investment)

    st.subheader('Biggest Investment')
    biggest_investment_df = df[df['investors'].str.contains(investor, na=False)].nlargest(5, 'amount')
    plt.figure(figsize=(10, 6))
    plt.bar(biggest_investment_df['startup'], biggest_investment_df['amount'])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Startup')
    plt.ylabel('Amount')
    plt.title('Biggest Investments')
    st.pyplot()

    st.subheader('Sectors Invested In')
    sector_df = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
    plt.figure(figsize=(8, 6))
    sector_df.plot(kind='pie', autopct='%1.1f%%')
    st.pyplot()

    st.subheader('City')
    city_df = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
    plt.figure(figsize=(8, 6))
    city_df.plot(kind='pie', autopct='%1.1f%%')
    st.pyplot()

    # Investment trend over time
    st.subheader('Investment Trend Over Time')
    investment_over_time = df[df['investors'].str.contains(investor, na=False)].groupby('date')['amount'].sum()
    plt.figure(figsize=(12, 6))
    investment_over_time.plot()
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Investment Trend Over Time')
    st.pyplot()

    # Investment by rounds
    st.subheader('Investment by Rounds')
    investment_by_rounds = df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()
    plt.figure(figsize=(8, 6))
    investment_by_rounds.plot(kind='bar')
    plt.xlabel('Round')
    plt.ylabel('Amount')
    plt.title('Investment by Rounds')
    st.pyplot()

    # Yearly investment
    st.subheader('Yearly Investment')
    df['year'] = df['date'].dt.year
    yearly_investment = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
    plt.figure(figsize=(10, 6))
    yearly_investment.plot(kind='bar')
    plt.xlabel('Year')
    plt.ylabel('Amount')
    plt.title('Yearly Investment')
    st.pyplot()


def overall():
    st.title('Overall Analysis')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df.dropna(subset=['amount'], inplace=True)  # Drop rows with NaN values in the 'amount' column

    total = round(df['amount'].sum())
    max_f = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_f = df.groupby('startup')['amount'].sum().mean()
    num_start = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total', str(total) + 'Cr')

    with col2:
        st.metric('Max', str(max_f) + 'Cr')

    with col3:
        st.metric('Average', str(round(avg_f)) + 'Cr')

    with col4:
        st.metric('Funded Startups', str(num_start) + 'Cr')


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    overall()

elif option == 'Startup':
    st.title("Startup Analysis")
    selected_startup = st.sidebar.selectbox('Select One', df['startup'].unique().tolist())
    btn1 = st.sidebar.button('Find Startup Details')

    if btn1:
        load_startup_details(selected_startup)

else:
    st.title('Investor')
    selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')

    if btn2:
        load_investor_details(selected_investor)

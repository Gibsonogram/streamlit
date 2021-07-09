from matplotlib.pyplot import title
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import altair as alt

st.set_page_config(layout="wide",
                   initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                   page_title="I am a great investor")


big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
header = st.beta_container()
firstly = st.beta_container()
secondly = st.beta_container()
analysis = st.beta_container()
about = st.beta_container()

st.markdown(
    f"""
    <style>
        .reportview-container .main .block-container{{
            padding-top: {5}px;
            padding-bottom: {0}rem;
        }}
        h1{{
            font-family: "Comic Sans MS", "Comic Sans", cursive;
            padding-top: 0px;
        }}
        .header{{
            position: relative;
            text-align: center;
        }}
        .centered {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}
    </style>
""",
    unsafe_allow_html=True)
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

header_image = Image.open("images/school_athens.png")
prof_pic = Image.open("images/prof_pic2.png")
date = datetime.now().strftime('%m/%d/%y')

with header:
    st.image(header_image)
    st.markdown(f"""
        <div class = "header">
            <h1>
                I am a great investor
            </h1>
        </div>
        """, unsafe_allow_html=True)

#I'm gonna want this date column for stuff
bt_date = big_tuna.pop('date_hour')
big_tuna['date_hour'] = bt_date

col1_1, col1_2 = st.beta_columns((7,6))
with firstly:
    st.header("A final update on the project")
    with col1_1:
        p1 = """This site is getting a final update. 
        It will remain static after today, however, analysis on the results are available below."""

        results = """After months of using this bots advice intermittently, growing angry, then weary, I have gathered enough results to stop the experiment. 
        I am however going to do a rigorous analysis on price history vs r/wallstreetbets mentions. 
        I will be showing just how correlated these variables are, and whether or not this strategy is truly viable. 
        Here is a link to the new site, where the data from this project has been moved, and analysis continues:"""

        about_data = """The data obtained for this project is from a simple web scraper. Using the python reddit api, I scraped wsb for mentions of stocks and general sentiment. 
        The bot was run roughly once a day, (N=50) toward the end of the Nasdaq trading period. The stock data was obtained with yahoo finance in the form of daily closes. 
        The following analyses were done after the bot had collected data points from 4 March, 21 -- 12 July, 21."""

        col1_1.subheader(date)
        st.write(p1)
        st.subheader("Results")
        st.write(results)
        st.subheader('About the data')
        st.write(about_data)
        link = '[Project repository](https://github.com/Gibsonogram/streamlit)'
        st.markdown(link, unsafe_allow_html=True) 

    with col1_2:
        # most mentioned over the course of proj
        big_tun = big_tuna.drop('date_hour', axis=1)

        avg_arr = []
        for col in big_tun:
            col_sum = 0
            for item in big_tun[col]:
                col_sum += item
            avg = round(col_sum / len(big_tun),2)
            avg_arr.append([avg, col])
        
        most_mentioned = [[i,j] for i,j in avg_arr if i > 3.5]
        most_mentioned = pd.DataFrame(most_mentioned)
        most_mentioned.columns = ['mentions', 'stock']
        
        st.markdown(f"""
        <div class = "header">
            <h3>
                Average mentions per day
            </h3>
        </div>
        """, unsafe_allow_html=True)

        avg_mentions_chart = alt.Chart(most_mentioned).mark_bar(
            cornerRadiusTopLeft = 5,
            cornerRadiusTopRight= 5,
            color='6fb1ce').encode(
                x = 'stock',
                y = 'mentions').properties(height = 500)

        # @st.cache(suppress_st_warning=True)
        def chart_current():
            st.altair_chart(avg_mentions_chart, use_container_width=True)
        chart_current()

col2_1, col2_2 = st.beta_columns((1,6))
with secondly:
    top_5 = big_tuna.iloc[:,:5]
    top_5_10 = big_tuna.iloc[:,5:10]
    with col2_1:
        bt_cols = list(big_tuna.columns)
        bt_cols.insert(0, 'top 6-10')
        bt_cols.insert(0, 'top 1-5')
        selector = st.selectbox('view history of (you can type):', options=bt_cols)

    with col2_2:
        st.markdown("<h3 style='text-align: center; color: black;'>History</h3>", unsafe_allow_html=True)
        if selector == 'top 1-5':
            top_5['date'] = bt_date
            top_5 = top_5.melt('date', var_name='ticker', value_name='mentions')
            chart_data = top_5
        elif selector == 'top 6-10':
            top_5_10['date'] = bt_date
            top_5_10 = top_5_10.melt('date', var_name='ticker', value_name='mentions')
            chart_data = top_5_10
        else:
            ind_hist = pd.DataFrame()
            ind_hist['mentions'] = big_tuna[selector]
            ind_hist['date'] = bt_date
            ind_hist['ticker'] = selector
            chart_data = ind_hist
        
        interactive_chart = alt.Chart(chart_data).mark_line().encode(
            x = alt.X('date:T',
                      scale=alt.Scale(domain = [big_tuna.iat[30-len(big_tuna),-1], big_tuna.iat[-1,-1]])),
            y = 'mentions:Q',
            color = 'ticker:N'
            ).interactive(bind_y=False)

        st.altair_chart(interactive_chart, use_container_width=True)


col3_1, col3_2, col3_3 = st.beta_columns((1,1,1))
with analysis:
    with col3_1:
        st.subheader('high mentions')
    with col3_2:
        st.write('Results')
        st.subheader("high mentions (left)")
        st.subheader("low mentions (right)")
    with col3_3:
        st.subheader('low mention stocks')
    





col4_1 = st.beta_container()

with about:
    with col4_1:
        col4_1.subheader("About the project")
        st.write("""I started this project shortly after joining r/wallstreetbets, a community on reddit devoted to some of the worst trading tactics imaginable.
        With an applied math degree and too much time on my hands, I decided to learn a bit of web developent. I quickly got in way over my head. 
        While the idea for this site began as a blog-style trading experiment using a web-scraper, I couldn't resist making it about data science.
        I began stockpiling data after the gamestop shorting event in January-February 2021. I watched as my investment account soared to heights it had never seen.
        Then I watched as it slowly crumbled and fell back to earth. Then I watched as it sank below the earth and turned up somewhere in hell. 
        There is nothing left to do now but lose the rest of it to insane plays.
        """)
        st.write("""So I made a bot that tells me the most mentioned stocks on r/wallstreetbets and I will only take advice from there. 
        Feel free to check back and watch as my account plummets or soars. 
        This is not financial advice, I just wanted to see what would happen if I listened to the worst investors on the internet.
        """)
        st.write("""NOTE: This site is no longer being updated, the project continues here:
        """)
        st.markdown(link, unsafe_allow_html=True)

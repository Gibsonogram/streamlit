import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import altair as alt
import base64
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

st.set_page_config(layout="wide",
                   initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                   page_title="I am a great investor")


# params
big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
gme = pd.read_csv("correlation_dataframes/gme_data.csv")
nvda = pd.read_csv("correlation_dataframes/nvda_data.csv")

#I'm gonna want this date column for stuff
bt_date = big_tuna.pop('date_hour')
big_tuna['date_hour'] = bt_date

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
        #prof {{
            height: 200px;
            width: 200px;
            border-radius: 100px;
            padding: 30px; 
        }}
    </style>
""", unsafe_allow_html=True)


# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
header_image = Image.open("images/school_athens.png")
date = datetime.now().strftime('%m/%d/%y')

header = st.beta_container()
with header:
    st.image(header_image)
    st.markdown(f"""
        <div class = "header">
            <h1>
                I am a great investor
            </h1>
        </div>
        """, unsafe_allow_html=True)


firstly = st.beta_container()
col1_1, col1_2 = st.beta_columns((7,6))
with firstly:
    st.header("Final updates on the project")
    with col1_1:
        link = '[Project repository](https://github.com/Gibsonogram/streamlit)'
        results = f"""The question I set out to answer was this: 
        Is there a correlation between the movement of a stock, and the times it was mentioned on r/wallstreetbets leading up to that?
        After months of gathering data (and occasionally using this bots advice) I have enough information to stop the experiment. 
        Below is some ongoing analysis on this central question and relevant information about the data that was gathered.
        Additionally, I wanted to see if I could find a viable trading stategy based on these results... Which remains to be found. {link}."""

        about_data = """The data obtained for this project is from a simple web scraper. Using the python reddit API, I scraped wsb for mentions of stocks and general sentiment. 
        The bot was run roughly once a day, (N=50) toward the end of the Nasdaq trading period. The stock data was obtained with yahoo finance in the form of daily closes. 
        The following analyses were done after the bot had collected data points from 4 March, 21 -- 12 July, 21."""

        col1_1.subheader(date)
        st.subheader("Results")
        st.write(results)
        st.subheader('About the data')
        st.write(about_data)
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

secondly = st.beta_container()
col2_1, col2_2 = st.beta_columns((1,6))
with secondly:
    top_5 = big_tuna.iloc[:,:5]
    top_5_10 = big_tuna.iloc[:,5:10]
    with col2_1:
        bt_cols = []
        for col in big_tuna.iloc[:,:-1]:
            for row in big_tuna[col]:
                if col not in bt_cols:
                    if row > 2:
                        bt_cols.append(col)
                        break
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
                      scale=alt.Scale(domain = [big_tuna.iat[-len(big_tuna),-1], big_tuna.iat[-1,-1]])),
            y = 'mentions:Q',
            color = 'ticker:N'
            )
            # .interactive(bind_y=False)

        st.altair_chart(interactive_chart, use_container_width=True)


analysis_briefer = st.beta_container()
analysis = st.beta_container()
col3_1, col3_2, col3_3 = st.beta_columns((1,1,1))
with analysis:
    # load in csv shite

    with analysis_briefer:
        st.subheader('Analysis')
        st.write(
            """
            Of the 495 stocks that my bot has seen mentioned as it scrapes r/wallstreetbets/new, only a few actually ascend to meme status.
            The vast majority of these mentions are from completely original 'DD' posts that fly under the radar and never gain traction on the subreddit.
            The highly mentioned 'meme stocks' take up most of the subreddit these days. 
            While the meme formats are hilarious, it makes genuine analysis on the underlying stock difficult.
            With the wsb mentions delayed over different time periods, we can see if there is any true correlation with price data.
            """)
    with col3_1:
        st.subheader("highly mentioned stocks")
        high_mention_corr_v = [0.215, 0.215,  0.167, 0.005, 0.05]
        high_mention_corr_d = ['1', '2', '5', '7', '12']
        high_mention_corr = pd.DataFrame()
        high_mention_corr['delay(days)'] = high_mention_corr_d 
        high_mention_corr['Pearson Correlation Coefficient'] = high_mention_corr_v
        st.table(high_mention_corr.assign(hack='').set_index('hack'))

        fig, ax = plt.subplots()
        sns.scatterplot('GME Mentions', 'Shifted 12', data=gme, x_jitter=0.2, y_jitter=0.3)
        ax.set_ylabel('price')
        ax.set_xlabel('Mentions 12 days prior on r/wsb')
        plt.title('GME')
        st.pyplot(fig)
        
    with col3_2:
        st.write("""
            Taking the difference of each close period, we get the price change between closes. 
            We then shift this by different periods, to see if there is a correlation with how often that stock was mentioned prior on r/wsb.
            I first tested the correlation for the grandest of the meme stocks, that is, GameStop.
            The results for any period delay period highly disappointing.
            The highest correlation occurs with a 12 period delay, giving a Pearson correlation coefficient (C) of 0.18
            """)

        st.write("""
            I assumed memified stocks such as GME would fail to have any correlation. 
            I also hypothesized that low-mention stocks would fail to have any correlation, due to less overall interest.
            THIS IS WHERE I STOPPED EDITING

            This is where it gets interesting, because as an average, I was very wrong. 
            As you can see on the left, these stocks have the lowest overall correlation with price data. 
            However, the deviance in Correlation was higher among them. 
            With a four day delay, (this is roughly one trading week) there were stonger correlations.
            For example, the NVDA plot to the right, shows C = 0.3, while ITUB had C = 0.54. 
            Others had a strong negative correlation, such as WOOF with C = -0.23.

            """)
    with col3_3:
        # top 5 -- 15
        st.subheader('mid-level mention stocks')
        med_mention_corr_v = [0.085, 0.085,  0.01, -0.008,  0.005]
        med_mention_corr_d = ['1', '2', '5', '7', '12']
        med_mention_corr = pd.DataFrame()
        med_mention_corr['delay(days)'] = med_mention_corr_d 
        med_mention_corr['Pearson Correlation Coefficient'] = med_mention_corr_v
        st.table(med_mention_corr.assign(hack='').set_index('hack'))
        
        fig, ax = plt.subplots()
        sns.scatterplot('NVDA Mentions', 'Shifted 8', data=nvda, x_jitter=0.2, y_jitter=0.3)
        ax.set_ylabel('price')
        ax.set_xlabel('mentions 8 days prior on r/wsb')
        plt.title('NVDA')
        st.pyplot(fig)

analysis_closer = st.beta_container()
with analysis_closer:
    st.subheader('Remarks on averaged correlations')
    st.write(
        """
        With the above averages in correlation, It makes sense that there is nothing significant. 
        There are some outliers, which I will look at more closely below. 
        I also want to look next at specific changes in mentions of a stock.
        It makes sense that across individual price changes, we have a low correlation. 
        If it were statistically significant, then everyone would see this as a viable strategy.
        It remains to be seen if there is some correlation between big shifts in mention number 
        (which I'll refer to in the next section as "mention velocity") and change in close prices. 
        Looking at the history charts above, it is clear that some stocks become sudden beacons on r/wsb.
        I want to look more closely at these sudden changes.
        """)

analysis_continued = st.beta_container()
col4_1 = st.beta_columns((1,1)) 




about = st.beta_container()
col5_1, col5_2 = st.beta_columns((5,1))
with about:
    with col5_1:
        col5_1.subheader("About the project")
        st.write(
            """
            I started this project shortly after joining r/wallstreetbets, a community on reddit devoted to some of the worst trading tactics imaginable.
            With an applied math degree and too much time on my hands, I decided to learn a bit of web developent. I quickly got in way over my head. 
            While the idea for this site began as a blog-style trading experiment using a web-scraper, I couldn't resist making it about data science.
            I began stockpiling data after the gamestop shorting event in January-February 2021. I watched as my investment account soared to heights it had never seen.
            Then I watched as it slowly crumbled and fell back to earth. 
            Then I watched as it sank below the earth and turned up somewhere in hell. 
            There is nothing left to do but experiment with what is left.
            This is not financial advice, I just wanted to see what would happen if I listened to the worst investors on the internet.
            """)
    with col5_2:
        
        st.markdown(
            f"""
            <div class = "centered">
                <h3>
                    Me
                </h1>
            </div>
            """, unsafe_allow_html=True)

        # thank you streamlitopedia for this fxn
        def img_to_bytes(img_path):
            img_bytes = Path(img_path).read_bytes()
            encoded = base64.b64encode(img_bytes).decode()
            return encoded     
        pic = img_to_bytes("images/prof_pic2.jpeg")
        header_html = """
                    <img 
                    src='data:image/jpeg;base64,{}' 
                    id='prof' 
                    class='img-fluid'>""".format(img_to_bytes("images/prof_pic2.jpeg"))

        st.markdown(header_html, unsafe_allow_html=True)

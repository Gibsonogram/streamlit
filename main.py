import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import math
import seaborn as sns
from datetime import datetime

st.set_page_config(layout="wide",
                   initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                   page_title="I am a great investor")


currently_p1 = """Back in the red. This bot fucked me, the one time I decide to trust it, I lose big.
Until now I was just laughing along, buying whatever BS had two mentions, then this obsession with UWMC started.
Suddenly the mentions for this stock were through the roof and I started drinking the koolaid again. 
I learned nothing from Gamestonk."""
current_positions = """One UWMC call that has lost about 50% of its value. 
Calls on SPY. 
Some other meme stocks sprinked in. No large positions."""
currently_p2 = """I need time to recover from this betrayal. 
One thing I need to figure out is how the hell I'm going to handle exiting positions."""


big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
header = st.beta_container()
currently = st.beta_container()
analysis = st.beta_container()
about = st.beta_container()

st.markdown(
    f"""
    <style>
        .reportview-container .main .block-container{{
            padding-top: {5}px;
            padding-bottom: {5}rem;
        }}
    </style>
""",
    unsafe_allow_html=True)
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>"""
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)









header_image = Image.open("images/school_athens.png")
prof_pic = Image.open("images/prof_pic2.png")
date = datetime.now().strftime('%m/%d/%y')


with header:
    st.image(header_image, use_column_width=True)

#doing a calculation without date column
bt_date = big_tuna.pop('date_hour')
big_tuna = big_tuna.drop('GME ', axis = 1)
tuna_head = big_tuna.iloc[-1].sort_values(ascending=False).head(10)
big_tuna['date_hour'] = bt_date


col1_1, col1_2 = st.beta_columns((7,6))

with currently:
    st.header("Currently")
    with col1_1:
        col1_1.subheader(date)
        st.write(currently_p1)
        st.subheader("Current positions")
        st.write(current_positions)
        st.write(currently_p2)


    with col1_2:
        fig, ax = plt.subplots()
        fig.suptitle("trending on wsb")

        s = sns.barplot(x= tuna_head.index,
                y= tuna_head.values,
                color='gold',
                ax=ax)
        #s.set_ylim(0)
        ax.set_xlabel('ticker')
        ax.set_ylabel('mentions')
        st.pyplot(fig)


col2_1, col2_2 = st.beta_columns((1,5))
with analysis:
    col2_1.subheader("hot stocks")
    col2_2.subheader("chart")
    with col2_1:
        tuna_head
    with col2_2:

        fig, ax = plt.subplots(figsize = (9,4))

        top_5 = big_tuna.iloc[:, :5]
        first = big_tuna.iloc[:, 0]
        second = big_tuna.iloc[:, 1]
        third = big_tuna.iloc[:, 2]
        fourth = big_tuna.iloc[:, 3]
        fifth = big_tuna.iloc[:, 4]
        plt.xlim(0, len(big_tuna))

        plt.tight_layout()
        plt.xticks(rotation=0)
        ax.plot(first, color='green')
        ax.plot(second, color='red')
        ax.plot(third, color='purple')
        ax.plot(fourth, color='orange')
        ax.plot(fifth, color='blue')
        ax.set(ylabel='mentions',
               title='history of mentions on r/wsb',
               yscale ='linear')
        ax.legend(top_5.columns)

        plt.xticks(ticks = np.arange(0,len(big_tuna)), labels = big_tuna['date_hour'])
        n = math.floor(len(big_tuna) / 6)
        for index, label in enumerate(ax.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)

        ax.grid()
        col2_2.pyplot(fig)


col3_1, col3_2 = st.beta_columns((3,1))

with about:
    with col3_1:
        col3_1.subheader("About the project")
        st.write("""I started this project after I took an autists advice and invested in GME. I watched as my account soared to heights it had never seen.
        Then I watched as it slowly crumbled and fell back to earth. Then I watched as it sank below the earth and turned up somewhere in hell.
        Now, I have learned all the lessons. I am now completely qualified to make decisions about stonks and obviously options. 
        I know everything and I will succeed this time. I need only listen to the autists.
        """)
        st.write("""So I made a bot to judge the sentiment of given stocks on r/wallstreetbets and I will only take advice from there. 
        Feel free to check back and watch as my account plummets or soars. This is not financial advice, I just wanted to see what would happen
        and I lost most of my money already so... 
        """)

    with col3_2:
        col3_2.subheader("Me")
        st.image(prof_pic, use_column_width = True)

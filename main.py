import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import math
import seaborn as sns
from datetime import datetime
import altair as alt

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
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)









header_image = Image.open("images/school_athens.png")
prof_pic = Image.open("images/prof_pic2.png")
date = datetime.now().strftime('%m/%d/%y')


with header:
    st.image(header_image, use_column_width=True)

#doing a calculation without date column
bt_date = big_tuna.pop('date_hour')
big_tuna = big_tuna.drop('GME ', axis = 1)
tuna_chunk = big_tuna.iloc[:, :10].tail(10)
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
        tuna_head = pd.DataFrame({"stock" : tuna_chunk.columns,
                                  "mentions" : big_tuna.iloc[-1,:10]
                                  })
        c = alt.Chart(tuna_head).mark_bar().encode(
            x = 'stock',
            y = 'mentions'
        ).properties(
            height = 500
        )
        st.altair_chart(c, use_container_width=True)






col2_1, col2_2 = st.beta_columns((3,5))
with analysis:
    col2_1.subheader("hot stocks")
    col2_2.subheader("chart")
    with col2_1:
        tuna_head.values


    with col2_2:

        c = alt.Chart(big_tuna).mark_line().encode(
            x="date_hour:T",
            y="AMC "
        ).interactive()
        st.altair_chart(c, use_container_width=True)






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

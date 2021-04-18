import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
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

#doing a calculation without date column
bt_date = big_tuna.pop('date_hour')
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
        tuna_chunk = big_tuna.iloc[:, :10].tail(10)
        tuna_head = pd.DataFrame({"stock" : tuna_chunk.columns,
                                  "mentions" : big_tuna.iloc[-1,:10]
                                  })
        current_chart = alt.Chart(tuna_head).mark_bar(
            cornerRadiusTopLeft = 5,
            cornerRadiusTopRight= 5,
            color='6fb1ce').encode(
                x = 'stock',
                y = 'mentions').properties(height = 500)

        # @st.cache(suppress_st_warning=True)
        def chart_current():
            st.altair_chart(current_chart, use_container_width=True)
        chart_current()

col2_1, col2_2 = st.beta_columns((1,6))
with analysis:
    top_5 = big_tuna.iloc[:,:5]
    # col2_1.subheader("hot stocks")
    col2_2.subheader("chart")
    with col2_1:
        top_15 = big_tuna.iloc[:,:15].columns.tolist()
        top_15_selector = st.selectbox('select chart', top_15, index=0)


    with col2_2:

        top_5['date'] = bt_date

        top_5 = top_5.melt('date', var_name='ticker', value_name='mentions')
        top_5_chart = alt.Chart(top_5).mark_line().encode(
            x = alt.X('date:T',
                      scale=alt.Scale(
                          domain = [big_tuna.iat[len(big_tuna) - 20,-1],
                                    big_tuna.iat[-1,-1]])),
            y = 'mentions:Q',
            color = 'ticker:N'
        ).interactive(bind_y = False)

        st.altair_chart(top_5_chart, use_container_width=True)









col3_1 = st.beta_container()
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

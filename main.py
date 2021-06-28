import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import altair as alt

st.set_page_config(layout="wide",
                   initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                   page_title="The college try")


currently_p1 = """This site is getting a final update. It will remain static after today, however the project continues! 
The analysis I begain here will be moving to my new website.
A website that is, dare I say, superior."""
current_positions = """After months of using this bots advice intermittently, growing angry, then weary, I have halted the experiment for now. 
I am not trading based on the bot any longer. 
I am however going to do a rigorous analysis on price history vs r/wallstreetbets mentions. 
I will be showing just how correlated these variables are, and whether or not this strategy is truly viable. 
Here is a link to the new site, where the data from this project has been moved, and analysis continues:"""


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
                The old college try
            </h1>
        </div>
        """, unsafe_allow_html=True)

#doing a calculation without date column
bt_date = big_tuna.pop('date_hour')
big_tuna['date_hour'] = bt_date

col1_1, col1_2 = st.beta_columns((7,6))
with currently:
    st.header("A final update on the project")
    with col1_1:
        col1_1.subheader(date)
        st.write(currently_p1)
        st.subheader("Thoughts")
        st.write(current_positions)
        link = '[put my new site link here](http://github.com)'
        st.markdown(link, unsafe_allow_html=True) 

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
    top_5_ls = top_5.iloc[-10:,:].transpose()
    top_5_ls = top_5_ls
    col2_1.subheader("top 5 over the last week")
    col2_2.subheader("most mentioned stocks")
    with col2_1:
        top_15 = big_tuna.iloc[:,:15].columns.tolist()
        top_15_selector = st.write(top_5_ls)


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

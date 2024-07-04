""" Dashboard for displaying analytical data from the RDS containing 
    information about StackExchange History questions."""

import pandas as pd
import streamlit as st
import altair as alt
import connect


def get_popular_tags_display(conn):
    """ Displays graphs for popular tags in two columns. """

    st.markdown('#')
    tags_columns = st.columns([1, 0.1, 1])  # spacer between columns

    with tags_columns[0]:
        st.altair_chart(get_most_popular_tags_graph(conn))

    with tags_columns[2]:
        st.altair_chart(get_most_popular_tags_this_week_graph(conn))


def get_most_popular_tags_graph(conn):
    """ Retrieves most popular tags as a DataFrame and returns its
        corresponding bar chart. """

    popular_tags_df = connect.load_most_popular_tags(conn)
    tag_column = popular_tags_df.columns[0]
    tag_count_column = popular_tags_df.columns[1]

    return alt.Chart(popular_tags_df, title="Popular Tags 🏷️ - all time").mark_bar().encode(
        x=alt.X(f'{tag_count_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None,
                        scale=alt.Scale(scheme="purples")),
    ).properties(
        width=500,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        titleColor='black'
    ).configure_title(
        fontSize=18,
        anchor='start'
    )


def get_most_popular_tags_this_week_graph(conn) -> alt.Chart:
    """ Retrieves most popular tags used this week as a DataFrame and returns its
        corresponding bar chart. """

    popular_tags_week_df = connect.load_most_popular_tags_this_week(conn)

    tag_column = popular_tags_week_df.columns[0]
    tag_count_column = popular_tags_week_df.columns[1]

    return alt.Chart(popular_tags_week_df, title="Popular Tags 🏷️ - for this week").mark_bar(
    ).encode(
        x=alt.X(f'{tag_count_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None,
                        scale=alt.Scale(scheme="purples")),
    ).properties(
        width=500,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        titleColor='black'
    ).configure_title(
        fontSize=18,
        anchor='start'
    )


def get_questions_asked_by_times_display(conn):
    """ Displays graph for time of day that questions are asked, and radio button to choose
        what times the graph displays. In 2 columns. """

    st.markdown('#')
    time_columns = st.columns([1, 0.5, 0.5])

    with time_columns[1]:
        st.markdown('#')
        chosen_time = st.radio(
            "Times:", ["All times",
                       "Morning (Before 12pm)",
                       "Afternoon (Before 5pm)",
                       "Night (After 5pm)"])

    with time_columns[0]:
        st.altair_chart(get_questions_asked_at_times_graph(conn, chosen_time))


def get_questions_asked_at_times_graph(conn, time) -> alt.Chart:
    """ Retrieves number of questions asked at specific times of the day: morning, afternoon, night
        as a DataFrame. Plots a scatter graph and returns it. """

    if time == "Morning":
        questions_df = connect.load_num_questions_asked_before_12pm(conn)
    elif time == "Afternoon":
        questions_df = connect.load_num_questions_asked_between_12_5pm(conn)
    elif time == "Night":
        questions_df = connect.load_num_questions_asked_after_5pm(conn)
    else:
        questions_df = pd.concat([connect.load_num_questions_asked_before_12pm(conn),
                                  connect.load_num_questions_asked_between_12_5pm(
                                      conn),
                                  connect.load_num_questions_asked_after_5pm(conn)])

    upload_hour = questions_df.columns[0]
    question_count = questions_df.columns[1]

    return alt.Chart(questions_df, title="Questions uploaded hourly ⏰").mark_circle(size=60).encode(
        x=alt.X(upload_hour),
        y=alt.Y(question_count),
        color=alt.Color(upload_hour, legend=None,
                        scale=alt.Scale(scheme="purples")),
    ).properties(
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        titleColor='black'
    ).configure_title(
        fontSize=18,
        anchor='start'
    )


def get_tags_by_votes_and_answers_display(conn):
    """ Displays graphs for tags that are most visible per votes and answers their corresponding 
        questions receive. In 2 columns."""

    st.markdown('#')
    tags_columns = st.columns([1, 0.1, 1])

    with tags_columns[0]:
        st.altair_chart(get_tags_most_votes_graph(conn))

    with tags_columns[2]:
        st.altair_chart(get_tags_most_answers_graph(conn))


def get_tags_most_votes_graph(conn) -> alt.Chart:
    """ Retrieves tags and the total number of votes their corresponding questions receive 
        as a DataFrame. Plots a bar chart and returns it. """

    tags_most_votes_df = connect.load_tags_for_questions_with_most_votes(conn)

    tag_column = tags_most_votes_df.columns[0]
    tag_votes_column = tags_most_votes_df.columns[1]

    return alt.Chart(tags_most_votes_df, title="Tags for questions with most votes 🗳️").mark_bar(
    ).encode(
        x=alt.X(f'{tag_votes_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None,
                        scale=alt.Scale(scheme="purples")),
    ).properties(
        width=500,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        titleColor='black'
    ).configure_title(
        fontSize=18,
        anchor='start'
    )


def get_tags_most_answers_graph(conn) -> alt.Chart:
    """ Retrieves tags and the total number of answers their corresponding questions receive
        as a DataFrame. Plots a bar chart and returns it. """

    tags_most_answers_df = connect.load_tags_for_questions_with_most_answers(
        conn)

    tag_column = tags_most_answers_df.columns[0]
    tag_answers_column = tags_most_answers_df.columns[1]

    return alt.Chart(tags_most_answers_df, title="Tags for questions with most answers 💡").mark_bar(
    ).encode(
        x=alt.X(f'{tag_answers_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None,
                        scale=alt.Scale(scheme="purples"))
    ).properties(
        width=500,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        titleColor='black'
    ).configure_title(
        fontSize=18,
        anchor='start'
    )


def get_authors_with_most_questions_and_answers_display(conn):
    """ Displays graphs for authors who ask most questions and authors
        who write most answers. In 2 columns."""

    st.markdown('#')
    tags_columns = st.columns([1, 0.1, 1])

    with tags_columns[0]:
        st.markdown(f"""<h4 style='font-size:{'18px'}; color:{
            'black'};'> Users who have written the most questions: </h4>""", unsafe_allow_html=True)
        st.dataframe(connect.load_author_asks_most_questions(
            conn))

    with tags_columns[2]:
        st.markdown(f"""<h4 style='font-size:{'18px'}; color:{
                    'black'};'> Users who have written the most answers: </h4>""", unsafe_allow_html=True)
        st.dataframe(connect.load_author_writes_most_answers(conn))


def set_up_dashboard():
    """ Sets up Streamlit dashboard and fills page with graphs. """

    st.set_page_config(page_title="StackExchange-History Analytics",
                       page_icon="📊",
                       layout="wide",
                       initial_sidebar_state="collapsed")
    st.title("StackExchange - History Analytics")

    conn = connect.get_connection()

    get_popular_tags_display(conn)

    get_questions_asked_by_times_display(conn)

    get_tags_by_votes_and_answers_display(conn)

    get_authors_with_most_questions_and_answers_display(conn)

    conn.close()


if __name__ == "__main__":
    set_up_dashboard()
    # external link: 3.10.208.9:8501

    # streamlit run dashboard.py

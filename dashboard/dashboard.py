import pandas as pd
import streamlit as st
# import charts
import connect
import altair as alt


def get_most_popular_tags_graph(conn):
    """ Retrieves most popular tags as a DataFrame and returns its
        corresponding bar chart. """

    popular_tags_df = connect.load_most_popular_tags(conn)
    tag_column = popular_tags_df.columns[0]
    tag_count_column = popular_tags_df.columns[1]

    return alt.Chart(popular_tags_df, title="Popular Tags 🏷️ - all time").mark_bar().encode(
        x=alt.X(f'{tag_count_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None),
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

    return alt.Chart(popular_tags_week_df, title="Popular Tags 🏷️ - for this week").mark_bar().encode(
        x=alt.X(f'{tag_count_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None),
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
        color=alt.Color(upload_hour, legend=None),
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


def get_tags_most_votes_graph(conn) -> alt.Chart:
    tags_most_votes_df = connect.load_tags_for_questions_with_most_votes(conn)

    tag_column = tags_most_votes_df.columns[0]
    tag_votes_column = tags_most_votes_df.columns[1]

    return alt.Chart(tags_most_votes_df, title="Tags for questions most votes 🏷️").mark_bar().encode(
        x=alt.X(f'{tag_votes_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None),
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
    tags_most_answers_df = connect.load_tags_for_questions_with_most_answers(
        conn)

    tag_column = tags_most_answers_df.columns[0]
    tag_answers_column = tags_most_answers_df.columns[1]

    return alt.Chart(tags_most_answers_df, title="Tags for questions most answers 🏷️").mark_bar().encode(
        x=alt.X(f'{tag_answers_column}:Q'),
        y=alt.Y(f'{tag_column}:N', sort='x'),
        color=alt.Color(tag_column, legend=None),
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


def set_up_dashboard():
    """ Sets up Streamlit dashboard and fills graphs"""
    st.set_page_config(page_title="StackExchange-History Analytics",
                       page_icon="📊",
                       layout="wide",
                       initial_sidebar_state="collapsed")
    st.title("StackExchange - History Analytics")

    conn = connect.get_connection()

    st.markdown('#')
    tags_columns = st.columns([1, 0.1, 1])  # spacer between columns
    with tags_columns[0]:
        st.altair_chart(get_most_popular_tags_graph(
            conn))
    with tags_columns[2]:
        st.altair_chart(get_most_popular_tags_this_week_graph(
            conn))

    st.markdown('#')
    time_columns = st.columns([1, 0.5, 0.5])
    with time_columns[1]:
        st.markdown('#')
        chosen_time = st.radio(
            "Times:", ["All times", "Morning (Before 12pm)", "Afternoon (Before 5pm)", "Night (After 5pm)"])
    with time_columns[0]:
        st.altair_chart(get_questions_asked_at_times_graph(conn, chosen_time))

    st.markdown('#')
    tags_columns = st.columns([1, 0.1, 1])
    with tags_columns[0]:
        st.altair_chart(get_tags_most_votes_graph(
            conn))
    with tags_columns[2]:
        st.altair_chart(get_tags_most_answers_graph(
            conn))


if __name__ == "__main__":
    set_up_dashboard()

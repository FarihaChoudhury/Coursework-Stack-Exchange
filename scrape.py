""" Web scrapes stack exchange history questions for latest 50 questions.
    https://history.stackexchange.com/questions?tab=newest&pagesize=50.
    Retrieves details about each question and their answers. """

import requests as req
from bs4 import BeautifulSoup


def get_website(url: str):
    """ Gets URL for recent 50 history questions """
    return req.get(url)


def soup_website(response: str):
    """ Web scrapes response of website and parses it. """
    return BeautifulSoup(response.text, features="html.parser")


def get_all_questions(soup: str):
    """ Retrieves all questions """
    return soup.find_all("div", class_="js-post-summary")


def get_questions_details(questions: str):
    """ Retrieves details for each question: title, tags, votes, answer count, views,
        username, answers and its details"""
    for question in questions:
        title = get_question_title(question)
        tags = get_question_tags(question)
        votes, answers_count, views, username = get_question_stats(question)
        answers = get_answers(question)

        print("title: ", title)
        print("tags: ", tags)
        print("votes: ", votes)
        print("answers count: ", answers_count)
        print("views: ", views)
        print("username: ", username)
        print("answers - text", len(answers))

        print("\n")


def get_question_title(question: str):
    """ Retrieves question title """
    return question.find(
        "h3", class_="s-post-summary--content-title").get_text().strip()


def get_question_tags(question: str):
    """ Retrieves question tags """
    return [tag.get_text() for tag in question.find_all(
        "li", class_="d-inline mr4 js-post-tag-list-item")]


def get_question_stats(question: str):
    """ Retrieves statistics for a question regarding: votes, answer count, views, username. """
    all_stats = question.find_all(
        "div", class_="s-post-summary--stats-item")
    votes = 0
    answers_count = 0
    views = 0
    for x in all_stats:
        stat_text = x.find(
            'span', class_="s-post-summary--stats-item-unit").get_text().strip()
        stat_value = x.find(
            'span', class_="s-post-summary--stats-item-number").get_text().strip()

        if stat_text == "votes" or stat_text == "vote":
            votes = stat_value
        if stat_text == "answers" or stat_text == "answer":
            answers_count = stat_value
        elif stat_text == "views" or stat_text == "view":
            views = stat_value

    username = question.find(
        "div", class_="s-user-card--link d-flex gs4").get_text().strip()

    return votes, answers_count, views, username


def get_answers(question):
    """ Retrieves all answers for a questions and its details" answer, username, vote"""
    link = f"https://history.stackexchange.com/{
        question.find("a", class_="s-link").get("href")}"

    question_response = req.get(link)
    print(link)
    soup = BeautifulSoup(question_response.text, features="html.parser")

    all_answers = soup.find_all("div", class_="answer js-answer")
    answers = []
    for answer in all_answers:
        answers.append(
            {'answer': answer.find(
                'div', class_='s-prose js-post-body').get_text(),
             'username': answer.find('div', itemprop="author").find('a').get_text().strip(),
             'vote_count': answer.find('div', class_='js-vote-count').get_text().strip()})
        print(answers)

    return answers


if __name__ == "__main__":
    response = get_website(
        "https://history.stackexchange.com/questions?tab=Newest")
    soup = soup_website(response)

    questions = get_all_questions(soup)
    result = get_questions_details(questions)

    print(len(questions))

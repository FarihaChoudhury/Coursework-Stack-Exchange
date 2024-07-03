""" Web scrapes stack exchange history questions for latest 50 questions.
    https://history.stackexchange.com/questions?tab=newest&pagesize=50.
    Retrieves details about each question and their answers. """

import requests as req
from bs4 import BeautifulSoup


def get_website(url: str):
    """ Gets URL for recent 50 history questions """

    return req.get(url, timeout=15)


def soup_website(response: str):
    """ Web scrapes response of website and parses it. """

    return BeautifulSoup(response.text, features="html.parser")


def get_all_questions(soup: str) -> str:
    """ Retrieves all questions """

    return soup.find_all("div", class_="js-post-summary")


def get_questions_details(questions: str) -> list[dict]:
    """ Retrieves details for each question: title, tags, votes, answer count, views,
        username, answers and its details"""

    questions_data = []
    for question in questions:

        votes, views, username = get_question_stats(question)
        questions_data.append(
            {
                'question_id': get_question_id(question),
                'title': get_question_title(question),
                'tags': get_question_tags(question),
                'votes': votes,
                'views': views,
                'username': username,
                'answers': get_answers(question)
            })
        # print(len(questions_data))
    return questions_data


def get_question_id(question: str) -> str:
    """ Retrieves id from question """

    question_id = question.get('data-post-id')
    return question_id if question_id else None


def get_question_title(question: str) -> str:
    """ Retrieves question title """

    return question.find(
        "h3", class_="s-post-summary--content-title").get_text().strip()


def get_question_tags(question: str) -> list:
    """ Retrieves question tags """

    return [tag.get_text() for tag in question.find_all(
        "li", class_="d-inline mr4 js-post-tag-list-item")]


def get_question_stats(question: str) -> str:
    """ Retrieves statistics for a question regarding: votes, answer count, views, username. """

    all_stats = question.find_all(
        "div", class_="s-post-summary--stats-item")

    votes = 0
    views = 0

    for stat in all_stats:
        stat_text = stat.find(
            'span', class_="s-post-summary--stats-item-unit").get_text().strip()
        stat_value = stat.find(
            'span', class_="s-post-summary--stats-item-number").get_text().strip()

        if stat_value.endswith('k'):
            stat_value = stat_value.replace('k', '000')

        if stat_text in ("vote", "votes"):
            votes = stat_value
        elif stat_text in ("view", "views"):
            views = stat_value

    username = question.find(
        "div", class_="s-user-card--link d-flex gs4").get_text().strip()

    return votes, views, username


def get_answers(question) -> list[dict]:
    """ Retrieves all answers for a questions and its details" answer, username, vote. """

    all_answers = scrape_answer(question)
    answers = []

    for answer in all_answers:

        answers.append(
            {'answer_id': get_answer_id(answer),
             'answer': answer.find(
                 'div', class_='s-prose js-post-body').get_text().strip(),
             'username': get_answer_author(answer),
             'vote_count':
                answer.find('div', class_='js-vote-count').get_text().strip().replace('k', '000')})

    return answers


def scrape_answer(question) -> list[str]:
    """ Extracts all answers for a given question. """

    link = f"https://history.stackexchange.com/{
        question.find("a", class_="s-link").get("href")}"

    question_response = get_website(link)
    soup = soup_website(question_response)

    all_answers = soup.find_all("div", class_="answer js-answer")

    return all_answers


def get_answer_author(answer: str) -> str:
    """ Retrieves username of author of an answer to a question. """

    author = answer.find('div', itemprop="author").find(
        'span', itemprop='name')

    if author:
        username = author.get_text()
    else:
        username = answer.find(
            'div', itemprop="author").find('a').get_text()

    return username


def get_answer_id(answer: str) -> str:
    """ Retrieves id from answer """

    answer_id = answer.get('data-answerid')
    return answer_id if answer_id else None


def extract_stack_exchange_history_data() -> dict:
    """ Extracts stack exchange data for history questions"""

    response = get_website(
        "https://history.stackexchange.com/questions?tab=Newest")
    print(response.status_code)
    soup = soup_website(response)

    questions = get_all_questions(soup)
    result = get_questions_details(questions)

    print(len(questions))

    return result


if __name__ == "__main__":
    history_questions = extract_stack_exchange_history_data()

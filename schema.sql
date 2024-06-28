-- -- psql -d postgres -c "CREATE DATABASE stack_exchange"
-- -- psql postgres 
-- -- \c stack_exchange
-- -- \i schema.sql

-- psql -h c11-fariha-stackexchange.c57vkec7dkkx.eu-west-2.rds.amazonaws.com -U stack_exchange -d c11-fariha-stackexchange
-- -- Creating tables: 

DROP TABLE IF EXISTS Answer CASCADE;
DROP TABLE IF EXISTS Tag CASCADE;
DROP TABLE IF EXISTS Question CASCADE;
DROP TABLE IF EXISTS Author CASCADE;



CREATE TABLE Author(
    author_id INT GENERATED ALWAYS AS IDENTITY,
    author_username TEXT,

    PRIMARY KEY (author_id)
);

CREATE TABLE Question (
    question_id INT GENERATED ALWAYS AS IDENTITY,
    author_id INT NOT NULL,
    question TEXT NOT NULL,
    votes INT NOT NULL,
    views INT NOT NULL,

    PRIMARY KEY (question_id),
    FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

CREATE TABLE Tag(
    tag_id INT GENERATED ALWAYS AS IDENTITY,
    tag TEXT NOT NULL,
    question_id INT NOT NULL,

    PRIMARY KEY(tag_id),
    FOREIGN KEY(question_id) REFERENCES Question(question_id)
);

CREATE TABLE Answer(
    answer_id INT GENERATED ALWAYS AS IDENTITY,
    answer TEXT NOT NULL,
    votes INT NOT NULL,
    question_id INT NOT NULL,
    author_id INT NOT NULL,

    PRIMARY KEY(answer_id),
    FOREIGN KEY(question_id) REFERENCES Question(question_id),
    FOREIGN KEY(author_id) REFERENCES Author(author_id)
);


-- INSERT INTO Author (author_username) VALUES ('3rdk') RETURNING author_id;
-- INSERT INTO Question (author_id, question, votes, views) VALUES (1, 'how old am i?', 2, 1);
-- INSERT INTO Tag (tag, question_id) VALUES ('gross', 1);
-- INSERT INTO Answer(answer, votes, question_id, author_id) VALUES ('idk', 6, 1, 1);

SELECT * FROM Author;
SELECT * FROM Question;
SELECT * FROM Tag;
SELECT * FROM Answer;
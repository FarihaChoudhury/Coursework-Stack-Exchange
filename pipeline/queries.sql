-- SELECT * FROM Author;
SELECT COUNT(*) FROM Question;
SELECT * FROM Question;
-- SELECT * FROM Tag;
-- SELECT * FROM Question_Tag_Assignment;
-- SELECT * FROM Answer;

-- SELECT question, qt.question_id, tag, qt.tag_id 
-- FROM Question_Tag_Assignment qt
-- JOIN Question q ON qt.question_id = q.question_id
-- JOIN Tag t on t.tag_id = qt.tag_id
-- WHERE qt.tag_id = 3;






-- -- most popular tags, all time 
-- SELECT t.tag, COUNT(qt.tag_id) AS tag_count
-- FROM Question_Tag_Assignment qt
-- JOIN Tag t ON qt.tag_id = t.tag_id
-- GROUP BY t.tag
-- ORDER BY tag_count DESC
-- LIMIT 10;

-- -- most popular tags this week:  
-- SELECT t.tag, COUNT(qt.tag_id) AS tag_count
-- FROM Question_Tag_Assignment qt
-- JOIN Tag t ON qt.tag_id = t.tag_id
-- JOIN Question q ON qt.question_id = q.question_id
-- WHERE q.upload_timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
-- GROUP BY t.tag
-- ORDER BY tag_count DESC
-- LIMIT 10;

-- -- questions asked before 12pm:
-- COUNT(*) AS questions_before_12pm
            -- SELECT COUNT(*) AS questions_before_12pm
            -- FROM Question q
            -- WHERE DATE_PART('HOUR', q.upload_timestamp) < 12;


-- SELECT question_id, upload_timestamp
-- FROM Question q
-- WHERE DATE_PART('HOUR', q.upload_timestamp) < 12;


--NEWWWW: 
-- SELECT DATE_TRUNC('hour', q.upload_timestamp) AS upload_hour,
--        COUNT(*) AS question_count
-- FROM Question q
-- WHERE DATE_PART('HOUR', q.upload_timestamp) < 12
-- GROUP BY upload_hour
-- ORDER BY upload_hour;

-- SELECT DATE_PART('hour', q.upload_timestamp) AS upload_hour,
--        COUNT(*) AS question_count
-- FROM Question q
-- WHERE DATE_PART('HOUR', q.upload_timestamp) < 12
-- GROUP BY upload_hour
-- ORDER BY upload_hour;

-- -- questions asked between 12-5pm:
-- SELECT COUNT(*) AS questions_between_12_5pm
-- FROM Question q
-- WHERE DATE_PART('HOUR', q.upload_timestamp) >= 12
--     AND DATE_PART('HOUR', q.upload_timestamp) < 17;

-- SELECT DATE_PART('hour', q.upload_timestamp) AS upload_hour,
--        COUNT(*) AS question_count
-- FROM Question q
-- WHERE DATE_PART('HOUR', q.upload_timestamp) >= 12
--     AND DATE_PART('HOUR', q.upload_timestamp) < 17;
-- GROUP BY upload_hour
-- ORDER BY upload_hour;

-- -- questions after 5pm:
-- SELECT COUNT(*) AS questions_after_5pm
-- FROM Question q
-- WHERE DATE_PART('HOUR', q.upload_timestamp) >= 17;

-- SELECT DATE_PART('hour', q.upload_timestamp) AS upload_hour,
--        COUNT(*) AS question_count
-- FROM Question q
-- WHERE DATE_PART('HOUR', q.upload_timestamp) >= 17
-- GROUP BY upload_hour
-- ORDER BY upload_hour;



-- -- tags associated with questions with most votes (shows attention) - sum of votes for tags 
-- SELECT t.tag, SUM(q.votes) AS total_votes
-- FROM Tag t 
-- JOIN Question_Tag_Assignment qt ON t.tag_id = qt.tag_id
-- JOIN Question q ON q.question_id = qt.question_id
-- GROUP BY t.tag
-- ORDER BY total_votes DESC
-- LIMIT 10;

-- -- tags associated with questions with most answers (shows attention) - sum of answers for tags 
-- SELECT t.tag, COUNT(a.answer_id) AS total_answers
-- FROM Tag t 
-- JOIN Question_Tag_Assignment qt ON t.tag_id = qt.tag_id
-- JOIN Question q ON q.question_id = qt.question_id
-- JOIN Answer a on a.question_id = q.question_id
-- GROUP BY t.tag
-- ORDER BY total_answers DESC
-- LIMIT 10;


-- --authors who ask most questions
-- SELECT a.author_username, a.author_id, COUNT(q.question_id) AS num_questions_asked
-- FROM Author a 
-- JOIN Question q on q.author_id = a.author_id
-- GROUP BY a.author_id, a.author_username
-- ORDER BY num_questions_asked DESC
-- LIMIT 10;

-- --authors who answer most questions
-- SELECT a.author_username, a.author_id, COUNT(aw.answer_id) AS num_answers_written
-- FROM Author a 
-- JOIN Answer aw on aw.author_id = a.author_id
-- GROUP BY a.author_id, a.author_username
-- ORDER BY num_answers_written DESC
-- LIMIT 10;
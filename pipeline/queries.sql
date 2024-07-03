-- SELECT * FROM Author;
-- SELECT * FROM Question;
-- SELECT * FROM Tag;
-- SELECT * FROM Question_Tag_Assignment;
-- SELECT * FROM Answer;

-- SELECT question, qt.question_id, tag, qt.tag_id 
-- FROM Question_Tag_Assignment qt
-- JOIN Question q ON qt.question_id = q.question_id
-- JOIN Tag t on t.tag_id = qt.tag_id
-- WHERE qt.tag_id = 3;

-- most popular tags, all time 
-- SELECT t.tag, COUNT(qt.tag_id) AS tag_count
-- FROM Question_Tag_Assignment qt
-- JOIN Tag t ON qt.tag_id = t.tag_id
-- GROUP BY t.tag
-- ORDER BY tag_count DESC
-- LIMIT 10;

-- most popular tags this week:  
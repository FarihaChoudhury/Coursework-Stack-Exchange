SELECT * FROM Author;
SELECT * FROM Question;
SELECT * FROM Tag;
SELECT * FROM Question_Tag_Assignment;
SELECT * FROM Answer;

SELECT question, qt.question_id, tag, qt.tag_id 
FROM Question_Tag_Assignment qt
JOIN Question q ON qt.question_id = q.question_id
JOIN Tag t on t.tag_id = qt.tag_id
WHERE qt.tag_id = 3;
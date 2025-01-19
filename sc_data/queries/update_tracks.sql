UPDATE users
SET
    track_times = ?
WHERE
    chat_id = ? AND
    user_id = ?
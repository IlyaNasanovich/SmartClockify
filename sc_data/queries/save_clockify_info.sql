UPDATE users
SET
    clockify_apikey = ?,
    clockify_user_id = ?,
    clockify_name = ?,
    clockify_email = ?
WHERE
    chat_id = ? AND
    user_id = ?;

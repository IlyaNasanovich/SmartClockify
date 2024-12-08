UPDATE users
SET
    tracking_time_confirmation = ?,
    confirmation_message_id = ?
WHERE
    chat_id = ? AND
    user_id = ?;
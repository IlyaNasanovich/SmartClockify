SELECT
    clockify_apikey,
    tracking_time_confirmation,
    confirmation_message_id
FROM users
WHERE chat_id = ? AND user_id = ?
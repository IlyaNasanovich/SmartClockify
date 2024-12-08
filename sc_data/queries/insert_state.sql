INSERT INTO users (chat_id, user_id, state, clockify_apikey, clockify_user_id, clockify_name, clockify_email, tracking_time_confirmation, confirmation_message_id)
VALUES (?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL)
ON CONFLICT(chat_id, user_id)
DO UPDATE SET state = ?

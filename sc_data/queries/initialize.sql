CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    chat_id INTEGER,
    state TEXT,
    clockify_apikey TEXT,
    clockify_user_id TEXT,
    clockify_name TEXT,
    clockify_email TEXT,
    clockify_timezone TEXT,
    tracking_time_confirmation TEXT,
    confirmation_message_id INTEGER,
    track_times TEXT,
    PRIMARY KEY (chat_id, user_id)
);

def test_signup_new_account(app):
    username = "user2"
    password = "test"
    app.james.ensure_user_exists(username, password)

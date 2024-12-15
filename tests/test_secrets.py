"test_secrets.py"
from streamlit.testing.v1 import AppTest

def test_secrets():
    # Initialize an AppTest instance.
    at = AppTest.from_file("app.py")
    # Declare the secrets.
    at.secrets["db_username"] = "Jane"
    at.secrets["db_password"] = "mypassword"
    at.secrets["my_other_secrets.things_i_like"] = ["Streamlit", "Python"]
    # Run the app.
    at.run()

    assert at.secrets["my_other_secrets.things_i_like"] == ["Streamlit", "Python"]
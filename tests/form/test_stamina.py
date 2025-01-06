"test_stamina"
from streamlit.testing.v1 import AppTest



def test_number_input():
    """A user number input, then clicks save"""
    at = AppTest.from_file("pages/form/stamina.py").run()
    
    at.number_input(key="distance_input").set_value(45).run()
    assert at.number_input(key="distance_input").value == 45

if __name__ == "__main__":
    test_number_input()
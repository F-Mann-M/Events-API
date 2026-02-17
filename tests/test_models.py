from models import User

def test_user_password_hashing_behaves_correctly():
    """check if password hashing works correctly"""

    # Arrange
    user = User(username="TestUser01")
    user.set_password("TestPassword01")

    # Act & Assert
    assert user.check_password("TestPassword01") == True
    assert user.check_password("WrongPass") == False
    assert user.password_hash != "TestPassword01"
    assert user.password_hash is not None


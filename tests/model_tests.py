from unittest import main, TestCase
from models.models import User, Role


class UserTest(TestCase):
    user = User(username="arseniiohar228",
                firstName="Arsenii",
                lastName="Ohar",
                email="arsen.ogar@gmail.com",
                password="arseniiohar228",
                phone="+380987669293",
                role=Role.student
                )

    def test_wrong_password(self):
        with self.assertRaises(ValueError):
            self.user.password = "onlycharacters"

    def test_wrong_email(self):
        with self.assertRaises(ValueError):
            self.user.email = "arsen.ogar gmail.com"

    def test_wrong_firstname(self):
        with self.assertRaises(ValueError):
            self.user.firstName = "s"  # too short

    def test_wrong_lastname(self):
        with self.assertRaises(ValueError):
            self.user.lastName = "p"  # too short to be a name

    def test_wrong_role(self):
        with self.assertRaises(ValueError):
            self.user.role = 'bullshit'  # definitely not a role

    def test_wrong_phone(self):
        with self.assertRaises(ValueError):
            self.user.phone = '0505'  # too short

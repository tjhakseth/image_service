"""Tests for image service"""
import server
import unittest
from model import connect_to_db, db, Profile

TEST_DATABASE_URI = 'postgresql://localhost/servicetestdb'


class ServiceTestCase(unittest.TestCase):

    def setUp(self):

        server.app.config['TESTING'] = True
        server.app.config['DEBUG'] = False
        self.app = server.app.test_client()
        connect_to_db(server.app, TEST_DATABASE_URI)

        db.create_all()


    def tearDown(self):
        """Close DB session and drop all tables"""
        db.session.remove()
        db.drop_all()

class TestProfileCreation(ServiceTestCase):

    def test_sunny_day(self):
        """Creates a profile successfully"""

        # Given
        username = "bluesteel"
        date_of_birth = "1980-01-30"
        full_name = "Derek Zoolander"

        # When
        result = self.app.post('/profiles', data=dict(
            username=username,
            date_of_birth=date_of_birth,
            full_name=full_name
        ))

        # Then
        self.assertEqual(200, result.status_code)

        profile = Profile.query.get(username)
        self.assertIsNotNone(profile)
        self.assertEqual(username, profile.username)
        self.assertEqual(date_of_birth, profile.date_of_birth.isoformat())
        self.assertEqual(full_name, profile.full_name)
        self.assertIsNotNone(profile.api_token)

    def test_username_too_long(self):
        """Fails when username is too long"""

        # Given
        username = "bluesteel" * 50

        # When
        result = self.app.post('profiles', data=dict(username=username))

        # Then
        self.assertEqual(400, result.status_code)

class ProfileRetrieval(ServiceTestCase):
    """docstring"""

    def setUp(self):
        super(ProfileRetrieval, self).setUp()

        username = "test_username"
        date_of_birth = "1990-04-08"
        full_name = "Test Fullname"

        self.test_profile = Profile(
            username=username,
            api_token="bananas",
            date_of_birth=date_of_birth,
            full_name=full_name
        )

        db.session.add(self.test_profile)
        db.session.commit()

    def test_sunny_day(self):
        """Renders proper profile"""

        # given
        username = "test_username"

        # when
        result = self.app.get('/profiles', data=dict(username=username))

        # then
        self.assertEqual(200, result.status_code)

    def test_profile_list(self):
        """Profile list contains username"""

    def test_nonexistent_user(self):
        """Returns 404 status code for non-existent user"""


if __name__ == '__main__':
    unittest.main()

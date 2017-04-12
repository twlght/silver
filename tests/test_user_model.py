import unittest
from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        print('setup...')

    def tearDown(self):
        print('teardown...')

    def test_password_setter(self):
        u = User(password='Flint')
        self.assertTrue(u.password_hash is not None)

    def test_password_getter(self):
        u = User(password='Bill')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='Rogers')
        self.assertTrue(u.verify_password('Rogers'))
        self.assertFalse(u.verify_password('Roger'))

    def test_password_salts_are_random(self):
        u = User(password='Vane')
        u2 = User(password='Vane')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

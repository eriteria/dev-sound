import unittest

from soundclaz.models import AnonymousUser, Permission, Role, Users


class MyTestCase(unittest.TestCase):
    def test_roles_and_permissions(self):
        # Role.insert_roles()
        u = Users(name="John", email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()

        self.assertFalse(u.can(Permission.COMMENT))


if __name__ == '__main__':
    unittest.main()

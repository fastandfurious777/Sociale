from django.test import TestCase
from django.utils import timezone
from users.tests.factories import TestUserFactory


class UserModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = TestUserFactory.create()

    def test_deactivate(self):
        self.user.deactivate()
        self.assertFalse(self.user.is_active)

    def test_is_eligible(self):
        self.assertFalse(self.user.is_eligible)
        self.user.is_verified = True
        self.assertTrue(self.user.is_eligible)

    def test_verify(self):
        self.assertFalse(self.user.is_verified)
        self.assertIsNone(self.user.verified_at)
        self.user.verify()
        self.assertTrue(self.user.is_verified)
        self.assertAlmostEqual(
            self.user.verified_at, timezone.now(), delta=timezone.timedelta(seconds=1)
        )

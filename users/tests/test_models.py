from django.test import TestCase
from users.models import User
from django.utils import timezone

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User(
            email="user@test.com",
            password="pwd",
            is_active=True,
            is_verified=False
        )
        

    def test_deactivate(self):
        self.user.deactivate()
        self.assertFalse(self.user.is_active, "user should be deactivated")

    def test_is_eligible(self):
        self.assertFalse(self.user.is_eligible, "user should not be eligible when not verified")
        self.user.is_verified = True
        self.assertTrue(self.user.is_eligible, "user should be eligible when active and verified")

    def test_verify(self):
        self.assertFalse(self.user.is_verified)
        self.assertIsNone(self.user.verified_at, "verified_at should be None")
        self.user.verify()
        self.assertTrue(self.user.is_verified)
        self.assertAlmostEqual(
            self.user.verified_at, timezone.now(), delta=timezone.timedelta(seconds=1),
            msg="verified_at should be close to the current time"
        )
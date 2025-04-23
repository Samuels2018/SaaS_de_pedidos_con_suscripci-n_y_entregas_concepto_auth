""" init file for tests module """
from register_tests import RegisterUSerViewTestCase
from login_tests import LoginUserViewTestCase
from profile_tests import UserProfileViewTest

__all__ = ["RegisterUSerViewTestCase", "LoginUserViewTestCase", "UserProfileViewTest"]
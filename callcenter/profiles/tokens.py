from django.contrib.auth.tokens import PasswordResetTokenGenerator
import django.utils

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            django.utils.six.text_type(user.pk) + six.text_type(timestamp) +
            django.utils.six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()
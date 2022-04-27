from django.test import TestCase

# Create your tests here.

# https://docs.djangoproject.com/zh-hans/4.0/topics/testing/tools/#django.test.TransactionTestCase


class ContactTests(TestCase):
    def setUp(self):
        pass

    def test_post(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(
                # '/contact/',
                # {'message': 'I like your site'},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)

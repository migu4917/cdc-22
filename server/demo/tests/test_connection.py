from django.test import TestCase
from django.urls import reverse

# Create your tests here.

# https://docs.djangoproject.com/zh-hans/4.0/topics/testing/tools/

# refs:
# https://elfgzp.cn/2018/12/07/django-experience-2-test-case.html
# https://zhuanlan.zhihu.com/p/108049398


class GetContactTests(TestCase):
    def setUp(self):
        self.app_name = "server"
        pass

    def test_getall(self):
        url = reverse(self.app_name + ":getall")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_testget(self):
        url = reverse(self.app_name + ":testget")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_getAllContacts(self):
        url = reverse(self.app_name + ":getAllContacts")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_getAllEpidemics(self):
        url = reverse(self.app_name + ":getAllEpidemics")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_getAllPlace(self):
        url = reverse(self.app_name + ":getAllPlace")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

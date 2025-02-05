import csv
import os
import random

from django.conf import settings
from django.test import TestCase

from apps.frontend.servises.file_services import get_file_encoding, check_csv_file


class FileServicesTestCase(TestCase):
    encoding = ['utf-8', 'UTF-16', 'cp1251']
    ext = ['csv', 'txt']

    @classmethod
    def setUpClass(cls):
        for ext in cls.ext:
            for encoding in cls.encoding:
                with open(f"media/test/{encoding}.{ext}", "w", encoding=encoding, newline="") as csv_file:
                    fieldnames = settings.FIELDNAMES_FILE_MU
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
                    writer.writeheader()
                    row = {}
                    for key in settings.FIELDNAMES_FILE_MU:
                        row[key] = key
                    writer.writerow(row)

    @classmethod
    def tearDownClass(cls):
        for ext in cls.ext:
            for encoding in cls.encoding:
                os.remove(f"media/test/{encoding}.{ext}")

    def test_check_csv_file(self):
        for ext in self.ext:
            for encoding in self.encoding:
                self.assertEqual(check_csv_file(f"media/test/{encoding}.{ext}", settings.FIELDNAMES_FILE_MU, encoding=encoding), True)
                self.assertEqual(check_csv_file(f"media/test/{encoding}.{ext}", settings.FIELDNAMES_FILE_TYPE, encoding=encoding), False)

        # self.assertEqual(check_csv_file("media/test/TypeToRegistry.csv", settings.FIELDNAMES_FILE_TYPE, 'utf-8'), True)
        # self.assertEqual(check_csv_file("media/test/база поверок_new_.csv", settings.FIELDNAMES_FILE_TYPE, 'cp1251'), False)

    def test_get_file_encoding(self):
        for ext in self.ext:
            for encoding in self.encoding:
                self.assertEqual(get_file_encoding(f"media/test/{encoding}.{ext}"), encoding)

        # self.assertEqual(get_file_encoding("media/test/TypeToRegistry.csv"), 'utf-8')
        # self.assertEqual(get_file_encoding("media/test/база поверок_new_.csv"), 'cp1251')




# Create your tests here.


# class TestPage(TestCase):
#
#     def test_menu(self):
#         response = self.client.get("/api/page/menu/")
#         self.assertEqual(response.status_code, 200)
#
#     def test_addresses(self):
#         response = self.client.get("/api/page/addresses/")
#         self.assertEqual(response.status_code, 200)


# Create your tests here.
# from string import ascii_letters
# from random import choices
#
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.urls import reverse
#
# from shopapp.models import Product
# from shopapp.utils import add_two_numbers
#
#
# class AddTwoNumbersTestCase(TestCase):
#     def test_add_two_numbers(self):
#         result = add_two_numbers(2, 3)
#         self.assertEqual(result, 5)
#
#
# class ProductCreateViewTestCase(TestCase):
#     def setUp(self) -> None:
#         self.product_name = "".join(choices(ascii_letters, k=10))
#         Product.objects.filter(name=self.product_name).delete()
#
#     def test_create_product(self):
#         response = self.client.post(
#             reverse("shopapp:product_create"),
#             {
#                 "name": self.product_name,
#                 "price": "123.45",
#                 "description": "A good table",
#                 "discount": "10",
#             }
#         )
#         self.assertRedirects(response, reverse("shopapp:products_list"))
#         self.assertTrue(
#             Product.objects.filter(name=self.product_name).exists()
#         )
#
#
# class ProductDetailsViewTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.product = Product.objects.create(name="Best Product")
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.product.delete()
#
#     def test_get_product(self):
#         response = self.client.get(
#             reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
#         )
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_product_and_check_content(self):
#         response = self.client.get(
#             reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
#         )
#         self.assertContains(response, self.product.name)


# class AddressesListViewTestVase(TestCase):
#     fixtures = [
#         "db_20240918_new_address_region.json",
#     ]
#
#     def test_products(self):
#         response = self.client.get(reverse("for_page:addresses"))
#         self.assertQuerysetEqual(
#             qs=Address.objects.all(),
#             values=(p.pk for p in response.json()),
#             transform=lambda p: p.pk,
#         )
#         # self.assertTemplateUsed(response, "shopapp/products-list.html")
#
#
# #
# class OrdersListViewTestCase(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.user = User.objects.create_user(username="admin", password="123")
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.user.delete()
#
#     def setUp(self) -> None:
#         self.client.force_login(self.user)
#
#     def test_orders_view(self):
#         response = self.client.get(reverse("for_page:addreses"))
#         self.assertContains(response, "Adresses")
#
#     def test_orders_view_not_authenticated(self):
#         self.client.logout()
#         response = self.client.get(reverse("for_page:addresses"))
#         self.assertEqual(response.status_code, 302)
#         self.assertIn(str(settings.LOGIN_URL), response.url)
#

#
#
# class ProductsExportViewTestCase(TestCase):
#     fixtures = [
#         'products-fixture.json',
#     ]
#
#     def test_get_products_view(self):
#         response = self.client.get(
#             reverse("shopapp:products-export"),
#         )
#         self.assertEqual(response.status_code, 200)
#         products = Product.objects.order_by("pk").all()
#         expected_data = [
#             {
#                 "pk": product.pk,
#                 "name": product.name,
#                 "price": str(product.price),
#                 "archived": product.archived,
#             }
#             for product in products
#         ]
#         products_data = response.json()
#         self.assertEqual(
#             products_data["products"],
#             expected_data,
#         )

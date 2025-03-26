from django.test import TestCase
from django.urls import reverse


class BaseViewsTestCase(TestCase):
    index_template_name = "frontend/index.html"
    template_name = None
    url_name = None

    def setUp(self):
        self.client.post(
            reverse("my_auth:register"),
            {
                "username": "ADMIN_USERNAME",
                "email": "ADMIN_EMAIL@gmail.com",
                "password1": "ADMIN_password",
                "password2": "ADMIN_password",
            },
        )
        self.client.post(
            reverse("my_auth:login"),
            {
                "username": "ADMIN_USERNAME",
                "password": "ADMIN_password",
            },
        )

    def tearDown(self):
        self.client.get(reverse("my_auth:logout"))

    def test_status_code(self):
        if self.url_name:
            response = self.client.get(reverse(self.url_name))
            self.assertEqual(response.status_code, 200)

    def test_template_with_htmx(self):
        if self.template_name and self.url_name:
            headers = {"HTTP_Hx-Request": True}
            response = self.client.get(reverse(self.url_name), **headers)
            self.assertTemplateUsed(response, self.template_name)

    def test_template_without_htmx(self):
        if self.template_name and self.url_name:
            response = self.client.get(reverse(self.url_name))
            self.assertTemplateUsed(response, self.index_template_name)


class IndexViewsTestCase(BaseViewsTestCase):
    """Test index view"""

    url_name = "frontend:home"
    template_name = "frontend/index.html"


class UserOrganizationsListViewTestCase(BaseViewsTestCase):
    """Test user organization list view"""

    url_name = "frontend:user_organization_list"
    template_name = "frontend/user_organizations_list.html"


class MeteringUnitListViewTestCase(BaseViewsTestCase):
    """Test metering unit list view"""

    url_name = "frontend:metering_unit_list"
    template_name = "frontend/metering_unit_list.html"


class MenuItemListViewTestCase(BaseViewsTestCase):
    """Test menu item list view"""

    url_name = "frontend:menu_item_list"
    template_name = "frontend/menu_item_list.html"


class DeviceListViewTestCase(BaseViewsTestCase):
    """Test device list view"""

    url_name = "frontend:device_list"
    template_name = "frontend/device_list.html"

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

from django.test import TestCase
from django.urls import reverse


class BaseViewsTestCase(TestCase):
    index_template_name = "device/index.html"
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

    url_name = "device:home"
    template_name = "device/index.html"


class UserOrganizationsListViewTestCase(BaseViewsTestCase):
    """Test user organization list view"""

    url_name = "device:user_organization_list"
    template_name = "device/user_organizations_list.html"


class MeteringUnitListViewTestCase(BaseViewsTestCase):
    """Test metering unit list view"""

    url_name = "device:metering_unit_list"
    template_name = "device/metering_unit_list.html"


class MenuItemListViewTestCase(BaseViewsTestCase):
    """Test menu item list view"""

    url_name = "device:menu_item_list"
    template_name = "device/menu_item_list.html"


class DeviceListViewTestCase(BaseViewsTestCase):
    """Test device list view"""

    url_name = "device:device_list"
    template_name = "device/device_list.html"


# class MenuItemDetailView(ViewsTestCase):
#     """"""
#     url_name =
#     template_name =
#
#
# class DeviceDetailView(ViewsTestCase):
#     """"""
#     url_name =
#     template_name =
#
#
# class upload_device_from_file_view(ViewsTestCase):
#     """"""
#     url_name =
#     template_name =
#
#
# class download_device_to_file_view(ViewsTestCase):
#     """"""
#     url_name =
#     template_name =
#
#
# class refresh_valid_date_view(ViewsTestCase):
#     """"""
#     url_name =
#     template_name =
#
#
# class device_verifications_update_view(ViewsTestCase):
#     """"""
#     url_name =
#     template_name =

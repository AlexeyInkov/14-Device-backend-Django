import csv
import os

from django.conf import settings
from django.test import TestCase

from apps.device.servises.arshin_servises import request_to_arshin
from apps.device.servises.file_services import (
    get_file_encoding,
    check_csv_file,
    create_excel_from_dict_list,
)


class ArshinServiceTestCase(TestCase):
    def test_request_to_arshin_status_code(self):
        response = request_to_arshin("28313-11", "А522956")
        self.assertEqual(response.status_code, 200)

    def test_request_to_arshin_result(self):
        result = request_to_arshin("28313-11", "А522956").json().get("result")
        self.assertIsNotNone(result)

        result = request_to_arshin("", "").json().get("result")
        self.assertIsNone(result)

    def test_request_to_arshin_count(self):
        count = (
            request_to_arshin("28313-11", "А522956").json().get("result").get("count")
        )
        self.assertNotEqual(count, 0)

        count = request_to_arshin("рег", "3").json().get("result").get("count")
        self.assertEqual(count, 0)


# class DBServiceTestCase(TestCase):
#     pass


class FileServicesTestCase(TestCase):
    test_path = os.path.join(settings.MEDIA_ROOT, "test")
    encoding = ["utf-8", "UTF-16", "cp1251"]
    ext = ["csv", "txt"]

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls.test_path):
            os.makedirs(cls.test_path)
        for ext in cls.ext:
            for encoding in cls.encoding:
                with open(
                    f"{cls.test_path}/{encoding}.{ext}",
                    "w",
                    encoding=encoding,
                    newline="",
                ) as csv_file:
                    fieldnames = settings.FIELDNAMES_FILE_MU
                    writer = csv.DictWriter(
                        csv_file, fieldnames=fieldnames, delimiter=";"
                    )
                    writer.writeheader()
                    row = {}
                    for key in settings.FIELDNAMES_FILE_MU:
                        row[key] = key
                    writer.writerow(row)

    @classmethod
    def tearDownClass(cls):
        for ext in cls.ext:
            for encoding in cls.encoding:
                os.remove(f"{cls.test_path}/{encoding}.{ext}")

    def test_check_csv_file(self):
        for ext in self.ext:
            for encoding in self.encoding:
                self.assertEqual(
                    check_csv_file(
                        f"{self.test_path}/{encoding}.{ext}",
                        settings.FIELDNAMES_FILE_MU,
                        encoding=encoding,
                    ),
                    True,
                )
                self.assertEqual(
                    check_csv_file(
                        f"{self.test_path}/{encoding}.{ext}",
                        settings.FIELDNAMES_FILE_TYPE,
                        encoding=encoding,
                    ),
                    False,
                )

    def test_get_file_encoding(self):
        for ext in self.ext:
            for encoding in self.encoding:
                self.assertEqual(
                    get_file_encoding(f"{self.test_path}/{encoding}.{ext}"), encoding
                )

    def test_create_excel_from_dict_list(self):
        dict_list = [{"name": "test1"}, {"name": "test2"}]
        file_path = create_excel_from_dict_list(
            dict_list=dict_list, output_filename="test.xlsx"
        )
        self.assertTrue(os.path.exists(file_path))


class DBServiceTestCase(TestCase):
    pass


class RequestServiceTestCase(TestCase):
    pass
    # fixtures = []
    # query_params_list = [
    #     {'organization': '',
    #      'tso': '',
    #      'customer': '',
    #      'metering_unit': ''
    #      },
    #     {'organization': 'galax',
    #      'tso': 'te',
    #      'customer': 'sad',
    #      'metering_unit': '1'
    #      },
    #     {'organization': '',
    #      'tso': '',
    #      'customer': '',
    #      'metering_unit': ''
    #      },
    #     {'organization': '',
    #      'tso': '',
    #      'customer': '',
    #      'metering_unit': ''
    #      },
    # ]
    #
    # def test_get_org_selected(self):
    #     pass
    #
    # def test_get_tso_selected(self):
    #     pass
    #
    # def test_get_cust_selected(self):
    #     pass
    #
    # def test_get_mu_selected(self):
    #     pass
    #
    # def test_reset_selected_param(self):
    #     self.client.post(
    #         reverse("my_auth:login"),
    #         {
    #             "username": os.environ.get("ADMIN_USERNAME"),
    #             "password": os.environ.get("ADMIN_PASSWORD"),
    #         },
    #     )
    #     url = reverse('frontend:home')
    #     print(self.client.get(url, query_params=self.query_params_list[1]))
    #     org=get_org_selected(self.client.get(url, query_params=self.query_params_list[1]))
    #     print(org)

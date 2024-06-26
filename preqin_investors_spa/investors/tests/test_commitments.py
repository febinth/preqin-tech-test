# test_views.py
import json
from django.test import TestCase, Client
from django.urls import reverse
import requests_mock
from investors.tests.resources import constants
from investors.tests import settings_test
from investors import views


class InvestorDetailsTestCase(TestCase):

    def setUp(self):
        views.settings = settings_test
        self.client = Client()
        self.asset_classes_mock_data = {constants.ASSET_CLASSES: ["RE", "PE"]}

    def test_get_asset_classes(self):
        '''This test validates successful loading of the asset classes from json'''
        file_path = settings_test.ASSET_CLASSES_JSON_FILEPATH
        with open(file_path, "w") as f:
            json.dump(self.asset_classes_mock_data, f)
        asset_classes = views.get_asset_classes()
        self.assertEqual(
            asset_classes, self.asset_classes_mock_data[constants.ASSET_CLASSES]
        )

    @requests_mock.Mocker()
    def test_fetch_commitments_success(self, mock_request):
        '''This test validates the success scenario of retreiving commitment data'''
        asset_class = "RE"
        investor_id = 1
        mock_url = f"{settings_test.PREQIN_COMMITMENTS_API_URL}/{asset_class.lower()}/{investor_id}"
        mock_data = {"commitments": "sample commitments data"}
        mock_request.get(
            mock_url, json=mock_data, status_code=constants.STATUS_CODE_200
        )

        commitments = views.fetch_commitments(asset_class, investor_id)
        self.assertEqual(commitments, mock_data)

    @requests_mock.Mocker()
    def test_fetch_commitments_failure(self, mock_request):
        '''This test validates the failure scenario of retreiving commitment data'''
        asset_class = "Real Estate"
        investor_id = 1
        mock_url = f"{settings_test.PREQIN_COMMITMENTS_API_URL}/{asset_class.lower()}/{investor_id}"
        mock_request.get(mock_url, status_code=500)

        commitments = views.fetch_commitments(asset_class, investor_id)
        self.assertEqual(commitments, [])

    @requests_mock.Mocker()
    def test_get_commitments(self, mock_request):
        '''This test validates the rendering of commitment data'''
        asset_classes = self.asset_classes_mock_data[constants.ASSET_CLASSES]
        commitments_mock_data = {"commitments": "sample commitments data"}
        asset_class = "RE"
        investor_id = 1

        file_path = settings_test.ASSET_CLASSES_JSON_FILEPATH
        with open(file_path, "w") as f:
            json.dump(self.asset_classes_mock_data, f)

        mock_url = f"{settings_test.PREQIN_COMMITMENTS_API_URL}/{asset_class.lower()}/{investor_id}"
        mock_request.get(
            mock_url, json=commitments_mock_data, status_code=constants.STATUS_CODE_200
        )

        response = self.client.get(
            reverse(views.get_commitments, args=[asset_class, investor_id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, constants.TEMPLATE_INVESTOR_DETAILS)
        self.assertEqual(response.context["investor_id"], investor_id)
        self.assertEqual(response.context["asset_classes"], asset_classes)
        self.assertEqual(response.context["commitments"], commitments_mock_data)

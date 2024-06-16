# test_views.py
from django.test import TestCase, Client
from django.urls import reverse
import requests_mock
from investors.resources import constants
from investors import views

class InvestorViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    @requests_mock.Mocker()
    def test_fetch_investor_data_success(self, mock_request):
        mock_url = constants.PREQIN_INVESTORS_API_URL
        mock_data = [
            {'firm_id': 1, 'firm_name': 'Investor 1', 'firm_type': 'Type 1', 'date_added': '2023-01-01', 'address': 'Address 1'},
            {'firm_id': 2, 'firm_name': 'Investor 2', 'firm_type': 'Type 2', 'date_added': '2023-01-02', 'address': 'Address 2'}
        ]
        mock_request.get(mock_url, json=mock_data, status_code=constants.STATUS_CODE_200)

        response = self.client.get(reverse(views.get_investors))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, constants.TEMPLATE_INVESTORS)
        self.assertEqual(response.context['investor_data'], mock_data)
        
    def test_get_investor_details(self):
        investor_id = 1
        response = self.client.get(reverse('investor_details', args=[investor_id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, constants.TEMPLATE_INVESTOR_DETAILS)
        self.assertEqual(response.context['investor_id'], investor_id)

    @requests_mock.Mocker()
    def test_fetch_investor_data_failure(self, mock_request):
        mock_url = constants.PREQIN_INVESTORS_API_URL
        mock_request.get(mock_url, status_code=500)

        response = self.client.get(reverse(views.get_investors))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, constants.TEMPLATE_INVESTORS)
        self.assertEqual(response.context['investor_data'], [])
        self.assertContains(response, 'No investors found.')

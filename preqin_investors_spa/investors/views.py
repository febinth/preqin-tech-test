from django.shortcuts import render
from django.http import HttpResponse
from resources.constants import PREQIN_INVESTORS_API_URL, STATUS_CODE_200
import requests

# Create your views here.

def fetch_investor_data():
    url = PREQIN_INVESTORS_API_URL
    response = requests.get(url)
    if response.status_code == STATUS_CODE_200:
        return response.json()
    else:
        return []

def get_investors(request):
    investor_data=fetch_investor_data()
    return render(request, 'investors.html', {'investor_data':investor_data})
        

from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from investors.resources import constants
from investors import settings

# Create your views here.

def fetch_investor_data():
    url = settings.PREQIN_INVESTORS_API_URL
    response = requests.get(url)
    if response.status_code == constants.STATUS_CODE_200:
        return response.json()
    else:
        return []
    
def get_asset_classes():
    file_path = settings.ASSET_CLASSES_JSON_FILEPATH
    file = open(file_path, 'r')
    data = json.load(file) 
    return data.get(constants.ASSET_CLASSES)

def fetch_commitments(asset_class, investor_id):
    asset_class=asset_class.lower()
    url = f"{settings.PREQIN_COMMITMENTS_API_URL}/{asset_class}/{investor_id}"
    print(url)
    response = requests.get(url)
    if response.status_code == constants.STATUS_CODE_200:
        return response.json()
    else:
        return []    

def get_investors(request):
    investor_data=fetch_investor_data()
    return render(request, constants.TEMPLATE_INVESTORS, {'investor_data':investor_data})    

def get_investor_details(request, investor_id):
    asset_classes = get_asset_classes()
    return render(request, constants.TEMPLATE_INVESTOR_DETAILS, {'investor_id':investor_id, 'asset_classes':asset_classes})

def get_commitments(request, asset_class, investor_id):
    asset_classes = get_asset_classes()
    commitments = fetch_commitments(asset_class, investor_id)
    return render(request, constants.TEMPLATE_INVESTOR_DETAILS, {'investor_id':investor_id, 'asset_classes':asset_classes, 'commitments':commitments})

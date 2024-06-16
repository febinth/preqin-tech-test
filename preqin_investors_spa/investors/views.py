import json
import requests
from django.shortcuts import render
from investors.resources import constants
from investors import settings

# Create your views here.


def fetch_investor_data():
    '''Calls preqin-api to fetch the investors data'''
    url = settings.PREQIN_INVESTORS_API_URL
    response = requests.get(url)
    if response.status_code == constants.STATUS_CODE_200:
        return response.json()
    else:
        return []


def get_asset_classes():
    '''Reads the available asset classes from a json file '''
    file_path = settings.ASSET_CLASSES_JSON_FILEPATH
    file = open(file_path, "r")
    data = json.load(file)
    return data.get(constants.ASSET_CLASSES)


def fetch_commitments(asset_class, investor_id):
    '''Calls the preqin-api to fetch commitments data'''
    asset_class = asset_class.lower()
    url = f"{settings.PREQIN_COMMITMENTS_API_URL}/{asset_class}/{investor_id}"
    response = requests.get(url)
    if response.status_code == constants.STATUS_CODE_200:
        return response.json()
    else:
        return []


def get_investors(request):
    '''View responsible for rendering the investors page'''
    investor_data = fetch_investor_data()
    return render(
        request, constants.TEMPLATE_INVESTORS, {"investor_data": investor_data}
    )


def get_investor_details(request, investor_id):
    '''View responsible for rendering the investor details page'''
    asset_classes = get_asset_classes()
    return render(
        request,
        constants.TEMPLATE_INVESTOR_DETAILS,
        {"investor_id": investor_id, "asset_classes": asset_classes},
    )


def get_commitments(request, asset_class, investor_id):
    '''View responsible for rendering the commitments data'''
    asset_classes = get_asset_classes()
    commitments = fetch_commitments(asset_class, investor_id)
    return render(
        request,
        constants.TEMPLATE_INVESTOR_DETAILS,
        {
            "investor_id": investor_id,
            "asset_classes": asset_classes,
            "commitments": commitments,
        },
    )

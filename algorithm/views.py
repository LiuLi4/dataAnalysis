# Create your views here.

import pandas as pd
from utils import apriori
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
import json


@api_view(['POST'])
def callApriori(request):
    request.encoding = 'utf-8'

    dataPath = request.data['dataPath']
    columnList = request.data['columnList']

    df = pd.read_csv(dataPath)
    L, suppData = apriori.apriori(df, columnList, 0.1)
    rules, jsonList = apriori.generateRules(L, suppData, 0.3)
    jsonData = json.dumps(jsonList)

    return HttpResponse(jsonData, content_type="application/json")

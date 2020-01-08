import openpyxl
import requests
import json
import os
from datetime import date

from bluebird.models import KLASS_TYPES, Contragent
from bluebird.serializers import ContragentFullSerializer

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status


MIN_INNN_LEN = 10
MAX_INN_LEN = 12

TOKEN = os.environ.get('DADATA_TOKEN',
                       '')
URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'


def parse_from_file(xlsx_file):
    # bfrd_rdr = io.BytesIO(xlsx_file)
    xl = openpyxl.load_workbook(xlsx_file)
    sheet = xl.worksheets[0]
    results = []
    for row in sheet.iter_rows(min_row=3, max_row=42, min_col=2, max_col=5,
                               values_only=True):
        a, b, c, d = row
        # print('|', a, '|', b, '|', c, '|', d, '|')
        if a is not None:
            if MIN_INNN_LEN > len(str(a)) or len(str(a)) > MAX_INN_LEN:
                raise Exception(('200', 'Inn is wrong.'))
            else:
                tmp_obj = {
                    'inn': int(a),
                    'physical_address': b,
                    'excell_name': c,
                    'klass': KLASS_TYPES[d-1][0]
                }
                results.append(tmp_obj)
        else:
            continue
    return results


def get_object(pk, klass):
    try:
        return klass.objects.get(pk=pk)
    except klass.DoesNotExist:
        raise Http404


def get_dadata_data(contragent_inn: int) -> dict:
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": f"Token {TOKEN}"}
    data = {"query": contragent_inn}
    r = requests.post(
        URL,
        data=json.dumps(data),
        headers=headers
    )
    print('fetched data...')
    return r.json()


def get_data(id: int):
    contragent = get_object(id, Contragent)
    data = get_dadata_data(contragent.inn)
    print('get data...')
    sug = data.get('suggestions', None)
    if sug:
        if len(sug):
            result = {
                'ogrn': int(sug[0]['data']['ogrn']),
                'legal_address': sug[0]['data']['address']['data']['source'],
                'creation_date': date.fromtimestamp(int(int(sug[0]['data']['ogrn_date']) / 1000)),
            }
            serializer = ContragentFullSerializer(contragent, data=result)
            if serializer.is_valid():
                print('pre saving....')
                serializer.save()
                return "OK"
            return "Not OK"
        else:
            return "0 length suggestion, something wrong."
    else:
        return "No suggestion, something terribly wrong."

try:
    import openpyxl
    import requests
    import json
    import uuid
    import os
    from datetime import date
    from typing import List

    from bluebird.models import KLASS_TYPES, Contragent
    from bluebird.serializers import ContragentFullSerializer

    from django.http import Http404
    from django.template.loader import render_to_string

except ModuleNotFoundError:
    import os, sys
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    sys.path.append(parent_dir_path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'birds.settings'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.path.join(parent_dir_path, 'birds.settings'))
    print(os.environ.get("DJANGO_SETTINGS_MODULE"))
    import django
    django.setup()
    
    import openpyxl
    import requests
    import json
    import uuid
    import os
    from datetime import date
    from typing import List

    from bluebird.models import KLASS_TYPES, Contragent
    from bluebird.serializers import ContragentFullSerializer

    from django.http import Http404
    from django.template.loader import render_to_string


MIN_INNN_LEN = 10
MAX_INN_LEN = 12

TOKEN = os.environ.get('DADATA_TOKEN', '')
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
        headers=headers,
        timeout=(3.0, 5.0),
    )
    return r.json()


def get_data(id: int):
    contragent = get_object(id, Contragent)
    data = get_dadata_data(contragent.inn)
    sug = data.get('suggestions', None)
    if sug:
        if len(sug):
            result = {
                'dadata_name': sug[0]['data']['name']['full_with_opf'],
                'ogrn': int(sug[0]['data']['ogrn']),
                'kpp': int(sug[0]['data']['kpp']),
                'director_status': sug[0]['data']['management']['post'],
                'director_name': sug[0]['data']['management']['name'],
                'creation_date': date.fromtimestamp(int(int(sug[0]['data']['state']['registration_date']) / 1000)),
                'is_func': True if sug[0]['data']['state']['status'] == 'ACTIVE' else False,
                'okved': sug[0]['data']['okved'],
                'legal_address': sug[0]['data']['address']['data']['source'],
            }
            serializer = ContragentFullSerializer(contragent, data=result)
            if serializer.is_valid():
                serializer.save()
                return {'inn': contragent.inn, 'status': "OK"}
            return {'inn': contragent.inn, 'status': "Not OK",
                    'errors': serializer.errors}
        else:
            return {'inn': contragent.inn,
                    'status': "0 length suggestion, something wrong."}
    else:
        return {'inn': contragent.inn,
                'status': "No suggestions. Check, DADATA is availiable?"}


def generate_documents(data: List, contagent: Contragent):
    for d in data:
        generate_act(d, contagent)


def generate_act(data: dict, contagent: Contragent):
    data['consumer'] = contagent.excell_name
    print(render_to_string('act.html', context=data))


def create_unique_id():
    return str(uuid.uuid4())


if __name__ == '__main__':
    generate_act({'kolvo': 3.00000, 'tariff': 415.18, 'summ': 1495.44},
                 Contragent.objects.get(pk=1))

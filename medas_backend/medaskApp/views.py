import json
import re

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from medaskApp import models


# Проверяет тип страхового номера и возвращает Название СК и тип полиса
def company_name(request, insurance_number):
    insurance_list = models.CompanyInsurance.objects.all()

    # Проверяем тип страхового номера по шаблону регулярного выражения
    for insurance in insurance_list:
        pattern = insurance.insurance_number_type
        match = re.search(pattern, str(insurance_number))

        if match:
            response = {'companies names': [insurance.company_name],
                        'insurance type': insurance.insurance_type}
            return JsonResponse(response)

    # Если не нашли такой шаблон, возвращаем все значения, чтобы пользователь смог выбрать
    response = {'companies names': [], 'insurance type': 0}

    for insurance in insurance_list:
        response['companies names'].append(insurance.company_name)

    response['companies names'] = list(set(response['companies names']))

    return JsonResponse(response, safe=False)


# Убираем проверку csrf так как всего одна страница
@csrf_exempt
# Живой поиск услуг. Получаем начало строки услуги и возвращаем все валидные варианты
def services_search(request):
    user_service = str(request.body.decode('utf-8'))
    if len(user_service):
        with open('insurance_services.json') as insurance_services_file:
            insurance_services = json.load(insurance_services_file)
            response = {'services': []}
        for service in insurance_services['inservice'] + insurance_services['notservice']:
            if service.upper().startswith(user_service.upper()):
                response['services'].append(service)
        return JsonResponse(response, safe=False)
    return JsonResponse({}, safe=False)


@csrf_exempt
# Проверка клиента в "базе данных" СК. И проверка услуг.
def check_insurance(request):

    # Сразу отсеиваем, если не POST запрос
    if request.method == 'POST':
        # Проверяем подходит ли структура запроса
        try:
            data = json.loads(request.body)
            company_name = data['company name']
            insurance_type = data['insurance type']
            insurance_number = data['insurance number']
            services = data['services']
            print(data)

        except:
            return HttpResponse("Error with data")

        with open('insurance_company_db.json') as insurance_company_db_file:
            insurance_company_db = json.load(insurance_company_db_file)

        # Вначале проверяем: "Есть ли клиент в базе?"
        response = {}
        for company in insurance_company_db['insurance company']:
            if company['name'] == company_name:
                if insurance_type == 0:
                    for client in company['clients']['OMS']:
                        if client['insurance number'] == insurance_number:
                            response['end date'] = client['end date']
                            response['phone'] = company['phone']
                    if len(response) == 0:
                        return JsonResponse({})
                else:
                    for client in company['clients']['DMS']:
                        if client['insurance number'] == insurance_number:
                            response['end date'] = client['end date']
                            response['phone'] = company['phone']
                    if len(response) == 0:
                        return JsonResponse({})

        with open('insurance_services.json') as insurance_services_file:
            insurance_services = json.load(insurance_services_file)

        # Если нашли, то проверяем услуги
        response['inservice'] = [x for x in services if x in insurance_services['inservice']]
        response['notservice'] = [x for x in services if x in insurance_services['notservice']]
        response['not found service'] = [x for x in services if x not in response['inservice'] + response['notservice']]

        return JsonResponse(response, safe=False)

    else:
        return HttpResponse("Not POST request")

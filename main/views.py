from django.shortcuts import render, redirect
import sys
import main.parsers.BUTB.parser as butb
import main.parsers.goszakupki.zaku as zaku
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Parser, ParserDelete, ParserZaku, ParserZakuDelete
import uuid


# Create your views here.


@csrf_exempt
def form_data(request):
    parser_for_json = []

    result = butb.run_programm()

    for element in result:
        new_keyword = list(element.keys())[0]
        if not len(element[new_keyword]) == 0:
            print(element[new_keyword])
            for digit in range(len(element[new_keyword])):
                new_id_purchase = element[new_keyword][digit][0]
                new_name_company = element[new_keyword][digit][1]
                new_date = element[new_keyword][digit][2]
                new_name_purchase = element[new_keyword][digit][3]
                new_price = element[new_keyword][digit][4]
                new_payer_number = element[new_keyword][digit][5]
                new_location = element[new_keyword][digit][6]

                if ParserDelete.objects.filter(id_purchase=new_id_purchase).exists():
                    continue

                if not Parser.objects.filter(id_purchase=new_id_purchase).exists():
                    Parser.objects.create(
                                          keyword=new_keyword,
                                          id_purchase=new_id_purchase,
                                          name_company=new_name_company,
                                          name_purchase=new_name_purchase,
                                          date=new_date,
                                          price=new_price,
                                          payer_number=new_payer_number,
                                          location=new_location,
                                          forecast='Нету',
                                          )

                    parser_for_json.append({
                                 'keyword': new_keyword,
                                 'id_purchase': new_id_purchase,
                                 'name_company': new_name_company,
                                 'name_purchase': new_name_purchase,
                                 'date': new_date,
                                 'price': new_price,
                                 'payer_number': new_payer_number,
                                 'forecast': 'Нету',
                                })

    context = {
        'parser': parser_for_json,
    }

    return JsonResponse(context, safe=False)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        list_id = request.POST.getlist('id_list[]')
        for id_item in list_id:
            queryset = Parser.objects.filter(id_purchase=id_item)
            item = queryset.first()
            item.delete()
        table = Parser.objects.all()
        table_for_json = []
        for item in table:

            if ParserDelete.objects.filter(id_purchase=item.name_purchase).exists():
                continue

            table_for_json.append({
                'keyword': item.keyword,
                'id_purchase':  item.id_purchase,
                'name_company':  item.name_company,
                'name_purchase':  item.name_purchase,
                'date':  item.date,
                'price':  item.price,
                'payer_number':  item.payer_number,
                'forecast':  item.forecast,
            })
        context = {
            'parser': table_for_json,
        }
        return JsonResponse(context, safe=False)
    redirect('/')

@csrf_exempt
def delete_all(request):
    if request.method == 'GET':
        parser_all = Parser.objects.all()
        for item in parser_all:
            item.delete()
        return JsonResponse('ok', safe=False)
    return redirect('/')

def index(request):
    parser = Parser.objects.all()
    parser_zaku = ParserZaku.objects.all()

    context = {
        'parser': parser,
        'parser_zaku': parser_zaku,
    }
    return render(request, 'main/index.html', context)

@csrf_exempt
def complete(request):
    if request.method == 'POST':
        list_id = request.POST.getlist('id_list[]')
        list_id = list(filter(None, list_id))
        for id_item in list_id:
            queryset = Parser.objects.filter(id_purchase=id_item)
            add_delete = ParserDelete.objects.create(
                id_purchase=id_item,
            )
            item = queryset.first()
            item.delete()
        table = Parser.objects.all()
        table_for_json = []
        for item in table:
            table_for_json.append({
                'keyword': item.keyword,
                'id_purchase': item.id_purchase,
                'name_company': item.name_company,
                'name_purchase': item.name_purchase,
                'date': item.date,
                'price': item.price,
                'payer_number': item.payer_number,
                'forecast': item.forecast,
            })
        context = {
            'parser': table_for_json,
        }
        return JsonResponse(context, safe=False)
    redirect('/')


@csrf_exempt
def form_data_zaku(request):

    result = zaku.run_programm()
    parser_zaku_for_json = []

    for item in result:

        if ParserZakuDelete.objects.filter(url=item['url_purchase']).exists():
            continue

        if ParserZaku.objects.filter(url=item['url_purchase']).exists():
            continue

        ParserZaku.objects.create(
            keyword=item['keyword'],
            url=item['url_purchase'],
            name_company=item['name_company'],
            payer_number=item['payer_number'],
            main_name_purchase=item['main_name_purchase'],
            name_purchase=item['name_purchase'],
            price=item['price'],
            location=item['location'],
            forecast='Нету',
        )

        parser_zaku_for_json.append({
            'keyword': item['keyword'],
            'url': item['url_purchase'],
            'name_company': item['name_company'],
            'payer_number': item['payer_number'],
            'main_name_purchase': item['main_name_purchase'],
            'name_purchase': item['name_purchase'],
            'price': item['price'],
            'location': item['location'],
            'forecast': 'Нету',
        })

    context = {
        'parser_zaku': parser_zaku_for_json,
    }

    return JsonResponse(context, safe=False)

def delete_all_zaku(request):
    if request.method == 'GET':
        parser_zaku_all = ParserZaku.objects.all()
        for item in parser_zaku_all:
            item.delete()
        return JsonResponse('ok', safe=False)


@csrf_exempt
def complete_zaku(request):
    if request.method == 'POST':
        list_id = request.POST.getlist('id_list[]')
        list_id = list(filter(None, list_id))
        for id_item in list_id:
            queryset = ParserZaku.objects.filter(url=id_item)
            add_delete = ParserZakuDelete.objects.create(
                url=id_item,
            )
            item = queryset.first()
            item.delete()
        table = ParserZaku.objects.all()
        table_for_json = []
        for item in table:
            table_for_json.append({
                'keyword': item.keyword,
                'url': item.url,
                'name_company': item.name_company,
                'payer_number': item.payer_number,
                'main_name_purchase': item.main_name_purchase,
                'name_purchase': item.name_purchase,
                'price': item.price,
                'location': item.location,
                'forecast': item.forecast,
            })
        context = {
            'parser_zaku': table_for_json,
        }
        return JsonResponse(context, safe=False)

@csrf_exempt
def complete_all_zaku(request):
    if request.method == 'GET':
        parser_zaku_all = ParserZaku.objects.all()
        for item in parser_zaku_all:
            add_delete = ParserZakuDelete.objects.create(
                url=item.url,
            )
            item.delete()
        return JsonResponse('ok', safe=False)

@csrf_exempt
def ai_start(request):
    if request.method == 'POST':
        db_zaku = ParserZaku.objects.all()

        from main.ai_assistent.run_zaku import run_programm

        new_db_zaku = run_programm(db_zaku)

        parser_zaku = []

        for element in new_db_zaku:
            if ParserZaku.objects.filter(url=element['url']).exists():
                ParserZaku.objects.filter(url=element['url']).delete()

                ParserZaku.objects.create(
                    keyword=element['keyword'],
                    url=element['url'],
                    name_company=element['name_company'],
                    payer_number=element['payer_number'],
                    main_name_purchase=element['main_name_purchase'],
                    name_purchase=element['name_purchase'],
                    price=element['price'],
                    location=element['location'],
                    forecast=element['forecast'],
                )

                parser_zaku.append({
                    'keyword': element['keyword'],
                    'url': element['url'],
                    'name_company': element['name_company'],
                    'payer_number': element['payer_number'],
                    'main_name_purchase': element['main_name_purchase'],
                    'name_purchase': element['name_purchase'],
                    'price': element['price'],
                    'location': element['location'],
                    'forecast': element['forecast'],
                })

    context = {
            'parser_zaku': parser_zaku,
        }

    return JsonResponse(context, safe=False)

@csrf_exempt
def ai_start_butb(request):
    if request.method == 'POST':
        db = Parser.objects.all()

        from main.ai_assistent.run_butb import run_programm

        new_db = run_programm(db)

        parser = []

        for element in new_db:
            if Parser.objects.filter(id_purchase=element['id_purchase']).exists():
                Parser.objects.filter(id_purchase=element['id_purchase']).delete()

                Parser.objects.create(
                    keyword=element['keyword'],
                    id_purchase=element['id_purchase'],
                    name_company=element['name_company'],
                    payer_number=element['payer_number'],
                    date=element['date'],
                    name_purchase=element['name_purchase'],
                    price=element['price'],
                    location=element['location'],
                    forecast=element['forecast'],
                )

                parser.append({
                    'keyword': element['keyword'],
                    'id_purchase': element['id_purchase'],
                    'name_company': element['name_company'],
                    'payer_number': element['payer_number'],
                    'date': element['date'],
                    'name_purchase': element['name_purchase'],
                    'price': element['price'],
                    'location': element['location'],
                    'forecast': element['forecast'],
                })

        context = {
            'parser': parser,
        }

        return JsonResponse(context, safe=False)

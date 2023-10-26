from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.parsers.BUTB.parser import run_programm
from django.views.decorators.csrf import csrf_exempt
from .models import Parser, ParserDelete
import uuid

# Create your views here.

def generate_unique_id():
    print(uuid.uuid4())
    return str(uuid.uuid4())

@csrf_exempt
def form_data(request):
    parser_for_json = []

    result = run_programm()

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
                new_id = generate_unique_id()

                if ParserDelete.objects.filter(id_purchase=new_id_purchase).exists():
                    continue

                if not Parser.objects.filter(id=new_id).exists():
                    Parser.objects.create(
                                          keyword=new_keyword,
                                          id_purchase=new_id_purchase,
                                          name_company=new_name_company,
                                          name_purchase=new_name_purchase,
                                          date=new_date,
                                          price=new_price,
                                          payer_number=new_payer_number,
                                          id=new_id,
                                          )

                    parser_for_json.append({
                                 'keyword': new_keyword,
                                 'id_purchase': new_id_purchase,
                                 'name_company': new_name_company,
                                 'name_purchase': new_name_purchase,
                                 'date': new_date,
                                 'price': new_price,
                                 'payer_number': new_payer_number
                                })

        else:
            if not Parser.objects.filter(keyword=new_keyword).exists():
                new_id = generate_unique_id()
                Parser.objects.create(
                    keyword=new_keyword,
                    id=new_id,
                )
                parser_for_json.append({
                    'keyword': new_keyword,
                    'id': new_id,
                })
    context = {
        'table': parser_for_json,
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
            })
        context = {
            'table': table_for_json,
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
    context = {
        'parser': parser,
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
            })
        context = {
            'table': table_for_json,
        }
        return JsonResponse(context, safe=False)
    redirect('/')
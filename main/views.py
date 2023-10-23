from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .parser.parser import run_programm
from django.views.decorators.csrf import csrf_exempt
from .models import Parser
# Create your views here.


@csrf_exempt
def form_data(request):
    parser_for_json = []

    result = run_programm()

    for element in result:
        new_keyword = list(element.keys())[0]
        new_id_purchase = element[new_keyword][0][0]
        new_name_company = element[new_keyword][0][1]
        new_date = element[new_keyword][0][2]
        new_name_purchase = element[new_keyword][0][3]
        new_price = element[new_keyword][0][4]
        if not Parser.objects.filter(id=new_id_purchase).exists():
            Parser.objects.create(
                                  keyword=new_keyword,
                                  id_purchase=new_id_purchase,
                                  name_company=new_name_company,
                                  name_purchase=new_name_purchase,
                                  date=new_date,
                                  price=new_price,
                                  )
            parser_for_json.append({
                         'keyword': new_keyword,
                         'id_purchase': new_id_purchase,
                         'name_company': new_name_company,
                         'name_purchase': new_name_purchase,
                         'date': new_date,
                         'price': new_price,
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
            table_for_json.append({
                'keyword': item.keyword,
                'id_purchase':  item.id_purchase,
                'name_company':  item.name_company,
                'name_purchase':  item.name_purchase,
                'date':  item.date,
                'price':  item.price,
            })
        context = {
            'table': table_for_json,
        }
        return JsonResponse(context, safe=False)

def index(request):
    parser = Parser.objects.all()
    context = {
        'parser': parser,
    }
    return render(request, 'main/index.html', context)
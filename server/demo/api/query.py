import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .database import col, col_epidemic

"""""
根据名字查询
输入:json
{
    "keyword":"***"
}
返回: 包含所有basic信息的list
{
    "result": []
}
"""""


@api_view(["POST"])
def query(request):
    data = request.data
    keyword = data['keyword'].strip()
    if len(keyword) == 0:
        query_res = col.find()
        res_return = []
        for res in query_res:
            res["_id"] = str(res["_id"])
            res_return.append(res)
        return Response({"result": res_return}, status=status.HTTP_200_OK)

    res = []
    query_res = col.find({"basic.name": {"$regex": ".*{}.*".format(keyword)}})
    if query_res is None:
        return Response({"result": res}, status=status.HTTP_200_OK)
    else:
        for post in query_res:
            #post["_id"] = str(post["_id"])
            res.append(post["basic"])
            print(res)
        return Response({"result": res}, status=status.HTTP_200_OK)


"""""
查找指定某人,返回除_id外的PersonDocument
输入:paraments
 personal_id:***
"""""


@api_view(["GET"])
def queryperson(request):
    if request.method == "GET":
        ret = col.find_one(
            {"basic.personal_id": request.GET.get("personal_id")})
        ret2 = {}
        ret2['basic'] = ret['basic']
        ret2['routes'] = ret['routes']
        ret1 = json.dumps(ret2)
        response = HttpResponse(
            ret1, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


"""""
根据名字查询疫情
输入:json
{
    "name":"***"
}
返回: 包含所有信息的list
{
    "name":"日本东京",
    "patients":0,
    "first_time":"2021-01-03",
    "gene":"L型欧洲家系分支2.3",
    "temprature":[],
    "humidity":[]
}
"""""


@api_view(["POST"])
def queryEpidemic(request):
    if request.method == "POST":
        data = request.data
        name = data['name'].strip()
        ret = col_epidemic.find_one({"name": name})
        ret2 = {}
        ret2['name'] = ret['name']
        ret2['patients'] = ret['patients']
        ret2['first_time'] = ret['first_time']
        ret2['gene'] = ret['gene']
        ret2['temprature'] = ret['temprature']
        ret2['humidity'] = ret['humidity']
        ret1 = json.dumps(ret2)
        response = HttpResponse(
            ret1, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


"""""
根据名字查询属于疫情的Person
输入:json
{
    "name":"***" //疫情名称
}
返回: 属于该波疫情的所有人员的资料
"""""


@api_view(["POST"])
def queryEpidemicPerson(request):
    if request.method == "POST":
        data = request.data
        name = data['name'].strip()
        mydoc = col.find({"epidemic": name})
        ret = []
        for x in mydoc:
            temp = {}
            temp['epidemic'] = x['epidemic']
            temp['basic'] = x['basic']
            temp['routes'] = x['routes']
            ret.append(temp)
        ret1 = json.dumps(ret)
        response = HttpResponse(
            ret1, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


"""""
根据经纬度查询这个范围内的detail_location
输入:json
{
    "location":"***" //
    'epidemic'
}
返回: 这个范围内的所有detail_location
"""""


@api_view(["POST"])
def queryDetailLocation(request):
    if request.method == "POST":
        data = request.data
        location = data['location'].strip()
        #date = data['date'].strip()
        epidemic = data['epidemic'].strip()
        longitude, latitude = location.split(',')
        longitude = float(longitude)
        latitude = float(latitude)
        mydoc = col.find({})
        ret = []
        eps = 0.1  # 10km
        for x in mydoc:
            if epidemic != x['epidemic']:
                continue
            routes = x['routes']
            for i in routes:
                # if date != i['date']:
                # continue
                route = i['route']
                for j in route:
                    pause = j['pause']
                    temp_location = pause['location']
                    temp_location = temp_location['location']
                    temp_longitude, temp_latitude = temp_location.split(',')
                    temp_longitude = float(temp_longitude)
                    temp_latitude = float(temp_latitude)
                    if temp_longitude >= longitude - eps and temp_longitude <= longitude + eps and temp_latitude >= latitude - eps and temp_latitude <= latitude + eps:
                        if 'detail_location' in pause:
                            temp_dict = {}
                            temp_dict["detail_location"] = pause['detail_location']
                            temp_dict["relate_basic"] = x["basic"]
                            ret.append(temp_dict)

        ret1 = json.dumps(ret)
        response = HttpResponse(
            ret1, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

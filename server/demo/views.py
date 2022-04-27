import json
from pathlib import Path

import dill
from bson import json_util
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .api.database import (col, col_contacts, col_epidemic)

# Create your views here.


# 返回所有人basic中的信息
@api_view(["GET"])
def getall(request):
    if request.method == "GET":
        #ret = col.find({}, {"_id": 0, "basic.name": 1, "basic.gender":1,"basic.phone":1,"basic.age":1,"basic.addr1":1,"basic.addr2":1,"basic.personal_id":1}).distinct("basic.personal_id")
        ret = col.find()
        json_list = []
        for i in ret.distinct("basic.personal_id"):
            ret2 = col.find_one({"basic.personal_id": i})
            json_list.append(ret2["basic"])
        ret1 = json.dumps(json_list)
        response = HttpResponse(
            ret1, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

# 测试用得到所有数据


@api_view(["GET"])
def testget(request):
    if request.method == "GET":
        ret = col.find()
        ret = json_util.dumps(ret)
        response = HttpResponse(
            ret, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

# 上传一条数据


@api_view(["POST"])
def newupload(request):
    if request.method == "POST":
        data = request.data
        col.insert_one(data)
        return HttpResponse("succeed", status=status.HTTP_200_OK)


"""""
更新person数据
输入:json
{
    "oldid":"**", 旧的personal_id
    "PersonDocument":{} (注意无_id)
}
"""""


@api_view(["POST"])
def update(request):
    if request.method == "POST":
        id = request.data["oldid"]
        persondocument = request.data["PersonDocument"]
        col.delete_one({"basic.personal_id": id})

        col.insert_one(persondocument)
        return HttpResponse("succeed", status=status.HTTP_200_OK)


"""""
上传疫情数据
}
"""""


@api_view(["POST"])
def epidemicUpload(request):
    if request.method == "POST":
        data = request.data
        col_epidemic.insert_one(data)
        return HttpResponse("succeed", status=status.HTTP_200_OK)


"""""
上传密接者数据
"""""


@api_view(["POST"])
def contactUpload(request):
    if request.method == "POST":
        data = request.data
        col_contacts.insert_one(data)
        return HttpResponse("succeed", status=status.HTTP_200_OK)


"""""
获取所有密接者数据
"""""


@api_view(["GET"])
def getAllContacts(request):
    if request.method == "GET":
        ret = col_contacts.find()
        ret = json_util.dumps(ret)
        response = HttpResponse(
            ret, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


"""""
获取所有疫情数据
"""""


@api_view(["GET"])
def getAllEpidemics(request):
    if request.method == "GET":
        ret = col_epidemic.find()
        ret = json_util.dumps(ret)
        response = HttpResponse(
            ret, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


@api_view(["POST"])
def deleteperson(request):
    if request.method == "POST":
        x = col_contacts.delete_many({})

        return HttpResponse(x.deleted_count, status=status.HTTP_200_OK)


@api_view(["POST"])
def updateNull(request):
    if request.method == "POST":
        mydoc = col.find({}, {"_id": 0})
        mydoc = json_util.dumps(mydoc)
        mydoc = json.loads(mydoc)
        for x in mydoc:
            col.update_one({"basic.personal_id": x["basic"]["personal_id"]}, {
                           "$set": {"epidemic": "北京顺义"}})
        """""
        mydoc = col.find({},{ "_id": 0})
        ret = []
        for x in mydoc:
            personal_id = x['basic']['personal_id']
            x = json_util.dumps(x)
            x = json.loads(x)
            routes = x['routes']
            for i in routes:
                route = i['route']
                for j in route:
                    pause = j['pause']
                    y = pause["time"].split(':')
                    a = y[0].strip().zfill(2)
                    b = y[1].strip().zfill(2)
                    pause["time"] = a+":"+b+":"+"00"

            col.delete_one({"basic.personal_id": personal_id})
            col.insert_one(x)
        """""
        """""
        mydoc = col.find({},{"_id": 0})
        mydoc = json_util.dumps(mydoc)
        mydoc = json.loads(mydoc)
        mylist = ["二楼的超市","超市门口的凳子","旁边的电话亭","里面的贩卖机","旁边的小站台","一楼的娃娃机"]
        count = 0
        for i in mydoc:
            if i["basic"]["name"] == "未某某":
                temp = i
                routes = i["routes"]
                routes.pop(0)
                for j in routes:
                    route = j["route"]
                    for t in route:
                        #t["pause"]["detail_location"] = mylist[count]
                        if count == 1:
                            print(t["pause"]["detail_location"])
                        if t["pause"]["detail_location"] == "超市门口的凳子":
                            t["pause"]["detail_location"] = "猪肉铺"
                        elif t["pause"]["detail_location"] == "里面的贩卖机":
                            t["pause"]["detail_location"] = "水果摊"
                        elif  t["pause"]["detail_location"] == "一楼的娃娃机":
                            t["pause"]["detail_location"] = "冷柜"
                        count = count + 1
                        #print(t["pause"]["detail_location"])
                #i["epidemic"] = "北京顺义"
                i["basic"]["name"] = "未某某"
                print(i)
            #col.delete_one({"basic.personal_id":i["basic"]["personal_id"]})
            #col.insert_one(i)
            """""
        """""
        mydoc = col.find({}, {"_id": 0})
        mydoc = json_util.dumps(mydoc)
        mydoc = json.loads(mydoc)
        for i in mydoc:
            if "epidemic" not in i:
                i["epidemic"] = "北京顺义"
                col.delete_one({"basic.personal_id":i["basic"]["personal_id"]})
                col.insert_one(i)
        """""
        return HttpResponse("success", status=status.HTTP_200_OK)


@api_view(["POST"])
def initData(request):
    if request.method == "POST":
        with open("contact.json", 'r') as load_f:
            load_dict = json.load(load_f)
            for i in load_dict:
                del i["_id"]
                col_contacts.insert_one(i)
        return HttpResponse("success")

# 返回包含所有患者的地点list 热力图


@api_view(["GET"])
def getAllPlace(request):
    if request.method == "GET":
        mydoc = col.find({}, {"_id": 0})
        mydoc = json_util.dumps(mydoc)
        mydoc = json.loads(mydoc)
        ret = []
        count = 0
        for i in mydoc:
            if "routes" in i:
                routes = i["routes"]
                if routes == None:
                    continue
                for j in routes:
                    if "route" in j:
                        route = j["route"]
                        for k in route:
                            count = count + 1
                            temp_dict = {}
                            location = k["pause"]["location"]["location"]
                            lng, lat = location.split(",")
                            temp_dict["lng"] = float(lng)
                            temp_dict["lat"] = float(lat)
                            temp_dict["count"] = 10
                            ret.append(temp_dict)
        print(count)
        ret = json.dumps(ret)
        response = HttpResponse(
            ret, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

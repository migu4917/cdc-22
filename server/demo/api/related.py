import datetime
import json
import math

from bson import json_util
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .database import col

"""""
根据身份证号筛查相关信息
时间差8小时 距离差5km
输入:json
{
    "personal_id":"***" //身份证号
    "hour":8 //时间 小时
    "distance":5 //距离 千米
}
返回: 这个时间和距离范围内的所有相关信息
"""""


@api_view(["POST"])
def queryRelatedInfo(request):
    # lat lon - > distance
    # 计算经纬度之间的距离，单位为千米

    EARTH_REDIUS = 6378.137

    def rad(d):
        return d * math.pi / 180.0

    def getDistance(lat1, lng1, lat2, lng2):
        radLat1 = rad(lat1)
        radLat2 = rad(lat2)
        a = radLat1 - radLat2
        b = rad(lng1) - rad(lng2)
        s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) +
                                    math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
        s = s * EARTH_REDIUS
        return s

    if request.method == "POST":
        data = request.data
        personal_id = data['personal_id']
        doc1 = col.find_one({"basic.personal_id": personal_id})
        doc1 = json_util.dumps(doc1)
        doc1 = json.loads(doc1)  # 这个人的信息
        mydoc = col.find({})  # 所有人的信息
        mydoc = json_util.dumps(mydoc)
        mydoc = json.loads(mydoc)
        hour = data["hour"]  # 小时
        distance = data["distance"]  # 千米
        eps = 0.01*distance

        ret = []
        for i in doc1["routes"]:
            route = i["route"]
            date = i["date"]
            for j in route:
                time = j["pause"]["time"]
                location = j["pause"]["location"]["location"]
                longitude, latitude = location.split(',')
                longitude = float(longitude)
                latitude = float(latitude)

                #print(datetime.datetime.strptime(date+" "+time, "%Y-%m-%d %H: %M"))
                try:
                    datetime0 = datetime.datetime.strptime(
                        date+" "+time, "%Y-%m-%d %H:%M:%S")
                except:
                    print(doc1["basic"]["personal_id"])
                    print(doc1["basic"]["age"])
                datetime1 = (datetime0 - datetime.timedelta(hours=hour))  # 范围左
                datetime2 = (datetime0 + datetime.timedelta(hours=hour))  # 范围右
                # print(datetime0,datetime1,datetime2)
                for person in mydoc:  # 遍历所有人
                    if person["basic"]["personal_id"] == personal_id:  # 跳过自己
                        continue
                    for k in person["routes"]:
                        route2 = k["route"]
                        date2 = k["date"]
                        for t in route2:
                            time2 = t["pause"]["time"]
                            datetime3 = datetime.datetime.strptime(
                                date2+" "+time2, "%Y-%m-%d %H:%M:%S")
                            location2 = t["pause"]["location"]["location"]
                            longitude2, latitude2 = location2.split(',')
                            longitude2 = float(longitude2)
                            latitude2 = float(latitude2)

                            my_distance = round(getDistance(
                                latitude, longitude, latitude2, longitude2), 2)
                            if datetime3 >= datetime1 and datetime3 <= datetime2:
                                if my_distance <= distance:
                                    temp_dict = {}
                                    temp_dict["basic"] = doc1["basic"]
                                    temp_dict["time"] = datetime0.strftime(
                                        "%Y-%m-%d %H:%M:%S")
                                    temp_dict["location"] = j["pause"]["location"]
                                    temp_dict["relate_basic"] = person["basic"]
                                    temp_dict["relate_time"] = datetime3.strftime(
                                        "%Y-%m-%d %H:%M:%S")
                                    temp_dict["relate_location"] = t["pause"]["location"]
                                    temp_dict["distance_interval"] = my_distance
                                    if datetime3 > datetime0:
                                        temp_dict["time_interval"] = (
                                            datetime3 - datetime0).seconds
                                    else:
                                        temp_dict["time_interval"] = (
                                            datetime0 - datetime3).seconds
                                    ret.append(temp_dict)

        ret = json.dumps(ret)
        response = HttpResponse(
            ret, content_type="application/json", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

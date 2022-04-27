import json

from bson import json_util
from django.http import HttpResponse
from py2neo import Node, Relationship
from rest_framework import status
from rest_framework.decorators import api_view

from .database import col, graph, node_matcher, rel_matcher

"""""
插入一条路径
输入json
{
   "personal_id":
    "data": {
        "date":""
        "route":[]
        "remarks":""
    }
}
"""""


@api_view(["POST"])
def insertRoute(request):
    if request.method == "POST":
        # print(request.data)
        id = request.data["personal_id"]
        print(id)
        data = request.data["data"]
        print(data)
        ret = col.find_one({"basic.personal_id": id})
        ret = json_util.dumps(ret)
        ret = json.loads(ret)

        # 先删掉这个数据后面更新后再插入
        # col.delete_one({"basic.personal_id":id})
        date1 = data["date"]
        month, day, year = date1.split("-")
        if len(year) == 4:
            data["date"] = year+"-"+month.zfill(2)+"-"+day.zfill(2)
        if ret["routes"] is None:
            routes = []
        else:
            routes = list(ret["routes"])
        routes.append(data)

        routes.sort(key=lambda x: x["date"])
        #col.update_one({"basic.personal_id": id},{"$set":{"routes":routes}})
        # col.insert_one(new)

        pname = ret["basic"]["name"].strip()
        gender = "男" if ret["basic"]["gender"].strip() == "male" else "女"
        phone = ret["basic"]["phone"].strip()
        age = ret["basic"]["age"].strip()
        address = "".join(ret["basic"]["addr1"]) + ret["basic"]["addr2"]

        path = request.data["data"]["route"]
        # path = data["path"]
        tx = graph.begin()
        res = node_matcher.match("Patient", name=pname).first()
        if res is not None:
            person_node = res
            person_node["count"] += 1
            tx.push(person_node)
        else:
            person_node = Node("Patient", name=pname)
            person_node["count"] = 1
            person_node["gender"] = gender
            person_node["phone"] = phone
            person_node["age"] = age
            person_node["address"] = address
            tx.create(person_node)

        # create loc nodes
        # nodes = path["nodes"]
        nodes = [obj["pause"] for obj in path]
        loc_nodes = []
        for node in nodes:
            print(node.keys())
            time = node["time"]
            name = node["location"]["name"]
            address = node["location"]["address"]
            district = node["location"]["district"]
            location = node["location"]["location"]

            res = node_matcher.match("Location", name=name).first()
            if res is not None:
                loc_node = res
                loc_node["count"] += 1
                tx.push(loc_node)
            else:
                loc_node = Node("Location", name=name)
                loc_node["count"] = 1
                loc_node["name"] = name
                loc_node["time"] = time
                loc_node["address"] = address
                loc_node["district"] = district
                loc_node["location"] = location

                tx.create(loc_node)

            loc_nodes.append(loc_node)

            # create person loc relationship
            print(person_node)
            print(loc_node)
            res = rel_matcher.match(nodes=[person_node, loc_node]).first()
            if res is not None:
                rel = res
                rel["count"] += 1
                tx.push(rel)
            else:
                rel = Relationship(person_node, "TravelTo", loc_node)
                rel["count"] = 1
                tx.create(rel)

            # create contact and links
            if "contacts" in node:
                # contacts = node["contacts"].replace("，", ",").split(",")
                contacts = [obj["name"] for obj in node["contacts"]]
                print(len(contacts))

                for c in contacts:
                    res = node_matcher.match("Contact", name=c).first()
                    if res is not None:
                        c_node = res
                        c_node["count"] += 1
                        tx.push(c_node)
                    else:
                        c_node = Node("Contact", name=c)
                        c_node["count"] = 1
                        tx.create(c_node)

                    # link to person
                    res = rel_matcher.match(
                        nodes=[person_node, c_node]).first()
                    if res is not None:
                        rel = res
                        rel["count"] += 1
                        tx.push(rel)
                    else:
                        rel = Relationship(person_node, "With", c_node)
                        rel["count"] = 1
                        tx.create(rel)

                    # link to location
                    res = rel_matcher.match(nodes=[c_node, loc_node]).first()
                    if res is not None:
                        rel = res
                        rel["count"] += 1
                        tx.push(rel)
                    else:
                        rel = Relationship(c_node, "Locate", loc_node)
                        rel["count"] = 1
                        tx.create(rel)

        # create edges
        # edges = path["edges"]
        for obj in path:
            if "travel" not in obj:
                obj["travel"] = None
        edges = [obj["travel"] for obj in path]
        edges = edges[:-1] if len(edges) == len(loc_nodes) else edges
        for i, e in enumerate(edges):
            if e is None:
                continue
            if "transform" not in e:
                continue
            # traffic = e["traffic"]
            traffic = e["transform"]
            # if "description" in e:
            #    description = e["description"]
            if "note" in e:
                description = e["note"]
            else:
                description = ""
            from_node = loc_nodes[i]
            to_node = loc_nodes[i + 1]

            res = rel_matcher.match(nodes=[from_node, loc_node]).first()
            if res is not None:
                rel = res
                rel["count"] += 1
                tx.push(rel)
            else:
                rel = Relationship(from_node, "To", to_node)
                rel["count"] = 1
                rel["traffic"] = traffic
                rel["description"] = description
                tx.create(rel)
        tx.commit()
        col.update_one({"basic.personal_id": id}, {"$set": {"routes": routes}})

        response = HttpResponse("succeed", status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

from py2neo import Node, Relationship
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .database import col, graph, node_matcher, rel_matcher


@api_view(["POST"])
def upload(request):
    if request.method == "POST":
        data = request.data
        print(request.data)
        pname = data["basic"]["name"].strip()
        gender = "男" if data["basic"]["gender"].strip() == "male" else "女"
        phone = data["basic"]["phone"].strip()
        age = data["basic"]["age"].strip()
        address = "".join(data["basic"]["addr1"]) + data["basic"]["addr2"]

        routes = data["routes"]
        if routes is not None:
            for r in routes:
                path = r["route"]
                #path = data["path"]
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
                #nodes = path["nodes"]
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
                    res = rel_matcher.match(
                        nodes=[person_node, loc_node]).first()
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
                        #contacts = node["contacts"].replace("，", ",").split(",")
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
                            res = rel_matcher.match(
                                nodes=[c_node, loc_node]).first()
                            if res is not None:
                                rel = res
                                rel["count"] += 1
                                tx.push(rel)
                            else:
                                rel = Relationship(c_node, "Locate", loc_node)
                                rel["count"] = 1
                                tx.create(rel)

                # create edges
                #edges = path["edges"]
                edges = [obj["travel"] for obj in path]
                edges = edges[:-1] if len(edges) == len(loc_nodes) else edges
                for i, e in enumerate(edges):
                    if e is None:
                        continue
                    #traffic = e["traffic"]
                    traffic = e["transform"]
                    # if "description" in e:
                    #    description = e["description"]
                    if "note" in e:
                        description = e["note"]
                    else:
                        description = ""
                    from_node = loc_nodes[i]
                    to_node = loc_nodes[i+1]

                    res = rel_matcher.match(
                        nodes=[from_node, loc_node]).first()
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
        col.insert_one(data)
        return Response({"result": "upload successfully!"}, status=status.HTTP_200_OK)

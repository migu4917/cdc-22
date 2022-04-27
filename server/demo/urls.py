from django.urls import path
from . import views
from .api import query, route, upload, related

app_name = "server"
urlpatterns = [
    path("api/upload", upload.upload, name="upload"),

    path("api/query", query.query, name="query"),
    path("api/queryEpidemic", query.queryEpidemic),  # 查询某个疫情数据
    path("api/queryEpidemicPerson", query.queryEpidemicPerson),  # 查询属于该波疫情的所有人员的资料
    # 查询这个范围内的所有detail_location
    path("api/queryDetailLocation", query.queryDetailLocation),
    path("api/queryperson", query.queryperson),

    path("api/insertroute", route.insertRoute),

    path("api/queryRelatedInfo", related.queryRelatedInfo),

    path("api/getall", views.getall),
    path("api/testget", views.testget),
    path("api/newupload", views.newupload),
    path("api/update", views.update),
    path("api/delete", views.deleteperson),
    path("api/epidemicUpload", views.epidemicUpload),  # 上传疫情数据
    path("api/contactUpload", views.contactUpload),  # 上传密接者数据
    path("api/getAllContacts", views.getAllContacts),  # 得到所有密接者数据
    path("api/getAllEpidemics", views.getAllEpidemics),  # 得到所有疫情数据
    path("api/updateNull", views.updateNull),
    path("api/getAllPlace", views.getAllPlace),
    path("api/initData", views.initData),
    # path("api/text2Info", views.text2Info),
    # path("api/download", views.download_template),
    # path("api/downloadDocx", views.download_docx),
]

from django.urls import path
from . import views
from .api import query, route, upload, related, login

app_name = "server"
urlpatterns = [
    path("api/upload", upload.upload, name="upload"),

    path("api/query", query.query, name="query"),
    path("api/queryEpidemic", query.queryEpidemic,
         name="queryEpidemic"),  # 查询某个疫情数据

    path("api/queryEpidemicPerson", query.queryEpidemicPerson,
         name="queryEpidemicPerson"),  # 查询属于该波疫情的所有人员的资料

    # 查询这个范围内的所有detail_location
    path("api/queryDetailLocation", query.queryDetailLocation,
         name="queryDetailLocation"),

    path("api/queryperson", query.queryperson, name="queryperson"),

    path("api/insertroute", route.insertRoute, name="insertroute"),

    path("api/queryRelatedInfo", related.queryRelatedInfo, name="queryRelatedInfo"),

    path("api/getall", views.getall, name="getall"),

    path("api/testget", views.testget, name="testget"),

    path("api/newupload", views.newupload, name="newupload"),

    path("api/update", views.update, name="update"),

    path("api/delete", views.deleteperson, name="delete"),

    path("api/epidemicUpload", views.epidemicUpload,
         name="epidemicUpload"),  # 上传疫情数据

    path("api/contactUpload", views.contactUpload,
         name="contactUpload"),  # 上传密接者数据

    path("api/getAllContacts", views.getAllContacts,
         name="getAllContacts"),  # 得到所有密接者数据

    path("api/getAllEpidemics", views.getAllEpidemics,
         name="getAllEpidemics"),  # 得到所有疫情数据

    path("api/updateNull", views.updateNull, name="updateNull"),

    path("api/getAllPlace", views.getAllPlace, name="getAllPlace"),

    path("api/initData", views.initData, name="initData"),

    path("api/login", login.login, name="login"),

    # path("api/text2Info", views.text2Info),
    # path("api/download", views.download_template),
    # path("api/downloadDocx", views.download_docx),
]

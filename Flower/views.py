from django.http import JsonResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.authtoken.views import APIView, AuthTokenSerializer

from rest_framework.utils import json
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from Flower.models import Data, Recognition, Card


# Create your views here.
class DataView(View):
    def get(self, request):
        data = Data.objects.filter(is_delete=False)
        total = Data.objects.filter(is_delete=False).count()
        data_list = list(data.values('id', 'time', 'temperature', 'humidty', 'gas'))
        data = {
            "code": 200,
            "msg": "success",
            "total": total,
            "data": data_list
        }
        return JsonResponse(data)

class CardView(View):
    def get(self, request):
        data = Card.objects.filter(is_delete=False)
        total = Card.objects.filter(is_delete=False).count()
        data_list = list(data.values('id', 'time', 'uid', 'num'))
        data = {
            "code": 200,
            "msg": "success",
            "total": total,
            "data": data_list
        }
        return JsonResponse(data)


class RecognitionView(View):
    def get(self, request):
        recognition = Recognition.objects.filter(is_delete=False)
        total = Recognition.objects.filter(is_delete=False).count()
        recognition_list = list(recognition.values('id', 'time', 'result', 'img'))
        data = {
            "code": 200,
            "msg": "success",
            "total": total,
            "data": recognition_list
        }
        return JsonResponse(data)

    def delete(self, request):
        recognition_json = request.body.decode()
        recognition_dict = json.loads(recognition_json)
        id = recognition_dict.get('id')
        recognition = Recognition.objects.get(id=id)
        recognition.is_delete = True
        recognition.save()
        return JsonResponse({
            "code": 200,
            "msg": "success"
        })

    def post(self, request):
        recognition_json = request.body.decode()
        recognition_dict = json.loads(recognition_json)
        Recognition.objects.create(**recognition_dict)
        return JsonResponse({
            "code": 200,
            "msg": "success"
        })

    def put(self, request):
        recognition_json = request.body.decode()
        recognition_dict = json.loads(recognition_json)
        id = recognition_dict.get('id')
        time = recognition_dict.get('time')
        result = recognition_dict.get('result')
        img = recognition_dict.get('img')
        recognition = Recognition.objects.get(id=id)
        recognition.time = time
        recognition.result = result
        recognition.img = img
        recognition.save()
        return JsonResponse({
            "code": 200,
            "msg": "success"
        })


# 用户注册
class Register(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            resp = {
                'status': False,
                'data': '用户名已被注册'
            }
        else:
            user = User.objects.create_user(username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            resp = {
                'status': True,
                'token': token.key,
                'user_id': user.pk,
                'user_name': user.username,
            }
        return Response(resp)


# 用户登录
class Login(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status': True,
            'token': token.key,
            'user_id': user.pk,
            'user_name': user.username,
        })

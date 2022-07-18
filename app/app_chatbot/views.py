from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json


def index(request):
    return render(request, "chatroom.html")


class NLPView(APIView):
    def post(self, request):
        data = request.data
        user = data['sender']
        message = data['message'].strip(' ')
        r = requests.post('http://localhost:5005/webhooks/rest/webhook', json=data)
        res = json.loads(r.text)
        return Response(res)


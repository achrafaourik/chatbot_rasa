from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json


def index(request):
    return render(request, "chatroom.html")


class NlpValidationView(APIView):
    def post(self, request):
        data = request.data
        user = data['sender']
        message = data['message'].strip(' ')
        r = requests.get('http://localhost:5005/conversations/' + user + '/tracker')
        response = json.loads(r.text)
        events = response['events']
        # print(response['latest_message'])
        previous_questions = [x['name'] for x in events if 'name' in x]
        # print(previous_questions)
        previous_utterances = [x for x in previous_questions if x in utterances_digits]
        # print(previous_utterances)
        if len(previous_utterances) == 0:
            print("len == 0")
            r1 = requests.post('http://localhost:5005/webhooks/rest/webhook', json=data)
            r = requests.get('http://localhost:5005/conversations/' + user + '/tracker')
            response = json.loads(r.text)
            events = response['events']
            previous_questions = [x['name'] for x in events if 'name' in x]
            previous_utterances_choices = previous_questions[-2]
            print(previous_utterances_choices)
            res = json.loads(r1.text)[0]
            if previous_utterances_choices in utterances_choices:
                res['choices'] = questions_choices[previous_utterances_choices]
            print(res)
            if len(json.loads(r1.text)) > 1:
                return Response([res] + [json.loads(r1.text)[1]])
            return Response([res])
        last_question = previous_utterances[-1]
        print(message)
        print(last_question)
        try:
            number = int(message)
            print('digit')
            data['message'] = str(number) + ' ' + dict_questions[last_question]
        except ValueError:
            print('VALUE ERROR!!')
        r1 = requests.post('http://localhost:5005/webhooks/rest/webhook', json=data)
        r = requests.get('http://localhost:5005/conversations/' + user + '/tracker')
        response = json.loads(r.text)
        events = response['events']
        print(response['latest_message'])
        previous_questions = [x['name'] for x in events if 'name' in x]
        print(previous_questions)
        previous_utterances = [x for x in previous_questions if x in utterances_digits]
        print(previous_utterances)
        previous_utterances_choices = previous_questions[-2]
        print(previous_utterances_choices)
        res = json.loads(r1.text)[0]
        if previous_utterances_choices in utterances_choices:
            res['choices'] = questions_choices[previous_utterances_choices]
        print(res)
        if len(json.loads(r1.text)) > 1:
            return Response([res] + [json.loads(r1.text)[1]])
        return Response([res])

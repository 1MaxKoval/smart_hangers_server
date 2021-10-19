from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render


# Create your views here.
@api_view(['GET'])
def hello_view(request):
    return Response(data={'message': 'Hello World!'})

def test_commit_func():
    return None
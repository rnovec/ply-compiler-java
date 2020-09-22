"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from compiler.lexer import JavaLexer
from compiler.parser import JavaParser
import re
import json

@csrf_exempt
def compile(request):
    json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
    program = json_data['program']
    JL = JavaLexer()
    JP = JavaParser()
    tokensFile, simbolTable, lexerr = JL.tokenizer(program)
    errors, names = JP.compile(program)
    for t in simbolTable:
        if re.match(r'ID', t['type']):
            try:
                t['vartype'] = names[t['value']]['vartype']
            except Exception as err:
                pass
    return JsonResponse({'simbolTable': simbolTable, 'tokensFile': tokensFile, 'errors': lexerr + errors})

urlpatterns = [
    path('compile', compile),
]

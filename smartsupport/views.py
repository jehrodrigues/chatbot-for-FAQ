from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets

from django.shortcuts import render
from serializers import RecordSerializer
from .models import Record

# Create your views here

@api_view(['GET', 'POST'])
def record_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        record = Record.objects.all()
        #serializer = RecordSerializer(record, many=True)
        metrics = RecordSerializer().set_update()

        return Response(metrics)

    elif request.method == 'POST':
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            param = request.POST
            print param.__getitem__('name'),'\n'
            sentences = RecordSerializer().main(param.__getitem__('name'))
            return Response(sentences)
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
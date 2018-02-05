# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

import requests
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from .models import User,Token, Note, Image
from .serializers import ImageSerializer, NoteSerializer
from drf_extra_fields.fields import Base64ImageField


def convert_image_to_base64(url):
    return base64.b64encode(requests.get(url).content)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return JsonResponse({'Token': token.key, 'id': token.user_id})


class NoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=Note):
        user = get_object_or_404(User, pk=pk)
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk, format=None):

        user = get_object_or_404(User, pk=pk)
        notes = Note.objects.filter(owner=user)
        serializer = NoteSerializer(notes, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class ImageView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        base64_data = convert_image_to_base64(request.data['image'])
        data = {"image": base64_data}
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors)

    def get(self, request, pk, format=None):
        images = Image.objects.filter(owner=pk)
        return JsonResponse({"images": images})

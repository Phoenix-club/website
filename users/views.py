from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
from rest_framework import generics
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def landing(request):
    return HttpResponse("landing.html")


class EventListView(generics.ListAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class RegistrationView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        """Manually handle OPTIONS request with CORS headers"""
        response = JsonResponse({"message": "OPTIONS request allowed"})
        response["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Log uploaded files for debugging
            if request.FILES:
                logger.info(f"Uploaded Files: {request.FILES}")

            return Response(
                {"message": "Registration created successfully."},
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            logger.warning(f"Validation Error: {e.detail}")
            return Response(
                {"errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return Response(
                {"message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

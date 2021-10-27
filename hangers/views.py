from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hangers.api.serializers import StatusSerializer, TemperatureAtLocationSerializer
from hangers.models import Status, TemperatureAtLocation
from hangers import utils
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET'])
def hello_view(request):
    return Response(data={'message': 'Hello World!'})


class StatusView(APIView):

    def post(self, request):
        queryset = Status.objects.all()
        if len(queryset) != 0:
            return Response(data={'error': 'The status has already been created!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StatusSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def get(self, request):
        queryset = Status.objects.all()
        if len(queryset) == 0:
            return Response(data={'error': 'The status has not been set!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(queryset[0], context={'request': request})
        return Response(data=serializer.data)

    def patch(self, request):
        queryset = Status.objects.all()
        if len(queryset) == 0:
            return Response(data={'error': 'The status has not been set!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(queryset[0], data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class TemperatureAtLocationView(APIView):

    def post(self, request):
        queryset = Status.objects.all()
        # Create a new TemperatureLocation
        if len(queryset) == 0:
            serializer = TemperatureAtLocationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data)
        else:
            temperature_object = queryset[0]
            ser = TemperatureAtLocationSerializer(temperature_object, data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(data=ser.data)

    def get(self, request):
        queryset = TemperatureAtLocation.objects.all()
        if len(queryset) == 0:
            return Response(data={'error': 'The environment temperature has not been set!'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = TemperatureAtLocationSerializer(queryset[0])
        return Response(data=serializer.data)


@api_view(['GET'])
def recommendations(request):
    return Response(data=utils.recommend_clothing())

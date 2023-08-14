from rest_framework import generics, permissions, decorators, exceptions
from rest_framework.parsers import FormParser
from events.models import Event
from events.serializers import EventsSerializer
from utils import custom_response, custom_parsers
# Create your views here.


@decorators.api_view(["GET"])
def getAGMEvent(request):
    if request.method == "GET":
        agm_event = Event.objects.get(is_agm=True)
        serializer = EventsSerializer(agm_event)
        return custom_response.Success_response(msg="agm event", data=serializer.data)
    else:
        raise exceptions.MethodNotAllowed


class EventView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = Event.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="events", data=serializer.data)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    lookup_field = "id"

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset


class EventViewPublic(generics.ListAPIView):
    serializer_class = EventsSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="events")

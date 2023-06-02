from rest_framework import generics, permissions, exceptions, status
from membership import serializers
from membership.models import WhyJoinMan, JoiningStep, FAQs, HomePage, WhyWeAreUnique, OurMembers
from rest_framework.parsers import FormParser
from utils import custom_parsers, custom_response, custom_permissions
# Create your views here.


class WhyJoinManView(generics.ListCreateAPIView):
    serializer_class = serializers.WhyJoinManSerializers
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return WhyJoinMan.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="Why Join MAN Listing", data=serializer.data)


class WhyJoinManDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.WhyJoinManSerializers
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return WhyJoinMan.objects.all()


class JoiningStepView(generics.ListCreateAPIView):
    serializer_class = serializers.JoiningStepSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return JoiningStep.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="Steps To Join Man", data=serializer.data)


class JoiningStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.JoiningStepSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return JoiningStep.objects.all()


class FAQsView(generics.ListCreateAPIView):
    serializer_class = serializers.FAQsSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return FAQs.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="FAQs Listings", data=serializer.data)


class FAQsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FAQsSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return FAQs.objects.all()


class HomePageView(generics.GenericAPIView):
    serializer_class = serializers.HomePageSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)

    def get(self, request):
        try:
            home_data = HomePage.objects.get(id=1)
            serializer = self.serializer_class(home_data)

            return custom_response.Success_response(msg="home main", data=serializer.data)
        except HomePage.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        about_data = HomePage.objects.get(id=1)
        serializer = self.serializer_class(about_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="home main updated", data=serializer.data)


class WhyWeAreUniqueView(generics.ListCreateAPIView):
    serializer_class = serializers.WhyWeAreUniqueSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser)

    def get_queryset(self):
        return WhyWeAreUnique.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="why we are unique data", data=serializer.data)


class WhyWeAreUniqueDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.WhyWeAreUniqueSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser)
    lookup_field = "id"

    def get_queryset(self):
        return WhyWeAreUnique.objects.all()


class OurMembersView(generics.ListCreateAPIView):
    serializer_class = serializers.OurMembersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OurMembers.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="our members", data=serializer.data)


class OurMembersDetialView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.OurMembersSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OurMembers.objects.all()


# PUBLIC VIEWS HERE


class WhyJoinManPublicView(generics.ListAPIView):
    serializer_class = serializers.WhyJoinManSerializers

    def get_queryset(self):
        return WhyJoinMan.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="Why Join MAN Listing", data=serializer.data)


class JoiningStepPublicView(generics.ListAPIView):
    serializer_class = serializers.JoiningStepSerializer

    def get_queryset(self):
        return JoiningStep.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="Steps To Join Man", data=serializer.data)


class FAQsPublicView(generics.ListAPIView):
    serializer_class = serializers.FAQsSerializer

    def get_queryset(self):
        return FAQs.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="FAQs Listing", data=serializer.data)


class WhyWeAreUniquePublicView(generics.ListAPIView):
    serializer_class = serializers.WhyWeAreUniqueSerializer

    def get_queryset(self):
        return WhyWeAreUnique.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="why we are unique data", data=serializer.data)


class OurMembersPublicView(generics.ListAPIView):
    serializer_class = serializers.OurMembersSerializer

    def get_queryset(self):
        return OurMembers.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="our members", data=serializer.data)

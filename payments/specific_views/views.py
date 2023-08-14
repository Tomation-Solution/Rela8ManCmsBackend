from rest_framework import generics, permissions, status
from utils import custom_response, custom_permissions, mailer
from payments.specific_views.serializers import LuncheonSerializer, MembersAGMRegistrationSerializer, ExhibitionBootSerializer, ExhibitorsAGMRegistrationSerializer, OthersAGMRegistrationSerializer, AGMInvitationSerializer, AGMInvitationVerificationSerializer, QuickRegistrationSerializer

from payments.models import Luncheon, MembersAGMRegistration, ExhibitionBoot, ExhibitorsAGMRegistration, OthersAGMRegistration, AGMInvitation, QuickRegistration
from django.forms import model_to_dict

from utils.extras import initialize_payment
from django.template.loader import render_to_string


# AGM VIEWS
class LuncheonViews(generics.UpdateAPIView):
    serializer_class = LuncheonSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Luncheon.objects.all()


class ExhibitionBootView(generics.ListCreateAPIView):
    serializer_class = ExhibitionBootSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExhibitionBoot.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="exhibition boots")


class ExhibitionBootDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExhibitionBootSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return ExhibitionBoot.objects.all()


class MembersAGMRegistrationView(generics.GenericAPIView):
    serializer_class = MembersAGMRegistrationSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return MembersAGMRegistration.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="agm registrations members", data=serializer.data)

    def post(self, request):
        body = request.data
        gatewaytype = request.POST.get("gatewaytype")
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        registration = MembersAGMRegistration.objects.get(
            email=serializer.data["email"], ref=serializer.data["ref"])

        payment_amount = registration.amount_to_pay

        buyer_obj = model_to_dict(registration)

        reason_for_payment = "member_agm_purchase"

        return initialize_payment(reason_for_payment=reason_for_payment,
                                  gatewaytype=gatewaytype,
                                  amount=payment_amount, buyer_obj=buyer_obj)


class ExhibitorsAGMRegistrationView(generics.GenericAPIView):
    serializer_class = ExhibitorsAGMRegistrationSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return ExhibitorsAGMRegistration.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="agm registrations exhibitors", data=serializer.data)

    def post(self, request):
        body = request.data
        gatewaytype = request.GET.get("gatewaytype", "")
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        registration = ExhibitorsAGMRegistration.objects.get(
            email=serializer.data["email"], ref=serializer.data["ref"])

        payment_amount = registration.amount_to_pay

        buyer_obj = model_to_dict(registration)

        reason_for_payment = "exhibitor_agm_purchase"

        return initialize_payment(reason_for_payment=reason_for_payment,
                                  gatewaytype=gatewaytype,
                                  amount=payment_amount, buyer_obj=buyer_obj)


class OthersAGMRegistrationView(generics.GenericAPIView):
    serializer_class = OthersAGMRegistrationSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return OthersAGMRegistration.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="agm registrations others", data=serializer.data)

    def post(self, request):
        body = request.data
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        registration = OthersAGMRegistration.objects.get(
            email=serializer.data["email"], ref=serializer.data["ref"])

        reg_obj = model_to_dict(registration)

        email_subject = f"Registration for Annual General Meeting"

        html_message = render_to_string('EventTrainingRegistration.html', {
                                        'ref_no': reg_obj["ref"], 'client_mail': reg_obj["email"], 'registration_name': f"MAN AGM event with the title of {reg_obj['type']}", 'type': "AGM Event"})

        # my send mail utility class
        mailer.sib_send_mail(to=[{"email": reg_obj["email"], "name": reg_obj["company_name"]}],
                             html_content=html_message, subject=email_subject)

        return custom_response.Success_response(msg='other agm registration', data=serializer.data)


class AGMInvitationView(generics.GenericAPIView):
    serializer_class = AGMInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AGMInvitation.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="agm invitations", data=serializer.data)

    def post(self, request):
        body = request.data
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        invitation = AGMInvitation.objects.get(
            ref=serializer.data["ref"], email=serializer.data["email"])
        invitation_obj = model_to_dict(invitation)

        email_subject = f"Invitaion to MAN's Annual General Meeting"

        html_message = render_to_string('EventTrainingRegistration.html', {
                                        'ref_no': invitation_obj["ref"], 'client_mail': invitation_obj["email"], 'registration_name':  invitation_obj['type'], 'type': "AGM Event"})

        # my send mail utility class
        mailer.sib_send_mail(to=[{"email": invitation_obj["email"], "name": invitation_obj["company_name"]}],
                             html_content=html_message, subject=email_subject)

        return custom_response.Success_response(msg='other agm registration', data=serializer.data)


class AGMInvitationVerification(generics.GenericAPIView):
    serializer_class = AGMInvitationVerificationSerializer

    def post(self, request):

        body = request.data
        serializer = self.serializer_class(data=body)
        if serializer.is_valid(raise_exception=True):
            try:
                invite = AGMInvitation.objects.get(
                    ref=body["ref"], type=body["type"])
                if invite.is_valid == True:
                    invite.is_valid = False
                    invite.save()
                    return custom_response.Success_response(msg="invitaion verified")
                return custom_response.Response(msg="invalid invitation code", status=status.HTTP_401_UNAUTHORIZED)
            except:
                return custom_response.Response({"message": "not found"}, status=status.HTTP_400_BAD_REQUEST)


class QuickRegistrationView(generics.GenericAPIView):
    serializer_class = QuickRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuickRegistration.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="quick registration", data=serializer.data)

    def post(self, request):

        body = request.data
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="quick registration", data=serializer.data)


# PUBLIC VIEWS


class ExhibitionBootPublicView(generics.ListAPIView):
    serializer_class = ExhibitionBootSerializer

    def get_queryset(self):
        return ExhibitionBoot.objects.filter(is_occupied=False)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="exhibition boots")


class LuncheonPublicView(generics.ListAPIView):
    serializer_class = LuncheonSerializer

    def get_queryset(self):
        return Luncheon.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="luncheon prices")

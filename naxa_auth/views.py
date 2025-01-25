from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import GetUserSerializer
from .serializers import RegisterSerializer, UpdateUserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from .models import VerificationCode
from django.utils import timezone
import random
from .send_email import EmailSender
from .models import UserProfile

from rest_framework.views import APIView
from datetime import timedelta


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    allowed_methods = ("POST",)

    def mask_email(self, email):
        name, domain = email.split("@")
        name = name[:1] + "***" + name[-1:] if len(name) > 1 else name + "***"
        return f"{name}@{domain}"

    def create(self, request, *args, **kwargs):
        otp = random.randint(100000, 999999)

        # Extract data from request
        password = request.data.get("password")
        password2 = request.data.get("password2")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")

        # Validate user data
        serializer = self.get_serializer(
            data={
                "username": email,
                "password": password,
                "password2": password2,
                "email": email,
            }
        )

        # Save user
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save user
        user = serializer.save()

        # Create verification code
        VerificationCode.objects.create(
            user=user, code=otp, created_at=timezone.localtime(timezone.now())
        )

        # Update user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile_serializer = UpdateUserProfileSerializer(
            instance=profile, data={"phone_number": phone_number}, partial=True
        )
        if not profile_serializer.is_valid():
            user.delete()
            return Response(
                profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        profile_serializer.save()

        # Send OTP email
        try:
            EmailSender.send_otp_email(user, otp)
        except Exception as e:
            user.delete()
            # Use logging instead of print
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error sending OTP email: {str(e)}")
            return Response(
                {"message": "Error sending verification code"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Mask email for response
        masked_email = self.mask_email(email)
        message = (
            f"User created successfully. A verification code has been sent to your email ({masked_email}). "
            f"Please verify your account immediately before the session expires in 10 minutes."
        )

        return Response(
            {"message": message, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def mask_email(self, email):
        parts = email.split("@")
        masked_username = parts[0][:2] + "*" * (len(parts[0]) - 2)
        return f"{masked_username}@{parts[1]}"


class ResendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp = random.randint(100000, 999999)

        try:
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            verification_model = VerificationCode.objects.get(user=user)
        except VerificationCode.DoesNotExist:
            return Response(
                {"message": "No verification code found for the given user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active:
            return Response(
                {"message": "ACCOUNT ALREADY ACTIVATED, NO NEED TO RESEND OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        time_remaining = (
            verification_model.created_at
            + timedelta(minutes=10)
            - timezone.localtime(timezone.now())
        )
        if time_remaining > timedelta(minutes=0):

            # If the time remaining is more than 0, return an error with the time remaining
            return Response(
                {
                    "message": f"PLEASE WAIT FOR {time_remaining.seconds // 60} MINUTES AND {time_remaining.seconds % 60} SECONDS BEFORE SENDING ANOTHER OTP"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        verification_model.code = otp
        verification_model.otp_used = False
        verification_model.created_at = timezone.localtime(timezone.now())
        verification_model.save()
        try:
            EmailSender.send_otp_email(user, otp)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Error sending email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response({"message": "OTP SENT SUCCESSFULLY"}, status=status.HTTP_200_OK)


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        try:
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        if user.is_active:
            return Response(
                {"message": "ACCOUNT ALREADY ACTIVATED"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = request.data.get("otp", None)
        # user = User.objects.get(email=request.data.get('email'))
        verification_model = VerificationCode.objects.get(user=user)
        if verification_model.code == otp and timezone.localtime(
            timezone.now()
        ) < verification_model.created_at + timedelta(minutes=10):
            user.is_active = True
            verification_model.otp_used = True
            verification_model.save()
            user.save()
            return Response(
                {"message": "ACCOUNT ACTIVATED SUCCESSFULLY"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": " Invalid OTP or OTP expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

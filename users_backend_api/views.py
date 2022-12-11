from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .tokens import get_tokens_for_user
from .models import OTPModel
from .serializers import MyUserSerializer
from rest_framework.views import APIView
from .models import MyUser
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from .utilities import sendMessage
import random
from rest_framework_simplejwt.tokens import RefreshToken


# Backend methods:
class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Logged out succesfully")


# CRUD for User:
@api_view(['POST'])
def createUser(request):
    req_fields = ['username', 'email', 'password']
    all_prs = True
    for field in req_fields:
        all_prs = all_prs and (field in request.data)
    if not all_prs:
        return Response(data={"message": "Required fields not present"},status=status.HTTP_400_BAD_REQUEST)

    try:
        user = MyUser.objects.get(username=request.data.get('username'))
    except:
        user = None
    if user:
        return Response({"message": "A user with this username already exists"},status=status.HTTP_400_BAD_REQUEST)

    try:
        user = MyUser(**request.data)
        user.set_password(request.data.get('password'))
        user.save()
        return Response(data = {'message': 'You have been registered, now you can login' })
    except:
        return Response(data={"message": "User not created"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    try:
        user = MyUser.objects.get(username=request.data.get('login_identifier'))
    except:
        try:
            user = MyUser.objects.get(email=request.data.get('login_identifier'))
        except:
            user = None
    if not user:
        return Response({"message": "Invalid username"},status=status.HTTP_401_UNAUTHORIZED)

    if user.check_password(request.data.get('password')):
        refresh = RefreshToken.for_user(user)
        return Response(data={ 'refresh': str(refresh), 'access': str(refresh.access_token) })

    return Response(data={"message": "Username or password inccorect"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user(request, pk=None):
    if pk:
        try:
            user = MyUser.objects.get(pk=pk);
        except:
            return Response(data={'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        user, token = response


    serializer = MyUserSerializer(user)

    # GET for getting
    if request.method == "GET":
        return Response(data={**serializer.data})
    # Check if authenticated user is editing his own details
    elif not token:
        return Response(data={'message' : 'Insufficient permission'}, status=status.HTTP_403_FORBIDDEN)
    # PUT for updating
    if request.method == "PUT" and request.data:
        username = serializer.data['username']
        serializer = MyUserSerializer(user, data = request.data, partial=True)
        serializer.initial_data["username"] = username
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message' : 'Updated user', 'm2':serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(data={'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    # DELETE for deleting
    elif request.method == "DELETE":
        user.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Verify email:
@api_view(['POST'])
def sendOTP(request):
    user = MyUser.objects.get(username=request.data.get('username'))

    try:
        otp_row = OTPModel.objects.get(user = user)
    except:
        otp_row = None

    if otp_row:
        otp_row.delete()
    otp = random.randint(100000,999999)
    newOTP = OTPModel(user=user, otp=otp)
    newOTP.save()
    sendMessage(user.email, f'Your OTP is {otp}')
    print()
    print("otp:", otp)
    print()
    return Response(data={"message": "OTP send"})


@api_view(['POST'])
def verifyOTP(request):
    user = MyUser.objects.get(username=request.data.get('username'))
    otp = request.data.get('otp')
    if not (user and otp):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    otp = str(otp)
    try:
        otp_row = OTPModel.objects.get(user=user)
    except:
        otp_row = None
    if not otp_row:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if (otp_row.otp == otp) and (otp_row.creation_date_time + 300 > timezone.now()):
        otp_row.delete()
        token = get_tokens_for_user(user)

        return Response(data={"token": token})

    return Response(data={"message": "OTP invalid"}, status=status.HTTP_401_UNAUTHORIZED)


# Admin methods:
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    paginator = PageNumberPagination()

    if 'page_size' in request.data:
        paginator.page_size = int(request.data['page_size'])
    else:
        paginator.page_size = 10

    users = MyUser.objects.all()
    result_page = paginator.paginate_queryset(users, request)
    serializer = MyUserSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

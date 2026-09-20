from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from user.models import User
from user.serializers import UserRequestSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from django.db import transaction

# Create your views here.

class CreateUser(APIView):
    serializer_class = UserRequestSerializer
    # parser_classes = [JSONParser,]

    @transaction.atomic
    def post(self, request):
        data = request.data

        serializer = UserRequestSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        # check if email already exist

        validated_data = serializer.validated_data
        print(validated_data)
        try:
           User.objects.get(email=validated_data.get("email"))
           return Response({"detail": "User with this email already exist"}, status=HTTP_400_BAD_REQUEST)
        except:
            pass
            
        # create the user object

        new_user = User.objects.create(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name")
        )

        # # add their groups
        groups = validated_data.get("groups")

        new_user.groups.add(*groups)

        # set password
        new_user.set_password(validated_data.get("password"))

        new_user.save()

        response_serializer = UserSerializer(new_user,many=False, context={"request": request})
        return Response(response_serializer.data, HTTP_201_CREATED)
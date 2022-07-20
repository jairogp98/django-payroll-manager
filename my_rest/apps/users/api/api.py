from rest_framework.views import APIView, Response
from apps.users.models import User
from apps.users.api.serializers import UserSerializer

class UserAPIView(APIView):

    def get(self, request):

       users = User.objects.all()
       users_serialized = UserSerializer(users, many = True)
       return Response(users_serialized.data, 200)

    def post(self, request):

        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        else:
            return Response(serializer.errors)

    def put(self, request):
        pass

class UserAPIViewById(APIView):

    def get(self,request, pk):

        if pk is None:
            return Response("You must specify user's id", 400)
        else:
            user = User.objects.filter(id = pk).first()
            user_serialized = UserSerializer(user)

            if user is None:
                return Response("User not found", 400)
            else:
                return Response(user_serialized.data, 200)


        

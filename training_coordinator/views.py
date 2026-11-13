from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TrainingCoordinator
from .serializers import TrainingCoordinatorSerializer


class TrainingCoordinatorRegisterView(APIView):

    def post(self, request):
        serializer = TrainingCoordinatorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Training Coordinator registered successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
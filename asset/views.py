from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Asset
from .serializers import AssetSerializer, AgentAssetSerializer


class AssetViewSet(viewsets.ModelViewSet):

    queryset = Asset.objects.all().order_by("-created_at")

    serializer_class = AssetSerializer

    permission_classes = [IsAuthenticated]


class AgentRegisterAsset(APIView):

    def post(self, request):

        hostname = request.data.get("hostname")

        asset = Asset.objects.filter(hostname=hostname).first()

        if asset:

            serializer = AssetSerializer(asset, data=request.data, partial=True)

        else:

            serializer = AssetSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {"message": "Inventario registrado"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import Asset, AssetHistory
from .serializers import AssetSerializer, AgentAssetSerializer


"""class AssetViewSet(viewsets.ModelViewSet):

    queryset = Asset.objects.all().order_by("-created_at")

    serializer_class = AssetSerializer

    permission_classes = [IsAuthenticated]"""
    
class AssetViewSet(viewsets.ModelViewSet):

    queryset = Asset.objects.all().order_by("-created_at")
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):

        history = AssetHistory.objects.filter(asset_id=pk).order_by("-snapshot_date")

        data = [
            {
                "hostname": h.hostname,
                "serial_number": h.serial_number,
                "cpu": h.cpu,
                "ram": h.ram,
                "ip_address": h.ip_address,
                "status": h.status,
                "user_email": h.user_email,
                "department_name": h.department_name,
                "snapshot_date": h.snapshot_date,
                "change_reason": h.change_reason
            }
            for h in history
        ]

        return Response(data)

class AgentAssetDetail(APIView):

    def get(self, request, serial):

        asset = Asset.objects.filter(serial_number=serial).first()

        if not asset:
            return Response(
                {"exists": False},
                status=status.HTTP_200_OK
            )

        serializer = AgentAssetSerializer(asset)

        return Response(
            {
                "exists": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    


class AgentRegisterAsset(APIView):

    def post(self, request):

        serializer = AgentAssetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Inventario registrado"},
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AgentUpdateAsset(APIView):
    def patch(self, request, serial):

        asset = Asset.objects.filter(serial_number=serial).first()

        if not asset:
            return Response(
                {"error": "Asset no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AgentAssetSerializer(asset, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Inventario actualizado"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
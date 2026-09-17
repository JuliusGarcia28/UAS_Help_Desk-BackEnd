from rest_framework import viewsets, status
from rest_framework.views import APIView, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .permissions import HasAgentAPIKey
from .models import Asset, AssetHistory
from .serializers import AssetSerializer, AgentAssetSerializer

from user.permissions import IsAdmin, IsTechnician, IsClient
    
# ViewSet de CRUD Completo para assets
class AssetViewSet(viewsets.ModelViewSet):

    queryset = Asset.objects.all().order_by("-created_at")
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
    
            queryset = Asset.objects.all().order_by("-created_at")
    
            if self.request.user.role == "client":
                queryset = queryset.filter(
                    responsible=self.request.user
                )
    
            return queryset
    
    def check_permissions(self, request):
        
        super().check_permissions(request)
        
        role = request.user.role
                
        if request.method == "GET":
            if role not in ["admin", "technician", "client"]:
                raise PermissionDenied(
                    "No tienes permiso para consultar el inventario."
                )
        
        elif request.method == "POST":
            if role != "admin":
                raise PermissionDenied(
                    "Solo un administrador puede registrar equipos."
                )

        elif request.method in ["PUT", "PATCH"]:
            if role not in ["admin", "technician"]:
                raise PermissionDenied(
                    "No tienes permiso para modificar equipos."
                )
                
    # Prohibe la eliminación de assets a través de la API
    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied(
            "La eliminación de assets no está permitida."
        )

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

# Endpoint para ver detalles de asset para agente
class AgentAssetDetail(APIView):
    
    permission_classes = [HasAgentAPIKey]

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
    
# Enpoint para registrar asset desde agente
class AgentRegisterAsset(APIView):

    permission_classes = [HasAgentAPIKey]

    def post(self, request):

        serializer = AgentAssetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Inventario registrado"},
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Endpoint para actualizar asset desde agente
class AgentUpdateAsset(APIView):
    
    permission_classes = [HasAgentAPIKey]
    
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
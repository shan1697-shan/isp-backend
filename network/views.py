from rest_framework.response import Response

from accounts.views import AdminAPIView

from . import services
from .serializers import NasDeviceSerializer


class NasDeviceListView(AdminAPIView):
    def get(self, request):
        entries = services.list_nas_devices()
        data = []
        for entry in entries:
            device_data = NasDeviceSerializer(entry["device"]).data
            device_data["online_session_count"] = entry["online_session_count"]
            device_data["active_subscribers"] = entry["active_subscribers"]
            data.append(device_data)
        return Response(data)

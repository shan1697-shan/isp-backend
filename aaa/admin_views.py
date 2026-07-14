from rest_framework.response import Response

from accounts.views import AdminAPIView

from .models import AccountingRecord, ActiveSession
from .serializers import AccountingRecordSerializer, ActiveSessionSerializer


class ActiveSessionListView(AdminAPIView):
    def get(self, request):
        sessions = ActiveSession.objects.all().order_by("-started_at")
        return Response(ActiveSessionSerializer(sessions, many=True).data)


class SessionDisconnectView(AdminAPIView):
    def post(self, request, session_id):
        session = ActiveSession.objects.filter(session_id=session_id).first()
        if session is None:
            return Response({"message": "Session not found", "session": None})

        session.status = ActiveSession.Status.DISCONNECTING
        session.save(update_fields=["status", "updated_at"])
        return Response(
            {"message": "Disconnect requested", "session": ActiveSessionSerializer(session).data}
        )


class AccountingRecordListView(AdminAPIView):
    def get(self, request):
        records = AccountingRecord.objects.all().order_by("-event_at")[:500]
        return Response(AccountingRecordSerializer(records, many=True).data)

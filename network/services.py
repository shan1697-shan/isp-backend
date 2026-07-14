from collections import defaultdict

from aaa.models import ActiveSession

from .models import NasDevice


def _sync_nas_devices_from_sessions() -> None:
    for session in ActiveSession.objects.all():
        service_types = ["pppoe"] if session.called_station_id else []
        NasDevice.objects.update_or_create(
            nas_ip_address=session.nas_ip_address,
            defaults={
                "nas_identifier": session.nas_identifier,
                "name": session.nas_identifier or session.nas_ip_address,
                "status": NasDevice.Status.ONLINE,
                "last_seen_at": session.last_interim_at or session.started_at,
                "service_types": service_types,
            },
        )


def list_nas_devices() -> list[dict]:
    _sync_nas_devices_from_sessions()

    active_counts: dict[str, int] = defaultdict(int)
    active_subscribers: dict[str, set] = defaultdict(set)
    for nas_ip_address, username in ActiveSession.objects.values_list(
        "nas_ip_address", "username"
    ):
        active_counts[nas_ip_address] += 1
        active_subscribers[nas_ip_address].add(username)

    devices = NasDevice.objects.all().order_by("-last_seen_at", "-created_at")

    results = []
    for device in devices:
        results.append(
            {
                "device": device,
                "online_session_count": active_counts.get(device.nas_ip_address, 0),
                "active_subscribers": sorted(active_subscribers.get(device.nas_ip_address, set())),
            }
        )
    return results

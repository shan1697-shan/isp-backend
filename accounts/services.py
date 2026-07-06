from django.utils import timezone

from aaa.exceptions import AppError
from common.passwords import verify_password

from .jwt import sign_admin_token
from .models import AdminUser


def login(email: str, password: str) -> dict:
    admin = AdminUser.objects.filter(email=email.lower().strip(), is_active=True).first()
    if admin is None:
        raise AppError("Invalid credentials", 401)

    if not verify_password(password, admin.password_hash):
        raise AppError("Invalid credentials", 401)

    admin.last_login_at = timezone.now()
    admin.save(update_fields=["last_login_at"])

    token = sign_admin_token(
        {"userId": str(admin.id), "email": admin.email, "role": admin.role}
    )

    return {
        "token": token,
        "admin": {
            "id": str(admin.id),
            "name": admin.name,
            "email": admin.email,
            "role": admin.role,
        },
    }

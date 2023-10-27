from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import User


def get_user(openid):
    try:
        u = User.objects.get(openid=openid)
        return u, True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False


def create_user(openid, nickname, age, addr, gender,avatarUrl,phone,intro):
    try:
        now = timezone.now()
        u = User.objects.create(
            openid=openid,
            nickname=nickname,
            age=age,
            addr=addr,
            gender=gender,
            avatarUrl=avatarUrl,
            phone=phone,
            intro=intro,
            updated=now
        )
        u.save()
        return True
    except Exception as e:
        print(e)
        return False




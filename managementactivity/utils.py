from enum import IntEnum
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import localtime

class ActivityStatus(IntEnum):
    REJECTED = 0
    APPROVED = 1
    WAITING_APPROVAL = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_key_text(cls, status):
        match status:
            case (ActivityStatus.REJECTED):
                return 'Di Tolak'
            case (ActivityStatus.APPROVED):
                return 'Di Setujui'
            case _:
                return 'Menunggu Persetujuan'

    @classmethod
    def get_badge_status(cls, status):
        match status:
            case (ActivityStatus.REJECTED):
                return 'badge-danger'
            case (ActivityStatus.APPROVED):
                return 'badge-success'
            case _:
                return 'badge-warning'


class DateTimeHelper:
    @staticmethod
    def get_current_local_time() -> datetime :
        return localtime(timezone.now())

    @staticmethod
    def get_formatted_local_time(datetime_object: datetime=None,format_str: str='%d-%m-%Y %H:%M') -> str:
        if not datetime_object:
            datetime_object = DateTimeHelper.get_current_local_time()
        return datetime_object.strftime(format_str)

    @staticmethod
    def get_epoch_time(datetime_object: datetime=None) -> int:
        if not datetime_object:
            return int(DateTimeHelper.get_current_local_time().timestamp())
        return int(datetime_object.timestamp())

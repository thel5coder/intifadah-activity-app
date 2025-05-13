from enum import IntEnum


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

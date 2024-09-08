from src.core._shared.domain.exceptions import NotFoundException


class CastMemberInvalidError(Exception):
    pass


class CastMemberNotFoundException(NotFoundException):
    pass

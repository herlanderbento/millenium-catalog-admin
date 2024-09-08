from pydantic import ValidationError
from rest_framework.views import exception_handler as rest_framework_exception_handler
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)


def handle_validation_error(exc: ValidationError, context):
    errors = [{error["loc"][-1]: [error["msg"]]} for error in exc.errors()]
    return Response(errors, HTTP_422_UNPROCESSABLE_ENTITY)


def handle_entity_validation_error(exc: EntityValidationException, context):
    errors = []

    for key, error in exc.errors.items():
        if isinstance(error, list):
            errors.append({key: error})
        else:
            errors.append(error)

    return Response(errors, HTTP_422_UNPROCESSABLE_ENTITY)


def handle_not_found_error(exc: NotFoundException, context):
    response = Response({"message": exc.args[0]}, HTTP_404_NOT_FOUND)
    response.status_code = HTTP_404_NOT_FOUND
    return response


handlers = [
    {"exception": ValidationError, "handle": handle_validation_error},
    {"exception": EntityValidationException, "handle": handle_entity_validation_error},
    {"exception": NotFoundException, "handle": handle_not_found_error},
]


def custom_exception_handler(exc, context):

    for handler in handlers:
        if isinstance(exc, handler["exception"]):
            return handler["handle"](exc, context)

    return rest_framework_exception_handler(exc, context)

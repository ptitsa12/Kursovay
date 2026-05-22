from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, ValidationError):
        if isinstance(response.data, dict) and 'alternatives' in response.data:
            return Response(
                {
                    'error': True,
                    'message': str(response.data.get('detail', 'Ошибка валидации')),
                    'alternatives': response.data.get('alternatives', []),
                },
                status=422,
            )
        message = response.data
        if isinstance(message, dict):
            parts = []
            for key, val in message.items():
                if isinstance(val, list):
                    parts.append(f"{key}: {', '.join(str(v) for v in val)}")
                else:
                    parts.append(f"{key}: {val}")
            message = '; '.join(parts)
        elif isinstance(message, list):
            message = '; '.join(str(m) for m in message)

        return Response(
            {'error': True, 'message': str(message)},
            status=response.status_code,
        )

    if response.status_code == 401:
        message = 'Требуется аутентификация'
    elif response.status_code == 403:
        message = 'Недостаточно прав для выполнения операции'
    elif response.status_code == 404:
        message = 'Ресурс не найден'
    else:
        detail = response.data.get('detail') if isinstance(response.data, dict) else response.data
        message = str(detail) if detail else 'Ошибка запроса'

    return Response(
        {'error': True, 'message': message},
        status=response.status_code,
    )

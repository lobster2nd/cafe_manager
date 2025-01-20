from drf_yasg import openapi

response_400 = openapi.Response(
    description="Некорректный запрос",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "error": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Сообщение об ошибке",
                example="Недопустимое значение",
            )
        }
    )
)

response_404 = openapi.Response(
    description="Объект не найден",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Сообщение об ошибке",
                example="Объект не найден",
            )
        }
    )
)

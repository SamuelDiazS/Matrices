import json
from http import HTTPStatus


def sumar_matrices(matriz_a, matriz_b):
    return [
        [matriz_a[i][j] + matriz_b[i][j] for j in range(len(matriz_a[0]))]
        for i in range(len(matriz_a))
    ]


def _leer_json(request):
    if hasattr(request, "json"):
        try:
            return request.json()
        except Exception:
            pass

    body = getattr(request, "body", b"")
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8")

    if isinstance(body, str) and body:
        return json.loads(body)

    return {}


def handler(request, response):
    try:
        datos = _leer_json(request)
        matriz_a = datos.get("matrizA")
        matriz_b = datos.get("matrizB")

        if not isinstance(matriz_a, list) or not isinstance(matriz_b, list):
            raise ValueError("Se requieren dos matrices")

        if len(matriz_a) != 3 or len(matriz_b) != 3:
            raise ValueError("Las matrices deben ser 3x3")

        if any(len(fila) != 3 for fila in matriz_a + matriz_b):
            raise ValueError("Cada matriz debe tener 3 columnas")

        resultado = sumar_matrices(matriz_a, matriz_b)
        response.status = HTTPStatus.OK
        response.headers["Content-Type"] = "application/json"
        return {"resultado": resultado}
    except Exception as error:
        response.status = HTTPStatus.BAD_REQUEST
        response.headers["Content-Type"] = "application/json"
        return {"error": str(error)}

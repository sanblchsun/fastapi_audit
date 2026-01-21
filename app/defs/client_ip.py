from fastapi import Request


def get_client_ips(request: Request) -> tuple[str, str]:
    """
    Возвращает (ip_internal, ip_external)
    ip_internal: локальный IP Windows (передан в заголовке)
    ip_external: внешний IP из X-Forwarded-For или request.client.host
    """
    # внешний IP
    xff = request.headers.get("x-forwarded-for")
    if xff:
        ip_external = xff.split(",")[0].strip()
    elif request.client is not None:
        ip_external = request.client.host
    else:
        ip_external = "unknown"

    # локальный IP передан в кастомном заголовке
    ip_internal = request.headers.get("X-Internal-IP", "unknown")

    return ip_internal, ip_external

BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
CONFLICT = 409
UNPROCESSABLE_ENTITY = 422
INTERNAL_SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504
HTTP_STATUS_CODES = {
  BAD_REQUEST: "Bad Request",
  UNAUTHORIZED: "Unauthorized",
  FORBIDDEN: "Forbidden",
  NOT_FOUND: "Not Found",
  METHOD_NOT_ALLOWED: "Method Not Allowed",
  CONFLICT: "Conflict",
  UNPROCESSABLE_ENTITY: "Unprocessable Entity",
  INTERNAL_SERVER_ERROR: "Internal Server Error",
  SERVICE_UNAVAILABLE: "Service Unavailable",
  GATEWAY_TIMEOUT: "Gateway Timeout"
}
def get_http_status_message(status_code) -> str:
  """
  Get the HTTP status message for a given status code.
  :param status_code: HTTP status code
  :return: HTTP status message
  """
  return HTTP_STATUS_CODES.get(status_code, "Unknown Status Code")
#사용자 정의 에러 유형 코드
class UserDefineErrorCode:
    # Error Code에 대한 상세 msg와 return 값 정의
    CUSTOM_ERR_CODES = {
        1000: {"type": "VALID", "desc": "User Error", "url":""},
        1001: {"type": "VALID", "desc": "No permission", "url": ""},
        1002: {"type": "VALID", "desc": "Data not found!", "url": ""},
        1003: {"type": "VALID", "desc": "No access permission", "url": "back"},
        1004: {"type": "VALID", "desc": "No access to project", "url": "back"},
        1005: {"type": "VALID", "desc": "An error occurred while running analysis", "url": ""},
        1006: {"type": "VALID", "desc": "Please check the cluster parameter value", "url": ""},
        1007: {"type": "VALID", "desc": "user_id is required.", "url": "back"},
        1008: {"type": "VALID", "desc": "Fail to create project, user missing.", "url": ""},
        1009: {"type": "VALID", "desc": "The file is in use and cannot be deleted.", "url": ""},
        1010: {"type": "VALID", "desc": "Already a registered email.", "url": ""},
        1011: {"type": "VALID", "desc": "The number of registered email has been exceeded.", "url": ""},
        1012: {"type": "VALID", "desc": "User information does not exist.", "url": ""},
        1013: {"type": "VALID", "desc": "This email has been suspended or deleted.", "url": "reload"},
        1014: {"type": "VALID", "desc": "Your password fails 5 times, your account will be suspended for 10 minutes.", "url": "/"},
        1015: {"type": "VALID", "desc": "Your email or password is incorrect. If you fail 5 times, your account will be suspended for 10 minutes.", "url": "reload"},
        1016: {"type": "VALID", "desc": "Your password is incorrect.", "url": "reload"},
        1017: {"type": "VALID", "desc": "Please check the cluster parameter value.", "url": ""},
        1018: {"type": "VALID", "desc": "Parameter value Error", "url": ""},
        1019: {"type": "VALID", "desc": "Device name not found", "url": ""},
        1020: {"type": "VALID", "desc": "Model not found", "url": ""},


        3000: {"type": "SYSTEM", "desc": "SYSTEM Error", "url": "back"},

        4001: {"type": "VALID", "desc": "Image not found", "url": ""},
    }

    STATUS_CODES = {
        100: {"type": "HTTP", "desc": "HTTP_100_CONTINUE", "url": ""},
        101: {"type": "HTTP", "desc": "HTTP_101_SWITCHING_PROTOCOLS", "url": ""},
        200: {"type": "HTTP", "desc": "HTTP_200_OK", "url": ""},
        201: {"type": "HTTP", "desc": "HTTP_201_CREATED", "url": ""},
        202: {"type": "HTTP", "desc": "HTTP_202_ACCEPTED", "url": ""},
        203: {"type": "HTTP", "desc": "HTTP_203_NON_AUTHORITATIVE_INFORMATION", "url": ""},
        204: {"type": "HTTP", "desc": "HTTP_204_NO_CONTENT", "url": ""},
        205: {"type": "HTTP", "desc": "HTTP_205_RESET_CONTENT", "url": ""},
        206: {"type": "HTTP", "desc": "HTTP_206_PARTIAL_CONTENT", "url": ""},
        207: {"type": "HTTP", "desc": "HTTP_207_MULTI_STATUS", "url": ""},
        300: {"type": "HTTP", "desc": "HTTP_300_MULTIPLE_CHOICES", "url": ""},
        301: {"type": "HTTP", "desc": "HTTP_301_MOVED_PERMANENTLY", "url": ""},
        302: {"type": "HTTP", "desc": "HTTP_302_FOUND", "url": ""},
        303: {"type": "HTTP", "desc": "HTTP_303_SEE_OTHER", "url": ""},
        304: {"type": "HTTP", "desc": "HTTP_304_NOT_MODIFIED", "url": ""},
        305: {"type": "HTTP", "desc": "HTTP_305_USE_PROXY", "url": ""},
        306: {"type": "HTTP", "desc": "HTTP_306_RESERVED", "url": ""},
        307: {"type": "HTTP", "desc": "HTTP_307_TEMPORARY_REDIRECT", "url": ""},
        400: {"type": "HTTP", "desc": "HTTP_400_BAD_REQUEST", "url": ""},
        401: {"type": "HTTP", "desc": "HTTP_401_UNAUTHORIZED", "url": "back"},
        402: {"type": "HTTP", "desc": "HTTP_402_PAYMENT_REQUIRED", "url": ""},
        403: {"type": "HTTP", "desc": "HTTP_403_FORBIDDEN", "url": "back"},
        404: {"type": "HTTP", "desc": "HTTP_404_NOT_FOUND", "url": ""},
        405: {"type": "HTTP", "desc": "HTTP_405_METHOD_NOT_ALLOWED", "url": ""},
        406: {"type": "HTTP", "desc": "HTTP_406_NOT_ACCEPTABLE", "url": ""},
        407: {"type": "HTTP", "desc": "HTTP_407_PROXY_AUTHENTICATION_REQUIRED", "url": ""},
        408: {"type": "HTTP", "desc": "HTTP_408_REQUEST_TIMEOUT", "url": ""},
        409: {"type": "HTTP", "desc": "HTTP_409_CONFLICT", "url": ""},
        410: {"type": "HTTP", "desc": "HTTP_410_GONE", "url": ""},
        411: {"type": "HTTP", "desc": "HTTP_411_LENGTH_REQUIRED", "url": ""},
        412: {"type": "HTTP", "desc": "HTTP_412_PRECONDITION_FAILED", "url": ""},
        413: {"type": "HTTP", "desc": "HTTP_413_REQUEST_ENTITY_TOO_LARGE", "url": ""},
        414: {"type": "HTTP", "desc": "HTTP_414_REQUEST_URI_TOO_LONG", "url": ""},
        415: {"type": "HTTP", "desc": "HTTP_415_UNSUPPORTED_MEDIA_TYPE", "url": ""},
        416: {"type": "HTTP", "desc": "HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE", "url": ""},
        417: {"type": "HTTP", "desc": "HTTP_417_EXPECTATION_FAILED", "url": ""},
        422: {"type": "HTTP", "desc": "HTTP_422_UNPROCESSABLE_ENTITY", "url": ""},
        423: {"type": "HTTP", "desc": "HTTP_423_LOCKED", "url": ""},
        424: {"type": "HTTP", "desc": "HTTP_424_FAILED_DEPENDENCY", "url": ""},
        425: {"type": "HTTP", "desc": "HTTP_425_TOO_EARLY", "url": ""},
        428: {"type": "HTTP", "desc": "HTTP_428_PRECONDITION_REQUIRED", "url": ""},
        429: {"type": "HTTP", "desc": "HTTP_429_TOO_MANY_REQUESTS", "url": ""},
        431: {"type": "HTTP", "desc": "HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE", "url": ""},
        451: {"type": "HTTP", "desc": "HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS", "url": ""},
        500: {"type": "HTTP", "desc": "HTTP_500_INTERNAL_SERVER_ERROR", "url": ""},
        501: {"type": "HTTP", "desc": "HTTP_501_NOT_IMPLEMENTED", "url": ""},
        502: {"type": "HTTP", "desc": "HTTP_502_BAD_GATEWAY", "url": ""},
        503: {"type": "HTTP", "desc": "HTTP_503_SERVICE_UNAVAILABLE", "url": ""},
        504: {"type": "HTTP", "desc": "HTTP_504_GATEWAY_TIMEOUT", "url": ""},
        505: {"type": "HTTP", "desc": "HTTP_505_HTTP_VERSION_NOT_SUPPORTED", "url": ""},
        507: {"type": "HTTP", "desc": "HTTP_507_INSUFFICIENT_STORAGE", "url": ""},
        511: {"type": "HTTP", "desc": "HTTP_511_NETWORK_AUTHENTICATION_REQUIRED", "url": ""},

    }

    # Error Code에 대한 상세 msg와 url 값 정의
    def get_custom_error_msg(self, code):
        # 커스텀 코드의 에러 정보 추출
        error_info = self.CUSTOM_ERR_CODES.get(int(code))
        return self.get_error_msg(error_info)

    def get_http_error_msg(self, code):
        # http 에러에 해당하는 코드의 에러 정보 추출
        error_info = self.STATUS_CODES.get(int(code))
        return self.get_error_msg(error_info)

    def get_error_msg(self, error_info):
        """
        에러 정보에서 type, desc, url 값을 뽑아 리턴
        :param error_info:
        :return:
        """
        if error_info:
            type = error_info.get("type", "")
            description = error_info.get("desc", "")
            url = error_info.get("url", "")
            return type, description, url
        else:
            return None, None, None

from typing import Union

from src.common.define_error_codes import UserDefineErrorCode
from src.common.setup_log import SetupLogger


"""
try/except 문에서 except 부분에서 exception 추가

raise CustomException(type="VALID", code="1002", msg="Data not found!",
                      func="custom_exception.CustomException.exception_log_by_json")
또는
raise SystemException(type="SYSTEM", code="3000", msg="SYSTEM Error",
                      func="custom_exception.SystemException.exception_log")
형태로 사용
"""


# 에러 로그 및 메세지 관리를 위함 사용자 정의 class
# 값 검증에 대한 에러 유형 class
class CustomException(Exception):
    """
    :param type: "HTTP", "VALID", "SYSTEM"
    :param code: define_error_codes.py
    :param msg: message
    :param func: file_name.class_name.function
    """
    def __init__(self, type: str, code: Union[str, int], msg: str, func: str):
        super().__init__(code)
        # self.original_exception = e
        self.type = type
        self.code = str(code)
        self.msg = msg
        self.func = func

        self.sl = SetupLogger()
        self.exc_logger = self.sl.setup_logger(log_type="exception")

        ec = UserDefineErrorCode()
        if self.type == "HTTP":
            # http status code에 대한 오류 메세지
            type, msg, url = ec.get_http_error_msg(self.code)
        else:
            type, msg, url = ec.get_custom_error_msg(self.code)

        # 존재하지 않는 코드로 인해 None이 리턴된 경우 직접 작성한 메세지를 그대로 로그에 기록
        if msg is None:
            msg = self.msg

        self.exc_logger.error(f"{self.func} : {self.type} : {self.code} : {msg}")
        self.sl.close_logger()


# 값 검증에 대한 에러 유형을 제외한 클래스
class SystemException(CustomException):
    """
    :param type: "HTTP", "VALID", "SYSTEM"
    :param code: define_error_codes.py
    :param msg: message
    :param func: file_name.class_name.function
    """
    def __init__(self, type: str, code: Union[str, int], msg: str, func: str):
        super().__init__(type, code, msg, func)
        self.type = type
        self.code = str(code)
        self.msg = msg
        self.func = func

        self.exc_logger.error(f"{self.func} : {self.type} : {self.code} : {self.msg}")
        self.sl.close_logger()

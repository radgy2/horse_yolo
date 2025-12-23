import os
import logging
import inspect
from datetime import datetime

from src.common.file_path import FilePathClass


class SetupLogger:
    """
    로그 생성 객체 선언
    logger = setup_logger(log_type="run") 형태로 사용
    log_type 은 "exception" or "run"
    """
    def __init__(self):
        self.fp = FilePathClass()  # 경로 생성 도우미 클래스
        self.logger = None  # 실제 logger 객체

    def setup_logger(self, log_type="run"):
        # 어디서 setup_logger()를 불렀는지 자동으로 알아내서 그 파일 이름을 로거의 이름으로 쓰기 위한 작업
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        caller_name = os.path.splitext(os.path.basename(caller_module.__file__))[0]
        # ex. main.py에서 호출하면 'main'이라는 이름의 logger가 생성됨

        # 이름이 caller_name 인 로거 객체 생성
        self.logger = logging.getLogger(caller_name)

        # 이미 같은 이름의 logger가 만들어졌다면 핸들러를 지워서 중복 로그 방지
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 로그 레벨 설정
        # log level은 degbug로 고정 (전체 필터라고 생각)
        self.logger.setLevel(logging.DEBUG)

        # 핸들러 생성
        console_handler = logging.StreamHandler()  # 콘솔(터미널)에 출력할 로그

        # 로그 저장 파일 경로
        log_path = self.fp.get_user_id_log_path()

        # log_type 에 따라 파일명 지정
        if log_type == "exception":
            log_filename = f"{datetime.now().strftime('%Y%m%d')}_exception.log"
        elif log_type == "run":
            log_filename = f"{datetime.now().strftime('%Y%m%d')}_run.log"
        else:
            log_filename = f"{datetime.now().strftime('%Y%m%d')}_unknown_type.log"

        file_handler = logging.FileHandler(os.path.join(log_path, log_filename), encoding='utf-8')

        # 개별 핸들러의 로그 레벨 설정
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        # 핸들러에 로그 포맷 설정
        console_format = logging.Formatter('[%(levelname)s] - [%(name)s, %(lineno)d] - %(message)s')
        file_format = logging.Formatter('%(asctime)s - [%(levelname)s] - [%(name)s, %(lineno)d] - %(message)s')
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # 핸들러 등록
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        return self.logger

    def close_logger(self):
        """
        핸들러를 명시적으로 종료해줌
        :return:
        """
        if self.logger:
            # Close and remove all handlers
            handlers = self.logger.handlers[:]
            for handler in handlers:
                handler.close()
                self.logger.removeHandler(handler)

import os
import subprocess
from pathlib import Path
from datetime import datetime


class PathConst:
    def __init__(self):
        # 경로 관련
        self.DATA_PATH = "data"
        self.RESULT_PATH = "result"
        self.LOG_PATH = "logs"
        self.TEMP_PATH = "temp"
        self.NOTEBOOKS_PATH = "notebooks"
        # 나스 경로(사내 인터넷 망에서만 가능)
        self.NAS_PATH = '\\\limenas7f'


class FilePathClass(PathConst):
    def __init__(self):
        super().__init__()
        # root 경로
        self.root_path = self.get_project_root_path()
        # 사용자 정의 폴더
        self.data_path = self.DATA_PATH
        self.result_path = self.RESULT_PATH
        self.log_path = self.LOG_PATH
        self.temp_path = self.TEMP_PATH
        self.notebooks_path = self.NOTEBOOKS_PATH
        # 바탕화면 경로
        self.desktop_path = self.get_desktop_path()
        # 나스 경로(사내 인터넷 망에서만 가능)
        self.nas_path = self.NAS_PATH
        try:
            if not os.path.exists(self.root_path):
                raise ValueError
        except ValueError:
            print("폴더 확인")

    # 프로젝트 최상위 경로 추출 메서드
    def get_project_root_path(self):
        """
        작업 디렉토리를 기준으로 현재의 경로를 잡고 최상위 경로까지 반복하여 listdir로 .git 폴더를 찾아 프로젝트 경로 추출
        :return: 프로젝트 최상위 경로
        """
        # 작업 디렉토리를 시작 디렉토리로 현재의 폴더를 찾음
        start_path = os.getcwd()
        current_dir = os.path.abspath(start_path)
        try:
            # 최상위 경로가 될 때 까지 반복
            while current_dir != os.path.dirname(current_dir):
                if '.git' in os.listdir(current_dir):
                    return current_dir  # .git 폴더가 있는 디렉토리의 경로를 반환
                current_dir = os.path.dirname(current_dir)
        except FileNotFoundError as e:
            print(f".git 폴더를 찾을 수 없어 프로젝트 최상위 경로를 가져올 수 없습니다.: {e}")

    def get_desktop_path(self):
        """
        os 환경에 따라 유저프로필을 찾고 바탕화면 경로 추출
        :return: 바탕화면 경로
        """
        if os.name == 'nt':  # Windows // 유저 프로필을 찾아 바탕화면 경로 추출
            return str(Path(os.environ['USERPROFILE']) / 'Desktop')
        elif os.name == 'posix':  # macOS or Linux
            return str(Path.home() / 'Desktop')
        else:
            return OSError(f"Failed to retrieve OS information.")

    def is_path_exist_check(self, path):
        """
        파일 또는 폴더 존재 여부 확인 함수
        :param path: 파일 혹은 폴더 경로
        :return:
        """
        if not os.path.exists(path):
            return False
        else:
            return True

    def make_path(self, path):
        """
        폴더 생성 함수
        :param path: 생성할 폴더 경로
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_log_path(self):
        """
        로그파일 경로 반환
        (log 폴더 경로 LIME_PROJECT/logs/)
        :return:
        """
        folder = self.root_path + os.sep + self.log_path + os.sep
        return self.make_path(folder)

    def get_user_id_log_path(self):
        """
        사용자별 로그 파일 경로 반환
        (LIME_PROJECT/logs/{user_id}/{YYYYmm}/)
        :return:
        """
        folder = self.root_path + os.sep + self.log_path + os.sep + self.get_git_user_id() + os.sep + datetime.now().strftime('%Y%m') + os.sep
        return self.make_path(folder)

    def get_data_path(self):
        """
        data 폴더 경로 반환
        (LIME_PROJECT/data/)
        :return:
        """
        folder = self.root_path + os.sep + self.data_path + os.sep
        return self.make_path(folder)

    def get_result_path(self):
        """
        결과 파일 경로 반환(LIME_PROJECT/data/result/)
        :return:
        """
        folder = self.root_path + os.sep + self.data_path + os.sep + self.result_path + os.sep
        return self.make_path(folder)

    def get_temp_path(self):
        """
        임시(temp) 폴더 경로 반환(LIME_PROJECT/data/temp/)
        :return:
        """
        folder = self.root_path + os.sep + self.data_path + os.sep + self.temp_path + os.sep
        return self.make_path(folder)

    def get_nas_path(self):
        """
        NAS 경로 반환(window 폴더 경로, 라임솔루션 7층에서만 사용 가능)
        :return:
        """
        return self.nas_path

    def get_git_user_id(self):
        """
        git user_id 추출 함수
        :return:
        """
        try:
            result = subprocess.run(['git', 'config', '--get', 'user.name'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            user_name = result.stdout.strip()
            if user_name:
                return user_name
            else:
                return ValueError("Username not found.")

        except subprocess.CalledProcessError as e:
            print(e)
            raise EnvironmentError("The command cannot be executed.")

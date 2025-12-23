import os
import random
import shutil
from datetime import datetime

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from src.common.setup_log import SetupLogger
from src.common.custom_exceptions import CustomException


class CommonUtilCodes:
    def __init__(self):
        self.sl = SetupLogger()
        self.logger = self.sl.setup_logger(log_type="run")

    def find_error_image(self, dir_path):
        """
        꺠진 이미지 찾기
        :param dir_path: 폴더 경로
        :return: 깨진 파일 리스트
        """
        file_list = os.listdir(dir_path)
        error_file_list = []
        for file in tqdm(file_list):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                temp_img = cv2.imread(os.path.join(dir_path, file))
                if temp_img is not None:
                    pass
                else:
                    self.logger.info(f"{file} 이 깨짐")
                    error_file_list.append(file)

        return error_file_list

    def get_sample_list(self, item_list, ratio):
        """
        리스트에서 일부 랜덤 샘플링
        :param item_list: 아이템 리스트
        :param ratio: 추출할 비율(ex. 0.1)
        :return: 랜덤 샘플링한 리스트
        """
        sample_size = max(1, len(item_list) * ratio)
        self.logger.info(f"Sample Size = {sample_size}")

        return random.sample(item_list, sample_size)

    def get_split_list(self, item_list, ratio=(8, 1, 1)):
        """
        입력된 리스트에 대하여 정해진 비율로 나눠주는 함수
        :param item_list:
        :param ratio:
        :return:
        """
        # 리스트를 섞음
        random.shuffle(item_list)
        # 전체 리스트의 길이
        total_length = len(item_list)

        # 비율에 따른 각 부분의 길이 계산
        total_ratio = sum(ratio)
        lengths = [int(total_length * (r / total_ratio)) for r in ratio]

        # 마지막 부분의 길이는 남은 요소를 모두 포함하도록 조정
        lengths[-1] = total_length - sum(lengths[:-1])

        # 각 부분의 시작점 계산
        start_points = [sum(lengths[:i]) for i in range(len(lengths))]

        # 비율에 따라 리스트 분할
        divided_lists = [item_list[start:start + length] for start, length in zip(start_points, lengths)]

        return divided_lists


    def get_list_from_excel_copy(self, long_str):
        """
        엑셀에서 복사한 문자열을 리스트로 변경
        ex. '''
        aaaa
        bbbb
        cccc
        '''
        :param long_str: ''' 으로 연결된 문자열 입력
        :return: 문자열 리스트
        """
        return_list = [x.strip().replace("'", "") for x in long_str.strip().split('\n') if x.strip() != '']
        return return_list


    def crop_image_by_cv2(self, img_path, start_x, start_y, end_x, end_y):
        """
        이미지를 크롭하여 반환
        :param img_path: 이미지 경로
        :param start_x: 시작 x 좌표
        :param start_y: 시작 y 좌표
        :param end_x: 끝 x 좌표
        :param end_y: 끝 y 좌표
        :return: 크롭 이미지
        """
        try:
            temp_img = cv2.imread(img_path)
            self.logger.info(f"이미지 파일 로드 ==> {img_path}")
            crop_temp_img = temp_img[start_y:end_y, start_x:end_x]
            return crop_temp_img
        # TODO : 추후 image 로드별 오류 내용 정의
        except:
            raise CustomException(type="VALID", code="4001", msg="Image Not Found",
                                  func="utils.CommonUtilCodes.select_all_table")

    def open_image(self, img_path):
        """
        이미지파일을 cv2로 열어서 바로 출력하는 함수
        :param img_path: 이미지 파일 경로
        :return: 이미지 파일
        """
        self.logger.info("open_image 시작")

        # 이미지 열기
        image = cv2.imread(img_path)

        if image is not None:
            cv2.imshow("Original Image", image)
            # 이미지 출력
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.logger.info("image open")
            return image
        else:
            raise CustomException(type="VALID", code="4001", msg="Image Not Found",
                                  func="utils.CommonUtilCodes.select_all_table")

    def barh_chart(self, data, x_labels, save_path):
        """
        가로 막대 그래프 그리기

        :param data : 데이터 리스트 ex) [1,2,3,4,5]
        :param x_labels : x축 범주 리스트, ex) ['1994 ~ 2000', '2001 ~ 2005', '2006 ~ 2010']
        :param save_path : 그래프 이미지 저장 경로
        :return: 그래프 이미지 파일 저장
        """
        # plt 한글 깨짐 문제 해결
        plt.rcParams['axes.unicode_minus'] = False
        plt.rc('font', family='Malgun Gothic')

        plt.figure(figsize=(15, 6), facecolor='white')
        plt.barh(x_labels, data)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)

        # 데이터 레이블 (수치) 표시
        for i, v in enumerate(data):
            plt.text(v + 5, i, str(v), color='black', va='center', fontsize=18)

        plt.tight_layout()
        plt.savefig(os.path.join(save_path, 'all_year_of_birth'), dpi=300, bbox_inches='tight')

    def pie_chart(self, df, labels, save_path):
        """
        파이 차트 그리기

        :param df : 데이터프레임
        :param labels : 범주 리스트, ex) ['수컷', '암컷']
        :param save_path : 그래프 이미지 저장 경로
        :return:그래프 이미지 파일 저장
        """

        frequency = df['count']  # 그래프에 그리고 싶은 값이 들어있는 컬럼 선택, ex)'count'

        fig = plt.figure(figsize=(8, 8))
        fig.set_facecolor('white')  # 그래프 배경색 설정
        ax = fig.add_subplot()

        # 파이 차트 그리기
        pie = ax.pie(df['count'], autopct='%.1f%%', textprops={'fontsize': 25, 'weight': 'bold'}, pctdistance=0.5,
                     startangle=260, counterclock=False)

        # 전체 값의 합 계산
        total = np.sum(frequency)

        # 화살표와 텍스트 설정
        bbox_props = dict(boxstyle='square', fc='w', ec='w', alpha=0)
        config = dict(arrowprops=dict(arrowstyle='-'), bbox=bbox_props, va='center')  # 설정값 딕셔너리

        # 범주마다 텍스트(라벨)와 빈도수 표시
        for i, l in enumerate(labels):
            ang1, ang2 = ax.patches[i].theta1, ax.patches[i].theta2  # 시작 각도와 종료 각도 계산
            center, r = ax.patches[i].center, ax.patches[i].r  # 중심점과 반지름 계산
            text = f'{l} ({frequency[i]})'  # 텍스트 생성
            empty_text = ""  # 화살표를 그리기 위한 빈 텍스트 생성
            ang = (ang1 + ang2) / 2  # 중간 각도 계산
            x = np.cos(np.deg2rad(ang))  # x 좌표 계산
            y = np.sin(np.deg2rad(ang))  # y 좌표 계산
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]  # 수평 정렬 설정
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)  # 연결 스타일 설정
            config["arrowprops"].update({"connectionstyle": connectionstyle})  # 화살표 스타일 업데이트
            arrow_x = 1.2 * x  # 화살표 x 좌표
            arrow_y = 1.2 * y  # 화살표 y 좌표
            text_props = {'fontsize': 25, 'weight': 'bold'}  # 텍스트 스타일 설정
            ax.text(x=arrow_x, y=arrow_y, s=text, horizontalalignment=horizontalalignment, **text_props)  # 텍스트 추가
            ax.annotate(empty_text, xy=(x, y), xytext=(arrow_x, arrow_y), horizontalalignment=horizontalalignment, **config)  # 빈 텍스트 + 화살표 추가

        plt.savefig(os.path.join(save_path, 'all_sex_2'), dpi=300, bbox_inches='tight')

    def file_size_check(self, check_dir, save_to_excel=False):
        """
        경로 내 모든 파일들 중 크기가 100kb 이하인 파일 목록 출력
        :param check_dir: 확인하는 폴더 경로
        :param save_to_excel: 결과를 엑셀로 저장할 것인지 True, False
        :return: df, columns=['file_name', 'file_path', 'file_size']
        """
        data_list = []
        for current_folder, _, files in os.walk(check_dir):
            try:
                for file_name in tqdm(files, desc=f"{current_folder}"):
                    file_path = os.path.join(current_folder, file_name)
                    file_size = os.path.getsize(file_path)

                    # 약 100kb 이하인 파일의 이름 출력
                    if file_size <= 100000:
                        data = file_name, file_path, file_size
                        data_list.append(data)
                    else:
                        continue
            except FileNotFoundError:
                continue

        columns = ['file_name', 'file_path', 'file_size']
        df = pd.DataFrame(data_list, columns=columns)  # 데이터프레임 구성
        pd.set_option('display.max_rows', None)  # row 생략없이 출력하기 위한 옵션
        pd.set_option('display.max_columns', None)  # column 생략없이 출력하기 위한 옵션

        # 로그에 결과 추가
        self.logger.info(f"File size check completed for folder: {check_dir}")
        self.logger.warning(f"Number of files with size <= 100KB: {len(data_list)}")

        if save_to_excel:
            date = datetime.now()
            today_date = date.strftime("%Y%m%d")
            df.to_excel(f"{check_dir}/file_size_check_{today_date}.xlsx", index=False)  # 엑셀 파일로 저장

            # 엑셀로 저장 시 추가되는 로그
            self.logger.info(f"save_to_excel: {check_dir}/file_size_check_{today_date}.xlsx")

        return df

    def files_copy(self, origin_path: str, copied_path: str, files_list: list):
        """
        폴더 내 하위폴더까지 검색하여 리스트의 파일명을 찾아 복사해오는 함수
        :param origin_path: 원본 폴더 경로
        :param copied_path: 복사 파일 저장 경로
        :param files_list: 복사할 파일명 리스트
        """
        for root, dirs, files in os.walk(origin_path):
            for file in files:
                for filename in files_list:
                    if file == filename:
                        shutil.copy(os.path.join(root, file), copied_path)
                        self.logger.info(f"Copied {filename}")
                    else:
                        continue
        return self.logger.info(f"files Copy complete.")

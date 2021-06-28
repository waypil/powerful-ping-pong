""" Tools for debugging """

import time  # Framewatch/Time엔 사용하지 않음
from types import FunctionType, MethodType


def processing_time_gauge(func):  # method/function의 처리 속도 측정 데코레이터
    def __get_result(end_time, per_frame):
        spf = 1 / per_frame  # seconds_per_frame
        safety, notice, caution, warning = spf / 10, spf / 5, spf / 2, spf

        if safety > end_time:
            return SAFETY  # 양호(SAFETY) (return False로 바꾸면 표시 비활성화)
        elif notice > end_time:
            return NOTICE  # 유의(NOTICE)
        elif caution > end_time:
            return CAUTION  # 주의(CAUTION): frame drop에 영향을 줄 수 있음.
        elif warning > end_time:
            return WARNING  # 경고(WARNING): frame drop의 가능성. 최적화 요망
        else:
            return DANGER  # 위험(DANGER): frame drop 발생 중. 최적화 필수

    def wrapper(*args, **kwargs):
        if type(func) is MethodType:  # class method or instance method
            self, args = args[0], args[1:]

            if self.__class__.__name__ == 'type':  # class method
                name = self.__name__ + '.'
            else:  # instance method
                name = self.__class__.__name__ + '.'

            start_time = time.time()  # 처리 속도 측정 시작
            returned = func(self, *args, **kwargs)  # 처리 속도 측정 중
            end_time = time.time() - start_time  # 측정 종료

        elif type(func) is FunctionType:  # static method or function
            name = ''
            start_time = time.time()  # 처리 속도 측정 시작
            returned = func(*args, **kwargs)  # 함수 실행 & 처리 속도 측정 중
            end_time = time.time() - start_time  # 측정 종료

        else:  # 잘못된 사용
            raise AttributeError

        result = __get_result(end_time, FPS)
        if end_time != 0.0 and result:
            print(f"{name}{func.__name__}() : {end_time}  [{result}]")

        if returned is not None:
            return returned

    return wrapper

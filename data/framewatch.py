""" Tools consist of methods of class """

from data.clstools import *


class Framewatch:  # 상속 외 다른 용도로 사용하지 않음
    """Default is 100 fps.
    """
    s = []

    class DeciFrame:
        def __init__(self):
            self.speed = 1.0  # 배속 / 상승자(上昇子)
            self.under = 0.0  # 1 미만의 소수점을 저장하는 곳

        def __call__(self):
            self.under += self.speed
            if self.under >= 1:
                self.under -= 1
                return 1
            else:
                return 0

    @classmethod
    def tick_all(cls, force=False):  # 모든 Framewatch 객체의 시간 +0.01초
        for watch in cls.s:
            watch.tick(force)

    def __init__(self, preset_frame=0, immediate_start=False):
        if self not in self.__class__.s:  # 중복 담기 방지
            self.__class__.s.append(self)

        self._elapse = self.DeciFrame()
        self.now = self.preset = preset_frame
        self.running = False

        if immediate_start:
            self.start()

    def tick(self, force=False):
        if self.running or force:
            self.now += self._elapse()

    def _get(self, ndigits):  # frame을 초 단위로 변환, 소수점 지정
        if ndigits == 0:
            return self.now // 100  # 0초
        elif ndigits == 1:
            return self.now // 10 / 10  # 0.0초
        elif ndigits == 2:
            return self.now / 100  # 0.00초
        elif ndigits is None or not ndigits:  # 굳이 사용할 일 없음
            return self.now  # 000프레임
        else:
            raise ValueError("ndigits= must be integer 0/1/2")

    def call(self, item, ndigits):
        if ndigits is None:
            return item
        else:
            return item, self._get(ndigits)

    def speed(self, times):
        self._elapse.speed *= times

    def start(self):  # 스톱워치 시작 (+resume)
        if not self.running:
            self.running = True

    def pause(self):  # 스톱워치 일시정지 (게임 일시정지 시 사용)
        if self.running:
            self.running = False

    def reset(self, start_frame=None, immediate_start=False):
        self.now = self.preset if start_frame is None else start_frame
        if immediate_start:
            self.start()

    def off(self):
        self.running = False
        self.now = self.preset


class AntiMashing(Framewatch):
    def __init__(self, is_pushable: bool, limit_sec):
        super().__init__()
        self.limit = int(limit_sec * 100)
        self.is_pushable = is_pushable

    def __call__(self, ndigits=None):
        if self.now == 0:
            self.start()
            return self.call(self.is_pushable, ndigits)  # 연타 허용
        elif self.now >= self.limit:
            self.reset()
            return self.call(self.is_pushable, ndigits)  # 연타 허용
        else:
            return self.call(not self.is_pushable, ndigits)  # 연타 불허


class Stopwatch(Framewatch):
    def __init__(self, preset_sec=0, immediate_start=False):
        super().__init__(int(preset_sec * 100), immediate_start)
        self.checkpoints = []

    def __call__(self, ndigits=None):
        return self._get(ndigits)

    def check(self):
        self.checkpoints.append(self.now)

    def off(self):
        super().off()
        self.checkpoints = []


class Timer(Framewatch):
    def __init__(self, time_is_over: bool, limit_sec, immediate_start=False):
        super().__init__(immediate_start=immediate_start)

        if type(limit_sec) in [list, tuple]:
            now_sec, preset_sec = limit_sec
            self.now, self.preset = int(now_sec * 100), int(preset_sec * 100)
        else:  # int or float
            self.now = self.preset = int(limit_sec * 100)

        self.time_is_over = time_is_over

    def __call__(self, ndigits=None):
        if self.now == 0:  # 제한 시간 도달
            self.pause()
            return self.call(self.time_is_over, ndigits)
        else:
            return self.call(not self.time_is_over, ndigits)

    def tick(self, force=False):
        if (self.running and self.now > 0) or force:
            self.now -= self._elapse()


class RotationClock(Framewatch):
    def __init__(self, *args):  # [True, 1.5], [False, 6], ......
        super().__init__()
        self.rotation = args
        self.number = 0
        self.item = self.rotation[self.number][0]
        self.limit = int(self.rotation[self.number][1] * 100)
        self.checkpoint = 0  # -Cumulative 클래스에서만 사용.

    def __call__(self, ndigits=None):
        if self.now >= self.limit:  # 교대 타임 도달 시
            self.reset(), self._rotate()
        return self.call(self.item, ndigits)

    def _rotate(self):
        self.number = (self.number + 1) % len(self.rotation)
        self.item = self.rotation[self.number][0]
        self.limit = int(self.rotation[self.number][1] * 100) + self.checkpoint


class CycleClock(RotationClock):
    """fps.tick()이 이 클래스보다 앞에 올 경우,
    두 번째 인자부터 시작해버리는 버그가 발생하므로 주의!!!
    """
    def __call__(self, ndigits=None):
        if self.now == 0:
            return self.call(self.item, ndigits)
        elif self.now < self.limit:
            return self.call(False, ndigits)
        else:
            self.reset(), self._rotate()
            return self.call(self.item, ndigits)


class CumulativeClock(RotationClock):  # 상속 외 다른 용도로 사용하지 않음
    def reset(self, start_frame=None, immediate_start=False):
        super().reset(start_frame, immediate_start)
        self.checkpoint = 0

    def off(self):
        super().off()
        self.checkpoint = 0


class RotationClockCumulative(CumulativeClock):
    def __call__(self, ndigits=None):
        if self.now >= self.limit:  # 교대 타임 도달 시
            self.checkpoint = self.now  # 차이점
            self._rotate()
        return self.call(self.item, ndigits)


class CycleClockCumulative(CumulativeClock):
    """fps.tick()이 이 클래스보다 앞에 올 경우,
    두 번째 인자부터 시작해버리는 버그가 발생하므로 주의!!!
    """
    def __call__(self, ndigits=None):
        if self.now == 0:
            return self.call(self.item, ndigits)
        elif self.now < self.limit:
            return self.call(False, ndigits)
        else:
            self.checkpoint = self.now  # 차이점
            self._rotate()
            return self.call(self.item, ndigits)

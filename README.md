# Project PPP v1.0.2
The Indie Game Project.

# Wait!
|      |타입|동일표현 / 활용표현|
|------|---|---|
|foo.py|Python 파일||
|./foo/|폴더|/foo/bar/ : foo 폴더 속 bar 폴더 (점 생략 가능) |
|Foo|클래스|Foo(Bar) : Bar 클래스를 상속받은 Foo 클래스|
|foo|변수|foo=bar : bar가 할당되어 있는 foo 변수<br>foo:list : 리스트 타입의 foo 변수 (foo:[]와 동일)|
|FOO|상수||
|cls.foo|클래스 변수| Bar.foo : Bar 클래스의 foo 클래스 변수|
|self.foo|인스턴스 변수|Bar().foo : Bar 클래스의 foo 인스턴스 변수<br>bar.foo : bar 인스턴스(객체)의 foo 인스턴스 변수|
|'foo'|문자열| "foo", foo:str 과 같음.<br><br>'{foo}' : foo 변수값이 담긴 문자열<br>'{foo()}' : foo 함수의 리턴값이 담긴 문자열 |
|foo()|함수||
|foo(cls)|클래스 메소드| Bar.foo() : Bar 클래스의 foo() 클래스 메소드|
|foo(self)|인스턴스 메소드| Bar().foo() : Bar 클래스의 foo() 인스턴스 메소드|
|.foo()|정적(static) 메소드|Bar..foo() : Bar 클래스의 foo 정적 메소드<br>bar..foo() : bar 인스턴스(객체)의 foo 정적 메소드|
|...|앞의 것이 계속 이어짐|예시: {key: item, ...}|
|*foo|괄호가 풀어져 있는 상태|foo = [2, 3, 4]<br><br>bar = (1, foo) → (1, [2, 3, 4])<br>bar = (1, *foo) → (1, 2, 3, 4)|


# main.py



# keyinput.py
키보드 입력, 마우스 입력/움직임을 감지하는 공간.

## Keyinput:

### update(cls):
```
Mouse.pos = pg.mouse.get_pos()
```
* Mouse : 마우스의 클릭 여부, 좌표를 저장하는 클래스. (./data/_bios.py)
* pg.mouse.get_pos() → (x, y) : 마우스의 현재 좌표를 호출하는 pygame 고유 함수.

```
cls.input_keep(pg.key.get_pressed())
```
* pg.key.get_pressed() → {key: bool, ......} : 
  키보드의 모든 키들이 하나하나씩 담겨 있는 딕셔너리를 호출.
  **현재 눌러져 있으면** True, 그렇지 않을 경우 False와 짝 지어진다.

```
for event in [None, *pg.event.get()]:
    cls.input_once(event)
```
* pg.event.get() → list : 현재 게임에서 일어난 **모든 상태 변화**를 list에 담아 호출하는 pygame 
  고유 함수.
* None : *버그 방지를 위한 조치. cls.input_once( ) 항목 참조.*

## input_keep(cls, key):
Key.keep 


## input_once(cls, key):



# object.py

# package.py

# data/_bios.py

# data/_constants.py

# data/_debugtools.py

# data/_clstools.py

# data/_functools.py

# 각주


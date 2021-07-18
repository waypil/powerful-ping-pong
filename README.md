# Powerful Ping-Pong v1.4.5
The Indie Game Project.

# Wait!
|      |타입|동일표현 / 활용표현|
|------|---|---|
|foo.py|Python 파일|foo.py ⊃ Bar : foo.py 안에 있는 Bar 클래스|
|./foo/|폴더|/foo/bar/ : foo 폴더 속 bar 폴더 (점 생략 가능) |
|Foo|클래스|Foo(Bar) : Bar 클래스를 상속받은 Foo 클래스|
|foo|변수|foo=bar : bar가 할당되어 있는 foo 변수<br>foo<sup>[list](#)</sup> : 리스트 타입의 foo 변수|
|FOO|상수||
|cls.foo|클래스 변수| Bar.foo<sup>[cls](#)</sup> : Bar 클래스의 foo 클래스 변수|
|self.foo|인스턴스 변수|Bar.foo<sup>[self](#)</sup> : Bar 클래스의 foo 인스턴스 변수<br>bar.foo<sup>[self](#)</sup> : bar 인스턴스(객체)의 foo 인스턴스 변수|
|'foo'|문자열| "foo", foo<sup>[str](#)</sup> 과 같음.<br><br>'{foo}' : foo 변수값이 담긴 문자열<br>'{foo()}' : foo 함수의 리턴값이 담긴 문자열 |
|foo()|함수|foo() → list : foo 함수의 리턴값 타입이 list|
|foo(cls)|클래스 메소드| Bar.foo()<sup>[cls](#)</sup> : Bar 클래스의 foo() 클래스 메소드|
|foo(self)|인스턴스 메소드| Bar.foo()<sup>[self](#)</sup> : Bar 클래스의 foo() 인스턴스 메소드|
|.foo()|정적(static) 메소드|Bar.foo()<sup>[static](#)</sup> : Bar 클래스의 foo 정적 메소드<br>bar.foo()<sup>[static](#)</sup> : bar 인스턴스(객체)의 foo 정적 메소드|
|...|앞의 것이 계속 이어짐|...... 와 같음.<br>예시: {key: item, ...}|
|*foo|괄호가 풀어져 있는 상태|foo = [2, 3, 4]<br><br>bar = (1, foo) → (1, [2, 3, 4])<br>bar = (1, *foo) → (1, 2, 3, 4)|


# main.py

## Game
  Title, Stage, End의 상위 클래스.

### .assign_image_in_subclass():
```
for subclass in get_subclasses(Obj, get_subs=False):
    setattr(subclass, 'sprite', Image(subclass.__name__))
```
1. Obj의 하위 클래스들 중에서 제일 상위 클래스들만 불러옴.
2. 그 클래스들 하나하나에 cls.sprite = Image(subclass.\_\_name\_\_) 부여
   
### .assign_copied_in_subclass():
```
for subclass in get_subclasses(Obj, get_supers=False):
    setattr(subclass, 'copied', 0)
```
1. Obj의 하위 클래스들 중에서 제일 하위 클래스들만 불러옴.
2. 그 클래스들 하나하나에 cls.copied = 0 부여
   
### .assign_saves_in_subclass():
```
for subclass in get_subclasses(Obj, get_supers=False):  # 하위 cls들만
    setattr(subclass, 'saves', {})
```
1. Obj의 하위 클래스들 중에서 제일 하위 클래스들만 불러옴.
2. 그 클래스들 하나하나에 cls.saves = {} 부여


### set_obj_groups(self):
```
for subclass in [Obj, Package, Bin, *get_subclasses(Package), *get_subclasses(Obj, get_supers=False)]:
```
* 스프라이트 불러오기가 필요한 클래스들을 모두 [] 안에 담아, 하나씩 꺼냄.

```
    attr_name = f'{subclass.__name__.lower()}s'
```
예를 들어 Obj 클래스일 경우,
1. subclass.\_\_name__ == 'Obj'
2. 'Obj'.lower() → 'obj'
3. f'{'obj'}s' → 'objs'

```
    setattr(self, attr_name, pg.sprite.Group())
```
4. self.objs = pg.sprite.Group()

```
    subclass.s = getattr(self, attr_name)
```
5. Obj.s = self.objs


### .apply_system_keys():
게임 외적인(시스템적인) 키 설정.

### 추가 정보
* pg.mixer.Channel(0)에는 BGM.s['title']이 들어감.
* pg.mixer.Channel(1)에는 BGM.s['game1']이 들어감.
* pg.mixer.Channel(2)에는 BGM.s['game2']이 들어감.
* pg.mixer.Channel(3)에는 BGM.s['credits']가 들어감.


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
헌재 눌러져 있는 키가 있으면, 그 키를 <sup>[/data/_bios.py](#)</sup>Key.keep<sup>[list](#)</sup>에 저장.

## input_once(cls, event):
헌재 눌러져 있는 키가 있으면, 그 키를 Key.keep에 저장.

```
if event is None:
    Mouse.event, Key.down, Key.up = None, [], []
```
상태변화(event)가 있든 없든 무조건 Mouse.event<sup>[str](#)</sup>(마우스 클릭 여부 저장), Key.down(키보드 눌리기 시작한 키 저장), 
Key.up<sup>[list](#)</sup>(키보드 막 떼어진 키 저장) 변수를 초기화한다.

```
elif event.type == KEYDOWN:
......
```
* 지금 키보드의 어떤 키가 막 눌렸을 경우, 그 키를 Key.down<sup>[list](#)</sup>에 추가.

```
elif event.type == KEYUP:
......
```
* 지금 키보드의 어떤 키가 막 떼어졌을 경우, 그 키를 Key.up<sup>[list](#)</sup>에 추가.

```
elif event.type == QUIT:
    pg.quit(), sys.exit()
```
게임 창 우상단의 [X]를 클릭하면 게임 종료. 절대 삭제하지 말 것!!!


# object.py
## Obj(pg.sprite.Sprite)
### get(cls, name=None)
```
objs = cls.s.sprites()
```
* cls.s: 객체의 클래스에서 생성된 모든 객체들이 담겨 있는 그룹.
* .sprites(): Group 타입을 list 타입으로 변환. (Group 타입은 for문으로 하나씩 뽑기가 안 되기 때문)

```
if name is None:
    return objs[0]
```
어떤 객체를 불러올지 이름을 딱히 지정하지 않았다면, 그냥 그 객체들 list 중에서 제일 앞엣놈을 리턴.


```
else:
    for obj in objs:
        if obj.name == name:
            return obj
```
찾고자 하는 이름이 있다면, 그 이름을 가진 객체를 리턴.

### set_sprite(self, *keywords)

```
    for keyword in split(keywords):
```
입력한 키워드들을 list로 묶어 하나하나씩 꺼냄.\
키워드에 _ 문자가 있으면 (두 단어가 이어져 있는 것으로 간주하고) 쪼갬.

```
        for i, subkeys in self.__class__.sprite.subkeys.items():
```
객체 클래스의 스프라이트에 사용된 모든 단어들을 불러옴.
* i : 0이면 self.name에 사용된 모든 키워드들, 1이면 self.imgkey의 1번째 자릿수에 사용된 모든 키워드들, 2면, self.
  imgkey의 2번째 자릿수에 사용된 모든 키워드들, ......

```
            if keyword in subkeys:
                indexes[i] = keyword
            elif not keyword or keyword is None:
                self.hide()
```
* 입력한 키워드가 실제로 사용됐던 키워드라면, indexes<sup>[dict](#)</sup>에 {자릿수: 입력한 키워드} 추가
* 입력한 키워드가 '' 혹은 None이라면, 해당 객체의 스프라이트를 없애버림.

```
    assert indexes, f"잘못된 키워드{keywords}가 입력되었습니다."
```
indexes에 키워드가 하나도 없다면, 입력한 키워드가 실제로 사용되지 않은 **잘못된 키워드**라는 뜻이기에, 오류를 발생. 


```
    for i, self_subkey in enumerate(split(self.imgkey), start=1):
        if i in indexes:
            result.append(indexes[i])
        else:
            result.append(self_subkey)
            
    self.imgkey = '_'.join(result)
```
입력한 키워드가 해당 자릿수에 있으면 그 자릿수에 키워드를 넣고, 그렇지 않다면 기존 self.imgkey의 해당 자릿수에 있던 
키워드를 그대로 할당.




# package.py

# data/_bios.py

# data/_constants.py

# data/_debugtools.py

# data/_clstools.py

# data/_functools.py

# 각주

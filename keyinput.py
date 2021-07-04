""" Project PPP v0.4.0 """

import sys

from package import *


class Keyinput:
    __Lclick = Framewatch('ANTI-MASHING', min_sec=0.2)

    @classmethod
    def update(cls):
        """키 설정
        """
        Mouse.pos = pg.mouse.get_pos()  # 마우스 커서 좌표 할당

        cls.input_keep(pg.key.get_pressed())

        for event in [None, *pg.event.get()]:
            cls.input_once(event)

    @classmethod
    def input_keep(cls, key):
        """키 설정
        """
        if key[pg.K_BACKSPACE]:
            append(Key.keep, 'backspace')
        else:
            remove(Key.keep, 'backspace')

        if key[pg.K_TAB]:
            append(Key.keep, 'tab')
        else:
            remove(Key.keep, 'tab')

        if key[pg.K_ESCAPE]:
            append(Key.keep, 'esc')
        else:
            remove(Key.keep, 'esc')

        if key[pg.K_SPACE]:
            append(Key.keep, 'space')
        else:
            remove(Key.keep, 'space')

        if key[pg.K_EXCLAIM]:
            append(Key.keep, '!')
        else:
            remove(Key.keep, '!')

        if key[pg.K_QUOTE]:
            append(Key.keep, '\'')
        else:
            remove(Key.keep, '\'')

        if key[pg.K_QUOTEDBL]:
            append(Key.keep, '\"')
        else:
            remove(Key.keep, '\"')

        if key[pg.K_HASH]:
            append(Key.keep, '#')
        else:
            remove(Key.keep, '#')

        if key[pg.K_DOLLAR]:
            append(Key.keep, '$')
        else:
            remove(Key.keep, '$')

        if key[pg.K_AMPERSAND]:
            append(Key.keep, '&')
        else:
            remove(Key.keep, '&')

        if key[pg.K_LEFTPAREN]:
            append(Key.keep, '(')
        else:
            remove(Key.keep, '(')

        if key[pg.K_RIGHTPAREN]:
            append(Key.keep, ')')
        else:
            remove(Key.keep, ')')

        if key[pg.K_COMMA]:
            append(Key.keep, ',')
        else:
            remove(Key.keep, ',')

        if key[pg.K_QUESTION]:
            append(Key.keep, '?')
        else:
            remove(Key.keep, '?')

        if key[pg.K_COLON]:
            append(Key.keep, ':')
        else:
            remove(Key.keep, ':')

        if key[pg.K_SEMICOLON]:
            append(Key.keep, ';')
        else:
            remove(Key.keep, ';')

        if key[pg.K_LESS]:
            append(Key.keep, '<')
        else:
            remove(Key.keep, '<')

        if key[pg.K_GREATER]:
            append(Key.keep, '>')
        else:
            remove(Key.keep, '>')

        if key[pg.K_AT]:
            append(Key.keep, '@')
        else:
            remove(Key.keep, '@')

        if key[pg.K_LEFTBRACKET]:
            append(Key.keep, '[')
        else:
            remove(Key.keep, '[')

        if key[pg.K_BACKSLASH]:
            append(Key.keep, '\\')
        else:
            remove(Key.keep, '\\')

        if key[pg.K_RIGHTBRACKET]:
            append(Key.keep, ']')
        else:
            remove(Key.keep, ']')

        if key[pg.K_CARET]:
            append(Key.keep, '^')
        else:
            remove(Key.keep, '^')

        if key[pg.K_UNDERSCORE]:
            append(Key.keep, '_')
        else:
            remove(Key.keep, '_')

        if key[pg.K_BACKQUOTE]:
            append(Key.keep, '`')
        else:
            remove(Key.keep, '`')

        if key[pg.K_a]:
            append(Key.keep, 'a')
        else:
            remove(Key.keep, 'a')

        if key[pg.K_b]:
            append(Key.keep, 'b')
        else:
            remove(Key.keep, 'b')

        if key[pg.K_c]:
            append(Key.keep, 'c')
        else:
            remove(Key.keep, 'c')

        if key[pg.K_d]:
            append(Key.keep, 'd')
        else:
            remove(Key.keep, 'd')

        if key[pg.K_e]:
            append(Key.keep, 'e')
        else:
            remove(Key.keep, 'e')

        if key[pg.K_f]:
            append(Key.keep, 'f')
        else:
            remove(Key.keep, 'f')

        if key[pg.K_g]:
            append(Key.keep, 'g')
        else:
            remove(Key.keep, 'g')

        if key[pg.K_h]:
            append(Key.keep, 'h')
        else:
            remove(Key.keep, 'h')

        if key[pg.K_i]:
            append(Key.keep, 'i')
        else:
            remove(Key.keep, 'i')

        if key[pg.K_j]:
            append(Key.keep, 'j')
        else:
            remove(Key.keep, 'j')

        if key[pg.K_k]:
            append(Key.keep, 'k')
        else:
            remove(Key.keep, 'k')

        if key[pg.K_l]:
            append(Key.keep, 'l')
        else:
            remove(Key.keep, 'l')

        if key[pg.K_m]:
            append(Key.keep, 'm')
        else:
            remove(Key.keep, 'm')

        if key[pg.K_n]:
            append(Key.keep, 'n')
        else:
            remove(Key.keep, 'n')

        if key[pg.K_o]:
            append(Key.keep, 'o')
        else:
            remove(Key.keep, 'o')

        if key[pg.K_p]:
            append(Key.keep, 'p')
        else:
            remove(Key.keep, 'p')

        if key[pg.K_q]:
            append(Key.keep, 'q')
        else:
            remove(Key.keep, 'q')

        if key[pg.K_r]:
            append(Key.keep, 'r')
        else:
            remove(Key.keep, 'r')

        if key[pg.K_s]:
            append(Key.keep, 's')
        else:
            remove(Key.keep, 's')

        if key[pg.K_t]:
            append(Key.keep, 't')
        else:
            remove(Key.keep, 't')

        if key[pg.K_u]:
            append(Key.keep, 'u')
        else:
            remove(Key.keep, 'u')

        if key[pg.K_v]:
            append(Key.keep, 'v')
        else:
            remove(Key.keep, 'v')

        if key[pg.K_w]:
            append(Key.keep, 'w')
        else:
            remove(Key.keep, 'w')

        if key[pg.K_x]:
            append(Key.keep, 'x')
        else:
            remove(Key.keep, 'x')

        if key[pg.K_y]:
            append(Key.keep, 'y')
        else:
            remove(Key.keep, 'y')

        if key[pg.K_z]:
            append(Key.keep, 'z')
        else:
            remove(Key.keep, 'z')

        if key[pg.K_UP]:
            append(Key.keep, 'up')
        else:
            remove(Key.keep, 'up')

        if key[pg.K_DOWN]:
            append(Key.keep, 'down')
        else:
            remove(Key.keep, 'down')

        if key[pg.K_LEFT]:
            append(Key.keep, 'left')
        else:
            remove(Key.keep, 'left')

        if key[pg.K_RIGHT]:
            append(Key.keep, 'right')
        else:
            remove(Key.keep, 'right')

        if key[pg.K_DELETE]:
            append(Key.keep, 'delete')
        else:
            remove(Key.keep, 'delete')

        if key[pg.K_INSERT]:
            append(Key.keep, 'insert')
        else:
            remove(Key.keep, 'insert')

        if key[pg.K_HOME]:
            append(Key.keep, 'home')
        else:
            remove(Key.keep, 'home')

        if key[pg.K_END]:
            append(Key.keep, 'end')
        else:
            remove(Key.keep, 'end')

        if key[pg.K_PAGEUP]:
            append(Key.keep, 'pageup')
        else:
            remove(Key.keep, 'pageup')

        if key[pg.K_PAGEDOWN]:
            append(Key.keep, 'pagedown')
        else:
            remove(Key.keep, 'pagedown')

        if key[pg.K_F1]:
            append(Key.keep, 'F1')
        else:
            remove(Key.keep, 'F1')

        if key[pg.K_F2]:
            append(Key.keep, 'F2')
        else:
            remove(Key.keep, 'F2')

        if key[pg.K_F3]:
            append(Key.keep, 'F3')
        else:
            remove(Key.keep, 'F3')

        if key[pg.K_F4]:
            append(Key.keep, 'F4')
        else:
            remove(Key.keep, 'F4')

        if key[pg.K_F5]:
            append(Key.keep, 'F5')
        else:
            remove(Key.keep, 'F5')

        if key[pg.K_F6]:
            append(Key.keep, 'F6')
        else:
            remove(Key.keep, 'F6')

        if key[pg.K_F7]:
            append(Key.keep, 'F7')
        else:
            remove(Key.keep, 'F7')

        if key[pg.K_F8]:
            append(Key.keep, 'F8')
        else:
            remove(Key.keep, 'F8')

        if key[pg.K_F9]:
            append(Key.keep, 'F9')
        else:
            remove(Key.keep, 'F9')

        if key[pg.K_F10]:
            append(Key.keep, 'F10')
        else:
            remove(Key.keep, 'F10')

        if key[pg.K_F11]:
            append(Key.keep, 'F11')
        else:
            remove(Key.keep, 'F11')

        if key[pg.K_F12]:
            append(Key.keep, 'F12')
        else:
            remove(Key.keep, 'F12')

        if key[pg.K_CAPSLOCK]:
            append(Key.keep, 'capslock')
        else:
            remove(Key.keep, 'capslock')

        if key[pg.K_RETURN] or key[pg.K_KP_ENTER]:
            append(Key.keep, 'enter')
        else:
            remove(Key.keep, 'enter')

        if key[pg.K_ASTERISK] or key[pg.K_KP_MULTIPLY]:
            append(Key.keep, '*')
        else:
            remove(Key.keep, '*')

        if key[pg.K_PLUS] or key[pg.K_KP_PLUS]:
            append(Key.keep, '+')
        else:
            remove(Key.keep, '+')

        if key[pg.K_MINUS] or key[pg.K_KP_MINUS]:
            append(Key.keep, '-')
        else:
            remove(Key.keep, '-')

        if key[pg.K_PERIOD] or key[pg.K_KP_PERIOD]:
            append(Key.keep, '.')
        else:
            remove(Key.keep, '.')

        if key[pg.K_SLASH] or key[pg.K_KP_DIVIDE]:
            append(Key.keep, '/')
        else:
            remove(Key.keep, '/')

        if key[pg.K_EQUALS] or key[pg.K_KP_EQUALS]:
            append(Key.keep, '=')
        else:
            remove(Key.keep, '=')

        if key[pg.K_0] or key[pg.K_KP0]:
            append(Key.keep, '0')
        else:
            remove(Key.keep, '0')

        if key[pg.K_1] or key[pg.K_KP1]:
            append(Key.keep, '1')
        else:
            remove(Key.keep, '1')

        if key[pg.K_2] or key[pg.K_KP2]:
            append(Key.keep, '2')
        else:
            remove(Key.keep, '2')

        if key[pg.K_3] or key[pg.K_KP3]:
            append(Key.keep, '3')
        else:
            remove(Key.keep, '3')

        if key[pg.K_4] or key[pg.K_KP4]:
            append(Key.keep, '4')
        else:
            remove(Key.keep, '4')

        if key[pg.K_5] or key[pg.K_KP5]:
            append(Key.keep, '5')
        else:
            remove(Key.keep, '5')

        if key[pg.K_6] or key[pg.K_KP6]:
            append(Key.keep, '6')
        else:
            remove(Key.keep, '6')

        if key[pg.K_7] or key[pg.K_KP7]:
            append(Key.keep, '7')
        else:
            remove(Key.keep, '7')

        if key[pg.K_8] or key[pg.K_KP8]:
            append(Key.keep, '8')
        else:
            remove(Key.keep, '8')

        if key[pg.K_9] or key[pg.K_KP9]:
            append(Key.keep, '9')
        else:
            remove(Key.keep, '9')

        if key[pg.K_LSHIFT] or key[pg.K_RSHIFT]:
            append(Key.keep, 'shift')
        else:
            remove(Key.keep, 'shift')

        if key[pg.K_LCTRL] or key[pg.K_RCTRL]:
            append(Key.keep, 'ctrl')
        else:
            remove(Key.keep, 'ctrl')

        if key[pg.K_LALT] or key[pg.K_RALT]:
            append(Key.keep, 'alt')
        else:
            remove(Key.keep, 'alt')

        if pg.mouse.get_pressed(num_buttons=3)[0]:
            append(Key.keep, 'mouse_l')
        else:
            remove(Key.keep, 'mouse_l')

        if pg.mouse.get_pressed(num_buttons=3)[1]:
            append(Key.keep, 'mouse_m')
        else:
            remove(Key.keep, 'mouse_m')

        if pg.mouse.get_pressed(num_buttons=3)[2]:
            append(Key.keep, 'mouse_r')
        else:
            remove(Key.keep, 'mouse_r')

    @classmethod
    def input_once(cls, event):
        """키 설정
        """
        if event is None:
            Mouse.event, Key.down, Key.up = None, [], []

        elif event.type == QUIT:  # [x]를 클릭하면 게임 종료
            pg.quit(), sys.exit()

        elif event.type == KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                append(Key.down, 'backspace')
            elif event.key == pg.K_TAB:
                append(Key.down, 'tab')
            elif event.key == pg.K_ESCAPE:
                append(Key.down, 'esc')
            elif event.key == pg.K_SPACE:
                append(Key.down, 'space')
            elif event.key == pg.K_EXCLAIM:
                append(Key.down, '!')
            elif event.key == pg.K_QUOTE:
                append(Key.down, '\'')
            elif event.key == pg.K_QUOTEDBL:
                append(Key.down, '\"')
            elif event.key == pg.K_HASH:
                append(Key.down, '#')
            elif event.key == pg.K_DOLLAR:
                append(Key.down, '$')
            elif event.key == pg.K_AMPERSAND:
                append(Key.down, '&')
            elif event.key == pg.K_LEFTPAREN:
                append(Key.down, '(')
            elif event.key == pg.K_RIGHTPAREN:
                append(Key.down, ')')
            elif event.key == pg.K_COMMA:
                append(Key.down, ',')
            elif event.key == pg.K_QUESTION:
                append(Key.down, '?')
            elif event.key == pg.K_COLON:
                append(Key.down, ':')
            elif event.key == pg.K_SEMICOLON:
                append(Key.down, ';')
            elif event.key == pg.K_LESS:
                append(Key.down, '<')
            elif event.key == pg.K_GREATER:
                append(Key.down, '>')
            elif event.key == pg.K_AT:
                append(Key.down, '@')
            elif event.key == pg.K_LEFTBRACKET:
                append(Key.down, '[')
            elif event.key == pg.K_BACKSLASH:
                append(Key.down, '\\')
            elif event.key == pg.K_RIGHTBRACKET:
                append(Key.down, ']')
            elif event.key == pg.K_CARET:
                append(Key.down, '^')
            elif event.key == pg.K_UNDERSCORE:
                append(Key.down, '_')
            elif event.key == pg.K_BACKQUOTE:
                append(Key.down, '`')
            elif event.key == pg.K_a:
                append(Key.down, 'a')
            elif event.key == pg.K_b:
                append(Key.down, 'b')
            elif event.key == pg.K_c:
                append(Key.down, 'c')
            elif event.key == pg.K_d:
                append(Key.down, 'd')
            elif event.key == pg.K_e:
                append(Key.down, 'e')
            elif event.key == pg.K_f:
                append(Key.down, 'f')
            elif event.key == pg.K_g:
                append(Key.down, 'g')
            elif event.key == pg.K_h:
                append(Key.down, 'h')
            elif event.key == pg.K_i:
                append(Key.down, 'i')
            elif event.key == pg.K_j:
                append(Key.down, 'j')
            elif event.key == pg.K_k:
                append(Key.down, 'k')
            elif event.key == pg.K_l:
                append(Key.down, 'l')
            elif event.key == pg.K_m:
                append(Key.down, 'm')
            elif event.key == pg.K_n:
                append(Key.down, 'n')
            elif event.key == pg.K_o:
                append(Key.down, 'o')
            elif event.key == pg.K_p:
                append(Key.down, 'p')
            elif event.key == pg.K_q:
                append(Key.down, 'q')
            elif event.key == pg.K_r:
                append(Key.down, 'r')
            elif event.key == pg.K_s:
                append(Key.down, 's')
            elif event.key == pg.K_t:
                append(Key.down, 't')
            elif event.key == pg.K_u:
                append(Key.down, 'u')
            elif event.key == pg.K_v:
                append(Key.down, 'v')
            elif event.key == pg.K_w:
                append(Key.down, 'w')
            elif event.key == pg.K_x:
                append(Key.down, 'x')
            elif event.key == pg.K_y:
                append(Key.down, 'y')
            elif event.key == pg.K_z:
                append(Key.down, 'z')
            elif event.key == pg.K_UP:
                append(Key.down, 'up')
            elif event.key == pg.K_DOWN:
                append(Key.down, 'down')
            elif event.key == pg.K_LEFT:
                append(Key.down, 'left')
            elif event.key == pg.K_RIGHT:
                append(Key.down, 'right')
            elif event.key == pg.K_DELETE:
                append(Key.down, 'delete')
            elif event.key == pg.K_INSERT:
                append(Key.down, 'insert')
            elif event.key == pg.K_HOME:
                append(Key.down, 'home')
            elif event.key == pg.K_END:
                append(Key.down, 'end')
            elif event.key == pg.K_PAGEUP:
                append(Key.down, 'pageup')
            elif event.key == pg.K_PAGEDOWN:
                append(Key.down, 'pagedown')
            elif event.key == pg.K_F1:
                append(Key.down, 'F1')
            elif event.key == pg.K_F2:
                append(Key.down, 'F2')
            elif event.key == pg.K_F3:
                append(Key.down, 'F3')
            elif event.key == pg.K_F4:
                append(Key.down, 'F4')
            elif event.key == pg.K_F5:
                append(Key.down, 'F5')
            elif event.key == pg.K_F6:
                append(Key.down, 'F6')
            elif event.key == pg.K_F7:
                append(Key.down, 'F7')
            elif event.key == pg.K_F8:
                append(Key.down, 'F8')
            elif event.key == pg.K_F9:
                append(Key.down, 'F9')
            elif event.key == pg.K_F10:
                append(Key.down, 'F10')
            elif event.key == pg.K_F11:
                append(Key.down, 'F11')
            elif event.key == pg.K_F12:
                append(Key.down, 'F12')
            elif event.key == pg.K_CAPSLOCK:
                append(Key.down, 'capslock')
            elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                append(Key.down, 'enter')
            elif event.key in [pg.K_ASTERISK, pg.K_KP_MULTIPLY]:
                append(Key.down, '*')
            elif event.key in [pg.K_PLUS, pg.K_KP_PLUS]:
                append(Key.down, '+')
            elif event.key in [pg.K_MINUS, pg.K_KP_MINUS]:
                append(Key.down, '-')
            elif event.key in [pg.K_PERIOD, pg.K_KP_PERIOD]:
                append(Key.down, '.')
            elif event.key in [pg.K_SLASH, pg.K_KP_DIVIDE]:
                append(Key.down, '/')
            elif event.key in [pg.K_EQUALS, pg.K_KP_EQUALS]:
                append(Key.down, '=')
            elif event.key in [pg.K_0, pg.K_KP0]:
                append(Key.down, '0')
            elif event.key in [pg.K_1, pg.K_KP1]:
                append(Key.down, '1')
            elif event.key in [pg.K_2, pg.K_KP2]:
                append(Key.down, '2')
            elif event.key in [pg.K_3, pg.K_KP3]:
                append(Key.down, '3')
            elif event.key in [pg.K_4, pg.K_KP4]:
                append(Key.down, '4')
            elif event.key in [pg.K_5, pg.K_KP5]:
                append(Key.down, '5')
            elif event.key in [pg.K_6, pg.K_KP6]:
                append(Key.down, '6')
            elif event.key in [pg.K_7, pg.K_KP7]:
                append(Key.down, '7')
            elif event.key in [pg.K_8, pg.K_KP8]:
                append(Key.down, '8')
            elif event.key in [pg.K_9, pg.K_KP9]:
                append(Key.down, '9')
            elif event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                append(Key.down, 'shift')
            elif event.key in [pg.K_LCTRL, pg.K_RCTRL]:
                append(Key.down, 'ctrl')
            elif event.key in [pg.K_LALT, pg.K_RALT]:
                append(Key.down, 'alt')

        elif event.type == KEYUP:
            if event.key == pg.K_BACKSPACE:
                append(Key.up, 'backspace')
            elif event.key == pg.K_TAB:
                append(Key.up, 'tab')
            elif event.key == pg.K_ESCAPE:
                append(Key.up, 'esc')
            elif event.key == pg.K_SPACE:
                append(Key.up, 'space')
            elif event.key == pg.K_EXCLAIM:
                append(Key.up, '!')
            elif event.key == pg.K_QUOTE:
                append(Key.up, '\'')
            elif event.key == pg.K_QUOTEDBL:
                append(Key.up, '\"')
            elif event.key == pg.K_HASH:
                append(Key.up, '#')
            elif event.key == pg.K_DOLLAR:
                append(Key.up, '$')
            elif event.key == pg.K_AMPERSAND:
                append(Key.up, '&')
            elif event.key == pg.K_LEFTPAREN:
                append(Key.up, '(')
            elif event.key == pg.K_RIGHTPAREN:
                append(Key.up, ')')
            elif event.key == pg.K_COMMA:
                append(Key.up, ',')
            elif event.key == pg.K_QUESTION:
                append(Key.up, '?')
            elif event.key == pg.K_COLON:
                append(Key.up, ':')
            elif event.key == pg.K_SEMICOLON:
                append(Key.up, ';')
            elif event.key == pg.K_LESS:
                append(Key.up, '<')
            elif event.key == pg.K_GREATER:
                append(Key.up, '>')
            elif event.key == pg.K_AT:
                append(Key.up, '@')
            elif event.key == pg.K_LEFTBRACKET:
                append(Key.up, '[')
            elif event.key == pg.K_BACKSLASH:
                append(Key.up, '\\')
            elif event.key == pg.K_RIGHTBRACKET:
                append(Key.up, ']')
            elif event.key == pg.K_CARET:
                append(Key.up, '^')
            elif event.key == pg.K_UNDERSCORE:
                append(Key.up, '_')
            elif event.key == pg.K_BACKQUOTE:
                append(Key.up, '`')
            elif event.key == pg.K_a:
                append(Key.up, 'a')
            elif event.key == pg.K_b:
                append(Key.up, 'b')
            elif event.key == pg.K_c:
                append(Key.up, 'c')
            elif event.key == pg.K_d:
                append(Key.up, 'd')
            elif event.key == pg.K_e:
                append(Key.up, 'e')
            elif event.key == pg.K_f:
                append(Key.up, 'f')
            elif event.key == pg.K_g:
                append(Key.up, 'g')
            elif event.key == pg.K_h:
                append(Key.up, 'h')
            elif event.key == pg.K_i:
                append(Key.up, 'i')
            elif event.key == pg.K_j:
                append(Key.up, 'j')
            elif event.key == pg.K_k:
                append(Key.up, 'k')
            elif event.key == pg.K_l:
                append(Key.up, 'l')
            elif event.key == pg.K_m:
                append(Key.up, 'm')
            elif event.key == pg.K_n:
                append(Key.up, 'n')
            elif event.key == pg.K_o:
                append(Key.up, 'o')
            elif event.key == pg.K_p:
                append(Key.up, 'p')
            elif event.key == pg.K_q:
                append(Key.up, 'q')
            elif event.key == pg.K_r:
                append(Key.up, 'r')
            elif event.key == pg.K_s:
                append(Key.up, 's')
            elif event.key == pg.K_t:
                append(Key.up, 't')
            elif event.key == pg.K_u:
                append(Key.up, 'u')
            elif event.key == pg.K_v:
                append(Key.up, 'v')
            elif event.key == pg.K_w:
                append(Key.up, 'w')
            elif event.key == pg.K_x:
                append(Key.up, 'x')
            elif event.key == pg.K_y:
                append(Key.up, 'y')
            elif event.key == pg.K_z:
                append(Key.up, 'z')
            elif event.key == pg.K_UP:
                append(Key.up, 'up')
            elif event.key == pg.K_DOWN:
                append(Key.up, 'down')
            elif event.key == pg.K_LEFT:
                append(Key.up, 'left')
            elif event.key == pg.K_RIGHT:
                append(Key.up, 'right')
            elif event.key == pg.K_DELETE:
                append(Key.up, 'delete')
            elif event.key == pg.K_INSERT:
                append(Key.up, 'insert')
            elif event.key == pg.K_HOME:
                append(Key.up, 'home')
            elif event.key == pg.K_END:
                append(Key.up, 'end')
            elif event.key == pg.K_PAGEUP:
                append(Key.up, 'pageup')
            elif event.key == pg.K_PAGEDOWN:
                append(Key.up, 'pagedown')
            elif event.key == pg.K_F1:
                append(Key.up, 'F1')
            elif event.key == pg.K_F2:
                append(Key.up, 'F2')
            elif event.key == pg.K_F3:
                append(Key.up, 'F3')
            elif event.key == pg.K_F4:
                append(Key.up, 'F4')
            elif event.key == pg.K_F5:
                append(Key.up, 'F5')
            elif event.key == pg.K_F6:
                append(Key.up, 'F6')
            elif event.key == pg.K_F7:
                append(Key.up, 'F7')
            elif event.key == pg.K_F8:
                append(Key.up, 'F8')
            elif event.key == pg.K_F9:
                append(Key.up, 'F9')
            elif event.key == pg.K_F10:
                append(Key.up, 'F10')
            elif event.key == pg.K_F11:
                append(Key.up, 'F11')
            elif event.key == pg.K_F12:
                append(Key.up, 'F12')
            elif event.key == pg.K_CAPSLOCK:
                append(Key.up, 'capslock')
            elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                append(Key.up, 'enter')
            elif event.key in [pg.K_ASTERISK, pg.K_KP_MULTIPLY]:
                append(Key.up, '*')
            elif event.key in [pg.K_PLUS, pg.K_KP_PLUS]:
                append(Key.up, '+')
            elif event.key in [pg.K_MINUS, pg.K_KP_MINUS]:
                append(Key.up, '-')
            elif event.key in [pg.K_PERIOD, pg.K_KP_PERIOD]:
                append(Key.up, '.')
            elif event.key in [pg.K_SLASH, pg.K_KP_DIVIDE]:
                append(Key.up, '/')
            elif event.key in [pg.K_EQUALS, pg.K_KP_EQUALS]:
                append(Key.up, '=')
            elif event.key in [pg.K_0, pg.K_KP0]:
                append(Key.up, '0')
            elif event.key in [pg.K_1, pg.K_KP1]:
                append(Key.up, '1')
            elif event.key in [pg.K_2, pg.K_KP2]:
                append(Key.up, '2')
            elif event.key in [pg.K_3, pg.K_KP3]:
                append(Key.up, '3')
            elif event.key in [pg.K_4, pg.K_KP4]:
                append(Key.up, '4')
            elif event.key in [pg.K_5, pg.K_KP5]:
                append(Key.up, '5')
            elif event.key in [pg.K_6, pg.K_KP6]:
                append(Key.up, '6')
            elif event.key in [pg.K_7, pg.K_KP7]:
                append(Key.up, '7')
            elif event.key in [pg.K_8, pg.K_KP8]:
                append(Key.up, '8')
            elif event.key in [pg.K_9, pg.K_KP9]:
                append(Key.up, '9')
            elif event.key in [pg.K_LSHIFT, pg.K_RSHIFT]:
                append(Key.up, 'shift')
            elif event.key in [pg.K_LCTRL, pg.K_RCTRL]:
                append(Key.up, 'ctrl')
            elif event.key in [pg.K_LALT, pg.K_RALT]:
                append(Key.up, 'alt')
                
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # click Left
                Mouse.event = CLICK_LEFT_DOWN
            elif event.button == 2:  # click Middle
                Mouse.event = CLICK_MIDDLE_DOWN
            elif event.button == 3:  # click Right
                Mouse.event = CLICK_RIGHT_DOWN
            elif event.button >= 4 and event.button % 2 == 0:  # wheel UP
                Mouse.event = WHEEL_UP
            elif event.button >= 5 and event.button % 2 == 1:  # wheel DOWN
                Mouse.event = WHEEL_DOWN

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:  # click Left
                Mouse.event = CLICK_LEFT_UP
            elif event.button == 2:  # click Middle
                Mouse.event = CLICK_MIDDLE_UP
            elif event.button == 3:  # click Right
                Mouse.event = CLICK_RIGHT_UP

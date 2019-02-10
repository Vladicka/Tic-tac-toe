# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

image bg = 'images/white_bg.png'
image x1 = 'images/x1.png'
default gamemode='single'
default field=['e','e','e','e','e','e','e','e','e']
default field_valuation=[1,1,1,1,2,1,1,1,1]
default player_mark='x'
default ai_mark='o'
default player_sound='/sound/cross_drawing.wav'
default ai_sound='/sound/circle_drawing.wav'
default valid_turn=True
default turn='player'
default winner='None'
default win_combination='000'
default game_status='preparing'
default mark_num=[1,1,1,1,1,1,1,1,1]
default packet_template=[0, '', '', True, '', []]
default nickname=None
default lobbies={}
default sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
default lobby_name=''
default current_lobby=[]
default recv_packet_thread=threading.Thread(target=recv_packet, args=())
default combination='000'
default countdown_sec=3
#current_lobby=[lobby_name, player_1, player_2, {player1:pl1_mark, player2:pl2_mark}, {player1:True/False, player2:True/False}]

init python:
    import socket
    import json

    def close_sock():
        global sock
        if gamemode=='multi':
            packet=[9]
            sock.send(json.dumps(packet).encode())
            sock.close()
        else:
            pass

define config.quit_action = [Function (close_sock)]

image my_caret:
    '/images/caret.png'
    linear 0.01 alpha 1.0
    pause 0.5
    linear 0.01 alpha 0.0
    pause 0.5
    repeat
init:
    $ style.input.caret = 'my_caret'

init python:
    import random
    import sys
    import socket
    import json
    import threading
    import time

    def ai():
        for i in range(0,9):
            if field[i]=='e':
                field_valuation[i]=1
        if field[4]=='e':
            field_valuation[4]=2
        val=0
        slice=field[0:3]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (0,3):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        val=0
        slice=field[3:6]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (3,6):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        val=0
        slice=field[6:9]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (6,9):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        val=0
        slice=field[0:7:3]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (0,7,3):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        val=0
        slice=field[1:8:3]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (1,8,3):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        val=0
        slice=field[2:9:3]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (2,9,3):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        val=0
        slice=field[0:9:4]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (0,9,4):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        val=0
        slice=field[2:7:2]
        if (slice.count(ai_mark)==2):
            val=4
        else:
            val=slice.count(player_mark)
            if (val==2):
                val=3
        for i in range (2,7,2):
            if (field[i]=='e'):
                field_valuation[i]=field_valuation[i]+val
            else:
                field_valuation[i]=0
        i=field_valuation.index(max(field_valuation))
        field_valuation[i]=0
        renpy.pause(0.5)
        ai_click(i)

    def click(i):
        global turn
        global valid_turn
        global mark_num
        global field
        if field[i]=='e' and turn=='player':
            renpy.play(player_sound, channel='sound')
            field[i]=player_mark
            mark_num[i]=random.randint(1,4)
            valid_turn=True
            turn='ai'

    def ai_click(i):
        global turn
        global valid_turn
        global field
        global mark_num
        if field[i]=='e':
            renpy.play(ai_sound, channel='sound')
            field[i]=ai_mark
            mark_num[i]=random.randint(1,4)
            valid_turn=True
            turn='player'

    def field_state_check():
        global winner
        global win_combination
        global game_status
        global turn
        global combination
        global field
        combination='000'
        if (field[0]==player_mark and field[1]==player_mark and field[2]==player_mark):
            winner='player'
            combination='012'
        elif (field[3]==player_mark and field[4]==player_mark and field[5]==player_mark):
            winner='player'
            combination='345'
        elif (field[6]==player_mark and field[7]==player_mark and field[8]==player_mark):
            winner='player'
            combination='678'
        elif (field[0]==player_mark and field[3]==player_mark and field[6]==player_mark):
            winner='player'
            combination='036'
        elif (field[1]==player_mark and field[4]==player_mark and field[7]==player_mark):
            winner='player'
            combination='147'
        elif (field[2]==player_mark and field[5]==player_mark and field[8]==player_mark):
            winner='player'
            combination='258'
        elif (field[0]==player_mark and field[4]==player_mark and field[8]==player_mark):
            winner='player'
            combination='048'
        elif (field[2]==player_mark and field[4]==player_mark and field[6]==player_mark):
            winner='player'
            combination='246'
        elif (field[0]==ai_mark and field[1]==ai_mark and field[2]==ai_mark):
            winner='ai'
            combination='012'
        elif (field[3]==ai_mark and field[4]==ai_mark and field[5]==ai_mark):
            winner='ai'
            combination='345'
        elif (field[6]==ai_mark and field[7]==ai_mark and field[8]==ai_mark):
            winner='ai'
            combination='678'
        elif (field[0]==ai_mark and field[3]==ai_mark and field[6]==ai_mark):
            winner='ai'
            combination='036'
        elif (field[1]==ai_mark and field[4]==ai_mark and field[7]==ai_mark):
            winner='ai'
            combination='147'
        elif (field[2]==ai_mark and field[5]==ai_mark and field[8]==ai_mark):
            winner='ai'
            combination='258'
        elif (field[0]==ai_mark and field[4]==ai_mark and field[8]==ai_mark):
            winner='ai'
            combination='048'
        elif (field[2]==ai_mark and field[4]==ai_mark and field[6]==ai_mark):
            winner='ai'
            combination='246'
        if (combination!='000' or field.count('e')==0):
            game_status='over'
            turn='None'

    def store_new_lobby_name(newstring):
        global lobby_name
        lobby_name=newstring

    def update_lobbies_list():
        global packet_template
        global lobbies
        global sock
        packet=packet_template
        packet[0]=1
        sock.send(json.dumps(packet).encode())
        recv_packet_thread=threading.Thread(target=recv_packet, args=())
        recv_packet_thread.start()

    def create_lobby():
        global packet_template
        global lobbies
        global sock
        global current_lobby
        global recv_packet_thread
        packet=[2, nickname, lobby_name, True, '', []]
        sock.send(json.dumps(packet).encode())
        recv_packet_thread=threading.Thread(target=recv_packet, args=())
        recv_packet_thread.start()

    def join_lobby(lobby_name):
        global sock
        packet=[3, nickname, lobby_name, True, '', []]
        sock.send(json.dumps(packet).encode())
        recv_packet_thread=threading.Thread(target=recv_packet, args=())
        recv_packet_thread.start()

    def multiplayer_reg():
        global nickname
        global sock
        global packet_template
        nickname=renpy.input('Enter your nickname for multiplayer.')
        nickname=nickname.strip()
        packet=packet_template
        packet[1]=nickname
        sock.send(json.dumps(packet).encode())
        buff=json.loads(sock.recv(1024))
        while buff[3]!=True:
            nickname=renpy.input('"'+buff[2]+'" is already taken.', default=buff[2])
            nickname=nickname.strip()
            packet[1]=str(nickname)
            sock.send(json.dumps(packet).encode())
            buff=json.loads(sock.recv(1024))
        renpy.show_screen('multiplayer_main_screen')
        update_lobbies_list()

    def change_rdy_status():
        global nickname
        global sock
        global packet_template
        global current_lobby
        if current_lobby[4][nickname]==True:
            packet=[4, '', '', False, '', []]
            current_lobby[4][nickname]=False
        else:
            packet=[4, '', '', True, '', []]
            current_lobby[4][nickname]=True
        sock.send(json.dumps(packet).encode())

    def recv_packet():
        global current_lobby
        global lobbies
        global sock
        global recv_packet_thread
        global game_status
        global player_mark
        global field
        buff=json.loads(sock.recv(1024))
        if buff[0]==1:
            lobbies=buff[5][0]
        elif buff[0]==2:
            if buff[3]==True:
                current_lobby=[buff[1], buff[2], buff[4], {}, {}]
                renpy.hide_screen('multiplayer_main_screen')
                renpy.show_screen('lobby_screen')
                recv_packet_thread=threading.Thread(target=recv_packet, args=())
                recv_packet_thread.start()
            else:
                renpy.show_screen('error_message_screen', 'Lobby with that name already exists! Please choose another one.')
        elif buff[0]==3:
            if buff[3]==True:
                current_lobby=[buff[1], buff[2], buff[4], {buff[2]:buff[5][0], buff[4]:buff[5][1]}, {buff[2]:False, buff[4]:False}]
                player_mark=current_lobby[3][nickname]
                renpy.hide_screen('multiplayer_main_screen')
                renpy.show_screen('lobby_screen')
                recv_packet_thread=threading.Thread(target=recv_packet, args=())
                recv_packet_thread.start()
            else:
                if buff[4]=='notexists':
                    renpy.show_screen('error_message_screen', 'Lobby you were trying to join does not exist! Please refresh lobby list.')
                if buff[4]=='lobbyfull':
                    renpy.show_screen('error_message_screen', 'Lobby is full!. Please refresh your lobby list and choose another one.')
        elif buff[0]==4:
            current_lobby[4][buff[1]]=buff[3]
            recv_packet_thread=threading.Thread(target=recv_packet, args=())
            recv_packet_thread.start()
        elif buff[0]==5:
            packet=[8]
            sock.send(json.dumps(packet).encode())
            game_status='on'
            multiplayer_game()

    def multiplayer_game():
        global sock
        global player_mark
        global ai_mark
        global player_sound
        global ai_sound
        global turn
        global field
        global mark_num
        global valid_turn
        global game_status
        global countdown_sec
        if player_mark=='o':
            ai_mark='x'
            turn='ai'
            player_sound='/sound/circle_drawing.wav'
            ai_sound='/sound/cross_drawing.wav'
        renpy.show_screen('countdown')
        time.sleep(1)
        countdown_sec=2
        time.sleep(1)
        countdown_sec=1
        time.sleep(1)
        renpy.hide_screen('countdown')
        renpy.hide_screen('lobby_screen')
        renpy.show_screen('tic_tac_toe', mode='multi')
        if turn=='ai':
            buff=json.loads(sock.recv(1024))
            print(buff)
            renpy.play(ai_sound, channel='sound')
            field=buff[2]
            mark_num=buff[3]
            turn='player'
        while game_status!='over':
            if turn=='ai' and valid_turn:
                field_state_check()
                if game_status=='over':
                    print('game_over')
                    packet=[7, nickname, field, mark_num]
                    sock.send(json.dumps(packet).encode())
                    break
                else:
                    packet=[6, nickname, field, mark_num]
                    sock.send(json.dumps(packet).encode())
                if game_status=='on':
                    print(game_status)
                    buff=json.loads(sock.recv(1024))
                    print(buff)
                    print('here')
                    renpy.play(ai_sound, channel='sound')
                    field=buff[2]
                    mark_num=buff[3]
                    field_state_check()
                    if game_status=='over':
                        break
                    turn='player'

define config.quit_action = [Function (close_sock), Quit()]
# The game starts here.

screen countdown():
    #modal True
    frame:
        area (350, 250, 550, 150)
        if countdown_sec==3:
            text 'Game starts in 3' xalign 0.5 yalign 0.5
        elif countdown_sec==2:
            text 'Game starts in 2' xalign 0.5 yalign 0.5
        elif countdown_sec==1:
            text 'Game starts in 1' xalign 0.5 yalign 0.5

screen error_message_screen(error_message):
    modal True
    frame:
        area (350, 250, 550, 150)
        text [error_message] xalign 0.5 yalign 0.1
        textbutton 'Ok' xalign 0.5 yalign 0.8 action Hide('error_message_screen')

screen multiplayer_main_screen():
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_D" action NullAction()
    key "noshift_d" action NullAction()
    key "noshift_V" action NullAction()
    key "noshift_v" action NullAction()
    key "noshift_F" action NullAction()
    key "noshift_f" action NullAction()
    key "noshift_S" action NullAction()
    key "noshift_s" action NullAction()
    key "noshift_H" action NullAction()
    key "noshift_h" action NullAction()
    default show_input=False
    tag multiplayer_main_screen
    add 'images/white_bg.png'
    button:
        area (0, 0, 1280, 720)
        action SetScreenVariable('show_input',False)
    frame: #lobbies list
        area (50, 50, 500, 600)
        text 'Lobbies'
        imagebutton auto 'images/refresh_%s.png' xpos 460 ypos 0 action Function(update_lobbies_list)
        vbox:
            label 'Name' text_size 32
            pos (10, 30, 150, 400)
            for lobby in lobbies:
                text [lobby] size 28
        vbox:
            label 'Host' text_size 32
            pos (250, 30, 100, 400)
            for lobby in lobbies:
                text [lobbies[lobby][int(0)]] size 28
        vbox:
            pos (380, 65, 100, 400)
            for lobby in lobbies:
                textbutton 'Join' text_size 28 action Function(join_lobby, lobby_name=lobby)

    frame: #new lobby
        area (600, 50, 600, 400)
        text 'New lobby'
        text 'Lobby name: ' pos (10, 60)
        add '/images/input_box.png' pos (165, 57)
        button:
            area (165, 60, 300, 32)
            action SetScreenVariable('show_input',True)
        if show_input:
            input default lobby_name changed store_new_lobby_name pos (172, 60) adjust_spacing False
        else:
            text [lobby_name] pos (172, 60) adjust_spacing False
        textbutton 'Create a lobby' xalign 0.5 yalign 0.5 action [SetScreenVariable('show_input',False), Function(create_lobby)]

screen lobby_screen():
    add 'images/white_bg.png'
    frame: #lobby
        area (50, 50, 1180, 600)
        text 'Lobby [current_lobby[0]]' size 32
        vbox:
            pos (10, 70, 150, 400)
            text [current_lobby[1]] size 24
            if current_lobby[2]=='':
                text 'Waiting for 2nd player...' size 24 ypos 30
            else:
                text [current_lobby[2]] size 24 ypos 30
        vbox:
            pos (300, 70, 100, 400)
            if current_lobby[2]!='':
                text [current_lobby[3][current_lobby[1]]] size 24
                text [current_lobby[3][current_lobby[2]]] size 24 ypos 30
        vbox:
            pos (450, 70, 100, 400)
            if current_lobby[2]!='':
                if current_lobby[4][current_lobby[1]]==True:
                    text 'Ready' size 24
                else:
                    text 'Not ready' size 24
                if current_lobby[4][current_lobby[2]]==True:
                    text 'Ready' size 24 ypos 30
                else:
                    text 'Not ready' size 24 ypos 30
        if current_lobby[2]!='':
            if current_lobby[4][nickname]==False:
                textbutton "I'm ready" pos (0, 200) sensitive game_status=='preparing' action Function(change_rdy_status)
            else:
                textbutton "I'm not ready" pos (0, 200) sensitive game_status=='preparing' action Function(change_rdy_status)


screen tic_tac_toe(mode):
    default align_tuple=((0.38, 0.25), (0.5, 0.25), (0.63, 0.25), (0.38, 0.47), (0.5, 0.46), (0.635, 0.467), (0.375, 0.72), (0.502, 0.72), (0.64, 0.72))
    add 'images/white_bg.png'
    add 'images/field.png' align 0.5, 0.5
    add 'images/%s.png'%(win_combination) align 0.5, 0.5
    for j in range (9):
        imagebutton idle 'images/b%s.png'%(j) hover 'images/b%s.png'%(j) selected_idle 'images/%s%s.png'%(field[j], mark_num[j]) selected_hover 'images/%s%s.png'%(field[j], mark_num[j]) selected field[j]!='e' align align_tuple[j] action Function (click, i=j)
    if mode=='multi':
        text '[current_lobby[1]] VS [current_lobby[2]]' size 32 xalign 0.5 yalign 0.1
        if game_status!='over':
            if turn=='player':
                text 'Your turn!' size 32 xalign 0.5 yalign 0.9
            else:
                if current_lobby[1]!=nickname:
                    text "[current_lobby[1]]'s turn!" xalign 0.5 yalign 0.9 size 32
                else:
                    text "[current_lobby[2]]'s turn!" xalign 0.5 yalign 0.9 size 32
screen mark_choosing():
    default hovered='none'
    add 'images/white_bg.png'
    text 'Choose your mark' size 36 xalign 0.5 yalign 0.25
    imagebutton auto 'images/o_button_%s.png' xalign 0.35 yalign 0.5 hovered SetScreenVariable('hovered', 'o') unhovered SetScreenVariable('hovered', 'none') action [SetVariable('player_mark','o'), SetVariable('ai_mark','x'), SetVariable('player_sound','/sound/circle_drawing.wav'), SetVariable('ai_sound','/sound/cross_drawing.wav'), SetVariable('turn','ai'), Hide('mark_choosing'), Show('tic_tac_toe',  mode='single')]
    imagebutton auto 'images/x_button_%s.png' xalign 0.65 yalign 0.5 hovered SetScreenVariable('hovered', 'x') unhovered SetScreenVariable('hovered', 'none') action [SetVariable('player_mark','x'), SetVariable('ai_mark','o'), SetVariable('player_sound','/sound/cross_drawing.wav'), SetVariable('ai_sound','/sound/circle_drawing.wav'), Hide('mark_choosing'), Show('tic_tac_toe', mode='single')]
    if (hovered=='x'):
        text 'You move first.' size 36 xalign 0.5 yalign 0.75
    elif (hovered=='o'):
        text 'Computer moves first.' size 36 xalign 0.5 yalign 0.75

screen game_over():
    add 'images/white_bg.png'
    if winner=='player':
        add 'images/victory.png' xalign 0.5 yalign 0.7
        text 'You won!' size 42 xalign 0.5 yalign 0.07
    elif winner=='ai':
        add 'images/loss.png' xalign 0.5 yalign 0.7
        text 'You lost, desu!' size 42 xalign 0.5 yalign 0.07
    else:
        add 'images/draw.png' xalign 0.5 yalign 0.7
        text 'Draw!' size 42 xalign 0.5 yalign 0.07

label start:
    $quick_menu=False
    $renpy.music.set_volume(0.8, channel='sound')
    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.`

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    # These display lines of dialogue.
    scene bg
    menu:
        "Singleplayer":
            $gamemode='single'
            $renpy.transition(fade)
            show screen mark_choosing
            $renpy.pause(1)
            $game_status='on'
        "Multiplayer":
            #$gamemode='multi'
            jump multiplayer

label singleplayer_game:
    $renpy.pause(0.1)
    if turn=='ai' and valid_turn==True:
        $field_state_check()
        $ai()
    if game_status=='on':
        $field_state_check()
        $renpy.pause(0.1)
        jump singleplayer_game
    else:
        if combination!='000':
            $renpy.pause(0.75)
            $win_combination=combination
            $renpy.play('/sound/line_drawing.wav', channel='sound')
        $renpy.pause(1)
        hide screen tic_tac_toe
        $renpy.transition(fade)
        show screen game_over
    $renpy.pause()
    $renpy.transition(fade)
    jump exit

label multiplayer:
    python:
        global sock
        global gamemode
        if renpy.mobile:
            addr='46.36.35.101'
            port='9090'
        else:
            if not renpy.loadable('./multiplayer_config'):
                renpy.show_screen('error_message_screen', "No multiplayer config file.")
                renpy.pause()
                renpy.jump('exit')
            else:
                file=renpy.file('./multiplayer_config')
                for line in file:
                    if line[0]=='#':
                        continue
                    else:
                        addr, port=line.split(':')
                        print(addr, port)
        try:
            sock.settimeout(1)
            sock.connect((addr, int(port)))
            sock.settimeout(None)
            gamemode='multi'
            multiplayer_reg()
        except socket.error:
            renpy.show_screen('error_message_screen', "Couldn't connect to server.")
            renpy.pause()
            renpy.jump('exit')

label multiplayer_game:
    $renpy.pause(0.1)
    if game_status!='over':
        jump multiplayer_game
    else:
        if combination!='000':
            $renpy.pause(0.75)
            $win_combination=combination
            $renpy.play('/sound/line_drawing.wav', channel='sound')
        $renpy.pause(1)
        hide screen tic_tac_toe
        $renpy.transition(fade)
        show screen game_over
        $renpy.pause()
        $renpy.pause(1)
        $renpy.transition(fade)
        show screen multiplayer_main_screen
        $renpy.pause(1)
        $field=['e','e','e','e','e','e','e','e','e']
        $field_valuation=[1,1,1,1,2,1,1,1,1]
        $player_mark='x'
        $ai_mark='o'
        $player_sound='/sound/cross_drawing.wav'
        $ai_sound='/sound/circle_drawing.wav'
        $valid_turn=True
        $turn='player'
        $winner='None'
        $win_combination='000'
        $game_status='preparing'
        $mark_num=[1,1,1,1,1,1,1,1,1]
        $lobbies={}
        $lobby_name=''
        $current_lobby=[]
        $combination='000'
        jump multiplayer_game

label exit:
    return
    # This ends the game.

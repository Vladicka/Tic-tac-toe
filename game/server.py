# -*- coding: utf-8 -*-

import socket
import sys
import random
import threading
import time
import json

#clients={'player1':conn}
#lobbies={'lobby_name':['pl1_name', 'pl_mark', 'pl2_name', 'pl2_mark']}
lobbies={}
clients={}
players_readiness_status={}
threads={}
packet_template=[0, 'server', '', True, '', []]
#[msg_type, 'nick1/win/lose/draw', 'nick2/confirmed/lobby_name', True/False, 'yes/no/win_comb/confirmed', field]
#    0              1(from whom)          2 (to whom)                3                    4                 5

def readiness_watchdog(player1, player2):
    conn1=clients[player1]
    conn2=clients[player2]
    while True:
        buff = json.loads(conn1.recv(1024))
        print(buff)
        if buff[0]==4:
            players_readiness_status[player1]=buff[3]
            packet=[4, player1, player2, buff[3], '', []]
            conn2.send(json.dumps(packet).encode())
        elif buff[0]==8:
            break
        
def lobby(lobby_name):
    global players
    global packet_template
    global lobbies
    global players_readiness_status
    packet=packet_template
    while lobbies[lobby_name][2]=='':
        time.sleep(0.1)
    print(lobbies)
    player1, player2 = lobbies[lobby_name][0], lobbies[lobby_name][2]
    players_readiness_status[player1]=False
    players_readiness_status[player2]=False
    if random.randint(1,10)>5:
        lobbies[lobby_name]=[player1, 'o', player2, 'x']
        packet=[3, lobby_name, player1, True, player2, ['o', 'x']]
    else:
        lobbies[lobby_name]=[player1, 'x', player2, 'o']
        packet=[3, lobby_name, player1, True, player2, ['x', 'o']]
    clients[player1].send(json.dumps(packet).encode())
    clients[player2].send(json.dumps(packet).encode())
    watchdog1=threading.Thread(name=player1, target=readiness_watchdog, args=(player1, player2))
    watchdog2=threading.Thread(name=player2, target=readiness_watchdog, args=(player2, player1))
    watchdog1.start()
    watchdog2.start()
    while not players_readiness_status[player1] or not players_readiness_status[player2]:
        continue
    packet=[5]
    clients[player1].send(json.dumps(packet).encode())
    clients[player2].send(json.dumps(packet).encode())
    #game1=threading.Thread(name='game_'+player1, target=game, args=(lobby_name, player1, player2))
    #game2=threading.Thread(name='game_'+player2, target=game, args=(lobby_name, player2, player1))
    #game1.start()
    #game2.start()
    if lobbies[lobby_name][1]=='x':
        game(lobby_name, player1, player2)
    else:
        game(lobby_name, player2, player1)

def game(lobby_name, player1, player2):
    global packet_template
    global lobbies
    global clients
    conn1=clients[player1]
    conn2=clients[player2]
    while True:
        try:
            buff=json.loads(conn1.recv(1024))
            print(buff)
        except EOFError:
            continue
        packet=buff
        L=conn2.send(json.dumps(packet).encode())
        print(l)
        if buff[0]==7:
            break
        try:
            buff=json.loads(conn2.recv(1024))
            print(buff)
        except EOFError:
            continue
        packet=buff
        L=conn1.send(json.dumps(packet).encode())
        print(l)
        if buff[0]==7:
            break
    del lobbies[lobby_name]
    

def process_client_sock(conn, addr):
    global players
    global players_in_game
    global packet_template
    global lobbies
    global threads
    print('Client at {}'.format(addr))
    while True:
        packet=packet_template
        try:
            buff=json.loads(conn.recv(1024))
            print(buff)
        except EOFError:
            continue
        if buff[0]==0: #player reg
            packet[2]=buff[1]
            if buff[1] in clients:
                packet[3]=False
                conn.send(json.dumps(packet).encode())
            else:
                clients[buff[1]]=conn
                print('Client at {} is now known as {}'.format(addr, buff[1]))
                packet[3]=True
                conn.send(json.dumps(packet).encode())
        elif buff[0]==1: #lobby list req
            packet=[1, 'server', buff[1], True, '', [lobbies]]
            conn.send(json.dumps(packet).encode())
        elif buff[0]==2: #creating a new lobby
            packet=[2, buff[2], buff[1], True, '', ['','']]
            if buff[2] in lobbies:
                packet[3]=False
                conn.send(json.dumps(packet).encode())
            else:
                lobbies[buff[2]]=[buff[1], '', '', '']
                lobby_thread=threading.Thread(name=buff[2], target=lobby,args=(buff[2],))
                threads[buff[2]]=lobby_thread
                lobby_thread.start()
                conn.send(json.dumps(packet).encode())
                lobby_thread.join()
        elif buff[0]==3: #joining a lobby
            if buff[2] not in lobbies:
                packet=[3, 'server', buff[1], False, 'notexists', []]
                conn.send(json.dumps(packet).encode())
            elif lobbies[buff[2]][2]!='':
                packet=[3, 'server', buff[1], False, 'lobbyfull', []]
                conn.send(json.dumps(packet).encode())
            else:
                temp_list=lobbies[buff[2]]
                temp_list[2]=buff[1]
                lobbies[buff[2]]=temp_list
                print(lobbies)
                print(threading.enumerate())
                threads[buff[2]].join()
        elif buff[0]==9:
            for i in clients:
                if clients[i]==conn:
                    del clients[i]
                    break
            conn.close()

print('Server running\n')
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('',9090))
sock.listen(4)
while True:
    conn, addr=sock.accept()
    client=threading.Thread(name='client'+str(len(clients)),target=process_client_sock, args=(conn, addr))
    client.start()

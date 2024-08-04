#remember to pip3 install pygame
from time import sleep,time
from pygame import mixer
from wave import open as wave_open
from winsound import Beep
from datetime import datetime as dt
from json import loads,dump
from ctypes import windll
from easygui import msgbox,ccbox
from os import system
from winreg import CreateKey,QueryInfoKey,HKEY_CURRENT_USER
import urllib.request,urllib.parse
headers={'User-Agent':'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36'}
clock_list=[]#unixtime name contect_id
delete_list=[]
def write_clock_list():
    global clock_list
    try:
        file=open('contest.json','w')
        dump(clock_list,file)
        file.close()
    except:
        pass
def read_clock_list():
    global clock_list
    try:
        file=open('contest.json','r')
        clock_list=loads(file.read())
        file.close()
    except:
        write_clock_list()
read_clock_list()
def play(path):
    try:
        file=wave_open(path,'rb')
        mixer.init(frequency=file.getframerate())
        mixer.Sound(file=path).play()
        file.close()
    except:
        Beep(600,1000)
def get_contest(url):
    try:
        web=urllib.request.urlopen(urllib.request.Request(url,headers=headers))
    except Exception as e:
        print('[error]:',e)
        return
    if web.getcode()==200:
        global clock_list
        web=urllib.parse.unquote(web.read().decode('utf-8')).split('window._feInjection = JSON.parse(decodeURIComponent("')[1].split(';</script>')[0]
        data=loads(web[web.find('{'):web.rfind('}')+1])['currentData']['contests']['result']
        for contest in data:
            if contest['startTime']<time():
                continue
            continue_flag=0
            for have_contest in clock_list:
                if have_contest and have_contest[2]==contest['id']:
                    continue_flag=1
                    break
            if continue_flag:
                continue
            if contest['rated']:
                rated='rated'
            else:
                rated='unrated'
            msgbox(f"检测到洛谷上由 {contest['host']['name']} 举办的 {rated} 比赛 {contest['name']} ，开始时间 {dt.fromtimestamp(contest['startTime'])} ，结束时间 {dt.fromtimestamp(contest['endTime'])} 。\n将自动提醒您参加比赛",title='Luogu Contest Helper',ok_button='确定')
            clock_list.append([contest['startTime'],contest['name'],contest['id']])
        write_clock_list()
    else:
        print('[error]:',url,'return',web.getcode())
get_contest('https://www.luogu.com.cn/contest/list')
while 1:
    if time()%60==0:
        get_contest('https://www.luogu.com.cn/contest/list')
    for i in range(len(clock_list)):
        if clock_list[i][0]<time():
            play('clock.wav')
            if clock_list[0][2]!=-1:
                system('start https://www.luogu.com.cn/contest/'+str(clock_list[0][2]))
            msgbox('比赛 '+clock_list[i][1]+' 已开始',title='Luogu Contest Helper',ok_button='确定')
            delete_list.append(i)
    if delete_list:
        clock_list=[clock_list[i] for i in range(len(clock_list)) if not(i in delete_list)]
        write_clock_list()
        delete_list=[]
    sleep(4)

import pygame
import random
import sys
import os
import random
import time
import pygame_gui
# initialization and define object
pygame.init()
pygame.mixer.init()
run = True
pygame.display.set_caption("計程大富翁")  # caption
player_now = 0
size = (1400, 924)
screen = pygame.display.set_mode(size)
white = (255, 255, 255)
black = (0, 0, 0)

win_color = (0, 255, 255)

dice_number = 0
players = []
point = pygame.image.load("./resource/pic/dice1.png").convert()
point = pygame.transform.scale(point, (50, 50))
main_font = pygame.font.SysFont("mingliu", 25)  # main font

win_font = pygame.font.SysFont("dfkaisb", 200)  # win font
building_icon = pygame.image.load("./resource/pic/building_icon.png").convert()
building_icon = pygame.transform.scale(building_icon, (25, 25))
set_up = False
game_start = False
MapXYvalue = [(861, 861), (756, 861), (672, 861), (588, 861), (504, 861), (420, 861), (336, 861), (252, 861), (168, 861), (63, 861), (63, 756), (63, 672), (63, 588), (63, 504), (63, 420), (63, 336), (63, 256), (63, 168),
              (63, 63), (168, 63), (252, 63), (336, 63), (420, 63), (504, 63), (588, 63), (672, 63), (756, 63), (861, 63), (861, 168), (861, 256), (861, 336), (861, 420), (861, 504), (861, 588), (861, 672), (861, 756)]

pygame.mixer.music.load("./resource/sound/bgm.wav")
rollDiceSound = pygame.mixer.Sound("./resource/sound/dice.wav")
ding=pygame.mixer.Sound("./resource/sound/ding.wav")
win_sound=pygame.mixer.Sound("./resource/sound/win.wav")
pygame.mixer.music.set_volume(0.2)
ding.set_volume(0.5)
pygame.mixer.music.play(-1)

class Player():
    def __init__(self, image, name, isPlayer, position: tuple):
        self.name = name  # 創造角色的名字
        self.money = 10000  # 角色初始金額
        self.movable = True  # 玩家可以移動
        self.move = 0
        self.buyable = False
        self.image = image  # 角色之圖像
        self.isPlayer = isPlayer  # 判斷條件:玩家是玩家
        self.ownedBuildings = []  # 玩家擁有的土地,建一個list
        self.soundPlayList = 0
        self.position = position
        self.ownedHouse = 0
        self.chance_fate = True
        ###
        self.gameable = True
        ###
        # 以機會和命運代替,範例程式碼中的財神、土地神、衰神、破壞神

    def judgePosition(self, buildings):  # 位置判斷 返回值是所在位置的建築

        for each in buildings:  # 對於任一個建築物
            if each.location == self.position:
                return each

    def addahouse(self, isPressYes):
        if isPressYes and self.locatedBuilding.owner == self.name:
            self.money -= self.locatedBuilding.add_House_price
    ###


class Building():              # 好像所有功能都在Player類裏實現了=_=
    def __init__(self, name, price, payment, location, width, height, add_House_price):
        self.name = name  # 土地之名字
        self.price = price  # 土地之價錢
        self.init_price = price
        self.add_House_price = add_House_price
        self.can_buy = True
        self.payment = payment  # 土地之過路費
        self.init_payment = payment
        self.location = location  # 土地之地點
        self.wasBought = False  # 土地是否被購買(初始為沒有)
        self.owner = None  # 土地的擁有者(初始為沒有) #class傳入
        self.height = height
        self.ownedHouse = 0
        self.width = width

    def build_Room(self, building_icon):
        for i in range(self.ownedHouse):
            screen.blit(building_icon, (self.build_x_pos +
                        self.x_direct*25*i, self.build_y_pos+self.y_direct*25*i))


class Button():
    def __init__(self, image, x_pos, y_pos, text_input, clickFunction):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.clickFunction = clickFunction
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.clickFunction()

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


start = Building('起點', 0, 0, MapXYvalue[0], 10.5, 10.5,0)
foundation2 = Building('普通教學館', 500, 100, MapXYvalue[1], 7, 10.5, 250)
foundation3 = Building('新生教學館', 1000, 200, MapXYvalue[2], 7, 10.5, 500)
foundation4 = Building('機會', 0, 0, MapXYvalue[3], 7, 10.5, 0)
foundation5 = Building('共同教學館', 1500, 300, MapXYvalue[4], 7, 10.5,750)
foundation6 = Building('電機一館', 2000, 400, MapXYvalue[5], 7, 10.5, 1000)
foundation7 = Building('新月台', 1500, 300, MapXYvalue[6], 7, 10.5, 750)
foundation8 = Building('命運', 0, 0, MapXYvalue[7], 7, 10.5, 0)
foundation9 = Building('農業陳列館', 1000, 200, MapXYvalue[8], 7, 10.5, 500)
foundation10 = Building('紅綠燈', 0, 0, MapXYvalue[9], 10.5, 10.5, 0)
foundation11 = Building('化學系館', 500, 100, MapXYvalue[10], 10.5, 7, 250)
foundation12 = Building('機會', 0, 0, MapXYvalue[11], 10.5, 7, 0)
foundation13 = Building('思亮館', 1000, 200, MapXYvalue[12], 10.5, 7, 500)
foundation14 = Building('化工系館', 1500, 300, MapXYvalue[13], 10.5, 7, 750)
foundation15 = Building('電機二館', 2000, 400, MapXYvalue[14], 10.5, 7, 1000)
foundation16 = Building('漁業科學館', 1500, 300, MapXYvalue[15], 10.5, 7, 750)
foundation17 = Building('命運', 0, 0, MapXYvalue[16], 10.5, 7, 0)
foundation18 = Building('天文數學館', 1000, 200, MapXYvalue[17], 10.5, 7, 500)
foundation19 = Building('多拉A夢的任意門', 0, 0, MapXYvalue[18], 10.5, 10.5, 0)
foundation20 = Building('土木工程系館', 1000, 200, MapXYvalue[19], 7, 10.5, 500)
foundation21 = Building('機會', 0, 0, MapXYvalue[20], 7, 10.5, 0)
foundation22 = Building('志鴻館', 1500, 300, MapXYvalue[21], 7, 10.5, 750)
foundation23 = Building('明達館', 2000, 400, MapXYvalue[22], 7, 10.5, 1000)
foundation24 = Building('博雅教學館', 1500, 300, MapXYvalue[23], 7, 10.5, 750)
foundation25 = Building('命運', 0, 0, MapXYvalue[24], 7, 10.5, 0)
foundation26 = Building('凝態科學研究中心', 1000, 200, MapXYvalue[25], 7, 10.5, 500)
foundation27 = Building('物學系館', 500, 100, MapXYvalue[26], 7, 10.5, 250)
foundation28 = Building('等待區', 0, 0, MapXYvalue[27], 10.5, 10.5, 0)
foundation29 = Building('計實中心', 500, 100, MapXYvalue[28], 10.5, 7, 250)
foundation30 = Building('機會', 0, 0, MapXYvalue[29], 10.5, 7, 0)
foundation31 = Building('德田館', 1000, 200, MapXYvalue[30], 10.5, 7, 500)
foundation32 = Building('綜合體育館', 1500, 300, MapXYvalue[31], 10.5, 7, 750)
foundation33 = Building('學新館', 2000, 400, MapXYvalue[32], 10.5, 7, 1000)
foundation34 = Building('學術倫理委員會', 1500, 300, MapXYvalue[33], 10.5, 7, 750)
foundation35 = Building('命運', 0, 0, MapXYvalue[34], 10.5, 7, 0)
foundation36 = Building('國發所', 1000, 200, MapXYvalue[35], 10.5, 7, 500)
start.can_buy = False
foundation10.can_buy = False
foundation19.can_buy = False
foundation28.can_buy = False
foundation4.can_buy = False
foundation8.can_buy = False
foundation12.can_buy = False
foundation17.can_buy = False
foundation21.can_buy = False
foundation25.can_buy = False
foundation30.can_buy = False
foundation35.can_buy = False
special_buildings = [start, foundation4, foundation8, foundation10, foundation12, foundation17,
                     foundation19, foundation21, foundation25, foundation28, foundation30, foundation35]

start.infor = "起點\n經過或停留起點\n，+2000"
foundation4.infor = "抽一張機會卡"
foundation8.infor = "抽一張命運卡"
foundation10.infor = f"{foundation10.name}闖紅燈\n或被喇吧嚇到\n移動-6到+6格"
foundation12.infor = "抽一張機會卡"
foundation17.infor = "抽一張命運卡"
foundation19.infor = f"{foundation19.name}\n傳送到任意地方"
foundation21.infor = "抽一張機會卡"
foundation25.infor = "抽一張命運卡"
foundation28.infor = f"{foundation28.name}\n傳送到原點"
foundation30.infor = "抽一張機會卡"
foundation35.infor = "抽一張命運卡"
buildings = [start, foundation2, foundation3, foundation4, foundation5, foundation6, foundation7, foundation8, foundation9, foundation10, foundation11, foundation12, foundation13, foundation14, foundation15, foundation16, foundation17, foundation18, foundation19, foundation20, foundation21, foundation22, foundation23, foundation24, foundation25, foundation26, foundation27, foundation28, foundation29, foundation30, foundation31, foundation32, foundation33, foundation34, foundation35, foundation36
             ]
for i in range(len(buildings)):
    if 0 < i < 9:
        buildings[i].build_x_pos = buildings[i].location[0] - \
            buildings[i].width*6+5
        buildings[i].build_y_pos = buildings[i].location[1] - \
            buildings[i].height*6
        buildings[i].x_direct = 1  # 往右邊
        buildings[i].y_direct = 0  # 下邊沒有
    if 9 < i < 18:
        buildings[i].build_x_pos = buildings[i].location[0] + \
            buildings[i].width*6-23
        buildings[i].build_y_pos = buildings[i].location[1] - \
            buildings[i].height*6
        buildings[i].x_direct = 0
        buildings[i].y_direct = 1
    if 18 < i < 27:
        buildings[i].build_x_pos = buildings[i].location[0] - \
            buildings[i].width*6+5
        buildings[i].build_y_pos = buildings[i].location[1] + \
            buildings[i].height*6-23
        buildings[i].x_direct = 1  # 往右邊
        buildings[i].y_direct = 0  # 往右邊
    if 27 < i <= 35:
        buildings[i].build_x_pos = buildings[i].location[0] - \
            buildings[i].width*6
        buildings[i].build_y_pos = buildings[i].location[1] - \
            buildings[i].height*6+5
        buildings[i].x_direct = 0  # 往右邊
        buildings[i].y_direct = 1  # 往右邊


def turn_over():
    global player_now, game_start
    if game_start == True:
        players[player_now].move = 0
        players[player_now].movable = False
        players[player_now].buyalbe = False
        if player_now >= 3:
            player_now -= 3
        else:
            player_now += 1

        if players[player_now].gameable == False:
            turn_over()
        players[player_now].movable = True
        players[player_now].buyable = False


def chance_fate():
    global players, player_now, buildings, point
    if game_start == True:
        card_number = random.randint(1, 14)
        #card_number = 13

        for each in buildings:
            if each.location == players[player_now].position:
                place_now = each
        if place_now.name == "機會" and players[player_now].buyable == True:
            if card_number == 1:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:Problem set\n錄影被助教選中，加一分，\n去買一箱飲料慶祝:+500")
                players[player_now].money += 500
            elif card_number == 2:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:在小福前擺攤 \n賣點心:+1000")
                players[player_now].money += 1000
            elif card_number == 3:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:瓶中精靈說:每許\n一個願，你最討厭的人會收到\n兩倍的願望。小明說:把我嚇\n個半死。哈哈不好笑:+1000")
                players[player_now].money += 1000
            elif card_number == 4:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:精準的配置藥劑，\n使碘鐘交響曲一次成功:+500")
                players[player_now].money += 500
            elif card_number == 5:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:耳邊突然響起:強\n龍不壓地頭蛇，嚇了一跳，\n但瞬間明白local跟global\n的差異:+500")
                players[player_now].money += 500
            elif card_number == 6:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:作業寫不完，入住\n學新hotel，起床時全身痠痛\n:-500")
                players[player_now].money -= 500
            elif card_number == 7:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:在學新3F閱覽室\n被抓包偷吃東西:-1000")
                players[player_now].money -= 1000
            elif card_number == 8:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:學會動態規劃dp\n，期中破台，然後從睡夢中醒\n來:-500")
                players[player_now].money -= 500
            elif card_number == 9:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:參加全國大專校院\n英語說寫評量檢測，得到獎\n金:+600")
                players[player_now].money += 600
            elif card_number == 10:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:在新生盃大放異彩\n，圈粉無數:+1000")
                players[player_now].money += 1000
            elif card_number == 11:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:交電成績出爐\n，移動至電機二館閱卷\n，幾家歡樂幾家愁")
                players[player_now].position = MapXYvalue[14]
            elif card_number == 12:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:知道台大電機有5棟\n系館嗎?移動至電機一館\n，探索NTUEE最老的系館")
                players[player_now].position = MapXYvalue[5]
            elif card_number == 13:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:微積分課學會三角代換\n，隨機三人的錢互換")
                players[0].money,players[1].money,players[2].money = players[2].money,players[0].money,players[1].money
            elif card_number == 14:
                text_of_card = (
                    f"{players[player_now].name}\n機會效果:微積分課學會三角代換\n，隨機三人的錢互換")
                players[1].money,players[2].money,players[3].money = players[3].money,players[1].money,players[2].money
            players[player_now].buyable = False
            render_multi_line(text_of_card,
                              1000, 300, 25, 600, 500)

        elif place_now.name == "命運" and players[player_now].buyable == True:

            if card_number == 1:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:為了享受系服的\n折價，決定補繳系學會費:-2500")
                players[player_now].money -= 2500
            elif card_number == 2:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:積極參與所有抽獎，\n不斷分享抽獎頁面，\n瘋狂填問卷，\n最後成功重頭獎:+1500")
                players[player_now].money += 1500
            elif card_number == 3:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:正在被窩裡躺著\n，突然想起來要上lab:\n移動至學新館")
                players[player_now].position = MapXYvalue[32]
            elif card_number == 4:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:參加系烤，\n棒式撐了三分鐘以上\n，成功獲得一隻烤雞:+1000")
                players[player_now].money += 1000
            elif card_number == 5:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:先載好25GB\n的Quartus lab，\n拿USB拯救裝不了的人，\n得到大家的感謝:+1500")
                players[player_now].money += 1500
            elif card_number == 6:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:忘記參加晚上\n十點開始的線上測驗，\n心情低落:-500")
                players[player_now].money -= 500
            elif card_number == 7:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:耶誕節交換禮物，\n送出價值500的禮物，\n得到馬克杯*n:-500")
                players[player_now].money -= 500
            elif card_number == 8:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:為了準備考試，\n印了200頁的考古題，\n結果選到彩色列印:-1000")
                players[player_now].money -= 1000
            elif card_number == 9:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:回母校參加校慶，\n被強制要求消費:-500")
                players[player_now].money -= 500
            elif card_number == 10:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:世足壓法國，\n直接大哭:-1500")
                players[player_now].money -= 1500
            elif card_number == 11:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:10點20分從男一醒來\n，群組通知生物要小考:\n移動至明達館")
                players[player_now].position = MapXYvalue[22]
            elif card_number == 12:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:憑藉嫵媚的表演\n，被選為宿營小姐，\n獲得獎金2000元")
                players[player_now].money += 2000

            elif card_number == 13:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:微積分課學會三角代換\n，隨機三人的錢互換")
                players[2].money,players[3].money,players[0].money = players[0].money,players[2].money,players[3].money
            elif card_number == 14:
                text_of_card = (
                    f"{players[player_now].name}\n命運效果:微積分課學會三角代換\n，隨機三人的錢互換")
                players[3].money,players[0].money,players[1].money = players[1].money,players[3].money,players[0].money

            players[player_now].buyable = False
            render_multi_line(text_of_card,
                              1000, 300, 25, 600, 500)


def doraemon():
    door = random.choice([i for i in range(0, 35) if i not in [
                         3, 7, 9, 11, 16, 20, 24, 27, 29, 34]])
    if players[player_now].position == MapXYvalue[18]:
        players[player_now].position = MapXYvalue[door]
        for each in buildings:
            if each.location == players[player_now].position:
                want_to_buy = each
        text = f"{players[player_now].name}\n多拉A夢的任意門效果:\n移到{want_to_buy.name}"
        render_multi_line(text, 1000, 300, 25, 600, 500)


def bathroom():
    if players[player_now].position == MapXYvalue[27] :
        players[player_now].position= MapXYvalue[0] 
        text = f"{players[player_now].name}\n傳送回原點"
        render_multi_line(text, 1000, 300, 25, 600, 500)
       


def Traffic_Light():
    if players[player_now].position == MapXYvalue[9]:
        dice_number = random.choice(
            [i for i in range(-6, 6) if i not in [-2, -6, 0, 2]])

        t_pos = (MapXYvalue.index(
            players[player_now].position)+dice_number) % 36
        players[player_now].position = MapXYvalue[t_pos]
        if dice_number > 0:
            text = f"{players[player_now].name}\n遇到紅綠燈,闖紅燈\n移動{dice_number}格"
        elif dice_number < 0:
            text = f"{players[player_now].name}\n遇到紅綠燈,被喇叭嚇到\n暴退{abs(dice_number)}格"
        render_multi_line(text, 1000, 300, 25, 600, 500)


def dice():
    global players, player_now, buildings, point
    if game_start == True:
        dice_number = random.randint(1, 6)
        if players[player_now].movable == True :
            copy=players[player_now].position
            pygame.mixer.music.pause()
            rollDiceSound.play()
            time.sleep(2)
            pygame.mixer.music.unpause()
            players[player_now].move = dice_number
            players[player_now].movable = False
            if dice_number == 1:
                point = pygame.image.load("./resource/pic/dice1.png").convert()
                point = pygame.transform.scale(point, (50, 50))
            elif dice_number == 2:
                point = pygame.image.load("./resource/pic/dice2.png").convert()
                point = pygame.transform.scale(point, (50, 50))
            elif dice_number == 3:
                point = pygame.image.load("./resource/pic/dice3.png").convert()
                point = pygame.transform.scale(point, (50, 50))
            elif dice_number == 4:
                point = pygame.image.load("./resource/pic/dice4.png").convert()
                point = pygame.transform.scale(point, (50, 50))
            elif dice_number == 5:
                point = pygame.image.load("./resource/pic/dice5.png").convert()
                point = pygame.transform.scale(point, (50, 50))
            elif dice_number == 6:
                point = pygame.image.load("./resource/pic/dice6.png").convert()
                point = pygame.transform.scale(point, (50, 50))
            t_pos = (MapXYvalue.index(
                players[player_now].position)+players[player_now].move) % 36

            players[player_now].position = MapXYvalue[t_pos]
            players[player_now].move = 0
            players[player_now].buyable = True
            now_pos_build = players[player_now].judgePosition(buildings)
            if now_pos_build.owner != players[player_now] and now_pos_build.owner != None:
                players[player_now].money -= now_pos_build.payment
                now_pos_build.owner.money += now_pos_build.payment
                text = f"經過{now_pos_build.owner.name}的地\n{players[player_now].name}付了{now_pos_build.payment}元"
                render_multi_line(text, 1000, 300, 25, 600, 500)
            if MapXYvalue.index(copy)-MapXYvalue.index(players[player_now].position) > 0:
                players[player_now].money += 2000
                text = f"{players[player_now].name}\n經過或停留起點，+2000"
                render_multi_line(text, 1000, 300, 25, 600, 500)


def buy():
    global buildings, players, player_now, building_icon
    if game_start == True:
        for each in buildings:
            if each.location == players[player_now].position:
                want_to_buy = each
        if want_to_buy.wasBought == False and want_to_buy.can_buy == True and players[player_now].buyable == True:
            ding.play()
            want_to_buy.owner = players[player_now]
            players[player_now].money -= want_to_buy.price
            want_to_buy.wasBought = True
            players[player_now].ownedBuildings.append(want_to_buy)
            players[player_now].buyable = False
            text = f"{players[player_now].name}購買了{want_to_buy.name}\n花了{want_to_buy.price}元"
            render_multi_line(text,
                              1000, 300, 25, 600, 500)
        elif want_to_buy.owner == players[player_now] and players[player_now].buyable == True and want_to_buy.ownedHouse < 3:
            ding.play()
            players[player_now].money -= want_to_buy.add_House_price
            players[player_now].buyable = False
            players[player_now].ownedHouse += 1
            want_to_buy.ownedHouse += 1
            want_to_buy.payment = int(want_to_buy.price * (2 * players[player_now].ownedHouse + 1) * 0.2)
            text = f"{players[player_now].name}蓋了一棟房子\n花了{want_to_buy.add_House_price}元"
            render_multi_line(text,
                              1000, 300, 25, 600, 500)
        elif want_to_buy.owner == players[player_now] and players[player_now].buyable == True and want_to_buy.ownedHouse >= 3:
            text = f"房子已經3棟了，不能再買了"
            render_multi_line(text,
                              1000, 300, 25, 600, 500)
        else:
            if want_to_buy.name in ["機會", "命運", "廁所", "左上角", "紅綠燈", "起點"]:
                text = f"無法購買{want_to_buy.name}"
                render_multi_line(text,
                                  1000, 300, 25, 600, 500)
            elif want_to_buy.owner != players[player_now] and want_to_buy.owner != None:
                text = f"無法購買{want_to_buy.name}\n{want_to_buy.owner.name}已經購買"
                render_multi_line(text,
                                  1000, 300, 25, 600, 500)
            elif players[player_now].buyable == False:
                text = "已經買過了喔"
                render_multi_line(text,
                                  1000, 300, 25, 600, 500)


class related_information_about_player():
    def __init__(self, player, x_pos, y_pos):
        self.name = player.name
        self.money = player.money
        self.player = player
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = (f"{self.player.money}\n{self.player.ownedHouse}")

    def update(self):
        self.text_input = (f"{self.player.money}\n{self.player.ownedHouse}")


def render_multi_line(text, x, y, fsize, overlapsize_x, overlapsize_y):
    lines = text.split("\n")
    for i, l in enumerate(lines):
        pygame.draw.rect(screen, (0, 0, 0), (x, y + fsize *
                         i, overlapsize_x, overlapsize_y))
        text_surface = main_font.render(l, True, white)
        screen.blit(text_surface, (x, y + fsize*i))


def render_multi_line_black_font(text, x, y, fsize, overlapsize_x, overlapsize_y):
    lines = text.split("\n")
    for i, l in enumerate(lines):
        pygame.draw.rect(screen, white, (x, y + fsize *
                         i, overlapsize_x, overlapsize_y))
        text_surface = main_font.render(l, True, black)
        screen.blit(text_surface, (x, y + fsize*i))

def check_mouse_position(position):
    global buildings
    for index, object in enumerate(buildings):
        if (object.location[0]-int(object.width*6)) < position[0] < (object.location[0]+int(object.width*6)) and (object.location[1]-int(object.height*6)) < position[1] < (object.location[1]+int(object.height*6)):
            if object not in special_buildings:
                if object.owner == None:
                    render_multi_line_black_font(
                        f"{object.name}\n擁有玩家:{object.owner}\n租金:{object.payment}\n價錢:{object.price}\n有幾間房:{object.ownedHouse}", 150, 430, 30, 200, 60)
                else:
                    render_multi_line_black_font(
                        f"{object.name}\n擁有玩家:{object.owner.name}\n租金:{object.payment}\n價錢:{object.price}\n有幾間房:{object.ownedHouse}", 150, 430, 30, 200, 60)
                break
            else:
                render_multi_line_black_font(
                    object.infor, 150, 430, 30, 200,
                    60)


def win_or_lose():
    global buildings, players, player_now, win_count, game_start, run
    check_list = []
    for player in players:
        if len(player.ownedBuildings) >= 7:
            win_sound.play()
            text = win_font.render(f'{player.name} WIN!!',True, win_color)
            screen.blit(text, (200, 300))
            pygame.display.update()
            time.sleep(3)
            game_start = False
            run = False
        elif player.money >= 20000:
            win_sound.play()
            text = win_font.render(f"{player.name} WIN!!", True, win_color)
            screen.blit(text, (200, 300))
            pygame.display.update()
            time.sleep(3)
            game_start = False
            run = False
        elif player.ownedHouse >= 5:
            win_sound.play()
            text = win_font.render(f"{player.name} WIN!!", True, win_color)
            screen.blit(text, (200, 300))
            pygame.display.update()
            time.sleep(3)
            game_start = False
            run = False
        check_list.append(player.gameable)
    if check_list.count(True) == 1:
        index = check_list.index(True)
        text = win_font.render(f"{players[index].name} WIN!!", True, win_color)
        screen.blit(text, (200, 300))
        game_start = False
        run = True
###


def main():
    global players, game_start, dice_number, buildings, player_now,set_up
    background = pygame.image.load('./resource/pic/new_map.png').convert()
    background = pygame.transform.scale(background, (924, 924))  # 924/77 =12
    background.set_colorkey(black)
    clock = pygame.time.Clock()
    chess1 = pygame.image.load("./resource/pic/chess1.png").convert()
    chess1 = pygame.transform.scale(chess1, (43, 43))
    chess2 = pygame.image.load("./resource/pic/chess2.png").convert()
    chess2 = pygame.transform.scale(chess2, (43, 43))
    chess3 = pygame.image.load("./resource/pic/chess3.png").convert()
    chess3 = pygame.transform.scale(chess3, (43, 43))
    chess4 = pygame.image.load("./resource/pic/chess4.png").convert()
    chess4 = pygame.transform.scale(chess4, (43, 43))
    chess1.set_colorkey(black)
    chess2.set_colorkey(black)
    chess3.set_colorkey(black)
    chess4.set_colorkey(black)
    button_surface = pygame.image.load("./resource/pic/button.png")
    button_surface = pygame.transform.scale(button_surface, (130, 70))
    building_icon = pygame.image.load(
        "./resource/pic/building_icon.png").convert()
    building_icon = pygame.transform.scale(building_icon, (25, 25))
    chess1_image = pygame.image.load("./resource/pic/StatusBar1.png").convert()
    chess1_image = pygame.transform.scale(chess1_image, (200, 125))
    chess2_image = pygame.image.load("./resource/pic/StatusBar2.png").convert()
    chess2_image = pygame.transform.scale(chess2_image, (200, 125))
    chess3_image = pygame.image.load("./resource/pic/StatusBar3.png").convert()
    chess3_image = pygame.transform.scale(chess3_image, (200, 125))
    chess4_image = pygame.image.load("./resource/pic/StatusBar4.png").convert()
    chess4_image = pygame.transform.scale(chess4_image, (200, 125))
    chess1_image_glow = pygame.image.load(
        "./resource/pic/StatusBar1_glow.png").convert()
    chess2_image_glow = pygame.image.load(
        "./resource/pic/StatusBar2_glow.png").convert()
    chess3_image_glow = pygame.image.load(
        "./resource/pic/StatusBar3_glow.png").convert()
    chess4_image_glow = pygame.image.load(
        "./resource/pic/StatusBar4_glow.png").convert()
    chess1_image_glow = pygame.transform.scale(chess1_image_glow, (200, 125))
    chess2_image_glow = pygame.transform.scale(chess2_image_glow, (200, 125))
    chess3_image_glow = pygame.transform.scale(chess3_image_glow, (200, 125))
    chess4_image_glow = pygame.transform.scale(chess4_image_glow, (200, 125))
    player_1 = Player(chess1, 'player1', True, MapXYvalue[0])
    player_2 = Player(chess2, 'player2', True, MapXYvalue[0])
    player_3 = Player(chess3, 'player3', True, MapXYvalue[0])
    player_4 = Player(chess4, 'player4', True, MapXYvalue[0])
    players.append(player_1)
    players.append(player_2)
    players.append(player_3)
    players.append(player_4)
    information1 = related_information_about_player(player_1, 1070, 110)
    information2 = related_information_about_player(player_2, 1270, 110)
    information3 = related_information_about_player(player_3, 1070, 710)
    information4 = related_information_about_player(player_4, 1270, 710)
    game_start = True
    Dice_button = Button(button_surface, 650, 200, "擲骰子", dice)
    overTurn_button = Button(button_surface, 650, 300, "結束回合", turn_over)
    buy_button = Button(button_surface, 650, 400, "購買/蓋房", buy)
    rect1 = pygame.Rect(0,0,924,924)
    rect2 = pygame.Rect(350,175,100,50)
    player_number_setup =False
    player_infor = []
    count =0
    current_count =0
    manager = pygame_gui.UIManager(size)
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (400, 50)), 
                                        manager=manager,object_id='#count_number')
    text = "輸入玩家數量"
    player_1_input_text = False
    player_2_input_text = False
    player_3_input_text = False
    player_4_input_text = False

    render_multi_line(text,100,280,25,100,50)       
    while set_up == False and player_number_setup == False:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#count_number" ):
                    if len(event.text) == 1:
                        if event.text.isdigit():
                            if 1<=int(event.text)<=4:
                                count=int(event.text)
                                player_number_setup = True
                            else:
                                pygame.draw.rect(screen,black,rect2)
                                text ="輸入1到4的數字"
                                render_multi_line(text, 350, 175, 25, 100,50)
                        else:
                            pygame.draw.rect(screen,black,rect2)
                            text ="輸入1到4的數字"
                            render_multi_line(text, 350, 175, 25, 100,50)
                    else:
                        pygame.draw.rect(screen,black,rect2)
                        text ="輸入1到4的數字"
                        render_multi_line(text, 350, 175, 25, 100,50)
            manager.process_events(event)   
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(screen)
        pygame.display.update()
    if count ==4:
        text_input1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 325), (400, 50)), 
                                        manager=manager,object_id='#player1')
        text = "輸入玩家1姓名"
        render_multi_line(text,100,330,25,100,50)     
        text_input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 375), (400, 50)), 
                                        manager=manager,object_id='#player2')
        text = "輸入玩家2姓名"
        render_multi_line(text,100,380,25,100,50)    
        text_input3 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 425), (400, 50)), 
                                        manager=manager,object_id='#player3')
        text = "輸入玩家3姓名"
        render_multi_line(text,100,430,25,100,50)     
        text_input4 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 475), (400, 50)), 
                                        manager=manager,object_id='#player4')
        text = "輸入玩家4姓名"
        render_multi_line(text,100,480,25,100,50)   
    if count ==3:
        text_input1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 325), (400, 50)), 
                                        manager=manager,object_id='#player1')
        text = "輸入玩家1姓名"
        render_multi_line(text,100,330,25,100,50)    
        text_input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 375), (400, 50)), 
                                        manager=manager,object_id='#player2')
        text = "輸入玩家2姓名"
        render_multi_line(text,100,380,25,100,50)     
        text_input3 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 425), (400, 50)), 
                                        manager=manager,object_id='#player3')
        text = "輸入玩家3姓名"
        render_multi_line(text,100,430,25,100,50)   
    if count ==2:
        text_input1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 325), (400, 50)), 
                                        manager=manager,object_id='#player1')
        text = "輸入玩家1姓名"
        render_multi_line(text,100,330,25,100,50)    
        text_input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 375), (400, 50)), 
                                        manager=manager,object_id='#player2')
        text = "輸入玩家2姓名"
        render_multi_line(text,100,380,25,100,50)   
    if count == 1:
        text_input1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 325), (400, 50)), 
                                        manager=manager,object_id='#player1')
        text = "輸入玩家1姓名"
        render_multi_line(text,100,330,25,100,50)    
    
    while set_up ==False and player_number_setup ==True and (current_count < count):
        UI_REFRESH_RATE = clock.tick(60)/1000  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#player1' and player_1_input_text == False):
                    text=event.text
                    player_infor.append(text)
                    player_1_input_text = True
                    current_count +=1
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#player2' and player_2_input_text == False):
                    text=event.text
                    player_infor.append(text)
                    player_2_input_text = True
                    current_count +=1
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#player3' and player_3_input_text == False):
                    text=event.text
                    player_infor.append(text)
                    player_3_input_text = True
                    current_count +=1
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#player4' and player_4_input_text == False):
                    text=event.text
                    player_infor.append(text)
                    player_4_input_text = True
                    current_count +=1
            manager.process_events(event)   
        if count == current_count:
            set_up =True
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(screen)
        pygame.display.update()
    for j in range(count):
        players[j].name = player_infor[j]
    for k in range(count,4):
        players[k].name = f"電腦{k-count+1}"
        players[k].isPlayer = False
    while run and set_up:
        pygame.draw.rect(screen,black,rect1)
        
        screen.blit(background, [0,0])
        if players[player_now].isPlayer == False:
            dice()
            chance_fate()
            time.sleep(0.2)
            win_or_lose()
            doraemon()
            bathroom()
            Traffic_Light()
            if MapXYvalue.index(players[player_now].position) not in [0,3,7,9,11,16,18,20,24,27,29,34]:
                buy()
            turn_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # check button
                overTurn_button.checkForInput(pygame.mouse.get_pos())
                Dice_button.checkForInput(pygame.mouse.get_pos())
                buy_button.checkForInput(pygame.mouse.get_pos())
        for i in range(len(players)):  # 畫人物的地方
            if i == 0:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay0 = [now_pos_build.location[0]-now_pos_build.width *
                                  6, now_pos_build.location[1]-now_pos_build.height*6]
                screen.blit(players[i].image, where_to_stay0)
            elif i == 1:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay1 = [now_pos_build.location[0],
                                  now_pos_build.location[1]-now_pos_build.height*6]
                screen.blit(players[i].image, where_to_stay1)
            elif i == 2:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay2 = [now_pos_build.location[0] -
                                  now_pos_build.width*6, now_pos_build.location[1]]
                screen.blit(players[i].image, where_to_stay2)
            elif i == 3:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay3 = [now_pos_build.location[0],
                                  now_pos_build.location[1]]
                screen.blit(players[i].image, where_to_stay3)

            if players[i].money <= 0 and players[i].gameable == True:
                players[i].gameable = False
                players[i].money = 0
                for j in buildings:
                    if j.owner == players[i]:
                        j.owner = None
                        j.ownedHouse = 0
                        j.price = j.init_price
                        j.payment = j.init_payment
        check_mouse_position(pygame.mouse.get_pos())

        Dice_button.changeColor(pygame.mouse.get_pos())
        overTurn_button.changeColor(pygame.mouse.get_pos())
        buy_button.changeColor(pygame.mouse.get_pos())
        information1.update()
        information2.update()
        information3.update()
        information4.update()

        text1 = main_font.render(players[0].name, True, white)
        text2 = main_font.render(players[1].name, True, white)
        text3 = main_font.render(players[2].name, True, white)
        text4 = main_font.render(players[3].name, True, white)
        if player_now == 0:
            screen.blit(chess1_image_glow, (940, 40))
            screen.blit(text1, (1025, 58))
            screen.blit(chess2_image, (1140, 40))
            screen.blit(text2, (1225, 58))
            screen.blit(chess3_image, (940, 640))
            screen.blit(text3, (1025, 658))
            screen.blit(chess4_image, (1140, 640))
            screen.blit(text4, (1225, 658))
        elif player_now == 1:
            screen.blit(chess1_image, (940, 40))
            screen.blit(text1, (1025, 58))
            screen.blit(chess2_image_glow, (1140, 40))
            screen.blit(text2, (1225, 58))
            screen.blit(chess3_image, (940, 640))
            screen.blit(text3, (1025, 658))
            screen.blit(chess4_image, (1140, 640))
            screen.blit(text4, (1225, 658))
        elif player_now == 2:
            screen.blit(chess1_image, (940, 40))
            screen.blit(text1, (1025, 58))
            screen.blit(chess2_image, (1140, 40))
            screen.blit(text2, (1225, 58))
            screen.blit(chess3_image_glow, (940, 640))
            screen.blit(text3, (1025, 658))
            screen.blit(chess4_image, (1140, 640))
            screen.blit(text4, (1225, 658))
        elif player_now == 3:
            screen.blit(chess1_image, (940, 40))
            screen.blit(text1, (1025, 58))
            screen.blit(chess2_image, (1140, 40))
            screen.blit(text2, (1225, 58))
            screen.blit(chess3_image, (940, 640))
            screen.blit(text3, (1025, 658))
            screen.blit(chess4_image_glow, (1140, 640))
            screen.blit(text4, (1225, 658))
        render_multi_line(information1.text_input,
                          information1.x_pos, information1.y_pos, 30, 40, 30)
        render_multi_line(information2.text_input,
                          information2.x_pos, information2.y_pos, 30, 40, 30)
        render_multi_line(information3.text_input,
                          information3.x_pos, information3.y_pos, 30, 40, 30)
        render_multi_line(information4.text_input,
                          information4.x_pos, information4.y_pos, 30, 40, 30)
        screen.blit(point, (428, 462))
       
        for i in buildings:
            i.build_Room(building_icon)
        chance_fate()
        win_or_lose()
        ###修改處
        doraemon()
        bathroom()
        Traffic_Light()
        ###
        check_mouse_position(pygame.mouse.get_pos())
        Dice_button.update()
        overTurn_button.update()
        buy_button.update()
      
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

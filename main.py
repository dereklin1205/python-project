import pygame
import random
import sys
import os
import random
import time
# initialization and define object
pygame.init()
run = True
pygame.display.set_caption("計程大富翁 - made by 王渤穎")  # caption
player_now = 0
size = (1400, 924)
screen = pygame.display.set_mode(size)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
dice_number = 0
players = []
point = pygame.image.load("./resource/pic/dice1.png").convert()
point = pygame.transform.scale(point, (50, 50))
main_font = pygame.font.SysFont("dfkaisb", 25)  # main font
game_start = False
MapXYvalue = [(861, 861), (756, 861), (672, 861), (588, 861), (504, 861), (420, 861), (336, 861), (252, 861), (168, 861), (63, 861), (63, 756), (63, 672), (63, 588), (63, 504), (63, 420), (63, 336), (63, 256), (63, 168),
              (63, 63), (168, 63), (252, 63), (336, 63), (420, 63), (504, 63), (588, 63), (672, 63), (756, 63), (861, 63), (861, 168), (861, 256), (861, 336), (861, 420), (861, 504), (861, 588), (861, 672), (861, 756)]


class Player():
    def __init__(self, image, name, isPlayer, position: tuple):
        self.name = name  # 創造角色的名字
        self.money = 10000  # 角色初始金額
        self.isGoingToMove = False  # 玩家正在移動??
        self.movable = True  # 玩家可以移動
        self.move = 0
        self.buyable = False
        self.image = image  # 角色之圖像
        self.locatedBuilding = 0  # 玩家所在之建築,初始值為0
        self.isPlayer = isPlayer  # 判斷條件:玩家是玩家
        self.ownedBuildings = []  # 玩家擁有的土地,建一個list
        self.soundPlayList = 0
        self.position = position
        # 以機會和命運代替,範例程式碼中的財神、土地神、衰神、破壞神

    def judgePosition(self, buildings):  # 位置判斷 返回值是所在位置的建築
        for each in buildings:  # 對於任一個建築物
            if each.location == self.position:
                return each

    def buyaBuilding(self, isPressYes):  # 購買方法
        if isPressYes and self.locatedBuilding.owner != self.name:  # 點擊YES鍵且此地沒有其他人購買
            self.locatedBuilding.owner = self.name  # 這塊地變購買者的
            self.locatedBuilding.wasBought = True  # 這塊地是建築(機會、命運、四角除外)
            self.ownedBuildings.append(
                self.locatedBuilding)  # 角色擁有的土地清單中,多了這塊地
            self.money -= self.locatedBuilding.price  # 角色的錢=原本--土地的售價
            self.showText = [self.name + '購買了' +
                             self.locatedBuilding.name + '!']  # 顯示文字:角色購買這塊土地
            self.soundPlayList = 1  # 背景音樂第1首
            return True  # 回傳正確
        else:
            return False  # 購買失敗
class Building():              # 好像所有功能都在Player類裏實現了=_=
    def __init__(self, name, price, payment, location, width, height):
        self.name = name  # 土地之名字
        self.price = price  # 土地之價錢
        self.can_buy = True
        self.payment = payment  # 土地之過路費
        self.location = location  # 土地之地點
        self.wasBought = False  # 土地是否被購買(初始為沒有)
        self.builtRoom = 0  # 小房子建造的數目(初始為沒有)
        self.owner = None  # 土地的擁有者(初始為沒有)
        self.height = height
        self.ownedHouse=0
        self.width = width


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


start = Building('起點', 0, 0, MapXYvalue[0], 10.5, 10.5)
foundation2 = Building('普通教學館', 1000, 200, MapXYvalue[1], 7, 10.5)
foundation3 = Building('新生教學館', 1000, 200, MapXYvalue[2], 7, 10.5)
foundation4 = Building('機會', 0, 0, MapXYvalue[3], 7, 10.5)
foundation5 = Building('共同教學館', 1000, 200, MapXYvalue[4], 7, 10.5)
foundation6 = Building('電機一館', 1000, 200, MapXYvalue[5], 7, 10.5)
foundation7 = Building('新月台', 1000, 200, MapXYvalue[6], 7, 10.5)
foundation8 = Building('命運', 0, 0, MapXYvalue[7], 7, 10.5)
foundation9 = Building('農業陳列館', 1000, 200, MapXYvalue[8], 7, 10.5)
foundation10 = Building('廁所', 0, 0, MapXYvalue[9], 10.5, 10.5)
foundation11 = Building('化學系館', 1000, 200, MapXYvalue[10], 10.5, 7)
foundation12 = Building('機會', 0, 0, MapXYvalue[11], 10.5, 7)
foundation13 = Building('思亮館', 1000, 200, MapXYvalue[12], 10.5, 7)
foundation14 = Building('化工系館', 1000, 200, MapXYvalue[13], 10.5, 7)
foundation15 = Building('電機二館', 1000, 200, MapXYvalue[14], 10.5, 7)
foundation16 = Building('漁業科學館', 1000, 200, MapXYvalue[15], 10.5, 7)
foundation17 = Building('命運', 0, 0, MapXYvalue[16], 10.5, 7)
foundation18 = Building('天文數學館', 1000, 200, MapXYvalue[17], 10.5, 7)
foundation19 = Building('左上角', 0, 0, MapXYvalue[18], 10.5, 10.5)
foundation20 = Building('土木工程系館', 1000, 200, MapXYvalue[19], 7, 10.5)
foundation21 = Building('機會', 0, 0, MapXYvalue[20], 7, 10.5)
foundation22 = Building('志鴻館', 1000, 200, MapXYvalue[21], 7, 10.5)
foundation23 = Building('明達館', 1000, 200, MapXYvalue[22], 7, 10.5)
foundation24 = Building('博雅教學館', 1000, 200, MapXYvalue[23], 7, 10.5)
foundation25 = Building('命運', 0, 0, MapXYvalue[24], 7, 10.5)
foundation26 = Building('凝態科學研究中心', 1000, 200, MapXYvalue[25], 7, 10.5)
foundation27 = Building('物學系館', 1000, 200, MapXYvalue[26], 7, 10.5)
foundation28 = Building('紅綠燈', 0, 0, MapXYvalue[27], 10.5, 10.5)
foundation29 = Building('計實中心', 1000, 200, MapXYvalue[28], 10.5, 7)
foundation30 = Building('機會', 0, 0, MapXYvalue[29], 10.5, 7)
foundation31 = Building('德田館', 1000, 200, MapXYvalue[30], 10.5, 7)
foundation32 = Building('綜合體育館', 1000, 200, MapXYvalue[31], 10.5, 7)
foundation33 = Building('學新館', 1000, 200, MapXYvalue[32], 10.5, 7)
foundation34 = Building('學術倫理委員會', 1000, 200, MapXYvalue[33], 10.5, 7)
foundation35 = Building('命運', 0, 0, MapXYvalue[34], 10.5, 7)
foundation36 = Building('國發所', 1000, 200, MapXYvalue[35], 10.5, 7)
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
special_buildings=[start,foundation4,foundation8,foundation10,foundation12,foundation17,foundation19,foundation21,foundation25,foundation28,foundation30,foundation35]
start.infor = ""
foundation4.infor = "抽一張機會卡"
foundation8.infor = "抽一張命運卡"
foundation10.infor = f"{foundation10.name}\n我還不知道"
foundation12.infor = "抽一張機會卡"
foundation17.infor = "抽一張命運卡"
foundation19.infor = f"{foundation19.name}\n我還是不知道"
foundation21.infor = "抽一張機會卡"
foundation25.infor = "抽一張命運卡"
foundation28.infor = f"{foundation28.name}\n紅綠燈"
foundation30.infor = "抽一張機會卡"
foundation35.infor = "抽一張命運卡"
buildings = [start, foundation2, foundation3, foundation4, foundation5, foundation6, foundation7, foundation8, foundation9, foundation10, foundation11, foundation12, foundation13, foundation14, foundation15, foundation16, foundation17, foundation18, foundation19, foundation20, foundation21, foundation22, foundation23, foundation24, foundation25, foundation26, foundation27, foundation28, foundation29, foundation30, foundation31, foundation32, foundation33, foundation34, foundation35, foundation36
             ]


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
        players[player_now].movable = True
        players[player_now].buyable = False


def dice():
    global players, player_now, buildings,point
    if game_start == True:
        dice_number = random.randint(1, 6)

        if players[player_now].movable == True:
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


def buy():
    global buildings, players, player_now
    for each in buildings:
        if each.location == players[player_now].position:
            want_to_buy = each
    if want_to_buy.wasBought == False and want_to_buy.can_buy == True and players[player_now].buyable == True:
        want_to_buy.owner = players[player_now]
        players[player_now].money -= want_to_buy.price
        want_to_buy.wasBought = True
        players[player_now].buyable = False
    elif want_to_buy.owner == players[player_now].name and players[player_now].buyable == True:
        want_to_buy.buildRoom += 1
        players[player_now].money -= 700
        players[player_now].buyable = False
        players[player_now].ownedHouse+=1
    else:
        print(f"{players[player_now].name} Can't buy {want_to_buy.name}")


button_surface = pygame.image.load("./resource/pic/button.png")
button_surface = pygame.transform.scale(button_surface, (130, 70))

Dice_button = Button(button_surface, 650, 200, "Dice", dice)
overTurn_button = Button(button_surface, 650, 300, "TurnOver", turn_over)
buy_button = Button(button_surface, 650, 400, "Buy it", buy)

class related_information_about_player():
    def __init__(self, player, x_pos, y_pos):
        self.name = player.name
        self.money = player.money
        self.player = player
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = (f"name: {self.name}\nmoney: {self.player.money}")

    def update(self):
        self.text_input = (f"name: {self.name}\nmoney: {self.player.money}")


def render_multi_line(text, x, y, fsize,overlapsize_x,overlapsize_y):
    lines = text.split("\n")
    for i, l in enumerate(lines):
        pygame.draw.rect(screen, (0, 0, 0), (x, y + fsize*i, overlapsize_x, overlapsize_y))
        text_surface = main_font.render(l,True,white)
        screen.blit(text_surface, (x, y + fsize*i))

def check_mouse_position(position):
    global buildings
    for index, object in enumerate(buildings):
        if (object.location[0]-int(object.width*6)) < position[0] < (object.location[0]+int(object.width*6)) and (object.location[1]-int(object.height*6)) < position[1] < (object.location[1]+int(object.height*6)):
            if object not in special_buildings:
                if object.owner ==None:
                    render_multi_line(f"{object.name}\nowner:{object.owner}\npayment:{object.payment}\nprice:{object.price}\n有幾間房:{object.ownedHouse}",200,500,25,200,170)
                else:
                    render_multi_line(f"{object.name}\nowner:{object.owner.name}\npayment:{object.payment}\nprice:{object.price}\n有幾間房:{object.ownedHouse}",200,500,25,200,170)
                break
            else:
                render_multi_line(object.infor,200,500,25,200,200)
def win_or_lose():
    global buildings, players, player_now, win_count,game_start,run
    for player in players:
        if len(player.ownedBuildings)>=7 :
            print(f'{player.name} WIN!!')
            game_start = False
            run=False
        elif player.money>=20000 :
            print(f'{player.name} WIN!!')
            game_start = False
            run=False
        elif len(player.ownedHouse)>=5 :
            print(f'{player.name} WIN!!')
            game_start = False
            run=False 
###
def main():
    global players, game_start, dice_number, buildings, player_now
    background = pygame.image.load('./resource/pic/Game_Map.png').convert()
    background = pygame.transform.scale(background, (924, 924))  # 924/77 =12
    clock = pygame.time.Clock()
    chess1 = pygame.image.load("./resource/pic/chess1.png").convert()
    chess1 = pygame.transform.scale(chess1, (50, 50))
    chess2 = pygame.image.load("./resource/pic/chess2.png").convert()
    chess2 = pygame.transform.scale(chess2, (50, 50))
    chess3 = pygame.image.load("./resource/pic/chess3.png").convert()
    chess3 = pygame.transform.scale(chess3, (50, 50))
    chess4 = pygame.image.load("./resource/pic/chess4.png").convert()
    chess4 = pygame.transform.scale(chess4, (50, 50))
    player_1 = Player(chess1, 'player1', True, MapXYvalue[0])
    player_2 = Player(chess2, 'player2', True, MapXYvalue[0])
    player_3 = Player(chess3, 'player3', True, MapXYvalue[0])
    player_4 = Player(chess4, 'player4', True, MapXYvalue[0])
    players.append(player_1)
    players.append(player_2)
    players.append(player_3)
    players.append(player_4)
    information1 = related_information_about_player(player_1, 950, 100)
    information2 = related_information_about_player(player_2, 1130, 100)
    information3 = related_information_about_player(player_3, 950, 600)
    information4 = related_information_about_player(player_4, 1130, 600)

    while run:
        game_start = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # check button
                overTurn_button.checkForInput(pygame.mouse.get_pos())
                Dice_button.checkForInput(pygame.mouse.get_pos())
                buy_button.checkForInput(pygame.mouse.get_pos())
        screen.blit(background, [0, 0])
        for i in range(len(players)):  # 畫人物的地方
            if i == 0:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay0 = [now_pos_build.location[0]-now_pos_build.width *
                                  6, now_pos_build.location[1]-now_pos_build.height*6]
                screen.blit(players[i].image, where_to_stay0)
            if i == 1:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay1 = [now_pos_build.location[0],
                                  now_pos_build.location[1]-now_pos_build.height*6]
                screen.blit(players[i].image, where_to_stay1)
            if i == 2:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay2 = [now_pos_build.location[0] -
                                  now_pos_build.width*6, now_pos_build.location[1]]
                screen.blit(players[i].image, where_to_stay2)
            if i == 3:
                now_pos_build = players[i].judgePosition(buildings)
                where_to_stay3 = [now_pos_build.location[0],
                                  now_pos_build.location[1]]
                screen.blit(players[i].image, where_to_stay3)
        check_mouse_position(pygame.mouse.get_pos())
        Dice_button.changeColor(pygame.mouse.get_pos())
        overTurn_button.changeColor(pygame.mouse.get_pos())
        buy_button.changeColor(pygame.mouse.get_pos())
        information1.update()
        information2.update()
        information3.update()
        information4.update()
        render_multi_line(information1.text_input,
                          information1.x_pos, information1.y_pos, 25,160,160)
        render_multi_line(information2.text_input,
                          information2.x_pos, information2.y_pos, 25,160,160)
        render_multi_line(information3.text_input,
                          information3.x_pos, information3.y_pos, 25,160,160)
        render_multi_line(information4.text_input,
                          information4.x_pos, information4.y_pos, 25,160,160)
        screen.blit(point,(462,462))
        Dice_button.update()
        overTurn_button.update()
        buy_button.update()
        pygame.display.update()


if __name__ == "__main__":
    main()

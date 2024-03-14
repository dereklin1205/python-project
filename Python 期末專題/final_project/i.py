import pygame, sys,os
from buttonss import Button

pygame.init()
black = (0,0,0)
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("./resource/pic/ntu_big_gate.jpg")
BG = pygame.transform.scale(BG, (1280, 720))
pygame.mixer.init()
pygame.mixer.music.load("./resource/sound/bgm.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
chess1 = pygame.image.load("./resource/pic/button.png").convert()
chess1 = pygame.transform.scale(chess1, (100, 43))
chess2 = pygame.image.load("./resource/pic/button.png").convert()
chess2 = pygame.transform.scale(chess2, (100, 43))
chess3 = pygame.image.load("./resource/pic/button.png").convert()
chess3 = pygame.transform.scale(chess3, (100, 43))
chess1.set_colorkey(black)
chess2.set_colorkey(black)
chess3.set_colorkey(black)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("mingliu", 25)

def play():
    pygame.mixer.init()
    pygame.mixer.music.stop()
    current = os.getcwd()
    target_py = os.path.join(current, "ntu_monopoly.py")
    os.system("python " + target_py)

    #os.system("python ./resource/ttt.py")
    pygame.quit()
    sys.exit()

    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT1 = get_font(45).render("遊戲規則:初始金額10000元", True, "White")
        OPTIONS_TEXT2 = get_font(45).render("玩法:1.停在無人之系館,選擇是否購買", True, "White")
        OPTIONS_TEXT3 = get_font(45).render("2.停在他人之系館,支付過路費", True, "White")
        OPTIONS_TEXT4 = get_font(45).render("3.停在自己之系館,選擇是否捐一棟系館", True, "White")
        OPTIONS_TEXT5 = get_font(45).render("勝利條件:1.擁有1/5的系館", True, "White")
        OPTIONS_TEXT6 = get_font(45).render("2.賺到20000元3.擁有5棟房子", True, "White")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(860, 160))
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(860, 200))
        OPTIONS_RECT3 = OPTIONS_TEXT3.get_rect(center=(860, 240))
        OPTIONS_RECT4 = OPTIONS_TEXT4.get_rect(center=(860, 280))
        OPTIONS_RECT5 = OPTIONS_TEXT5.get_rect(center=(860, 320))
        OPTIONS_RECT6 = OPTIONS_TEXT6.get_rect(center=(860, 360))
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        SCREEN.blit(OPTIONS_TEXT3, OPTIONS_RECT3)
        SCREEN.blit(OPTIONS_TEXT4, OPTIONS_RECT4)
        SCREEN.blit(OPTIONS_TEXT5, OPTIONS_RECT5)
        SCREEN.blit(OPTIONS_TEXT6, OPTIONS_RECT6)
        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "Black")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 70))

        PLAY_BUTTON = Button(image=chess1, pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
        OPTIONS_BUTTON = Button(image=chess2, pos=(640, 400), 
                            text_input="RULE", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
        QUIT_BUTTON = Button(image=chess3, pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
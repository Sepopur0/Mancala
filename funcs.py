import data
from agents import *


def start_screen(screen):  # 0 for p1 vs p2; 1 for p1 vs bot
    screen.fill(scenery)
    bg_img = pygame.image.load('download.jpeg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    screen.blit(bg_img, (0, 0))
    text = font_title.render("Ô ăn quan", False, boxcontent)
    tet_coor = text.get_rect(center=(650, 200))
    screen.blit(text, tet_coor)
    drawbutton(screen, "PvP", 575, 300)
    drawbutton(screen, "PvE", 575, 375)
    drawbutton(screen, "EvE", 575, 450)
    drawbutton(screen, "Thoát", 575, 525)
    pygame.display.update()
    act = -1
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                act = checkbox(mousepos, startbutton_coor, 150, 40)
                if act != -1:
                    screen.blit(s_1, (575, 300+75*act))
                    pygame.display.update()
            elif ev.type == pygame.MOUSEBUTTONUP:
                if act>-1 and act <= 2:
                    return 2-act
                elif act == 3:
                    sys.exit()
            elif ev.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


def options(screen, opt):  # 0 for p1 first, 1 for p2/bot first; if play w/ bot: return num as lv, -1 if play w/ human
    screen.fill(rock_1)
    bg_img = pygame.image.load('download.jpeg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    bg_img.set_alpha(40)
    screen.blit(bg_img, (0, 0))
    str1=font.render("Thứ tự", False, boxcontent)
    str1_rect=str1.get_rect(center=(450,485))
    screen.blit(str1,str1_rect)
    option = ""
    coor = []
    if opt == 2:
        drawbutton(screen, "P1 trước", 375, 500)
        option = "P2 trước"
        coor = option_coor_0
    elif opt == 1:
        drawbutton(screen, "Người trước", 375, 500)
        option = "Máy trước"
        coor = option_coor_1
        str2=font.render("Độ khó", False, boxcontent)
        str2_rect=str2.get_rect(center=(650,485))
        screen.blit(str2,str2_rect)
        drawbutton(screen, "Dễ", 575, 500)
    else:
        drawbutton(screen, "Máy 1 trước", 375, 500)
        option = "Máy 2 trước"
        coor = option_coor_2
        str2=font.render("Giải thuật máy 1", False, boxcontent)
        str2_rect=str2.get_rect(center=(650,485))
        str3=font.render("Giải thuật máy 2", False, boxcontent)
        str3_rect=str3.get_rect(center=(650,560))
        screen.blit(str2,str2_rect)
        screen.blit(str3,str3_rect)
        drawbutton(screen, "Random", 575, 500)
        drawbutton(screen, "Random", 575, 575)
    draw_grid(screen)
    drawbutton(screen, "Xác nhận", 775, 500)
    drawbutton(screen, "Trang chính", 775, 575)
    pygame.display.update()
    act = -1
    botdif1 = 0
    botdif2 = 0
    whofirst = 0
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                act = checkbox(mousepos, coor, 150, 40)
                if act != -1:
                    screen.blit(s_1, (coor[act][0], coor[act][1]))
                    pygame.display.update()
            elif ev.type == pygame.MOUSEBUTTONUP:
                if act == 0:
                    whofirst = (whofirst+1) % 2
                    if whofirst == 0:
                        if opt ==2:
                            drawbutton(screen, "P1 trước", 375, 500)
                        elif opt==1:
                            drawbutton(screen, "Người trước", 375, 500)
                        else:
                            drawbutton(screen, "Máy 1 trước", 375, 500)
                    elif whofirst == 1:
                        drawbutton(screen, option, 375, 500)
                elif opt == 1:
                    if act == 1:
                        botdif1 = (botdif1+1) % 4
                        if botdif1 == 0:
                            drawbutton(screen, "Dễ", 575, 500)
                        elif botdif1 == 1:
                            drawbutton(screen, "Vừa", 575, 500)
                        elif botdif1 == 2:
                            drawbutton(screen, "Khó", 575, 500)
                        elif botdif1==3:
                            drawbutton(screen, "Q-Learning", 575, 500)
                    elif act == 2:
                        return [whofirst, -1, botdif1]
                    elif act == 3:
                        return [whofirst, -2, -1]
                elif opt == 2:
                    if act == 1:
                        return [whofirst, -1, -1]
                    elif act == 2:
                        return [whofirst, -2, -1]
                elif opt == 0:
                    if act == 1:
                        botdif1 = (botdif1+1) % 8
                        drawbutton(screen, agentslist[botdif1], 575, 500)
                    elif act == 2:
                        botdif2 = (botdif2+1) % 8
                        drawbutton(screen, agentslist[botdif2], 575, 575)
                    elif act == 3:
                        return [whofirst, botdif1, botdif2]
                    elif act == 4:
                        return [whofirst, -2, -1]
            elif ev.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


# opt is for whofirst; opt2 is difficulty of bot1; opt3 is bot2
def everything(screen, numofps, opt, opt2, opt0):
    screen.fill(scenery)
    bg_img = pygame.image.load('download.jpeg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    bg_img.set_alpha(40)
    screen.blit(bg_img, (0, 0))
    BOARD = np.full(12, 5)
    state = GameState(board=BOARD)
    agent1 = None
    agent0 = None
    init_human = False  # False when not time to choose direc;True otherwwise
    direct = 0  # 1 if counter clockwise; -1 if clockwise
    # 0 for P1; 1 for bot1;2 for P2; 3 for bot2/ next turn: playturn=(numofps+playturn)%(numofps+1)
    playturn = numofps*opt
    if numofps == 0:
        playturn = (opt*2+3) % 4
        if opt2 == 0:
            agent1 = RandomAgent(gstate=state,reversed=True)
        elif opt2 == 1:
            agent1 = GreedyAgent(gstate=state,reversed=True)
        elif opt2 == 2:
            agent1 = MinimaxAgent(gstate=state, reversed=True, dept=2)
        elif opt2 == 3:
            agent1 = MinimaxAgent(gstate=state, reversed=True, dept=4)
        elif opt2 == 4:
            agent1 = AlphaBetaAgent(gstate=state, reversed=True, dept=2)
        elif opt2 == 5:
            agent1 = AlphaBetaAgent(gstate=state, reversed=True, dept=4)
        elif opt2 == 6:
            agent1 = AlphaBetaAgent(gstate=state, reversed=True, dept=6)
        elif opt2==7:
            agent1=QLearningAgent(gstate=state,reversed=True)
        # agent0
        if opt0 == 0:
            agent0 = RandomAgent(gstate=state,reversed=False)
        elif opt0 == 1:
            agent0 = GreedyAgent(gstate=state,reversed=False)
        elif opt0 == 2:
            agent0 = MinimaxAgent(gstate=state, reversed=False, dept=2)
        elif opt0 == 3:
            agent0 = MinimaxAgent(gstate=state, reversed=False, dept=4)
        elif opt0 == 4:
            agent0 = AlphaBetaAgent(gstate=state, reversed=False, dept=2)
        elif opt0 == 5:
            agent0 = AlphaBetaAgent(gstate=state, reversed=False, dept=4)
        elif opt0 == 6:
            agent0 = AlphaBetaAgent(gstate=state, reversed=False, dept=6)
        elif opt0==7:
            agent0=QLearningAgent(gstate=state,reversed=False)
    elif numofps==1:
        if opt2==0:
            agent1=GreedyAgent(gstate=state,reversed=True)
        elif opt2==1:
            agent1=MinimaxAgent(gstate=state, reversed=True, dept=2)
        elif opt2==2:
            agent1=AlphaBetaAgent(gstate=state, reversed=True, dept=6)
        elif opt2==3:
            agent1=QLearningAgent(gstate=state,reversed=True)
    draw_state(screen, state, playturn, numofps, opt2, opt0)
    pygame.display.update()
    pau = False
    cell = -1
    act = -1
    while True:
        for ev in pygame.event.get():
            if ev.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                act = checkbox(mousepos, gamebutton_coor, 150, 40)
                if act != -1:
                    screen.blit(s_1, (475+200*act, 545))
                    pygame.display.update()
                elif not(pau) and playturn % 2 == 0:
                    if not(init_human):
                        act = checkbox(mousepos, board_coor, 110, 110)
                        if act != -1:
                            act += 2
                        cell = act-2
                    else:
                        act = checkbox(mousepos, direct_coor, 44, 22)
                        if act != -1:
                            act += 14
            elif ev.type == MOUSEBUTTONUP:
                if act > 1 or (init_human and act == -1):
                    if init_human:
                        if act == -1:
                            change_board_coor(screen, 8, True)
                            draw_state(screen, state, playturn,
                                       numofps, opt2, opt0)
                        else:
                            if act == 14:
                                direct = 1*(1-playturn)
                            elif act == 15:
                                direct = -1*(1-playturn)
                            change_board_coor(screen, 8, True)
                            draw_state(screen, state, playturn,
                                       numofps, opt2, opt0)
                            point = GamePointer(cell, direct)
                            res = perform_action(
                                screen, state, point, playturn, numofps, opt2, opt0)
                            state = res
                            re = check_end(screen, state, numofps, opt2, opt0)
                            if re != -99:
                                return [re, state.player1_score, state.player2_score, opt2, opt0]
                            playturn = (numofps+playturn) % (numofps*2)
                            draw_state(screen, state, playturn,
                                       numofps, opt2, opt0)
                            pygame.display.update()
                        init_human = False
                    elif ((act in range(3, 8) and playturn == 0) or (act in range(9, 14) and playturn == 2)) and state.board[act-2] != 0:
                        change_board_coor(screen, act, False)
                        init_human = True
                elif act == 0:
                    pau = not(pau)
                    pygame.event.clear()
                    if pau:
                        drawbutton(screen, "Tiếp tục", 475, 545)
                        screen.blit(font.render("Trò chơi tạm dừng",
                                    False, black), (570, 590))
                    else:
                        draw_state(screen, state, playturn,
                                   numofps, opt2, opt0)
                elif act == 1:
                    change_board_coor(screen, act, True)
                    pygame.event.clear()
                    return [-2, 0, 0, 0, 0]
            elif ev.type == pygame.QUIT:
                sys.exit()
        if playturn==0 or playturn==2:
            is_upside = (playturn == 0)
            if state.no_more_moves(is_upside):
                state.scatter_stones(is_upside)
                if is_upside:
                    for coor in board_coor[1:6]:
                        screen.blit(s, coor)
                else:
                    for coor in board_coor[7:]:
                        screen.blit(s, coor)
                pygame.display.update()
                pygame.time.delay(300)
                draw_state(screen, state, playturn,
                                            numofps, opt2, opt0)
        if playturn == 1:
            pygame.time.delay(500)
            line = state.board[7:]
            if not(np.any(line)):
                for coor in board_coor[7:]:
                    screen.blit(s, coor)
                pygame.display.update()
                pygame.time.delay(300)
                draw_state(screen, state, playturn, numofps, opt2, opt0)
            point = agent1.find_best_move()[0]
            pygame.display.update()
            state = perform_action(screen, state, point,
                                   playturn, numofps, opt2, opt0)
            re = check_end(screen, state, numofps, opt2, opt0)
            if re != -99:
                return [re, state.player1_score, state.player2_score, opt2, opt0]
            if numofps == 0:
                playturn = (playturn+2) % 4
            else:
                playturn = (numofps+playturn) % (numofps+1)
            draw_state(screen, state, playturn, numofps, opt2, opt0)
            pygame.display.update()
        if playturn == 3:
            pygame.time.delay(500)
            line = state.board[1:6]
            if not(np.any(line)):
                for coor in board_coor[1:6]:
                    screen.blit(s, coor)
                pygame.display.update()
                pygame.time.delay(300)
                draw_state(screen, state, playturn, numofps, opt2, opt0)
            point = agent0.find_best_move()[0]
            pygame.display.update()
            state = perform_action(screen, state, point,
                                   playturn, numofps, opt2, opt0)
            re = check_end(screen, state, numofps, opt2, opt0)
            if re != -99:
                return [re, state.player1_score, state.player2_score, opt2, opt0]
            playturn = (playturn+2) % 4
            draw_state(screen, state, playturn, numofps, opt2, opt0)
        pygame.display.update()


def winner(screen, step_3: list):
    whowin = step_3[0]
    player1score = step_3[1]
    player2score = step_3[2]
    opt2 = step_3[3]
    opt0 = step_3[4]
    screen.fill(rock_1)
    bg_img = pygame.image.load('download.jpeg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    bg_img.set_alpha(40)
    screen.blit(bg_img, (0, 0))
    agentlist = ["Máy (Dễ)", "Máy (Vừa)", "Máy (Khó)", "Máy (Q-Learning)"]
    option = ""
    score1 = ""
    score2 = ""
    if whowin in [0, 3, 6]:
        score1 = agentslist[opt0]
        score2 = agentslist[opt2]
    elif whowin in [1, 4, 7]:
        score1 = "bạn"
        score2 = agentlist[opt2]
    else:
        score1 = "người chơi 1"
        score2 = "người chơi 2"
    if whowin in range(0, 3):
        option = score1[0].upper() + score1[1:] + " thắng!"
    elif whowin in range(3, 6):
        option = score2[0].upper() + score2[1:] + " thắng!"
    else:
        option = "Đây là một trận hòa!"
    text = font_end.render(option, False, boxcontent)
    tet_coor = text.get_rect(center=(650, 410))
    screen.blit(text, tet_coor)
    text2 = font_number.render(
        "Điểm của " + score1+": "+str(player1score), False, boxcontent)
    tet2_coor = text2.get_rect(center=(650, 450))
    screen.blit(text2, tet2_coor)
    text3 = font_number.render(
        "Điểm của "+score2+": "+str(player2score), False, boxcontent)
    tet3_coor = text3.get_rect(center=(650, 490))
    screen.blit(text3, tet3_coor)
    drawbutton(screen, "Thoát", 675, 545)
    drawbutton(screen, "Chơi mới", 475, 545)
    act = -1
    while True:
        for ev in pygame.event.get():
            if ev.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                act = checkbox(mousepos, gamebutton_coor, 150, 40)
                if act != -1:
                    screen.blit(s_1, (475+act*200, 545))
                    pygame.display.update()
            elif ev.type == MOUSEBUTTONUP:
                if act == 0:
                    return -2
                elif act == 1:
                    sys.exit()
            elif ev.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


def perform_action(screen, state: GameState, pointer: GamePointer, playturn, numofps, opt2, opt0):
    is_upside = (pointer.id in range(1, 6))
    score = 0
    is_continue = True
    pau = False
    act = -1
    while is_continue:
        stones = state.board[pointer.id]
        state.board[pointer.id] = 0
        draw_state(screen, state, playturn, numofps, opt2, opt0)
        if pointer.id in range(6, 12):
            draw_pile(
                screen, stones, (board_coor[pointer.id][0], board_coor[pointer.id][1]-110), -1)
        else:
            draw_pile(
                screen, stones, (board_coor[pointer.id][0], board_coor[pointer.id][1]+110), -1)
        pygame.display.update()
        pygame.time.delay(500)
        while stones > 0:
            if not(pau):
                pointer.next()
                state.board[pointer.id] += 1
                stones -= 1
                draw_state(screen, state, playturn, numofps, opt2, opt0)
                if pointer.id in range(6, 12):
                    draw_pile(
                        screen, stones, (board_coor[pointer.id][0], board_coor[pointer.id][1]-110), -1)
                else:
                    draw_pile(
                        screen, stones, (board_coor[pointer.id][0], board_coor[pointer.id][1]+110), -1)
            for ev in pygame.event.get():
                if ev.type == MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    act = checkbox(mousepos, gamebutton_coor, 150, 40)
                    if act != -1:
                        screen.blit(s_1, (475+200*act, 545))
                        pygame.display.update()
                elif ev.type == MOUSEBUTTONUP:
                    if act == 0:
                        pygame.event.clear()
                        pau = not(pau)
                        if pau:
                            drawbutton(screen, "Tiếp tục", 475, 545)
                            screen.blit(font.render(
                                "Trò chơi tạm dừng", False, boxcontent), (600, 590))
                        else:
                            draw_state(screen, state, playturn,
                                       numofps, opt2, opt0)
                    elif act == 1:
                        pygame.event.clear()
                        state.call = -99
                        return state
                elif ev.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
            pygame.time.delay(300)
        pointer.next()
        if pointer.id == 0 or pointer.id == 6:
            return state
        if state.board[pointer.id] == 0:
            while state.board[pointer.id] == 0:
                pointer.next()
                if state.board[pointer.id]:
                    score += state.board[pointer.id]
                    state.board[pointer.id] = 0
                    if pointer.id == 0:
                        state.empty_1 = True
                    elif pointer.id == 6:
                        state.empty_2 = True
                    screen.blit(s, (board_coor[pointer.id]))
                    pygame.display.update()
                    pygame.time.delay(500)
                    draw_state(screen, state, playturn, numofps, opt2, opt0)
                    pygame.display.update()
                    pygame.time.delay(500)
                    pointer.next()
                else:
                    is_continue = False
                    break
            else:
                break
    if is_upside:
        state.player1_score += score
    else:
        state.player2_score += score
    draw_state(screen, state, playturn, numofps, opt2, opt0)
    pointer.next()
    pygame.event.clear()
    return state


# support funcs
def check_end(screen, state: GameState, numofps, opt2, opt0):
    if state.is_end_state():
        winner = state.find_winner()
        draw_state(screen, state, -1, numofps, opt2, opt0)
        pygame.display.update()
        pygame.time.delay(1500)
        if winner == "Player 1":
            if numofps == 0:
                return 0
            elif numofps == 1:
                return 1
            else:
                return 2
        elif winner == "Player 2":
            if numofps == 0:
                return 3
            elif numofps == 1:
                return 4
            else:
                return 5
        elif winner == "Draw":
            if numofps == 0:
                return 6
            elif numofps == 1:
                return 7
            else:
                return 8
        else:
            return -2
    if state.call == -99:
        return -2
    return -99


def change_board_coor(screen, act, option=False):
    color = boxcontent
    if option:
        color = scenery
    if act < 8:
        data.direct_coor.append(
            [board_coor[act-2][0], board_coor[act-2][1]+121])
        data.direct_coor.append(
            [board_coor[act-2][0]+66, board_coor[act-2][1]+121])
    elif act > 8:
        data.direct_coor.append(
            [board_coor[act-2][0], board_coor[act-2][1]-33])
        data.direct_coor.append(
            [board_coor[act-2][0]+66, board_coor[act-2][1]-33])
    pygame.draw.rect(
        screen, color, (data.direct_coor[0][0]+19, data.direct_coor[0][1]+5, 25, 12))
    pygame.draw.rect(
        screen, color, (data.direct_coor[1][0], data.direct_coor[1][1]+5, 25, 12))
    pygame.draw.polygon(screen, color, ((data.direct_coor[0][0], data.direct_coor[0][1]+11), (
        data.direct_coor[0][0]+19, data.direct_coor[0][1]), (data.direct_coor[0][0]+19, data.direct_coor[0][1]+22)))
    pygame.draw.polygon(screen, color, ((data.direct_coor[1][0]+44, data.direct_coor[1][1]+11), (
        data.direct_coor[1][0]+25, data.direct_coor[1][1]), (data.direct_coor[1][0]+25, data.direct_coor[1][1]+22)))
    if option:
        data.direct_coor.clear()


def drawbutton(screen, str, left, top):
    tet = font.render(str, False, boxcontent)
    text_rect = tet.get_rect(center=(75, 20))
    pygame.draw.rect(screen, boxcolor, pygame.Rect(
        left, top, button_width, button_height), 0, 40)
    pygame.draw.rect(screen, boxcontent, pygame.Rect(
        left, top, button_width, button_height), 3, 40)
    screen.blit(tet, (text_rect[0]+left, text_rect[1]+top))


def checkbox(coor, coor_list, indent1, indent2):
    i = 0
    for lis in coor_list:
        if (coor[0] in range(lis[0], lis[0]+indent1)) and (coor[1] in range(lis[1], lis[1]+indent2)):
            return i
        i = i+1
    return -1


def draw_grid(screen):
    pygame.draw.rect(screen, playzonecolor, pygame.Rect(
        265, 215, 770, 220), width=0, border_radius=100)
    pygame.draw.rect(screen, shading, pygame.Rect(
        265, 215, 770, 220), 5, 100)
    for i in range(0, 6):
        pygame.draw.line(screen, shading, (375+110*i, 215),
                         (375+110*i, 433), 5)
    pygame.draw.line(screen, shading, (375, 325), (925, 325), 5)


def draw_state(screen, state: GameState, playturn, numofps, opt2, opt0):
    screen.fill(rock_1)
    bg_img = pygame.image.load('download.jpeg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    bg_img.set_alpha(40)
    screen.blit(bg_img, (0, 0))
    draw_grid(screen)
    drawbutton(screen, "Trang chính", 675, 545)
    drawbutton(screen, "Tạm dừng", 475, 545)
    option2 = ""
    option1 = ""
    diff = ["Dễ", "Vừa", "Khó","Q-Learning"]
    if numofps == 1:
        option1 = "Bạn"
        option2 = "Máy (" + diff[opt2] + ")"
    elif numofps == 2:
        option2 = "Người chơi 2"
        option1 = "Người chơi 1"
    else:
        option1 = agentslist[opt0]
        option2 = agentslist[opt2]
    for i in range(0, 12):
        if state.board[i] >= 5 and ((i == 0 and state.empty_1 == False) or (i == 6 and state.empty_2 == False)):
            draw_rock(screen, board_coor[i], 1, 2, special=True)
            draw_pile(screen, state.board[i]-5, board_coor[i], 0)
        else:
            draw_pile(screen, state.board[i], board_coor[i])
    s_empathize = pygame.Surface((185, 140))
    s_empathize.fill(boxcolor)
    s_empathize.set_alpha(180)
    if playturn == 0 or playturn == 3:
        pygame.draw.polygon(
            screen, boxcontent, ((1080, 475), (1035, 450), (1035, 500)))
        # pygame.draw.polygon(
        #     screen, boxcontent, ((1080, 475), (1035, 450), (1035, 500)),3)
        screen.blit(s_empathize, (1100, 405))
    elif playturn == 1 or playturn == 2:
        pygame.draw.polygon(
            screen, boxcontent, ((230, 175), (275, 150), (275, 200)))
        # pygame.draw.polygon(
        #     screen, boxcontent, ((230, 175), (275, 150), (275, 200)),3)
        screen.blit(s_empathize, (25, 105))
    pygame.draw.rect(screen, boxcontent, (1100, 405, 185, 140), 5)
    pygame.draw.rect(screen, boxcontent, (25, 105, 185, 140), 5)
    oprender1 = font_number.render(option1, False, boxcontent)
    oprender2 = font_number.render(option2, False, boxcontent)
    text_rect_1 = oprender1.get_rect(center=(1192, 375))
    text_rect_2 = oprender2.get_rect(center=(117, 75))
    screen.blit(oprender1, text_rect_1)
    screen.blit(oprender2, text_rect_2)
    screen.blit(font_number.render(
        "Điểm: " + str(state.player1_score), False, boxcontent), (1125, 440))
    screen.blit(font_number.render(
        "Nợ: " + str(state.player1_debt), False, boxcontent), (1125, 490))
    screen.blit(font_number.render(
        "Điểm: " + str(state.player2_score), False, boxcontent), (50, 140))
    screen.blit(font_number.render(
        "Nợ: " + str(state.player2_debt), False, boxcontent), (50, 190))


# code is for color option; special is for big rock option
def draw_rock(screen, coor, i, j, special=False):
    x = coor[0]
    y = coor[1]
    color = ()
    if j == 0:
        color = rock
    elif j == 1:
        color = rock_2
    else:
        color = rock_1
    if special == False:
        if i == 0:
            pygame.draw.ellipse(screen, color, (x+2, y+2, 20, 25))
            pygame.draw.ellipse(screen, black, (x+2, y+2, 20, 25), 1)
        elif i == 1:
            pygame.draw.ellipse(screen, color, (x+7, y+5, 26, 21))
            pygame.draw.ellipse(screen, black, (x+7, y+5, 26, 21), 1)
        elif i == 2:
            pygame.draw.ellipse(screen, color, (x+2, y+5, 24, 30))
            pygame.draw.ellipse(screen, black, (x+2, y+5, 24, 30), 1)
    else:
        pygame.draw.ellipse(screen, color, (x+22, y+2, 50, 85))
        pygame.draw.ellipse(screen, black, (x+22, y+2, 50, 85), 1)


def draw_pile(screen, num, pos, special=1):
    x = pos[0]
    y = pos[1]
    if special == 0:
        screen.blit(font.render(str(num+5), False, black), (x+7, y+82))
    elif special == 1:
        screen.blit(font.render(str(num), False, black), (x+7, y+82))
    if num == 1:
        draw_rock(screen, (x+57, y+36), 0, 1)
    elif num == 2:
        draw_rock(screen, (x+8, y+25), 0, 1)
        draw_rock(screen, (x+63, y+30), 2, 1)
    elif num == 3:
        draw_rock(screen, (x+28, y+45), 0, 1)
        draw_rock(screen, (x+72, y+43), 2, 1)
        draw_rock(screen, (x+46, y+7), 1, 2)
    elif num == 4:
        draw_rock(screen, (x+10, y+47), 0, 1)
        draw_rock(screen, (x+71, y+45), 2, 1)
        draw_rock(screen, (x+12, y+7), 1, 2)
        draw_rock(screen, (x+69, y+5), 2, 2)
    elif num == 5:
        draw_rock(screen, (x+10, y+47), 0, 1)
        draw_rock(screen, (x+61, y+52), 2, 1)
        draw_rock(screen, (x+12, y+17), 1, 2)
        draw_rock(screen, (x+59, y+25), 2, 2)
        draw_rock(screen, (x+45, y+55), 0, 0)
    elif num == 6:
        draw_rock(screen, (x+12, y+32), 0, 1)
        draw_rock(screen, (x+51, y+30), 2, 1)
        draw_rock(screen, (x+31, y+17), 1, 2)
        draw_rock(screen, (x+44, y+15), 2, 0)
        draw_rock(screen, (x+68, y+37), 0, 2)
        draw_rock(screen, (x+27, y+45), 0, 0)
    elif num >= 7:
        draw_rock(screen, (x+21, y+48), 0, 1)
        draw_rock(screen, (x+12, y+30), 2, 1)
        draw_rock(screen, (x+26, y+36), 1, 2)
        draw_rock(screen, (x+56, y+48), 2, 0)
        draw_rock(screen, (x+74, y+32), 0, 2)
        draw_rock(screen, (x+73, y+26), 0, 0)
        draw_rock(screen, (x+48, y+59), 1, 1)

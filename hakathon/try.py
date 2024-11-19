import pygame
import random
import time
import os

# 初始化 Pygame
pygame.init()

# 設定螢幕尺寸
screen_width, screen_height = 1021, 1021
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Natural Disaster Game")

# 顏色
BLUE = (0, 0, 255)   # 窗戶顏色
BROWN = (139, 69, 19) # 櫃子顏色
YELLOW = (255, 255, 0) # 桌子顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)  # 定義白色

# 設定角色參數
player_score = 6
game_time = 10  # 10 秒限時
start_time = time.time()

# 角色
player_pos = [400, 300]
player_size = 50

# 障礙物和目標位置
cabinet_pos = [32, 867]
window_pos = [109, 0]
window_pos1 = [749, 0]
desk_pos = [163, 361]
desk_pos1 = [674, 361]
desk_pos2 = [193, 683]
desk_pos3 = [673, 683]

# 加載背景圖片
background_image = pygame.image.load('background1.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # 調整圖片大小以符合螢幕

# 變數控制顯示警告
show_warning = False
game_over = False
win = False

# 變數控制提示顯示
show_hint = True  # 初始狀態為顯示提示
hint_close = False  # 控制提示關閉狀態

# 在遊戲主循環的碰撞檢查部分添加對話框邏輯
dialogue_open = False  # 控制對話框開啟狀態
selected_action = None  # 記錄玩家選擇的行動

cat_image  = pygame.image.load('cat.png')

# Function to shake the screen
def screen_shake(duration, intensity):
    start_time = time.time()
    while time.time() - start_time < duration:
        # Random offset for shaking effect
        offset_x = random.randint(-intensity, intensity)
        offset_y = random.randint(-intensity, intensity)

        # Apply the shake by blitting the background image with the offset
        screen.blit(background_image, (offset_x, offset_y))

        # Update the display
        pygame.display.flip()
        pygame.time.delay(30)  # Adjust delay for smoother effect



# 遊戲主循環
running = True
while running:
    if not game_over:
        screen.blit(background_image, (0, 0))  # 繪製背景圖片

        safety_hint_font = pygame.font.SysFont("Arial", 30)
        safety_hint_text = safety_hint_font.render("Please try to find a safer place inside the classroom!", True, BLACK)
        screen.blit(safety_hint_text, (screen_width // 2 - safety_hint_text.get_width() // 2, 10))  # 在螢幕上方居中顯示


        # 計算剩餘時間
        elapsed_time = time.time() - start_time
        remaining_time = game_time - elapsed_time

        # 設定每個物品的尺寸
        window_size = (161, 156)  # 窗戶大小
        cabinet_size = (188, 134)  # 櫃子大小
        desk_size = (182, 130)  # 桌子大小

        # 繪製完全透明的障礙物和目標
        window_surface = pygame.Surface(window_size, pygame.SRCALPHA)
        window_surface.fill((0, 0, 255))  # 窗戶顏色
        window_surface.set_alpha(0)  # 設定透明度為 0 (完全透明)
        screen.blit(window_surface, window_pos)

        window_surface1 = pygame.Surface(window_size, pygame.SRCALPHA)
        window_surface1.fill((0, 0, 255))
        window_surface1.set_alpha(0)
        screen.blit(window_surface1, window_pos1)

        cabinet_surface = pygame.Surface(cabinet_size, pygame.SRCALPHA)
        cabinet_surface.fill((139, 69, 19))  # 櫃子顏色
        cabinet_surface.set_alpha(0)
        screen.blit(cabinet_surface, cabinet_pos)

        desk_surface = pygame.Surface(desk_size, pygame.SRCALPHA)
        desk_surface.fill((255, 255, 0))  # 桌子顏色
        desk_surface.set_alpha(0)
        screen.blit(desk_surface, desk_pos)
        screen.blit(desk_surface, desk_pos1)
        screen.blit(desk_surface, desk_pos2)
        screen.blit(desk_surface, desk_pos3)

        # 繪製角色
        screen.blit(cat_image, (player_pos[0], player_pos[1]))

        # 更新分數和時間顯示
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {player_score}", True, BLACK)
        time_text = font.render(f"Time: {max(0, int(remaining_time))}", True, BLACK)
        screen.blit(score_text, (10, 30))  # 調整 X 和 Y 座標以更改分數顯示位置
        screen.blit(time_text, (10, 60))   # 調整 X 和 Y 座標以更改時間顯示位置

        # 檢查遊戲結束條件
        if remaining_time <= 0:
            game_over = True
            win = False
            print("Time's up")
        if player_score < 0:
            game_over = True
            win = False
            print("Your score is less than 0")
        touching_desk = (desk_pos[0] <= player_pos[0] <= desk_pos[0] + desk_size[0] and 
                         desk_pos[1] <= player_pos[1] <= desk_pos[1] + desk_size[1]) or \
                        (desk_pos1[0] <= player_pos[0] <= desk_pos1[0] + desk_size[0] and 
                         desk_pos1[1] <= player_pos[1] <= desk_pos1[1] + desk_size[1]) or \
                        (desk_pos2[0] <= player_pos[0] <= desk_pos2[0] + desk_size[0] and 
                         desk_pos2[1] <= player_pos[1] <= desk_pos2[1] + desk_size[1]) or \
                        (desk_pos3[0] <= player_pos[0] <= desk_pos3[0] + desk_size[0] and 
                         desk_pos3[1] <= player_pos[1] <= desk_pos3[1] + desk_size[1])

        if touching_desk:
            dialogue_open = True  # 打開對話框
        else:
            dialogue_open = False  # 離開桌子時關閉對話框


        if dialogue_open:
            # 繪製對話框
            dialogue_font = pygame.font.SysFont("Arial", 30)
            dialogue_surface = pygame.Surface((300, 150))
            dialogue_surface.fill(WHITE)
            screen.blit(dialogue_surface, (player_pos[0] + 50, player_pos[1] - 150))  # 在角色旁邊顯示

            # 顯示選項
            crunch_button = pygame.Rect(player_pos[0] + 70, player_pos[1] - 100, 100, 40)
            sit_button = pygame.Rect(player_pos[0] + 70, player_pos[1] - 50, 100, 40)

            pygame.draw.rect(screen, (0, 255, 0), crunch_button)  # 綠色按鈕
            crunch_text = dialogue_font.render("Crouch", True, BLACK)
            screen.blit(crunch_text, (crunch_button.x + 15, crunch_button.y + 5))

            pygame.draw.rect(screen, (255, 0, 0), sit_button)  # 紅色按鈕
            sit_text = dialogue_font.render("Sit on the Chair", True, BLACK)
            screen.blit(sit_text, (sit_button.x + 10, sit_button.y + 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if crunch_button.collidepoint(mouse_pos):
                        selected_action = 'crouch'
                        win = True
                        game_over = True  # 遊戲結束
                        dialogue_open = False  # 關閉對話框
                    elif sit_button.collidepoint(mouse_pos):
                        selected_action = 'sit on the chair'
                        player_score -= 5  # 扣除分數
                        if player_score<0:
                            win = False
                            game_over = True
                            dialogue_open = False  # 關閉對話框
                        game_over = False  # 遊戲繼續
                        dialogue_open = False  # 關閉對話框

        # 在遊戲主循環中添加這段代碼以顯示提示
        if show_hint:
            hint_font = pygame.font.SysFont("Arial", 20)
            hint_text = hint_font.render("Hint: Find a safe place to stay!!! Good luck (click me to close the hint)", True, BLACK)
            hint_rect = hint_text.get_rect(topleft=(screen_width - 550, 30))  # 右上角位置
            pygame.draw.rect(screen, WHITE, (hint_rect.x - 5, hint_rect.y - 5, hint_rect.width + 10, hint_rect.height + 10))  # 繪製提示框
            screen.blit(hint_text, hint_rect)

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠標點擊事件
                mouse_pos = event.pos
                if hint_rect.collidepoint(mouse_pos):  # 如果點擊到提示框
                    show_hint = False  # 關閉提示

        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 5
        if keys[pygame.K_UP]:
            player_pos[1] -= 5
        if keys[pygame.K_DOWN]:
            player_pos[1] += 5

        # 檢查碰撞
        if (window_pos[0] <= player_pos[0] <= window_pos[0] + window_size[0] and 
            window_pos[1] <= player_pos[1] <= window_pos[1] + window_size[1]) or \
           (window_pos1[0] <= player_pos[0] <= window_pos1[0] + window_size[0] and 
            window_pos1[1] <= player_pos[1] <= window_pos1[1] + window_size[1]) or \
           (cabinet_pos[0] <= player_pos[0] <= cabinet_pos[0] + cabinet_size[0] and 
            cabinet_pos[1] <= player_pos[1] <= cabinet_pos[1] + cabinet_size[1]):
            if not show_warning:  # 如果還沒有顯示警告，則扣分並顯示警告
                player_score -= 2  # 碰到窗戶或櫃子扣分
                show_warning = True  # 顯示警告
                screen_shake(duration=0.5, intensity=5) 
        else:
            show_warning = False  # 離開後隱藏警告

        # 顯示警告訊息
        if show_warning:
            warning_text = font.render("This is not safe!", True, BLACK)
            screen.blit(warning_text, (screen_width // 2 - 100, screen_height // 2 - 15))  # 在畫面中央顯示警告

    else:  # 遊戲結束後顯示結果畫面
        show_hint = False
        screen.fill(WHITE)  # 用白色填充螢幕
        result_font = pygame.font.SysFont("Arial", 50)
        if win:
            result_text = result_font.render("Congratulations! You win!", True, BLACK)
        else:
            result_text = result_font.render("Game Over! You lost!", True, BLACK)

        score_final_text = result_font.render(f"Final Score: {player_score}", True, BLACK)
        screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(score_final_text, (screen_width // 2 - score_final_text.get_width() // 2, screen_height // 2))

        # 設定按鈕大小
        button_width = 200
        button_height = 50

        # 繪製繼續按鈕
        continue_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 50, button_width, button_height)
        pygame.draw.rect(screen, (0, 255, 0), continue_button_rect)  # 綠色按鈕
        continue_text = result_font.render("Continue", True, BLACK)
        screen.blit(continue_text, (screen_width // 2 - continue_text.get_width() // 2, screen_height // 2 + 55))

        # 繪製退出按鈕
        exit_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 140, button_width, button_height)
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)  # 紅色按鈕
        exit_text = result_font.render("Exit", True, BLACK)
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 145))

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠標點擊事件
                mouse_pos = event.pos
                if continue_button_rect.collidepoint(mouse_pos):  # 如果點擊到繼續按鈕
                    pygame.quit()  # 關閉 Pygame
                    os.system('python scene2.py')  # 執行 scene2.py
                    exit()  # 確保當前程式完全退出
                if exit_button_rect.collidepoint(mouse_pos):  # 如果點擊到退出按鈕
                    running = False
                

    pygame.display.flip()  # 更新顯示
    pygame.time.delay(30)  # 限制遊戲迴圈速度

pygame.quit()
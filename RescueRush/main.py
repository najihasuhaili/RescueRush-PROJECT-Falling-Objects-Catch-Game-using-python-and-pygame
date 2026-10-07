import pygame
pygame.mixer.init()
from player import Player
from objects import create_random_object

# INITIALIZE
pygame.init()
pygame.mixer.music.load(
    "assets/background_music.wav"
)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

collect_sound = pygame.mixer.Sound(
    "assets/collect.wav"
)
collect_sound.set_volume(0.7)

hit_sound = pygame.mixer.Sound(
    "assets/hit.wav"
)
hit_sound.set_volume(0.7)

typing_sound = pygame.mixer.Sound(
    "assets/typing.wav"
)

typing_sound.set_volume(0.3)


WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
home_bg = pygame.image.load("assets/home_bg.jpg").convert()
home_bg = pygame.transform.scale(home_bg, (WIDTH, HEIGHT))
logo_image = pygame.image.load("assets/logo.png").convert_alpha()
logo_image = pygame.transform.smoothscale(logo_image, (220, 75))
start_image = pygame.image.load("assets/start.png").convert_alpha()
start_image = pygame.transform.smoothscale(start_image, (180, 70))
exit_image = pygame.image.load("assets/exit.png").convert_alpha()
exit_image = pygame.transform.smoothscale(exit_image, (120, 60))
game_bg = pygame.image.load("assets/bg.jpg").convert()
game_bg = pygame.transform.scale(
    game_bg,
    (WIDTH, HEIGHT)
)
pause_image = pygame.image.load("assets/pause.png").convert_alpha()

pause_image = pygame.transform.scale(
    pause_image,
    (300, 150)
)
pygame.display.set_caption("Rescue Rush")

clock = pygame.time.Clock()

# FONTS
font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 60)
countdown_font = pygame.font.Font(None, 120)

# PLAYER
player = Player(
    WIDTH // 2 - 40,
    HEIGHT - 150
)


# OBJECTS
falling_objects = []

# GAME SETTINGS
LEVEL_TIME = 20
current_level = 1
level_start_time = 0
remaining_time = LEVEL_TIME
spawn_timer = 0
spawn_delay = 1000

# GAME STATES
# story_intro
# playing
# story_between
# countdown
# game_over
# complete
game_state = "story_intro"

# STORY

story_intro = (
    "A disaster has struck the area without warning. "
    "The rescue team has arrived, but the situation "
    "is far from safe. Essential supplies are being "
    "delivered to the rescue zone, while dangerous "
    "debris continues to fall from above. You are "
    "one of the rescue workers assigned to collect "
    "the supplies and keep the operation running. "
    "Every second counts. Can you complete the rescue mission?"
)
story_level_2 = (
    "The rescue operation was going well, but the "
    "situation suddenly began to change. More debris "
    "started falling into the rescue zone, while fire "
    "broke out nearby. The rescue team is now facing "
    "greater danger, and they need you to stay focused "
    "and collect as many supplies as possible."
)
story_level_3 = (
    "The situation has now become critical. The rescue "
    "zone is becoming harder to control, supplies are "
    "running low, and dangerous objects are falling "
    "faster than before. This is the final stage of "
    "the operation. The survivors are depending on you."
)
story_intro_bm = (
    "Satu bencana telah berlaku tanpa amaran. Pasukan "
    "penyelamat telah tiba, tetapi keadaan masih tidak "
    "selamat. Bekalan penting sedang dihantar ke zon "
    "menyelamat, manakala serpihan berbahaya terus "
    "jatuh dari atas. Anda ialah salah seorang pekerja "
    "penyelamat yang ditugaskan untuk mengumpul bekalan "
    "dan memastikan operasi terus berjalan. Setiap saat "
    "amat penting. Bolehkah anda menyelesaikan misi menyelamat?"
)

story_level_2_bm = (
    "Operasi menyelamat berjalan dengan baik, tetapi "
    "keadaan tiba-tiba berubah. Lebih banyak serpihan "
    "mula jatuh ke zon menyelamat, manakala kebakaran "
    "berlaku berhampiran. Pasukan penyelamat kini "
    "menghadapi bahaya yang lebih besar, dan mereka "
    "memerlukan anda untuk terus fokus dan mengumpul "
    "sebanyak mungkin bekalan."
)

story_level_3_bm = (
    "Keadaan kini menjadi kritikal. Zon menyelamat "
    "semakin sukar dikawal, bekalan semakin berkurangan, "
    "dan objek berbahaya jatuh lebih pantas daripada "
    "sebelum ini. Ini ialah peringkat terakhir operasi. "
    "Para mangsa bergantung kepada anda."
)

# STORY VARIABLES
current_story = story_intro
story_char_index = 0
story_finished = False
story_last_update = 0
STORY_SPEED = 30
floating_texts = []
paused = False
pause_start_time = 0
total_pause_time = 0
language = "EN"

# COUNTDOWN VARIABLES
countdown_start = 0
countdown_level = 0

# HIT COOLDOWN
last_hit_time = 0
HIT_COOLDOWN = 500

def add_floating_text(text, x, y, color):
    floating_texts.append({
        "text": text,
        "x": x,
        "y": y,
        "color": color,
        "timer": 0
    })

# START STORY
def start_story(text, next_level=None):
    global game_state
    global current_story
    global story_char_index
    global story_finished
    global story_last_update
    global countdown_level
    game_state = "story_between" if next_level else "story_intro"
    current_story = text
    story_char_index = 0
    story_finished = False
    story_last_update = pygame.time.get_ticks()
    if next_level is not None:
        countdown_level = next_level

# START LEVEL
def start_level(level):
    global current_level
    global level_start_time
    global spawn_timer
    global spawn_delay
    global game_state
    global falling_objects
    current_level = level
    level_start_time = pygame.time.get_ticks()
    spawn_timer = 0
    falling_objects.clear()

    # Difficulty
    if level == 1:
        spawn_delay = 1000
    elif level == 2:
        spawn_delay = 700
    else:
        spawn_delay = 450
    game_state = "playing"

# START COUNTDOWN
def start_countdown(level):
    global game_state
    global countdown_start
    global countdown_level
    game_state = "countdown"
    countdown_start = pygame.time.get_ticks()
    countdown_level = level

# TEXT WRAPPING
def draw_wrapped_text(
        text,
        font_used,
        color,
        center_x,
        start_y,
        max_width
):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font_used.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    y = start_y
    for line in lines:
        text_surface = font_used.render(
            line,
            True,
            color
        )

        screen.blit(
            text_surface,
            (
                center_x - text_surface.get_width() // 2,
                y
            )
        )
        y += font_used.get_height() + 8

# INITIAL GAME STATE
game_state = "home"

# HOME BUTTON POSITIONS
en_button = pygame.Rect(WIDTH - 100, 15, 35, 30)
bm_button = pygame.Rect(WIDTH - 55, 15, 35, 30)
start_button = pygame.Rect(WIDTH // 2 - start_image.get_width() // 2, 330, start_image.get_width(), start_image.get_height())
exit_button = pygame.Rect(WIDTH // 2 - exit_image.get_width() // 2, 525, exit_image.get_width(), exit_image.get_height())
home_button = pygame.Rect(WIDTH // 2 - 75, 455, 150, 50)

# MAIN LOOP
running = True
while running:

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # LANGUAGE BUTTONS
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "home":

                if en_button.collidepoint(event.pos):
                    language = "EN"

                elif bm_button.collidepoint(event.pos):
                    language = "BM"

                elif start_button.collidepoint(event.pos):
                    start_story(story_intro if language == "EN" else story_intro_bm)

                elif exit_button.collidepoint(event.pos):
                    running = False

            elif game_state in ["game_over", "complete"]:
                if home_button.collidepoint(event.pos):
                    player.lives = 3
                    player.score = 0
                    player.x = WIDTH // 2 - player.width // 2
                    falling_objects.clear()
                    current_level = 1
                    remaining_time = LEVEL_TIME
                    paused = False
                    total_pause_time = 0
                    game_state = "home"
        if event.type == pygame.KEYDOWN:
            #PAUSE
            if event.key == pygame.K_p:
                if game_state == "playing":
                    if not paused:
                        paused = True
                        pause_start_time = pygame.time.get_ticks()
                    else:
                        paused = False
                        total_pause_time += (
                                pygame.time.get_ticks()
                                - pause_start_time
                        )
            # STORY
            if event.key == pygame.K_SPACE:
                if game_state in [
                    "story_intro",
                    "story_between"
                ]:

                    # Finish typing immediately
                    if not story_finished:
                        story_char_index = len(current_story)
                        story_finished = True
                        # Stop typing sound when skipping
                        typing_sound.stop()
                    else:
                        # Stop typing sound before leaving story
                        typing_sound.stop()
                        # INTRO → LEVEL 1
                        if game_state == "story_intro":
                            start_level(1)

                        # LEVEL 1 STORY → LEVEL 2
                        elif countdown_level == 2:
                            start_countdown(2)

                        # LEVEL 2 STORY → LEVEL 3
                        elif countdown_level == 3:
                            start_countdown(3)

            # RESTART
            if event.key == pygame.K_r:
                if game_state in [
                    "game_over",
                    "complete"
                ]:
                    player.lives = 3
                    player.score = 0
                    player.x = WIDTH // 2 - player.width // 2
                    falling_objects.clear()
                    current_level = 1
                    start_story(
                        story_intro if language == "EN"
                        else story_intro_bm
                    )

            # HOME MENU
            if game_state == "home":

                if event.key == pygame.K_RETURN:
                    start_story(
                        story_intro if language == "EN"
                        else story_intro_bm
                    )

                elif event.key == pygame.K_i:
                    game_state = "instructions"

                elif event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_l:
                    if language == "EN":
                        language = "BM"
                    else:
                        language = "EN"

            # INSTRUCTIONS
            if game_state == "instructions":
                if event.key == pygame.K_ESCAPE:
                    game_state = "home"

    # STORY
    if game_state in [
        "story_intro",
        "story_between"
    ]:
        current_time = pygame.time.get_ticks()
        if not story_finished:
            if not typing_sound.get_num_channels():
                typing_sound.play(-1)
            if current_time - story_last_update >= STORY_SPEED:
                story_char_index += 1
                story_last_update = current_time
                if story_char_index >= len(current_story):
                    story_char_index = len(current_story)
                    story_finished = True
                    typing_sound.stop()

    # PLAYING
    elif game_state == "playing":
        if not paused:
            # TIMER
            elapsed_time = (
                                   pygame.time.get_ticks()
                                   - level_start_time
                                   - total_pause_time
                           ) // 1000

            remaining_time = LEVEL_TIME - elapsed_time
            if remaining_time < 0:
                remaining_time = 0

            # PLAYER
            player.move(WIDTH)
            # SPAWN OBJECTS
            spawn_timer += clock.get_time()
            if spawn_timer >= spawn_delay:
                new_object = create_random_object(
                    WIDTH,
                    current_level
                )
                falling_objects.append(
                    new_object
                )
                spawn_timer = 0

            # UPDATE OBJECTS
            for obj in falling_objects:
                obj.update()
            # COLLISION
            current_time = pygame.time.get_ticks()
            for obj in falling_objects[:]:
                player_rect = player.get_rect()
                object_rect = obj.get_rect()
                if player_rect.colliderect(object_rect):
                    # Hazard
                    if obj.is_hazard():
                        # Prevent multiple damage too quickly
                        if current_time - last_hit_time >= HIT_COOLDOWN:
                            player.lives -= 1
                            hit_sound.play()
                            add_floating_text(
                                (
                                    "-1 LIFE"
                                    if language == "EN"
                                    else "-1 NYAWA"
                                ),
                                player.x + player.width // 2,
                                player.y,
                                (255, 80, 80)
                            )
                            last_hit_time = current_time
                    # Supply
                    else:
                        player.score += obj.get_score()
                        collect_sound.play()
                        add_floating_text(
                            f"+{obj.get_score()}",
                            player.x + player.width // 2,
                            player.y,
                            (255, 215, 0)
                        )
                    falling_objects.remove(obj)

            # UPDATE FLOATING TEXT
            for item in floating_texts[:]:
                item["y"] -= 1
                item["timer"] += 1
                if item["timer"] >= 40:
                    floating_texts.remove(item)

            # REMOVE OFF-SCREEN OBJECTS
            for obj in falling_objects[:]:
                if obj.is_off_screen(HEIGHT):
                    falling_objects.remove(obj)

        # GAME OVER
        if player.lives <= 0:
            game_state = "game_over"

        # LEVEL FINISHED
        elif remaining_time <= 0:
            if current_level == 1:
                start_story(
                    story_level_2 if language == "EN"
                    else story_level_2_bm,
                    next_level=2
                )
            elif current_level == 2:
                start_story(
                    story_level_3 if language == "EN"
                    else story_level_3_bm,
                    next_level=3
                )
            elif current_level == 3:
                game_state = "complete"

    # COUNTDOWN
    elif game_state == "countdown":
        current_time = pygame.time.get_ticks()
        elapsed = (
            current_time - countdown_start
        ) / 1000
        if elapsed >= 3:
            start_level(countdown_level)

    # BACKGROUND
    screen.fill(
        (20, 25, 35)
    )
    # HOME SCREEN
    if game_state == "home":
        screen.blit(home_bg, (0, 0))

        # Logo
        screen.blit(
            logo_image,
            (WIDTH // 2 - logo_image.get_width() // 2, 95)
        )

        # LANGUAGE BUTTONS
        pygame.draw.rect(screen, (45, 45, 55), en_button, border_radius=6)
        pygame.draw.rect(screen, (45, 45, 55), bm_button, border_radius=6)

        en_text = small_font.render("EN", True, (255, 255, 255))
        bm_text = small_font.render("BM", True, (255, 255, 255))

        screen.blit(en_text, (en_button.centerx - en_text.get_width() // 2, en_button.centery - en_text.get_height() // 2))
        screen.blit(bm_text, (bm_button.centerx - bm_text.get_width() // 2, bm_button.centery - bm_text.get_height() // 2))

        # START IMAGE BUTTON
        screen.blit(start_image, start_button.topleft)

        # CUSTOM INSTRUCTIONS PANEL
        instruction_title = "HOW TO PLAY" if language == "EN" else "CARA BERMAIN"
        instruction_hint = "Press I for Instructions" if language == "EN" else "Tekan I untuk Arahan"

        panel = pygame.Rect(55, 415, 390, 85)
        pygame.draw.rect(screen, (20, 25, 35), panel, border_radius=14)
        pygame.draw.rect(screen, (255, 215, 0), panel, 2, border_radius=14)

        instruction_text = small_font.render(instruction_title, True, (255, 215, 0))
        hint_text = small_font.render(instruction_hint, True, (255, 255, 255))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 430))
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, 460))

        # EXIT IMAGE BUTTON
        screen.blit(exit_image, exit_button.topleft)
    # INSTRUCTIONS SCREEN
    elif game_state == "instructions":

        title = big_font.render(
            "HOW TO PLAY",
            True,
            (255, 215, 0)
        )

        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                80
            )
        )

        if language == "EN":

            instructions = [
                "< LEFT / RIGHT > - Move Rescuer",
                "Catch supplies to gain points",
                "Avoid dangerous objects",
                "P - Pause / Resume",
                "R - Restart after Game Over",
                "",
                "Press ESC to return to Home"
            ]

        else:

            instructions = [
                "< KIRI / KANAN > - Gerakkan Penyelamat",
                "Tangkap bekalan untuk dapatkan mata",
                "Elakkan objek berbahaya",
                "P - Berhenti / Sambung",
                "R - Mula semula selepas Permainan Tamat",
                "",
                "Tekan ESC untuk kembali ke Home"
            ]

        y = 180

        for line in instructions:
            text = small_font.render(
                line,
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    y
                )
            )

            y += 50
    # INTRO STORY SCREEN
    if game_state == "story_intro":
        screen.blit(home_bg, (0, 0))
        screen.blit(logo_image, (WIDTH // 2 - logo_image.get_width() // 2, 55))

        displayed_text = current_story[:story_char_index]
        draw_wrapped_text(displayed_text, font, (255, 255, 255), WIDTH // 2, 180, 420)

        if story_finished:
            continue_text = small_font.render(
                "PRESS SPACE TO CONTINUE" if language == "EN" else "TEKAN SPACE UNTUK TERUSKAN",
                True, (255, 215, 0)
            )
            screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, 620))

    # BETWEEN LEVEL STORY
    elif game_state == "story_between":
        screen.blit(home_bg, (0, 0))
        screen.blit(logo_image, (WIDTH // 2 - logo_image.get_width() // 2, 45))
        title_text = (
            "THE SITUATION CHANGES..."
            if language == "EN"
            else "KEADAAN BERUBAH..."
        )
        title = font.render(
            title_text,
            True,
            (255, 215, 0)
        )
        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                135
            )
        )
        displayed_text = current_story[
            :story_char_index
        ]
        draw_wrapped_text(
            displayed_text,
            font,
            (255, 255, 255),
            WIDTH // 2,
            185,
            420
        )
        if story_finished:
            continue_text = small_font.render(
                "PRESS SPACE TO CONTINUE"
                if language == "EN"
                else "TEKAN SPACE UNTUK TERUSKAN",
                True,
                (255, 215, 0)
            )
            screen.blit(
                continue_text,
                (
                    WIDTH // 2
                    - continue_text.get_width() // 2,
                    620
                )
            )

    # PLAYING SCREEN
    elif game_state == "playing":
        screen.blit(
            game_bg,
            (0, 0)
        )
        # Player
        player.draw(screen)
        # Objects
        for obj in falling_objects:
            obj.draw(screen)
        for item in floating_texts:
            text_surface = small_font.render(
                item["text"],
                True,
                item["color"]
            )
            screen.blit(
                text_surface,
                (
                    item["x"] - text_surface.get_width() // 2,
                    item["y"]
                )
            )

        # SCORE
        score_text = font.render(
            (
                f"Score: {player.score}"
                if language == "EN"
                else f"Skor: {player.score}"
            ),
            True,
            (255, 255, 255)
        )
        screen.blit(
            score_text,
            (10, 10)
        )

        # LIVES
        lives_text = font.render(
            (
                f"Lives: {player.lives}"
                if language == "EN"
                else f"Nyawa: {player.lives}"
            ),
            True,
            (255, 255, 255)
        )
        screen.blit(
            lives_text,
            (350, 10)
        )

        # LEVEL
        level_text = font.render(
            (
                f"Level {current_level}"
                if language == "EN"
                else f"Aras {current_level}"
            ),
            True,
            (255, 255, 255)
        )
        screen.blit(
            level_text,
            (10, 45)
        )

        # TIMER
        time_text = font.render(
            (
                f"Time: {remaining_time}"
                if language == "EN"
                else f"Masa: {remaining_time}"
            ),
            True,
            (255, 255, 255)
        )
        screen.blit(
            time_text,
            (350, 45)
        )
        # PAUSE SCREEN
        if paused:
            # Pause symbol
            pause_y = HEIGHT // 2 - 100
            screen.blit(
                pause_image,
                (
                    WIDTH // 2 - pause_image.get_width() // 2,
                    pause_y
                )
            )

            # Resume text
            resume_text = small_font.render(
                (
                    "PRESS P TO RESUME"
                    if language == "EN"
                    else "TEKAN P UNTUK SAMBUNG"
                ),
                True,
                (255, 215, 0)
            )
            screen.blit(
                resume_text,
                (
                    WIDTH // 2
                    - resume_text.get_width() // 2,
                    pause_y + 150
                )
            )

    # COUNTDOWN SCREEN
    elif game_state == "countdown":
        level_up_text = big_font.render(
            (
                "LEVEL UP!"
                if language == "EN"
                else "NAIK ARAS!"
            ),
            True,
            (255, 215, 0)
        )
        screen.blit(
            level_up_text,
            (
                WIDTH // 2
                - level_up_text.get_width() // 2,
                170
            )
        )
        current_time = pygame.time.get_ticks()
        elapsed = (
            current_time - countdown_start
        ) / 1000
        number = 3 - int(elapsed)
        if number > 0:
            number_text = countdown_font.render(
                str(number),
                True,
                (255, 255, 255)
            )
            screen.blit(
                number_text,
                (
                    WIDTH // 2
                    - number_text.get_width() // 2,
                    290
                )
            )
        level_text = font.render(
            (
                f"GET READY FOR LEVEL {countdown_level}"
                if language == "EN"
                else f"SEDIA UNTUK ARAS {countdown_level}"
            ),
            True,
            (255, 255, 255)
        )
        screen.blit(
            level_text,
            (
                WIDTH // 2
                - level_text.get_width() // 2,
                470
            )
        )

    # GAME OVER
    elif game_state == "game_over":
        game_over_text = (
            "GAME OVER"
            if language == "EN"
            else "PERMAINAN TAMAT"
        )
        game_over_font = pygame.font.Font(
            None, 55 if language == "EN" else 45
        )
        title = game_over_font.render(
            game_over_text,
            True,
            (255, 80, 80)
        )
        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                180
            )
        )

        score_text = font.render(
            (
                f"Final Score: {player.score}"
                if language == "EN"
                else f"Skor Akhir: {player.score}"
            ),
            True,
            (255, 255, 255)
        )
        screen.blit(
            score_text,
            (
                WIDTH // 2 - score_text.get_width() // 2,
                300
            )
        )

        restart_text = small_font.render(
            (
                "PRESS R TO RESTART"
                if language == "EN"
                else "TEKAN R UNTUK MULA SEMULA"
            ),
            True,
            (255, 215, 0)
        )
        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                365
            )
        )

        pygame.draw.rect(
            screen,
            (45, 45, 55),
            home_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (255, 215, 0),
            home_button,
            2,
            border_radius=10
        )
        home_text = small_font.render(
            "HOME" if language == "EN" else "UTAMA",
            True,
            (255, 255, 255)
        )
        screen.blit(
            home_text,
            (
                home_button.centerx - home_text.get_width() // 2,
                home_button.centery - home_text.get_height() // 2
            )
        )

    # COMPLETE
    elif game_state == "complete":
        complete_text = (
            "RESCUE COMPLETE!"
            if language == "EN"
            else "MISI MENYELAMAT SELESAI!"
        )
        complete_font = pygame.font.Font(
            None, 50 if language == "EN" else 35
        )
        title = complete_font.render(
            complete_text,
            True,
            (100, 255, 150)
        )
        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                180
            )
        )

        score_text = font.render(
            (
                f"Final Score: {player.score}"
                if language == "EN"
                else f"Skor Akhir: {player.score}"
            ),
            True,
            (255, 255, 255)
        )
        screen.blit(
            score_text,
            (
                WIDTH // 2 - score_text.get_width() // 2,
                300
            )
        )

        restart_text = small_font.render(
            (
                "PRESS R TO PLAY AGAIN"
                if language == "EN"
                else "TEKAN R UNTUK MAIN LAGI"
            ),
            True,
            (255, 215, 0)
        )
        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                365
            )
        )

        pygame.draw.rect(
            screen,
            (45, 45, 55),
            home_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (255, 215, 0),
            home_button,
            2,
            border_radius=10
        )
        home_text = small_font.render(
            "HOME" if language == "EN" else "UTAMA",
            True,
            (255, 255, 255)
        )
        screen.blit(
            home_text,
            (
                home_button.centerx - home_text.get_width() // 2,
                home_button.centery - home_text.get_height() // 2
            )
        )

    # UPDATE SCREEN
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

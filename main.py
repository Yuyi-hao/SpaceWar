from pyray import *
from raylib import *
from os.path import join
from random import uniform, randint

BG_COLOR = Color(15, 10, 50, 255)
PLAYER_SPEED = 500
BULLET_SPEED = 300
METEORITE_SPEED = 290
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
METEOR_TIMER_DURATION = 0.2

def main():
    # initialize raylib
    start_time = get_time()
    lives = 3
    player_pos = Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    player_scale = 0.5
    player_direction = Vector2(0, 0)
    player_texture = load_image(join('assets', 'spaceship.png'))
    player_texture = load_texture_from_image(player_texture)

    # bullets
    bullets = []
    bullet_scale = 1
    bullet_direction = Vector2(0, -1)
    bullet_texture = load_texture_from_image(load_image(join('assets', 'laser.png')))

    # meteorite
    meteorites = []
    meteorite_scale = 0.6
    meteorite_texture = load_texture_from_image(load_image(join('assets', 'meteor.png')))

    # sound load
    laser_sound = load_sound(join('assets', 'audio', 'laser.wav'))
    explosion_sound = load_sound(join('assets', 'audio', 'explosion.wav'))
    bg_music = load_music_stream(join('assets', 'audio', 'music.wav'))
    play_music_stream(bg_music)

    while not window_should_close():
        update_music_stream(bg_music)
        dt = get_frame_time()
        if get_time() - start_time > METEOR_TIMER_DURATION and len(meteorites) < 30:
            pos = Vector2(uniform(0, WINDOW_WIDTH-meteorite_texture.width*meteorite_scale), -meteorite_texture.height*meteorite_scale-100)
            direction = Vector2(uniform(-0.5, 0.5), 1)
            fine = True
            meteorites.append([pos, direction, fine])
            start_time = get_time()

        # see player movement
        player_direction.x = int(is_key_down(KEY_RIGHT) or is_key_down(KEY_D)) - int(is_key_down(KEY_LEFT) or is_key_down(KEY_A))
        player_direction.y = int(is_key_down(KEY_DOWN) or is_key_down(KEY_S)) - int(is_key_down(KEY_UP) or is_key_down(KEY_W))
        if is_key_pressed(KEY_SPACE) and len(bullets) < 10:
            bullets.append([Vector2(player_pos.x+player_texture.width*player_scale//2-bullet_texture.width//2, player_pos.y), True])
            play_sound(laser_sound)

        # if len(meteorites) < 30:

        player_direction = Vector2Normalize(player_direction)
        player_pos.x += player_direction.x*PLAYER_SPEED*dt
        player_pos.y += player_direction.y*PLAYER_SPEED*dt
        player_pos.x = max(min(player_pos.x, WINDOW_WIDTH-player_texture.width*player_scale), 0)
        player_pos.y = max(min(player_pos.y, WINDOW_HEIGHT-player_texture.height*player_scale), 0)

        bullets = [[bullet, alive] for bullet, alive in bullets if bullet.y > -500 and alive]
        meteorites = [[meteorite, direction, fine] for meteorite, direction, fine in meteorites if meteorite.y < WINDOW_HEIGHT + 100 and fine]

        for bullet, _ in bullets:
            bullet.x += bullet_direction.x*BULLET_SPEED*dt
            bullet.y += bullet_direction.y*BULLET_SPEED*dt


        for meteorite, meteorite_direction, _ in meteorites:
            meteorite.x += meteorite_direction.x*METEORITE_SPEED*dt
            meteorite.y += meteorite_direction.y*METEORITE_SPEED*dt
        
        for i in range(len(bullets)):
            for j in range(len(meteorites)):
                bullet = bullets[i][0]
                bullet_rect = Rectangle(bullet.x, bullet.y, bullet_scale*bullet_texture.width, bullet_texture.height*bullet_scale)
                meteorite = meteorites[j][0]
                meteorite_rect = Rectangle(meteorite.x, meteorite.y, meteorite_scale*meteorite_texture.width, meteorite_texture.height*meteorite_scale)
                if CheckCollisionRecs(bullet_rect, meteorite_rect):
                    meteorites[j][2] = False
                    bullets[i][1] = False
                    play_sound(explosion_sound)

        for j in range(len(meteorites)):
            player_rect = Rectangle(player_pos.x, player_pos.y, player_scale*player_texture.width, player_texture.height*player_scale)
            meteorite = meteorites[j][0]
            meteorite_rect = Rectangle(meteorite.x, meteorite.y, meteorite_scale*meteorite_texture.width, meteorite_texture.height*meteorite_scale)
            if CheckCollisionRecs(player_rect, meteorite_rect):
                meteorites[j][2] = False
                lives -= 1

        begin_drawing()
        clear_background(BG_COLOR)
        if lives > 0:
            for i in range(lives):
                x = player_texture.width*0.2*(i+1)*1.2
                draw_texture_ex(player_texture, Vector2(x, 20), 0, 0.2, WHITE)

            for bullet, _ in bullets:
                draw_texture_ex(bullet_texture, bullet, 0, bullet_scale, WHITE)

            for meteorite, _, _ in meteorites:
                draw_texture_ex(meteorite_texture, meteorite, 0, meteorite_scale, WHITE)


            for i in range(10-len(bullets)):
                draw_texture_ex(bullet_texture, Vector2((WINDOW_WIDTH - bullet_texture.width*2*0.4*(i+1)), WINDOW_HEIGHT-bullet_texture.height-10), 0, 0.4, WHITE)
            draw_texture_ex(player_texture, player_pos, 0, player_scale, WHITE)
        end_drawing()
    
    close_window()

if __name__=="__main__":
    init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Space War")
    init_audio_device()
    icon = load_image(join("assets", "icon.png"))
    set_window_icon(icon)
    main()
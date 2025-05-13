from pyray import *
from raylib import *
from os.path import join

BG_COLOR = Color(15, 10, 50, 255)
PLAYER_SPEED = 500
BULLET_SPEED = 400
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

def main():
    # initialize raylib
    player_pos = Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    player_scale = 0.5
    player_direction = Vector2(0, 0)
    player_texture = load_image(join('assets', 'spaceship.png'))
    player_texture = load_texture_from_image(player_texture)

    # bullets
    bullet_scale = 1
    bullet_direction = Vector2(0, -1)
    bullet_texture = load_texture_from_image(load_image(join('assets', 'laser.png')))

    bullets = []


    while not window_should_close():
        dt = get_frame_time()
        # see player movement
        player_direction.x = int(is_key_down(KEY_RIGHT) or is_key_down(KEY_D)) - int(is_key_down(KEY_LEFT) or is_key_down(KEY_A))
        player_direction.y = int(is_key_down(KEY_DOWN) or is_key_down(KEY_S)) - int(is_key_down(KEY_UP) or is_key_down(KEY_W))
        if is_key_pressed(KEY_SPACE) and len(bullets) < 10:
            bullets.append(Vector2(player_pos.x+player_texture.width*player_scale//2-bullet_texture.width//2, player_pos.y))
        player_direction = Vector2Normalize(player_direction)
        player_pos.x += player_direction.x*PLAYER_SPEED*dt
        player_pos.y += player_direction.y*PLAYER_SPEED*dt
        player_pos.x = max(min(player_pos.x, WINDOW_WIDTH-player_texture.width*player_scale), 0)
        player_pos.y = max(min(player_pos.y, WINDOW_HEIGHT-player_texture.height*player_scale), 0)

        for bullet in bullets:
            bullet.x += bullet_direction.x*BULLET_SPEED*dt
            bullet.y += bullet_direction.y*BULLET_SPEED*dt

        begin_drawing()
        clear_background(BG_COLOR)
        print(len(bullets))
        for bullet in bullets:
            draw_texture_ex(bullet_texture, bullet, 0, bullet_scale, WHITE)

        for i in range(10-len(bullets)):
            draw_texture_ex(bullet_texture, Vector2((WINDOW_WIDTH - bullet_texture.width*2*0.4*(i+1)), WINDOW_HEIGHT-bullet_texture.height-10), 0, 0.4, WHITE)
        draw_texture_ex(player_texture, player_pos, 0, player_scale, WHITE)
        end_drawing()
    
    close_window()

if __name__=="__main__":
    init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Space War")
    main()
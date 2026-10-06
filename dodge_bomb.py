import os
import random
import time  # 1-6：time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool,bool]:  # 練習3
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル(横方向判定結果、縦方向判定結果)
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    black_bg = pg.Surface((WIDTH,HEIGHT))  # 1-1：空のsurface
    black_bg_rct = black_bg.get_rect()
    pg.draw.rect(black_bg, (0, 0, 0), black_bg_rct)  # 1-1：矩形
    black_bg.set_alpha(200)  # 1-2：透明度設定
    fonto = pg.font.Font(None, 100)  # 1-3：文字サイズ
    txt = fonto.render("Game Over", True, (255, 255, 255))  # 1-3：白文字
    black_bg.blit(txt, [WIDTH*(1/3), HEIGHT*(1/2)])  # 1-3：文字貼り付け
    kk_cry_img = pg.image.load("fig/8.png")  # 1-4：こうかとんsurface作成
    black_bg.blit(kk_cry_img, [WIDTH*(3/4),HEIGHT*(1/2)])
    black_bg.blit(kk_cry_img, [WIDTH*(1/4),HEIGHT*(1/2)])
    screen.blit(black_bg, [0, 0])
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() ->tuple[list[pg.Surface], list[int]]:
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (250, 0, 0), (10*r, 10*r), 10*r)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2-1
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)  # 練習2-3
    vx, vy = +5, +5 #練習2-5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # kkとbbのrectが重なっていたら
            print("game over")
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向移動量
                sum_mv[1] += tpl[1]  # 縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこかしらはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 先程の動きをキャンセル
        screen.blit(kk_img, kk_rct)
        # bb_rct.move_ip(vx,vy)  # 練習2-7：爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1

        screen.blit(bb_img,bb_rct)  # 練習2-4：爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

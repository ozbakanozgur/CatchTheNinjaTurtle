import turtle
import random

screen_turtle = turtle.Screen()
screen_turtle.bgcolor("peru")
screen_turtle.title("Catch the Ninja Turtle")
FONT = ("Arial", 24, "normal")                          # Büyük harf değişkenin SABİT (CONSTANT) olduğunu ifade eder.
FONT_MESSAGE = ("Arial", 30, "bold")
TARGET_SCORE = 20                                        # Hedef Puan

# Tam ekran yapmayı kapatma ve pencere boyutu
screen_turtle.setup(width=900, height=600)
cv = screen_turtle.getcanvas()                  # Çizim yapılan alanı (tuvali) al
root = cv.winfo_toplevel()                      # Tuvalin bağlı olduğu ana pencereyi bul
root.resizable(False, False)       # Değişimi Kitle

# Oyun Durumu Değişkenleri
game_over = False
time_left = 20                 # Oyun süresi
level = 1                      # Başlangıç seviyesi
ninja_speed = 750              # Ninjanın kaçma hızı (milisaniye)

# Resim yükleme
image_ninja = "image.gif"
screen_turtle.addshape(image_ninja)

ninja = turtle.Turtle()
ninja.shape(image_ninja)
ninja.penup()             # hareket ederken çizgi çizmesin.
ninja.speed(0)            # en yüksek hız

# Kalem oluşturma fonksiyonu
def create_pen(x, y, color):
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.color(color)
    pen.penup()
    pen.goto(x, y)
    return pen

# Süre, Mesaj, Skor Kalemi
timer_pen = create_pen(330, 260, "gold")
message_pen = create_pen(0, 0, "brown4")
Point = 0
score = create_pen(0, 260, "gold")

# Süreyi güncelleme fonksiyon
def update_timer_display():
    timer_pen.clear()
    timer_pen.write(f"⏳ Time: {time_left}", align="center", font=FONT)
timer_pen.write(f"⏳ Time: {time_left}", align="center", font= FONT)       # Oyun açıldığında ekranda görünsün diye


# Skoru güncelleme fonksiyonu
def update_score_board():
    score.clear()
    score.write(f"🎯 Score: {Point}/{TARGET_SCORE} |🥋 Level: {level}", align="center", font=FONT)


update_score_board()           # Başlangıç puanı ve Level yazdırma.


# Oyun açıktığında başlatma fonksiyonu
def start_game():
    global game_over
    game_over = False

    ninja.showturtle()
    message_pen.clear()  # "Press SPACE" yazısını sil
    # Tuş dinlemeyi kapat
    screen_turtle.onkey(None, "space")

    move_ninja()       # ilk hareketi tetikle
    countdown()        # Sayacı başlat


# Başlangıçta bekleme ayarı
ninja.hideturtle()
message_pen.write("Press SPACE to Start⚔️", align="center", font=FONT_MESSAGE)

screen_turtle.onkey(start_game, "space")
screen_turtle.listen()


# Hareket etme fonksiyonu
def move_ninja():
    if game_over: return          # Oyun bittiyse dur
    if not screen_turtle: return  # Oyun kapatıldığında işlemi durdur

    new_x = random.randint(-400, 400)  # yatayda random
    new_y = random.randint(-250, 230)  # dikeyde random
    ninja.goto(new_x, new_y)  # Belirlenen yere ışınla


    screen_turtle.ontimer(move_ninja, ninja_speed)  # ninja_speed ms kadar bekle ve tekrar hareket et. (Döngü)


# Tıklama Fonksiyonu
# (x, y) Zorunludur, tıklanan yerin koordinatlarını gönderir
def click_the_ninja(x, y):
    if game_over: return  # Oyun bittiyse puan alma

    global Point
    Point += 1       # Puanı 1 arttır
    update_score_board()


# Kaybederse Tekrar başlatma fonksiyonu
def restart_game():
    global game_over, time_left, Point, level, ninja_speed
    # Level 1 ayarlarına dön
    game_over = False
    time_left = 20
    Point = 0
    if level == 1:
        ninja_speed = 750
    elif level == 2:
        ninja_speed = 500

    # Ekran temizlikleri
    message_pen.clear()
    update_score_board()
    update_timer_display()

    ninja.showturtle()   # Ninjayı tekrar göster

    screen_turtle.onkey(None, "space")  # Tuşu dinlemeyi kapat
    # Döngüleri baştan başlat
    move_ninja()
    countdown()


# Level 2'ye Geçiş Fonksiyonu
def start_level_2():
    # İZİN İSTİYORUZ: "Bu değişkenlerin orijinallerini değiştireceğim"
    global time_left, Point, level, ninja_speed, game_over

    screen_turtle.onkey(None, "space")   # Tuşu dinlemeyi kapat

    level = 2              # yazı için
    time_left = 20        # Süreyi sıfırla
    Point = 0              # Puanı sıfırla
    ninja_speed = 500       # HIZI ARTTIR
    game_over = False        # Oyunu tekrar aktif et

    ninja.showturtle()        # Ninjayı görünür yap

    # Ekranı temizle ve güncelle
    message_pen.clear()       # Eski bildirimleri temizle
    update_score_board()
    update_timer_display()

    # Döngüleri tekrar başlat
    move_ninja()             # Haraket başlar
    countdown()              # zaman 20den geriye sayar


# Geri Sayım ve Oyun Kontrolü
def countdown():
    global time_left, game_over, level

    if time_left > 0:             # Zaman bitmemişse çalıştır
        time_left -= 1           # Süreyi azaltır
        update_timer_display()
        screen_turtle.ontimer(countdown, 1000)  # Her saniye bir döngü oluşur
    else:
        # Süre bittiğinde çalışır
        game_over = True
        timer_pen.clear()     # Sayacı temizle

        # Kazanma Kontrolü
        if Point >= TARGET_SCORE:
            if level == 1:     # 2. seviyeye hazırlık
                ninja.hideturtle()       # sakla ( Yazı için)
                message_pen.write("Great job! 👍\nPress SPACE for Level 2 🚀", align="center", font=FONT_MESSAGE)
                screen_turtle.onkey(start_level_2, "space")
                screen_turtle.listen()
            else:       # seviye 1 bittiyse kazanmıştır
                message_pen.write("You Won! 🏆\nYou're a Ninja! 🥷✨", align="center", font=FONT_MESSAGE)
        else:          # süre bittiğinde puan 20'den azsa.
            ninja.hideturtle()
            message_pen.write(f"GAME OVER!😢\nDon't give up!: {Point}\nPress SPACE to Restart", align="center", font=FONT_MESSAGE)
            # restart_game fonksiyonunu çalıştır
            screen_turtle.onkey(restart_game, "space")
            screen_turtle.listen()   # Klavyeyi dinlemeye başla

ninja.onclick(click_the_ninja)  # Ninjaya tıkladığında çalıştır

turtle.mainloop()
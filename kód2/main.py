import pygame 
from os.path import join
from random import randint, uniform

# globális változók
futás = True
pontszám = 0  # Hozzáadva

class Játékos(pygame.sprite.Sprite):
    def __init__(self, csoportok):
        super().__init__(csoportok)
        self.image = pygame.image.load(join('mindenjáték', 'Második', 'image', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.irány = pygame.Vector2()
        self.sebesség = 300

        # várakozási idő 
        self.tud_lőni = True
        self.lézer_lövés_ideje = 0
        self.várakozási_idő = 350

        # maszk 
        self.maszk = pygame.mask.from_surface(self.image)
    
    def lézer_időzítő(self):
        if not self.tud_lőni:
            aktuális_idő = pygame.time.get_ticks()
            if aktuális_idő - self.lézer_lövés_ideje >= self.várakozási_idő:
                self.tud_lőni = True

    def update(self, dt):
        gombok = pygame.key.get_pressed()
        self.irány.x = int(gombok[pygame.K_RIGHT]) - int(gombok[pygame.K_LEFT])
        self.irány.y = int(gombok[pygame.K_DOWN]) - int(gombok[pygame.K_UP])  
        self.irány = self.irány.normalize() if self.irány else self.irány 
        self.rect.center += self.irány * self.sebesség * dt

        legutóbbi_gombok = pygame.key.get_pressed()
        if legutóbbi_gombok[pygame.K_SPACE] and self.tud_lőni:
            Lézer(lézer_kép, self.rect.midtop, (összes_sprite, lézer_spritek)) 
            self.tud_lőni = False
            self.lézer_lövés_ideje = pygame.time.get_ticks()
            '''lézer_hang.play()'''
        
        self.lézer_időzítő()

class Csillag(pygame.sprite.Sprite):
    def __init__(self, csoportok, surf):
        super().__init__(csoportok)
        self.image = surf
        self.rect = self.image.get_rect(center = (randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)))
        
class Lézer(pygame.sprite.Sprite):
    def __init__(self, surf, pos, csoportok):
        super().__init__(csoportok)
        self.image = surf 
        self.rect = self.image.get_rect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, csoportok):
        super().__init__(csoportok)
        self.eredeti_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.kezdő_idő = pygame.time.get_ticks()
        self.élettartam = 3000
        self.irány = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.sebesség = randint(400, 500)
        self.elfordulási_sebesség = randint(40, 60)
        self.elfordulás = 0
    
    def update(self, dt):
        self.rect.center += self.irány * self.sebesség * dt
        if pygame.time.get_ticks() - self.kezdő_idő >= self.élettartam:
            self.kill()
        self.elfordulás += self.elfordulási_sebesség * dt
        self.kép = pygame.transform.rotozoom(self.eredeti_surf, self.elfordulás, 1)
        self.rect = self.kép.get_rect(center = self.rect.center)

class Különleges_Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, csoportok):
        super().__init__(csoportok)
        self.eredeti_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.kezdő_idő = pygame.time.get_ticks()
        self.élettartam = 3000
        self.irány = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.sebesség = randint(400, 500)
        self.elfordulási_sebesség = randint(40, 80)
        self.elfordulás = 0
    
    def update(self, dt):
        self.rect.center += self.irány * self.sebesség * dt
        if pygame.time.get_ticks() - self.kezdő_idő >= self.élettartam:
            self.kill()
        self.elfordulás += self.elfordulási_sebesség * dt
        self.kép = pygame.transform.rotozoom(self.eredeti_surf, self.elfordulás, 1)
        self.rect = self.kép.get_rect(center = self.rect.center)

class AnimáltRobbanás(pygame.sprite.Sprite):
    def __init__(self, keretek, pos, csoportok):
        super().__init__(csoportok)
        self.keretek = keretek
        self.kép_index = 0
        self.image = self.keretek[self.kép_index]
        self.rect = self.image.get_rect(center = pos)
        '''robbanás_hang.play()'''
    
    def update(self, dt):
        self.kép_index += 20 * dt
        if self.kép_index < len(self.keretek):
            self.image = self.keretek[int(self.kép_index)]
        else:
            self.kill()

def ütközések():
    global futás, pontszám  # Frissítve

    ütköző_spritek = pygame.sprite.spritecollide(játékos, meteor_spritek, True, pygame.sprite.collide_mask)
    if ütköző_spritek:
        futás = False
    
    for lézer in lézer_spritek:
        ütközött_spritek = pygame.sprite.spritecollide(lézer, meteor_spritek, True)
        if ütközött_spritek:
            lézer.kill()
            pontszám += 10  # Pontszám növelése meteornál
            AnimáltRobbanás(robbanás_keretek, lézer.rect.midtop, összes_sprite)

        ütközött_különleges_spritek = pygame.sprite.spritecollide(lézer, különleges_meteor_spritek, True)
        if ütközött_különleges_spritek:
            lézer.kill()
            pontszám += 50  # Pontszám növelése különleges meteornál
            AnimáltRobbanás(robbanás_keretek, lézer.rect.midtop, összes_sprite)

def kijelző_eredmény():
    aktuális_idő = pygame.time.get_ticks() // 100
    szöveg_surf = betű.render(str(aktuális_idő), True, (240,240,240))
    pontszám_surf = betű.render(f'Pontszám: {pontszám}', True, (240, 240, 240))  # Pontszám kiírása
    szöveg_rect = szöveg_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    pontszám_rect = pontszám_surf.get_rect(midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))

    display_surface.blit(szöveg_surf, szöveg_rect)
    display_surface.blit(pontszám_surf, pontszám_rect)  # Pontszám megjelenítése
    pygame.draw.rect(display_surface, (240,240,240), szöveg_rect.inflate(20,10).move(0,-8), 5, 10)

# Irányítási útmutató kijelzése
def irányítás_kijelzése():
    # Irányítási útmutató szövege
    útmutató = [
        "Mozgás: Nyilak",
        "Lövés: Space",
    ]
    
    # Szöveg renderelése és kirajzolása
    for i, szöveg in enumerate(útmutató):
        szöveg_surf = betű.render(szöveg, True, (240, 240, 240))
        szöveg_rect = szöveg_surf.get_rect(topleft=(10, 10 + i * 40))
        display_surface.blit(szöveg_surf, szöveg_rect)

# általános beállítás 
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Űrlövöldözős játék')
óra = pygame.time.Clock()

# importálás
csillag_kép = pygame.image.load(join('mindenjáték', 'Második' ,'image', 'csillag_kép.png')).convert_alpha()
meteor_kép = pygame.image.load(join('mindenjáték', 'Második', 'image', 'meteor.png')).convert_alpha()
lézer_kép = pygame.image.load(join('mindenjáték', 'Második', 'image', 'lézer.png')).convert_alpha()
betű = pygame.font.Font(join('mindenjáték', 'Második', 'image', 'Oxanium-Bold.ttf'), 40)
különleges_meteor_kép = pygame.image.load(join('mindenjáték', 'Második', 'image', 'különleges_meteor.png')).convert_alpha()
robbanás_keretek = [pygame.image.load(join('mindenjáték', 'Második', 'image', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
'''
lézer_hang = pygame.mixer.Sound(join('mindenjáték', 'Második', 'audio', 'lézer.wav'))
lézer_hang.set_volume(0.02)
robbanás_hang = pygame.mixer.Sound(join('mindenjáték', 'Második', 'audio', 'explosion.wav'))
robbanás_hang.set_volume(0.02)
játék_zene = pygame.mixer.Sound(join('mindenjáték', 'Második', 'audio', 'game_music.wav'))
játék_zene.play(loops= -1)
játék_zene.set_volume(0.04)
#játék_zene.play(loops= -1)
'''
# sprite-ok 
összes_sprite = pygame.sprite.Group()
meteor_spritek = pygame.sprite.Group()
lézer_spritek = pygame.sprite.Group()
különleges_meteor_spritek = pygame.sprite.Group()
for i in range(20):
    Csillag(összes_sprite, csillag_kép) 
játékos = Játékos(összes_sprite)

# egyedi esemény -> meteor esemény
meteor_esemény = pygame.event.custom_type()
különleges_meteor_esemény = pygame.event.custom_type()

# Időzítők a meteorokhoz
pygame.time.set_timer(meteor_esemény, 200)
pygame.time.set_timer(különleges_meteor_esemény, 5000)  # 5 másodpercenként különleges meteor

while futás:
    dt = óra.tick() / 1000
    # esemény ciklus
    for esemény in pygame.event.get():
        if esemény.type == pygame.QUIT:
            futás = False
        if esemény.type == meteor_esemény:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_kép, (x, y), (összes_sprite, meteor_spritek))

        if esemény.type == különleges_meteor_esemény:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Különleges_Meteor(különleges_meteor_kép, (x, y), (összes_sprite, különleges_meteor_spritek))
    
    # Frissítés
    összes_sprite.update(dt)
    ütközések()  # Események frissítése
    
    # Játék kirajzolása
    display_surface.fill('#3a2e3f')
    kijelző_eredmény()
    összes_sprite.draw(display_surface)

    # Irányítási útmutató kirajzolása
    irányítás_kijelzése()

    pygame.display.update()

pygame.quit()

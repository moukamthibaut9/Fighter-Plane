import pygame, sys
from random import randint

pygame.init()

taille_ecran=(L_ecran,H_ecran)=(1350,700)
nbr_cell_x,nbr_cell_y=130,70
dim_cell_x,dim_cell_y=L_ecran/nbr_cell_x,H_ecran/nbr_cell_y
taille_fenetre=(L_fenetre,H_fenetre)=nbr_cell_x*dim_cell_x,nbr_cell_y*dim_cell_y
if L_fenetre>=H_fenetre: parametre_taille_police=dim_cell_y
else: parametre_taille_police=dim_cell_x
ticks_per_sec=1000

image_1=pygame.image.load("terrain2.jpg") ###
img_terrain=pygame.transform.scale(image_1,(L_fenetre,H_fenetre))
image_2=pygame.image.load("Avion3.png")   ###
img_avion=image_2.subsurface((26,108,446,170))
img_avion=pygame.transform.scale(img_avion,(16*dim_cell_x,10*dim_cell_y))
img_balle=image_2.subsurface((232,21,73,25))
img_balle=pygame.transform.scale(img_balle,(8*dim_cell_x,3*dim_cell_y))
image_3=pygame.image.load("Oiseau2.png")
rects_oiseaux=[(72,93,429,300),(618,128,429,268),(75,722,429,329),(618,728,429,226)]
dico_images_oiseaux={}
for rect in rects_oiseaux:
    sous_image=rects_oiseaux.pop(0)
    sous_image=image_3.subsurface(sous_image)
    sous_image=pygame.transform.scale(sous_image,(5*dim_cell_x,4*dim_cell_y))
    sous_image=pygame.transform.flip(sous_image,True,False)
    rects_oiseaux.append(sous_image)
dico_images_oiseaux["voler"]=rects_oiseaux
    
image_4=pygame.image.load("Multi-Perso1.png")
img_collision=image_4.subsurface((534,1843,165,203))
img_collision=pygame.transform.scale(img_collision,(dim_cell_x*6,dim_cell_y*5))

song1=pygame.mixer.Sound("Door.wav")
song2=pygame.mixer.Sound("Splash.wav")
pygame.mixer.music.load("Naruto1.mp3")
pygame.mixer.music.queue("fairy_tail.mp3")

fenetre_jeu=pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Apprentissage_Pygame2")


class Terrain:
    def __init__(self):
        self.rect_terrain=pygame.Rect(0,0,L_fenetre,H_fenetre)
    def dessin_terrain(self):
        fenetre_jeu.blit(img_terrain,self.rect_terrain)
        pygame.draw.rect(fenetre_jeu,pygame.Color("white"),self.rect_terrain,10)

class Avion:
    def __init__(self):
        self.rect_avion=pygame.Rect(0,0,16*dim_cell_x,10*dim_cell_y)
        self.direction_avion=[1,1]
    def dessin_avion(self):
        #pygame.draw.rect(fenetre_jeu,pygame.Color("blue"),self.rect_avion)
        fenetre_jeu.blit(img_avion,self.rect_avion)
    def deplacement_avion(self,vitesse_avion):
        if self.rect_avion.right>=L_fenetre/5 and self.direction_avion[0]==1: self.direction_avion[0]=-1
        elif self.rect_avion.left<=0 and self.direction_avion[0]==-1: self.direction_avion[0]=1
        if self.rect_avion.bottom>=H_fenetre and self.direction_avion[1]==1: self.direction_avion[1]=-1
        elif self.rect_avion.top<=0 and self.direction_avion[1]==-1: self.direction_avion[1]=1
        self.rect_avion.x+=self.direction_avion[0]*vitesse_avion/3
        self.rect_avion.y+=self.direction_avion[1]*vitesse_avion/5

class Balle:
    def __init__(self):
        self.rect_balle=pygame.Rect(0,0,8*dim_cell_x,3*dim_cell_y)
        self.direction_balle=0
    def dessin_deplacement_balle(self,vitesse_balle,pox_balle_x,pox_balle_y):
        if self.rect_balle.right<L_fenetre and self.direction_balle==1: 
            self.rect_balle.x+=vitesse_balle
            self.rect_balle.y=pox_balle_y
            fenetre_jeu.blit(img_balle,self.rect_balle)
            #pygame.draw.rect(fenetre_jeu,pygame.Color("black"),self.rect_balle)
        else: 
            self.direction_balle=0
            self.rect_balle.x=pox_balle_x


class Enemies:
    def __init__(self):
        self.rect_enemies=[
            pygame.Rect(dim_cell_x*(nbr_cell_x-7),dim_cell_y*randint(1,12),dim_cell_x*5,dim_cell_y*4),
            pygame.Rect(dim_cell_x*(nbr_cell_x-7),dim_cell_y*randint(17,29),dim_cell_x*5,dim_cell_y*4),
            pygame.Rect(dim_cell_x*(nbr_cell_x-7),dim_cell_y*randint(34,45),dim_cell_x*5,dim_cell_y*4),
            pygame.Rect(dim_cell_x*(nbr_cell_x-7),dim_cell_y*randint(50,65),dim_cell_x*5,dim_cell_y*4),
        ]
        self.image_enemie_index=0
    def dessin_enemies(self):
        if self.image_enemie_index>=len(dico_images_oiseaux["voler"]):
            self.image_enemie_index=0
        for enemie in self.rect_enemies:
            #pygame.draw.rect(fenetre_jeu,pygame.Color("red"),enemie)
            fenetre_jeu.blit(dico_images_oiseaux["voler"][self.image_enemie_index],enemie)
        self.image_enemie_index+=1
        pygame.time.delay(40)
            
class Game:
    def __init__(self):
        self.terrain=Terrain()
        self.avion=Avion()
        self.balle=Balle()
        self.enemies=Enemies()
        self.score=0
        self.traceur_score=1
        self.fin_partie=False
        self.temps_critique1=pygame.time.get_ticks()//ticks_per_sec
        self.temps_critique2=0
        pygame.mixer.music.play()
    def dessin_elements(self):
        self.terrain.dessin_terrain()
        self.avion.rect_avion.clamp_ip(self.terrain.rect_terrain)
        self.avion.dessin_avion()
        self.enemies.dessin_enemies()
    def deplacement_avion_balle(self):
        self.avion.deplacement_avion(25)
        self.balle.dessin_deplacement_balle(40,self.avion.rect_avion.left+self.avion.rect_avion.width/4,self.avion.rect_avion.top+game.avion.rect_avion.height/2)
    def colision_balle_enemie(self):
        for enemie in self.enemies.rect_enemies:
            if self.balle.rect_balle.colliderect(enemie):
                self.enemies.rect_enemies.remove(enemie)
                self.score+=1
                song2.play()
                fenetre_jeu.blit(img_collision,enemie)
                pygame.time.delay(50)
                
    def afficher_texte(self,texte,police,taille,couleur,position):
        police=pygame.font.SysFont(police,taille,bold=True)
        texte=police.render(texte,True,couleur)
        fenetre_jeu.blit(texte,position)
    def verification_marge_temps(self):
        self.temps_critique2=pygame.time.get_ticks()//ticks_per_sec
        if (self.temps_critique2-self.temps_critique1)%60==0 and self.score>=15*self.traceur_score:
            self.traceur_score+=1
        elif (self.temps_critique2-self.temps_critique1)%60>=59 and self.score<15*self.traceur_score:
            self.fin_partie=True



pygame.time.set_timer(pygame.USEREVENT,5000)


game=Game()
lancer=True
while lancer:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            lancer=False
        if event.type==pygame.USEREVENT:
            game.enemies=Enemies()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                game.balle.direction_balle=1
                if game.balle.rect_balle.centerx<game.avion.rect_avion.right: song1.play()
    

    if game.fin_partie==True:
        reprendre_partie=False
        pygame.mixer.music.stop()
        while reprendre_partie==False:
            fenetre_jeu.fill((0,0,0))
            game.afficher_texte("Partie Terminé! Une minute sans rapporter au moins 15 points","arial",3*int(parametre_taille_police),pygame.Color("white"),(5*dim_cell_x,35*dim_cell_y))
            game.afficher_texte("Appuiyer sur 'R' pour recommencer ou 'Q' pour quitter.","arial",2*int(parametre_taille_police),pygame.Color("white"),(25*dim_cell_x,38*dim_cell_y))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    lancer=False
                    reprendre_partie=True
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        lancer=False
                        reprendre_partie=True
                    elif event.key==pygame.K_r:
                        game=Game()
                        reprendre_partie=True

            
    fenetre_jeu.fill(pygame.Color("gray"))
    game.dessin_elements()
    game.deplacement_avion_balle()
    game.colision_balle_enemie()
    game.verification_marge_temps()
    game.afficher_texte("SCORE : {}".format(game.score),"times-new-roman",20,pygame.Color("maroon"),(40*dim_cell_x,2*dim_cell_y))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.Clock().tick(100)

pygame.quit()
sys.exit()

import pygame
from random import randint

pygame.init()

# None = ei aloitettu, True = käynnissä, False = hävitty
pelin_tila = None

sanat = ["kuvat\peruslaatta.png",
         "kuvat\ykkönen.png",
         "kuvat\kakkonen.png",
         "kuvat\kolmonen.png",
         r"kuvat\nelonen.png",
         r"kuvat\vitonen.png",
         "kuvat\kutonen.png",
         "kuvat\seiska.png",
         "kuvat\kasi.png",
         "kuvat\miina.png",
         "kuvat\AvattuTyhjä.png"
         ]

kuvat = []

# Lisää kaikki tarvittavat kuvat yhteen listaan
for i in sanat:
    kuvat.append(pygame.image.load(i))

fontti_iso = pygame.font.SysFont("Helvetica", 100)
fontti_pieni = pygame.font.SysFont("Helvetica", 30)

blokki_koko = kuvat[10].get_height()

naytto_leveys = 32 * blokki_koko
naytto_korkeus = 19 * blokki_koko
klikkaus_sijainti = (-1, -1)

naytto = pygame.display.set_mode((naytto_leveys, naytto_korkeus))

# 0=avaamaton, 1-8=vastaavat numerolaatat, 9=miina, 10=avattu tyhjä luukku
ruudukko = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# Palauttaa True, jos jäljellä ei ole yhtään avaamattomia luukkuja, eli peli on voitettu
def voiton_havaitsija():
    for i in ruudukko:
        if 0 in i:
            return False
    return True


# Arpoo miinakentän siten, että parametreinä annetun alkupisteen ympärillä on vähintään 3 X 3 miinaton alue.
def miina_arpoja(ei_x: int, ei_y: int):
    maara = 0

    # "Kielletyn" alueen koordinaatit lisätään tupleina tähän listaan
    kielletty_alue = []

    # Ottaa huomioon tapauksen jossa aloitus on ylä- tai alarivillä ja poistaa ne indeksit.
    alku_y = -1
    loppu_y = 2
    if ei_y == 0:
        alku_y = 0
    elif ei_y == 15:
        loppu_y = 1

    # Kirjaa listoihin ylös kielletyt koordinaatit
    for i in range(alku_y, loppu_y):
        for j in range(-1, 2):
            if ei_x == 0 and j == -1:
                continue
            if ei_x == 29 and j == 1:
                continue
            kielletty_alue.append((ei_x + j, ei_y + i))

    # Lisää 100 miinaa satunnaisesti kielletyn alueen ulkopuolelle.
    while maara < 99:
        y, x = randint(0, 15), randint(0, 29)
        if ruudukko[y][x] == 0 and ((x, y) not in kielletty_alue):
            ruudukko[y][x] = 9
            maara += 1


# Määrittää mikä laattatyyppi kuuluu parametreina annettuihin koordinaatteihin.
def numeroiden_maaritys(x: int, y: int):
    maara = 0
    alku_y = -1
    loppu_y = 2
    if y == 0:
        alku_y = 0
    elif y == 15:
        loppu_y = 1

    # Laskee miinojen määrän 3X3 alueelta klikkauksen ympäriltä.
    for i in range(alku_y, loppu_y):
        for j in range(-1, 2):
            if x == 0 and j == -1:
                continue
            if x == 29 and j == 1:
                continue
            if ruudukko[y + i][x + j] == 9:
                maara += 1

    return maara


# Avaa isot tyhjät alueet automaattisesti kun jokin sen luukuista avataan.
def alue_siivous():
    vanha_ruudukko = [rivi[:] for rivi in ruudukko]
    muutos = False
    for y in range(0, 16):
        for x in range(0, 30):
            # Tarkistaa 3X3 alueelta vain avattujen tyhjien ruutujen ympäriltä
            if ruudukko[y][x] == 10:
                alku_y = -1
                loppu_y = 2
                if y == 0:
                    alku_y = 0
                elif y == 15:
                    loppu_y = 1

                # Määrittää viereisten pommien määrän yhdessä koordinaatissa kerrallaan.
                loyty = []
                seuraava = False
                for i in range(alku_y, loppu_y):
                    if seuraava:
                        break
                    for j in range(-1, 2):
                        if x == 0 and j == -1:
                            continue
                        if x == 29 and j == 1:
                            continue
                        numero = numeroiden_maaritys(x + j, y + i)
                        loyty.append(numero)

                        # Jos avaamaton pommi löytyi, jätetään tämä ruutu huomioimatta
                        # ja siirrytään seuraavaan alueeseen.
                        if 9 in loyty:
                            seuraava = True
                            break

                        # Päivittää ruutujen tilat oikeiksi
                        ruutu = numeroiden_maaritys(x + j, y + i)
                        if ruutu != 0:
                            ruudukko[y + i][x + j] = ruutu
                        else:
                            ruudukko[y + i][x + j] = 10

                if ruudukko != vanha_ruudukko and not muutos:
                    muutos = True

    # Jos läpäisykierroksella on tehty muutoksia ruudukkoon,
    # kutsutaan funktiota uudestaan rekursiivisesti.
    if muutos:
        alue_siivous()

# Valmistelee ruudukon sekä päivittää sitä pellin edetessä
def ruudukon_manipulointi(ruudukko: list, kohta: tuple):
    global pelin_tila

    # Aloittaa pelin, kun jotain ruutua klikataan hiirellä
    if pelin_tila == None and (32 < kohta[0] < 992) and (64 < kohta[1] < 578):
        ei_x = int((kohta[0] - 32) / 32)
        ei_y = int((kohta[1] - 64) / 32)
        miina_arpoja(ei_x, ei_y)
        pelin_tila = True

    # Jos peli ei ole käynnissä, piiretään tyhjä ruudukko
    elif pelin_tila == None:
        for y in range(len(ruudukko)):
            for x in range(len(ruudukko[y])):
                naytto.blit(kuvat[ruudukko[y][x]], (blokki_koko * (1 + x), blokki_koko * (2 + y)))

    # Päivittää ruudukkoa pelin edetessä ja piirtää sen
    for y in range(len(ruudukko)):
        if not pelin_tila:
            break
        for x in range(len(ruudukko[y])):
            if ruudukko[y][x] == 0 or ruudukko[y][x] == 9:
                if (blokki_koko * (1 + x)) <= kohta[0] < (blokki_koko * (1 + x) + blokki_koko) and blokki_koko * (
                        2 + y) <= kohta[1] < blokki_koko * (2 + y) + blokki_koko:
                    if ruudukko[y][x] == 0:
                        maara = numeroiden_maaritys(x, y)
                        if maara != 0:
                            ruudukko[y][x] = maara
                            naytto.blit(kuvat[maara], (blokki_koko * (1 + x), blokki_koko * (2 + y)))
                        else:
                            ruudukko[y][x] = 10
                            alue_siivous()
                            naytto.blit(kuvat[10], (blokki_koko * (1 + x), blokki_koko * (2 + y)))

                    elif ruudukko[y][x] == 9:
                        pelin_tila = False
                        break

                elif ruudukko[y][x] == 9:
                    naytto.blit(kuvat[0], (blokki_koko * (1 + x), blokki_koko * (2 + y)))
                else:
                    naytto.blit(kuvat[0], (blokki_koko * (1 + x), blokki_koko * (2 + y)))

            else:
                naytto.blit(kuvat[ruudukko[y][x]], (blokki_koko * (1 + x), blokki_koko * (2 + y)))

    return pelin_tila


while True:
    uusi_peli = False
    naytto.fill((100, 0, 0))
    ohjeet_esc = fontti_pieni.render("Poistu pelistä: esc", True, (255, 0, 0))
    naytto.blit(ohjeet_esc, (10, 0))

    # Kerää annettuja inputteja
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()

        if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
            klikkaus_sijainti = tapahtuma.pos

        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_ESCAPE:
                exit()

        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_SPACE:
                uusi_peli = True

    # Kun peli hävitään
    if ruudukon_manipulointi(ruudukko, klikkaus_sijainti) == False:
        for y in range(len(ruudukko)):
            for x in range(len(ruudukko[y])):
                naytto.blit(kuvat[ruudukko[y][x]], (blokki_koko * (1 + x), blokki_koko * (2 + y)))

        teksti = fontti_iso.render("Hävisit!", True, (255, 0, 0))
        teksti3 = fontti_iso.render("Uusi peli: space", True, (255, 0, 0))
        naytto.blit(teksti, ((naytto_leveys - teksti.get_width()) / 2, (naytto_korkeus - teksti.get_height()) / 2))
        naytto.blit(teksti3,
                    ((naytto_leveys - teksti3.get_width()) / 2, (200 + naytto_korkeus - teksti3.get_height()) / 2))
        if uusi_peli:
            ruudukko = [[0 for i in range(30)] for j in range(16)]
            klikkaus_sijainti = (-1, -1)
            pelin_tila = None

    # Kun peli voitetaan
    if pelin_tila:
        voitto = voiton_havaitsija()
        if voitto:
            fontti2 = pygame.font.SysFont("Helvetica", 100)
            teksti2 = fontti_iso.render("Voitit!", True, (255, 0, 0))
            teksti3 = fontti_iso.render("Uusi peli: space", True, (255, 0, 0))
            naytto.blit(teksti2,
                        ((naytto_leveys - teksti2.get_width()) / 2, (naytto_korkeus - teksti2.get_height()) / 2))
            naytto.blit(teksti3,
                        ((naytto_leveys - teksti3.get_width()) / 2, (200 + naytto_korkeus - teksti3.get_height()) / 2))

            if uusi_peli:
                pelin_tila = None

    pygame.display.flip()
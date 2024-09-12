import os

from pdf2image import convert_from_path

NB_PIX_ALLOWED = 30
NB_ROWS = 2
NB_COLS = 3


def get_margins(image):  # (left, top, right, bottom)
    width, height = image.size
    pix = image.load()
    left, top, right, bottom = -1, -1, -1, -1

    for x in range(width):
        counter = 0  # permet de tolérer les lignes noires de découpage
        for y in range(height):
            if pix[x, y][:3] != (255, 255, 255):  # Canal alpha ATTENTION!!  (255,255,255,...)
                counter += 1
                if 0 > counter > NB_PIX_ALLOWED:
                    """ Ici je souhaite modifier la fonction pour que s'il y a des petites marques noir 
                    (0 > counter > NB_PIX_ALLOWED), on note une marge ou une division """
                    left = x
                    break
        if left >= 0:
            break

    for x in range(width - 1, left, -1):
        counter = 0
        for y in range(height):
            if pix[x, y][:3] != (255, 255, 255):
                counter += 1
                if counter > NB_PIX_ALLOWED:
                    right = x
                    break
        if right >= 0:
            break

    for y in range(height):
        counter = 0
        for x in range(width):
            if pix[x, y][:3] != (255, 255, 255):
                counter += 1
                if counter > NB_PIX_ALLOWED:
                    top = y
                    break
        if top >= 0:
            break

    for y in range(height - 1, top, -1):
        counter = 0
        for x in range(width):
            if pix[x, y][:3] != (255, 255, 255):
                counter += 1
                if counter > NB_PIX_ALLOWED:
                    bottom = y
                    break
        if bottom >= 0:
            break

    return left, top, right + 1, bottom + 1


card_list = []

# Je converti le pdf en une liste d'image
# pdf_path = 'ressources/pdf/Unlock ! Tutoriel.pdf'
pdf_path = 'ressources/pdf/Unlock_Spirou_PNP_A4.pdf'
pages_stream = convert_from_path(pdf_path, 500, poppler_path=r"C:/Users/CelineLucas/PycharmProjects"
                                                             "/downloaded_libraries/poppler-24.07.0"
                                                             "/Library/bin")
# Je crée le répertoire de stockage
directory = pdf_path[:-4]
try:
    os.mkdir(directory)
except FileExistsError:
    for file in os.listdir(directory):
        os.remove(directory + '/' + file)

# Je recupère les marges:
margins = get_margins(pages_stream[0])


# Je voudrais m'appuyer sur les traits noirs pour diviser ma page

# Je rogne les bords blancs
for i in range(len(pages_stream)):
    pages_stream[i] = pages_stream[i].crop(margins)

page_width, page_height = pages_stream[0].size
card_width, card_height = page_width / NB_COLS, page_height / NB_ROWS

counter = 0
for page in pages_stream:
    # Je divise la page en 6:
    for y in range(NB_ROWS):
        for x in range(NB_COLS):
            image = page.crop((x * card_width, y * card_height, (x + 1) * card_width, (y + 1) * card_height))
            card_list.append(image)

            # Je sauvegarde :
            image.save(directory + "/image" + str(counter) + ".jpg", 'JPEG')

            counter += 1

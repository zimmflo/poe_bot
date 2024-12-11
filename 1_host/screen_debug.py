
from utils.gamehelper import PoeBot, Entity
import matplotlib.pyplot as plt
import cv2


UNIQUE_ID = '123'
REMOTE_IP = '172.123.123.123'

poe_bot = PoeBot(unique_id=UNIQUE_ID, remote_ip = REMOTE_IP)

poe_bot.bot_controls.restartScript()
poe_bot.refreshAll()
input("press smth to take screen")
game_img = poe_bot.getImage()
cv2.imwrite('./inventory_and_chest_opened.bmp', game_img)
print('game_img')
plt.imshow(game_img);plt.show()
input("partial screen")
plt.imshow(game_img[531-20:531+20, 490-20:490+20]);plt.show()


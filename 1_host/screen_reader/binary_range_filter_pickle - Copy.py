import cv2
import numpy as np
import pickle

if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow( "result" ) # создаем главное окно
cv2.namedWindow( "original" ) # создаем главное окно
cv2.namedWindow( "settings",cv2.WINDOW_NORMAL ) # создаем окно настроек
cv2.resizeWindow('result', 300, 300)
cv2.resizeWindow('original', 300, 300)


# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('threshhold_min', 'settings', 0, 255, nothing)
cv2.createTrackbar('threshhold_max', 'settings', 255, 255, nothing)
crange = [0,0,0, 0,0,0]

f = open('./blue_drops.pickle', 'rb')
# dict_keys(['minimap_initial', 'minimap_0', 'minimap_225', 'minimap_270'])
loaded_minimaps = pickle.load(f)
f.close()
img = loaded_minimaps
# img = cv2.medianBlur(img,3)
while True:
    
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
   


 
    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('threshhold_min', 'settings')
    h2 = cv2.getTrackbarPos('threshhold_max', 'settings')

    # формируем начальный и конечный цвет фильтра
    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h1, h2)

    cv2.imshow('result', thresh) 
    cv2.imshow('original', img) 
 
    ch = cv2.waitKey(5)
    if ch == 27:
        break

cv2.destroyAllWindows()
import cv2, numpy as np
src = cv2.imread('/root/.claude/uploads/15e9b8bd-6042-5d1d-b51f-045396c3a676/91101af1-image.jpg')
img = src.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
H,W = gray.shape
# large bright regions (letters, paper) -> protect
bright = (gray > 150).astype(np.uint8)*255
large = cv2.morphologyEx(bright, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
large = cv2.dilate(large, np.ones((3,3),np.uint8))
# thin bright strokes
toph = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, cv2.getStructuringElement(cv2.MORPH_RECT,(9,9)))
thin = ((toph > 35) & (gray > 110)).astype(np.uint8)*255
boxes = [(190,25,995,92),(600,260,1010,335),(140,600,620,800),(605,900,1065,1040),(320,1130,800,1300),(218,1440,955,1605)]
mask = np.zeros_like(gray)
for x0,y0,x1,y1 in boxes:
    m = thin[y0:y1,x0:x1].copy()
    m[large[y0:y1,x0:x1]>0] = 0
    mask[y0:y1,x0:x1] = m
mask = cv2.dilate(mask, np.ones((5,5),np.uint8))
for x0,y0,x1,y1 in [(436,1138,492,1172),(596,1136,660,1172),(596,1196,660,1232),(548,560,600,642)]: mask[y0:y1,x0:x1]=255
# title block + bars: whole-area except letter A region (x<560)
tb = np.zeros_like(gray); tb[392:672, 572:1100] = 255

mask = cv2.bitwise_or(mask, tb)
cv2.imwrite('mask.png', mask)
out = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
cv2.imwrite('clean.png', out)
cv2.imwrite('clean_small.jpg', cv2.resize(out,(590,804)))

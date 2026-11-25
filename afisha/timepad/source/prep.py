import cv2, numpy as np
src = cv2.imread('/root/.claude/uploads/15e9b8bd-6042-5d1d-b51f-045396c3a676/91101af1-image.jpg')
clean = cv2.imread('clean.png')
def paper_cut(img, box, name, thr=135):
    x0,y0,x1,y1 = box
    crop = img[y0:y1,x0:x1].copy()
    g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    m = (g>thr).astype(np.uint8)*255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    cnts,_ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = [c for c in cnts if cv2.contourArea(c) > 0.05*m.size]
    full = np.zeros_like(m); cv2.drawContours(full, cnts, -1, 255, -1)
    full = cv2.erode(full, np.ones((3,3),np.uint8))
    full = cv2.GaussianBlur(full,(3,3),0)
    rgba = np.dstack([crop, full])
    cv2.imwrite(name, rgba)
    return full
# logo papers (bottom-left) and decorative papers
lm = paper_cut(src, (40,1278,225,1605), 'logo.png')
paper_cut(src, (405,135,585,235), 'paper_top.png')
pm = paper_cut(src, (970,630,1120,890), 'paper_right.png')
# remove logo from art: inpaint its area
mask = np.zeros(clean.shape[:2], np.uint8)
mask[1278:1605, 40:225] = cv2.dilate(lm, np.ones((9,9),np.uint8))
mask[630:890, 970:1120] = cv2.dilate(pm, np.ones((15,15),np.uint8))
art = cv2.inpaint(clean, mask, 15, cv2.INPAINT_TELEA)
# soften title-box smear: blend blurred version with feathered mask
fm = np.zeros(clean.shape[:2], np.float32); fm[380:690, 560:1110] = 1
fm = cv2.GaussianBlur(fm, (0,0), 25)[...,None]
blur = cv2.GaussianBlur(art, (0,0), 18)
art = (art*(1-fm) + blur*fm).astype(np.uint8)
# blur logo area too
fm2 = np.zeros(clean.shape[:2], np.float32); fm2[1270:1608, 30:235] = 1
fm2 = cv2.GaussianBlur(fm2,(0,0),20)[...,None]
blur2 = cv2.GaussianBlur(art,(0,0),14)
art = (art*(1-fm2)+blur2*fm2).astype(np.uint8)
art = art[:, 6:1172]
cv2.imwrite('art.jpg', art, [cv2.IMWRITE_JPEG_QUALITY, 95])
print(art.shape, art[:, -40:].reshape(-1,3).mean(0)[::-1].round())

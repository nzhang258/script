import os
import cv2
import sys

def v2p(path):
    cap = cv2.VideoCapture(path)
    suc = cap.isOpened()  # 是否成功打开
    frame_count = 0
    pics=[]
    while suc:
        frame_count += 1
        suc, frame = cap.read()
        if suc:
            pics.append(frame)
    cap.release()
    return pics

def p2v(pic, out, fps, ith):
    f_all = {1: cv2.VideoWriter_fourcc('P','I','M','1'),
             2: cv2.VideoWriter_fourcc('M','J','P','G'),
             3:cv2.VideoWriter_fourcc('M','P','4','2'),
             4:cv2.VideoWriter_fourcc('D','I','V','3'),
             5:cv2.VideoWriter_fourcc('D','I','V','X'),
             6:cv2.VideoWriter_fourcc('U','2','6','3'),
             7:cv2.VideoWriter_fourcc('I','2','6','3'),
             8:cv2.VideoWriter_fourcc('F','L','V','1')}
    fourcc = f_all[ith]
    h,w,c = pic[0].shape
    vw = cv2.VideoWriter(out, fourcc, fps, (w,h))
    for i in pic:
        vw.write(i)
    vw.release()


def p2v1(pic, out, fps, ith):
    '''
    fourcc = cv2.VideoWriter_fourcc('P','I','M','1')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    fourcc = cv2.VideoWriter_fourcc('M','P','4','2')
    fourcc = cv2.VideoWriter_fourcc('D','I','V','3')
    fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
    fourcc = cv2.VideoWriter_fourcc('U','2','6','3')
    fourcc = cv2.VideoWriter_fourcc('I','2','6','3')
    fourcc = cv2.VideoWriter_fourcc('F','L','V','1')
    '''
    
    f_all = {1: cv2.VideoWriter_fourcc('P','I','M','1'),
             2: cv2.VideoWriter_fourcc('M','J','P','G'),
             3:cv2.VideoWriter_fourcc('M','P','4','2'),
             4:cv2.VideoWriter_fourcc('D','I','V','3'),
             5:cv2.VideoWriter_fourcc('D','I','V','X'),
             6:cv2.VideoWriter_fourcc('U','2','6','3'),
             7:cv2.VideoWriter_fourcc('I','2','6','3'),
             8:cv2.VideoWriter_fourcc('F','L','V','1')}
    fourcc = f_all[ith]
    #fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    a = os.listdir(pic)
    a.sort()
    img0 = cv2.imread(os.path.join(pic,a[0]))
    h,w,c = img0.shape
    vw = cv2.VideoWriter(out, fourcc, fps, (w,h))
    for i in a:
        img = cv2.imread(os.path.join(pic,i))
        vw.write(img)
    vw.release()

if __name__ == '__main__':
    in_vid = sys.argv[1]
    out = sys.argv[2]
    fps = 30
    imgs = v2p(in_vid)
    p2v(imgs,out,fps,5)

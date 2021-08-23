
import cv2
import numpy as np

def parsePIVlabTextFile(filePath, demiliter=',', image=None, scaleFactor=5):
    lines = []
    with open(filePath, 'r') as f:
        print(f.readline().strip())
        print(f.readline().strip())
        print(f.readline().strip())
        lines = f.readlines()
    print(f'Number of lines: {len(lines)}')
    vec_x, vec_y, vec_u, vec_v = [], [], [], []

    for line in lines:
        tokens = line.strip().split(',')
        x, y, u, v, vecType = int(tokens[0]), int(tokens[1]), float(
            tokens[2]), float(tokens[3]), int(tokens[4])
        vec_x.append(x)
        vec_y.append(y)
        vec_u.append(u)
        vec_v.append(v)

        if isinstance(image, type(None)):
            # magatxy = mag_colormap[y, x]
            # color = (int(magatxy[0]), int(magatxy[1]), int(magatxy[2]))
            p2 = (int(round(x+u*scaleFactor)), int(round(y+v*scaleFactor)))
            cv2.arrowedLine(image, (x, y), p2, (0, 255, 0), 1)

    vec_x, vec_y, vec_u, vec_v = np.array(vec_x), np.array(vec_y), np.array(vec_u), np.array(vec_v)
    return vec_x, vec_y, vec_u, vec_v, image
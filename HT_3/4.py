RGB_TO_YIQ = [
    [0.299, 0.587, 0.114],
    [0.596, -0.274, -0.322],
    [0.211, -0.523, 0.312]
]

YIQ_TO_RGB = [
    [1.000, 0.956, 0.621],
    [1.000, -0.272, -0.647],
    [1.000, -1.106, 1.703]
]

def dot3(M, v):
    return [M[0][0]*v[0]+M[0][1]*v[1]+M[0][2]*v[2],
            M[1][0]*v[0]+M[1][1]*v[1]+M[1][2]*v[2],
            M[2][0]*v[0]+M[2][1]*v[1]+M[2][2]*v[2]]

def convert_rgb_yiq(vec4):
    x, y, z, t = vec4
    if int(round(t))==0:
        r,g,b = x,y,z
        yv, iv, qv = dot3(RGB_TO_YIQ, [r,g,b])
        return [yv, iv, qv, 1]
    else:
        yv, iv, qv = x,y,z
        r,g,b = dot3(YIQ_TO_RGB, [yv,iv,qv])
        r = max(0.0, min(1.0, r))
        g = max(0.0, min(1.0, g))
        b = max(0.0, min(1.0, b))
        return [r, g, b, 0]
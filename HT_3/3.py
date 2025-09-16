def per_channel_filter(filter2d):
    def wrapped(img):
        if not img or not img[0] or not isinstance(img[0][0], list):
            return filter2d(img)
        h, w, c = len(img), len(img[0]), len(img[0][0])
        out = [[[0.0 for _ in range(c)] for _ in range(w)] for _ in range(h)]
        for ch in range(c):
            plane = [[img[i][j][ch] for j in range(w)] for i in range(h)]
            fp = filter2d(plane)
            for i in range(len(fp)):
                for j in range(len(fp[0])):
                    out[i][j][ch]=fp[i][j]
        return out
    return wrapped
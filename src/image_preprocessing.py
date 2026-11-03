"""Separate a single uploaded digit from a plain background or photographed paper."""
import cv2
import numpy as np


def extract_uploaded_digit(rgb):
    h, w = rgb.shape[:2]
    if max(h, w) > 800:
        scale = 800 / max(h, w)
        rgb = cv2.resize(rgb, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    # Photographed paper contains midtones, shadows and ruling. Local contrast
    # on the red channel separates dark/blue ink from the lighter paper grid.
    photo = max(h, w) > 200 and np.mean((gray > 30) & (gray < 225)) > 0.2
    if photo:
        contrast = cv2.morphologyEx(rgb[..., 0], cv2.MORPH_BLACKHAT,
                                  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
        threshold, _ = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, mask = cv2.threshold(contrast, max(35, threshold * 1.6), 255, cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    else:
        border = np.concatenate([gray[0], gray[-1], gray[:, 0], gray[:, -1]])
        if np.median(border) > 127:
            gray = 255 - gray
        mask = np.uint8(gray > 20) * 255
    count, labels, stats, centers = cv2.connectedComponentsWithStats(mask)
    choices = []
    for i in range(1, count):
        x, y, cw, ch, area = stats[i]
        if area < 10:
            continue
        if photo and (cw > w * .85 or ch > h * .85 or x < 2 or y < 2 or x + cw > w - 2 or y + ch > h - 2):
            continue
        cx, cy = centers[i]
        central = np.exp(-4 * ((cx / w - .5) ** 2 + (cy / h - .5) ** 2))
        choices.append((area * central, i))
    if not choices:
        return np.zeros_like(gray)
    selected = max(choices)[1]
    mask = np.uint8(labels == selected) * 255
    if photo:
        # A thin pen stroke can disappear when reduced to 20 pixels in height.
        # Restore stroke width in proportion to the detected digit's height.
        size = max(1, round(int(stats[selected, cv2.CC_STAT_HEIGHT]) * .05))
        return cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size)))
    # Preserve antialiased grayscale strokes for clean images. Only crop away
    # disconnected artifacts far from the main digit; binarizing these pixels
    # would change the MNIST input that the saved model expects.
    x, y, cw, ch, _ = stats[selected]
    margin = max(2, round(max(cw, ch) * .1))
    x0, y0 = max(0, x - margin), max(0, y - margin)
    x1, y1 = min(w, x + cw + margin), min(h, y + ch + margin)
    other = np.uint8((labels > 0) & (labels != selected))
    other[y0:y1, x0:x1] = 0
    if other.any():
        result = np.zeros_like(gray)
        result[y0:y1, x0:x1] = gray[y0:y1, x0:x1]
        return result
    return gray

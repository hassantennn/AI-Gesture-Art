import colorsys

def neon_color_from_hue(hue):
    saturation = 0.9
    brightness = 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)
    return (int(r * 255), int(g * 255), int(b * 255))

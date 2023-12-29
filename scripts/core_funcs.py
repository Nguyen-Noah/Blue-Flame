import pygame, math

def swap_color(img, old_c, new_c):
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img, (0, 0))
    surf.set_colorkey((0, 0, 0))
    return surf

def blit_center(target_surf, surf, loc, add=False):
    if not add:
        target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2))
    else:
        target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2), special_flags=pygame.BLEND_RGBA_ADD)

def itr(l):
    return sorted(enumerate(l), reverse=True)

def normalize(value, amount, around=0):
    if (value - amount) > around:
        value -= amount
    elif (value + amount) < around:
        value += amount
    else:
        value = around
    return value

def advance(pos, angle, amt=1):
    pos[0] += math.cos(angle) * amt
    pos[1] += math.sin(angle) * amt
    return pos

def get_dis(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def get_magnitude(x, y):
    return math.sqrt(x*x + y*y)

def get_angle(start, end):
    return math.atan2(end[1] - start[1], end[0] - start[0])

def clamp(value_to_clamp, min_val, max_val):
    return max(min_val, min(max_val, value_to_clamp))

def easeInOutCubic(t):
    t *= 2
    if t < 1:
        return t * t * t / 2
    else:
        t -= 2
        return (t * t * t + 2) / 2

def swap_color(img,old_c,new_c):
    e_colorkey = (0, 0, 0, 0)
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    surf.set_colorkey(e_colorkey)
    return surf
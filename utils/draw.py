from data.screen import SCREEN

def draw_text(text, font, text_col, x, y, center=False):
    img = font.render(text, True, text_col)
    
    if center:
        rect = img.get_rect(center=(x, y))
        SCREEN.blit(img, rect)
    else:
        SCREEN.blit(img, (x, y))
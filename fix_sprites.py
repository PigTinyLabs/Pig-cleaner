from PIL import Image
import os

def process_image(img_path, cols, rows, output_dir, prefix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    im = Image.open(img_path).convert('RGBA')
    w, h = im.size
    
    cell_w = w / cols
    cell_h = h / rows
    
    for row in range(rows):
        for col in range(cols):
            left = int(col * cell_w)
            top = int(row * cell_h)
            right = int((col + 1) * cell_w)
            bottom = int((row + 1) * cell_h)
            
            cell = im.crop((left, top, right, bottom))
            pixels = cell.load()
            cw, ch = cell.size
            
            min_x = cw; min_y = ch; max_x = 0; max_y = 0
            
            for y in range(ch):
                for x in range(cw):
                    r, g, b, a = pixels[x, y]
                    
                    if a < 10:
                        is_bg = True
                    else:
                        d1 = abs(r-93) + abs(g-78) + abs(b-73)
                        d2 = abs(r-148) + abs(g-129) + abs(b-123)
                        d3 = abs(r-149) + abs(g-130) + abs(b-124)
                        d4 = abs(r-150) + abs(g-131) + abs(b-125)
                        d5 = abs(r-94) + abs(g-79) + abs(b-74)
                        is_bg = (d1 < 40) or (d2 < 40) or (d3 < 40) or (d4 < 40) or (d5 < 40)
                        if r > 240 and g > 240 and b > 240:
                            is_bg = True
                        
                    if is_bg:
                        pixels[x, y] = (0, 0, 0, 0)
                    else:
                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)
            
            if min_x <= max_x and min_y <= max_y:
                fg = cell.crop((min_x, min_y, max_x + 1, max_y + 1))
                final_img = Image.new('RGBA', (300, 200), (0, 0, 0, 0))
                fw, fh = fg.size
                
                scale = 1
                if fw > 280 or fh > 180:
                    scale = min(280/fw, 180/fh)
                    new_w = int(fw * scale)
                    new_h = int(fh * scale)
                    fg = fg.resize((new_w, new_h), Image.Resampling.NEAREST)
                    fw, fh = new_w, new_h
                
                paste_x = (300 - fw) // 2
                paste_y = 200 - fh - 20
                final_img.paste(fg, (paste_x, paste_y))
                
                idx = row * cols + col + 1
                final_img.save(f"{output_dir}/{prefix}_{idx}.png")

# Actually, the user's second image has only 2 rows. Wait, if it has 2 rows but it's 1536px high,
# maybe the grid is actually 4 rows, but only top 2 rows have content?
# Let's just crop it as 4 rows, and save the non-empty ones?
# If we use rows=2, the cell height is 768. If it's correctly cropped, it will still place it at the bottom of 300x200!
# Wait! Let's check the position in 768.
# If I use rows=2, it will work correctly as long as I ignore transparent pixels!
process_image('/Users/tiny/Downloads/dog-eat-dog-sleep.png', 8, 4, './src/renderer/assets/sprites/dog_extra', 'dog_extra')

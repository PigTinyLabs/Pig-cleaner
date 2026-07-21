from PIL import Image
import os
from collections import deque

def is_bg_color(r, g, b, a):
    if a < 10:
        return True
    d1 = abs(r-93) + abs(g-78) + abs(b-73)
    d2 = abs(r-148) + abs(g-129) + abs(b-123)
    d3 = abs(r-149) + abs(g-130) + abs(b-124)
    d4 = abs(r-150) + abs(g-131) + abs(b-125)
    d5 = abs(r-94) + abs(g-79) + abs(b-74)
    if (d1 < 40) or (d2 < 40) or (d3 < 40) or (d4 < 40) or (d5 < 40):
        return True
    if r > 240 and g > 240 and b > 240:
        return True
    return False

def process_sniff(img_path, cols, rows, output_dir, prefix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    im = Image.open(img_path).convert('RGBA')
    w, h = im.size
    
    cell_w = w / cols
    cell_h = h / rows
    
    idx = 1
    for row in range(rows):
        for col in range(cols):
            left = int(col * cell_w)
            top = int(row * cell_h)
            right = int((col + 1) * cell_w)
            bottom = int((row + 1) * cell_h)
            
            cell = im.crop((left, top, right, bottom))
            pixels = cell.load()
            cw, ch = cell.size
            
            visited = set()
            queue = deque()
            
            # Initialize queue with perimeter pixels that are bg
            for x in range(cw):
                if is_bg_color(*pixels[x, 0]): queue.append((x, 0))
                if is_bg_color(*pixels[x, ch-1]): queue.append((x, ch-1))
            for y in range(1, ch-1):
                if is_bg_color(*pixels[0, y]): queue.append((0, y))
                if is_bg_color(*pixels[cw-1, y]): queue.append((cw-1, y))
                
            for q in queue:
                visited.add(q)
                
            while queue:
                x, y = queue.popleft()
                pixels[x, y] = (0, 0, 0, 0)
                
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < cw and 0 <= ny < ch:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            if is_bg_color(*pixels[nx, ny]):
                                queue.append((nx, ny))
            
            # Find bounding box of foreground
            min_x = cw; min_y = ch; max_x = 0; max_y = 0
            for y in range(ch):
                for x in range(cw):
                    r, g, b, a = pixels[x, y]
                    if a > 0:
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
                
                # Align the bottom to baseline 179
                paste_y = 179 - fh + 1
                final_img.paste(fg, (paste_x, paste_y))
                
                out_path = f'{output_dir}/{prefix}_{idx}.png'
                final_img.save(out_path)
                print(f"Saved {out_path}, size {final_img.size}, bbox {final_img.getbbox()}")
            idx += 1

process_sniff('/Users/tiny/Documents/Personal/Pig-cleaner/src/renderer/assets/sniff.png', 3, 1, './src/renderer/assets/sprites/dog_sniff', 'dog_sniff')

from PIL import Image
import math
import os

def process_image(img_path, cols, rows, output_dir, prefix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    im = Image.open(img_path).convert('RGBA')
    w, h = im.size
    
    cell_w = w / cols
    cell_h = h / rows
    
    # Define background colors (brownish checkerboard and grid lines)
    # The background colors observed: (93, 78, 73), (148, 129, 123), etc.
    # We will just assume anything that is roughly grayish/brownish is background.
    # But wait, we can just pick the color of the top-left pixel of each cell.
    # Actually, a better way is to see if the pixel differs from the checkerboard pattern.
    
    for row in range(rows):
        for col in range(cols):
            left = int(col * cell_w)
            top = int(row * cell_h)
            right = int((col + 1) * cell_w)
            bottom = int((row + 1) * cell_h)
            
            cell = im.crop((left, top, right, bottom))
            
            # Let's remove background. 
            # We know the background has low saturation and specific colors.
            pixels = cell.load()
            cw, ch = cell.size
            
            # Find bounding box of foreground
            min_x = cw; min_y = ch; max_x = 0; max_y = 0
            
            for y in range(ch):
                for x in range(cw):
                    r, g, b, a = pixels[x, y]
                    
                    # Check if it's background
                    # Background is roughly r=93, g=78, b=73 or r=148, g=129, b=123
                    # Let's use a heuristic: if it's brown/gray and not yellow/golden.
                    # The dog is golden (high r and g).
                    # Let's compute color distance to the two main background colors
                    d1 = abs(r-93) + abs(g-78) + abs(b-73)
                    d2 = abs(r-148) + abs(g-129) + abs(b-123)
                    d3 = abs(r-149) + abs(g-130) + abs(b-124)
                    d4 = abs(r-150) + abs(g-131) + abs(b-125)
                    d5 = abs(r-94) + abs(g-79) + abs(b-74)
                    
                    is_bg = (d1 < 40) or (d2 < 40) or (d3 < 40) or (d4 < 40) or (d5 < 40)
                    
                    # Also the grid lines or white numbers
                    if r > 240 and g > 240 and b > 240:
                        is_bg = True # white numbers
                        
                    if is_bg:
                        pixels[x, y] = (0, 0, 0, 0)
                    else:
                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)
            
            # Crop to bounding box
            if min_x <= max_x and min_y <= max_y:
                fg = cell.crop((min_x, min_y, max_x + 1, max_y + 1))
                
                # Resize or pad to 300x200? Or just save it tightly?
                # The existing sprites are 300x200. We can paste the dog in the bottom center.
                final_img = Image.new('RGBA', (300, 200), (0, 0, 0, 0))
                # Paste at bottom center
                fw, fh = fg.size
                
                # Scale if it's too big
                scale = 1
                if fw > 280 or fh > 180:
                    scale = min(280/fw, 180/fh)
                    new_w = int(fw * scale)
                    new_h = int(fh * scale)
                    fg = fg.resize((new_w, new_h), Image.Resampling.NEAREST)
                    fw, fh = new_w, new_h
                
                paste_x = (300 - fw) // 2
                paste_y = 200 - fh - 20 # 20px from bottom
                final_img.paste(fg, (paste_x, paste_y))
                
                idx = row * cols + col + 1
                final_img.save(f"{output_dir}/{prefix}_{idx}.png")
            
process_image('/Users/tiny/Downloads/dog-spirte.png', 8, 4, './src/renderer/assets/sprites/dog', 'dog')
process_image('/Users/tiny/Downloads/dog-eat-dog-sleep.png', 8, 2, './src/renderer/assets/sprites/dog_extra', 'dog_extra')
print("Done!")

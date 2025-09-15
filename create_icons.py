from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icons():
    """Create PWA app icons"""
    
    # Create a simple icon with plant emoji or design
    sizes = [192, 512]
    
    for size in sizes:
        # Create image with gradient background
        img = Image.new('RGB', (size, size), color='#0c0c0c')
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for i in range(size):
            color_val = int(12 + (i / size) * 100)  # Gradient from dark to lighter
            draw.line([(0, i), (size, i)], fill=(color_val, color_val//2, color_val))
        
        # Add plant icon (simple leaf shape)
        center = size // 2
        leaf_size = size // 3
        
        # Draw leaf shape
        draw.ellipse([
            center - leaf_size//2, center - leaf_size,
            center + leaf_size//2, center + leaf_size//2
        ], fill='#00ff7f', outline='#32cd32', width=3)
        
        # Add text
        try:
            font_size = size // 8
            font = ImageFont.load_default()
            text = "🌱"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text((center - text_width//2, center + leaf_size//3), text, 
                     fill='white', font=font)
        except:
            pass
        
        # Save icon
        img.save(f'icon-{size}.png', 'PNG')
        print(f"Created icon-{size}.png")

if __name__ == "__main__":
    create_app_icons()
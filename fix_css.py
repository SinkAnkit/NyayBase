import re

with open("frontend/app/page.module.css", "r") as f:
    css = f.read()

# Remove glassmorphism
css = re.sub(r'backdrop-filter:\s*blur\([^)]+\);\n?', '', css)

# Fix backgrounds
css = re.sub(r'rgba\(6,\s*10,\s*20,\s*[0-9.]+\)', 'var(--bg-card)', css)
css = re.sub(r'rgba\(255,\s*255,\s*255,\s*0\.0[0-9]\)', 'rgba(0, 0, 0, 0.04)', css)
css = re.sub(r'rgba\(255,\s*255,\s*255,\s*0\.1[0-9]?\)', 'rgba(0, 0, 0, 0.08)', css)
css = re.sub(r'rgba\(14,\s*14,\s*28,\s*[0-9.]+\)', 'var(--bg-card)', css)

# Fix purple gradients
css = re.sub(r'linear-gradient\(135deg,\s*#8b5cf6,\s*#3b82f6\)', 'var(--purple)', css)
css = re.sub(r'linear-gradient\(135deg,\s*var\(--accent\),\s*var\(--blue\)\)', 'var(--purple)', css)
css = re.sub(r'linear-gradient\(135deg,\s*rgba\(139,\s*92,\s*246,\s*[0-9.]+\),\s*rgba\(99,\s*102,\s*241,\s*[0-9.]+\)\)', 'var(--purple-glow)', css)
css = re.sub(r'linear-gradient\(135deg,\s*rgba\(139,\s*92,\s*246,\s*[0-9.]+\),\s*rgba\(59,\s*130,\s*246,\s*[0-9.]+\)\)', 'var(--purple-glow)', css)

# Fix text colors that were forced to white for dark mode
css = re.sub(r'color:\s*#fff;', 'color: #ffffff;', css)
# Wait, some buttons need white text.
# Replace color: #ffffff with var(--bg-card) where appropriate?
# Buttons (like .btnPrimary) have color: #fff. That's fine (indigo bg, white text).
# For other things, keep #fff as is, or let's be specific:

# Remove glowing shadows
css = re.sub(r'box-shadow:\s*0\s*[0-9]+px\s*[0-9]+px\s*rgba\(139,\s*92,\s*246,\s*[0-9.]+\);', 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);', css)
css = re.sub(r'box-shadow:\s*0\s*0\s*[0-9]+px\s*[0-9]+px\s*rgba\(139,\s*92,\s*246,\s*[0-9.]+\);', '', css)
css = re.sub(r'box-shadow:\s*0\s*0\s*[0-9]+px\s*rgba\(139,\s*92,\s*246,\s*[0-9.]+\);', '', css)

# Remove animations
css = re.sub(r'animation:\s*glowPulse[^;]+;\n?', '', css)
css = re.sub(r'animation:\s*chatPulse[^;]+;\n?', '', css)
css = re.sub(r'animation:\s*pulse[^;]+;\n?', '', css)
css = re.sub(r'animation:\s*stopPulse[^;]+;\n?', '', css)

# Remove hover lifts
css = re.sub(r'transform:\s*translateY\(-[0-9]+px\)(?:\s*scale\([0-9.]+\))?;', '', css)

# Fix specific layout issues for the plan
# 1. Feature Cards layout
css = re.sub(r'\.cardIcon \{\s*width: 40px;\s*height: 40px;\s*display: flex;\s*align-items: center;\s*justify-content: center;\s*background: var\(--purple-glow\);\s*border-radius: 10px;\s*color: var\(--purple\);\s*\}',
             '.cardIcon { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: var(--purple-glow); border-radius: 8px; color: var(--purple); margin-right: 12px; float: left; }', css)

# Let's save it back
with open("frontend/app/page.module.css", "w") as f:
    f.write(css)

print("Done fixing CSS.")

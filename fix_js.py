import re

with open("frontend/app/page.js", "r") as f:
    js = f.read()

# 1. Remove Hero Eyebrow
js = re.sub(r'<div className=\{styles\.heroTag\}>[^<]+</div>\n?', '', js)

# 2. Remove Hero SVG BG
js = re.sub(r'\{\s*/\*\s*Decorative SVG background.*?\*/\s*\}.*?<div className=\{styles\.heroBg\} aria-hidden="true">\s*<svg className=\{styles\.heroBgSvg\}[^>]+>.*?</svg>\s*</div>', '', js, flags=re.DOTALL)

# 3. Simplify Trust Section dots
js = re.sub(r'<div className=\{styles\.trustDot\}></div>\n?', '', js)

# 4. Remove section divider SVGs
js = re.sub(r'<div className=\{styles\.sectionDivider\}>\s*<svg viewBox="0 0 1200 2" fill="none">.*?</svg>\s*</div>', '<hr style={{ border: "none", borderTop: "1px solid var(--border)", margin: "0 auto", maxWidth: "800px" }} />', js, flags=re.DOTALL)

# 5. Fix Stat Cards top borders
js = re.sub(r'<div className=\{styles\.statCard\} style=\{\{ borderTop: "3px solid #[a-f0-9]+" \}\}>', '<div className={styles.statCard}>', js)

# 6. Feature Cards Layout
js = js.replace('<div key={i} className={styles.card}><div className={styles.cardIcon}>{I(ic)}</div><h3>{t}</h3><p>{d}</p></div>',
                '<div key={i} className={styles.card}><div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "8px" }}><div className={styles.cardIcon} style={{ margin: 0 }}>{I(ic)}</div><h3 style={{ margin: 0 }}>{t}</h3></div><p>{d}</p></div>')

# Write back
with open("frontend/app/page.js", "w") as f:
    f.write(js)

print("Done fixing JS.")

#!/usr/bin/env python3
"""Build one static catalog page for every CSV in ayoub/."""
from __future__ import annotations
import csv, html, re, shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "ayoub"
OUT = ROOT / "catalog"
ALIASES = {
    "title": ["Product Desc","Title","Product Name","Name","Design Name","File Name","Description","Product Title","Item Name","Nom","Titre"],
    "image": ["Image Url","Image URL","Image","Image Link","Image Urls","ImageURL","Photo","Picture Url","Picture URL","Thumbnail","Image Src"],
    "link": ["Promotion Url","Promotion URL","Product Url","Product URL","Product Link","URL","Link","Download Url","Download URL","File Url","File URL","Website","Affiliate Link","Lien","Lien de téléchargement"],
    "description": ["Long Description","Product Description","Details","Details Description","Résumé","Description SEO","Description"],
    "price": ["Discount Price","Sale Price","Price","Current Price","Prix","Prix de vente","SalePrice"],
    "old_price": ["Origin Price","Original Price","Old Price","Regular Price","Prix original"],
}
def norm(s): return re.sub(r"[^a-z0-9]", "", str(s or "").lower())
def pick(row, names):
    lookup = {norm(k): (v or "").strip() for k,v in row.items()}
    for name in names:
        value = lookup.get(norm(name), "")
        if value: return value
    return ""
def safe_url(value):
    value = (value or "").strip()
    return value if urlparse(value).scheme in ("http","https") else ""
def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "csv-catalog"
def read_csv(path):
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    try: dialect = csv.Sniffer().sniff(raw[:8192], delimiters=",;\t|")
    except csv.Error: dialect = csv.excel
    return list(csv.DictReader(raw.splitlines(), dialect=dialect))
def page_template(title, source_name, rows):
    cards=[]
    for i,row in enumerate(rows,1):
        name=pick(row,ALIASES["title"]) or f"Item {i}"
        image=safe_url(pick(row,ALIASES["image"]))
        link=safe_url(pick(row,ALIASES["link"]))
        desc=pick(row,ALIASES["description"])
        price=pick(row,ALIASES["price"])
        old=pick(row,ALIASES["old_price"])
        image_html=f'<img src="{html.escape(image, quote=True)}" alt="{html.escape(name, quote=True)}" loading="lazy" onerror="this.remove()">' if image else '<span class="placeholder">CNC</span>'
        action=f'<a class="cta" href="{html.escape(link, quote=True)}" target="_blank" rel="noopener noreferrer">View product / design ↗</a>' if link else '<span class="cta muted">Contact us for details</span>'
        cards.append(f'<article class="card"><div class="photo">{image_html}</div><div class="body"><h2>{html.escape(name)}</h2>{f"<p>{html.escape(desc)}</p>" if desc and norm(desc)!=norm(name) else ""}{f"<div class=price>{html.escape(price)}</div>" if price else ""}{f"<div class=old>Was {html.escape(old)}</div>" if old and norm(old)!=norm(price) else ""}{action}</div></article>')
    cards_html="".join(cards) or '<p class="empty">No products found in this CSV file.</p>'
    safe_title=html.escape(title)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{safe_title} CNC catalog"><title>{safe_title} | CNC Forge Maroc</title><style>
:root{{--ink:#172033;--muted:#687386;--line:#e6eaf0;--paper:#f5f7fb;--orange:#f36b3f;--navy:#101827}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,Arial,sans-serif}}a{{color:inherit;text-decoration:none}}.wrap{{width:min(1200px,calc(100% - 30px));margin:auto}}header{{background:#101827;color:white;padding:18px 0}}header .wrap{{display:flex;justify-content:space-between;align-items:center;gap:14px}}.brand{{font-weight:900;font-size:20px}}.brand span{{color:#ff936d}}.back{{font-size:13px;color:#ffd0bd}}.hero{{padding:35px 0 20px}}.eyebrow{{color:var(--orange);font-weight:900;letter-spacing:2px;text-transform:uppercase;font-size:11px}}h1{{font-size:clamp(27px,4vw,42px);line-height:1.12;margin:8px 0}}.summary{{color:var(--muted)}}.tools{{display:flex;justify-content:space-between;gap:12px;align-items:center;margin:12px 0 18px}}input{{width:min(360px,100%);padding:12px;border:1px solid var(--line);border-radius:10px;font:inherit}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;padding-bottom:45px}}.card{{background:white;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 10px 25px #1018270b}}.photo{{height:205px;background:#edf0f5;display:grid;place-items:center;overflow:hidden}}.photo img{{width:100%;height:100%;object-fit:contain;padding:10px}}.placeholder{{font-size:35px;font-weight:950;color:#aab3c2}}.body{{padding:14px;display:flex;flex:1;flex-direction:column}}h2{{font-size:15px;line-height:1.4;margin:0 0 8px}}.body p{{font-size:12px;color:var(--muted);margin:0 0 10px}}.price{{font-size:17px;font-weight:900;margin:5px 0}}.old{{font-size:11px;color:var(--muted);text-decoration:line-through}}.cta{{margin-top:auto;padding:10px 12px;border-radius:9px;background:var(--orange);color:white;text-align:center;font-size:12px;font-weight:900;display:block}}.muted{{background:#eef1f5;color:#596579}}.empty{{grid-column:1/-1;background:white;padding:30px;border-radius:14px;text-align:center;color:var(--muted)}}footer{{background:#101827;color:#aab4c4;padding:22px 0;font-size:12px}}@media(max-width:560px){{.tools{{align-items:stretch;flex-direction:column}}.photo{{height:190px}}}}
</style></head><body><header><div class="wrap"><a class="brand" href="../../">CNC <span>FORGE</span> MAROC</a><a class="back" href="../">← All CSV catalogs</a></div></header><main class="wrap"><section class="hero"><div class="eyebrow">Dedicated CSV catalog</div><h1>{safe_title}</h1><p class="summary">{len(rows)} products · Source: {html.escape(source_name)}</p></section><div class="tools"><strong id="count">{len(rows)} products</strong><input id="search" type="search" placeholder="Search in this catalog…"></div><section class="grid" id="grid">{cards_html}</section></main><footer><div class="wrap">CNC Forge Maroc · One CSV, one independent catalog page.</div></footer><script>const search=document.getElementById('search'),cards=[...document.querySelectorAll('.card')];search.addEventListener('input',()=>{{const q=search.value.toLowerCase();let n=0;cards.forEach(c=>{{const show=c.innerText.toLowerCase().includes(q);c.hidden=!show;if(show)n++}});document.getElementById('count').textContent=n+' products'}});</script></body></html>'''

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    csvs=sorted(p for p in SOURCE.glob("*.csv") if p.is_file())
    current=set()
    links=[]
    for path in csvs:
        slug=slugify(path.stem)
        current.add(slug)
        rows=[r for r in read_csv(path) if any((v or "").strip() for v in r.values())]
        title=re.sub(r"[-_]+"," ",path.stem).strip().title()
        dest=OUT/slug
        dest.mkdir(parents=True,exist_ok=True)
        (dest/"index.html").write_text(page_template(title,path.name,rows),encoding="utf-8")
        links.append((title,slug,len(rows),path.name))
    # Remove stale generated catalog directories, never touch source CSVs.
    for child in OUT.iterdir():
        if child.is_dir() and child.name not in current: shutil.rmtree(child)
    listing=''.join(f'<a class="item" href="{slug}/"><strong>{html.escape(title)}</strong><span>{count} products · {html.escape(filename)}</span></a>' for title,slug,count,filename in links)
    index=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>All CNC CSV Catalogs | CNC Forge Maroc</title><style>body{{margin:0;background:#f5f7fb;color:#172033;font:15px/1.5 Arial}}header,footer{{background:#101827;color:white;padding:20px}}main{{width:min(1000px,calc(100% - 30px));margin:35px auto}}h1{{font-size:34px}}p{{color:#687386}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:13px}}.item{{background:white;border:1px solid #e6eaf0;border-radius:13px;padding:17px;display:flex;flex-direction:column;gap:7px;text-decoration:none;color:#172033}}.item:hover{{border-color:#f36b3f;transform:translateY(-2px)}}.item span{{font-size:12px;color:#687386}}</style></head><body><header><a href="../" style="color:white;text-decoration:none;font-weight:900">CNC FORGE MAROC</a></header><main><h1>All CSV catalogs</h1><p>Each CSV file has its own independent product page. Add a CSV to the ayoub/ folder and the catalog pages rebuild automatically.</p><section class="grid">{listing}</section></main><footer>CNC Forge Maroc</footer></body></html>'''
    (OUT/"index.html").write_text(index,encoding="utf-8")
    print(f"Generated {len(csvs)} independent catalog pages.")
if __name__=="__main__": main()

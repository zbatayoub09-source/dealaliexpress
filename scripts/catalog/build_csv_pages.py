#!/usr/bin/env python3
"""Generate AliExpress-inspired independent storefront pages from every CSV in ayoub/."""
from __future__ import annotations
import csv, html, re, shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "ayoub"
OUT = ROOT / "catalog"
ALIASES = {
 "title":["Product Desc","Title","Product Name","Name","Design Name","File Name","Description","Product Title","Item Name","Nom","Titre"],
 "image":["Image Url","Image URL","Image","Image Link","Image Urls","ImageURL","Photo","Picture Url","Picture URL","Thumbnail","Image Src"],
 "link":["Promotion Url","Promotion URL","Product Url","Product URL","Product Link","URL","Link","Download Url","Download URL","File Url","File URL","Website","Affiliate Link","Lien","Lien de téléchargement"],
 "description":["Long Description","Product Description","Details","Details Description","Résumé","Description SEO","Description"],
 "price":["Discount Price","Sale Price","Price","Current Price","Prix","Prix de vente","SalePrice"],
 "old_price":["Origin Price","Original Price","Old Price","Regular Price","Prix original"],
}
def norm(s): return re.sub(r"[^a-z0-9]", "", str(s or "").lower())
def pick(row,names):
 d={norm(k):(v or "").strip() for k,v in row.items()}
 for n in names:
  if d.get(norm(n)): return d[n]
 return ""
def safe_url(v):
 v=(v or "").strip()
 return v if urlparse(v).scheme in ("http","https") else ""
def slugify(name):
 s=re.sub(r"[^a-z0-9]+","-",name.lower()).strip("-")
 return s or "csv-catalog"
def read_csv(path):
 raw=path.read_text(encoding="utf-8-sig",errors="replace")
 try: dialect=csv.Sniffer().sniff(raw[:8192],delimiters=",;\\t|")
 except csv.Error: dialect=csv.excel
 return list(csv.DictReader(raw.splitlines(),dialect=dialect))
def page_template(title,source_name,rows):
 cards=[]
 for i,row in enumerate(rows,1):
  name=pick(row,ALIASES["title"]) or f"Design CNC {i}"
  image=safe_url(pick(row,ALIASES["image"]))
  link=safe_url(pick(row,ALIASES["link"]))
  desc=pick(row,ALIASES["description"])
  price=pick(row,ALIASES["price"])
  old=pick(row,ALIASES["old_price"])
  photo=f'<img src="{html.escape(image,quote=True)}" alt="{html.escape(name,quote=True)}" loading="lazy" onerror="this.style.display=\'none\'">' if image else '<div class="no-photo">CNC<br>DESIGN</div>'
  action=f'<a class="buy" href="{html.escape(link,quote=True)}" target="_blank" rel="noopener noreferrer">View details <b>›</b></a>' if link else '<span class="buy disabled">Contact for details</span>'
  cards.append(f'<article class="product"><a class="image" href="{html.escape(link,quote=True) if link else "#"}" target="_blank" rel="noopener">{photo}<span class="ship">CNC FORGE</span></a><div class="details"><h2>{html.escape(name)}</h2>{f"<p>{html.escape(desc[:180])}</p>" if desc and norm(desc)!=norm(name) else ""}<div class="prices">{f"<strong>{html.escape(price)}</strong>" if price else "<strong>See details</strong>"}{f"<del>{html.escape(old)}</del>" if old and norm(old)!=norm(price) else ""}</div>{action}</div></article>')
 safe=html.escape(title)
 cards_html="".join(cards) or '<div class="empty">No products found in this CSV file.</div>'
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{safe} CNC designs and products"><title>{safe} | CNC Forge Maroc</title><style>
*{{box-sizing:border-box}}:root{{--red:#f44336;--orange:#ff6a00;--ink:#222;--muted:#777;--line:#eee;--bg:#f5f5f5}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px Arial,Helvetica,sans-serif}}a{{color:inherit;text-decoration:none}}.wrap{{width:min(1280px,calc(100% - 28px));margin:auto}}.top{{background:#222;color:#eee;font-size:11px;padding:8px 0}}.top .wrap{{display:flex;justify-content:space-between;gap:10px}}header{{background:#fff;border-bottom:1px solid var(--line)}}.head{{display:flex;align-items:center;gap:24px;min-height:76px}}.logo{{font-size:23px;font-weight:900;white-space:nowrap;color:#222}}.logo b{{color:var(--orange)}}.search{{display:flex;flex:1;max-width:650px;border:2px solid var(--orange);border-radius:24px;overflow:hidden;height:42px}}.search input{{flex:1;min-width:0;border:0;outline:0;padding:0 17px;font-size:13px}}.search button{{border:0;background:var(--orange);color:white;padding:0 25px;font-weight:bold;cursor:pointer}}.back{{font-size:12px;color:#555;margin-left:auto}}.crumb{{font-size:11px;color:#888;padding:14px 0}}.hero{{background:linear-gradient(110deg,#fff,#fff5ed);border-radius:12px;padding:24px;margin:4px 0 18px;display:flex;justify-content:space-between;align-items:center;gap:15px}}.eyebrow{{color:var(--orange);font-size:10px;font-weight:bold;letter-spacing:1.5px}}h1{{font-size:clamp(23px,3vw,34px);margin:8px 0}}.sub{{color:#777;font-size:12px}}.count{{background:#fff;border:1px solid #ffe0ce;border-radius:9px;padding:12px 18px;text-align:center;white-space:nowrap}}.count strong{{display:block;color:var(--orange);font-size:22px}}.toolbar{{background:#fff;border:1px solid var(--line);border-radius:9px;padding:12px 15px;display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}}.toolbar input{{width:min(340px,60%);border:1px solid #ddd;border-radius:5px;padding:10px 12px;outline-color:var(--orange)}}.toolbar strong{{font-size:12px}}.grid{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;padding-bottom:35px}}.product{{background:#fff;border:1px solid #eee;border-radius:7px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .15s,transform .15s}}.product:hover{{box-shadow:0 5px 18px #00000012;transform:translateY(-2px)}}.image{{height:190px;background:#fafafa;display:grid;place-items:center;position:relative;overflow:hidden}}.image img{{width:100%;height:100%;object-fit:contain;padding:8px}}.no-photo{{font-size:22px;line-height:1.5;text-align:center;font-weight:900;color:#bbb}}.ship{{position:absolute;left:8px;top:8px;background:#fff;border-radius:3px;padding:5px 7px;font-size:9px;font-weight:bold;color:var(--orange)}}.details{{padding:11px;display:flex;flex-direction:column;flex:1}}h2{{font-size:13px;line-height:1.4;font-weight:500;margin:0 0 7px;min-height:36px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}.details p{{font-size:11px;color:#888;line-height:1.45;margin:0 0 8px;min-height:32px}}.prices{{display:flex;align-items:center;gap:8px;margin:7px 0 12px;min-height:22px}}.prices strong{{font-size:17px;color:#e53935}}.prices del{{font-size:10px;color:#999}}.buy{{margin-top:auto;background:var(--orange);color:#fff;border-radius:4px;text-align:center;padding:10px;font-size:12px;font-weight:bold;display:block}}.buy b{{font-size:16px;margin-left:4px}}.disabled{{background:#eee;color:#777}}.empty{{grid-column:1/-1;background:white;border-radius:8px;padding:35px;text-align:center;color:#888}}footer{{background:#222;color:#bbb;padding:22px 0;font-size:11px}}@media(max-width:1050px){{.grid{{grid-template-columns:repeat(4,minmax(0,1fr))}}}}@media(max-width:760px){{.grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}.head{{gap:10px;flex-wrap:wrap;padding:12px 0}}.search{{order:3;max-width:none;flex-basis:100%}}.back{{margin-left:auto}}}}@media(max-width:520px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}}.image{{height:155px}}.details{{padding:9px}}.hero{{padding:17px}}.count{{padding:9px}}.top .wrap{{justify-content:center}}.top .wrap span:last-child{{display:none}}}}
</style></head><body><div class="top"><div class="wrap"><span>Welcome to CNC Forge Maroc</span><span>Independent CNC product & design catalog</span></div></div><header><div class="wrap head"><a class="logo" href="../../">CNC <b>FORGE</b></a><label class="search"><input id="search" type="search" placeholder="Search in {safe}"><button type="button" onclick="document.getElementById('search').focus()">SEARCH</button></label><a class="back" href="../">All categories ›</a></div></header><main class="wrap"><div class="crumb"><a href="../../">Home</a> › <a href="../">CNC catalogs</a> › {safe}</div><section class="hero"><div><div class="eyebrow">CNC FORGE MAROC · SHOP BY CATEGORY</div><h1>{safe}</h1><div class="sub">Explore CNC designs and products selected for your workshop · Source: {html.escape(source_name)}</div></div><div class="count"><strong>{len(rows)}</strong><span>Products</span></div></section><div class="toolbar"><strong id="count">{len(rows)} products</strong><input id="filter" type="search" placeholder="Filter products..."></div><section class="grid" id="grid">{cards_html}</section></main><footer><div class="wrap">CNC Forge Maroc · Discover, compare and choose your CNC products and designs.</div></footer><script>const input=document.getElementById('filter'),cards=[...document.querySelectorAll('.product')];input.addEventListener('input',()=>{{let n=0;const q=input.value.toLowerCase();cards.forEach(c=>{{const ok=c.innerText.toLowerCase().includes(q);c.hidden=!ok;if(ok)n++}});document.getElementById('count').textContent=n+' products'}});document.getElementById('search').addEventListener('input',e=>{{input.value=e.target.value;input.dispatchEvent(new Event('input'))}});</script></body></html>'''

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 csvs=sorted(p for p in SOURCE.glob("*.csv") if p.is_file())
 current=set(); links=[]
 for path in csvs:
  slug=slugify(path.stem); current.add(slug)
  rows=[r for r in read_csv(path) if any((v or "").strip() for v in r.values())]
  title=re.sub(r"[-_]+"," ",path.stem).strip().title()
  dest=OUT/slug; dest.mkdir(parents=True,exist_ok=True)
  (dest/"index.html").write_text(page_template(title,path.name,rows),encoding="utf-8")
  links.append((title,slug,len(rows),path.name))
 for child in OUT.iterdir():
  if child.is_dir() and child.name not in current: shutil.rmtree(child)
 listing="".join(f'<a class="tile" href="{slug}/"><div class="tile-icon">CNC</div><div><strong>{html.escape(title)}</strong><small>{count} products · {html.escape(filename)}</small></div><b>›</b></a>' for title,slug,count,filename in links)
 index=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CNC Categories | CNC Forge Maroc</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#f5f5f5;color:#222;font:14px Arial}}header{{background:#222;color:#fff;padding:18px}}main{{width:min(1200px,calc(100% - 28px));margin:28px auto}}.logo{{font-size:22px;font-weight:900}}.logo b{{color:#ff6a00}}h1{{font-size:30px}}p{{color:#777}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}.tile{{background:white;border:1px solid #eee;border-radius:8px;padding:15px;display:flex;align-items:center;gap:12px;text-decoration:none;color:#222}}.tile:hover{{border-color:#ff6a00}}.tile-icon{{width:54px;height:54px;border-radius:7px;background:#fff1e7;color:#ff6a00;display:grid;place-items:center;font-weight:900}}.tile div:nth-child(2){{flex:1}}small{{display:block;color:#888;margin-top:6px;font-size:11px}}.tile>b{{color:#ff6a00;font-size:22px}}footer{{background:#222;color:#bbb;padding:22px}}</style></head><body><header><div class="logo">CNC <b>FORGE</b> MAROC</div></header><main><p>HOME › CNC CATEGORIES</p><h1>Shop CNC categories</h1><p>Every CSV file is displayed as its own independent catalog. Add a CSV file to ayoub/ and its page is generated automatically.</p><section class="grid">{listing}</section></main><footer>CNC Forge Maroc</footer></body></html>'''
 (OUT/"index.html").write_text(index,encoding="utf-8")
 print(f"Generated {len(csvs)} independent catalog pages.")
if __name__=="__main__": main()

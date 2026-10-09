# CNC Forge — CNC Products Storefront

A responsive, SEO-ready storefront for CNC routers, laser engravers, cutting tools, spindle motors, machine parts and workshop accessories.

## Files
- `index.html` — storefront homepage, category browsing, search, sort and product cards.
- `products.csv` — add your CNC catalogue here (not included yet; it must contain real product data).

## Connect your CNC product CSV
Put a file named `products.csv` in the same folder as `index.html`. The page reads these columns when available:

- `ProductId`
- `Image Url`
- `Product Desc` (used as a title until we add a dedicated SEO Title column)
- `Origin Price`, `Discount Price`, `Currency`
- `Promotion Url` (the actual product/affiliate link)
- Optional: `Category`, `SEO Title`, `SEO Description`

Keep the original product IDs, image URLs, prices and promotion URLs unchanged. Do not fabricate product specifications, ratings or discounts. The page categorizes products by title/description if no category is supplied.

## Publish with GitHub Pages
1. Open **Settings → Pages** in this repository.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch **main** and folder **/(root)**, then save.
4. Wait for GitHub Pages to provide the published URL.

## Next improvements
- Add the actual CNC-only CSV from the existing CNC repositories.
- Create SEO titles, descriptions and relevant hashtags in additional CSV columns while preserving the original columns.
- Verify product links, categories, mobile layout and search after the real catalogue is added.

## Note
The catalogue is not populated yet because the correct CNC-only product file needs to be identified. This prevents unrelated products or invented product details from appearing on the store.

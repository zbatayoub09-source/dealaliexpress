# Automatic CSV catalog pages

- Source files stay in `ayoub/*.csv`.
- Every CSV produces its own independent page at `/catalog/<csv-name>/`.
- The directory `/catalog/` is an index linking to every generated page.
- Adding or updating a CSV in `ayoub/` automatically runs GitHub Actions and rebuilds the pages.
- CSV files are not merged into one category; the CSV filename is the page/category name.
- CSV parsing supports UTF-8 BOM and common comma, semicolon, tab, and pipe delimiters.
- Product image/title/link/price columns are detected by common AliExpress and CNC CSV header names.
- If a row has no product URL, the card shows a contact/details note instead of inventing a link.

The generator is `scripts/catalog/build_csv_pages.py`.

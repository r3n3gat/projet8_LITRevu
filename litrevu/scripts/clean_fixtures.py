# scripts/clean_fixtures.py

import pathlib

# Chemins relatifs aux fixtures
fixtures = [
    'accounts/fixtures/users_fixture.json',
    'reviews/fixtures/tickets.json',
    'reviews/fixtures/reviews.json',
    'reviews/fixtures/follows.json',
]

for path_str in fixtures:
    p = pathlib.Path(path_str)
    # Lire en utf-8-sig : enlève automatiquement le BOM UTF-8
    text = p.read_text(encoding='utf-8-sig')
    # Écrire en utf-8 (sans BOM)
    p.write_text(text, encoding='utf-8')
    print(f'✔ Converted {path_str} to UTF-8 without BOM')

---
name: digitaliza-data-extractor
description: |
  Extract and prepare client data for digitalizaweb.vercel.app LinkTree-style digital cards.
  Use when: (1) Processing restaurant/business client folders containing screenshots, scraped HTML, or LinkTree data,
  (2) Extracting brand colors from logos/images,
  (3) Generating Digitaliza-ready JSON with slug, name, links, colors, and theme configuration,
  (4) Batch processing multiple client folders for 100+ restaurants project,
  (5) User mentions "digitaliza", "tarjeta digital", "linktree", "extraer datos de cliente", or "procesar carpeta de restaurante".
---

# Digitaliza Data Extractor

Extract client data from folders to generate digital business cards for digitalizaweb.vercel.app.

## Workflow

```
Client Folder → Extract Data → Extract Colors → Generate JSON → Review
```

## Step 1: Scan Client Folder

```bash
ls -la <client_folder>/
```

Expected files:
- `datos_extraier.md` - Scraped HTML from LinkTree/profile
- `*.png/*.jpg` - Screenshots, logo images
- `logo.*` - Brand logo

## Step 2: Extract Data

Run extraction:
```bash
python scripts/extract_client_data.py <client_folder> --pretty
```

Batch all clients:
```bash
python scripts/extract_client_data.py <base_folder> --scan-all --output all_clients.json
```

Extracts: business name, WhatsApp, links (with icons), locations.

## Step 3: Extract Brand Colors

```bash
python scripts/extract_colors.py <image_path> --num-colors 5 --output json
```

Returns: `customPrimaryColor`, `customSecondaryColor`, `customAccentColor`, `suggestedTheme`.

## Step 4: Generate Final JSON

Combine into Digitaliza format:

```json
{
  "slug": "doomo-saltado",
  "name": "Doomo Saltado",
  "phone": "+51014711000",
  "whatsapp": "51014711000",
  "address": "Local en Surco, Lima",
  "logoUrl": "logo.png",
  "theme": "custom",
  "customPrimaryColor": "#dc2626",
  "customSecondaryColor": "#b91c1c",
  "backgroundStyle": "mesh",
  "links": [
    {"title": "Reservar", "url": "https://wa.me/51014711000", "icon": "whatsapp", "order": 0, "isActive": true},
    {"title": "Instagram", "url": "https://instagram.com/doomo", "icon": "instagram", "order": 1, "isActive": true}
  ]
}
```

## Manual Completion

Verify after extraction:

| Field | Source |
|-------|--------|
| `name` | Screenshots or website |
| `whatsapp` | Country code + number |
| `address` | Google Maps or screenshot |
| `description` | 1-2 sentences about business |
| `theme` | general, italian, mexican, japanese, coffee, hamburguesa, barber, spa, salon |

## Link Icons

| Service | Icon |
|---------|------|
| WhatsApp | `whatsapp` |
| Instagram | `instagram` |
| Facebook | `facebook` |
| TikTok | `tiktok` |
| Google Maps | `location` |
| UberEats | `ubereats` |
| Rappi | `rappi` |
| Menu/Carta | `menu` |

## Batch Checklist

1. Scan all: `python scripts/extract_client_data.py . --scan-all`
2. Review extraction notes
3. Extract colors for folders with logos
4. Flag incomplete data for manual review

## Schema Reference

See `references/digitaliza_schema.md` for complete field definitions.

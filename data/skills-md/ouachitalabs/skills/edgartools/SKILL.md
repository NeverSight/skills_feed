---
name: edgartools
description: Learn the basics of the edgartools library - an SEC EDGAR API wrapper.
---

# Edgartools

Find the latest up to date information by visiting https://edgartools.readthedocs.io/en/latest/.

Edgartools is a python wrapper around the SEC EDGAR API.
It's extremely useful for navigating anything that is publicly accessible through this API.

This includes but is not limited to:
- Explore companies
- Get latest filings of all types
- Manipulate structured xbrl data
- Download entire filings as text or markdown

## Some tips

- You must always set an identity with `edgar.set_identity("First Last first.last@example.com")`.
- This format of `"name email"` is enforced by the SEC.
- There are convenience methods to access a company's latest filings, see `docs/filings.md`
- Do not veer into the deep end of XBRL parsing unless explicitly asked
- Most documents can fit into your context window.
- However, if you must partially read a filing, read the appropriate report.

## Reading filings

Essential setup

Install with uv
```sh
uv add edgartools
```

```python
>>> import edgar # Notice the difference between package install name and import name. This is extremely important.
>>> edgar.set_identity("name email@example.com")
```

Fetching company filings
```python
>>> filing = edgar.get_by_accession_number("0000104169-25-000191") # fetch filing by ID - no need to create Company class.

>>> company = edgar.Company("WMT") # protip: you can use CIK, or ticker here.
>>> filing = company.latest(form=["10-K", "10-Q"]) # protip: you can specify multiple form types here
>>> filing.markdown() # get entire filing as markdown
>>> filing.text() # get entire filing as beautifully rendered text. Prefer this as output for readability.

>>> # You may save the entire file to /tmp/ for fast repeated grepping
>>> with open(f"/tmp/{filing.accession_number}.txt", "w") as fh:
...     fh.write(filing.text())

>>> filing.reports # get list of specific reports (disaggregated revenues, etc)
>>> print(str(filing.reports[37].text())) # get a specific report as text
```

A full filing may be too large to read at once with the `Read` tool.
However, you can either split the file into 3-4 chunks, or read only the relevant reports directly.

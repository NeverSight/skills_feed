---
name: gembox-skill
description: Coding assistance for [GemBox components](https://www.gemboxsoftware.com/). Use when users ask about any GemBox component or coding task that can be performed with a GemBox component. This includes GemBox.Spreadsheet (.NET read/write Excel files), GemBox.Document (.NET read/write Word files), GemBox.Pdf (.NET read/write PDF files), GemBox.Presentation (.NET read/write PowerPoint files), GemBox.Email (.NET read/write email files, send/receive emails), GemBox.Imaging (.NET read/write image files), and GemBox.PdfViewer (JavaScript display/print/save PDF files).
license: MIT
metadata:
  author: gemboxsoftware.com
  version: "0.9"
---

# CLI tips
- .NET runtime check: `dotnet --list-runtimes`
- GemBox .NET component version: `dotnet list package`
- If you need GemBox API details, look them up locally in the XML docs. Example GemBox.Spreadsheet NuGet paths:
  - Linux/macOS: `~/.nuget/packages/gembox.spreadsheet/2025.12.105/lib/*/GemBox.Spreadsheet.xml`
  - PowerShell: `$env:USERPROFILE\.nuget\packages\gembox.spreadsheet\2025.12.105\lib\*\GemBox.Spreadsheet.xml`
- Use ripgrep to search the XML. E.g.:
  - Linux/macOS: `rg -n "Autofit" ~/.nuget/packages/gembox.spreadsheet/2025.12.105/lib/**/GemBox.Spreadsheet.xml`
- If the API is unclear, scan namespaces and remarks/examples in the doc XML before coding. E.g.:
  - Linux/macOS: `rg -n "namespace GemBox|Drawing|PivotTables" ~/.nuget/packages/gembox.spreadsheet/2025.12.105/lib/**/GemBox.Spreadsheet.xml`

# Online search
If you don't find relevant docs via CLI, and you have network access, search online:
1. Open a relevant official example page, as examples listed below provide the most information. E.g, if you need custom fonts in GemBox.Document, the base URL is "https://www.gemboxsoftware.com/document/examples/". The specific example that mentions fonts is "fonts/103", so open "https://www.gemboxsoftware.com/document/examples/fonts/103" page.
2. If examples are insufficient, search the official API documentation of a specific component. 
   E.g. GemBox.Spreadsheet online search filter: "site:https://www.gemboxsoftware.com/spreadsheet/docs"

# Validation
Once you are finished, validate the code by compiling the project. If there are errors related to GemBox API usage, modify the code accordingly. Ignore compilation errors that are not related to GemBox or not caused by your edits.

## GemBox.Spreadsheet examples URLs
BASE: https://www.gemboxsoftware.com/spreadsheet/examples/
SPREADSHEET EXAMPLES:
asp-net-core-create-excel/5601
asp-net-excel-export-gridview/5101
asp-net-excel-viewer/6012
blazor-create-excel/5602
c-sharp-convert-excel-to-image/405
c-sharp-convert-excel-to-pdf/404
c-sharp-create-write-excel-file/402
c-sharp-excel-range/204
c-sharp-export-datatable-dataset-to-excel/501
c-sharp-export-excel-to-datatable/502
c-sharp-microsoft-office-interop-excel-automation/6004
c-sharp-open-read-excel-file/401
c-sharp-read-write-csv/122
c-sharp-vb-net-convert-excel-html/117
c-sharp-vb-net-create-excel-chart-sheet/302
c-sharp-vb-net-create-excel-tables/119
c-sharp-vb-net-excel-chart-formatting/306
c-sharp-vb-net-excel-conditional-formatting/105
c-sharp-vb-net-excel-form-controls/123
c-sharp-vb-net-excel-row-column-autofit/108
c-sharp-vb-net-excel-style-formatting/202
c-sharp-vb-net-import-export-excel-datagridview/5301
c-sharp-vb-net-print-excel/451
c-sharp-vb-net-xls-decryption/707
convert-excel-table-range-vb-net-c-sharp/6011
convert-import-write-json-to-excel-vb-net-c-sharp/6010
convert-xls-xlsx-ods-csv-html-net-c-sharp/6001
create-excel-charts/301
create-excel-file-maui/5802
create-excel-file-xamarin/5801
create-excel-files-c-sharp/6013
create-excel-pdf-on-azure/5901
create-excel-pdf-on-docker-net-core/5902
create-excel-pdf-on-linux-net-core/5701
create-excel-pivot-tables/114
create-read-write-excel-classic-asp/5501
create-read-write-excel-php/5502
create-read-write-excel-python/5503
edit-save-excel-template/403
excel-autofilter/112
excel-calculations-c-sharp-vb-net/6022
excel-cell-comments/208
excel-cell-data-types/201
excel-cell-hyperlinks/207
excel-cell-inline-formatting/203
excel-cell-number-format/205
excel-chart-components/304
excel-charts-guide-c-sharp/6019
excel-data-validation/106
excel-defined-names/214
excel-encryption/701
excel-find-replace-text/109
excel-formulas/206
excel-freeze-split-panes/102
excel-grouping/101
excel-header-footer-formatting/6021
excel-headers-footers/210
excel-images/209
excel-performance-metrics/5401
excel-preservation/801
excel-print-title-area/104
excel-print-view-options/103
excel-properties/107
excel-shapes/211
excel-sheet-copy-delete/111
excel-sheet-protection/704
excel-textboxes/212
excel-workbook-protection/705
excel-wpf/5201
excel-xlsx-digital-signature/706
fixed-columns-width-text/118
fonts/115
free-trial-professional/1001
getting-started/601
merge-excel-cells-c-sharp-vb-net/213
open-read-excel-files-c-sharp/6009
pdf-digital-signature/703
pdf-encryption/702
progress-reporting-and-cancellation/121
protecting-excel-data-c-sharp/6020
right-to-left-text/120
sort-data-excel/113
unit-conversion-excel/116
vba-macros/124
xlsx-write-protection/708

## GemBox.Document examples
BASE: https://www.gemboxsoftware.com/document/examples/
DOCUMENT EXAMPLES:
asp-net-core-create-word-docx-pdf/5601
asp-net-create-generate-export-pdf-word/5101
auto-hyphenation/109
blazor-create-word/5602
c-sharp-convert-aspx-to-pdf/6002
c-sharp-convert-html-to-pdf/307
c-sharp-convert-pdf-to-docx/308
c-sharp-convert-word-to-from-html/105
c-sharp-convert-word-to-image/306
c-sharp-convert-word-to-pdf/304
c-sharp-convert-word-to-pdf/6007
c-sharp-microsoft-office-interop-word-automation/6005
c-sharp-read-extract-pdf-tables/305
c-sharp-vb-net-create-generate-pdf/6004
c-sharp-vb-net-create-update-word-toc/207
c-sharp-vb-net-create-word-form/701
c-sharp-vb-net-create-write-word-file/302
c-sharp-vb-net-docx-encryption/1102
c-sharp-vb-net-edit-save-word-template/303
c-sharp-vb-net-find-replace-word/405
c-sharp-vb-net-mail-merge-word/901
c-sharp-vb-net-manipulate-content-word/403
c-sharp-vb-net-open-read-word-file/301
c-sharp-vb-net-pdf-digital-signature/1104
c-sharp-vb-net-pdf-encryption/1103
c-sharp-vb-net-print-word/351
c-sharp-vb-net-read-word-form/702
c-sharp-vb-net-update-word-form/703
c-sharp-vb-net-word-performance/5401
cloning/501
combine-word-file-c-sharp-vb-net/502
content-controls/106
create-read-write-word-pdf-classic-asp/5501
create-read-write-word-pdf-php/5502
create-read-write-word-pdf-python/5503
create-table-in-word-csharp/1201
create-word-file-maui/5802
create-word-file-xamarin/5801
create-word-pdf-on-azure-functions-app-service/5901
create-word-pdf-on-docker-net-core/5902
create-word-pdf-on-linux-net-core/5701
customize-mail-merge/904
docx-digital-signature/1106
docx-write-protection/1101
extract-individual-pages/112
find-replace-word-csharp/6003
fonts/103
free-trial-professional/1301
generate-barcodes-qr-codes-csharp-vb-net/217
getting-started/801
html-to-pdf-converter-csharp/6001
iterating/503
load-process-pdf-csharp/6006
mail-merge-clear-options/905
mail-merge-if-fields/902
mail-merge-labels/909
mail-merge-pictures/908
mail-merge-ranges/903
merge-barcodes-qr-codes/907
nested-mail-merge/906
progress-reporting-and-cancellation/108
restrict-editing/1105
right-to-left-text/107
unit-conversion/104
vba-macros/111
word-bookmarks-hyperlinks/204
word-breaks/205
word-character-formatting/601
word-charts/213
word-comments/215
word-editor-asp-net-mvc/5102
word-editor-windows-forms/5301
word-editor-wpf/5203
word-fields/206
word-footnote-endnote/212
word-header-footer/208
word-lists/603
word-merge-cells/1203
word-page-setup/209
word-paragraph-formatting/602
word-pictures/201
word-preservation/1001
word-properties/211
word-shapes/203
word-styles/604
word-table-formatting/1204
word-table-styles/1205
word-textboxes/202
word-track-changes/216
word-view-options/210
word-watermarks/214
word-wpf-xpsdocument-imagesource/5201

## GemBox.Pdf examples URLs
BASE: https://www.gemboxsoftware.com/pdf/examples/
PDF EXAMPLES:
add-export-images-pdf/6001
asp-net-core-create-pdf/1401
basic-pdf-objects/402
blazor-create-pdf/1402
c-sharp-convert-pdf-to-image/208
c-sharp-export-pdf-interactive-form-data/503
c-sharp-pdf-associated-files/704
c-sharp-pdf-embedded-files/701
c-sharp-pdf-file-attachment-annotations/702
c-sharp-pdf-portfolios/703
c-sharp-vb-add-pdf-shapes-paths/306
c-sharp-vb-export-import-images-to-pdf/206
c-sharp-vb-net-create-write-pdf-file/209
c-sharp-vb-net-merge-pdf/201
c-sharp-vb-net-ocr-pdf/408
c-sharp-vb-net-pdf-advanced-electronic-signature-pades/1103
c-sharp-vb-net-pdf-bookmarks-outlines/301
c-sharp-vb-net-pdf-digital-signature-pkcs11-cryptoki/1104
c-sharp-vb-net-pdf-digital-signature-validation/1105
c-sharp-vb-net-pdf-digital-signature/1102
c-sharp-vb-net-pdf-pages/401
c-sharp-vb-net-read-pdf/205
c-sharp-vb-net-redact-content-pdf/410
c-sharp-vb-net-split-pdf/202
c-sharp-vb-pdf-hyperlinks/308
charts-barcodes-slides/309
cloning-pdf-pages/203
convert-pdf-image-png-jpg-csharp/6004
create-pdf-file-maui/1502
create-pdf-file-xamarin/1501
create-pdf-interactive-form-fields/505
create-pdf-on-azure-functions-app-service/1601
create-pdf-on-docker-net-core/1602
create-pdf-on-linux-net-core/1301
decrypt-encrypt-pdf-file/1101
extract-content-pdf/6005
fill-in-pdf-interactive-form/502
flatten-pdf-interactive-form-fields/506
fonts/404
free-trial-professional/601
getting-started/101
incremental-update/204
interactive-form-actions/504
pdf-content-formatting/307
pdf-content-groups/409
pdf-content-streams-and-resources/403
pdf-digital-signature-workflows/1106
pdf-document-properties/302
pdf-form-xobjects/405
pdf-header-footer/304
pdf-marked-content/407
pdf-security-c-sharp/6003
pdf-table-of-contents/310
pdf-viewer-preferences/303
pdf-watermarks/305
pdf-xpsdocument-wpf/1001
png-jpg-images-to-pdf/210
print-pdf-c-sharp/6002
read-merge-split-pdf-classic-asp/1201
read-merge-split-pdf-php/1202
read-merge-split-pdf-python/1203
read-pdf-interactive-form-fields/501

## GemBox.Presentation examples URLs
BASE: https://www.gemboxsoftware.com/presentation/examples/
PRESENTATION EXAMPLES:
asp-net-core-create-powerpoint-pptx-pdf/2001
asp-net-powerpoint-export/1601
blazor-create-powerpoint/2002
c-sharp-clone-slides/205
c-sharp-convert-powerpoint-to-image/207
c-sharp-convert-powerpoint-to-pdf/204
c-sharp-print-powerpoint/251
c-sharp-vb-net-create-write-powerpoint/202
c-sharp-vb-net-find-replace-text-powerpoint/206
c-sharp-vb-net-open-read-powerpoint/201
c-sharp-vb-net-powerpoint-performance/1501
c-sharp-vb-net-powerpoint-slide-notes/411
c-sharp-vb-net-powerpoint-slides/401
c-sharp-vb-net-pptx-encryption/803
c-sharp-vb-net-pptx/203
create-format-powerpoint-tables-csharp/6001
create-powerpoint-file-maui/2102
create-powerpoint-file-xamarin/2101
create-powerpoint-pdf-on-azure-functions-app-service/2201
create-powerpoint-pdf-on-docker-net-core/2202
create-powerpoint-pdf-on-linux-net-core/1901
create-read-write-powerpoint-classic-asp/1801
create-read-write-powerpoint-php/1802
create-read-write-powerpoint-python/1803
fonts/503
free-trial-professional/901
getting-started/101
pdf-digital-signature/802
pdf-encryption/801
powerpoint-audio-video/406
powerpoint-character-formatting/304
powerpoint-charts/412
powerpoint-comments/408
powerpoint-header-footer/407
powerpoint-hyperlinks/409
powerpoint-list-formatting/305
powerpoint-load-html/208
powerpoint-paragraph-formatting/303
powerpoint-pictures/405
powerpoint-placeholders/402
powerpoint-preservation/701
powerpoint-properties/410
powerpoint-shape-formatting/301
powerpoint-shapes/403
powerpoint-slide-transition/501
powerpoint-slideshow/502
powerpoint-table-formatting/602
powerpoint-tables/601
powerpoint-textbox-formatting/302
powerpoint-textboxes/404
powerpoint-wpf/1701
pptx-digital-signature/805
pptx-modify-protection/804
right-to-left-text/505
unit-conversion/504
vba-macros/506

## GemBox.Email examples URLs
BASE: https://www.gemboxsoftware.com/email/examples/
EMAIL EXAMPLES:
add-calendar-to-mail-message/903
asp-net-core-mail-message/5101
authenticate-using-oauth-c-sharp-vb/109
blazor-mail-message/5102
c-sharp-convert-email-to-pdf/107
c-sharp-create-send-emails/6001
c-sharp-imap-client/301
c-sharp-oauth-microsoft365-gmail/6002
c-sharp-outlook-msg-eml-mht/106
c-sharp-pop3-client/701
c-sharp-send-bulk-email/804
c-sharp-send-word-as-email/108
c-sharp-smtp-client/801
c-sharp-validate-email/401
c-sharp-vb-net-create-email/601
c-sharp-vb-net-load-email/105
c-sharp-vb-net-mail-merge-datatable/501
c-sharp-vb-net-save-email/104
c-sharp-vb-net-search-emails/308
c-sharp-vb-net-sign-email/1202
create-and-save-calendar/901
folder-flags/305
free-trial-professional/1101
get-email-message-maui/2002
get-email-message-xamarin/2001
getting-started/201
headers/604
imap-email-folders/302
imap-idle/310
list-email-messages-imap/303
list-email-messages-pop/702
load-calendar/902
mailbox-info/703
manipulate-messages-exchange-ews/1002
manipulate-messages-microsoft-graph/3002
mbox/605
message-flags/306
message-headers-imap/307
message-headers-pop/705
modify-folders-exchange-ews/1003
modify-folders-microsoft-graph/3003
receive-read-email-c-sharp-vb/102
reply-forward-email-c-sharp-vb-net/103
search-email-exchange-ews/1004
search-email-microsoft-graph/3004
send-email-c-sharp-vb-asp-net/101
send-email-exchange-ews/1001
send-email-microsoft-graph/3001
send-html-email-with-attachment-c-sharp-vb-net/603
ssl-certificate-validation-imap/309
ssl-certificate-validation-pop/706
ssl-certificate-validation-smtp/803
upload-email-message-exchange/1005
upload-email-message-imap/311
upload-email-message-microsoft-graph/3005

## GemBox.Imaging examples URLs
BASE: https://www.gemboxsoftware.com/imaging/examples/
IMAGING EXAMPLES:
asp-net-core-crop-image/2101
c-sharp-vb-net-apply-filter-to-image/203
c-sharp-vb-net-convert-image/202
c-sharp-vb-net-crop-image/302
c-sharp-vb-net-merge-split-frames/204
c-sharp-vb-net-read-image/201
c-sharp-vb-net-resize-image/301
c-sharp-vb-net-rotate-flip-image/303
free-trial-professional/1001
getting-started/101
load-edit-save-image-on-linux-net-core/2103
read-image-on-docker-net-core/2102
rotate-flip-image-maui/2105
rotate-flip-image-xamarin/2104

## GemBox.PdfViewer examples URLs
BASE: https://www.gemboxsoftware.com/pdfviewer/examples/
PDFVIEWER EXAMPLES:
angular-pdf-viewer/205
asp-net-core-pdf-viewer/201
demo/301
free-trial-professional/107
getting-started/101
how-to-digitally-sign-pdf/108
navigation-and-zooming/102
react-pdf-viewer/204
search/103
svelte-pdf-viewer/206
themes/104
themes/105
ui-customization/106
vanilla-js-pdf-viewer/202
vue-js-pdf-viewer/203
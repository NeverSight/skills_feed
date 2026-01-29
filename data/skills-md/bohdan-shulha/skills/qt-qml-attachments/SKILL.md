---
name: qt-qml-attachments
description: >-
  Guidance for Qt/QML chat attachment rows and message bubbles: Flow wrapping, image/file chip alignment, right/left alignment, and width/height sizing quirks. Use when fixing attachment layouts that stack vertically, wrap incorrectly, or appear full-width in Qt Quick/QML.
---

# Qt Qml Attachments

## Overview

Fix and tune QML chat attachment layouts so chips/images wrap in rows, align to the correct side, preserve ordering, and keep message bubbles from stretching full width.

## Quick Diagnosis

- If attachments stack vertically, the Flow likely has no usable width. Avoid binding `Flow.width` to its own `implicitWidth`.
- If the row aligns left when it should align right, check `layoutDirection`, anchors, and model order.
- If bubbles appear full-width, clamp `Layout.preferredWidth` and Flow width to a max ratio or fixed pixel cap.

## Flow Width & Wrap

- Give `Flow` an explicit width based on available space (e.g., `chatArea.width - margins`).
- Use `Math.max(0, ...)` to avoid negative widths during resize.
- For the container height, prefer `implicitHeight` over `height` when it’s driven by a Flow.

Example:

```qml
Item {
    implicitHeight: attachmentsFlow.implicitHeight
    Flow {
        id: attachmentsFlow
        width: Math.max(0, Math.min(chatArea.width - 120, chatArea.width * 0.65))
        spacing: 8
    }
}
```

## Right-Aligning Attachments

- Set `anchors.right: parent.right` on the Flow container.
- Use `layoutDirection: Qt.RightToLeft` for a right-aligned wrap.
- Preserve order: if you want **newest on the right**, keep the model order and use `RightToLeft`.
- Preserve chronological left-to-right: reverse the model when using `RightToLeft`.

Order rules:

- Model is oldest → newest: `RightToLeft` shows newest on the right.
- Model is newest → oldest: reverse it or switch to `LeftToRight`.

## Bubble Width Caps

- Clamp `Layout.preferredWidth` so bubbles don’t stretch full width, even for long text or many attachments.
- Use a ratio (e.g., `0.6–0.7`) or a fixed max pixel value.

Example:

```qml
Rectangle {
    Layout.preferredWidth: Math.min(msgText.implicitWidth + 24, chatArea.width * 0.65)
    Layout.preferredHeight: msgText.height + 16
}
```

## Clipboard Image Attachments (Qt)

- Always read clipboard image data on the GUI thread (`qApp->thread()`), otherwise `QClipboard` may return empty.
- Prefer `QClipboard::image()` but add fallbacks: `application/x-qt-image`, then `mime->imageData()` to `QImage` or `QPixmap`.
- Normalize image format and colorspace before saving to PNG to avoid libpng/ICC crashes.
- Save to a temp attachment folder and return a file path for QML to attach.

Example:

```cpp
if (QThread::currentThread() != qApp->thread())
    return "";

QImage image = clipboard->image();
if (image.isNull() && mime->hasFormat("application/x-qt-image")) {
    QByteArray raw = mime->data("application/x-qt-image");
    QDataStream stream(&raw, QIODevice::ReadOnly);
    stream >> image;
    if (stream.status() != QDataStream::Ok)
        image = QImage();
}
if (image.isNull()) {
    QVariant data = mime->imageData();
    if (data.canConvert<QImage>())
        image = data.value<QImage>();
    else if (data.canConvert<QPixmap>())
        image = data.value<QPixmap>().toImage();
}
if (image.isNull())
    return "";

if (image.format() != QImage::Format_RGBA8888)
    image = image.convertToFormat(QImage::Format_RGBA8888);
image.setColorSpace(QColorSpace::SRgb);
image = image.copy();
```

## Common Pitfalls

- `Flow.width: implicitWidth` often collapses to a single-column layout.
- Using `height` instead of `implicitHeight` on containers causes clipping or over-expansion.
- Right alignment without `layoutDirection` keeps the wrap left-biased.
- Long filenames: cap chip width with `Text.elide` and a fixed max width.

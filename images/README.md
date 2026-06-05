# images/ — figure assets for the Shlav Alef MCQ app

Images placed here ship with the PWA and are runtime-cached by the service
worker (cached on first view, then available offline).

## How to attach an image to a question

In any `Question Bank - *.md`, add ONE markdown image line **between the stem
line and the option list** (optional — leave it out for text-only questions):

```
**N-I-14.1** *[Ch14 · Flap classification]* Which flap is shown?
![Reverse-flow radial forearm flap](images/N-I-14-1.jpg)
- A. ...
- B. ...
- C. ...
- D. ...
```

- The path must point inside this folder (`images/<file>`).
- The alt text becomes the on-screen **caption** (optional — `![](images/x.jpg)` works too).
- `parse_bank.py` emits optional `image` (and `imgcap`) fields on the question
  object; `index.html` renders the figure under the stem with tap-to-zoom.
- Text-only questions are unaffected — both fields are simply absent.

## Naming convention

`<question-id-with-dots-as-dashes>.<ext>` — keeps files 1:1 with question IDs
and globally unique, mirroring the ID scheme.

- Neligan: `N-I-14-1.jpg`  (question `N-I-14.1`)
- Bologna: `B113-2.jpg`    (question `B113.2`)
- Sabiston: `S11-3.jpg`
- Shared figure used by several Qs: `fig-fitzpatrick.jpg` (descriptive slug).

Prefer `.jpg` for photos, `.png`/`.svg` for diagrams. Keep files small
(long edge ~1200 px, < ~300 KB) so the PWA stays light.

## Copyright

This repo is **public**. Do **not** commit raw textbook scans (Neligan /
Bologna / Sabiston figures are copyrighted). Use original/redrawn schematic
diagrams, openly-licensed clinical images, or describe the finding in the stem
text when a figure isn't strictly required. When an image is genuinely needed
for recognition (lesion morphology, flap geometry), prefer a redrawn diagram or
a properly-licensed photo.

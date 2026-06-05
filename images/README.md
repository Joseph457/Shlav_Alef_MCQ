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

## Usage — personal study tool

This app is **Yossi's personal exam-prep tool**, so use the **actual Neligan /
Bologna / Sabiston figures**: crop the specific figure from the chapter PDF
(e.g. with `pdftoppm`/`pdfimages` or a screenshot), name it per the convention
above, and drop the file in this folder.

Note: the GitHub repo is currently **public**, so files here are reachable by
anyone with the URL. If true privacy is wanted, make the repo private (GitHub
Pages then requires a paid plan) — separate decision, doesn't affect this folder.

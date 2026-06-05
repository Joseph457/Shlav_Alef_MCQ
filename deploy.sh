#!/usr/bin/env bash
# One-command deploy for the Shlav Alef MCQ app.
#
# Run from inside a FRESH clone of Joseph457/Shlav_Alef_MCQ:
#   git clone --depth 1 "https://<PAT>@github.com/Joseph457/Shlav_Alef_MCQ.git" repo
#   cd repo
#   GH_PAT=<PAT> PROJECT="/sessions/.../Studying To Shlav Alef" bash deploy.sh
#
# It append-merges any NEW bank items into questions.json (parse_bank.py aborts if a
# bank reads truncated -- the OneDrive gotcha), bumps the three cache markers, commits,
# and pushes. The PAT is used inline for the push only and is never written to disk.
set -euo pipefail
GH_PAT="${GH_PAT:?paste the fine-grained PAT: GH_PAT=...}"
PROJECT="${PROJECT:?set PROJECT to the bank folder, e.g. PROJECT=\"/sessions/.../Studying To Shlav Alef\"}"
REPO="github.com/Joseph457/Shlav_Alef_MCQ.git"

# 1. Merge new items (aborts on truncated/short reads)
python3 parse_bank.py questions.json "$PROJECT"/Question\ Bank\ -\ *.md

# 2. Cache-bust: bump cache name (sw.js) + ?b= tag (index.html), kept in sync, and VERSION minor
cur=$(grep -oE 'shlav-mcq-v[0-9]+' sw.js | grep -oE '[0-9]+')
next=$((cur+1))
sed -i "s/shlav-mcq-v${cur}/shlav-mcq-v${next}/" sw.js
sed -i "s/questions\.json?b=${cur}/questions.json?b=${next}/" index.html
ver=$(grep -oE 'VERSION="v[0-9]+\.[0-9]+"' index.html | grep -oE '[0-9]+\.[0-9]+')
maj=${ver%.*}; min=${ver#*.}; newver="v${maj}.$((min+1))"
sed -i "s/VERSION=\"v${ver}\"/VERSION=\"${newver}\"/" index.html

# 3. Commit + push (token inline, redacted in output, never persisted)
total=$(python3 -c "import json;print(len(json.load(open('questions.json'))))")
git add questions.json sw.js index.html
git -c user.email="yossi.levi15@gmail.com" -c user.name="Yossi Levi" \
    commit -q -m "Deploy: ${total} items, cache v${next}, ${newver}"
git push "https://${GH_PAT}@${REPO}" HEAD:main 2>&1 | sed -E 's#//[^@]*@#//[REDACTED]@#'
echo "DEPLOYED: ${total} items | cache v${next} | ?b=${next} | ${newver}"
echo "Tell Yossi to fully close & reopen the home-screen app (or load ?b=${next})."

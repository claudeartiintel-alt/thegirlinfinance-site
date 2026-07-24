# The Girl in Finance — website

The live site for **thegirlinfinance.com**. Plain static HTML/CSS — no build step.

## Pages
- `index.html` — home
- `blog.html` — Learn library
- `work-with-me.html` — Work with me
- `newsletter.html` — Newsletter page (a fixed wrapper that displays the latest issue)
- `issue.html` — **the current weekly issue** (managed automatically — see below)
- `thank-you.html` — form confirmation page
- `styles.css`, `assets/` — shared styling and brand images

## How the weekly newsletter publishes itself
1. A scheduled task (outside this repo) researches the week and **emails** the
   "Friday Edition" from the `eric0649@agentmail.to` inbox, every Friday morning.
2. The GitHub Action in `.github/workflows/publish-newsletter.yml` runs every
   Friday at **05:00 UTC (08:00 Bahrain)**. It calls the AgentMail API, takes the
   latest issue's HTML, and writes it to `issue.html`, then commits it.
3. Netlify is connected to this repo, so that commit **auto-deploys** — the public
   newsletter page updates on its own.

`newsletter.html` never changes; it just frames whatever `issue.html` currently holds.

## The one secret
The Action needs `AGENTMAIL_API_KEY` — add it under
**Settings → Secrets and variables → Actions → New repository secret**.
It lives only in GitHub's encrypted store; it is never committed to the repo.
Create the key (inbox-scoped to `eric0649@agentmail.to`) at https://console.agentmail.to.

## Publishing a manual change
Edit a file and `git push` — Netlify deploys within about a minute.

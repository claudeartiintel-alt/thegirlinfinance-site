#!/usr/bin/env python3
"""Fetch the latest 'Friday Edition' issue from AgentMail and write it to issue.html.
Runs inside the GitHub Action. The only secret it needs (AGENTMAIL_API_KEY) is read
from the environment, which GitHub injects from the repo's encrypted Secrets store.
It never leaves anything sensitive in the repo.
"""
import os, sys, json, urllib.request, urllib.parse

KEY   = os.environ.get("AGENTMAIL_API_KEY")
INBOX = os.environ.get("AGENTMAIL_INBOX", "eric0649@agentmail.to")
BASE  = "https://api.agentmail.to/v0"

if not KEY:
    print("::error::AGENTMAIL_API_KEY is not set. Add it under Settings -> Secrets and variables -> Actions.")
    sys.exit(1)

def api(path):
    req = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode())

inbox_q = urllib.parse.quote(INBOX, safe="")

# 1) Find the most recent sent message whose subject contains "Friday Edition".
q = urllib.parse.urlencode({"labels": "sent", "subject": "Friday Edition", "limit": "5", "ascending": "false"})
try:
    listing = api("/inboxes/%s/messages?%s" % (inbox_q, q))
except Exception as ex:
    print("::error::Could not list messages: %s" % ex)
    sys.exit(1)

msgs = listing.get("messages") or listing.get("data") or []
if not msgs:
    print("No 'Friday Edition' message found yet - leaving issue.html unchanged.")
    sys.exit(0)

top = msgs[0]
mid = top.get("message_id") or top.get("id")
if not mid:
    print("::error::Message has no id field: %s" % json.dumps(top)[:300])
    sys.exit(1)

# 2) Fetch the full message to get its HTML body.
try:
    msg = api("/inboxes/%s/messages/%s" % (inbox_q, urllib.parse.quote(str(mid), safe="")))
except Exception as ex:
    print("::error::Could not fetch message %s: %s" % (mid, ex))
    sys.exit(1)

html = msg.get("html") or msg.get("body_html") or msg.get("html_body") or ""
if not html.strip():
    print("Latest message had no HTML body - leaving issue.html unchanged.")
    sys.exit(0)

with open("issue.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Wrote issue.html from message %s (subject: %s)" % (mid, top.get("subject", "")))

#!/usr/bin/env python3
“””
fetch_feeds.py — run by GitHub Actions every 30 minutes.
Fetches all 76 CTI RSS/Atom feeds, strips HTML, saves feeds.json.
No API keys required. Handles both RSS 2.0 and Atom formats.
“””

import json
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser

import feedparser
import requests

# ── FEED CATALOGUE ────────────────────────────────────────────────────────────

FEEDS = [{“url”: “https://www.cisa.gov/cybersecurity-advisories/all.xml”, “src”: “CISA”, “cat”: “gov”}, {“url”: “https://www.cisa.gov/uscert/ncas/alerts.xml”, “src”: “US-CERT Alerts”, “cat”: “gov”}, {“url”: “https://isc.sans.edu/rssfeed.xml”, “src”: “SANS ISC”, “cat”: “gov”}, {“url”: “https://blogs.jpcert.or.jp/en/atom.xml”, “src”: “JPCERT”, “cat”: “gov”}, {“url”: “https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml”, “src”: “NVD / NIST CVEs”, “cat”: “gov”}, {“url”: “https://www.ncsc.gov.uk/feeds/all.xml”, “src”: “NCSC UK”, “cat”: “gov”}, {“url”: “https://www.cyber.gov.au/feed”, “src”: “ACSC Australia”, “cat”: “gov”}, {“url”: “https://www.enisa.europa.eu/news/enisa-news/RSS”, “src”: “ENISA (EU)”, “cat”: “gov”}, {“url”: “https://www.bleepingcomputer.com/feed/”, “src”: “BleepingComputer”, “cat”: “news”}, {“url”: “https://feeds.feedburner.com/TheHackersNews”, “src”: “The Hacker News”, “cat”: “news”}, {“url”: “https://www.darkreading.com/rss.xml”, “src”: “Dark Reading”, “cat”: “news”}, {“url”: “https://www.securityweek.com/rss”, “src”: “SecurityWeek”, “cat”: “news”}, {“url”: “https://www.zdnet.com/topic/security/rss.xml”, “src”: “ZDNet Security”, “cat”: “news”}, {“url”: “https://www.infosecurity-magazine.com/rss/news/”, “src”: “InfoSecurity Mag”, “cat”: “news”}, {“url”: “https://techcrunch.com/author/zack-whittaker/feed/”, “src”: “TechCrunch Sec”, “cat”: “news”}, {“url”: “https://therecord.media/feed/”, “src”: “The Record”, “cat”: “news”}, {“url”: “https://gbhackers.com/feed/”, “src”: “GBHackers”, “cat”: “news”}, {“url”: “https://securityaffairs.com/feed”, “src”: “Security Affairs”, “cat”: “news”}, {“url”: “https://cyware.com/rss-feed/”, “src”: “Cyware”, “cat”: “news”}, {“url”: “https://www.wired.com/feed/category/security/latest/rss”, “src”: “Wired Security”, “cat”: “news”}, {“url”: “https://cyberscoop.com/feed/”, “src”: “CyberScoop”, “cat”: “news”}, {“url”: “https://www.scmagazine.com/feed”, “src”: “SC Magazine”, “cat”: “news”}, {“url”: “https://www.helpnetsecurity.com/feed/”, “src”: “Help Net Security”, “cat”: “news”}, {“url”: “https://www.csoonline.com/feed/”, “src”: “CSO Online”, “cat”: “news”}, {“url”: “https://unit42.paloaltonetworks.com/feed/”, “src”: “Unit 42”, “cat”: “research”}, {“url”: “https://research.checkpoint.com/feed/”, “src”: “CheckPoint Research”, “cat”: “research”}, {“url”: “https://blog.talosintelligence.com/rss/”, “src”: “Cisco Talos”, “cat”: “research”}, {“url”: “https://blog.google/threat-analysis-group/rss”, “src”: “Google TAG”, “cat”: “research”}, {“url”: “https://thedfirreport.com/feed/”, “src”: “DFIR Report”, “cat”: “research”}, {“url”: “https://posts.specterops.io/feed”, “src”: “SpecterOps”, “cat”: “research”}, {“url”: “https://asec.ahnlab.com/en/feed/”, “src”: “AhnLab ASEC”, “cat”: “research”}, {“url”: “https://labs.sentinelone.com/feed/”, “src”: “SentinelOne Labs”, “cat”: “research”}, {“url”: “https://www.recordedfuture.com/feed/”, “src”: “Recorded Future”, “cat”: “research”}, {“url”: “https://dragos.com/feed/”, “src”: “Dragos”, “cat”: “research”}, {“url”: “https://forensicitguy.github.io/feed.xml”, “src”: “ForensicITGuy”, “cat”: “research”}, {“url”: “https://www.redcanary.com/blog/feed/”, “src”: “Red Canary”, “cat”: “research”}, {“url”: “https://www.greynoise.io/blog/rss.xml”, “src”: “GreyNoise”, “cat”: “research”}, {“url”: “https://bushidotoken.blogspot.com/feeds/posts/default”, “src”: “BushidoToken”, “cat”: “research”}, {“url”: “https://citizenlab.org/category/lab-news/feed/”, “src”: “Citizen Lab”, “cat”: “research”}, {“url”: “https://bellingcat.com/feed/”, “src”: “Bellingcat”, “cat”: “research”}, {“url”: “https://www.mandiant.com/resources/blog/rss.xml”, “src”: “Mandiant”, “cat”: “research”}, {“url”: “https://msrc-blog.microsoft.com/feed/”, “src”: “Microsoft MSRC”, “cat”: “research”}, {“url”: “https://securelist.com/feed/”, “src”: “Kaspersky Securelist”, “cat”: “research”}, {“url”: “https://www.welivesecurity.com/feed/”, “src”: “ESET WeLiveSecurity”, “cat”: “research”}, {“url”: “https://blog.malwarebytes.com/feed/”, “src”: “Malwarebytes Labs”, “cat”: “research”}, {“url”: “https://www.elastic.co/security-labs/rss/feed.xml”, “src”: “Elastic Security”, “cat”: “research”}, {“url”: “https://blog.sekoia.io/feed/”, “src”: “Sekoia”, “cat”: “research”}, {“url”: “https://intezer.com/feed/”, “src”: “Intezer”, “cat”: “research”}, {“url”: “https://news.sophos.com/en-us/feed/”, “src”: “Sophos”, “cat”: “vendor”}, {“url”: “https://www.crowdstrike.com/blog/feed/”, “src”: “CrowdStrike”, “cat”: “vendor”}, {“url”: “https://feeds.trendmicro.com/TrendMicroResearch”, “src”: “Trend Micro”, “cat”: “vendor”}, {“url”: “https://www.tenable.com/blog/feed”, “src”: “Tenable”, “cat”: “vendor”}, {“url”: “https://blog.qualys.com/feed/”, “src”: “Qualys”, “cat”: “vendor”}, {“url”: “https://www.huntress.com/blog/rss.xml”, “src”: “Huntress”, “cat”: “vendor”}, {“url”: “https://expel.io/feed/”, “src”: “Expel”, “cat”: “vendor”}, {“url”: “https://cybersecurity.att.com/site/blog-all-rss”, “src”: “AT&T Cybersec”, “cat”: “vendor”}, {“url”: “https://www.proofpoint.com/us/blog/feed”, “src”: “Proofpoint”, “cat”: “vendor”}, {“url”: “https://www.secureworks.com/rss?feed=blog”, “src”: “Secureworks”, “cat”: “vendor”}, {“url”: “https://www.tripwire.com/state-of-security/feed/”, “src”: “Tripwire”, “cat”: “vendor”}, {“url”: “https://www.blackhillsinfosec.com/feed/”, “src”: “BHIS”, “cat”: “vendor”}, {“url”: “https://blog.rapid7.com/rss/”, “src”: “Rapid7”, “cat”: “vendor”}, {“url”: “https://www.cybereason.com/blog/rss.xml”, “src”: “Cybereason”, “cat”: “vendor”}, {“url”: “https://stairwell.com/feed/atom/”, “src”: “Stairwell”, “cat”: “vendor”}, {“url”: “https://labs.withsecure.com/feed”, “src”: “WithSecure Labs”, “cat”: “vendor”}, {“url”: “https://www.binarydefense.com/feed/”, “src”: “Binary Defense”, “cat”: “vendor”}, {“url”: “https://krebsonsecurity.com/feed/”, “src”: “Krebs on Security”, “cat”: “community”}, {“url”: “https://www.schneier.com/blog/atom.xml”, “src”: “Schneier on Security”, “cat”: “community”}, {“url”: “https://rss.packetstormsecurity.com/files/”, “src”: “Packet Storm”, “cat”: “community”}, {“url”: “https://hackerone.com/news.rss”, “src”: “HackerOne”, “cat”: “community”}, {“url”: “https://www.sans.org/blog/feed/”, “src”: “SANS Blog”, “cat”: “community”}, {“url”: “https://www.exploit-db.com/rss.xml”, “src”: “Exploit-DB”, “cat”: “community”}, {“url”: “https://portswigger.net/daily-swig/rss”, “src”: “Daily Swig”, “cat”: “community”}, {“url”: “https://grahamcluley.com/feed/”, “src”: “Graham Cluley”, “cat”: “community”}, {“url”: “https://danielmiessler.com/feed/”, “src”: “Daniel Miessler”, “cat”: “community”}, {“url”: “https://www.troyhunt.com/rss/”, “src”: “Troy Hunt”, “cat”: “community”}, {“url”: “https://risky.biz/feeds/risky-business/”, “src”: “Risky Business”, “cat”: “community”}]

HEADERS = {
“User-Agent”: “CTI-Radar/2.0 (+https://github.com/spac3gh0st00/Cybersecurity-Threat-Intelligence-Dashboard)”,
“Accept”: “application/rss+xml, application/atom+xml, application/xml, text/xml, */*”,
}
TIMEOUT    = 15   # seconds per feed
ARTICLES   = 3    # articles to keep per feed
MAX_DESC   = 300  # characters

# ── HTML STRIPPER ─────────────────────────────────────────────────────────────

class _Stripper(HTMLParser):
def **init**(self):
super().**init**()
self.parts = []
def handle_data(self, d):
self.parts.append(d)

def strip_html(text: str) -> str:
if not text:
return “”
s = _Stripper()
try:
s.feed(text)
except Exception:
pass
out = “ “.join(s.parts)
return re.sub(r”\s+”, “ “, out).strip()

# ── FETCH & PARSE ─────────────────────────────────────────────────────────────

def fetch_feed(feed: dict) -> tuple[list[dict], bool]:
“”“Returns (articles, success).”””
try:
resp = requests.get(feed[“url”], headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()
parsed = feedparser.parse(resp.content)
except Exception as e:
print(f”  FAIL  {feed[‘src’]}: {e}”)
return [], False

```
if parsed.bozo and not parsed.entries:
    print(f"  SKIP  {feed['src']}: bozo feed, no entries")
    return [], False

items = []
for entry in parsed.entries[:ARTICLES]:
    title = entry.get("title", "").strip()
    if not title:
        continue

    # Link — try standard fields
    link = (
        entry.get("link")
        or next((l.href for l in entry.get("links", []) if l.get("rel") == "alternate"), None)
        or entry.get("id", "#")
    )

    # Description — prefer summary over content
    raw_desc = (
        entry.get("summary")
        or (entry.get("content") or [{}])[0].get("value", "")
        or entry.get("description", "")
    )
    desc = strip_html(raw_desc)[:MAX_DESC]

    # Date — try published, then updated
    pub = entry.get("published_parsed") or entry.get("updated_parsed")
    date_str = ""
    if pub:
        try:
            date_str = datetime(*pub[:6], tzinfo=timezone.utc).isoformat()
        except Exception:
            pass

    items.append({
        "title": title,
        "desc":  desc,
        "link":  link or "#",
        "src":   feed["src"],
        "cat":   feed["cat"],
        "date":  date_str,
    })

status = "OK  " if items else "EMPTY"
print(f"  {status}  {feed['src']} ({len(items)} articles)")
return items, bool(items)
```

# ── MAP DATA FETCHERS ─────────────────────────────────────────────────────────

def fetch_feodo() -> list:
“”“Fetch active C2 botnet servers from Feodo Tracker (abuse.ch).”””
url = “https://feodotracker.abuse.ch/downloads/ipblocklist_aggressive.json”
try:
resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()
data = resp.json()
if isinstance(data, list):
print(f”  OK    Feodo Tracker ({len(data)} C2 servers)”)
return data
except Exception as e:
print(f”  FAIL  Feodo Tracker: {e}”)
return []

def fetch_kev() -> dict:
“”“Fetch CISA Known Exploited Vulnerabilities catalog.”””
url = “https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json”
try:
resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()
data = resp.json()
vulns = data.get(“vulnerabilities”, [])
print(f”  OK    CISA KEV ({len(vulns)} vulnerabilities)”)
return data
except Exception as e:
print(f”  FAIL  CISA KEV: {e}”)
return {}

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
print(f”Fetching {len(FEEDS)} feeds…\n”)
all_articles = []
loaded = 0
failed = 0

```
for i, feed in enumerate(FEEDS):
    items, ok = fetch_feed(feed)
    all_articles.extend(items)
    if ok:
        loaded += 1
    else:
        failed += 1
    if i < len(FEEDS) - 1:
        time.sleep(0.3)

# Sort newest first
all_articles.sort(key=lambda a: a["date"], reverse=True)

print("\nFetching map data…\n")
feodo = fetch_feodo()
kev   = fetch_kev()

output = {
    "updated":  datetime.now(timezone.utc).isoformat(),
    "loaded":   loaded,
    "failed":   failed,
    "total":    len(FEEDS),
    "articles": all_articles,
    "feodo":    feodo,
    "kev":      kev,
}

with open("feeds.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, separators=(",", ":"))

print(f"\nDone — {len(all_articles)} articles from {loaded}/{len(FEEDS)} sources → feeds.json")
```

if **name** == “**main**”:
main()
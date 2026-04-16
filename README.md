# 🛰️ CTI Radar — Cybersecurity Threat Intelligence Dashboard

> A live, browser-based threat intelligence dashboard aggregating **68 curated sources** across government advisories, news, research, vendor blogs, and community intelligence — with built-in IOC lookup, CVE monitoring, keyword alerts, TTP tagging, threat actor tracking, bookmarks, a live threat map, and analytics. Feeds are fetched server-side via GitHub Actions every 30 minutes — no CORS issues, no rate limits, no API keys required.

**Live:** [spac3gh0st00.github.io/Cybersecurity-Threat-Intelligence-Dashboard](https://spac3gh0st00.github.io/Cybersecurity-Threat-Intelligence-Dashboard)

-----

## 🚀 Features

### ⬡ Live Feed

- 68 verified RSS/Atom feeds fetched server-side and served as a single local `feeds.json`
- Articles load instantly — no browser-side fetching, no CORS, no timeouts
- Auto-refreshes every **10 minutes** with a live countdown timer
- Color-coded **severity tags** (Critical / High / Medium / Low) per article
- Color-coded **source badges** by category
- Relative timestamps (“2h ago”, “just now”)
- Live status bar showing sources loaded, unavailable, article count, and last updated time

### 🔍 Search & Filter

- Full-text search across title, description, and source name
- Category filters: Gov/CERT · News · Research · Vendor · Community
- Results update instantly as you type

### 🔔 Keyword Alerts

- Add custom alert keywords (e.g. `ransomware`, `CVE-2025`, `cobalt strike`)
- Matching articles get a glowing yellow border and ALERT badge
- Stack multiple keywords, remove individually as chips

### 🎯 TTP Tagging (MITRE ATT&CK)

- Every article is automatically scanned against **25 MITRE ATT&CK techniques**
- Matching articles display red technique tags (e.g. `T1566`, `T1059`, `T1486`)
- Click any TTP tag to instantly filter the feed to only articles matching that technique
- Active TTP filter shown as a banner with a clear button
- Techniques covered include: Phishing, Ransomware, C2, Credential Dumping, Process Injection, Supply Chain, DDoS, Data Destruction, and more

### 🎭 Threat Actor Tracker

- Dedicated tab tracking **25 major APT groups and cybercrime actors**
- Each card shows group name, nation attribution, known aliases, description, and a live count of how many current articles mention them
- Click any card to expand and see the matching articles with direct links
- Filter by nation: China · Russia · North Korea · Iran · Unknown
- Search across actor names and aliases
- Actors tracked include:
  - **Chinese:** APT41, APT10, APT40, Volt Typhoon, Salt Typhoon, APT31
  - **Russian:** APT29 (Cozy Bear), APT28 (Fancy Bear), Sandworm, Turla, Killnet
  - **North Korean:** Lazarus Group, Kimsuky, ScarCruft
  - **Iranian:** APT33, APT34, Charming Kitten, MuddyWater
  - **Cybercrime:** LockBit, ALPHV/BlackCat, Cl0p, Scattered Spider, FIN7, REvil

### ⚡ IOC Lookup

Paste any indicator — type is auto-detected — and get instant links to the right tools:

|Type                   |Tools                                                                    |
|-----------------------|-------------------------------------------------------------------------|
|**IPv4 / IPv6**        |VirusTotal · Shodan · AbuseIPDB · GreyNoise · Censys · IPInfo · MXToolbox|
|**Domain**             |VirusTotal · URLScan.io · Shodan · OTX · URLVoid · Whois · SecurityTrails|
|**URL**                |VirusTotal · URLScan.io · URLVoid · OTX · Google Safe Browsing           |
|**MD5 / SHA1 / SHA256**|VirusTotal · MalwareBazaar · Hybrid-Analysis · Triage · OTX              |
|**CVE**                |NVD · MITRE · Exploit-DB · GitHub Advisory · Vulhub · GreyNoise          |

Keeps a recent lookup history as clickable chips.

### ⚑ CVE Watch

- Live feed of latest CVEs from the **NVD / NIST API**
- Filter by Critical / High / Medium severity
- Shows CVE ID, CVSS score, description, affected product, and publish date
- Direct links to NVD entries

### ⊕ Live Threat Map

Built on **Leaflet.js** with two real data layers — both fetched server-side and bundled into `feeds.json`:

**C2 Botnet Servers** (Feodo Tracker / abuse.ch)

- Live command & control server locations plotted globally
- Markers sized by C2 count per country, color-coded by malware family
- Click any country for total/online count and malware family breakdown
- Sidebar shows stats, top countries, and malware family distribution

**CISA KEV** (Known Exploited Vulnerabilities)

- Full CISA KEV catalog plotted by vendor country
- Fresh additions (last 30 days) highlighted in red
- Click any dot for CVE ID, vendor, product, description, and due date
- Sidebar shows the 8 most recently added KEVs

### ◈ Analytics

- Articles by category (donut chart)
- Top 10 sources by article count (bar chart)
- Threat type distribution based on keyword matching across live article titles

### 🔖 Saved Articles

- Bookmark any article with the ☆ button
- Saved articles collect in a dedicated SAVED tab
- Live count badge on the tab button

### ⬇ Export CSV

- One-click download of the current filtered feed
- Includes: Title · Source · Category · Severity · Date · URL

-----

## 📡 Feed Sources (68 total)

### 🏛 Gov / CERT (7)

CISA · US-CERT · SANS ISC · JPCERT · NCSC UK · ACSC Australia · ENISA (EU)

### 📰 News (14)

BleepingComputer · The Hacker News · Dark Reading · ZDNet Security · InfoSecurity Magazine · TechCrunch Security · The Record · Security Affairs · Wired Security · CyberScoop · Help Net Security · CSO Online · BankInfoSecurity · GovInfoSecurity

### 🔬 Research (23)

Unit 42 · Check Point Research · Cisco Talos · Google TAG · DFIR Report · AhnLab ASEC · SentinelOne Labs · Recorded Future · Dragos · ForensicITGuy · Red Canary · GreyNoise · BushidoToken · Citizen Lab · Bellingcat · Mandiant · Microsoft MSRC · Kaspersky Securelist · ESET WeLiveSecurity · Malwarebytes Labs · Elastic Security · Sekoia · Intezer

### 🛡 Vendor (14)

Sophos · CrowdStrike · Trend Micro · Tenable · Qualys · Huntress · Proofpoint · BHIS · Rapid7 · Cybereason · Stairwell · WithSecure Labs · Binary Defense · Varonis

### 🌐 Community (10)

Krebs on Security · Schneier on Security · Packet Storm · SANS Blog · Exploit-DB · Graham Cluley · Daniel Miessler · Troy Hunt · Risky Business · The Cyber Wire

-----

## ⚙️ How It Works

```
GitHub Actions (every 30 min)
  └── fetch_feeds.py
        ├── Fetches 68 RSS/Atom feeds
        ├── Fetches Feodo Tracker C2 data
        ├── Fetches CISA KEV catalog
        └── Saves everything to feeds.json

Browser (visitor)
  └── Loads index.html
        └── Fetches feeds.json (one local file, instant)
              ├── Renders articles, map, analytics
              ├── TTP tags auto-detected from article content
              ├── Threat actor mentions scanned across all articles
              └── No CORS issues, no rate limits
```

-----

## 🛠 Setup

### 1. Fork or clone the repo

```bash
git clone https://github.com/spac3gh0st00/Cybersecurity-Threat-Intelligence-Dashboard.git
```

### 2. Enable GitHub Pages

Go to **Settings → Pages → Deploy from branch → main → / (root)** and save.

### 3. Commit the workflow and fetch script

Make sure these two files are in your repo:

- `.github/workflows/fetch-feeds.yml` — schedules the feed fetch every 30 minutes
- `fetch_feeds.py` — the Python script that fetches all feeds and builds `feeds.json`

### 4. Trigger the first run

Go to **Actions → Fetch RSS Feeds → Run workflow**. It takes about 2 minutes and commits `feeds.json` to your repo. After that it runs automatically every 30 minutes.

### 5. Visit your site

`https://YOUR-USERNAME.github.io/Cybersecurity-Threat-Intelligence-Dashboard`

-----

## 📝 Adding or Removing Feeds

Edit the `FEEDS` list in **both** `fetch_feeds.py` and `index.html` — they must stay in sync. Each entry takes this shape:

**Python (`fetch_feeds.py`):**

```python
{"url": "https://example.com/feed.xml", "src": "Display Name", "cat": "news"},
```

**JavaScript (`index.html`):**

```javascript
{url:"https://example.com/feed.xml", src:"Display Name", cat:"news"},
```

Valid categories: `gov` · `news` · `research` · `vendor` · `community`

The source count in the UI updates automatically from the feed list length.

-----

## 🔧 Tech Stack

- **Frontend:** Vanilla HTML/CSS/JS — no frameworks, no build tools
- **Map:** [Leaflet.js](https://leafletjs.com/) with CartoDB dark tiles
- **Charts:** [Chart.js](https://www.chartjs.org/)
- **Feed parsing:** Python `feedparser` + `requests` (GitHub Actions)
- **Threat Intel:** MITRE ATT&CK TTP detection, 25 APT group tracking
- **Hosting:** GitHub Pages (free)
- **Data:** GitHub Actions cron job writing `feeds.json` to the repo

-----

*Credit: Gerard King — Cybersecurity Overlord and Master of Excess*
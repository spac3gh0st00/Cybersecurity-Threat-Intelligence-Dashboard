# 🛰️ CTI Radar — Cybersecurity Threat Intelligence Dashboard

> A live, browser-based threat intelligence dashboard aggregating **76 curated sources** across government advisories, news, research, vendor blogs, and community intelligence — with built-in IOC lookup, CVE monitoring, keyword alerts, bookmarks, and analytics.

**Live demo:** [spac3gh0st00.github.io/Cybersecurity-Threat-Intelligence-Dashboard](https://spac3gh0st00.github.io/Cybersecurity-Threat-Intelligence-Dashboard)

-----

## 🚀 Features

### ⬡ Live Feed

- Aggregates **76 verified, active RSS/Atom feeds** across 5 categories
- Articles load progressively in batches — no page freezing
- Auto-refreshes every **10 minutes** with a live countdown timer
- Per-article **severity tags** (Critical / High / Medium / Low)
- Color-coded **source badges** by category
- Relative timestamps (“2h ago”, “just now”)

### 🔍 Search & Filter

- **Full-text search** across title, description, and source name
- **Category filters:** Gov/CERT · News · Research · Vendor · Community
- Results update instantly as you type

### 🔔 Keyword Alerts

- Add custom keywords (e.g. `ransomware`, `CVE-2025`, `cobalt strike`)
- Matching articles get a **glowing yellow border** and ALERT badge
- Stack multiple keywords; remove as chips at any time

### ⚡ IOC Lookup

Paste any indicator and get instant links to the right tools — type is **auto-detected**:

|Type                   |Tools                                                                    |
|-----------------------|-------------------------------------------------------------------------|
|**IPv4 / IPv6**        |VirusTotal · Shodan · AbuseIPDB · GreyNoise · Censys · IPInfo · MXToolbox|
|**Domain**             |VirusTotal · URLScan.io · Shodan · OTX · URLVoid · Whois · SecurityTrails|
|**URL**                |VirusTotal · URLScan.io · URLVoid · OTX · Google Safe Browsing           |
|**MD5 / SHA1 / SHA256**|VirusTotal · MalwareBazaar · Hybrid-Analysis · Triage · OTX              |
|**CVE**                |NVD · MITRE · Exploit-DB · GitHub Advisory · Vulhub · GreyNoise          |

Keeps a **recent lookup history** as clickable chips.

### ⚑ CVE Watch

- Live feed of latest CVEs pulled from the **NVD / NIST API**
- Filter by **Critical / High / Medium** severity
- Shows CVE ID, CVSS score, description, affected product, and publish date
- Direct links to NVD entries

### ◈ Analytics

- **Articles by category** — donut chart
- **Top 10 sources** — horizontal bar chart
- **Threat type distribution** — keyword-matched counts from live article titles (Phishing, Malware, Ransomware, APT, CVE/Vuln, DDoS, Data Breach, Supply Chain, Credential Theft, ICS/OT)

### 🔖 Saved Articles

- Bookmark any article with the ☆ button
- Saved articles collect in a dedicated **SAVED tab**
- Live count badge on the tab button

### ⬇ Export CSV

- One-click download of the **current filtered feed** as a `.csv` file
- Includes: Title · Source · Category · Severity · Date · URL

### ⊕ Live Threat Map

- Embedded [Check Point live cyber attack map](https://threatmap.checkpoint.com/)

-----

## 📡 Feed Sources (76 total)

### 🏛 Gov / CERT (8)

CISA · US-CERT · SANS ISC · JPCERT · NVD/NIST · NCSC UK · ACSC Australia · ENISA (EU)

### 📰 News (16)

BleepingComputer · The Hacker News · Dark Reading · SecurityWeek · ZDNet Security · InfoSecurity Magazine · TechCrunch Security · The Record · GBHackers · Security Affairs · Cyware · Wired Security · CyberScoop · SC Magazine · Help Net Security · CSO Online

### 🔬 Research (24)

Unit 42 · Check Point Research · Cisco Talos · Google TAG · DFIR Report · SpecterOps · AhnLab ASEC · SentinelOne Labs · Recorded Future · Dragos · ForensicITGuy · Red Canary · GreyNoise · BushidoToken · Citizen Lab · Bellingcat · Mandiant · Microsoft MSRC · Kaspersky Securelist · ESET WeLiveSecurity · Malwarebytes Labs · Elastic Security · Sekoia · Intezer

### 🛡 Vendor (17)

Sophos · CrowdStrike · Trend Micro · Tenable · Qualys · Huntress · Expel · AT&T Cybersecurity · Proofpoint · Secureworks · Tripwire · BHIS · Rapid7 · Cybereason · Stairwell · WithSecure Labs · Binary Defense

### 🌐 Community (11)

Krebs on Security · Schneier on Security · Packet Storm · HackerOne · SANS Blog · Exploit-DB · Daily Swig · Graham Cluley · Daniel Miessler · Troy Hunt · Risky Business

-----

## 🛠 Technical Notes

- **Pure HTML/CSS/JS** — no build tools, no dependencies to install
- RSS feeds are proxied through [rss2json.com](https://rss2json.com) (free tier) to handle CORS
- All feeds are **HTTPS only** — `http://` feeds are blocked as mixed content on GitHub Pages
- Feed list is **auto-deduplicated** at runtime
- Source count in the UI is **dynamically read** from the feed list — no hardcoded numbers
- The `UNAVAIL` counter in the status bar is normal — some feeds may be rate-limited, offline, or behind paywalls at any given time
- CVE Watch uses the public [NVD REST API v2](https://nvd.nist.gov/developers/vulnerabilities) — free, no key required (5 req/30s limit without a key)

-----

## 🧠 Who Uses This

- **SOC Analysts** — morning brief, threat triage, IOC enrichment without leaving the browser
- **Threat Hunters** — track actor activity, keyword-alert on campaign names, pivot on IOCs
- **Vulnerability Management** — CVE Watch tab gives a fast view of what just dropped and how severe
- **Security Researchers** — centralized reading list with bookmark + export
- **Students & Enthusiasts** — best single-pane-of-glass view of the security landscape, free and open source

-----

## 🔧 Running Locally

No server needed. Just open `index.html` in any modern browser:

```bash
git clone https://github.com/spac3gh0st00/Cybersecurity-Threat-Intelligence-Dashboard.git
cd Cybersecurity-Threat-Intelligence-Dashboard
open index.html
```

Or deploy to GitHub Pages by enabling it in **Settings → Pages → Deploy from branch → main**.

-----

## 📝 Adding or Removing Feeds

Edit the `FEEDS` array near the top of `index.html`. Each entry takes this shape:

```js
{ url: "https://example.com/feed.xml", src: "Display Name", cat: "news" }
```

Valid categories: `gov` · `news` · `research` · `vendor` · `community`

The source count in the UI updates automatically.

-----

*Credit: Gerard King — Cybersecurity Overlord and Master of Excess*
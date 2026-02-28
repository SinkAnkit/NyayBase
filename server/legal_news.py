"""
NyayBase — Legal News Feed (RSS-based)
Fetches latest legal news from Indian legal news RSS feeds.
Cache resets daily at IST midnight (12:00 AM).
Fetches og:image from article pages for articles missing RSS images.
"""

import feedparser
import time
import html
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

# RSS feed sources — authoritative Indian legal news
RSS_FEEDS = [
    {"url": "https://www.livelaw.in/feed", "source": "LiveLaw", "icon": "⚖️"},
    {"url": "https://www.barandbench.com/feed", "source": "Bar & Bench", "icon": "📰"},
    {"url": "https://news.google.com/rss/search?q=supreme+court+india+OR+high+court+india+OR+indian+law+amendment&hl=en-IN&gl=IN&ceid=IN:en", "source": "Google News", "icon": "🔍"},
    {"url": "https://news.google.com/rss/search?q=indian+judiciary+OR+legal+india+OR+court+judgment+india&hl=en-IN&gl=IN&ceid=IN:en", "source": "Google News", "icon": "🔍"},
    {"url": "https://news.google.com/rss/search?q=BNS+OR+BNSS+OR+indian+penal+code+OR+criminal+law+india&hl=en-IN&gl=IN&ceid=IN:en", "source": "Google News", "icon": "🔍"},
    {"url": "https://news.google.com/rss/search?q=property+dispute+india+OR+consumer+court+india+OR+family+law+india&hl=en-IN&gl=IN&ceid=IN:en", "source": "Google News", "icon": "🔍"},
    {"url": "https://news.google.com/rss/search?q=cyber+crime+india+OR+tax+tribunal+india+OR+NCLAT+india&hl=en-IN&gl=IN&ceid=IN:en", "source": "Google News", "icon": "🔍"},
    {"url": "https://news.google.com/rss/search?q=bail+india+OR+FIR+india+OR+arrest+india+law&hl=en-IN&gl=IN&ceid=IN:en", "source": "Google News", "icon": "🔍"},
]

# Cache: articles + the IST date they were fetched for
_cache = {"articles": [], "date_key": ""}


def _get_ist_now():
    return datetime.now(IST)


def _get_date_key():
    return _get_ist_now().strftime("%Y-%m-%d")


def _next_midnight_ist_epoch():
    now = _get_ist_now()
    tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return int(tomorrow.timestamp())


def _clean_html(raw):
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", "", raw)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:300]


def _extract_image(entry):
    """Try hard to extract an image URL from the RSS entry."""
    if hasattr(entry, "media_content") and entry.media_content:
        for media in entry.media_content:
            if "url" in media:
                return media["url"]
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        for thumb in entry.media_thumbnail:
            if "url" in thumb:
                return thumb["url"]
    if hasattr(entry, "enclosures") and entry.enclosures:
        for enc in entry.enclosures:
            url = enc.get("href") or enc.get("url", "")
            etype = enc.get("type", "")
            if etype.startswith("image") or re.search(r"\.(jpg|jpeg|png|webp|gif)", url, re.I):
                return url
    html_sources = []
    for field in ["summary", "description", "content"]:
        val = entry.get(field, "")
        if val:
            html_sources.append(val)
    if hasattr(entry, "content") and entry.content:
        for c in entry.content:
            html_sources.append(c.get("value", ""))
    if hasattr(entry, "summary_detail"):
        html_sources.append(getattr(entry.summary_detail, "value", ""))
    for src in html_sources:
        if not src:
            continue
        img_match = re.search(r'<img[^>]+src=["\']([^"\'>]+)["\']', src)
        if img_match:
            url = img_match.group(1)
            if url.startswith("http"):
                return url
        srcset = re.search(r'<img[^>]+srcset=["\']([^"\'>]+)["\']', src)
        if srcset:
            first_url = srcset.group(1).split(",")[0].strip().split(" ")[0]
            if first_url.startswith("http"):
                return first_url
    for link in entry.get("links", []):
        href = link.get("href", "")
        if re.search(r"\.(jpg|jpeg|png|webp|gif)(\?|$)", href, re.I):
            return href
    return None


def _parse_date(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6]).strftime("%d %b %Y, %I:%M %p")
        except Exception:
            pass
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6]).strftime("%d %b %Y, %I:%M %p")
        except Exception:
            pass
    return "Recent"


def _categorize(title, summary):
    text = (title + " " + summary).lower()
    if any(k in text for k in ["supreme court", "sc ", "apex court"]):
        return "Supreme Court"
    if any(k in text for k in ["high court", "hc ", "calcutta", "bombay", "delhi hc", "madras"]):
        return "High Court"
    if any(k in text for k in ["amendment", "bill", "act ", "bns", "bnss", "bsa", "new law", "parliament", "ordinance"]):
        return "Legislation"
    if any(k in text for k in ["bail", "arrest", "fir", "criminal", "murder", "rape", "police"]):
        return "Criminal"
    if any(k in text for k in ["property", "land", "real estate", "eviction", "encroach"]):
        return "Property"
    if any(k in text for k in ["divorce", "custody", "maintenance", "dowry", "domestic violence", "marriage"]):
        return "Family Law"
    if any(k in text for k in ["consumer", "complaint", "deficiency"]):
        return "Consumer"
    if any(k in text for k in ["cyber", "it act", "data", "privacy", "online"]):
        return "Cyber Law"
    if any(k in text for k in ["tax", "gst", "income tax", "tribunal"]):
        return "Tax"
    return "Legal News"


def _fetch_og_image(url):
    """Fetch og:image from an article URL — follows redirects, reads first 15KB."""
    if not url or not url.startswith("http"):
        return None
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
        })
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        with opener.open(req, timeout=5) as resp:
            chunk = resp.read(15360).decode("utf-8", errors="ignore")
        # og:image
        for pat in [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\'>]+)["\']',
            r'<meta[^>]+content=["\']([^"\'>]+)["\'][^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\'>]+)["\']',
            r'<meta[^>]+content=["\']([^"\'>]+)["\'][^>]+name=["\']twitter:image["\']',
            r'<meta[^>]+property=["\']og:image:url["\'][^>]+content=["\']([^"\'>]+)["\']',
        ]:
            m = re.search(pat, chunk, re.I)
            if m and m.group(1).startswith("http"):
                return m.group(1)
        # Fallback: any large img in head/top of page
        imgs = re.findall(r'<img[^>]+src=["\']([^"\'>]+)["\']', chunk)
        for img_url in imgs[:3]:
            if img_url.startswith("http") and not any(x in img_url.lower() for x in ["logo", "icon", "favicon", "avatar", "1x1", "pixel"]):
                return img_url
    except Exception:
        pass
    return None


def _fill_missing_images(articles):
    """Fill in images for articles missing them using og:image from their URLs."""
    missing = [(i, a) for i, a in enumerate(articles) if not a.get("image")]
    if not missing:
        return

    print(f"[NyayBase] Fetching og:image for {len(missing)} articles without images...")
    filled = 0

    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(_fetch_og_image, a["link"]): i for i, a in missing}
        for future in as_completed(futures):
            idx = futures[future]
            try:
                img = future.result()
                if img:
                    articles[idx]["image"] = img
                    filled += 1
            except Exception:
                pass

    print(f"[NyayBase] og:image fill: {filled}/{len(missing)} articles now have images")


def fetch_legal_news():
    """
    Fetch legal news from RSS feeds.
    Cache lasts until IST midnight — same content for the entire day.
    Returns dict with articles, next refresh timestamp, etc.
    """
    today_key = _get_date_key()

    # Return cache if still the same IST day
    if _cache["articles"] and _cache["date_key"] == today_key:
        return {
            "articles": _cache["articles"],
            "cached": True,
            "next_refresh": _next_midnight_ist_epoch(),
            "last_updated": _cache["date_key"],
        }

    # New day — fetch fresh articles
    articles = []
    seen_titles = set()

    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:30]:
                title = entry.get("title", "").strip()
                if not title:
                    continue
                title_key = re.sub(r"[^a-z0-9]", "", title.lower())[:50]
                if title_key in seen_titles:
                    continue
                seen_titles.add(title_key)

                summary = _clean_html(entry.get("summary", "") or entry.get("description", ""))
                link = entry.get("link", "")
                image = _extract_image(entry)
                date_str = _parse_date(entry)
                category = _categorize(title, summary)

                articles.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "source": feed_info["source"],
                    "source_icon": feed_info["icon"],
                    "image": image,
                    "date": date_str,
                    "category": category,
                })
        except Exception as e:
            print(f"[NyayBase] RSS fetch error ({feed_info['source']}): {e}")

    # Cap at 102 articles
    articles = articles[:102]

    # Fetch og:image for articles missing images (concurrent, fast)
    _fill_missing_images(articles)

    # Update cache
    _cache["articles"] = articles
    _cache["date_key"] = today_key

    print(f"[NyayBase] Legal news: fetched {len(articles)} articles from {len(RSS_FEEDS)} sources (date: {today_key})")

    return {
        "articles": articles,
        "cached": False,
        "next_refresh": _next_midnight_ist_epoch(),
        "last_updated": today_key,
    }

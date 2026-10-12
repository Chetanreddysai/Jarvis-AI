"""
SAMPAN Knowledge & Internet Information Engine
Searches the live internet (DuckDuckGo Live Web Search, Wikipedia, DuckDuckGo Instant Answers,
and live weather/math) to answer any question asked by the user without requiring API keys.
"""

import re
import math
import json
import urllib.request
import urllib.parse
from html import unescape

def clean_for_speech(text: str) -> str:
    """Cleans raw text for clear, natural speech synthesis and console display."""
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\([^)]*\)', '', text)  # remove parentheticals like (born 1971)
    text = re.sub(r'\[[^\]]*\]', '', text)  # remove citations [1], [2]
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Replace common symbols with spoken words
    text = text.replace('°C', ' degrees Celsius').replace('°F', ' degrees Fahrenheit')
    text = text.replace('±', 'plus or minus ')
    text = text.replace('²', ' squared').replace('³', ' cubed')
    # Filter to standard printable characters
    text = text.encode('ascii', 'ignore').decode()
    return text

def format_spoken_answer(text: str, query: str = "") -> str:
    """Polishes raw internet search snippets into articulate, human-like spoken answers."""
    if not text:
        return ""
    clean = text.strip()
    # Strip leading timestamps like "Jun 29, 2024 - ", "12 hours ago - "
    clean = re.sub(r'^(?:[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}|\d+\s+(?:days?|hours?|mins?)\s+ago)\s*[-:]?\s*', '', clean)
    # Strip leading website navigation headers like "Former Prime Ministers PM's Profile ", "Home > News > ", "Profile - "
    clean = re.sub(r'^(?:(?:Former\s+)?Prime\s+Ministers?\s+(?:PM\'?s?\s+)?Profile\s*|Home\s*>\s*|Overview\s*[-|:]?\s*)+', '', clean, flags=re.I)
    # Strip trailing website footer artifacts
    clean = re.sub(r'(?:Read more|Click here|Full article|Image credit|Photo by|Sign up|\.\.\.).*$', '', clean, flags=re.I)
    clean = clean_for_speech(clean)
    if clean:
        clean = clean[0].upper() + clean[1:]
        if not clean.endswith(('.', '!', '?')):
            clean += '.'
    return clean

def solve_math(query: str) -> str:
    """Detects and calculates mathematical expressions in natural language."""
    clean = query.lower().strip()

    # Percentage: "what is 15 percent of 200", "20% of 850"
    pct_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s+of\s+(\d+(?:\.\d+)?)', clean)
    if pct_match:
        pct = float(pct_match.group(1))
        total = float(pct_match.group(2))
        res = (pct / 100.0) * total
        return f"{pct:g} percent of {total:g} is {res:g}."

    # Square root: "square root of 144"
    sqrt_match = re.search(r'(?:square root of|sqrt of|sqrt)\s+(\d+(?:\.\d+)?)', clean)
    if sqrt_match:
        val = float(sqrt_match.group(1))
        res = math.isqrt(int(val)) if val.is_integer() else round(math.sqrt(val), 3)
        return f"The square root of {val:g} is {res:g}."

    # General arithmetic
    expr = clean
    expr = re.sub(r'^(?:what is|calculate|compute|solve|how much is)\s+', '', expr).strip('? ')
    expr = expr.replace(' multiplied by ', ' * ').replace(' times ', ' * ').replace(' x ', ' * ')
    expr = expr.replace(' divided by ', ' / ').replace(' over ', ' / ')
    expr = expr.replace(' plus ', ' + ').replace(' added to ', ' + ')
    expr = expr.replace(' minus ', ' - ').replace(' subtracted by ', ' - ')

    if re.search(r'^\s*[-+]?\d+(?:\.\d+)?(?:\s*[-+*/^%]\s*[-+]?\d+(?:\.\d+)?)+\s*$', expr):
        try:
            expr_eval = expr.replace('^', '**')
            res = eval(expr_eval, {"__builtins__": None}, {})
            if isinstance(res, (int, float)):
                return f"The answer to {expr} is {res:g}."
        except Exception:
            pass
    return ""

def get_weather_report(query: str) -> str:
    """Fetches real-time weather information for cities using wttr.in."""
    clean = query.lower().strip()
    if not any(w in clean for w in ["weather", "temperature", "forecast", "how hot", "how cold"]):
        return ""
    city_match = re.search(r'(?:weather|temperature|forecast)(?:\s+in|\s+for|\s+at)?\s+([a-zA-Z\s]+)', clean, re.I)
    city = city_match.group(1).strip('? ') if city_match else "Hyderabad"
    if not city or len(city) < 2 or city in ["today", "now", "outside", "like"]:
        city = "Hyderabad"

    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=%C,+temperature+%t"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            raw = res.read().decode('utf-8', errors='ignore').strip()
            raw = clean_for_speech(raw)
            if raw and "Unknown location" not in raw and "<html" not in raw.lower():
                return f"The weather in {city.title()} is currently {raw}."
    except Exception:
        pass
    return ""

def search_dictionary_definition(query: str) -> str:
    """Fetches instant word definitions from free English Dictionary API."""
    match = re.search(r'(?:meaning of|definition of|define|what does\s+([a-zA-Z]+)\s+mean)\s*([a-zA-Z]+)?', query, re.I)
    if not match:
        return ""
    word = (match.group(2) or match.group(1) or "").strip().lower()
    if not word or len(word) < 2:
        return ""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=2.2) as res:
            data = json.loads(res.read().decode('utf-8'))
            if isinstance(data, list) and data:
                meanings = data[0].get("meanings", [])
                if meanings:
                    part_of_speech = meanings[0].get("partOfSpeech", "")
                    definitions = meanings[0].get("definitions", [])
                    if definitions:
                        defn = definitions[0].get("definition", "")
                        if defn:
                            pos_prefix = f"As a {part_of_speech}, " if part_of_speech else ""
                            return format_spoken_answer(f"{pos_prefix}{word} means {defn}", query)
    except Exception:
        pass
    return ""

def search_wikidata_entity(query: str) -> str:
    """Queries Wikidata for ultra-fast, structured factual descriptions of notable entities."""
    clean_q = re.sub(r'^(?:who is|who was|what is|what was|tell me about|explain|describe)\s+', '', query, flags=re.I).strip('? ')
    if not clean_q or len(clean_q) < 2:
        return ""
    try:
        url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(clean_q)}&language=en&format=json&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "SampanAI/3.0 (https://github.com/Chetanreddysai/Jarvis-AI)"})
        with urllib.request.urlopen(req, timeout=2.0) as res:
            data = json.loads(res.read().decode('utf-8'))
            results = data.get("search", [])
            if results and results[0].get("description"):
                label = results[0].get("label", clean_q.title())
                desc = results[0].get("description", "")
                # Skip meta-articles and generic disambiguations
                if any(bad in desc.lower() for bad in ["wikimedia list", "disambiguation", "category", "wikipedia:", "none"]):
                    return ""
                if len(desc) > 12:
                    return format_spoken_answer(f"{label} is {desc}", query)
    except Exception:
        pass
    return ""

def search_wikipedia_live(query: str) -> str:
    """Searches Wikipedia API for authoritative, high-speed summaries."""
    clean_q = re.sub(r'^(?:who is|who was|what is|what was|what are|where is|tell me about|explain|describe|define)\s+', '', query, flags=re.I).strip('? ')
    if not clean_q:
        clean_q = query.strip('? ')

    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(clean_q)}&utf8=&format=json&srlimit=3"
        req = urllib.request.Request(search_url, headers={"User-Agent": "SampanAI/3.0 (https://github.com/Chetanreddysai/Jarvis-AI; chetan@example.com)"})
        with urllib.request.urlopen(req, timeout=2.5) as res:
            data = json.loads(res.read().decode('utf-8'))
            hits = data.get("query", {}).get("search", [])
            if hits:
                title = hits[0]["title"]
                sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
                req2 = urllib.request.Request(sum_url, headers={"User-Agent": "SampanAI/3.0 (https://github.com/Chetanreddysai/Jarvis-AI; chetan@example.com)"})
                with urllib.request.urlopen(req2, timeout=2.5) as res2:
                    d2 = json.loads(res2.read().decode('utf-8'))
                    extract = d2.get("extract", "")
                    if extract:
                        clean = clean_for_speech(extract)
                        sentences = [s.strip() for s in clean.split('. ') if s.strip()]
                        if sentences:
                            ans = '. '.join(sentences[:2])
                            if not ans.endswith('.'):
                                ans += '.'
                            return format_spoken_answer(ans, query)
    except Exception:
        pass
    return ""

def search_live_web_fast(query: str) -> str:
    """
    Fast live web search fallback using Bing with ad-filtering
    and strict 2.5s timeout.
    """
    clean_q = re.sub(r'^(?:sampan|hey sampan|can you tell me|do you know|tell me about|tell me)\s+', '', query, flags=re.I).strip('? ')
    if not clean_q or len(clean_q) < 3:
        return ""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        url = f"https://www.bing.com/search?q={urllib.parse.quote(clean_q)}&setlang=en"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=2.5) as res:
            html = res.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<li class=[\x22\x27]b_algo[\x22\x27][^>]*>.*?<p[^>]*>(.*?)</p>', html, re.DOTALL)
            for m in matches:
                clean = re.sub(r'<[^>]+>', '', m).strip()
                # Skip sponsored ads and promotional blurbs
                if any(bad in clean.lower() for bad in ["stream popular", "amazon.com", "prime video", "subscription", "shop now", "free shipping"]):
                    continue
                clean = clean_for_speech(clean)
                if len(clean) > 25:
                    sentences = re.split(r'(?<=[.?!])\s+', clean)
                    if sentences and sentences[0].strip().endswith('?') and len(sentences) > 1:
                        sentences = sentences[1:]
                    if sentences:
                        res_text = ' '.join(sentences[:2]).strip()
                        if len(res_text) > 20:
                            return format_spoken_answer(res_text, query)
    except Exception:
        pass

    return ""

def query_general_knowledge(query: str) -> str:
    """
    Ultra-fast multi-tier general knowledge engine.
    Returns highly accurate, verified answers in under 1 second without stalling.
    """
    clean = query.lower().strip()

    # 1. Instant Dictionary lookup for meanings and definitions
    if any(w in clean for w in ["meaning of", "definition of", "define", "what does"]):
        dict_ans = search_dictionary_definition(query)
        if dict_ans and len(dict_ans) > 15:
            return dict_ans

    # 2. Instant Wikidata for concise entity descriptions (who is X, what is X)
    if clean.startswith("who is") or clean.startswith("who was"):
        wiki_data_ans = search_wikidata_entity(query)
        if wiki_data_ans and len(wiki_data_ans) > 20:
            return wiki_data_ans

    # 3. Wikipedia Live Search & Summary (comprehensive, verified encyclopedia facts)
    wiki_res = search_wikipedia_live(query)
    if wiki_res and len(wiki_res) > 25:
        return wiki_res

    # 4. Wikidata fallback for general concepts
    wiki_data_ans = search_wikidata_entity(query)
    if wiki_data_ans and len(wiki_data_ans) > 20:
        return wiki_data_ans

    # 5. Live web search fallback for recent events, sports, scores
    web_res = search_live_web_fast(query)
    if web_res and len(web_res) > 25:
        return web_res

    return ""

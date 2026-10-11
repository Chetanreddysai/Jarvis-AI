"""
SAMPAN Knowledge & Information Engine
Provides real-time mathematical calculation, live weather, universal Wikipedia search,
and DuckDuckGo instant answers without requiring any API keys.
"""

import re
import math
import json
import urllib.request
import urllib.parse

def clean_for_speech(text: str) -> str:
    """Cleans text for clean, natural speech synthesis and console display."""
    if not text:
        return ""
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\([^)]*\)', '', text)  # remove parentheticals like (born 1971)
    text = re.sub(r'\[[^\]]*\]', '', text)  # remove citations [1]
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Replace common mathematical and degree symbols with spoken words
    text = text.replace('°C', ' degrees Celsius').replace('°F', ' degrees Fahrenheit')
    text = text.replace('±', 'plus or minus ')
    text = text.replace('²', ' squared').replace('³', ' cubed')
    # Clean non-ascii artifacts
    text = text.encode('ascii', 'ignore').decode()
    return text

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
    city_match = re.search(r'(?:weather|temperature|forecast)(?:\s+in|\s+for|\s+at)?\s+([a-zA-Z\s]+)', clean, re.I)
    city = city_match.group(1).strip('? ') if city_match else "Hyderabad"
    if not city or len(city) < 2 or city in ["today", "now", "outside", "like"]:
        city = "Hyderabad"

    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=%C,+temperature+%t"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=4) as res:
            raw = res.read().decode('utf-8', errors='ignore').strip()
            raw = clean_for_speech(raw)
            if raw and "Unknown location" not in raw and "<html" not in raw.lower():
                return f"The weather in {city.title()} is currently {raw}."
    except Exception:
        pass
    return ""

def search_wikipedia(query: str) -> str:
    """Searches Wikipedia using the query search API and summary endpoint."""
    try:
        clean_q = re.sub(r'^(?:who is|who was|what is|what are|tell me about|explain|describe|define)\s+', '', query, flags=re.I).strip('? ')
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(clean_q)}&utf8=&format=json"
        req = urllib.request.Request(search_url, headers={"User-Agent": "SampanAI/2.0 (desktop-assistant)"})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))
            hits = data.get("query", {}).get("search", [])
            if hits:
                title = hits[0]["title"]
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
                req2 = urllib.request.Request(summary_url, headers={"User-Agent": "SampanAI/2.0 (desktop-assistant)"})
                with urllib.request.urlopen(req2, timeout=5) as res2:
                    d2 = json.loads(res2.read().decode('utf-8'))
                    extract = d2.get("extract", "")
                    if extract:
                        clean = clean_for_speech(extract)
                        sentences = [s.strip() for s in clean.split('. ') if s.strip()]
                        if sentences:
                            return '. '.join(sentences[:2]) + '.'
    except Exception:
        pass
    return ""

def search_duckduckgo(query: str) -> str:
    """Fetches instant answer or abstract from DuckDuckGo."""
    try:
        clean_q = urllib.parse.quote(query.strip('? '))
        url = f"https://api.duckduckgo.com/?q={clean_q}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as res:
            data = json.loads(res.read().decode('utf-8', errors='ignore'))
            abstract = data.get("AbstractText") or data.get("Abstract") or data.get("Answer")
            if abstract:
                clean = clean_for_speech(abstract)
                sentences = [s.strip() for s in clean.split('. ') if s.strip()]
                if sentences:
                    return '. '.join(sentences[:2]) + '.'
    except Exception:
        pass
    return ""

def query_general_knowledge(query: str) -> str:
    """Tries Wikipedia first, then DuckDuckGo as fallback."""
    wiki_res = search_wikipedia(query)
    if wiki_res and len(wiki_res) > 20:
        return wiki_res
    ddg_res = search_duckduckgo(query)
    if ddg_res and len(ddg_res) > 20:
        return ddg_res
    return ""

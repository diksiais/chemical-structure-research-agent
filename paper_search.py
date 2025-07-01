import requests
import urllib.parse
import xml.etree.ElementTree as ET
import logging
import re
from html import unescape
from requests.exceptions import SSLError, RequestException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

VERIFY_SSL = True
MAX_RETRIES = 3

def safe_get(url, timeout=10, verify=VERIFY_SSL):
    try:
        return requests.get(url, timeout=timeout, verify=verify)
    except SSLError:
        if verify:
            logger.warning(f"SSL failed for {url}. Retrying with verify=False...")
            return safe_get(url, timeout=timeout, verify=False)
        raise

def clean_abstract(raw_abstract):
    if not raw_abstract:
        return "No abstract available."
    clean = re.sub('<[^<]+?>', '', raw_abstract)
    return unescape(clean).strip()

def parse_semantic_response(response):
    data = response.json().get("data", [])
    papers = []
    for paper in data:
        authors = ", ".join([a.get("name", "N/A") for a in paper.get("authors", [])])
        pdf_url = paper.get("openAccessPdf", {}).get("url") if paper.get("openAccessPdf") else None
        papers.append({
            "title": paper.get("title", ""),
            "authors": authors,
            "year": paper.get("year", "N/A"),
            "url": paper.get("url", ""),
            "abstract": paper.get("abstract", "No abstract available."),
            "pdf_url": pdf_url
        })
    return papers

def search_semantic_scholar(query, limit=5):
    if not query.strip():
        return []
    encoded_query = urllib.parse.quote(query)
    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/search?"
        f"query={encoded_query}&limit={limit}&fields=title,authors,year,url,abstract,externalIds,openAccessPdf"
    )
    logger.debug(f"Semantic Scholar: {url}")
    for _ in range(MAX_RETRIES):
        try:
            response = safe_get(url)
            if response.status_code == 200:
                return parse_semantic_response(response)[:limit]
        except Exception as e:
            logger.error(f"Semantic Scholar error: {e}")
    return []

def search_crossref(query, limit=5):
    if not query.strip():
        return []
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.crossref.org/works?query={encoded_query}&rows={limit}"
    logger.debug(f"CrossRef: {url}")
    try:
        response = safe_get(url)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"CrossRef error: {e}")
        return []

    items = response.json().get("message", {}).get("items", [])
    results = []
    for item in items:
        authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in item.get("author", [])]
        authors_str = ", ".join(authors) if authors else "N/A"
        pdf_url = next((link.get("URL") for link in item.get("link", []) if link.get("content-type") == "application/pdf"), None)
        results.append({
            "title": item.get("title", [""])[0],
            "authors": authors_str,
            "year": item.get("issued", {}).get("date-parts", [[None]])[0][0],
            "url": item.get("URL", ""),
            "abstract": clean_abstract(item.get("abstract")),
            "pdf_url": pdf_url
        })
    return results[:limit]

def search_arxiv(query, limit=5):
    if not query.strip():
        return []
    base_url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results={limit}"
    logger.debug(f"arXiv: {base_url}")
    try:
        response = safe_get(base_url)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"arXiv error: {e}")
        return []

    entries = []
    try:
        root = ET.fromstring(response.text)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            abstract = entry.find("atom:summary", ns).text.strip()
            url = entry.find("atom:id", ns).text
            year = entry.find("atom:published", ns).text[:4]
            arxiv_id = url.split('/abs/')[-1]
            pdf_url = f"http://arxiv.org/pdf/{arxiv_id}.pdf"
            authors = [author.text for author in entry.findall("atom:author/atom:name", ns)]
            authors_str = ", ".join(authors) or "N/A"
            entries.append({
                "title": title,
                "authors": authors_str,
                "year": year,
                "url": url,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    except Exception as e:
        logger.error(f"Failed to parse arXiv response: {e}")
        return []

    return entries[:limit]

def search_papers(query, limit=10):
    all_papers = []
    for source, func in [
        ("Semantic Scholar", search_semantic_scholar),
        ("CrossRef", search_crossref),
        ("arXiv", search_arxiv)
    ]:
        papers = func(query, limit=limit - len(all_papers))
        if papers:
            all_papers.extend(papers)
            if len(all_papers) >= limit:
                return all_papers[:limit], "Multiple Sources"
    return all_papers, "Multiple Sources" if all_papers else "None"
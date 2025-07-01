from chemical_lookup import fetch_pubchem_image
from paper_search import search_papers

def main():
    chemical_name = input("Enter chemical name or CAS number: ").strip()
    if not chemical_name:
        print("No chemical name entered. Exiting.")
        return

    print("\n=== 🔍 Fetching chemical image and info ===")
    try:
        cid, image_url, source, label = fetch_pubchem_image(chemical_name)
        display_name = label or chemical_name
        if image_url:
            print(f"✅ Chemical Label: {display_name}")
            print(f"🖼️ Image URL: {image_url} (source: {source})")
            if cid:
                print(f"🧬 PubChem CID: {cid}")
        else:
            print("⚠️ No image found for the chemical.")
    except Exception as e:
        print(f"[ERROR] Failed to fetch chemical info: {e}")
        return

    print("\n=== 📚 Searching related research papers ===")
    try:
        papers, source_used = search_papers(display_name)
        if papers:
            print(f"\n📄 Found {len(papers)} papers from {source_used} related to '{display_name}':\n")
            for i, p in enumerate(papers, 1):
                print(f"{i}. 📘 Title: {p['title']}")
                print(f"   📅 Year: {p.get('year', 'Unknown')}")
                print(f"   👨‍🔬 Authors: {p.get('authors', 'N/A')}")
                print(f"   🔗 URL: {p.get('url', 'No URL')}")
                abstract = p.get('abstract', 'No abstract available')
                print(f"   📑 Abstract: {abstract[:300]}{'...' if len(abstract) > 300 else ''}\n")
        else:
            print("⚠️ No papers found.")
    except Exception as e:
        print(f"[ERROR] Failed to fetch papers: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting by user request.")

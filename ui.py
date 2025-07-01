# === File: ui.py ===
import streamlit as st
from chemical_lookup import fetch_pubchem_image
from paper_search import search_papers
from database import save_chemical, load_history, clear_history
from datetime import datetime
from urllib.parse import quote
import pandas as pd

# Cache search results for 1 hour; cache key includes query and limit
@st.cache_data(ttl=3600)
def cached_search_papers(query, limit=10):
    return search_papers(query, limit=limit)

def search_interface():
    chemical_input = st.text_input("Enter chemical name or CAS number:")

    if st.button("🔍 Search"):
        if not chemical_input.strip():
            st.warning("Please enter a valid chemical name.")
            return

        with st.spinner("Fetching chemical info and related papers..."):
            cid, image_url, source, matched_name = fetch_pubchem_image(chemical_input)
            search_term = matched_name or chemical_input

            if cid or image_url:
                if image_url:
                    st.image(image_url, caption=f"{search_term} (Source: {source})", use_container_width=False)
                if cid:
                    st.success(f"CID: {cid}")

                save_chemical(chemical_input, matched_name or "", cid or "N/A", image_url or "")

                st.subheader("📚 Related Papers")
                st.caption(f"Searching papers for: `{search_term}`")

                try:
                    papers, source_used = cached_search_papers(search_term, limit=10)
                    st.markdown(f"✅ Showing up to 10 results from **{source_used}**")
                except Exception as e:
                    st.error("❌ Failed to fetch papers.")
                    st.exception(e)
                    return

                if papers:
                    paper_list = []
                    for p in papers:
                        st.markdown(f"**{p['title']}** ({p['year']})")
                        st.markdown(f"👨‍🔬 *{p.get('authors', 'N/A')}*")
                        st.markdown(f"[🔗 Read more]({p.get('url', '#')})")
                        st.markdown(p.get('abstract', '_No abstract available._'))
                        st.markdown("---")
                        paper_list.append(p)

                    df = pd.DataFrame(paper_list)
                    csv_data = df.to_csv(index=False).encode("utf-8")

                    st.download_button(
                        label="⬇️ Download CSV of Papers",
                        data=csv_data,
                        file_name=f"papers_{search_term.replace(' ', '_').lower()}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No related papers found.")
            else:
                st.warning("🔍 Compound not found in structured chemical databases.")
                query_encoded = quote(chemical_input)
                pubchem_url = f"https://pubchem.ncbi.nlm.nih.gov/#query={query_encoded}"
                wikidata_url = f"https://www.wikidata.org/w/index.php?search={query_encoded}"

                st.info(
                    "⚠️ This compound may still exist in scientific literature, but no structure or CID was found.\n\n"
                    "💡 Try entering a more precise identifier such as:\n"
                    "- CAS number (e.g. `50-00-0`)\n"
                    "- IUPAC name (e.g. `methanal`)\n"
                    "- SMILES notation (e.g. `C=O`)\n\n"
                    f"You can also try searching manually:\n"
                    f"- 🔬 [Search on PubChem]({pubchem_url})\n"
                    f"- 🧠 [Search on Wikidata]({wikidata_url})"
                )

def show_history_section():
    st.markdown("### 🔁 Recent Search History")
    if st.button("🗑️ Clear History"):
        clear_history()
        st.success("Search history cleared!")

    history = load_history(limit=10)
    if history:
        for name, cid, time in history:
            time_str = datetime.fromisoformat(time).strftime("%Y-%m-%d %H:%M")
            st.markdown(f"🧪 **{name}** — CID: `{cid}`  _(at {time_str})_")
    else:
        st.info("No search history yet.")

import os
import re
import shutil
from bs4 import BeautifulSoup
import requests
import streamlit as st

# Streamlit Page Setup
st.set_page_config(
    page_title="Task Automation Toolkit", page_icon="⚡", layout="centered"
)

st.title("⚡ Task Automation Toolkit")
st.write("Automate repetitive tasks: Email Extraction, Web Title Scraping, and File Sorting.")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(
    ["📧 Email Extractor", "🌐 Web Title Scraper", "📁 File Organizer"]
)

# ---------------------------------------------------------
# TAB 1: Extract Email Addresses from Text / File
# ---------------------------------------------------------
with tab1:
    st.subheader("📧 Extract Email Addresses")
    st.write("Extract all valid email addresses from raw text or uploaded `.txt` files.")

    source_choice = st.radio("Choose Input Method:", ["Text Input", "Upload .txt File"])
    raw_text = ""

    if source_choice == "Text Input":
        raw_text = st.text_area(
            "Paste your text here:",
            placeholder="Contact us at support@example.com or sales@company.org",
        )
    else:
        uploaded_file = st.file_uploader("Upload a text file:", type=["txt"])
        if uploaded_file is not None:
            raw_text = uploaded_file.read().decode("utf-8")

    if st.button("Extract Emails", use_container_width=True):
        if raw_text.strip():
            # Regex pattern for email matching
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            found_emails = list(set(re.findall(email_pattern, raw_text)))

            if found_emails:
                st.success(f"Found {len(found_emails)} unique email(s):")
                st.write(found_emails)

                # Save extracted emails to text file for download
                output_content = "\n".join(found_emails)
                st.download_button(
                    label="📥 Download Extracted Emails (.txt)",
                    data=output_content,
                    file_name="extracted_emails.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            else:
                st.warning("No email addresses were found in the provided text.")
        else:
            st.error("Please provide text or upload a file first.")

# ---------------------------------------------------------
# TAB 2: Scrape Webpage Title
# ---------------------------------------------------------
with tab2:
    st.subheader("🌐 Webpage Title Scraper")
    st.write("Fetch and extract the `<title>` tag from any live webpage.")

    url_input = st.text_input(
        "Enter Webpage URL:", value="https://www.example.com"
    )

    if st.button("Scrape Webpage Title", use_container_width=True):
        if url_input:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url_input, headers=headers, timeout=5)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                page_title = soup.title.string.strip() if soup.title else "No Title Tag Found"

                st.success("Successfully scraped webpage title!")
                st.code(f"URL: {url_input}\nTitle: {page_title}", language="text")

                # Save title result to file download
                st.download_button(
                    label="📥 Download Scraped Result (.txt)",
                    data=f"URL: {url_input}\nTitle: {page_title}",
                    file_name="scraped_title.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Error scraping URL: {e}")
        else:
            st.error("Please enter a valid URL.")

# ---------------------------------------------------------
# TAB 3: File Extension Organizer
# ---------------------------------------------------------
with tab3:
    st.subheader("📁 Organize Folder Files")
    st.write("Demonstrates sorting files into subfolders based on extension (`.jpg`, `.pdf`, `.txt`).")

    st.info(
        "Enter a local directory path below to auto-organize files by extension."
    )

    folder_path = st.text_input("Enter Folder Path on your computer:")

    if st.button("Organize Folder", use_container_width=True):
        if folder_path and os.path.exists(folder_path):
            try:
                files = os.listdir(folder_path)
                moved_count = 0

                for file_name in files:
                    file_path = os.path.join(folder_path, file_name)

                    if os.path.isfile(file_path):
                        ext = file_name.split(".")[-1].lower() if "." in file_name else "others"
                        target_dir = os.path.join(folder_path, ext.upper() + "_Files")

                        os.makedirs(target_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(target_dir, file_name))
                        moved_count += 1

                st.success(f"Organized {moved_count} file(s) into category subfolders!")
            except Exception as e:
                st.error(f"Error organizing directory: {e}")
        else:
            st.error("Please enter a valid folder path that exists on your system.")
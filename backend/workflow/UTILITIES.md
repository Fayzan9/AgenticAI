### System Utilities

**System Utilities** are reusable helper tools designed to perform common operational tasks within the workflow system. They operate at the **agent level**, meaning they are not tied to a specific use case and can be reused across multiple workflows, agents, or processes.

These utilities encapsulate frequently needed functionality such as:

* downloading files from the internet,
* reading or processing data,
* scraping or extracting information from web sources,
* running scripts or system operations,
* or performing other generic automation tasks.

If a required capability is not available, a new utility should be created in the **`workflow/utils/`** directory. Once implemented, the utility must be **registered and documented** in the **Available Utilities** section so that other developers and workflows can easily discover and reuse it.

The goal of System Utilities is to **centralize common functionality**, reduce code duplication, and make workflows easier to maintain and extend.

---

## Developing Utilities

**1. Create**
Add the new utility logic to the directory:
`workflow/utils/`

**2. Register**
Add the utility to the **Available Utilities**  below.

**3. Document**
Provide a short description including:

* What the utility does
* Required inputs
* Example usage

---

## Available Utilities

**pdf-text-extractor**
* **Description:** Extracts plain text from PDF files using local libraries.
* **Path:** `utils/pdf_text_extractor.py`
* **Purpose / Usage:** Use when you need to get text from a PDF for analysis, summarization, or processing.
* **Example:**
  `python utils/pdf_text_extractor.py input.pdf -o output.txt`

**file-downloader**
* **Description:** Downloads files from the internet and saves them to the workflow output folder.
* **Path:** `utils/file_downloader.py`
* **Purpose / Usage:** Use when you need to download files from URLs for processing, archival, or analysis. Supports custom output directories and filenames.
* **Example:**
  `python utils/file_downloader.py https://example.com/data.csv`
  `python utils/file_downloader.py https://example.com/report.pdf -f custom_name.pdf`
  `python utils/file_downloader.py https://example.com/file.zip -o /custom/path/`


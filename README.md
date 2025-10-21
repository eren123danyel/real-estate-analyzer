
---

# 🏠 Real Estate Rent Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered tool that utilizes Playwright MCP to scrape, parse, and analyze real estate rental data for a given area.

This repository contains an automated real estate rent analyzer that helps you gather and understand rental listings and neighborhood information through the power of AI.

## ✨ Features

*   **Automated Web Scraping:** Extracts real estate listings from the web using Playwright.
*   **Intelligent Content Parsing:** Structures the scraped data for analysis.
*   **AI-Powered Filtering:** Leverages AI and Playwright MCP to apply filters based on user criteria. 
*   **Dual Interface:** Can be run as a command-line tool for direct analysis or as a FastAPI server for API access.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.10+ (3.11 recommended)
*   Node.js and npm (for running Playwright MCP with `npx`)

These installation steps are for Windows, and the commands provided are for PowerShell.

### 💻 Installation

1.  **Clone the repository:**
    ```powershell
    git clone https://github.com/eren123danyel/real-estate-analyzer.git
    cd real-estate-analyzer
    ```

2.  **Create and activate a virtual environment:**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```powershell
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Install the spaCy English model:**
    ```powershell
    python -m spacy download en_core_web_sm
    ```

5.  **Install Playwright browsers:**
    ```powershell
    python -m playwright install
    # Or, if you encounter issues, you can use the Node tooling:
    # npx playwright install
    ```

### ⚙️ Configuration

This project uses `python-dotenv` to manage environment variables.

1.  Create a `.env` file in the root of the project.
2.  Add your OpenAI API key to the `.env` file:

    ```text
    OPENAI_API_KEY="YOUR-API-KEY"    # Your OpenAI key
    ```

## 🏃‍♀️ Running the Application

You can run this tool as a command-line application or as a web server with an API.

### As a CLI Tool

To get started directly from your terminal:

```powershell
python rentanalyzer.py --help
```

### As an API Server

To start the FastAPI server:

```powershell
python rentanalyzer.py -api
```
The API will then be available at `http://127.0.0.1:8080`.

## 🎬 Demos

Here are some examples of how to use the Real Estate Rent Analyzer.

### 🤖 CLI Demo


```powershell

```

**Expected Output:**

```powershell
```

### 🔌 API Demo

Once the server is running, you can interact with the API. Here’s an example using `curl`:

```powershell

```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

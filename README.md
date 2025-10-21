
---

# 🏠 Real Estate Rent Analyzer
![Playwright](https://img.shields.io/badge/-playwright-%232EAD33?style=for-the-badge&logo=playwright&logoColor=white) ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered tool that utilizes Playwright MCP to scrape, parse, and analyze real estate rental data for a given area.

This repository contains an automated real estate rent analyzer that helps you gather rental listings in specific area based on user criteria. (Currently only works with Redfin)

## ✨ Features

*   **Automated Web Scraping:** Extracts real estate listings from the web using Playwright.
*   **Intelligent Content Parsing:** Structures the scraped data for analysis directly to the terminal or saves it as a CSV file.
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

#### Sample commands
Find rentals in LA and print to terminal:
```powershell
python rentanalyzer.py -l "Los Angeles" 
```

Find rentals in New York City under 3k and save as CSV:
```powershell
python rentanalyzer.py -l "NYC" -m 3000 -o "output.csv" 
```

Find apartments under $3k that have 2+ beds and are dog friendly in Seattle and save as CSV:
```powershell
python rentanalyzer.py -g "Find apartments in Seattle that have 2+ beds and that are dog friendly and under $3k" -o "output.csv" 
```

### As an API Server

To start the FastAPI server:

```powershell
python rentanalyzer.py -api
```
The API will then be available at `http://127.0.0.1:8080`.

When run as a server, two endpoints will be made available:
 - /search_redfin_with_ai
	 - Takes parameter *goal* in natural language, which lets the AI know what to scrape.
 - /search_redfin
	 - Takes *location* and optionally *max_price*.


## 🎬 Demos

Here are some examples of how to use the Real Estate Rent Analyzer.

### 🖥️ CLI Demo w/o AI
![losangeles](https://github.com/user-attachments/assets/8d41cd17-95a6-4521-9040-5bd083ae698f)
![NY](https://github.com/user-attachments/assets/fe31b90f-5c34-4ac7-a971-150e7b51d6be)

### 🤖 CLI Demo w/ AI
![ai](https://github.com/user-attachments/assets/2b0dbb14-c340-43b6-ab30-4a7666bd3592)


### 🔌 API Demo

Once the server is running, you can interact with the API via Swagger UI by going to: (http://127.0.0.1:8080/docs/). 
<img width="1000" alt="image of Swagger UI" src="https://github.com/user-attachments/assets/3bd66498-23e0-4641-9f3f-53008361d4b7" />
<img width="1000" alt="image of successful request" src="https://github.com/user-attachments/assets/a7598b66-8a8e-4222-a7a0-c554f303fc5c" />

You can also make requests using curl, for example:

```powershell
curl.exe -X GET "http://127.0.0.1:8080/search_redfin?location=Seattle" -H "accept: application/json"
```

or

```powershell
curl.exe -X GET "http://127.0.0.1:8080/search_redfin_with_ai?goal=Find%20rental%20listings%20under%203000%20in%20Los%20Angeles" -H "accept: application/json"
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

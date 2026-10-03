# 📄 AI Resume Analyzer

An AI-powered web app that compares a resume against a job description and returns a structured analysis: match score, matched skills, missing skills, experience gaps, and recommended improvements.

## Demo

<img width="1288" height="595" alt="image" src="https://github.com/user-attachments/assets/92e9e950-1c21-4a57-985c-2e9cf0dbbe31" />


## Features

- Upload a resume as a PDF
- Paste any job description
- Get a match score out of 100 with a short summary
- See matched and missing skills side by side
- Get experience gaps and specific, actionable resume improvements

## Tech Stack

- **Python**
- **Streamlit** for the web UI
- **Google Gemini API** (`google-genai`) for the LLM analysis
- **Pydantic** to define the structured output schema
- **pypdf** for extracting text from PDF resumes
- **python-dotenv** for managing the API key

## How It Works

1. `extractor.py` reads the uploaded PDF and extracts its text.
2. `analyzer.py` sends the resume text and job description to Gemini with a system prompt and a Pydantic schema, so the model always returns valid, structured JSON.
3. `app.py` displays the result in a clean Streamlit interface.

## Getting Started

```bash
git clone https://github.com/farazbashirr/resume-analyzer.git
cd resume-analyzer
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

You can get a free key from [Google AI Studio](https://aistudio.google.com/apikey).

Run the app:

```bash
streamlit run app.py
```

## Project Structure

```
resume-analyzer/
├── app.py            # Streamlit UI
├── analyzer.py       # LLM call + structured output
├── extractor.py      # PDF text extraction
├── requirements.txt
└── .gitignore
```

## Challenges and How I Solved Them

- **Structured output:** Free-text LLM answers are hard to display reliably. I defined a Pydantic schema and used Gemini's JSON response mode, so every response has the same fields and the UI never needs to parse messy text.
- **API provider change:** I first built the app with the Claude API using tool use for structured output. Since I had no API credits, I ported it to the Gemini free tier and kept the same output fields, so the UI needed zero changes.
- **Deprecated model:** The first model name I used was no longer available to new users. I updated the model name to the one suggested in the API error message.
- **Server overload (503 errors):** The free tier sometimes returns "high demand" errors. I added retry logic with increasing delays, and the app shows a friendly error if all retries fail.
- **Git push rejected:** The remote repo already had a commit, so I resolved the merge conflict and pushed successfully.

## Future Improvements

- Support DOCX resumes
- Export the analysis as a PDF report
- Rewrite resume bullet points for a specific job
- Deploy the app online (Streamlit Community Cloud)

## Author

**Muhammad Faraz Bashir**
GitHub: [@farazbashirr](https://github.com/farazbashirr)

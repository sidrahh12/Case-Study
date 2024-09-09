# Test Case Generator

This project creates a web-based tool for generating test cases from screenshots and optional context. It uses a multimodal Large Language Model (LLM) to process the input and produce detailed, step-by-step guides for testing functionalities.

The app is hosted live at https://test-cases-generator.streamlit.app/ 

## Features

- Upload multiple screenshot images
- Provide optional context for the application being tested
- Generate detailed test cases automatically
- View generated test cases in a structured format

## How It Works

1. Users upload one or more screenshot images of the application they want to test.
2. Optionally, users can provide additional context about the application or specific features they want to test.
3. Clicking the "Describe Testing Instructions" button triggers the LLM to analyze the images and context.
4. The system generates detailed test cases, including descriptions, pre-conditions, step-by-step instructions, and expected results.

## Requirements

- Python 3.7+
- Streamlit
- Google GenerativeAI SDK
- Pillow (PIL)
- pytesseract
- python-dotenv

## Installation

1. Clone this repository
2. Install the required dependencies:
   
```bash
   pip install -r requirements.txt
```

3. Set up your Google GenerativeAI API key in a `.env` file:
```bash
   GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Run the application:
```bash
   streamlit run Test_Cases.py
```

2. Open a web browser and navigate to `http://localhost:8501`
3. Upload screenshot images and optionally provide context
4. Click "Describe Testing Instructions" to generate test cases

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import base64
import pytesseract
import io
import json
import re

# Setting Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Getting API key froos.getenv('GEMINI_API_KEY')m environment variable
api_key = 'AIzaSyCDDrJ6pqDjnU3zcJffyciYzhSCog9Efw4'

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=api_key)

st.title("Test Case Generator")

# Input fields
image_files = st.file_uploader("Upload Screenshot(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
context = st.text_area("Optional Context")

# Convert image to base64 string
def image_to_base64(image):
    img = Image.open(image)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Extract text from an image using OCR (pytesseract)
def extract_text_from_image(image):
    img = Image.open(image)
    return pytesseract.image_to_string(img)

# Generate test cases using Gemini AI
def generate_test_cases(extracted_text, context):
    # Prepare prompt for Gemini AI
    prompt = f"""
    Based on the following extracted text and context, generate test cases:
    Text: {extracted_text}
    Context: {context if context else 'None provided'}
    
    Return the test cases in the following format:
    {{
        "description": "<description>",
        "pre_conditions": ["<pre_condition_1>", "<pre_condition_2>"],
        "testing_steps": ["<step1>", "<step2>", "..."],
        "expected_result": "<expected_result>"
    }}
    """
    
    # Generate content using Gemini AI
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Send the request
        response = model.generate_content(prompt)
        
        # Access response information correctly
        st.write("Response content:", response.content if hasattr(response, 'content') else str(response))
        st.write("Response status code:", getattr(response, 'status_code', 'Unknown'))
        
        # Parse the JSON-like response
        try:
            parsed_response = json.loads(str(response)) if not hasattr(response, 'content') else json.loads(response.content)
            
            # Validate structure
            expected_structure = {
                "description": str,
                "pre_conditions": list,
                "testing_steps": list,
                "expected_result": str
            }
            
            for key, expected_type in expected_structure.items():
                if not isinstance(parsed_response.get(key), expected_type):
                    raise ValueError(f"Unexpected type for '{key}'")
            
            # Extract test case details
            description = parsed_response['description']
            pre_conditions = parsed_response['pre_conditions']
            testing_steps = parsed_response['testing_steps']
            expected_result = parsed_response['expected_result']

            # Create the final formatted string
            formatted_string = f"{description}\n\nPre-conditions: {', '.join(pre_conditions)}\n\nTesting Steps:\n{' '.join(testing_steps)}\n\nExpected Result: {expected_result}"

            return {
                "description": description, 
                "pre_conditions": pre_conditions, 
                "testing_steps": testing_steps, 
                "expected_result": expected_result
            }
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON response: {str(e)}")
            return {}
        except KeyError as e:
            st.error(f"Missing key in response: {str(e)}")
            return {}
        except Exception as e:
            st.error(f"Error parsing response: {str(e)}")
            return {}
    
    except Exception as e:
        # Display a friendly error message for users
        st.error(f"An error occurred while generating test cases: {str(e)}")
        return {}

# Handle button click
def handle_generate_test_cases():
    test_cases = []
    for i, image in enumerate(image_files, start=1):
        extracted_text = extract_text_from_image(image)
        test_case = generate_test_cases(extracted_text, context)
        test_cases.append(test_case)
    
    return test_cases

# Button with unique key
if st.button('Describe Testing Instructions', key='generate_test_cases'):
    if image_files:
        test_cases = handle_generate_test_cases()
        
        # Display results
        st.write("Generated Test Cases:")
        for i, test_case in enumerate(test_cases, start=1):
            st.subheader(f"Test Case {i}:")
            st.write("Description:")
            st.write(test_case.get('description', 'No description available'))
            st.write("Pre-conditions:")
            st.write(test_case.get('pre_conditions', 'No pre-conditions available'))
            st.write("Testing Steps:")
            st.write("\n".join(test_case.get('testing_steps', ['No steps available'])))
            st.write("Expected Result:")
            st.write(test_case.get('expected_result', 'No expected result available'))
            st.write("---")  

# Display uploaded images
if image_files:
    for i, file in enumerate(image_files):
        st.image(file, caption=f"Uploaded Image {i+1}")
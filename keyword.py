from flask import Flask, request
import openai
import json

# Set up Flask app and OpenAI API key
app = Flask(__name__)
openai.api_key = "YOUR_API_KEY_HERE"

# Define route for ChatGPT endpoint
@app.route("/chat", methods=["POST"])
def chat():
    # Get input from request body
    input_text = request.get_data(as_text=True)

    # Use OpenAI's API to generate a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=input_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract response text from OpenAI API response
    response_text = response.choices[0].text.strip()

    # Return response as JSON
    return json.dumps({"response": response_text})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)



def xtract_risk_code_digital(croped_image_dict, coordinates_dict, written_date, page_number, text_dict):
    ref_risk_dict = {}
    ref_pattern = "[A-Z]{3}[0-9]{3}[A-Z]{1}[0-9]{2}[A-Z]{2}"
    ref_pattern1 = '(?e)(' + ref_pattern + '){e<=1}'
    rx1 = regex.compile(ref_pattern1)
    entity_list = ['510', '1880', '5307', '5332']
    final_output = []
    writ_line_pattern = "(\d*(\.\d+)?%)"
    writ_line_dict = {}
    entity_values = []

    for key, value in croped_image_dict.items():
        for entity in entity_list:
            idx = value.find(entity)
            if idx != -1:
                entity_values.append(entity)

        writ_line_values = []
        for writ_mat in re.finditer(writ_line_pattern, value):
            if re.search("written", value, re.I):
                writ_line_values.append(writ_mat.group())

        if len(writ_line_values) > 0:
            for ref_match in rx1.finditer(value):
                if ref_match.group() not in writ_line_dict:
                    writ_line_dict[ref_match.group()] = []
                writ_line_dict[ref_match.group()].extend(writ_line_values)

    for key, value in croped_image_dict.items():
        syd_list = [""]
        ref_map_dict = {}
        ref_match = ""
        ref_text = value.replace(" ", "").upper()
        syd_list = re.findall("510|1880|5307|5332", ref_text)
        all_ref_matches = re.findall(ref_pattern, ref_text)

        for ref_matches in rx1.finditer(ref_text):
            mid_output = {}
            ref_match = ref_matches.group()
            search_string = " ".join(list(ref_match))
            page_number = get_page_number(text_dict, search_string, page_number)
            entity = ""
            risk_code = []

            for word in master_risk_code_list:
                crop_value = value
                for ref_entity_match in all_ref_matches:
                    ref_search_string = " ".join(list(ref_entity_match))
                    crop_value = crop_value.replace(ref_search_string, "")
                crop_value_list = re.split(',+|\s+', crop_value)
                for risk_code_value in crop_value_list:
                    if risk_code_value == word:
                        risk_code.append(word)

            risk_code = list(set(risk_code))
            ref_risk_dict[ref_match] = risk_code

            if ref_match in writ_line_dict:
                written_line_values = writ_line_dict[ref_match]
                if len(written_line_values) > 0:
                    written_lines = []
                    for written_line in written_line_values:
                        writ_line_value = round((float(written_line.split("%")[0]) * 0.80), 2)
                        written_lines.append(writ_line_value)
                    writ_line_value = max(written_lines)
                else:
                    writ_line_value = 0.0
            else:
                writ_line_value = 0.0

            coords = coordinates_dict[value]
            if len(entity_values) > 1:
                if len(syd_list) > 1:
                    if "510" in syd_list:
                        entity = "510"
                        syd_list.remove(entity)
                        mid_output[ref_match] = {"overall_written_line": str(writ_line_value),
                                                 "written_line": str(writ_line_value),
                                                 "entity": entity,
                                                 "written_date": written_date,
                                                 "Risk_Code": risk_code,
                                                 "page_number": str(page_number),
                                                 "coordinates": coords}
                    
                    if "5307" in syd_list:
                        entity = "5307"
                        syd_list.remove(entity)
                        mid_output[ref_match] = {"overall_written_line": str(writ_line_value),
                                                 "written_line": str(writ_line_value),
                                                 "entity": entity,
                                                 "written_date": written_date,
                                                 "Risk_Code": risk_code,
                                                 "page_number": str(page_number),
                                                 "coordinates": coords}
                    
                    if "1880" in syd_list:
                        entity = "1880"
                        syd_list.remove(entity)
                        mid_output[ref_match] = {"overall_written_line": str(writ_line_value),
                                                 "written_line": str(writ_line_value),
                                                 "entity": entity,
                                                 "written_date": written_date,
                                                 "Risk_Code": risk_code,
                                                 "page_number": str(page_number),
                                                 "coordinates": coords}
            
                    if "5332" in syd_list:
                        entity = "5332"
                        syd_list.remove(entity)
                        mid_output[ref_match] = {"overall_written_line": str(writ_line_value),
                                                 "written_line": str(writ_line_value),
                                                 "entity": entity,
                                                 "written_date": written_date,
                                                 "Risk_Code": risk_code,
                                                 "page_number": str(page_number),
                                                 "coordinates": coords}
                else:
                    if "510" in syd_list or "5307" in syd_list:
                        entity = syd_list[0]
                        mid_output[ref_match] = {"overall_written_line": str(writ_line_value),
                                                 "written_line": str(writ_line_value),
                                                 "entity": entity,
                                                 "written_date": written_date,
                                                 "Risk_Code": risk_code,
                                                 "page_number": str(page_number),
                                                 "coordinates": coords}
                    elif "1880" in syd_list or "5332" in syd_list:
                        entity = syd_list[0]
                        mid_output[ref_match] = {"overall_written_line": str(writ_line_value),
                                                 "written_line": str(writ_line_value),
                                                 "entity": entity,
                                                 "written_date": written_date,
                                                 "Risk_Code": risk_code,
                                                 "page_number": str(page_number),
                                                 "coordinates": coords}
            else:
                if len(syd_list) > 0:
                    entity = syd_list[0]
                else:
                    entity = ""
                mid_output[ref_match] = {"overall_written_line": str(writ_line_value),
                                         "written_line": str(writ_line_value),
                                         "entity": entity,
                                         "written_date": written_date,
                                         "Risk_Code": risk_code,
                                         "page_number": str(page_number),
                                         "coordinates": coords}

            if len(mid_output) > 0:
                final_output.append(mid_output)

    return final_output
























































import boto3
import io
import pandas as pd
from PIL import Image

# Create a Textract client
textract = boto3.client('textract')

# Specify the S3 bucket and key of the image
s3_bucket = 'your_s3_bucket'
s3_key = 'your_s3_key.jpg'

# Load a DataFrame containing the coordinates of the regions to extract text from
region_df = pd.read_csv('region_coordinates.csv')

# Loop over each row in the DataFrame and extract text from the specified region
for i, row in region_df.iterrows():
    x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
    print(f"Extracting text from region {i+1} ({x1}, {y1}) - ({x2}, {y2})...")
    
    # Download the image from S3
    s3 = boto3.resource('s3')
    image_obj = s3.Object(s3_bucket, s3_key).get()
    image = Image.open(io.BytesIO(image_obj['Body'].read()))

    # Crop the image to the specified region
    region_image = image.crop((x1, y1, x2, y2))

    # Convert the image to JPEG format and save it to a bytes buffer
    jpeg_buffer = io.BytesIO()
    region_image.save(jpeg_buffer, format='JPEG')
    image_bytes = jpeg_buffer.getvalue()

    # Create a Textract request to analyze the specified region of the image
    textract_request = {
        'Document': {
            'Bytes': image_bytes
        },
        'FeatureTypes': ['TABLES', 'FORMS']
    }

    # Call Textract to analyze the image and extract the specified region of text
    response = textract.analyze_document(Document=textract_request)

    # Extract the raw text from the Textract response
    raw_text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            for word in block['Relationships'][0]['Ids']:
                for item in response['Blocks']:
                    if item['Id'] == word and item['BlockType'] == 'WORD':
                        raw_text += item['Text'] + ' '

    print(f"Text extracted from region {i+1}:")
    print(raw_text)
    print()
    
    # Specify the bucket and folder
bucket_name = 'your-bucket-name'
folder_name = 'your-folder-name'

# List all objects in the folder
objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

# Iterate over the objects
for obj in objects['Contents']:
    key = obj['Key']
    if key.lower().endswith('.pdf'):  # Check if the object is a PDF file
        # Download the PDF file into memory
        response = s3.get_object(Bucket=bucket_name, Key=key)
        file_data = response['Body'].read()

        # Read the PDF content using PyPDF2
        with BytesIO(file_data) as file:
            pdf_reader = PyPDF2.PdfFileReader(file)

            # Iterate over the pages and extract the text
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text = page.extractText()
                print(f"Content of {key} - Page {page_num + 1}:\n{text}\n")


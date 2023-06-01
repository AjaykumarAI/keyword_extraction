import json
import boto3
import re

def load_textract_json(bucket_name, file_name):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = json.loads(obj['Body'].read().decode('utf-8'))  # decode the bytes to string and then load as json
    return data

def add_spaces(string):
    return ' '.join(string)

def find_string_and_percentage_and_dates(response, search_string, page):
    search_string_box = None
    percentages_near_search = []
    dates_near_search = []
    current_page = 0
    date_pattern = r"\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/(19|20)\d\d\b"
    percentage_pattern = r"\b\d{1,3}\.\d{1,2}%\b"
    for item in response["Blocks"]:
        if item["BlockType"] == "PAGE":
            current_page += 1
        if current_page == page and item["BlockType"] == "LINE":
            text = item.get("Text", "")
            if search_string in text:
                search_string_box = item["Geometry"]["BoundingBox"]
            else:
                percentage_matches = re.findall(percentage_pattern, text)
                if percentage_matches and search_string_box is not None:
                    percentage_box = item["Geometry"]["BoundingBox"]
                    # If the percentage_box is to the left side of the search_string_box
                    if search_string_box["Top"] <= percentage_box["Top"] and percentage_box["Left"] + percentage_box["Width"] <= search_string_box["Left"]:
                        percentages_near_search.append((percentage_matches, percentage_box))
                else:
                    date_matches = re.findall(date_pattern, text)
                    if date_matches:
                        date_box = item["Geometry"]["BoundingBox"]
                        dates_near_search.append((date_matches, date_box))

    return percentages_near_search, dates_near_search

bucket_name = '<your_bucket_name>'  # replace with your bucket name
file_name = '<your_file_name>'  # replace with your file name

search_string = "hello"
search_string = add_spaces(search_string)
page = 2  # The page number you want to search

response = load_textract_json(bucket_name, file_name)
percentages, dates = find_string_and_percentage_and_dates(response, search_string, page)

for percentage in percentages:
    print(f"Found '{percentage[0]}' at coordinates {percentage[1]}")

for date in dates:
    print(f"Found '{date[0]}' at coordinates {date[1]}")

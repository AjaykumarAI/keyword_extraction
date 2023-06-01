import json

def load_textract_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

def add_spaces(string):
    return ' '.join(string)

def find_string_and_percentage(response, search_string, page):
    search_string_box = None
    percentages_near_search = []
    current_page = 0
    for item in response["Blocks"]:
        if item["BlockType"] == "PAGE":
            current_page += 1
        if item["BlockType"] == "LINE" and current_page == page:
            text = item["Text"]
            if search_string in text:
                search_string_box = item["Geometry"]["BoundingBox"]
            elif '%' in text and search_string_box is not None:
                percentage_box = item["Geometry"]["BoundingBox"]
                # Check if percentage is near the search string horizontally and on the same line or below
                if search_string_box["Top"] <= percentage_box["Top"] and search_string_box["Left"] < percentage_box["Left"] <= search_string_box["Left"] + 0.1:
                    percentages_near_search.append((text, percentage_box))

    return percentages_near_search

json_file = "<your_json_file_path>"
search_string = "hello"
search_string = add_spaces(search_string)  # add spaces to the search string
page = 2  # The page number you want to search
response = load_textract_json(json_file)
percentages = find_string_and_percentage(response, search_string, page)

for percentage in percentages:
    print(f"Found '{percentage[0]}' at coordinates {percentage[1]}")

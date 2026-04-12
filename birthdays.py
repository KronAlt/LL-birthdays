#Program to create a table with birthdays from calendar.json
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#calendar.json file based on https://github.com/ratius/LLS/blob/master/data/calendar.json
#GPL doesn't apply to calendar.json.


import json
from collections import defaultdict
from datetime import datetime

def load_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def process_birthday_data(data):
    #Group the birthdays by month (keyed by month)
    birthdays_by_month = defaultdict(list)
    character_images = {}  #Store character name -> image mappings

    for person in data:
        birth_date = person["birth"]
        month = birth_date[:2]  #Get the month part (first two digits)
        day = int(birth_date[2:])  #Get the day part (last two digits)

        #Add to the correct month and day group
        if person["group"] == "llsif":
            continue #Skip game-only characters
            
        #Store character images for lookup
        if person["type"] == "C":
            character_images[person["name"]] = person["image"]
            
        birthdays_by_month[month].append({
            "name": person["name_en"],
            "name_hover": person["name"],
            "birth": birth_date,
            "image": person["image"],
            "day": day,
            "group": person["group"],
            "type": person["type"],
            "character": person.get("character", ""),
            "tips": person["tips"] if "tips" in person.keys() else ""
        })

    #Sort each month's birthdays by day
    for month, birthdays in birthdays_by_month.items():
        birthdays.sort(key=lambda x: x["day"])

    return birthdays_by_month, character_images

def generate_html(birthdays_by_month, character_images):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Birthday List</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            h2 {
                color: #4CAF50;
            }
            .month {
                margin-top: 30px;
            }
            .birthday-list {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .birthday-item {
                border: 1px solid #ccc;
                padding: 5px;
                text-align: center;
                width: 150px;
                position: relative;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .birthday-item img {
                width: 100px;
                height: 130px;
                object-fit: cover;
            }

            .birthday-item p {
                margin-top: 5px;
                margin-bottom: 5px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }

            .birthday-item .group-logo-container {
                display: flex;
                align-items: center;
                justify-content: flex-start; /* Align text and logo to the left */
                gap: 5px;
                font-size: 14px;
                width: 100%;
                padding-left: 10px; /* Small left padding for better spacing */
            }

            .birthday-item .group-logo {
                width: 45px;
                height: 20px;
            }
            .birthday-item .small-circle {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                object-fit: cover;
                position: absolute;
                top: 5px;
                right: 5px;
                background-color: white;
            }
        </style>
    </head>
    <body>
        <h1>Character Birthdays by Month</h1>
    """
    
    #Group logos dictionary
    group_logos = {
        "muse": "https://i.idol.st/static/img/i_unit/%CE%BC-s.png?0",
        "a-rise": "https://i.idol.st/static/img/i_unit/A-RISE.png?&0",
        "aqours": "https://i.idol.st/static/img/i_unit/Aqours.png?0",
        "saint-snow": "https://i.idol.st/static/img/i_unit/Saint-Snow.png?&0",
        "niji": "https://i.idol.st/static/img/i_unit/Nijigasaki-High-School.png?0",
        "liella": "https://i.idol.st/static/img/i_unit/Liella.png?0",
        "sunny-passion": "https://i.idol.st/static/img/i_unit/Sunny-Passion.png?&0",
        "musical": "https://i.idol.st/static/img/i_unit/School-Idol-Musical.png?0",
        "hasu": "https://i.idol.st/static/img/i_unit/Hasunosora-Girls-High-School-Idol-Club.png?0",
        "musical-drama": "https://i.imgur.com/EZ9ncn6.png",
        "bluebird": "https://i.imgur.com/56JKoVy.png",
    }

    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "99"]
    months_name = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December", "99": "Unknown birthday"}

    #Add the birthdays for each month
    for month in months:
        if month in birthdays_by_month:
            html += f'<div class="month"><h2>{months_name[month]}</h2><div class="birthday-list">'

            for person in birthdays_by_month[month]:
                #Determine the logo based on the group
                group_logo = group_logos.get(person["group"], "")  # Get logo, default to empty if not found
                
                #Get character image if person is a seiyuu
                character_image = ""
                if person["type"] == "V" and person["character"] in character_images:
                    character_image = character_images[person["character"]]
                
                html += f'''
                    <div class="birthday-item">
                        <img src="{person['image']}" alt="{person['name']}">
                        <p title="{person['name_hover']}">{person['name']}</p>
                '''
                
                #Add small circle image for seiyuus
                if character_image:
                    html += f'<img src="{character_image}" alt="{person["character"]}" class="small-circle">'
                    
                html +='<div class="group-logo-container">'       
                #Add the group logo if available
                if group_logo:
                    html += f'<img src="{group_logo}" alt="{person["group"]} logo" class="group-logo">'
                if person["birth"]=="9999": #unknown
                	html += f'</div></div>'
                else:
                	html += f'{person["birth"][:2]}-{person["birth"][2:]}</div></div>'
                
                

            
            html += '</div>'

    html += """
    </body>
    </html>
    """

    return html

#Main function
def create_birthday_html_file():
    #Load the data from the calendar.json file
    data = load_json_data('calendar.json')
    
    #Process the data to group birthdays by month
    birthdays_by_month, character_images = process_birthday_data(data)
    
    #Generate the HTML content
    html_content = generate_html(birthdays_by_month, character_images)
    
    #Write the HTML content to a file
    with open("birthdays.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("HTML file generated: birthdays.html")

#Run the program
create_birthday_html_file()


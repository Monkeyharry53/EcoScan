from flask import Flask, request, render_template, jsonify, redirect, url_for,render_template_string,send_file,Response
import os
import base64
from roboflow import Roboflow
from PIL import Image, ImageDraw, ImageFont
#from ultralytics import YOLO
import sqlite3
from datetime import datetime
import csv

app = Flask(__name__)
app.config['DATABASE'] = 'feedbacks.db' #SQLite database file
count = 0
current_time = None
def get_db():
    db = getattr(app, '_database', None)
    if db is None:
        db = sqlite3.connect(app.config['DATABASE'],check_same_thread=False)
        app._database = db
    return db

def create_table():
    db = sqlite3.connect('feedbacks.db')  # Replace 'your_database.db' with your desired database file name
    cursor = db.cursor()

    # SQL statement to create the table
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feedback TEXT,
        prediction_correct INTEGER,
        information_helpful INTEGER,
        current_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''

    cursor.execute(create_table_sql)
    db.commit()
    db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    global count, current_time 
    count = 0
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")  # Get current timestamp

    image_data = request.form['image']
    filename = 'user_image.png'  # You can use a unique filename if needed
    filepath = os.path.join(app.static_folder, filename)

    # Remove the data URL prefix and decode the base64 image data
    _, encoded_data = image_data.split(',')
    decoded_data = base64.b64decode(encoded_data)

    with open(filepath, 'wb') as f:
        f.write(decoded_data)

    # Redirect to the capture.html page to display the captured image
    return redirect(url_for('display_capture'))


@app.route('/display_capture', methods=['POST','GET'])
def display_capture():
    global count, current_time
    
    if request.method == 'POST':
        print('i;m working')
        data = request.get_json()
        feedback = data['feedback']
        prediction_correct = data['prediction_correct']
        information_helpful = data['information_helpful']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO feedbacks (feedback, prediction_correct, information_helpful, current_time) VALUES (?,?,?,?)',
                       (feedback, prediction_correct, information_helpful,current_time))

        db.commit()
        return redirect(url_for('display_capture'))
    
    create_table()
 

    if count == 1:
        return render_template('capture.html')
    
    rf = Roboflow(api_key="YOUR API")
    project = rf.workspace("material-identification").project("garbage-classification-3")
    #model = YOLO("C:/Users/manjo/rgc/runs/detect/train/weights/best.pt")
    model = project.version(2).model
   
    predict = model.predict("static/user_image.png", confidence=40, overlap=30)
    #model.predict("static/user_image.png", confidence=50, overlap=30).save("prediction.jpg")
    length = len(predict)
    print(length)

    #for i in range(0,1):
    if (length == 0):
        return render_template('capture.html')

    else:
        count = 1
        print(predict.predictions[0]["class"])
        type = predict.predictions[0]["class"]
        if (type == "BIODEGRADABLE"):
            model.predict("static/user_image.png", confidence=40, overlap=30).save("prediction.jpg")

            # Open the prediction image with Pillow
            image = Image.open("prediction.jpg")
            draw = ImageDraw.Draw(image)
            # Define the text and style properties
            text = "COMPOST"
            font_size = 30
            font_color = (150, 75, 0)
            font = ImageFont.truetype("arial.ttf", font_size)

            # Calculate the text position
            text_width, text_height = draw.textsize(text, font=font)
            text_x = image.width - text_width - 10  # Adjust the x position as needed
            text_y = image.height - text_height - 10  # Adjust the y position as needed

            # Draw the text on the image
            draw.text((text_x, text_y), text, font=font, fill=font_color)
            # Save the final image with the text
            final_image_path = "static/user_image.png"
            image.save(final_image_path)

            
            final_image_filename = f"{current_time}.png" 
            final_image_path_t = os.path.join("image", final_image_filename)
            image.save(final_image_path_t)
            # Print the path to the final image
            print("Final image saved:", final_image_path)

        elif (type == "CARDBOARD" or type == "PAPER"  or type == "CLOTH" or type == "GLASS" or type == "METAL" or type == "PLASTIC"):

            model.predict("static/user_image.png", confidence=40, overlap=30).save("prediction.jpg")

            # Open the prediction image with Pillow
            image = Image.open("prediction.jpg")
            draw = ImageDraw.Draw(image)
            # Define the text and style properties
            text = "recycle"
            font_size = 30
            font_color = (0, 0, 255)  # White color
            font = ImageFont.truetype("arial.ttf", font_size)

            # Calculate the text position
            text_width, text_height = draw.textsize(text, font=font)
            text_x = image.width - text_width - 10  # Adjust the x position as needed
            text_y = image.height - text_height - 10  # Adjust the y position as needed

            # Draw the text on the image
            draw.text((text_x, text_y), text, font=font, fill=font_color)
            # Save the final image with the text
            final_image_path = "static/user_image.png"
            image.save(final_image_path)

           
            final_image_filename = f"{current_time}.png" 
            final_image_path_t = os.path.join("image", final_image_filename)
            image.save(final_image_path_t)
            # Print the path to the final image
            print("Final image saved:", final_image_path)

        else:
        
            model.predict("static/user_image.png", confidence=40, overlap=30).save("prediction.jpg")
            # Open the prediction image with Pillow
            image = Image.open("prediction.jpg")
            draw = ImageDraw.Draw(image)
            # Define the text and style properties
            text = "garbage"
            font_size = 30
            font_color = (0, 0, 0)  # White color
            font = ImageFont.truetype("arial.ttf", font_size)
            # Calculate the text position
            text_width, text_height = draw.textsize(text, font=font)
            text_x = image.width - text_width - 10  # Adjust the x position as needed
            text_y = image.height - text_height - 10  # Adjust the y position as needed
            # Draw the text on the image
            draw.text((text_x, text_y), text, font=font, fill=font_color)
            # Save the final image with the text
            final_image_path = "static/user_image.png"
            image.save(final_image_path)
            # Print the path to the final image
            
            final_image_filename = f"{current_time}.png" 
            final_image_path_t = os.path.join("image", final_image_filename)
            image.save(final_image_path_t)
            
            print("Final image saved:", final_image_path)


    return render_template('capture.html')



# ...

@app.route('/download_csv')
def download_csv():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM feedbacks')
    feedbacks = cursor.fetchall()

    # Define the CSV file path
    csv_filename = 'feedbacks.csv'
    csv_filepath = os.path.join(app.static_folder, csv_filename)

    # Convert the feedbacks data to CSV format
    with open(csv_filepath, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([column[0] for column in cursor.description])  # Write CSV header
        csv_writer.writerows(feedbacks)  # Write CSV data rows

    # Read the CSV file data
    with open(csv_filepath, 'r') as file:
        csv_data = file.read()

    # Send the CSV file data as a response for download
    response = Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename={csv_filename}'}
    )
    return response

if __name__ == '__main__':
    app.run()

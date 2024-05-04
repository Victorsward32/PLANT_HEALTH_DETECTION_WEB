from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np



app = Flask(__name__)
app.static_folder = 'templates'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('ChatBot.html')

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')


@app.route('/color-detection', methods=['POST'])
def detect_color():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Get the uploaded file
    uploaded_file = request.files['file']

    # Read the image
    img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of colors in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([20, 255, 255])

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    lower_green = np.array([36, 25, 25])
    upper_green = np.array([70, 255, 255])

    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    # Create binary masks for each color
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Calculate the number of pixels for each color
    red_pixels = cv2.countNonZero(red_mask)
    orange_pixels = cv2.countNonZero(orange_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    green_pixels = cv2.countNonZero(green_mask)
    blue_pixels = cv2.countNonZero(blue_mask)

    # Calculate the total number of pixels in the image
    total_pixels = img.shape[0] * img.shape[1]

    # Calculate the percentage of each color in the image
    red_percentage = round((red_pixels / total_pixels) * 100, 2)
    orange_percentage = round((orange_pixels / total_pixels) * 100, 2)
    yellow_percentage = round((yellow_pixels / total_pixels) * 100, 2)
    green_percentage = round((green_pixels / total_pixels) * 100, 2)
    blue_percentage = round((blue_pixels / total_pixels) * 100, 2)

    # # Render the HTML template with the color detection results
    # return render_template('index.html', 
    #                        red_percentage=red_percentage,
    #                        orange_percentage=orange_percentage,
    #                        yellow_percentage=yellow_percentage,
    #                        green_percentage=green_percentage,
    #                        blue_percentage=blue_percentage)

    # Return the results as a JSON object
    return jsonify({
        "Red Percentage": red_percentage,
        "Orange Percentage": orange_percentage,
        "Yellow Percentage": yellow_percentage,
        "Green Percentage": green_percentage,
        "Blue Percentage": blue_percentage,
    })

# Error handler for 404 Not Found error
@app.errorhandler(404)
def page_not_found(error):
    return "404 Not Found", 404

if __name__ == '__main__':
    app.run(debug=True)

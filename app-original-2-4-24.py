
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_ngrok import run_with_ngrok
import os
import random

# Set the upload folder
UPLOAD_FOLDER = '/content/static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create a Flask app
app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when the app is run

# Set the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Get the list of uploaded image filenames
uploaded_images = [filename for filename in os.listdir(UPLOAD_FOLDER) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
current_image_index = 0  # Index to track the current image being displayed

# Define the home route
@app.route("/")
def home():
    global current_image_index
    current_image = uploaded_images[current_image_index]
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
    return render_template("index.html", current_image=current_image, image_path=image_path, uploaded_images=uploaded_images)

# Define the route for handling file uploads
# Define the route for handling file uploads
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'files[]' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('files[]')

        # If the user does not select a file, t
        if not files:
            return redirect(request.url)

        # Save the uploaded files
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        # Redirect to the home page after successful file upload
        return redirect(url_for('home'))

    # If the request method is GET, render the home page
    return render_template("index.html")

# Define the route for showing the next image
@app.route("/next")
def next_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(uploaded_images)
    return redirect(url_for('home'))

# Define the route for showing the previous image
@app.route("/previous")
def previous_image():
    global current_image_index
    current_image_index = (current_image_index - 1) % len(uploaded_images)
    return redirect(url_for('home'))

# Define the route for handling bounding box request
@app.route("/bounding_box", methods=["POST"])
def get_bounding_box():
    global current_image_index
    coordinates = request.json['coordinates']
    
    # Generate random bounding box
    x, y = coordinates
    width = random.uniform(10, 50)
    height = random.uniform(10, 50)

    return jsonify({
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'color': 'red'
    })

# Run the app
if __name__ == "__main__":
    app.run()
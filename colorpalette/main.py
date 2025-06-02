from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, DecimalRangeField
from wtforms.validators import DataRequired, NumberRange
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)
from scipy.ndimage.interpolation import zoom

sum_pixels = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class ShowColorsForm(FlaskForm):
    file = FileField("Upload File")
    color_num = IntegerField("Number of colors", default=10 , validators=[DataRequired(), NumberRange(min=1, max=50, message="Please choose a number between 0 and 51")])
    accuracy = IntegerField("Accuracy (px)", default=20, validators=[DataRequired(), NumberRange(min=1, max=50, message="Please choose a number between 0 and 51")])
    quality = DecimalRangeField("Quality (the lower the faster)", default=0.5, validators=[NumberRange(min=0, max=1)])
    submit = SubmitField("Show Colors")

# Saves the chosen file into static and then deletes the previous uploaded file
def upload_file(form):
    filename = secure_filename(form.file.data.filename)
    if filename:
        form.file.data.save('static/' + filename)
        arr = next(os.walk('./static'))[2]
        for file in arr:
            if file != "example.jpg" and file != filename:
                os.remove(f"./static/{file}")

# Returns either the standard image or the uploaded image
def grab_image():
    arr = next(os.walk('./static'))[2]
    if len(arr) == 1:
        return "example.jpg"
    else:
        new_image = [filename for filename in arr if filename != 'example.jpg']
        return new_image[0]

def find_colors(img, color_num, accuracy, quality_reduce):
    # load the image and convert into numpy array
    image = Image.open(f"static/{img}")

    # convert PIL image into NumPy array
    rgb_3d_array = np.asarray(image)

    # reduce pixels to improve calculation speed
    small_rgb_3d_array = zoom(rgb_3d_array, (quality_reduce, quality_reduce, 1))
    global sum_pixels
    sum_pixels = int(small_rgb_3d_array.shape[0]*small_rgb_3d_array.shape[1])

    # Define a function
    def round_up(x):
        return accuracy * round(x/accuracy)

    rgb_3d_array_rounded = np.array([[[round_up(i) for i in el] for el in row] for row in small_rgb_3d_array])

    # transform list from 3d into 1d, by combining 3rd dim into a string for each element
    rgb_list = []
    for row in rgb_3d_array_rounded:
        for el in row:
            # rgb_list.append(f"{el[0]}, {el[1]}, {el[2]}")
            rgb_list.append((el[0], el[1], el[2]))

    # count occurences of rgb-combinations in list
    rgb_counter = dict()
    for el in rgb_list:
        if el not in rgb_counter:
            rgb_counter[el] = 1
        else:
            rgb_counter[el] += 1

    # sort dictionary
    sorted_counter = sorted(rgb_counter.items(), key=lambda x: x[1], reverse=True)
    return sorted_counter[:color_num]

def calc_perc(counter):
    return [round(tuple[1] / sum_pixels * 100, 2) for tuple in counter]

def find_color_names(color):
    def convert_rgb_to_names(rgb_tuple):
        # a dictionary of all the hex and their respective names in css3
        css3_db = CSS3_HEX_TO_NAMES
        names = []
        rgb_values = []
        for color_hex, color_name in css3_db.items():
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))

        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return names[index].title()

    return convert_rgb_to_names(color[0])

@app.route("/", methods=["GET", "POST"])
def home():
    color_num = 5
    accuracy = 20
    quality_reduce = 0.3
    form = ShowColorsForm()
    if form.validate_on_submit():
        upload_file(form)
        color_num = form.color_num.data
        accuracy = form.accuracy.data
        quality_reduce = form.quality.data

    img = grab_image()
    top_colors = find_colors(img, color_num, accuracy, quality_reduce)
    color_names = [find_color_names(color) for color in top_colors]
    percentages = calc_perc(top_colors)
    return render_template("index.html", form=form, img=img, top_colors=top_colors, color_names=color_names, zip=zip, percentages=percentages)

if __name__ == '__main__':
    app.run(debug=True)
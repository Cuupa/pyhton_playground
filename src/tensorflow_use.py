import numpy as np
import tensorflow as tf
from flask import request, Flask

model = tf.keras.models.load_model('/home/simon/Schreibtisch/damaged_cars_model')

app = Flask(__name__)


@app.route('/classify', methods=['POST'])
def classify():
    file = request.files['file']
    # img_data = np.fromstring(request.data, np.uint8)
    # image = cv2.imdecode(img_data, np.uint8)

    image = np.array(file)

    # image_generator = ImageDataGenerator(rescale=1. / 255)
    # data = image_generator.flow(file)

    result = model.predict(image)
    print(result)


@app.route('/', methods=['GET'])
def root():
    return "200"


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True)

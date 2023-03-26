# import numpy as np
# from keras.models import load_model
# import efficientnet.keras as efn
# from PIL import Image

# LABELS = ['normal', 'adenocarinoma']

# filePath = "ml/tf_model.h5"
# model = load_model(filePath)

def model_predict(image):
    # image = Image.open(image)
    # image = image.resize((224, 224))
    # image_array = np.array(image)
    # result = model.predict(image_array[np.newaxis, ...])
    # print('prediction: ', result)
    # prediction = np.argmax(result)
    # return LABELS[prediction]
    return 'normal'

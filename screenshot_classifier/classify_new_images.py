from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import numpy as np


# Define a function to perform majority voting on multiple image crops
def classify_image_majority_voting(image_path, num_crops=5):
    # # Load and preprocess the image
    # image = load_and_preprocess_image(image_path)

    # # Generate multiple random crops of the image
    # crops = generate_random_crops(image, num_crops)

    # # Make predictions for each crop using the loaded model
    # predictions = [model.predict(np.expand_dims(crop, axis=0))[0] for crop in crops]

    # # Perform majority voting on the predictions
    # majority_vote = np.argmax(np.sum(predictions, axis=0))

    # # Return the predicted class label
    # return majority_vote
    return

# Define a function to perform majority voting on multiple image crops
def classify_image(model, image_path) :
    img_height, img_width = 256, 256

    img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    prediction = model.predict(img_array)[0][0]
    predicted_class = "bad_images" if prediction < 0.5 else "good_images"
    print(image_path, " : ", prediction, predicted_class)
    with open("predictions_" + predicted_class + ".txt", "a") as f:
      print(image_path, f)
    return 

def classify_new_images(images_names, folder):
    # Load the saved model
    model = load_model("screenshot_classifier/resnet50.h5")

    # Read images to process
    with open(images_names, "r") as f:
        for image_name in f:
            classify_image(model, folder + "/" + image_name.strip() + ".png")

    return

if __name__ == "__main__":
    experiment ="websites_majestic_million2"
    folder = "results_" + experiment
    images_names = "included_" + folder + ".txt" 
    classify_new_images(images_names, folder)


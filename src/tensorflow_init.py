import os
from math import ceil

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.models import Sequential


def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20, 20))
    axes = axes.flatten()
    for img, ax in zip(images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def init_model():
    zip_file = '/home/simon/Schreibtisch/cars_damage_dataset.zip'
    url = 'https://drive.google.com/file/d/1IYx9kCFgCWUJgudc8Uxn59CkExRei431'

    path_to_zip = tf.keras.utils.get_file(zip_file, origin=url, extract=True)
    PATH = os.path.join(os.path.dirname(path_to_zip), 'cars_filtered')

    # Trainings- und Validierungsordner
    undamaged_damaged_cars_dir = os.path.join(PATH, 'data1a')
    # Trainingsdaten #
    # ============== #
    cars_training_dir = os.path.join(undamaged_damaged_cars_dir, 'training')
    # Unbeschädigte Autos
    undamaged_cars_training_dir = os.path.join(cars_training_dir, '01-whole')
    # beschädigte Autos
    damaged_cars_training_dir = os.path.join(cars_training_dir, '00-damage')

    # Validierungsdaten #
    # ================= #
    cars_validation_dir = os.path.join(undamaged_damaged_cars_dir, 'validation')
    # Unbeschädigte Autos
    undamaged_cars_validation_dir = os.path.join(cars_validation_dir, '01-whole')
    # beschädigte Autos
    damaged_cars_validation_dir = os.path.join(cars_validation_dir, '00-damage')

    # Position des Schadens
    damage_position_dir = os.path.join(PATH, 'data2a')
    # Trainingsdaten #
    # ============== #
    position_training_dir = os.path.join(damage_position_dir, 'training')
    front_position_training_dir = os.path.join(position_training_dir, '00-front')
    rear_position_training_dir = os.path.join(position_training_dir, '01-rear')
    side_position_training_dir = os.path.join(position_training_dir, '02-side')

    # Validierungsdaten #
    # ================= #
    position_validation_dir = os.path.join(damage_position_dir, 'validation')
    front_position_validation_dir = os.path.join(position_validation_dir, '00-front')
    rear_position_validation_dir = os.path.join(position_validation_dir, '01-rear')
    side_position_validation_dir = os.path.join(position_validation_dir, '02-side')

    # Schadenart
    damage_severity_dir = os.path.join(PATH, 'data3a')
    # Trainingsdaten #
    # ============== #
    severity_training_dir = os.path.join(damage_severity_dir, 'training')
    minor_severity_training_dir = os.path.join(severity_training_dir, '01-minor')
    moderate_severity_training_dir = os.path.join(severity_training_dir, '02-moderate')
    severe_severity_training_dir = os.path.join(severity_training_dir, '03-severe')

    # Validierungsdaten #
    # ================= #
    severity_validation_dir = os.path.join(damage_severity_dir, 'validation')
    minor_severity_validation_dir = os.path.join(severity_validation_dir, '01-minor')
    moderate_severity_validation_dir = os.path.join(severity_validation_dir, '02-moderate')
    severe_severity_validation_dir = os.path.join(severity_validation_dir, '03-severe')

    # Debugausgaben
    num_undamaged_cars_train = len(os.listdir(undamaged_cars_training_dir))
    num_damaged_cars_train = len(os.listdir(damaged_cars_training_dir))

    num_front_train = len(os.listdir(front_position_training_dir))
    num_rear_train = len(os.listdir(rear_position_training_dir))
    num_side_train = len(os.listdir(side_position_training_dir))

    num_minor_train = len(os.listdir(minor_severity_training_dir))
    num_moderate_train = len(os.listdir(moderate_severity_training_dir))
    num_severe_train = len(os.listdir(severe_severity_training_dir))

    num_total_train = num_undamaged_cars_train + num_damaged_cars_train + num_front_train + num_rear_train + num_side_train + num_minor_train + num_moderate_train + num_severe_train

    num_undamaged_cars_val = len(os.listdir(undamaged_cars_validation_dir))
    num_damaged_cars_val = len(os.listdir(damaged_cars_validation_dir))

    num_front_val = len(os.listdir(front_position_validation_dir))
    num_rear_val = len(os.listdir(rear_position_validation_dir))
    num_side_val = len(os.listdir(side_position_validation_dir))

    num_minor_val = len(os.listdir(minor_severity_validation_dir))
    num_moderate_val = len(os.listdir(moderate_severity_validation_dir))
    num_severe_val = len(os.listdir(severe_severity_validation_dir))

    print('Meine Trainingsdaten sind:')
    print('Unbeschädigte Autos: ', num_undamaged_cars_train)
    print('Beeschädigte Autos: ', num_damaged_cars_train)
    print('Schäden vorne: ', num_front_train)
    print('Schäden hinten: ', num_rear_train)
    print('Schäden seitlich: ', num_side_train)
    print('Kleinere Schäden: ', num_minor_train)
    print('Moderate Schäden: ', num_moderate_train)
    print('Schwere Schäden: ', num_severe_train)

    print('--')

    print('Meine Validierungsdaten sind:')
    print('Unbeschädigte Autos: ', num_undamaged_cars_val)
    print('Beeschädigte Autos: ', num_damaged_cars_val)
    print('Schäden vorne: ', num_front_val)
    print('Schäden hinten: ', num_rear_val)
    print('Schäden seitlich: ', num_side_val)
    print('Kleinere Schäden: ', num_minor_val)
    print('Moderate Schäden: ', num_moderate_val)
    print('Schwere Schäden: ', num_severe_val)

    train_image_generator = ImageDataGenerator(rescale=1. / 255)
    validation_image_generator = ImageDataGenerator(rescale=1. / 255)

    batch_size = 128
    epochs = 15

    # Trainingsdaten
    train_cars_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                                    directory=cars_training_dir,
                                                                    class_mode='binary')
    train_position_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                                        directory=position_training_dir,
                                                                        class_mode='binary')
    train_severity_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                                        directory=severity_training_dir,
                                                                        class_mode='binary')

    # Validationsdaten
    validation_cars_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                                              directory=cars_validation_dir,
                                                                              class_mode='binary')
    validation_position_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                                                  directory=position_validation_dir,
                                                                                  class_mode='binary')
    validation_severity_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                                                  directory=severity_validation_dir,
                                                                                  class_mode='binary')

    sample_cars_valaining_images, _ = next(train_cars_data_gen)
    sample_position_valaining_images, _ = next(train_position_data_gen)
    sample_severity_valaining_images, _ = next(train_position_data_gen)

    plotImages(sample_cars_valaining_images[:100])
    plotImages(sample_position_valaining_images[:100])
    plotImages(sample_severity_valaining_images[:100])

    model = Sequential([Conv2D(16, 3, padding='same', activation='relu'), MaxPooling2D(),
                        Conv2D(32, 3, padding='same', activation='relu'),
                        MaxPooling2D(), Conv2D(64, 3, padding='same', activation='relu'), MaxPooling2D(), Flatten(),
                        Dense(512, activation='relu'),
                        Dense(1)])

    model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

    # model.fit_generator(train_cars_data_gen, steps_per_epoch=num_undamaged_cars_train + num_undamaged_cars_train,
    #                     epochs=epochs, validation_data=validation_cars_data_gen,
    #                     validation_steps=num_undamaged_cars_val + num_undamaged_cars_val)
    #
    # model.fit_generator(train_position_data_gen, steps_per_epoch=num_front_train + num_rear_train + num_side_train,
    #                     epochs=epochs,
    #                     validation_data=validation_position_data_gen,
    #                     validation_steps=num_front_train + num_rear_val + num_side_val + num_undamaged_cars_val)
    #
    # model.fit_generator(train_severity_data_gen,
    #                     steps_per_epoch=num_minor_train + num_moderate_train + num_severe_train,
    #                     epochs=epochs,
    #                     validation_data=validation_severity_data_gen,
    #                     validation_steps=num_minor_val + num_moderate_val + num_severe_val)

    print(num_undamaged_cars_train + num_damaged_cars_train)

    model.fit_generator(train_cars_data_gen,
                        steps_per_epoch=ceil((num_undamaged_cars_train + num_damaged_cars_train) / batch_size),
                        epochs=epochs, validation_data=validation_cars_data_gen,
                        validation_steps=num_undamaged_cars_val + num_undamaged_cars_val)

    model.fit_generator(train_position_data_gen,
                        steps_per_epoch=ceil((num_front_train + num_rear_train + num_side_train) / batch_size),
                        epochs=epochs,
                        validation_data=validation_position_data_gen,
                        validation_steps=num_front_val + num_rear_val + num_side_val)

    model.fit_generator(train_severity_data_gen,
                        steps_per_epoch=ceil((num_minor_train + num_moderate_train + num_severe_train) / batch_size),
                        epochs=epochs,
                        validation_data=validation_severity_data_gen,
                        validation_steps=num_minor_val + num_moderate_val + num_severe_val)

    return model


def save_model(model):
    model.save('/home/simon/Schreibtisch/damaged_cars_model')


def main():
    model = init_model()
    save_model(model)


main()

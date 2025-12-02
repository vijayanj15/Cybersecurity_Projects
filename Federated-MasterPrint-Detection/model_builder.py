import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import config

def build_model():
    # Loads MobileNetV2 (Pre-trained on ImageNet)
    base_model = MobileNetV2(
        weights='imagenet', 
        include_top=False, 
        input_shape=(config.IMG_HEIGHT, config.IMG_WIDTH, config.CHANNELS)
    )
    
    # Freeze base layers to keep pre-learned features
    base_model.trainable = False

    # Add Custom Classification Head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    
    # Output: 2 Neurons [0=Genuine, 1=Attack]
    predictions = Dense(2, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=Adam(learning_rate=0.001), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    
    return model
import argparse
import os
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train an animal disease classifier and save a TensorFlow model."
    )
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Path to the dataset root containing class subdirectories.",
    )
    parser.add_argument(
        "--output",
        default="model/animal_disease_model.keras",
        help="Path to save the trained model file.",
    )
    parser.add_argument(
        "--image-size",
        type=int,
        default=224,
        help="Image height/width used for training.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Training batch size.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=8,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--validation-split",
        type=float,
        default=0.2,
        help="Validation split fraction from the dataset.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=123,
        help="Random seed for reproducible dataset splits.",
    )
    return parser.parse_args()


DISEASE_LABELS = [
    "Eye Infection",
    "Fungal Infection",
    "Mange in Dog",
    "Parvovirus in Dog",
    "Scabies in Cat",
    "Skin Allergy",
    "foot-and-mouth",
    "healthy",
    "lumpy",
]


def build_model(num_classes: int, image_size: int):
    import tensorflow as tf

    inputs = tf.keras.layers.Input(shape=(image_size, image_size, 3))
    x = tf.keras.applications.efficientnet.preprocess_input(inputs)
    base_model = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_tensor=x,
        pooling="avg",
    )
    base_model.trainable = False

    x = base_model.output
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(256, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model


def prepare_datasets(data_dir: Path, image_size: int, batch_size: int, validation_split: float, seed: int):
    import tensorflow as tf

    missing = [label for label in DISEASE_LABELS if not (data_dir / label).exists()]
    if missing:
        raise FileNotFoundError(
            f"Dataset folder is missing the following class directories: {missing}."
            "\nCreate all class folders under the dataset root using the labels exactly as listed."
        )

    train_ds = tf.keras.utils.image_dataset_from_directory(
        str(data_dir),
        labels="inferred",
        label_mode="int",
        class_names=DISEASE_LABELS,
        validation_split=validation_split,
        subset="training",
        seed=seed,
        image_size=(image_size, image_size),
        batch_size=batch_size,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        str(data_dir),
        labels="inferred",
        label_mode="int",
        class_names=DISEASE_LABELS,
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=(image_size, image_size),
        batch_size=batch_size,
    )

    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.08),
            tf.keras.layers.RandomContrast(0.08),
        ]
    )

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = (
        train_ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE)
        .shuffle(1024)
        .prefetch(AUTOTUNE)
    )
    val_ds = val_ds.prefetch(AUTOTUNE)

    return train_ds, val_ds


def main():
    args = parse_args()
    data_dir = Path(args.data_dir).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not data_dir.exists():
        raise FileNotFoundError(f"Dataset path not found: {data_dir}")

    print("Training data directory:", data_dir)
    print("Saving trained model to:", output_path)

    try:
        import tensorflow as tf
    except ImportError as exc:
        raise ImportError(
            "TensorFlow is required to train the model. Install it with `pip install tensorflow`."
        ) from exc

    train_ds, val_ds = prepare_datasets(
        data_dir,
        args.image_size,
        args.batch_size,
        args.validation_split,
        args.seed,
    )

    model = build_model(len(DISEASE_LABELS), args.image_size)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(output_path),
            monitor="val_accuracy",
            save_best_only=True,
            save_weights_only=False,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=3,
            restore_best_weights=True,
            verbose=1,
        ),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(output_path))

    print("Training complete. Model saved to:", output_path)
    print("Use the API again after restarting the server.")


if __name__ == "__main__":
    main()

from tensorflow.keras import callbacks
from display import display
from hyperparameters import WEIGHT_PATH

def model_checkpoint_callback():
    return callbacks.ModelCheckpoint(
        filepath=WEIGHT_PATH,
        save_weights_only=True,
        save_freq="epoch",
        verbose=0,
    )

def tensorboard_callback():
    return callbacks.TensorBoard(log_dir="./logs")


class ImageGenerator(callbacks.Callback):
    def __init__(self, num_img):
        self.num_img = num_img

    def on_epoch_end(self, epoch, logs=None):
        generated_images = self.model.generate(
            num_images=self.num_img,
            diffusion_steps=PLOT_DIFFUSION_STEPS,
        ).numpy()
        display(
            generated_images,
            save_to="./output/generated_img_%03d.png" % (epoch),
        )


def image_generator_callback():
    return ImageGenerator(num_img=10)
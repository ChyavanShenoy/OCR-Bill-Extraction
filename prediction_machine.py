from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import matplotlib.pyplot as plt
import os

os.environ["USE_TORCH"] = "1"


model = ocr_predictor(pretrained=True)


def predict(image):
    doc = DocumentFile.from_images(image)
    pred = model(doc)
    synth_image = synthesize_image(pred)
    print(synth_image)
    return pred, synth_image


def synthesize_image(image):
    synth_image = image.synthesize()
    plt.ioff
    plt.figure(dpi=600)
    plt.imshow(synth_image[0])
    plt.axis('off')
    plt.savefig('synth_image.jpg', bbox_inches='tight', pad_inches=0)
    return synth_image

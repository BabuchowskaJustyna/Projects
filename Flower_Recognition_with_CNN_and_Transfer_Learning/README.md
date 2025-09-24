# Flower Recognition (TensorFlow + ResNet50 + Gradio)

This project classifies images of five flower categories: dandelion, daisy, tulips, sunflowers, roses.
Training and comparison of models (a CNN from scratch and transfer learning with ResNet50) are contained in the notebook `Flower_Recognition_with_CNN_and_Transfer_Learning.ipynb`.

## Requirements
- Python 3.9–3.11
- Packages:
  - tensorflow
  - tensorflow-datasets
  - gradio
  - pillow
  - matplotlib
  - numpy

Quick install:
```bash
pip install -r requirements.txt
```
If you do not use `requirements.txt`, install manually:
```bash
pip install tensorflow tensorflow-datasets gradio pillow matplotlib numpy
```

## Run the demo (Gradio)
1. Make sure the model file `best_model.keras` is present in the project directory (it is saved by the ResNet50 training section in the notebook).
2. Open `Flower_Recognition_with_CNN_and_Transfer_Learning.ipynb` and run the last cell titled "Deployment with Gradio".
3. Gradio will start locally. In hosted environments (e.g., Colab)

The model is loaded with:
```python
from tensorflow import keras
from tensorflow.keras.applications.resnet50 import preprocess_input
model = keras.models.load_model('best_model.keras', compile=False, custom_objects={'preprocess_input': preprocess_input})
```
This ensures safe loading of the saved model that contains a `Lambda(preprocess_input)` layer.

## Data
- Dataset: `tf_flowers` from `tensorflow_datasets` (5 classes)
- Split: ~80/10/10 (train/val/test)
- Image size: 224×224


# Background Removal API Python Integration

Python wrapper for the BEN API that removes backgrounds from images.

## Installation

```bash
git clone https://github.com/PramaLLC/api-python-integration
cd api-python-integration
pip install -r requirements.txt
```

## Generate api token 
You must have a business subscription that can be found at https://backgrounderase.net/pricing. To generate the token navigate to
https://backgrounderase.net/account and scroll to the bottom of the page.

## Example
create example.py
```python
from PIL import Image
from main import predict_image # import predict image function from repo

image = Image.open("image.jpg") # your image file path or pil image object


mask, foregorund = predict_image(image,"your_ben_api_token")


mask.save("mask.png")
foregorund.save("foreground.png")

```


## API documentation
For full API documentation visit: https://backgrounderase.net/api-docs

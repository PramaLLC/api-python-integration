import requests
import base64
from PIL import Image
import io
import numpy as np
import torch 
import torch.nn.functional as F
from torchvision import transforms 




def post_process(result: torch.Tensor, im_size: list) -> np.ndarray:
    result = torch.squeeze(F.interpolate(result, size=im_size, mode='bilinear'), 0)
    ma = torch.max(result)
    mi = torch.min(result)
    result = (result - mi) / (ma - mi)
    im_array = (result * 255).permute(1, 2, 0).cpu().data.numpy().astype(np.uint8)
    im_array = np.squeeze(im_array)
    return im_array




def predict_image(image, api_key, api_url="https://api.backgrounderase.net/v2"):
    buffer = io.BytesIO()
    image_resized = image.resize((1024, 1024), Image.BILINEAR)
    image_resized.save(buffer, format='JPEG', quality=85, optimize=True)
    image_bytes = buffer.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        "image": image_base64
    }
    response = requests.post(
        api_url, 
        headers=headers, 
        json=payload 
    )
    if response.status_code == 200:
        try:
            result = response.json()
            mask_bytes = base64.b64decode(result['mask'])
            
            mask_img = Image.open(io.BytesIO(mask_bytes))
            
            mask_array = np.array(mask_img)

            mask_tensor = torch.from_numpy(mask_array).float().div(255.0)

            mask_tensor = mask_tensor.unsqueeze(0).unsqueeze(0) 
            
            alpha = post_process(mask_tensor,image.size)



            pred_pil = transforms.ToPILImage()(alpha)
            mask = pred_pil.resize(image.size)
            image.putalpha(mask)

            mask = Image.fromarray(alpha)



            return mask, image 
        except Exception as e:
            print(f"Error processing response: {e}")
            return None
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.content)
        return None





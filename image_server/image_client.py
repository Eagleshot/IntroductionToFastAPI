import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8002/image"

resp = requests.get(API_URL, stream=True)
print(resp.status_code)
image = np.asarray(bytearray(resp.raw.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image)
plt.axis('off')
plt.show()

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor_path = "INSERT_PATH"
model_path = "INSERT_PATH"

processor = BlipProcessor.from_pretrained(processor_path)
model = BlipForConditionalGeneration.from_pretrained().to("cuda")

raw_image = Image.open('F:\Python\\codsoft\\image_captioning\\testingimg.jpg').convert('RGB')

text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt").to("cuda")

out = model.generate(**inputs)
inputs = processor(raw_image, return_tensors="pt").to("cuda")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

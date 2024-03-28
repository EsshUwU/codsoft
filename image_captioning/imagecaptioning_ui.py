import gradio as gr
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor_dir = "INSERT_PATH" 
model_dir = "INSERT_PATH"

processor = BlipProcessor.from_pretrained(processor_dir)
model = BlipForConditionalGeneration.from_pretrained(model_dir).to("cuda")

def generate_caption(image):
    raw_image = Image.fromarray(image.astype('uint8'), 'RGB')
    inputs = processor(raw_image, return_tensors="pt").to("cuda")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


iface = gr.Interface(
    fn=generate_caption,
    inputs=[
        gr.Image(type="numpy", label="Upload an image")
    ],
    outputs=gr.Textbox(label="Generated Caption"),
    allow_flagging="never",
    title = "Image Captioning",
    description = "Upload an image and get the generated caption."
)

iface.launch()


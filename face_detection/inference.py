import PIL.Image as Image
import gradio as gr
import cv2
from ultralytics import ASSETS, YOLO
import os

ModelPath = "face_detect_model.pt"
VideoOutputFolder = "output_videos_path" #create output path and enter here

if __name__ == '__main__':
    model = YOLO(ModelPath)  # load a pretrained model
    model.model.names = {0: 'Male', 1: 'Female'}

def predict_image(img, conf_threshold):
    img_pil = img.convert('RGB')

    results = model.predict(
        source=img_pil,
        conf=conf_threshold,
        iou=0.45,
        show_labels=True,
        show_conf=False,
    )
    for r in results:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])

    return im


iface_image = gr.Interface(
    fn=predict_image,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold"),
    ],
    outputs=gr.Image(type="pil", label="Result"),
    description="Upload image for inference.",
    allow_flagging="never"
)


def detect_vid(input_vid, conf_threshold):
    model = YOLO(ModelPath)

    input_vid = input_vid.name
    results = model.track(source=input_vid, conf=conf_threshold, iou=0.5, save=True, project=VideoOutputFolder)
    print("done")

    filename = os.path.splitext(os.path.basename(input_vid))[0]
    output_folder = VideoOutputFolder
    folnum = str(len([name for name in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, name))]))
    temp_output_video_path = os.path.join(output_folder, f"track{folnum}", f"{filename}.avi")
    output_video_path = temp_output_video_path.replace(".avi", ".mp4")
    os.rename(temp_output_video_path, output_video_path)

    return output_video_path  


#gradio interface 
iface_video = gr.Interface(
    fn=detect_vid,
    inputs=[
        gr.File(label="Input Video"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold"),
    ],
    outputs=gr.Video(label="Output Video", type="mp4"),
    description="Upload video for inference.",
    allow_flagging="never"
)


iface = gr.TabbedInterface([iface_image, iface_video], ["Image Inference", "Video Inference"])

if __name__ == '__main__':
    iface.launch()
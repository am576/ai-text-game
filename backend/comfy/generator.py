import json
import urllib.request as request
import random
import string
import shutil
import os
import time
from PIL import Image
import io
class Generator:
    latest_prompt = ""
    latest_seed = 0
    def generateAdventurePreview(self, prompt):
        workflow = self.loadWorkflow("turbo")
        workflow["33"]["inputs"]["text_a"] = prompt
        prefix = self.random_prefix(32)
        seed = self.random_seed()
        workflow["37"]["inputs"]["filename_prefix"] = prefix 
        workflow["13"]["inputs"]["noise_seed"] = seed
        self.queue_prompt(workflow)
        preview_file = self.wait_for_file(prefix)
        if self.is_image_saved(preview_file):
            image = self.get_image(preview_file)
            os.remove(preview_file)
            self.latest_prompt = prompt
            self.latest_seed = seed
            
            return image
        
        return None

    def loadWorkflow(self, name):
        file_path = f"comfy/{name}_workflow.json"
        try:
            with open(file_path) as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Workflow '{name}' not found.")
        
    def queue_prompt(self, prompt):
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')
        req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
        request.urlopen(req)

    def random_prefix(self, length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))

        return random_string
    
    def random_seed(self):
        length = random.randint(1, 16)
        digits = [str(random.randint(0, 9)) for _ in range(length)]
        random_string = ''.join(digits)

        return random_string
    
    def find_file_by_prefix(self, prefix):
        for file_name in os.listdir('./comfyui/output'):
            if prefix in file_name:
                return file_name
        return None
    
    def wait_for_file(self, path):
        timeout = time.time() + 5
        while True:
            file_name = self.find_file_by_prefix(path)
            if file_name:
                return './comfyui/output/' + file_name
            if time.time() > timeout:
                raise FileNotFoundError(f"File '{path}' not found after waiting for 5 seconds.")
            time.sleep(0.1)

    def copy_file_to_frontend(self, file_path):
        file_path = os.path.join('./comfyui/output', file_path)
        destination_path = "../frontend/src/assets/previews/" + file_path.split("/")[-1]
        shutil.copy2(file_path, destination_path)
        
        return destination_path
    
    def get_image(self, file_name):
        pil_image = Image.open(file_name)
        img_byte_stream = io.BytesIO()
        pil_image.save(img_byte_stream, format='PNG')
        img_byte_stream.seek(0)

        return img_byte_stream
    
    def is_image_saved(self, image_path):
        initial_size = os.path.getsize(image_path)
        # Wait for the image to be saved for a certain period of time
        timeout = time.time() + 3
        while True:
            final_size = os.path.getsize(image_path)
            if final_size == initial_size:
                time.sleep(0.5)
                return True  # Image is saved successfully
            if time.time() > timeout:
                return False  # Image is still being saved or truncated
            time.sleep(0.1)
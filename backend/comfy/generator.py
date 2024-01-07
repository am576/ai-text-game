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
    prompt = ""
    seed = 0
    workflow = None
    world_preview_path = None
    avatar_preview_path = None

    def __init__(self):
        self.initWorkflow()

    def initWorkflow(self):
        self.workflow = self.loadWorkflow("turbo")

    def setGenerationParameters(self, prompt):
        self.prompt = prompt
        self.workflow["6"]["inputs"]["text"] = self.prompt
        self.prefix = self.random_prefix(32)
        self.seed = self.random_seed()
        self.workflow["27"]["inputs"]["filename_prefix"] = self.prefix 
        self.workflow["13"]["inputs"]["noise_seed"] = self.seed

    def generateWorldPreview(self, prompt):
        self.setGenerationParameters(prompt)
        self.queue_prompt(self.workflow)
        worldImage, self.world_preview_path = self.getSavedFile()

        return worldImage
    
    def generateAvatarPreview(self, prompt):
        self.setGenerationParameters(prompt)
        self.queue_prompt(self.workflow)
        avatarImage, self.avatar_preview_path = self.getSavedFile()
        
        return avatarImage

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

    def getSavedFile(self):
        preview_file_path = self.wait_for_file(self.prefix)
        if self.is_image_saved(preview_file_path):
            image = self.get_image(preview_file_path)
            os.remove(preview_file_path)
            
            return image, preview_file_path
        
        return None

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

    def get_image(self, file_name):
        pil_image = Image.open(file_name)
        img_byte_stream = io.BytesIO()
        pil_image.save(img_byte_stream, format='PNG')
        img_byte_stream.seek(0)

        return img_byte_stream
    
    def is_image_saved(self, image_path):
        initial_size = os.path.getsize(image_path)
        timeout = time.time() + 3
        while True:
            final_size = os.path.getsize(image_path)
            if final_size == initial_size:
                time.sleep(0.5)
                return True
            if time.time() > timeout:
                return False
            time.sleep(0.1)
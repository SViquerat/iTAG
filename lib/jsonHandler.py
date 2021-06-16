from base64 import b64encode, b64decode
from json import dumps
from io import BytesIO


class jsonHandler():
    def __init__(self):
        pass

    def encode(self,IMAGE_NAME, ENCODING = 'utf-8'):
        with open(IMAGE_NAME, 'rb') as open_file:
            byte_content = open_file.read()
        base64_bytes = b64encode(byte_content)
        base64_string = base64_bytes.decode(ENCODING)
        return base64_string

    def dict2JSON(self,dictionary):
        json_data = dumps(dictionary, indent=2)
        return json_data

    def save(self,json_data,json_file):
        with open(json_file, 'w') as outfile:
            outfile.write(json_data)

    def decode(self,base64_string):
        return BytesIO(b64decode(base64_string))
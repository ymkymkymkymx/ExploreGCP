import base64
import json
import os
from google.cloud import vision
credential_path = "D:/githubrepos/ExploreGCP/ymk.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

os.environ['GCP_PROJECT']="nifty-digit-285901"
project_id = os.environ['GCP_PROJECT']


import io
from PIL import Image, ImageDraw

client = vision.ImageAnnotatorClient()
def highlight_carplates(path, carplates, output_filename):
    
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for i in range( len(carplates)):
        if i+1<len(carplates) and ((len(carplates[i].description)==2 and len(carplates[i+1].description)==5)or(len(carplates[i].description)==1 and len(carplates[i+1].description)==6)):
            
            box = [(carplates[i].bounding_poly.vertices[0].x,carplates[i].bounding_poly.vertices[0].y),(carplates[i+1].bounding_poly.vertices[1].x,carplates[i+1].bounding_poly.vertices[1].y),(carplates[i+1].bounding_poly.vertices[2].x,carplates[i+1].bounding_poly.vertices[2].y),(carplates[i].bounding_poly.vertices[3].x,carplates[i].bounding_poly.vertices[3].y)]
            draw.line(box + [box[0]], width=3, fill='#00ff00')
        
    im.save(output_filename)
path="D:\githubrepos\ExploreGCP\images\car4.jpeg"
output_filename="D:\githubrepos\ExploreGCP\images\car4circled.jpg"
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    print('\n"{}"'.format(text.description))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))

highlight_carplates(path, texts, output_filename)

if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))
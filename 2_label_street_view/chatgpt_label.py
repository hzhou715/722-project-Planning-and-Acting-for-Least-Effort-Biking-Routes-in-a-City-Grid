import base64
import os
from openai import OpenAI

#client = OpenAI()
client = OpenAI(api_key='xxx')
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "_BES4jCFzFuAzXdEK-nq9w_fov90_90.jpg"
filename    = os.path.basename(image_path)
image_id, _ = os.path.splitext(filename)
print(image_id)

# Getting the Base64 string
base64_image = encode_image(image_path)

labelgsv_user_prompt = '''
Your goal is to label the streetscape image based on the rubric. You will be provided with an image in the US, and you will output a json object containing the following information:

{
    ID: {image_id},
    road pavement condition: string // label it poor/fair/good based on the rubric,
    presence of sidewalk: string // yes/no,
    sidewalk condition: string // label it poor/fair/good based on the rubric,
    presence of sidewalk buffer zone: string // yes/no,
    crosswalk presence: string // yes/no,
    traffic signs: string // yes/no,
    streetlight presence: string // yes/no
}

The rubric is: road pavement condition (Poor: Large potholes or patches, deep cracks, uneven surfaces, under construction,
 and driving conditions are very uncomfortable, potentially impassable, and unsafe. 
Fair: Several areas of distress, with more than one form of cracking, rutting, in need of maintenance repair, 
and driving conditions are somewhat uncomfortable, with vibrations and slight leaning in curvature. 
Good: Small areas of cracks, potholes, bleeding, etc., minor surface vibration, but driving conditions are generally 
smooth and comfortable), sidewalk condition (Poor: Large crack, uneven surfaces, missing 
sections, too narrow, or under construction, and hazardous conditions for pedestrians, potentially leading to trips and 
falls, and Surface is very uncomfortable to walk on, with significant obstructions or debris. Fair: Several areas of 
distress, or minor obstructions, narrow, and surface requires maintenance but is passable,
 and walking conditions are somewhat uncomfortable, with noticeable vibrations. Good: Minor cracks, smooth surface, and 
 well-maintained, and surface is comfortable for walking, with minimal obstructions, and walking conditions are generally 
 smooth and safe), Sidewalk buffer zone (yes: show Physical barriers between the sidewalk and roadway (such as street trees,
  landscaping, bike lanes and parked cars), no).
'''

response = client.responses.create(
    model="gpt-4.1",
    #temperature=0.1,
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": labelgsv_user_prompt

                  },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high",
                },
            ],
        }
    ],
)

print(response.output_text)

raw = response.output_text
data = json.loads(raw)

# override the ID field
data["ID"] = [image_id]

# print the corrected JSON
print(json.dumps(data, indent=2))

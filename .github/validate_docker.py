import docker, sys
import json, jsonschema

def validate_image_labels(image_name,schema): #, expected_labels):
  """
  This function checks if a Docker image has the specified structure.

  Args:
      image_name: Name of the Docker image to inspect.
      schema: Schema to validate against.

  Returns:
      True if the image attributes match the json schema, False otherwise.
  """
  client = docker.from_env()
  try:
    image = client.images.get(image_name)
  except docker.errors.ImageNotFound:
    print(f"Error: Image '{image_name}' not found.")
    return False

  jsonschema.validators.validate(instance=image.attrs,schema=schema)

if __name__ == "__main__":
  image_name = sys.argv[1]
  with open(sys.argv[2]) as fh:
    schema = json.load(fh)
  validate_image_labels(image_name,schema)
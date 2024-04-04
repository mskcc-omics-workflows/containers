import docker, sys
import json, jsonschema
import re

def validate_image_labels(image_name,schema,required_annot): #, expected_labels):
  """
  This function checks if a Docker image has the specified structure.

  Args:
      image_name: Name of the Docker image to inspect.
      schema: Schema to validate against.

  Returns:
      True if the image attributes match the json schema, False otherwise.
  """
  client = docker.from_env()
  # if fail, raises docker.errors.ImageNotFound
  image = client.images.get(image_name)
  #try:
  #  image = client.images.get(image_name)
  #except docker.errors.ImageNotFound:
  #  print(f"Error: Image '{image_name}' not found.")
  #  return False

  jsonschema.validators.validate(instance=image.attrs,schema=schema)

  #print(json.dumps(image.attrs["Config"]["Labels"], indent=4))
  missing_label = []
  for i in required_annot:
    if not any([re.search(i,j) for j in image.attrs["Config"]["Labels"]]):
      missing_label += [i]

  if len(missing_label) > 0:
    print(f"Missing labels in image:\n{"\n".join(missing_label)}")
    raise Exception("Failed due to missing labels")

#jsonschema doesn't seem like it can easily require patterned properties
required_annot = [
  r"^org\.opencontainers\.image\.url(\..+)?",
  r"^org\.opencontainers\.image\.created(\..+)?",
  r"^org\.opencontainers\.image\.authors(\..+)?",
  r"^org\.opencontainers\.image\.source(\..+)?",
  r"^org\.opencontainers\.image\.version(\..+)?",
  r"^org\.opencontainers\.image\.title(\..+)?",
  r"^org\.opencontainers\.image\.description(\..+)?"
]

if __name__ == "__main__":
  image_name = sys.argv[1]
  with open(sys.argv[2]) as fh:
    schema = json.load(fh)
  validate_image_labels(image_name,schema,required_annot)
# MLOPs
## Workflows
default workflows
1. Update config.yaml
2. Update params.yaml
3. update entity
4. update configuration manager     config.py
5. update components
6. update pipeline.py
7. update main.py
8. update dvc.yaml


python box for exception handling

from box import ConfigBox 
is used to convert and access the key value pairs in the yaml files as file.key insted of file["key"] -> used in read yaml

ensure annotations handles the erroro like 3*2 even when the data type for the x and y has been set. for eg: str inside int multiplication. 
ensure annotation decorators throws error in that case

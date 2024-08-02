import yaml
import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from scripts.MLOPs import logger
from scripts.MLOPs.entity.config_entity import DataSetConfig
from scripts.MLOPs.utils.common import read_yaml

class DataSetSorter:
    def __init__(self, yamlconfig: DataSetConfig):
        self.yamlconfig = yamlconfig

    def indices(self, base_set: list, new_set: list):
        base_set = [item.lower() for item in base_set]
        new_set = [item.lower() for item in new_set]
        new_indices =[]
        for item in new_set:
            indices = [i for i, x in enumerate(base_set) if x == item]
            new_indices.extend(indices)
        logger.info(f"index changes successfully into {new_indices}")
        return new_indices
        

    def filter_files(self, directory, classid_list):
        file_list = []
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory,filename)
                with open(file_path, 'r') as file:
                    content = file.readline().strip().split()
                    if content:
                        class_id = int(content[0])
                        if class_id in classid_list:
                            file_list.append(os.path.splitext(filename)[0])
        logger.info(f"file list has been updated")
        return file_list
    
    def copy_files(self, file_list, source, destination):
        for root, _, files in os.walk(source):
            for file in files:
                filebase, extension = os.path.splitext(file)
                if filebase in file_list:
                    source = os.path.join(root, file)
                    target = os.path.join(destination, file)

                    if not os.path.exists(os.path.dirname(target)):
                        os.makedirs(os.path.dirname(target))

                    shutil.copy2(source, target)
                    logger.info(f"copied {source} to {target}")
    
    def move_files(self, file_list, source, destination):
        for root, _, files in os.walk(source):
            for file in files:
                filebase, extension = os.path.splitext(file)
                if filebase in file_list:
                    source = os.path.join(root, file)
                    target = os.path.join(destination, file)

                    if not os.path.exists(os.path.dirname(target)):
                        os.makedirs(os.path.dirname(target))

                    shutil.move(source, target)
                    logger.info(f"copied {source} to {target}")

    def update_id(self, line, old_to_newid):
        parts = line.strip().split()
        if parts:
            original_id = int(parts[0])
            if original_id in old_to_newid:
                parts[0] = str(old_to_newid[original_id])
        return ' '.join(parts) + '\n'

    def subsetandcopy(self,filelist, source_dir,destination_dir,type,train_ratio:float = 0.7, valid_ratio:float = 0.2):
        ###type can be image or label
        train_files, test_files = train_test_split(filelist, test_size=1-train_ratio, random_state=42)
        valid_ratio_adj = valid_ratio/(1-train_ratio)
        train_files, valid_files = train_test_split(train_files, test_size=valid_ratio_adj, random_state=42)

        self.move_files(train_files,source_dir,os.path.join(destination_dir,"train",type))
        self.move_files(valid_files,source_dir,os.path.join(destination_dir,"valid",type))
        self.move_files(test_files,source_dir,os.path.join(destination_dir,"test",type))
        logger.info(f'files has been subset into train valid and test sets')

    def create_yaml(self, dir_path: str, class_name: list, op_file: str):
        data = {
            'path': dir_path,
            'train': "train/images",
            'val': "valid/images",
            'test': "test/images",
            'nc': len(class_name),
            'names': class_name
        }
        with open (op_file, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        
    def create_dataset(self):
        #rread the base yaml
        yaml_path = Path(f"{self.yamlconfig.base_Data_path}/data.yaml")
        print(yaml_path)
        base_yaml = read_yaml(yaml_path)
        new_dir = os.path.join(self.yamlconfig.new_data_path,self.yamlconfig.dataset_name)
        os.makedirs(new_dir, exist_ok=True)
        
        #create folder structure
        for folder in ['train','valid','test']:
            subdir = os.path.join(new_dir, folder)
            os.makedirs(os.path.join(subdir, 'images'), exist_ok=True)
            os.makedirs(os.path.join(subdir, 'labels'), exist_ok=True)
        logger.info("folder structure for the new dataset has been created")

        #set the classes to filter
        desired_classes = self.yamlconfig.classes
        logger.info(f"desired classes are: {desired_classes}")

        base_class = base_yaml.names
        logger.info(f"initial classes are: {base_class}")
        #finding index
        new_indx_wrt_base = self.indices(base_class,desired_classes)
        #filtering train files wrt to index
        filtered_train_filelist = self.filter_files(os.path.join(self.yamlconfig.base_Data_path,"train","labels"),new_indx_wrt_base)
        #filtering valid files wrt to index
        filtered_valid_filelist = self.filter_files(os.path.join(self.yamlconfig.base_Data_path,"valid","labels"),new_indx_wrt_base)
        #filtering test files wrt to index
        filtered_test_filelist = self.filter_files(os.path.join(self.yamlconfig.base_Data_path,"test","labels"),new_indx_wrt_base)
        filtered_filelist = filtered_train_filelist + filtered_valid_filelist + filtered_test_filelist
        #copy the images into train and labels into valid
        self.copy_files(filtered_train_filelist,os.path.join(self.yamlconfig.base_Data_path,"train","images"),os.path.join(new_dir,"train"))
        self.copy_files(filtered_train_filelist,os.path.join(self.yamlconfig.base_Data_path,"train","labels"),os.path.join(new_dir,"valid"))
        self.copy_files(filtered_valid_filelist,os.path.join(self.yamlconfig.base_Data_path,"valid","images"),os.path.join(new_dir,"train"))
        self.copy_files(filtered_valid_filelist,os.path.join(self.yamlconfig.base_Data_path,"valid","labels"),os.path.join(new_dir,"valid"))
        self.copy_files(filtered_test_filelist,os.path.join(self.yamlconfig.base_Data_path,"test","images"),os.path.join(new_dir,"train"))
        self.copy_files(filtered_test_filelist,os.path.join(self.yamlconfig.base_Data_path,"test","labels"),os.path.join(new_dir,"valid"))

        mapped_ids = {class_id: index for index, class_id in enumerate(new_indx_wrt_base)}
        logger.info(f"old to new class map successfull: {mapped_ids}")

        for filename in os.listdir(os.path.join(new_dir,"valid")):
            if filename.endswith('.txt'):
                filepath = os.path.join(new_dir,"valid",filename)

                with open(filepath,'r') as file:
                    lines = file.readlines()
                
                #update the class id
                updated = [self.update_id(line,mapped_ids) for line in lines]

                with open(filepath, 'w') as file:
                    file.writelines(updated)

        self.subsetandcopy(filtered_filelist, os.path.join(new_dir,"train"),new_dir,"images")
        self.subsetandcopy(filtered_filelist, os.path.join(new_dir,"valid"),new_dir,"labels")

        desired_classes = list(desired_classes)

        self.create_yaml(dir_path=new_dir,
                         class_name=desired_classes,
                         op_file=os.path.join(new_dir,"data.yaml"))

        return new_dir
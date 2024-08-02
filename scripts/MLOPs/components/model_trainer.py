from ultralytics import YOLO, settings
import os,sys
import logging
import torch
import mlflow
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.config.configuration import DataValidationConfig,TrainLogConfig,Params


class ModelTrainer:
    def __init__(self, config: TrainLogConfig, val: DataValidationConfig, param: Params):
        self.config = config
        self.val = val
        self.param = param

    def validation_status(self):
        with open(self.val.status_file_dir, 'r') as file:
            status = file.read().strip()
        key, value = status.split(':')
        key = key.strip()
        value = value.strip().lower()

        if key != "validation_status":
            raise ValueError("unexpected key in status file")
        
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            raise ValueError("validation status is invalid")

    def train_model(self):

        dataset_dir = self.val.current_dset
        data_path = os.path.join( dataset_dir, "data.yaml")
        logging.info(f"Dataset location: {data_path}")
        if torch.cuda.is_available():
            device = torch.cuda.current_device()
            logging.info(f"Device is running on: {torch.cuda.get_device_name(device)}")
        else:
            logging.info(f"CUDA is not available")
            device = "cpu"
            logging.info(f"Device to run on: {device}")
            logging.info(data_path)

        model = self.config.model

        os.makedirs(self.config.save_path, exist_ok=True)
        save_path = os.path.join(self.config.save_path,"Trainedv8.pt")
        # Load a pretrained YOLOv8n model
        model = YOLO(model)
        # Train the model
        model.train(
            data=data_path,
            optimizer = self.param.optimizer,
            lr0 = self.param.lr0,
            save_period = self.param.save_period,
            batch = self.param.batch,
            epochs = self.param.epochs,
            resume = self.param.resume,
            seed = self.param.seed,
            imgsz = self.param.imgsz
            )
        model.save(save_path)
        return model
    
    def log_into_mlflow(self):

        settings.update({'mlflow': True})
        run_name = self.config.model_name
        experiment_name = self.config.experiment_name
        os.environ["MLFLOW_TRACKING_URI"] = self.config.mlflow_uri
        os.environ["MLFLOW_RUN"] = run_name
        
        print("MLFLOW_TRACKING_URI: ", os.environ.get("MLFLOW_TRACKING_URI"))
        
        # settings.update({'datasets_dir': "X:\DL\Projects\MLOPs"})
        mlflow.autolog(log_models=True)
        mlflow.set_experiment(experiment_name=experiment_name)
        
        with mlflow.start_run(run_name=run_name) as run: 
            #run_name is the name of the task.
            run_id = run.info.run_id 
            #run_id is the directory name that will be stored within the MLFLOW_TRACKING_URI path.
            print(run_id)
            self.train_model()
            save_path = os.path.join(self.config.save_path,"Trainedv8.pt")
            model = YOLO(save_path)
            yolonnx = model.export(format="onnx", dynamic= True)
            mlflow.onnx.log_model(yolonnx, "YOLOv8n")             ##logged model
        mlflow.end_run()
            

    def run_pipeline(self):
        if (self.validation_status() == True):
            try:
                self.log_into_mlflow()
            except Exception as e:
                raise AppException(e, sys)
        else:
            logging.INFO(f"Model training not run due to invalid dataset. \n please ingest a valid dataset")

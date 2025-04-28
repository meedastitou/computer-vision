import yaml
from src.logger import setup_logger
logger = setup_logger()

class YamlHandler:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self.yaml_data = self.read_yaml_file(self.yaml_path)

    def read_yaml_file(self, file_path):
        """Read a YAML file."""
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            logger.error(f"Error reading YAML file {file_path}: {e}")
            return None

    def save_yaml_file(self):
        """Save updated YAML data back to the file."""
        try:
            with open(self.yaml_path, 'w') as file:
                yaml.dump(self.yaml_data, file, default_flow_style=False)

        except Exception as e:
            logger.error(f"Error saving YAML file {self.yaml_path}: {e}")

    def mark_as_modified(self, dataset_name):
        """Mark a dataset as modified."""
        if dataset_name in self.yaml_data:
            self.yaml_data[dataset_name]["modified"] = 1
            self.save_yaml_file()
    
    # function for getting parameters 
    # train_folder , test_folder, val_folder
    def get_path_folders(self, dataset_info):

        # get the parameters sinon if it's not exist set None
        base_folder = dataset_info.get("folder", "") if "folder" in dataset_info else None
        train_folder = dataset_info.get("train", "") if "train" in dataset_info else None
        test_folder = dataset_info.get("test", "") if "test" in dataset_info else None
        vall_folder = dataset_info.get("val", "") if "val" in dataset_info else None

        return base_folder, train_folder, test_folder, vall_folder

    def get_output_data_ingestion(self):
        return self.yaml_data.get("artifacts", {}).get("data_ingestion", {}) 
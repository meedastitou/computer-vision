import os
from rich.progress import track
from src.logger import setup_logger
from src.components.yaml_handler import YamlHandler
from dataclasses import dataclass
logger = setup_logger()


class DatasetProcessor:
    def __init__(self, base_folder, train_folder, test_folder, vall_folder, changes):
        self.labels_folder = {}
        self.labels_folder['train_folder'] = os.path.join(base_folder, train_folder, "labels") if train_folder is not None else None
        self.labels_folder['test_folder'] = os.path.join(base_folder, test_folder, "labels") if test_folder is not None else None
        self.labels_folder['val_folder'] = os.path.join(base_folder, vall_folder, "labels") if vall_folder is not None else None

        self.changes = changes

    def process_labels(self):
        """Modify class IDs in all label files."""
        
        for folder_name, folder in self.labels_folder.items():

            logger.info(f"processing : {folder_name}")

            if (folder is None) or (not os.path.exists(folder)):
                logger.warning(f"Labels folder does not exist: {folder_name}")
                continue

            # get all files
            files = os.listdir(folder)
            for file in track(files, description=f"processing folder {folder_name}"):
                file_path = os.path.join(folder, file)
                
                try:
                    lines = self.read_lines(file_path)
                    modified_lines = []

                    for line in lines:
                        parts = line.strip().split()
                        if parts:  # Ensure the line is not empty

                            class_id = int(parts[0])
                            if class_id in self.changes:
                                parts[0] = str(self.changes[class_id])  # Replace class ID

                                modified_lines.append(" ".join(parts))

                    # Write the modified lines back to the file
                    with open(file_path, 'w') as f:
                        f.write("\n".join(modified_lines))
                    
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
                
            logger.success(f"process {folder_name} is Done")    
            
    def read_lines(self, file_path):
        """Read lines from a file."""
        try:
            with open(file_path, 'r') as f:
                return f.readlines()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return []


class DataIngestion:

    def main_DataIngestion(self):
        # Load YAML configuration
        yaml_handler = YamlHandler("source.yaml")

        # Process each dataset
        for dataset_name, dataset_info in yaml_handler.yaml_data.items():
            if dataset_info.get("modified", 0) == 0:  # Process only unmodified datasets
                logger.info(f"Processing dataset: {dataset_name}")

                base_folder, train_folder, test_folder, vall_folder = yaml_handler.get_path_folders(dataset_info)
                
                changes = dataset_info.get("conf", {}).get("changes", {})

                processor = DatasetProcessor(base_folder, train_folder, test_folder, vall_folder, changes)
                processor.process_labels()
                
                # Mark the dataset as modified
                yaml_handler.mark_as_modified(dataset_name)
                
            else:
                logger.info(f"Dataset {dataset_name} is already modified.")
                pass
            
        logger.success("All datasets processed successfully.")

        
# main function
if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.main_DataIngestion()

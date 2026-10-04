from deepeval.dataset import EvaluationDataset


def generate_datasets_from_json(file_path, input_key):
    dataset = EvaluationDataset()
    dataset.add_goldens_from_json_file(
        file_path=file_path,
        input_key_name=input_key
    )
    return dataset
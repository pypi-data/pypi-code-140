import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)


if True:
    from alphafed.auto_ml import from_pretrained
    from alphafed.auto_ml.cv.res_net import ResNetFamily
    from alphafed.examples.auto_ml.cv.res_net import (DATA_OWNER_3_ID,
                                                      DEV_TASK_ID)


if __name__ == '__main__':
    auto_model = from_pretrained(
        name=ResNetFamily.SKIN_LESION_DIAGNOSIS_FED_AVG,
        meta_data={
            "name": ResNetFamily.SKIN_LESION_DIAGNOSIS_FED_AVG,
            "input_meta": {
                "image_size": [
                    224,
                    224
                ]
            },
            "model_file": "res_net.py",
            "module_dir": None,
            "param_file": "resnet18.pth",
            "model_class": "ResNet18",
            "epochs": 20,
            "batch_size": 32,
            "lr": 1e-4
        },
        resource_dir=os.path.join(CURRENT_DIR, 'res'),
        dataset_dir=os.path.join(CURRENT_DIR, 'data'),
    )
    auto_model.fine_tune(id=DATA_OWNER_3_ID,
                         task_id=DEV_TASK_ID,
                         is_debug_script=True)

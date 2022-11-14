import os
import pickle
import numpy as np
import scipy.io
import json
import pandas as pd
from typing import Union
from kgcnn.data.qm import QMDataset
from kgcnn.data.download import DownloadDataset


class QM9MolNetDataset(QMDataset, DownloadDataset):
    """Store and process QM9 dataset."""

    download_info = {
        "dataset_name": "QM9MolNet",
        "data_directory_name": "qm9_mol_net",
        "download_url": "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/gdb9.tar.gz",
        "download_file_name": 'gdb9.tar.gz',
        "unpack_tar": True,
        "unpack_zip": False,
        "unpack_directory_name": "gdb9"
    }

    def __init__(self, reload: bool = False, verbose: int = 1):
        """Initialize QM8 dataset.

        Args:
            reload (bool): Whether to reload the data and make new dataset. Default is False.
            verbose (int): Print progress or info for processing where 0=silent. Default is 1.
        """
        QMDataset.__init__(self, verbose=verbose, dataset_name="QM9MolNet")
        DownloadDataset.__init__(self, **self.download_info, reload=reload, verbose=verbose)

        self.label_names = [
            "A", "B", "C", "mu", "alpha", "homo", "lumo", "gap", "r2", "zpve", "u0", "u298", "h298", "g298",
            "cv", "u0_atom", "u298_atom", "h298_atom", "g298_atom"
        ]
        self.label_units = [
            "GHz", "GHz", "GHz", "D", r"a_0^3", "H", "H", "H", r"a_0^2", "H", "H", "H", "H", "H", r"cal/mol K",
            "kcal/mol", "kcal/mol", "kcal/mol", "kcal/mol"]
        self.dataset_name = "QM9MolNet"
        self.require_prepare_data = False
        self.fits_in_memory = True
        self.verbose = verbose
        self.data_directory = os.path.join(self.data_main_dir, self.data_directory_name, self.unpack_directory_name)
        self.file_name = "gdb9.csv"

        if not os.path.exists(self.file_path):
            original_name = os.path.join(self.data_directory, "gdb9.sdf.csv")
            if os.path.exists(original_name):
                os.rename(original_name, self.file_path)

        if self.require_prepare_data:
            self.prepare_data(overwrite=reload)

        if self.fits_in_memory:
            self.read_in_memory(label_column_name=self.label_names)

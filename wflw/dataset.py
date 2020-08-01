import os

import cv2
import numpy as np

from mark_dataset.dataset import MarkDataset
from mark_dataset.util import FileListGenerator


class WFLW(MarkDataset):
    """Please make sure the uncompressed files are in the same folder:
    .
    ├── WFLW_annotations
    └── WFLW_images
    """

    def populate_dataset(self, image_dir):
        """Populate the 300W dataset with essential data.

        Args:
            image_dir: the direcotry of the dataset images.
        """
        # As required by the abstract method, we need to override this function.

        # 1. Populate the mark file list. Note the order should be same with the
        # image file list. Since WFLW was not using single mark file, a virtual
        # mark file will be generated.

        # First, parse all the marks and store them in memory.
        self.dataset_root_folder = os.path.dirname(image_dir)
        mark_file_test = os.path.join(self.dataset_root_folder,
                                      "WFLW_annotations",
                                      "list_98pt_rect_attr_train_test",
                                      "list_98pt_rect_attr_test.txt")
        mark_file_train = os.path.join(self.dataset_root_folder,
                                       "WFLW_annotations",
                                       "list_98pt_rect_attr_train_test",
                                       "list_98pt_rect_attr_train.txt")

        self.image_files = []
        self.mark_group = []

        def _read_mark_file(mark_file):
            with open(mark_file) as fid:
                for line in fid:
                    raw_data = line.strip().split(sep=" ")
                    marks = np.array(raw_data[:98*2], np.float).reshape(-1, 2)
                    marks = np.pad(marks, (0, 1))
                    image_path = os.path.join(image_dir, raw_data[-1])
                    self.image_files.append(image_path)
                    self.mark_group.append(marks)

        _read_mark_file(mark_file_test)
        _read_mark_file(mark_file_train)

        # This is the virtual mark files. It is actually a int number.
        self.mark_files = range(len(self.image_files))

        # 3. Set the key marks indices. Here key marks are: left eye left corner,
        #  left eye right corner, right eye left corner, right eye right corner,
        #  mouse left corner, mouse right corner. For 300W the indices are 36,
        # 39, 42, 45, 48, 54. Most of the time you need to do this manually.
        # Refer to the mark dataset for details.
        self.key_marks_indices = [60, 64, 68, 72, 76, 82]

        # Even optional, it is highly recommended to update the meta data.
        self.meta.update({"authors": "Tsinghua National Laboratory",
                          "year": 2018,
                          "num_marks": 98,
                          "num_samples": len(self.image_files)
                          })

    def get_marks_from_file(self, mark_file):
        """This function should read the mark file and return the marks as a 
        numpy array in form of [[x, y, z], [x, y, z]].
        Be carefull we are using int numbers as virtual mark files"""
        return self.mark_group[mark_file]

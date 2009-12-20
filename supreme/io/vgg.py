"""Load a super-resolution dataset from Oxford's Vision and Geometry Group.

"""

__all__ = ['load_vgg']

import numpy as np

from _io import ImageCollection

import os
from glob import glob

def load_vgg(path):
    data_paths = ['pgm', 'fields']
    H_paths = ['H']

    data_paths = [os.path.join(path, p) for p in data_paths]
    data_paths = [p for p in data_paths if os.path.exists(p)]

    H_paths = [os.path.join(path, p) for p in H_paths]
    H_paths = [p for p in H_paths if os.path.exists(p)]

    if not len(data_paths) == len(H_paths) or \
       len(data_paths) == 0:
        raise ValueError('Cannot find VGG directory structure.')

    data_path = data_paths[0]
    H_path = H_paths[0]

    ic = ImageCollection(os.path.join(data_path, '*'), conserve_memory=False)

    H_sofar = np.eye(3)
    for i, img in enumerate(ic):
        if i == 0:
            img.info['H'] = np.eye(3)
        else:
            H_pat = os.path.join(H_path, '*%03d.%03d*.H' % (i - 1, i))
            H_file = glob(H_pat)[0]
            H = np.loadtxt(H_file)
            if not H.shape == (3, 3):
                raise RuntimeError("Invalid H-file found: %s" % H_file)

            H_sofar = np.dot(np.linalg.inv(H), H_sofar)
            img.info['H'] = H_sofar

    return ic
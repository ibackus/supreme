from supreme._build import CExtension
import os.path

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('ext', parent_package, top_path)

    c_files = [f for f in os.listdir(config.local_path) if f.endswith('.c')]
    config.ext_modules.append(CExtension('libsupreme_',
                                         c_files,
                                         path=config.local_path))

    return config

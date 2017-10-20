# Copyright 2017, Wenjia Bai. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
    This script demonstrates the segmentation of a test cardiac MR image using
    a pre-trained neural network.
    """
import os, urllib.request


if __name__ == '__main__':
    # Download exemplar short-axis images
    URL = 'https://www.doc.ic.ac.uk/~wbai/data/ukbb_cardiac/'
    print('Downloading images ...')
    for i in [1, 2]:
        if not os.path.exists('demo_image/{0}'.format(i)):
            os.makedirs('demo_image/{0}'.format(i))
            urllib.request.urlretrieve(URL + 'sa_{0}.nii.gz'.format(i),
                                       os.path.join('demo_image/{0}/sa.nii.gz'.format(i)))

    # Download the trained network
    print('Downloading the trained network ...')
    if not os.path.exists('trained_model'):
        os.makedirs('trained_model')
    for f in ['FCN_sa.meta', 'FCN_sa.index', 'FCN_sa.data-00000-of-00001']:
        urllib.request.urlretrieve(URL + f, os.path.join('trained_model', f))

    # Perform segmentation
    CUDA_VISIBLE_DEVICES = 5
    print('Performing segmentation ...')
    os.system('CUDA_VISIBLE_DEVICES={0} python3 deploy_network.py '
              '--testset_dir demo_image --dest_dir demo_image --model_path trained_model/FCN_sa '
              '--process_seq --clinical_measures'.format(CUDA_VISIBLE_DEVICES))
    print('Done.')
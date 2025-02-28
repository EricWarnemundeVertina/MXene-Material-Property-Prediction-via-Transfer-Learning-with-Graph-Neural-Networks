# MXene-Material-Property-Prediction-via-Transfer-Learning-with-Graph-Neural-Networks
GitHub repository corresponding to the paper: MXene Material Property Prediction via Transfer Learning with Graph Neural Networks




Create conda environment to run this code:
conda create --name env_name python=3.8
source activate env_name

Might need to install (the appropriate versions to get matching CUDA versions):
conda install dgl=2.1.0 pytorch torchvision torchaudio pytorch-cuda -c pytorch -c nvidia

conda install dgl=0.6.0 pytorch=1.7.1 torchvision=0.10.1 torchaudio=0.10.0 pytorch-cuda=10.1 -c pytorch -c nvidia
	(Check which versions to install and put them after each = sign, respectively)

Packages installed:
pip install numpy==1.19.5

pip install torch==1.8.0
	num-py
pip install scipy==1.6.1

pip install dgl-cu101==0.6.1
	sci-py
pip install dgl==0.6.1
pip install matplotlib=3.4.2
pip install tqdm==4.60.0
pip install pyparsing==2.2.1
pip install jarvis-tools==2021.07.19
	matplotlib
	tqdm
	pyparsing
pip install pytorch-ignite==0.4.7
pip install pydantic==1.8.1
pip install pycodestyle==2.7.0
pip install flake8==3.9.1
	pycodestyle
pip install pydocstyle==6.0.0


conda install pandas=1.2.3
	num-py
conda install matplotlib=3.4.2
conda install scikit-learn=0.23




conda install pandas=1.2.3
conda install matplotlib=3.4.2
conda install scikit-learn=0.23

pip install --force-reinstall charset-normalizer==2.0.4


In setup.py, changed scripts to have FineTuning/ prepended:
scripts=['FineTuning/alignn/pretrained.py','FineTuning/alignn/train_folder.py']


Ran this in ALIGNNTL:
python -m pip install -e .
	might not have worked

Ran this in ALIGNNTL/FineTuning:
python -m pip install -e .
	Note: I copied the original setup.py file from .. into FineTuning

pip install scikit-image
![image](https://github.com/user-attachments/assets/3df68f4b-4b9b-475e-8a96-50611f1e2516)






![image](https://github.com/user-attachments/assets/d18ca832-4d50-4b74-8a32-54fe1496ddd5)







Steps for using ALIGNNTL such that I specify a source dataset that is similar to (probably has to have same target property) as a specified MXene property I want to predict:
	
 1. If not super large dataset, copy POSCAR/CIF/etc. files into a directory for the source dataset here:
		/path/ALIGNNTL/SOURCE_DIRECTORY
	
 2. Copy the .csv target properties for the dataset into the source dataset directory such that there are two columns, the first one being the name of the POSCAR/CIF/etc. file for the corresponding record, and the second being the value of the target property
	
 3. Copy the default config file into this source dataset directory
	
 4. Modify the config file to make sure that train n, val n, and test n are correct. 
	
 5. Change source_model to be the pretrained model for the specific property. If there isn't one, change this to "null" (if it isn't already null)
		a. Can even change "target"? If you know it??? Not sure about this, though
	
 6. Make sure that the batch size is a multiple of the training, test, val sets (or, at the very least, that it is smaller than these sets)
	
 7. Make sure that the number of epochs is small enough to do a quick run to see if it works (e.g. 3)
	
 8. Run this code, making sure that the correct root_dir, config file, id_prop_file, and output directory are correctly specified
	
 9. In VS code, open the ALIGNNTL directory in the explorer taskbar to the left
	10. Download the output directory from this source training task onto my laptop
		a. Perhaps then delete .pt files until there is only one .pt file remaining?
	
 11. Open the file directory on my laptop, go to this downloaded directory, and zip this folder
	
 12. Move this .zip folder onto Turing by dragging its icon from the file directory onto VS code and place it into this directory:
		/path/ALIGNNTL/FineTuning/alignn/DIRECTORY_NAME.zip
	
 13. For my target MXenes dataset, change the config file's source model to have "DIRECTORY_NAME" as "source_model"
	
 14. Make sure that n_val, n_test, and n_train are correctly set
	
 15. Make sure that the batch size is smaller than the training, test, and val sets
	
 16. Make the number of epochs small just to make sure that this runs properly
	
 17. Edit the train.py file here to add the pretrained model that we just trained to the list of pretrained models. This file can be found here: /path/ALIGNNTL/FineTuning/alignn/train.py   . Code look something like this (if DIRECTORY_NAME is "2024-07-20"):
	
 BEFORE:
	all_models = {
	    "mp_e_form_alignnn": [
	        "https://figshare.com/ndownloader/files/31458811",
	        1,
	    ],
	    "mp_gappbe_alignnn": [
	        "https://figshare.com/ndownloader/files/31458814",
	        1,
	    ],
	    "jv_bulk_modulus_kv_alignn": [
	        "https://figshare.com/ndownloader/files/31458649",
	        1,
	    ],
	    }

AFTER:
all_models = {
    "mp_e_form_alignnn": [
        "https://figshare.com/ndownloader/files/31458811",
        1,
    ],
    "mp_gappbe_alignnn": [
        "https://figshare.com/ndownloader/files/31458814",
        1,
    ],
    "jv_bulk_modulus_kv_alignn": [
        "https://figshare.com/ndownloader/files/31458649",
        1,
    ],
    "2024-07-20": [
        "",
        1,
    ],
}
	


18. Run this code, making sure that the correct root_dir, config file, id_prop_file, and output directory are correctly specified. Transfer learning done!!





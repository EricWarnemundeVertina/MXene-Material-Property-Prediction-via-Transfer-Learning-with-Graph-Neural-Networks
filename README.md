# MXene-Material-Property-Prediction-via-Transfer-Learning-with-Graph-Neural-Networks
GitHub repository corresponding to the paper: MXene Material Property Prediction via Transfer Learning with Graph Neural Networks


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





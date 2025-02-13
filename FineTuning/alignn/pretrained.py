#!/usr/bin/env python

"""Module to download and load pre-trained ALIGNN models."""
import requests
import os
import zipfile
from tqdm import tqdm
from alignn.models.alignn import ALIGNN, ALIGNNConfig
import tempfile
import torch
import sys
from jarvis.db.jsonutils import loadjson
import argparse
from jarvis.core.atoms import Atoms
from jarvis.core.graphs import Graph
import pandas as pd

# Name of the model, figshare link, number of outputs
all_models = {
    "jv_formation_energy_peratom_alignn": [
        "https://figshare.com/ndownloader/files/31458679",
        1,
    ],
    "jv_optb88vdw_total_energy_alignn": [
        "https://figshare.com/ndownloader/files/31459642",
        1,
    ],
    "jv_optb88vdw_bandgap_alignn": [
        "https://figshare.com/ndownloader/files/31459636",
        1,
    ],
    "jv_mbj_bandgap_alignn": [
        "https://figshare.com/ndownloader/files/31458694",
        1,
    ],
    "jv_spillage_alignn": [
        "https://figshare.com/ndownloader/files/31458736",
        1,
    ],
    "jv_slme_alignn": ["https://figshare.com/ndownloader/files/31458727", 1],
    "jv_bulk_modulus_kv_alignn": [
        "https://figshare.com/ndownloader/files/31458649",
        1,
    ],
    "jv_shear_modulus_gv_alignn": [
        "https://figshare.com/ndownloader/files/31458724",
        1,
    ],
    "jv_n-Seebeck_alignn": [
        "https://figshare.com/ndownloader/files/31458718",
        1,
    ],
    "jv_n-powerfact_alignn": [
        "https://figshare.com/ndownloader/files/31458712",
        1,
    ],
    "jv_magmom_oszicar_alignn": [
        "https://figshare.com/ndownloader/files/31458685",
        1,
    ],
    "jv_kpoint_length_unit_alignn": [
        "https://figshare.com/ndownloader/files/31458682",
        1,
    ],
    "jv_avg_elec_mass_alignn": [
        "https://figshare.com/ndownloader/files/31458643",
        1,
    ],
    "jv_avg_hole_mass_alignn": [
        "https://figshare.com/ndownloader/files/31458646",
        1,
    ],
    "jv_epsx_alignn": ["https://figshare.com/ndownloader/files/31458667", 1],
    "jv_mepsx_alignn": ["https://figshare.com/ndownloader/files/31458703", 1],
    "jv_max_efg_alignn": [
        "https://figshare.com/ndownloader/files/31458691",
        1,
    ],
    "jv_ehull_alignn": ["https://figshare.com/ndownloader/files/31458658", 1],
    "jv_dfpt_piezo_max_dielectric_alignn": [
        "https://figshare.com/ndownloader/files/31458652",
        1,
    ],
    "jv_dfpt_piezo_max_dij_alignn": [
        "https://figshare.com/ndownloader/files/31458655",
        1,
    ],
    "jv_exfoliation_energy_alignn": [
        "https://figshare.com/ndownloader/files/31458676",
        1,
    ],
    "mp_e_form_alignn": [
        "https://figshare.com/ndownloader/files/31458811",
        1,
    ],
    "mp_gappbe_alignn": [
        "https://figshare.com/ndownloader/files/31458814",
        1,
    ],
    "qm9_U0_alignn": ["https://figshare.com/ndownloader/files/31459054", 1],
    "qm9_U_alignn": ["https://figshare.com/ndownloader/files/31459051", 1],
    "qm9_alpha_alignn": ["https://figshare.com/ndownloader/files/31459027", 1],
    "qm9_gap_alignn": ["https://figshare.com/ndownloader/files/31459036", 1],
    "qm9_G_alignn": ["https://figshare.com/ndownloader/files/31459033", 1],
    "qm9_HOMO_alignn": ["https://figshare.com/ndownloader/files/31459042", 1],
    "qm9_LUMO_alignn": ["https://figshare.com/ndownloader/files/31459045", 1],
    "qm9_ZPVE_alignn": ["https://figshare.com/ndownloader/files/31459057", 1],
    "hmof_co2_absp_alignnn": [
        "https://figshare.com/ndownloader/files/31459198",
        5,
    ],
    "hmof_max_co2_adsp_alignnn": [
        "https://figshare.com/ndownloader/files/31459207",
        1,
    ],
    "hmof_surface_area_m2g_alignnn": [
        "https://figshare.com/ndownloader/files/31459222",
        1,
    ],
    "hmof_surface_area_m2cm3_alignnn": [
        "https://figshare.com/ndownloader/files/31459219",
        1,
    ],
    "hmof_pld_alignnn": ["https://figshare.com/ndownloader/files/31459216", 1],
    "hmof_lcd_alignnn": ["https://figshare.com/ndownloader/files/31459201", 1],
    "hmof_void_fraction_alignnn": [
        "https://figshare.com/ndownloader/files/31459228",
        1,
    ],
    "C2DB-2024-10-29-Bulk_modulus_K_best": [
        "",
        1,
    ],
    "2024-10-29-Fermi_Level_best": [
        "",
        1,
    ],
    "2024-10-29-Poissons_ratio_best": [
        "",
        1,
    ],
    "2024-10-29-Shear_modulus_best": [
        "",
        1,
    ],
    "2024-10-29-Youngs_modulus_best": [
        "",
        1,
    ],
    "2024-10-29-Magnetic_best": [
        "",
        1,
    ],
    "2024-10-29-all_properties_best": [
        "",
        5,
    ],
    "2024-10-13-Bulk_modulus_K_best": [
        "",
        1,
    ],
    "2024-10-13-Fermi_Level_best": [
        "",
        1,
    ],
    "2024-10-13-Poissons_ratio_best": [
        "",
        1,
    ],
    "2024-10-13-Shear_modulus_best": [
        "",
        1,
    ],
    "2024-10-13-Youngs_modulus_best": [
        "",
        1,
    ],
    "extra_sc": [
        None,
        1,
    ],
    "extra_tl": [
        None,
        1,
    ],
}
parser = argparse.ArgumentParser(
    description="Atomistic Line Graph Neural Network Pretrained Models"
)
parser.add_argument(
    "--model_name",
    default="jv_formation_energy_peratom_alignn",
    help="Choose a model from these "
    + str(len(list(all_models.keys())))
    + " models:"
    + ", ".join(list(all_models.keys())),
)

parser.add_argument(
    "--file_format", default="poscar", help="poscar/cif/xyz/pdb file format."
)

parser.add_argument(
    "--file_path",
    default="alignn/examples/sample_data/",
    help="Path to directory where data is stored."
)

parser.add_argument(
    "--save_path",
    default="/home/ewvertina/ALIGNNTL/Experiment_Results/Best/2024-01-20/",
    help="Path to where predictions will be saved."
)

parser.add_argument(
    "--cutoff",
    default=8,
    help="Distance cut-off for graph constuction"
    + ", usually 8 for solids and 5 for molecules."
)


device = "cpu"
if torch.cuda.is_available():
    device = torch.device("cuda")


def get_prediction(
        model_name, 
        cutoff, 
        file_path, 
        save_path, 
        file_format
):
    """Get model with progress bar."""
    tmp = all_models[model_name]
    url = tmp[0]
    output_features = tmp[1]
    zfile = model_name + ".zip"
    path = str(os.path.join(os.path.dirname(__file__), zfile))
    if not os.path.isfile(path):
        print('.zip file with pretrained model not found!')
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(
            total=total_size_in_bytes, unit="iB", unit_scale=True
        )
        with open(path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    zp = zipfile.ZipFile(path)
    names = zp.namelist()
    for i in names:
        if "checkpoint_" in i and "pt" in i:
            tmp = i
            # print("chk", i)
    # print("Loading the zipfile...", zipfile.ZipFile(path).namelist())
    data = zipfile.ZipFile(path).read(tmp)
    if 'Magnetic' in model_name:
        model = ALIGNN(
            ALIGNNConfig(name="alignn", output_features=output_features, classification=True)
        )
    else:
        model = ALIGNN(
            ALIGNNConfig(name="alignn", output_features=output_features, classification=False)
        )
    new_file, filename = tempfile.mkstemp()
    with open(filename, "wb") as f:
        f.write(data)
    model.load_state_dict(torch.load(filename, map_location=device)["model"])
    model.to(device)
    model.eval()
    if os.path.exists(filename):
        os.remove(filename)


    all_items = os.listdir(file_path)
    material_name_list = []
    prediction_list = []
    print('About to start predictions')
    for file in all_items:
        if file_format == "poscar":
            atoms = Atoms.from_poscar(file_path + file)
        elif file_format == "cif":
            atoms = Atoms.from_cif(file_path + file)
        elif file_format == "xyz":
            atoms = Atoms.from_xyz(file_path + file, box_size=500)
        elif file_format == "pdb":
            atoms = Atoms.from_pdb(file_path + file, max_lat=500)
        else:
            raise NotImplementedError("File format not implemented", file_format)


        # print("Loading completed.")
        g, lg = Graph.atom_dgl_multigraph(atoms, cutoff=float(cutoff))
        #print(lg.edata)
        #print(lg)
        out_data = (
            model([g.to(device), lg.to(device)])
            .detach()
            .cpu()
            .numpy()
            .flatten()
            .tolist()
        )

        print("Predicted value:", model_name, file, out_data)
        
        material_name_list.append(file)
        if 'all_properties' in model_name:
            prediction_list.append(out_data)
        else:
            prediction_list.append(out_data[0])

    data = {"Material": material_name_list,
            model_name: prediction_list
            }
    df = pd.DataFrame(data)
    
    if 'Magnetic' in model_name: #if predicting whether or not a material is magnetic
        df[model_name] = df[model_name] < -0.5
        

    if os.path.exists(save_path + model_name + ".csv"):
        df.to_csv(save_path + model_name + ".csv", mode='a', index=False, header=False)
    else:
        df.to_csv(save_path + model_name + ".csv", index=False)


    return 'Done running get_prediction!'


if __name__ == "__main__":
    print('Code is running!')
    args = parser.parse_args(sys.argv[1:])
    model_name = args.model_name
    file_path = args.file_path
    save_path = args.save_path
    file_format = args.file_format
    cutoff = args.cutoff

    out_data = get_prediction(model_name, float(cutoff), file_path, save_path, file_format)

    print('Done!')
# x = get_model()
# print(x)

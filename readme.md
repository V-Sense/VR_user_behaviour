# Do Users Behave Similarly in VR? Investigation of the Influence on the System Design

<p align="center">
  <img src="https://github.com/V-Sense/VR_user_behaviour/blob/master/img/ucl_tcd.png?raw=true"/>
</p>

We are sharing our dataset and developed tools that we hope will enable in creating more immersive virtual reality experiences. This repository is for open source codes and materials for the paper: [Do users behave similarly in VR? Investigation of the influence on the system design](https://v-sense.scss.tcd.ie/research/3dof/vr_user_behaviour_system_design/)

## Downloading the dataset

### Requirements
Each available codes in this repository is based on Python 3.

Firstly, you should install the following dependencies:

* pip install wget

A python script, named `download.py` is provided to download the dataset.
The following script can download all the dataset and locate it into the project folder.

* python download.py

Alternatively, you can download it with this [link](http://v-sense.scss.tcd.ie/Datasets/data_ucl_tcd.zip).

## Dataset

<p align="center">
  <img src="https://github.com/V-Sense/VR_user_behaviour/blob/master/img/organization.png?raw=true" alt="Folder tree composition of the introduced dataset for viewport trajectories of ODVs."/>
</p>

Figure 1 illustrates the organization of the dataset. The folder of the downloaded and extracted `data` folder contains three sub-folders, namely `trajectories`and `videos`.  The `trajectories` folder contains three subfolders in which each one represents a device: `dev_0`: HMD ,`dev_1`: Laptop, and `dev_2`: Tablet. Each sub-folder is then contained a number of sub-sub-folders, omnidirectional video (ODV) folder, corresponding the names of the ODVs, *e.g., v01\_BabyPandas*. Each ODV folder contains the number of CSV files which corresponds to the number of participants.  The viewport trajectories are stored as comma-separated values (CSV) files in ASCII. The name of each CSV file specifies the participant ID, and each line of the CSV file has the following structure:

| u | v | university | category |
| ------------ | ------------- |
|0.523|	0.564| tcd|	cat1|

> **u**: u coordinate of the viewport center (normalized value).

> **v**:  v coordinate of the viewport (normalized value).

> **university**: subjective experiment location.

> **category**: category type of ODV.

The `videos` folder contains three sub-folders in which each one represents a category ID number: `cat1`: Documentary, `cat2`: Movie , and `cat3`: Action.  Each sub-folder is then contained a number of sub-sub-folders, omnidirectional video (ODV) folder, corresponding the names of the ODVs, *e.g., v01\_BabyPandas*. 

## Tools




## Citation 

Please cite our paper in your publications if it helps your research:

```
@article{rossi2020,
title = {Do users behave similarly in VR? Investigation of the influence on the system design},
author = {Silvia Rossi and Cagri Ozcinar and Aljosa Smolic and Laura Toni},
year = {2020},
booktitle = {Transactions on Multimedia Computing Communications and Applications}
}
```

## Authors

| [Silvia Rossi](https://www.ucl.ac.uk/iccs/silvia-rossi) | [Cagri Ozcinar](https://cagriozcinar.netlify.com/) |[Aljosa Smolic](https://v-sense.scss.tcd.ie/?profile=prof-aljosa-smolic) | [Laura Toni](https://www.ucl.ac.uk/iccs/dr-laura-toni) |

## Acknowledgement

This work has been partially funded by Adobe under Academic Donation scheme. Also, this publication has emanated from research supported in part by a research grant from Science Foundation Ireland (SFI) under the Grant Number 15/RP/2776.


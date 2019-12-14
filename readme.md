# Do Users Behave Similarly in VR? Investigation of the Influence on the System Design

## Requirements
Each available codes in this repository is based on Python 3.

### Downloading the dataset

Firstly, you should install the following dependencies:

* pip install wget

A python script, named `download.py` is provided to download the dataset.
The following script can download all the dataset and locate it into the project folder.

* python download.py

Alternatively, you can download it with this [link](http://v-sense.scss.tcd.ie/Datasets/data_ucl_tcd.zip).

## Dataset

![Alt text](/image/organization.png "Folder tree composition of the introduced dataset for viewport trajectories of ODVs.")

Figure 1 illustrates the organization of the dataset. The folder of the downloaded and extracted `data` folder contains three sub-folders, namely `trajectories`, `videos`, and `tools`.  The `trajectories` folder contains three subfolders in which each one represents a device: `dev_0`: HMD ,`dev_1`: Laptop, and `dev_2`: Tablet. Each sub-folder is then contained a number of sub-sub-folders, omnidirectional video (ODV) folder, corresponding the names of the ODVs, *e.g., v01\_BabyPandas*. Each ODV folder contains the number of CSV files which corresponds to the number of participants.  The viewport trajectories are stored as comma-separated values (CSV) files in ASCII. The name of each CSV file specifies the participant ID, and each line of the CSV file has the following structure:

| u | v | university | category |
| ------------ | ------------- |
|0.523|	0.564| tcd|	cat1|

**u**: u coordinate of the viewport center (normalized value).
**v**:  v coordinate of the viewport (normalized value).
**university**: subjective experiment location.
**category**: category type of ODV.

The `videos` folder contains three sub-folders in which each one represents a category ID number: `cat1`: Documentary, `cat2`: Movie , and `cat3`: Action.  Each sub-folder is then contained a number of sub-sub-folders, omnidirectional video (ODV) folder, corresponding the names of the ODVs, *e.g., v01\_BabyPandas*. 
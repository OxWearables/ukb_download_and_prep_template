# Downloading accelerometer data from UK Biobank database

We want to download raw accelerometer data to the BMRC/Rescomp system. However
it is not possible to run a parallel download of UK Biobank accelerometer data 
from this system (we could do it one-by-one but that would take forever). We
therefore use the NDPH NC system to download the UKBB accelerometer data to a 
temporary location on there. Then we rsync the data from NC to the BMRC/Rescomp
system.

- First, we want to extract the calibration information as this will reduce 
subsequent processing time of the raw accelerometer data by 50%. There is no 
clear benefit to recalibrating the UK Biobank accelerometer data. Therefore:
  ```Bash
  $../helpers/linux/ukb_conv /bm1/datasets/uk-biobank/aiden9126/participant-/dataukb9936.enc_ukb \
    csv -icalibrationCols.txt -oaccCalibrationVals
  # output = accCalibrationVals.csv
  ```

- Then read the calibrated values, create a [study structure](https://biobankaccanalysis.readthedocs.io/en/latest/usage.html#processing-multiple-files)
 to store the data, and write a list of commands to download each accelerometer 
 file one-by-one to a .cwa.gz file:
  ```Bash
  $ python download-UKBB-accData.py accCalibrationVals.csv \
    /bm1/datasets/uk-biobank/aiden9126/accelerometer/
  # output = study structure written to /bm1/.../accelerometer/ (subfolder for every 10k files)
  #         download.txt (line to download each file)
  ```

- Write commands to run download scripts on SLRUM scheduler (used on NC system).
 This system has an array job maximum limit of 1,000 
  ```Bash
  $ python ~/code/clusterProcessing/write-NC-scripts.py download.txt \
        --logDir /bm1/.../accelerometer/downloadLogs/
  # output = submit-download-*.sh (submission scripts)
  ```

- Submit jobs to kick-start download process. UK Biobank has a limit of 10
simultaneous downloads, therefore we restrict the process to just run 2 nodes
at a time (4 cpus per node). We use the dependency command to make subsequent
jobs wait on each job to finish (to ensure we don't violate the 10 simultaneous
download limit):
  ```Bash
  $ sbatch --array=0-999%2 --partition=general submit-download-0.sh

  #     if ID for task above is 356566...
  $ sbatch --dependency=afterok:356566 --array=0-999%2 --partition=general submit-download-1.sh

  #     if ID for task above is 356569...
  $ sbatch --dependency=afterok:356569 --array=0-500%2 --partition=general submit-download-2.sh

  # and so on ... for all submit-download-*.sh
  ```

- Finally, transfer raw files for each subfolder from NC to BMRC e.g.:
  ```Bash
    rsync -ar subfolder-9/ aidend@rescomp1.well.ox.ac.uk:/well/doherty/projects/ukBiobank/aiden/accelerometer/subfolder-9/ &
  ```



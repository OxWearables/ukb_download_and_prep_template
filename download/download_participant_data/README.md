# Downloading UK Biobank participant data

## Downloading a new copy of the data

This [well documented site on how to access UK Biobank data](http://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=AccessingData) is a good starting point. 
You should carefully read the ['Using UK Biobank data'](http://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=accessing_data_guide#intro) guide to setup decryption keys. 
Therefore, for Aiden's UKB 59070 research application and copy number 41733 we would decrypt to an 'unpacked' file
  ```Bash
  $ ../helpers/linux_tools/ukb_unpack /well/doherty/projects/UKBB/participant_info/ukb41733.enc k59070r41733.key
  # output = /well/doherty/projects/UKBB/participant-data/ukb.enc_ukb
  ```

Specific fields of interest can be extracted from the .enc_ukb file. 
# Downloading UK Biobank participant data

This [well documented site on how to access UK Biobank data](http://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=AccessingData) is a good starting point. 

You will download an encrypted `ukb12345.csv` file. This needs to be decrypted using the key provided by UK Biobank in an email. 

Using this, for research application 6789 and copy number 12345 we would decrypt to an 'unpacked' file: 
  ```Bash
  $ .helpers/linux_tools/ukb_unpack path_to_data/ukb12345.enc k6789r41733.key
  # output = path_to_data/ukb12345.enc_ukb
  ```
  
Specific fields of interest can be extracted from the `.enc_ukb` file (see main repo). 

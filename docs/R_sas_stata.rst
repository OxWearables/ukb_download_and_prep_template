######################################
An alternative for R/ SAS/ Stata users
######################################

If you prefer to use R, SAS or Stata for data preparation, UK Biobank has a built-in tool to facilitate this. However, note this tool doesn't have the column-renaming functionality and additional flexibility on recoding implemented as part of this tool.  

For example, to use R: 

.. code-block:: sh
 
  download/helpers/linux_tools/ukb_conv path_to_data/ukb12345.enc_ukb r -ianalysisCols.txt
  # output = path_to_data/ukb12345.r
  # output = path_to_data/ukb12345.tab
   
:code:`ukb12345.r` can be opened and run in R: it will automatically recode - but not rename - categorical columns.  


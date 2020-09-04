#############################
Downloading participant data
#############################

Here we are using only standard UK Biobank functionality, so `UK Biobank's guide to accessing the data <https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf>`_ is a very useful reference. 

You will have initially downloaded an encrypted :code:`ukb12345.enc` file. This needs to be decrypted using the key provided by UK Biobank in an email e.g. for research application 6789 and copy number 12345 we would decrypt to an 'unpacked' file: 

.. code-block::

  download/helpers/linux_tools/ukb_unpack path_to_data/ukb12345.enc k6789r12345.key
  download/helpers/linux_tools/ukb_unpack path_to_data/ukb12345.enc k6789r12345.key
  # output = path_to_data/ukb12345.enc_ukb
    
To extract data from this to :code:`.csv` format, see the `next section <https://ukb-download-and-prep-template.readthedocs.io/en/latest/extract.html>`_. 

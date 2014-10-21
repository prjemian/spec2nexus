.. restructured text format

About these example data files
----------------------------------

These files are examples of various
data files that may be read by **spec2nexus**.
They are used to test various components of the interface.


======================================  ==========  ==========================================================================
file						            type	    description
======================================  ==========  ==========================================================================
33bm_spec.dat                           SPEC scans  1-D & 2-D scans (includes hklscan & hklmesh)
33id_spec.dat                           SPEC scans  1-D & 2-D scans (includes mesh & Escan scans & MCA data)
APS_spec_data.dat                       SPEC scans  1-D scans (ascan & uascan), includes lots of metadata and comments
CdSe                                    SPEC scans  1-D scans (ascan), problem with scan abort on lines 5918-9, in scan 92
compression.h5                          NeXus HDF5  2-D compressed image, also demonstrates problem to be resolved in code
Data_Q.h5                               NeXus HDF5  2-D image at /entry/data/{I,Q}, test file
lmn40.spe                               SPEC scans  1-D & 2-D scans (hklmesh), two #E lines, has two header sections
writer_1_3.h5                           NeXus HDF5  1-D NeXus User Manual example
YSZ011_ALDITO_Fe2O3_planar_fired_1.spc  SPEC scans  1-D scans, text in #V metadata, also has #UIM control lines
======================================  ==========  ==========================================================================

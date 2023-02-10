.. _data.file.geometry:

Geometry
++++++++

*Geometry*, in the context of a SPEC data file, refers to the geometry of the
**diffractometer** used for the measurements, its configuration, and information
about the orientation of a specific crystalline sample on the diffractometer.

When a diffractometer geometry is used, any of the control lines in the next table
may be present in a scan.

==============  ==========  ========================================
control line    array       description
==============  ==========  ========================================
``#G0``         ``G[]``     geo mode, sector, etc
``#G1``         ``U[]``     lattice constants, orientation reflections
``#G2``         ..          unused
``#G3``         ``UB[]``    orientation matrix
``#G4``         ``Q[]``     lambda, frozen angles, cut points, etc
``#Q``          ..          *hkl* values at start of scan
==============  ==========  ========================================

Information provided by each of these control lines is encoded in a very compact
format, with just a sequence of values provided.  The content of some lines
depends on the specific diffractometer geometry used for the measurements. The
**name** of the diffractometer geometry is not reported in the data file.  To
identify the diffractometer geometry, it is necessary to examine the number and
names of the first motors defined in the ``#O`` control lines, and compare the
number of items in the various ``#G`` control lines with the SPEC standard
macros to match.  The **spec2nexus** code has a small database
[#diffractometer.dict]_ with this information to make a best efforts
identification of the specific diffractometer geometry name.

Since SPEC uses specific engineering :index:`units` when diffractometers are
used, it is possible to add appropriate units: [#NX.unittype]_

* motors (angles): ``@units="degrees"`` for motors
* wavelength: ``@units="angstrom"``
* crystal dimensions: ``@units="angstrom"``

.. code-block::
   :linenos:

   #G0 0 0 1 0 0 1 0 0 0 0 0 0 50 0 0.1 0 68 68 50 -1 1 1 3.13542 3.13542 0 463.6 838.8
   #G1 5.139 5.139 5.139 90 90 90 1.222647462 1.222647462 1.222647462 90 90 90 2 2 0 0 0 2 60 30 90 0 0 0 60 30 0 0 0 0 0.8265814273 0.8265814273
   #G3 -7.940607166e-18 1.138130079e-16 1.222647462 0.8645423114 -0.8645423114 0 0.8645423114 0.8645423114 -2.668317968e-16
   #G4 3.986173683 4.00012985 0 0.8265814273 0 0 0 90 0.15 0 0 0 86 0 0 0 -180 -180 -180 -180 -180 -180 -180 -180 -180 0
   #Q 3.98617 4.00013 0

It is possible to infer the diffractometer geometry in many cases by content in
the ``#G0`` and ``#G4`` control lines, which includes the number and names of
the motors in the geometry. With the control lines above and these motor names
as shown below, the geometry is inferred as **fourc**.

.. code-block::
   :linenos:

   #O0  2-theta     theta       chi       phi   antheta  an2theta    z-axis     m_1_8

The *hkl* values at the start of the scan are written to ``/SCAN/Q`` as shown here:

.. code-block::
   :linenos:

   Q:NX_FLOAT64[3] = [3.98617, 4.00013, 0.0]
      @description = "hkl at start of scan"

The uninterpreted information from the ``#G`` control lines is written to
``/SCAN/G`` as shown here:

.. code-block::
   :linenos:

   G:NXnote
      @NX_class = "NXnote"
      @description = "SPEC geometry arrays, meanings defined by SPEC diffractometer support"
      G0:NX_FLOAT64[27] = [0.0, 0.0, 1.0, '...', 838.8]
        @spec_name = "G0"
      G1:NX_FLOAT64[32] = [5.139, 5.139, 5.139, '...', 0.8265814273]
        @spec_name = "G1"
      G3:NX_FLOAT64[9] = [-7.940607166e-18, 1.138130079e-16, 1.222647462, '...', -2.668317968e-16]
        @spec_name = "G3"
      G4:NX_FLOAT64[26] = [3.986173683, 4.00012985, 0.0, '...', 0.0]
        @spec_name = "G4"

The interpreted information from the ``G[]`` array is written to
``/SCAN/instrument/diffractometer`` (and linked to
``/SCAN/instrument/geometry_parameters``).  Text description
of each parameter is provided when available.

If it was possible to determine the name of the diffractometer geometry, that
name will be reported in the ``name`` field.  In SPEC, some of the geometries
have variants.  The variant is appended to the name as:
``{GEOMETRY}.{VARIANT}``.  In the example below, the name is ``fourc.default``.

The **wavelength** of the scan, if available in the ``#G`` lines, is written to
the ``/SCAN/instrument/monochromator/wavelength`` field, [#NX.field]_ where
``/SCAN/instrument/monochromator`` is a **NXmonochromator** [#NXmonochromator]
group.

Consult the SPEC documentation (https://certif.com) or macros for further
descrption of any of the geometry information.

.. code-block::
   :linenos:

   instrument:NXinstrument
      @NX_class = "NXinstrument"
      name:NX_CHAR = [b'fourc.default']
      positioners --> /S1/positioners
      diffractometer:NXnote
        @NX_class = "NXnote"
        @description = "SPEC geometry arrays, interpreted"
        ALPHA:NX_FLOAT64 = 0.0
        AZIMUTH:NX_FLOAT64 = 90.0
        BETA:NX_FLOAT64 = 0.0
        CUT_AZI:NX_FLOAT64 = 0.0
          @description = "azimuthal cut-point flag"
        CUT_CHI:NX_FLOAT64 = -180.0
          @description = "chi cut point"
        CUT_CHIR:NX_FLOAT64 = -180.0
          @description = "chiR cut point"
        CUT_KAP:NX_FLOAT64 = -180.0
          @description = "kap cut point"
        CUT_KPHI:NX_FLOAT64 = -180.0
          @description = "phi cut point"
        CUT_KTH:NX_FLOAT64 = -180.0
          @description = "theta cut point"
        CUT_PHI:NX_FLOAT64 = -180.0
          @description = "phi cut point"
        CUT_PHIR:NX_FLOAT64 = -180.0
          @description = "phiR cut point"
        CUT_TH:NX_FLOAT64 = -180.0
          @description = "theta/omega cut point"
        CUT_TTH:NX_FLOAT64 = -180.0
          @description = "two-theta cut point"
        F_ALPHA:NX_FLOAT64 = 0.15
          @description = "Frozen values"
        F_AZIMUTH:NX_FLOAT64 = 0.0
        F_BETA:NX_FLOAT64 = 0.0
        F_CHI_Z:NX_FLOAT64 = 0.0
        F_OMEGA:NX_FLOAT64 = 0.0
        F_PHI:NX_FLOAT64 = 86.0
        F_PHI_Z:NX_FLOAT64 = 0.0
        F_THETA:NX_FLOAT64 = 0.0
        H:NX_FLOAT64 = 3.986173683
          @description = "1st Miller index"
        K:NX_FLOAT64 = 4.00012985
          @description = "2nd Miller index"
        L:NX_FLOAT64 = 0.0
          @description = "3rd Miller index"
        LAMBDA:NX_FLOAT64 = 0.8265814273
          @description = "wavelength, Angstrom"
        OMEGA:NX_FLOAT64 = 0.0
        diffractometer_full:NX_CHAR = [b'fourc.default']
          @description = "name of diffractometer (and variant), deduced from scan information"
        diffractometer_simple:NX_CHAR = [b'fourc']
          @description = "name of diffractometer, deduced from scan information"
        diffractometer_variant:NX_CHAR = [b'default']
          @description = "name of diffractometer variant, deduced from scan information"
        g_aa:NX_FLOAT64 = 5.139
          @description = "a lattice constant (real space)"
        g_aa_s:NX_FLOAT64 = 1.222647462
          @description = "a lattice constant (reciprocal space)"
        g_al:NX_FLOAT64 = 90.0
          @description = "alpha lattice angle (real space)"
        g_al_s:NX_FLOAT64 = 90.0
          @description = "alpha lattice angle (reciprocal space)"
        g_ana_d:NX_FLOAT64 = 3.13542
        g_ana_det_len:NX_FLOAT64 = 50.0
        g_ana_sign:NX_FLOAT64 = 1.0
        g_bb:NX_FLOAT64 = 5.139
          @description = "b lattice constant (real space)"
        g_bb_s:NX_FLOAT64 = 1.222647462
          @description = "b lattice constant (reciprocal space)"
        g_be:NX_FLOAT64 = 90.0
          @description = "beta  lattice angle (real space)"
        g_be_s:NX_FLOAT64 = 90.0
          @description = "beta  lattice angle (reciprocal space)"
        g_cc:NX_FLOAT64 = 5.139
          @description = "c lattice constant (real space)"
        g_cc_s:NX_FLOAT64 = 1.222647462
          @description = "c lattice constant (reciprocal space)"
        g_frz:NX_FLOAT64 = 1.0
          @description = "freeze"
        g_ga:NX_FLOAT64 = 90.0
          @description = "gamma lattice angle (real space)"
        g_ga_s:NX_FLOAT64 = 90.0
          @description = "gamma lattice angle (reciprocal space)"
        g_h0:NX_FLOAT64 = 2.0
          @description = "H of primary reflection"
        g_h1:NX_FLOAT64 = 0.0
          @description = "H of secondary reflection"
        g_haz:NX_FLOAT64 = 0.0
          @description = "h azimuthal reference"
        g_inci_offset:NX_FLOAT64 = 0.0
        g_k0:NX_FLOAT64 = 2.0
          @description = "K of primary reflection"
        g_k1:NX_FLOAT64 = 0.0
          @description = "K of secondary reflection"
        g_kappa:NX_FLOAT64 = 50.0
          @description = "angle of kappa tilt (in degrees)"
        g_kaz:NX_FLOAT64 = 0.0
          @description = "k azimuthal reference"
        g_l0:NX_FLOAT64 = 0.0
          @description = "L of primary reflection"
        g_l1:NX_FLOAT64 = 2.0
          @description = "L of secondary reflection"
        g_lambda0:NX_FLOAT64 = 0.8265814273
          @description = "lambda when or0 was set"
        g_lambda1:NX_FLOAT64 = 0.8265814273
          @description = "lambda when or1 was set"
        g_laz:NX_FLOAT64 = 1.0
          @description = "l azimuthal reference"
        g_mode:NX_FLOAT64 = 0.0
          @description = "spectrometer mode"
        g_mode_name:NX_CHAR = [b'Omega equals zero']
          @description = "name of spectrometer mode"
        g_mon_d:NX_FLOAT64 = 3.13542
        g_mon_sam_len:NX_FLOAT64 = 68.0
        g_mon_sign:NX_FLOAT64 = -1.0
        g_omsect:NX_FLOAT64 = 0.0
          @description = "omega-mode sector flag"
        g_picker:NX_FLOAT64 = 0.1
          @description = "picker-mode factor"
        g_sam_ana_len:NX_FLOAT64 = 68.0
        g_sam_sign:NX_FLOAT64 = 1.0
        g_sect:NX_FLOAT64 = 0.0
          @description = "sector"
        g_u00:NX_FLOAT64 = 60.0
          @description = "angle 0 of primary reflection"
        g_u01:NX_FLOAT64 = 30.0
          @description = "angle 1 of primary reflection"
        g_u02:NX_FLOAT64 = 90.0
          @description = "angle 2 of primary reflection"
        g_u03:NX_FLOAT64 = 0.0
          @description = "angle 3 of primary reflection"
        g_u04:NX_FLOAT64 = 0.0
          @description = "angle 4 of primary reflection"
        g_u05:NX_FLOAT64 = 0.0
          @description = "angle 5 of primary reflection"
        g_u10:NX_FLOAT64 = 60.0
          @description = "angle 0 of secondary reflection"
        g_u11:NX_FLOAT64 = 30.0
          @description = "angle 1 of secondary reflection"
        g_u12:NX_FLOAT64 = 0.0
          @description = "angle 2 of secondary reflection"
        g_u13:NX_FLOAT64 = 0.0
          @description = "angle 3 of secondary reflection"
        g_u14:NX_FLOAT64 = 0.0
          @description = "angle 4 of secondary reflection"
        g_u15:NX_FLOAT64 = 0.0
          @description = "angle 5 of secondary reflection"
        g_vmode:NX_FLOAT64 = 0.0
          @description = "set if vertical mode"
        g_xtalogic_d1:NX_FLOAT64 = 463.6
        g_xtalogic_d2:NX_FLOAT64 = 838.8
        g_zh0:NX_FLOAT64 = 0.0
          @description = "h zone vec 0"
        g_zh1:NX_FLOAT64 = 0.0
          @description = "h zone vec 1"
        g_zk0:NX_FLOAT64 = 0.0
          @description = "k zone vec 0"
        g_zk1:NX_FLOAT64 = 0.0
          @description = "k zone vec 1"
        g_zl0:NX_FLOAT64 = 0.0
          @description = "l zone vec 0"
        g_zl1:NX_FLOAT64 = 0.0
          @description = "l zone vec 1"
        ub_matrix:NX_FLOAT64[3,3] = __array
          __array = [
              [-7.940607166e-18, 1.138130079e-16, 1.222647462]
              [0.8645423114, -0.8645423114, 0.0]
              [0.8645423114, 0.8645423114, -2.668317968e-16]
            ]
          @description = "UB[] matrix"
      monochromator:NXmonochromator
        @NX_class = "NXmonochromator"
        wavelength:NX_FLOAT64 = 0.8265814273
          @target = "/S1/instrument/monochromator/wavelength"
          @units = "angstrom"

Crystal sample orientation information (``UB`` matrix, orientation reflections
and wavelength) is written to ``/SCAN/sample`` (a **NXsample** [#NXsample]_ group).

.. code-block::
   :linenos:

   sample:NXsample
      @NX_class = "NXsample"
      diffractometer_mode:NX_CHAR = [b'Omega equals zero']
      diffractometer_sector:NX_INT64 = 0
      ub_matrix:NX_FLOAT64[3,3] = __array
        __array = [
            [-7.940607166e-18, 1.138130079e-16, 1.222647462]
            [0.8645423114, -0.8645423114, 0.0]
            [0.8645423114, 0.8645423114, -2.668317968e-16]
          ]
      unit_cell:NX_FLOAT64[6] = [5.139, 5.139, 5.139, '...', 90.0]
      unit_cell_abc:NX_FLOAT64[3] = [5.139, 5.139, 5.139]
        @units = "angstrom"
      unit_cell_alphabetagamma:NX_FLOAT64[3] = [90.0, 90.0, 90.0]
        @units = "degrees"
      beam:NXbeam
        @NX_class = "NXbeam"
        incident_wavelength --> /S1/instrument/monochromator/wavelength
      or0:NXnote
        @NX_class = "NXnote"
        @description = "or0: orientation reflection"
        chi:NX_FLOAT64 = 90.0
          @description = "diffractometer angle"
          @units = "degrees"
        h:NX_FLOAT64 = 2.0
        k:NX_FLOAT64 = 2.0
        l:NX_FLOAT64 = 0.0
        phi:NX_FLOAT64 = 0.0
          @description = "diffractometer angle"
          @units = "degrees"
        th:NX_FLOAT64 = 30.0
          @description = "diffractometer angle"
          @units = "degrees"
        tth:NX_FLOAT64 = 60.0
          @description = "diffractometer angle"
          @units = "degrees"
        wavelength:NX_FLOAT64 = 0.8265814273
          @units = "Angstrom"
      or1:NXnote
        @NX_class = "NXnote"
        @description = "or1: orientation reflection"
        chi:NX_FLOAT64 = 0.0
          @description = "diffractometer angle"
          @units = "degrees"
        h:NX_FLOAT64 = 0.0
        k:NX_FLOAT64 = 0.0
        l:NX_FLOAT64 = 2.0
        phi:NX_FLOAT64 = 0.0
          @description = "diffractometer angle"
          @units = "degrees"
        th:NX_FLOAT64 = 30.0
          @description = "diffractometer angle"
          @units = "degrees"
        tth:NX_FLOAT64 = 60.0
          @description = "diffractometer angle"
          @units = "degrees"
        wavelength:NX_FLOAT64 = 0.8265814273
          @units = "Angstrom"

.. [#diffractometer.dict] database of diffractometer geometries in SPEC data files:   https://github.com/prjemian/spec2nexus/blob/main/spec2nexus/diffractometer-geometries.dict
.. [#NX.unittype] List of NeXus unit categories:   https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications
.. [#NX.field] A NeXus **field** is the same as an HDF5 **dataset**.  The rename is   due to historical reasons in NeXus when XML was used as a back-end data file   storage format.
.. [#NXmonochromator] **NXmonochromator**:   https://manual.nexusformat.org/classes/base_classes/NXmonochromator.html
.. [#NXsample] **NXsample**:   https://manual.nexusformat.org/classes/base_classes/NXsample.html

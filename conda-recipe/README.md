# Building for Conda

This document describes how to build and upload a 
conda package for ***spec2nexus***.

see: https://conda.io/docs/build_tutorials/pkgs.html

Note:  These commands should be run from the repository root: `..`

## linux-64
    
    export PROJECT=spec2nexus
    export RELEASE=`python ./setup.py --version | grep -o "^[0-9.]*"`

    export ANACONDA=$HOME/Apps/anaconda
    export BUILD_DIR=$ANACONDA/conda-bld
    export HOST_ARCH=linux-64
    export TARGET_DIR=./conda-recipe
    export OUTPUT_DIR=$TARGET_DIR/../conda-packages/
    
    /bin/rm -rf $OUTPUT_DIR
    conda build --python 2.7 $TARGET_DIR 2>&1 | tee $TARGET_DIR/build.log

    #BUILD START: spec2nexus-2017.3.0-py27_0
    #updating index in: /home/prjemian/Apps/anaconda/conda-bld/linux-64
    #updating index in: /home/prjemian/Apps/anaconda/conda-bld/noarch


## local test

this command will install the conda package (just built) install as a local test

    conda install --use-local spec2nexus

## Build & Upload

Build for all supported architectures
and upload to my conda channel.

    mkdir -p $OUTPUT_DIR

    # where $ARCH can be osx-64, linux-32, linux-64, win-32 or win-64
    for ARCH in osx-64 linux-32 linux-64 win-32 win-64; do
      BZ_TARGET=$PROJECT-$RELEASE-py27_0.tar.bz2
      conda convert --platform $ARCH $BUILD_DIR/$HOST_ARCH/$BZ_TARGET -o $OUTPUT_DIR
      #anaconda upload $OUTPUT_DIR/$ARCH/$BZ_TARGET
    done
    #  anaconda upload $OUTPUT_DIR/*/$BZ_TARGET


## win-64

    #BUILD START: spec2nexus-2017.3.0-py27_0
    #updating index in: D:\Apps\Anaconda\conda-bld\win-64
    #updating index in: D:\Apps\Anaconda\conda-bld\noarch

    $env:PROJECT = "spec2nexus"
    ###
    ### EDIT next line to chosen release
    ###
    $env:RELEASE = "2017.317.0"
    ###
    ###

note: FIXME: use correct powershell environment variable syntax!

    $env:ANACONDA   = "$HOME/Apps/anaconda"
    $env:BUILD_DIR  = "$ANACONDA/conda-bld"
    $env:HOST_ARCH  = "linux-64"
    $env:TARGET_DIR = "./conda-recipe"
    $env:OUTPUT_DIR = "$TARGET_DIR/../conda-packages/"
    
    conda build --python 2.7 $TARGET_DIR

    conda install --use-local spec2nexus

## query about ***spec2nexus***

Query conda-forge for any *spec2nexus* packages:

    anaconda search -t conda spec2nexus

What versions of *spec2nexus* are available from my channel?

    anaconda show prjemian/spec2nexus

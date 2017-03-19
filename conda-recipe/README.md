
# how to build and upload a conda package for spec2nexus

	# see: https://conda.io/docs/build_tutorials/pkgs.html\

	export PROJECT=spec2nexus
	export RELEASE=2017.3.0
	export ANACONDA=$HOME/Apps/anaconda
	export BUILD_DIR=$ANACONDA/conda-bld
	export HOST_ARCH=linux-64
	export TARGET_DIR=./conda-recipe
	export OUTPUT_DIR=$TARGET_DIR/builds/

	conda build --python 2.7 $TARGET_DIR

	#BUILD START: spec2nexus-2017.3.0-py27_0
	#updating index in: /home/prjemian/Apps/anaconda/conda-bld/linux-64
	#updating index in: /home/prjemian/Apps/anaconda/conda-bld/noarch


this command will install as a local test

	conda install --use-local spec2nexus

---------------------------

	mkdir -p $OUTPUT_DIR
	# where $ARCH can be osx-64, linux-32, linux-64, win-32 or win-64
	for ARCH in osx-64 linux-32; do
	    conda convert --platform $ARCH $BUILD_DIR/$HOST_ARCH/$PROJECT-$RELEASE-py27_0.tar.bz2 -o $OUTPUT_DIR
	    anaconda upload $OUTPUT_DIR/$ARCH/$PROJECT-$RELEASE-py27_0.tar.bz2
	done

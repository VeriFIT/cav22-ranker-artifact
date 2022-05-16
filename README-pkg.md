Artifact for the CAV'22 submission "Complementing Büchi automata with Ranker" (package version)
===============================================================================================

This file describes the package containing the needed code and tools to
replicate the results in the CAV'22 submission named "Complementing Büchi
automata with Ranker".  The package does not contain the operating system and
the libraries.

1. Requirements
===============
The package has been tested on the following VM image

  * https://doi.org/10.5281/zenodo.2759473

containing Ubuntu 18.04 LTS.  We used one x86_64 core running at 2.30 GHz and
4 GiB of RAM.  It should, however, work also on other systems.

The following extra packages may need to be installed (or similar packages at
the given system):

  * cmake
  * python3-dev
  * maven
  * libboost-dev
  * libboost-regex-dev
  * python3-pip
  * openjdk-17-jre
  * openjdk-17-jdk-headless
  * libjpeg-dev

Furthermore, the following Python packages should also be installed using pip3:

  * psutil
  * termcolor
  * pyyaml
  * tabulate
  * pandas
  * mizani
  * plotnine

2. Preparing
============
We need to prepare the tools first.  The tools are in the pkgs/ directory; they
need to be unpacked, compiled, and copied to ba-compl-eval/bin .

First, move the cav22-ranker-artifact/ directory to $HOME and go to the pkgs/ directory

  $ cd cav22-ranker-artifact/pkgs
  $ export LD_LIBRARY_PATH=$HOME/cav22-ranker-artifact/ba-compl-eval/bin

  (note that the LD_LIBRARY_PATH may need to be set in your ~/.bashrc or a similar file)

  a) GOAL:

     $ unzip GOAL-20200506.zip
     $ cp -r GOAL-20200506 ${LD_LIBRARY_PATH}/goal

  b) Fribourg Construction plugin for GOAL:

     $ unzip ch.unifr.goal.complement.zip
     $ cd ch.unifr.goal.complement
     $ zip -r ch.unifr.goal.complement.zip classes plugin.xml
     $ cp ch.unifr.goal.complement.zip ${LD_LIBRARY_PATH}/goal/plugins
     $ cd ..

  c) Spot:

     $ tar xzf spot-2.9.3.tar.gz
     $ cd spot-2.9.3/
     $ ./configure
     $ make
     $ cp bin/.libs/autfilt ${LD_LIBRARY_PATH}
     $ cp bin/.libs/autcross ${LD_LIBRARY_PATH}
     $ cp spot/.libs/libspot.so.0 ${LD_LIBRARY_PATH}
     $ cp buddy/src/.libs/libbddx.so.0 ${LD_LIBRARY_PATH}
     $ cd ../

  d) Seminator 2:

     $ tar xzvf seminator-2.0.tar.gz
     $ cd seminator-2.0/
     $ export SPOT="${HOME}/cav22-ranker-artifact/pkgs/spot-2.9.3"   # or the path to sources of Spot
     $ ./configure CXXFLAGS="-I${SPOT} -I${SPOT}/buddy/src" LDFLAGS="-L${SPOT}/spot/.libs -L${SPOT}/buddy/src/.libs"
     $ make
     $ cp .libs/seminator ${LD_LIBRARY_PATH}
     $ cp src/.libs/libseminator.so.0 ${LD_LIBRARY_PATH}
     $ cd ..

  e) ROLL:

     $ tar xzvf roll.tar.gz
     $ cd roll-library-dev/
     $ ./build.sh
     $ cp ROLL.jar ${LD_LIBRARY_PATH}
     $ cd ..

  f) LTL2dstar:

     $ tar xzvf ltl2dstar-0.5.4.tar.gz
     $ cd ltl2dstar-0.5.4
     $ mkdir build
     $ cd build
     $ cmake -DCMAKE_BUILD_TYPE=Release ../src
     $ make
     $ cp ltl2dstar ${LD_LIBRARY_PATH}
     $ cd ../..

  g) Ranker:

     $ tar xzvf ranker.tar.gz
     $ cd ranker/src
     $ make
        ... if there is an error, change GCC=g++ to GCC=clang++ in Makefile and run `make` again (without `make clean`)
     $ cp ranker ${LD_LIBRARY_PATH}
     $ cd ../../

  h) Ranker (TACAS'22 version):

     $ tar xzvf ranker-tacas22.tar.gz
     $ cd ranker-tacas22/src
     $ make
        ... if there is an error, change GCC=g++ to GCC=clang++ in Makefile and run `make` again (without `make clean`)
     $ cp ranker ${LD_LIBRARY_PATH}/ranker-tacas22
     $ cd ../../

3. Running experiments
======================
Everything should be set up now so you can follow the instructions in README.md
to perform the evaluation.

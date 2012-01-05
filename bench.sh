#!/bin/bash

# This is a script to benchmark building and packaging firefox
# along with other operations.  It will use a pristine copy of mozilla-central
# which will be cloned each operation to roughly approximate time to clone
# m-c without being impacted by the network

set -xe

DATAFILE=~/bench-data.csv
HG="hg"
MAKE="make"
ECHO="/bin/echo"
MOZCONF="browser/config/mozconfigs/macosx-universal/nightly"
REV=b87861e50640

# This function writes a timestamp to the data file with a trailing comma
t () {
  $ECHO -n "$(date "+%s")," >> $DATAFILE
}

$ECHO Cloning pristine copy of mozilla-central
if [ ! -e pristine ] ; then
  $HG clone -r $REV http://hg.mozilla.org/mozilla-central pristine
else
  # This is just to check that the repository on disk already has the revision we are looking for
  $HG export -R pristine -r $REV > /dev/null
fi

if [ -e $DATAFILE ] ; then
  $ECHO "will not overwrite $DATAFILE"
  exit 1
fi

# Put headers in the datafile since the data file is just a bunch of ints
$ECHO "clonestart,buildstart,packagestart,packagetestsstart,symbolsstart,clobberstart,finished," > $DATAFILE

# Avoid using the default of obj-<autoconf's triplet guess>
export MOZ_OBJDIR='objdir'

# Clean up previous runs to make sure we are doing a clobber build
rm -rf scratch

while true ; do
  t # clonestart
  $HG clone pristine scratch
  # Copy hgrc so we get the default locations, so that
  # make buildsymbols doesn't fail on not finding a URL as
  # the default repo
  cp pristine/.hg/hgrc scratch/.hg/hgrc
  t # buildstart
  pushd scratch >/dev/null
  cp $MOZCONF .mozconfig
  # On lion, there is no 10.5 SDK.  This makes the i386 binary use the 10.6 sdk.
  sed -i -e "s/MacOSX10.5.sdk/MacOSX10.6.sdk/" build/macosx/universal/mozconfig.common
  # On lion with macports, there is a weird error where the buildsymbols step
  # complains about the MAC_DEPLOYMENT_VERSION (or something like that)
  $ECHO "ac_add_options --enable-macos-target=10.7" >> .mozconfig
  sed -i -e "s/-j4/-j8/" .mozconfig
  $MAKE -f client.mk build
  popd > /dev/null # leave topsrcdir
  t # packagestart
  # Need to use the i386 subdir because of how universal builds work
  pushd scratch/$MOZ_OBJDIR/i386
  $MAKE package
  t # packagetestsstart
  $MAKE package-tests
  t # symbolsstart
  $MAKE buildsymbols
  popd # leave objdir
  t # cloberstart
  rm -rf scratch
  t #finished
  $ECHO >> $DATAFILE # This is so data is split across newlines
done




  

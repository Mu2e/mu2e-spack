#
# Define the mapping between Git repos and spack packages
#
# map all the non-trivial translations
declare -A SPACKMAP=(["Production"]="production" ["KinKal"]="kinkal" ["EventNtuple"]="event-ntuple" ["ArtAnalysis"]="art-analysis")
GITREPO=$1
SPACKAGE=${GITREPO}
if [ -v SPACKMAP[$GITREPO] ]; then
  SPACKAGE=${SPACKMAP[${GITREPO}]}
fi
echo $SPACKAGE

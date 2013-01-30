

#baseFileName=$1
baseFileName="wikipediaData/all"
#CV=$2
CV=4  # number of CV - 1
#maxExps=$3
maxExps=$1


for seed in $(seq 1 ${maxExps}); do

  for i in $(seq 0 ${CV}); do
      echo $seed
      echo "$baseFileName ${i}" > fileToLoad
      python -m scoop myGPCompareWiki.py "scoopTest_cxpb08_mutpb01_ngen100_npop400_tsize7_hCreation3_hNew2.result" ${seed}
  done
done

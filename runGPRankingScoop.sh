
fileToLoad="gpRankingPath"
threads=60

#baseFileName=$1
baseFileName="mathData/CV5/input"
#CV=$2
CV=4  # number of CV - 1
#maxExps=$3
maxExps=$1


for seed in $(seq 1 ${maxExps}); do

  for i in $(seq 0 ${CV}); do
      echo $seed
      echo "$baseFileName${i}" > ${fileToLoad}
      python -m scoop -n ${threads} myGPRankingScoop.py "gpRankingMath_cxpb07_mutpb01_ngen200_npop1000_tsize30_hCreation7_hNew2_regulation.result" ${seed}
  done
done

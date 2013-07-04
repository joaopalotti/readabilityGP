
fileToLoad="gpRankingPath"
threads=3

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
      #python -m scoop -n ${threads} myGPRankingScoop.py "scoopTest_cxpb08_mutpb01_ngen100_npop400_tsize7_hCreation3_hNew2.result" ${seed}
      python -m scoop -n ${threads} myGPRankingScoop.py "scoopTest.result" ${seed}
  done
done

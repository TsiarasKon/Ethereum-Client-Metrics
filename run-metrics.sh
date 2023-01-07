#!/bin/bash
# sudo required for nethogs (network metrics by process)
# <program> needs to already be running before run-metrics.sh is run
# if <program> is not showing up on nethogs then no metrics will be printed 
if [[ $# -lt 2 ]]; then 
  echo "Please run like 'sudo ./run-metrics.sh <program> <path_to_chaindata>'"
  exit 1
fi
pid=$(ps -a | grep $1 | awk '{ print $1 }')
# TODO: not all pidstat stats are needed
echo $(pidstat -druIh | grep "Command") "kbps_sent" "kbps_rec" "disk_used"
nethogs -t | while read line; do 
   if ! [[ "$line" == *"$1"* ]]; then
      continue
   fi
   pidstat=$(pidstat -druIh -p $pid -druIh | grep $1)
   kbps_sent=$(awk '{ print $2 }' <<< $line)
   kbps_rec=$(awk '{ print $3 }' <<< $line)
   disk_used=$(du -s $2 2> >(grep -v '^du: cannot \(access\|read\)' >&2) | awk '{ print $1 }')
   echo $pidstat $kbps_sent $kbps_rec $disk_used
done

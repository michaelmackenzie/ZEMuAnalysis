#! /bin/bash

resubmit=false
getoutput=false
year=2016

if [[ "$1" != "" ]]
then
    resubmit=true
fi

if [[ "$2" != "" ]]
then
    getoutput=true
fi

if [[ "$3" != "" ]]
then
    year=$3
fi

jobdir=crab_projects/samples_*_${year}/*LFVAnalysis*
if [[ "$4" != "" ]]
then
    jobdir=crab_projects/samples_$4_${year}/*LFVAnalysis*
fi

resubmitCommand="crab resubmit -d "
if [[ "$5" != "" ]]
then
    resubmitCommand="crab resubmit --maxjobruntime $5 -d "
fi
echo "Parameters are: resubmit=${resubmit}, getoutput=${getoutput}, year=${year}, and dir=${jobdir} with resubmitCommand=${resubmitCommand}"


numJobs=$(ls -d ${jobdir} | wc | awk '{print $1}')

if [ $numJobs != 0 ]
then
    for f in `ls -d ${jobdir}`
    do echo Looking at ${f}
       crab status -d $f | grep --color=always 'Looking\|failed\|running\|finished\|transferring\|idle\|toRetry\|held\|killed' |\
	   awk -v doResubmit=${resubmit} -v resub="${resubmitCommand}" -v doGetOutput=${getoutput} -v fin=$f '{
        print $0
        if(doResubmit != "false" && NF < 8 && /failed/) d=1
	else if(doGetOutput != "false" && NF<8 && /finished/ && /100.0%/) ad=1
       }
       END{
        if(d == 1) {
	 system("echo "resub""fin)
	 system(resub""fin)
	} else if(ad == 1) {
	 system("echo crab getoutput -d "fin)
	 system("crab getoutput -d "fin)
	 system("echo rename LFVAnalysis LFVDONE "fin)
	 system("rename LFVAnalysis LFVDONE "fin)
	}
       }'
    done
else
    echo "No jobs to check..."
fi

numJobsLeft=$(ls -d ${jobdir} | wc | awk '{print $1}')
echo "Finished! Checked ${numJobs} jobs, ${numJobsLeft} are left to run"

import sys
import os
from optparse import OptionParser

MYDIR=os.getcwd()

#get inputs
from optparse import OptionParser

usage = "usage: python %prog [options] arg"
parser=OptionParser(usage=usage)
parser.add_option("-q","--flavour",dest="jobFlavour",type="str",default="longlunch",help="job FLAVOUR",metavar="FLAVOUR")
parser.add_option("-p","--proxy",dest="proxyPath",type="str",default="noproxy",help="Proxy path")
parser.add_option("-n","--nFiles",dest="nFiles",type="str",default="-1",help="nFiles")

opts, args = parser.parse_args()


help_text = '\npython makejobs.py <jobName> <CMSSWrel> <filelist> -p <proxyPath> -n <nFiles> -q <jobFlavour> \n'
help_text += '\n<cfgFileName> (mandatory) = name of your configuration file (e.g. hlt_config.py)'
help_text += '\n<jobName> (mandatory) = name of the job (eg. Jobs_test)'
help_text += '\n<CMSSWrel> (mandatory) = directory where the top of a CMSSW release is located (eg. $CMSSW_BASE)'
help_text += '\n<filelist> (mandatory) = name of the text file which contains a list of sample root files'
help_text += '\n<proxyPath> (optional) = location of your voms cms proxy (needed if accessing non local files). Note: keep your proxy in a private directory.'
help_text += '\n<nFiles> (optional) = number of files to run over (1 file per job); Default: -1 (all files)'
help_text += '\n<flavour> (optional) = job flavour; Default : longlunch\n'


if len(sys.argv) < 4 : 
	sys.exit("Error: Too few arguments! Usage : \n"+help_text)

hltConfig = open ("hltGetConfiguration.py")
hltGetConfiglines = hltConfig.readlines()
hltGetConfig = ''
for line in hltGetConfiglines :
	line = line.rstrip()
	if "#" in line : continue
	if not len(line) : continue
	hltGetConfig = line
	
print hltGetConfig

if not "hltGetConfiguration.py" not in hltGetConfig : sys.exit("Error: Invalid hltGetConfiguration command in hltGetConfiguration.py")

filename = sys.argv[3]
signalfile = open(filename)
lines = signalfile.readlines()

cmsEnv = sys.argv[2] + '/src'
jobName = sys.argv[1]
k = 0

nFiles = int(opts.nFiles)
nJobs = len(lines) if nFiles == -1 else nFiles

if nJobs == 0 : sys.exit("No jobs made")
elif nJobs <-1 : sys.exit("Error : Invalid number of jobs! No jobs made")
elif nJobs > len(lines) :
	nJobs = len(lines) 
	print "Only {} files in {}\n".format(nJobs, filename)

for line in lines :
	line = line.rstrip()
	jobDir = jobName+"/Job_%s"%str(k)
	os.system("mkdir -p "+jobDir)
	jobFile = jobDir+"/job_%s.sh"%str(k)
	outputfile = open(jobFile,"w") 
	outputfile.write('#!/bin/sh\n')
	outputfile.write("export X509_USER_PROXY=$1\n")
        outputfile.write("voms-proxy-info -all\n")
        outputfile.write("voms-proxy-info -all -file $1\n")
	outputfile.write("ulimit -v 5000000\n")
	outputfile.write("cd %s\n"%(cmsEnv))
	outputfile.write("eval `scramv1 runtime -sh`\n")
	outputfile.write('cd $TMPDIR\n')
	outputfile.write(hltGetConfig+" --input "+line+" > hlt.py\n")
	outputfile.write('cmsRun hlt.py\n')
	outputfile.close()
	k+=1
	print "Making job file : (%d/%d)"%(k,nJobs)
	if k == nFiles : break

condor_str = 'executable = $(filename)\n'
if opts.proxyPath != "noproxy":
    condor_str += "Proxy_path = %s\n"%opts.proxyPath
    condor_str += "arguments = $(Proxy_path) $Fp(filename) $(ClusterID) $(ProcId)\n"
else:
    condor_str += "arguments = $Fp(filename) $(ClusterID) $(ProcId)\n"
condor_str += 'output = $Fp(filename)hlt.stdout\n'
condor_str += 'error = $Fp(filename)hlt.stderr\n'
condor_str += 'log = $Fp(filename)hlt.log\n'
condor_str += '+JobFlavour = "%s"\n'%opts.jobFlavour
condor_str += 'queue filename matching ('+MYDIR+"/"+jobName+'/Job_*/*.sh)'

condor_sub = open('condor_cluster.sub','w')
condor_sub.write(condor_str)
condor_sub.close()

subjob = open ('sub_total.jobb', 'w')
subjob.write("condor_submit "+MYDIR+"/condor_cluster.sub\n")
os.system("chmod +x sub_total.jobb")

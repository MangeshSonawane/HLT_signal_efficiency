# HLT_signal_efficiency
Scripts to run and calculate signal efficiencies for a given HLT_menu.

There are two main scripts : makejobs.py and mergeEffs.py
Supporting files are : hltGetConfiguration.py, HLTpaths.py and sample.list

1. makefile.py essentially takes your hltGetConfiguration command, uses it to obtain an hlt configuration file, and cmsRun's it on condor. It does this over all files provided in the sample list, or a subset.

Usage : $ python makefile.py <jobName> <CMSSWrel> <filelist> -p <proxyPath> -n <nFiles> -q <jobFlavour>

 <cfgFileName> (mandatory) = name of your configuration file (e.g. hlt_config.py)
 <jobName> (mandatory)     = name of the job (eg. Job_signal_V5)
 <CMSSWrel> (mandatory)    = directory where the top of a CMSSW release is located (eg. $CMSSW_BASE)
 <filelist> (mandatory)    = name of the text file which contains a list of sample root files
 <proxyPath> (optional)    = location of your voms cms proxy (needed if accessing non local files). Note: keep your proxy in a private directory.
 <nFiles> (optional)       = number of files to run over (1 file per job); Default: -1 (all files)
 <flavour> (optional)      = job flavour ; Default: longlunch
   
To create filelist, you can use :
 $ dasgoclient --query 'file dataset=<name of dataset>' > sample.list
   
Example : 
   $ python makejobs.py Jobs_test $CMSSW_BASE sample.list -p /afs/cern.ch/user/<u>/<user>/private/.proxy -q longlunch
   $ ./sub_total.jobb
   
2. mergeEffs.py parses the resulting output of cmsRun, and gathers the total number of events run over, the total number of events passing the menu, the number of events passing each path, and the corresponding efficiencies. It also can give the L1 efficiencies of events passing the L1 filters in each path. The path and L1 filter names must be input into HLTpaths.py
   
Usage : $ python  mergeEffs.py <jobName>
   
   <jobName> : Name of the job submitted to makejobs.py

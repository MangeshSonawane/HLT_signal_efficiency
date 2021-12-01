import os
import sys
from HLTpaths import HLTpathsList, L1FiltersList

HLTpaths = {}
L1filters = {}

maxlen = max([len(string) for string in HLTpathsList+L1FiltersList])

for path in HLTpathsList :
	HLTpaths[path] = 0

for L1filter in L1FiltersList :
	L1filters[L1filter] = 0

Total = 0
Passed = 0

MYDIR = os.getcwd()

helpstr = '\nUsage : python mergeEffs.py <jobName>\n'
helpstr += '\n<jobName> : Name of the job submitted to makejobs.py\n'

if len(sys.argv) != 2 : sys.exit("Error : Too few options\n"+helpstr)

jobName = sys.argv[1] 
jobDir = MYDIR+'/'+jobName

flags ={}

for i in range(90) :

	filename = jobDir+'/Job_%s/hlt.stderr'%str(i)
	if not os.path.exists(filename) : 
		continue
#	os.system("echo "+filename)
	hltout = open(filename)
	lines = hltout.readlines()
#	cond = False
	for l in L1filters :
		flags[l] = True

	for line in lines :
		line = line.rstrip()
		if not "TrigReport" in line : continue

#		print line
	
		for h in HLTpaths :		
			if h in line and "Modules in Path" not in line:
				chunks = line.split()
				HLTpaths[h] +=int(chunks[4])

		for l in L1filters :
			if l in line and flags[l] :
				chunks = line.split()
				if l != chunks[-1] : continue
				flags[l] = False
				L1filters[l]+= int(chunks[4])
	
		if 'passed' in line :
			chunks = line.split()
			Total += int(chunks[4])
			Passed += int(chunks[7])
			print i, chunks[4]

print 
print "Total events ; {}".format(Total)
print "Passed events; {} ;\t{}".format(Passed, float(Passed)/Total)
print

for l in L1filters :
	print"{} ; {:6} ;\t{:.3f}" .format(l.ljust(maxlen+4),L1filters[l],float(L1filters[l])/Total)
print

for path in HLTpaths :
	print "{} ; {:6} ;\t{:.3f}" .format(path.ljust(maxlen+4),HLTpaths[path],float(HLTpaths[path])/Total)
print

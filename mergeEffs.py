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

for jobN in os.listdir(jobDir) :

	filename = jobDir+'/'+jobN+'/hlt.stderr'
	if not os.path.exists(filename) : 
		print filename, " does not exist"
		continue
#	os.system("echo "+filename)
	hltout = open(filename)
	lines = hltout.readlines()

	for l in L1filters :
		flags[l] = True

	passed = False
	for line in lines :
		line = line.rstrip()
		if not "TrigReport" in line : continue

#		print line
#		if "End" in line : break
#		else : continue
	
		for h in HLTpaths :		
			if h in line and "Modules in Path" not in line:
				chunks = line.split()
				try : HLTpaths[h] +=int(chunks[4])
				except : continue

		for l in L1filters :
			if l in line and flags[l] :
				chunks = line.split()
				if l != chunks[-1] : continue
				flags[l] = False
				L1filters[l]+= int(chunks[4])
	
		if 'passed' in line :
			passed = True
			chunks = line.split()
			Total += int(chunks[4])
			Passed += int(chunks[7])
#			print jobN, chunks[4]
	if not passed :
		print jobN

#print 
print "{}  {:6}".format("Total events".ljust(maxlen+4), Total)
print "{}  {:6} \t{:.3f}".format("Passed events".ljust(maxlen+4), Passed, float(Passed)/Total)
print "{}  \t{:.3f}".format("Passed events".ljust(maxlen+4), float(Passed)/Total)
print

for l in L1filters :
#	print"{}  {:6} \t{:.3f}" .format(l.ljust(maxlen+4),L1filters[l],float(L1filters[l])/Total)
	print"{}  \t{:.3f}" .format(l.ljust(maxlen+4),float(L1filters[l])/Total)

for path in HLTpathsList :
#	print "{}  {:6} \t{:.3f}" .format(path.ljust(maxlen+4),HLTpaths[path],float(HLTpaths[path])/Total)
	print "{}  \t{:.3f}" .format(path.ljust(maxlen+4),float(HLTpaths[path])/Total)

print

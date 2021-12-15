inputfile = open("paths.list")

lines = inputfile.readlines()

print "HLTpathsList = ["
for line in lines :
	line = line.rstrip()
	line = line[:-1]
	print "\t'" + line + "',"
print "]\n"

print "L1FiltersList = ["
print "]"

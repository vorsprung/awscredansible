import sys

class AWScre(object):

    def __init__(self, inpath, outpath, account='default'):
        self.account = "[{}]".format(account)
        self.inpath = inpath
        self.outpath = outpath

    def ConvertLine(self,line):
        s = line.split(" = ")
        return("  {}: {}".format(s[0].upper(), s[-1]))
    
    def ValidateLine(self, line):
        try:
          line.index(" = ")
          return True
        except ValueError:
          return False
    
    def LoadLines(self, fh):
        ret = []
        for line in fh:
            if line.startswith(self.account):
                break
        for line in fh:
            if line == "\n" or line == '':
                return ret
            if not self.ValidateLine(line):
                print("bailing due to invalid line {}".format(line))
                return []
            ret.append(self.ConvertLine(line))

        return ret
    def ExtraAnsibleLines(self):
	    return [
		"---\n",
		"env_vars:\n",
		"  ANSIBLE_BECOME_FLAGS: '-H -S -n -E'\n"]
    
    def ReadProcessWrite(self):
        try:
            infile = open(self.inpath,"r")
            processed = self.LoadLines(infile)
            if len(processed) > 0:
                outfile = open(self.outpath, "w")
                outfile.writelines(self.ExtraAnsibleLines())
                outfile.writelines(processed)
 
        except Exception as e:
            print(e)

if __name__ == '__main__':
    args = sys.argv
    if len(args) <2:
        print("usage {} infile outfile account".format(sys.argv[0]))
    x = AWScre(*args[1:])
    x.ReadProcessWrite()

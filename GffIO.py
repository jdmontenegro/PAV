import re
import Feature

class GffIO:
    
    """ Creates a parser to read gff files and iterate feature by feature """
    def __init__(self, gff):
        """ On initialization a file is converted into a file handle """
        self.handle = open(gff, 'r')
        self.version = self.handle.readline().lstrip('#').rstrip()
        self.header = []
        while True:
            prev = self.handle.tell()
            line = self.handle.readline().rstrip()
            if line.startswith('#'):
                self.header.append(line.lstrip('#').rstrip())
            else:
                self.handle.seek(prev)
                break

    def __ParseInfo(self, inf):
        l = re.split(';|=', inf)
        try:
            len(l)%2 == 0
        except ValueError:
            print("Not enough information in INFO field. Malformed gff?")
        info={}
        for i in range(int(len(l)/2)):
            c=i*2
            info[l[c]] = l[c+1]
        return(info)

    def nextFeat(self):
        while True:
            line = self.handle.readline().rstrip()
            if not line:
                break
            f = line.split("\t")
            info = self.__ParseInfo(f[8])
            keys=['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase']
            feat = Feature.Feature({**dict(zip(keys, f[0:7])), **info})
            yield feat

    def nextGene(self):
        """ Loops through the handle and returns the next feature with subfeatures """
        current = None
        for feat in self.nextFeat():
            if not current  and feat.type != "gene":
                continue
            elif not current and feat.type == "gene":
                current = feat
            elif feat.type == "gene" and current:
                yield current
                current = feat
            else:
                current.addChild(feat)
        yield current
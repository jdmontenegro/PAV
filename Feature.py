### TODO
### 1. Add multiple level pretty print for subfeatures

class Feature:

    # This initialization will allow for instances with a minimum set of attributes
    # but that can contain additional attributes.
    def __init__(self, atts={}):
        # Create default minimum set attributes
        default = { 'seqid' : '', 'source' : '', 'type' : '', 'start' : int, \
                 'end' : int, 'score' : '.', 'strand' : '+', 'phase' : '', \
                 'ID' : '', 'subfeat' : [] }
        # Override the dafult values depending on the list given by user
        for key in atts.keys():
            default[key] = atts[key]
        # Override the namespace of the instance
        self.__dict__ = default
        if len(self.subfeat) >= 1:
            self.addChild(self.subfeat)

    def __repr__(self):
        line=''
        for k in self.__dict__.keys():
            line += str(k) + "\t->\t" + str(self.__dict__[k]) + "\n"
        return(line)

    # Just a way to check the contents of the Object
    def pprint (self, line=''):
        if line == '':
            line=self.ID+"\n"
        else:
            line+="\t"+self.ID+"\n\t"
        if len(self.subfeat) == 0:
        	print(line)
        else:
            for i in self.subfeat:
                (i.pprint(line))

    def addChild (self, *feats):
        for feat in feats:
            # First check the subfeature is of Class Feature 
            if not isinstance(feat, Feature):
                return("Cannot add feature as child. feature is not an instance of Feature class")
            elif not feat.Parent:
                return()
            # Now check that this is actually a Parent - Child relationship
            elif feat.Parent == self.ID:
                self.subfeat.append(feat)
            else:
                if not self.subfeat:
                    return("Cannot add feature, no relationship found between Parent and child")
                # Try adding to every subfeature in the amin feature
                for child in self.subfeat:
                    child.addChild(feat)

    def extractCoords(self, feat, coords={}):
        if not coords:
            coords={'starts':[], 'ends':[]}
        if self.type == feat:
            coords['starts'].append(self.start)
            coords['ends'].append(self.end)
        elif len(self.subfeat) == 0:
            return(coords)
        else:
            for subfeat in self.subfeat:
                subfeat.extractCoords(feat, coords)
        return(coords)
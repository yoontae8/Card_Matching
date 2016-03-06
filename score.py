from operator import itemgetter

class Score :
    def __init__(self, scfile) :
        self.scfile = scfile

        
        rhandle = open(self.scfile, 'r')

        flist = rhandle.readlines()
        
        rhandle.close()

        self.slist = list()

        #saves the list of username and score in the slist
        for item in flist :
            self.slist.append((item.split(':')[0], int(item.split(':')[1])))

    # get username and score, and sort it by reverse order of the score, and return
    def getslist(self, username, score) :
        self.slist.append((username, score))
        self.slist = sorted(self.slist, key = itemgetter(1), reverse = True)
        self.slist = self.slist[:10] # maintain only 10 scores
        self.writeslist()
        return self.slist

    def writeslist(self) :
        whandle = open('score.txt', 'w')

        for item in self.slist :
            whandle.write(item[0] + ':' + str(item[1]) + '\n')

        whandle.close()

    def deleteAll(self) :
        dhandle = open('score.txt', 'w')
        dhandle.close()

###############################################################################
###########################     errorHandler:    ##############################
###############################################################################
##Habib Ollah Boloorchi Tabrizi
# Course : Design and implementation of operating system
# Course number :20957
# main project of Operating system phase 1
#3/2/2018
# Variable Description: the most important variables are clock PC IR  which are in class of cpu
##    This programs contains 4 classes and 34 methods that simulate an operating system
#the Loader fetch data from a file line by line without any preprocess and pu it in memory as container give the data
# the program CPU routine do the main job about each function
#The Memory is concsise to exact memory that we had to in each tim memory routin can just fetch one 16 bit of data and
# put in instruction register.
# the main is 2 line to just ask CPU to start and cpu will command to loader and memory routin
# the Page map table is static for program input and output and the page will be -1 to show its emprt or null for
# resspecting error

import sys


class errorHandler:
    def __init__(self):
        self.No = 0
        self.Report =''

    def num(self, numberOfError,p):
        ecpu= CPU()
        edisk = Disk()
        ememory=Memory()
        pcb = PCB()



        if numberOfError == 1:
            self.Report ='error number 1 : instruction is too long'

        if numberOfError == 2:
            self.Report='error number 2 : stack is empty'
            self.forspooling(p)
        if numberOfError == 3:
            self.Report ='error number 3 : stack is full'
            self.forspooling(p)

        if numberOfError == 4:
            self.Report ='error number4 : devided to 0'
            self.forspooling(p)
        if numberOfError == 5:
            self.Report ='error number5 : infinit loop'
            self.forspooling(p)
        if numberOfError == 6:
            self.Report ='error number6 : input is too long'
            self.forspooling(p)
        if numberOfError == 7:
            self.Report ='error number7 : the input is not began with **JOB'
            self.forspooling(p)
        if numberOfError == 8:
            self.Report ='error number 8: bad input'
            self.forspooling(p)
        if numberOfError == 9:
            self.Report ='error number 9: more than one **input'
            self.forspooling(p)
        if numberOfError == 10:
            self.Report ='error number 10: missed **JOB'
            self.forspooling(p)
        if numberOfError == 11:
            self.Report ='error number 11: missing loader format'
            self.forspooling(p)
        if numberOfError == 12:
            self.Report ='error number 12: missing **FIN'
            self.forspooling(p)
        if numberOfError == 13:
            self.Report ='error number 13: input conflict'
            self.forspooling(p)
        if numberOfError == 14:
            self.Report ='error number 14: '
            self.forspooling(p)
        if numberOfError == 15:
            self.Report ='error number 15: reading beyond end of file'
            self.forspooling(p)
        if numberOfError == 16:
            self.Report ='error number 16: writing beyond end of file'
            self.forspooling(p)
    def forspooling(self,p):
        p.write('jobId =1')
        p.write("\n")
        p.write(self.Report)
        p.write("\n")
        p.write('the program terminated abnormally')
        exit(0)
#############################################################################
#############################     Disk    ##################################
###############################################################################
class Disk:
    def __init__(self):
        self.Pages = {}
        self.metaData = {}
        self.beginjobID={} # the index is jobid the content is number of the beginning in disk
    def DiskReady(self):
        for i in range(0,255):
            self.pages[i]= {}
            self.metaData[i] ={0}
###############################################################################
##############################     Memory    ##################################
###############################################################################
class Memory:
    def __init__(self):
        self.data = []
        self.frame = {}
        self.metaData = {}
        self.reserved ={}#if it is busy by others -1 if it is for ourjob 0


    def DATA(self, B):
        self.data = B
    def full_but6(self): # for test
        for i in range (0,32):
            if i == 5  or i== 8 or i == 10 or i==17 or i==20 or i==31:
                self.reserved[i]= 0
                self.frame[i]={}
            else:
                self.reserved[i] = -1

    def memory_routin(self):
        self.full_but6()

###############################################################################
#############################      loader      ################################
###############################################################################
class Loader:
    def __init__(self):
        self.lines = []
        self.binlines = []  ##binarylines for Memory
        self.lst = []  ##1st line of file for sending to CPU
        self.JobID = "A"
        self.LoadAddress = "A"
        self.initPC = "A"
        self.size = "A"
        self.traceflag = "A"
        self.pageframe = []
        self.memoryresereves = {}
        self.inputnum='00' #it shows how many input we have
        self.outputnum='00'#it shows how many output we have
        self.inputlines = {}
        self.input = []
        self.isegbegin =0
        self.osegbegin =0
        self.outputpagesnumbers =[]

        self.inputpagesnumbers = []

    def pagenum(self,pc):
        return int(pc/8)

    def reserved(self, r= {}):
        counter =0
        reserved = {}
        for i in range(0,32):
            if counter <6 and r[i]==0 :
                reserved[counter]=i
                counter += 1
        return reserved


    def pcIneach(self,pc):# it give us thenumber of Ir in our page
        return (pc % 8)


    def inputSpooling(self, pageframes, begin ,end,disk={}):

        self.isegbegin = int(end/2)
        self.osegbegin =int(end/2) +int( int(self.inputnum,16)/8) + 1
        if (end/2)%2==1:
            F = int(end/2)
        else:
            F=int(end / 2) +1


        for i in range(begin,F):

            disk[i] = pageframes[i][:]

        for i in range(F,F +int( int(self.inputnum,16)/8) + 1):
            self.inputpagesnumbers.append(i)
            disk[i]=self.input[i-F]
        #create input pages
        for i in range(int(end/2) +int( int(self.inputnum,16)/8) + 2,
                        int(end / 2) + int(int(self.inputnum, 16) / 8) + 1+int(int(self.outputnum,16)/8 + 2)):
            self.outputpagesnumbers.append(i)
            disk[i]=['0000000000000000','0000000000000000','0000000000000000','0000000000000000'
                     ,'0000000000000000','0000000000000000','0000000000000000','0000000000000000']

        #create output pages
        return disk

    def getlines(self, file,disk,memory,p):
        error = errorHandler()
        self.file = file
        self.lines = tuple(open(self.file, 'r'))
        self.lines = [i.replace('\n', '') for i in self.lines]

        ioline = str.split(self.lines[0], " ")
        del self.lines[0];

        J,self.inputnum,self.outputnum =  ioline

        if J != '**JOB':
            error.num(7,p)
        if self.lines[-1] != '**FIN':
            error.num(12)
        del self.lines[-1];

        ##############################################################input lines

        for i in range(int(int(self.inputnum,16)/4)+1,0,-1):#

            self.inputlines[-i+1] = self.lines[-i]

            del self.lines[-i]

        for i in range(0,int(int(self.inputnum,16)/4)+1):

            n = 4
            self.input.append(str(bin(int(self.inputlines[i], 16))[2:].zfill(16)))

        # ##################################################################

        if self.lines[-1] != '**INPUT':
            error.num(7,p)

        del self.lines[-1];


        #######put first line in cpu    
        self.lst = str.split(self.lines[0], " ")

        self.JobID, self.LoadAddress, self.initPC, self.size, self.traceflag = self.lst
        #######put data in Disk

        del self.lines[0];

        h=0
        for line in self.lines:
            n = 4
            t = [line[i:i + n] for i in range(0, len(line), n)]
            h+=1
            for s in t:
                self.binlines.append(str(bin(int(s, 16))[2:].zfill(16)))
##########################################3333

        counter =0
        Pnumber = 0
        counter = 0
        ptemp = []
        pageframe = []
        temp = []

        disk.beginjobID[self.JobID] = 0 # for next phase I need to have the beginning of job Id
        for i in self.binlines[::8]:

            ptemp=self.binlines[counter *8 : counter *8 +8]
            pageframe.append(ptemp)
            counter += 1
        # ptemp=self.inputer
        # pageframe.append(ptemp)
        a=0



        disk.Pages=self.inputSpooling(pageframe,a,h)

        memory.full_but6()

        self.memoryresereves=self.reserved(memory.reserved)









############################################################Prepare Disk

###############################################################################
#############################      PCB     ####################################
###############################################################################
##########################################################################
class PCB:
    def __init__(self):
        self.jobID=0
        self.abstractpmt = {0: {'page': -1, 'frame': -1, 'ref': 0, 'dirtybit': 0, 'null': 1},
                    1: {'page': -1, 'frame': -1, 'ref': 0, 'dirtybit': 0, 'null': 1},
                    2: {'page': -1, 'frame': -1, 'ref': 0, 'dirtybit': 0, 'null': 1},
                    3: {'page': -1, 'frame': -1, 'ref': 0, 'dirtybit': 0, 'null': 1},
                    4: {'page': -1, 'frame': -1, 'ref': 0, 'dirtybit': 0, 'null': 1},
                    5: {'page': -1, 'frame': -1, 'ref': 0, 'dirtybit': 0, 'null': 1},
                    }
        #PMT = {index :[pagenumber (Disk) ,frame number(in memory) ,refrence,Dirtybit]
        self.pmt={0: {'page': -1,'frame':  -1 ,'ref': 0, 'dirtybit': 0, 'null' :1},
                  1: {'page': -1,'frame':  -1 ,'ref': 0, 'dirtybit': 0, 'null' :1},
                  2: {'page': -1,'frame':  -1 ,'ref': 0, 'dirtybit': 0, 'null' :1},
                  3: {'page': -1,'frame':  -1 ,'ref': 0, 'dirtybit': 0, 'null' :1},
                  4: {'page': -1,'frame':  -1 ,'ref': 0, 'dirtybit': 0, 'null' :1},
                  5: {'page': -1,'frame':  -1 ,'ref': 0, 'dirtybit': 0, 'null' :1},
                  }
        self.ipmt={}
        self.opmt={}
        self.fmbv ={}
        self.pageframe1=0
        self.pageframe2 = 0
        self.pageframe3 = 0
        self.pageframe4 = 0
        self.pageframe5 = 0
        self.pageframe6 = 0
    def segfault(self,inseg=0,outseg=0):
        if inseg==1:
            self.ipmt={0: {'page': -1, 'frame': self.fmbv[0], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    1: {'page': -1, 'frame': self.fmbv[1], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    2: {'page': -1, 'frame': self.fmbv[2], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    3: {'page': -1, 'frame': self.fmbv[3], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    4: {'page': -1, 'frame': self.fmbv[4], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    5: {'page': -1, 'frame': self.fmbv[5], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    }
        elif outseg==1:
            self.opmt={0: {'page': -1, 'frame': self.fmbv[0], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    1: {'page': -1, 'frame': self.fmbv[1], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    2: {'page': -1, 'frame': self.fmbv[2], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    3: {'page': -1, 'frame': self.fmbv[3], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    4: {'page': -1, 'frame': self.fmbv[4], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    5: {'page': -1, 'frame': self.fmbv[5], 'ref': 0, 'dirtybit': 0, 'null': 1},
                    }
    def pageframereserved(self):
        self.fmbv[0] = self.pmt[0]['frame']
        self.fmbv[1] = self.pmt[1]['frame']
        self.fmbv[2] = self.pmt[2]['frame']
        self.fmbv[3] = self.pmt[3]['frame']
        self.fmbv[4] = self.pmt[4]['frame']
        self.fmbv[5] = self.pmt[5]['frame']
###############################################################################
#############################      CPU     ####################################
###############################################################################
##########################################################################
class CPU:
    def __init__(self):
        self.JobID =0
        self.trace = 0
        self.tos = 0
        self.s = []  ####stack
        self.instructionType = 0
        self.EA = 0
        self.clock = 0
        self.vtu = 0
        self.PC = 0
        self.IR = '0000000000000000'
        self.memEA ='0000000000000000'
        self.warn =0
        self.error = 0
        self.runtime=0
        self.exectime =0
        self.iotime =0
        self.out = 0
        self.hitpoint = 0
        self.hitindex = 0
        self.currentframe=0
        self.pagefault=0
        self.pageindex=0
        self.readCounter =0
        self.writeCounter =0
        self.beginofinput =0 # input segment begining
        self.beginofoutput = 0 #output segment begins
        self.victimframe =0
        self.fmbv = []
        self.inputnum=0
        self.ouputnum=0
        self.pagefaultnumerator =0
        self.segfaultnumerator =0

##########################################################################################################
##########################################outputspooling#####################################################
    def outputspooling(self,disk,memory,pcb,p, errornumber=0):
        p.write("\n")
        # a
        p.write("********************************************************************")
        p.write("*******************************output*************************************")
        p.write("********************************************************************")
        p.write("\n")

        p.write("JobID(DEC) = ")
        p.write(str(self.JobID))
        p.write("\n")
        p.write(" JobID : " )
        p.write(str(self.JobID))
        p.write("\n")
        p.write(" input Data Segment (DEC) : ")
        for i in range(self.beginofinput,self.beginofinput+self.inputnum):
            p.write(str(self.toint(disk.Pages[i])))
        p.write("\n")

        p.write(str(self.JobID))

        p.write(" output Data Segment (DEC) : ")
        p.write(str(self.ouputnum))
        p.write("\n")
        for i in range(self.beginofoutput,self.beginofoutput+int(self.ouputnum/8)+1):
            for j in range(0, self.ouputnum):
                p.write(str(self.toint(disk.Pages[i][j])))

        p.write("\n")


        # e
        if errornumber==0 :
            p.write("termination was normal")
            p.write("\n")
        else:
            p.write("termination was abnormal")
            p.write("\n")

        # f
        p.write("clock Value at termination (hex):")
        p.write(str(hex(self.clock)))
        p.write("\n")
        # g
        p.write("Runtime (DEC) :")
        p.write(str(self.clock))
        p.write("\n")
        p.write("execution time (HEX):")
        p.write("\n")

        p.write("runtime value = ")
        p.write(str(hex(self.clock) + "\n"))
        p.write("\n")
        p.write("Input output time value = ")
        p.write(str(self.iotime) )
        p.write("\n")
        self.exectime = self.clock - self.iotime
        p.write("execution time value = ")
        p.write(str(self.exectime) )
        p.write("\n")
        p.write("Pagefault time(DEC)")
        p.write(str(self.pagefaultnumerator))
        p.write("\n")
        p.write("segmentation fault time(DEC):")
        p.write(str(self.segfaultnumerator))
        p.write("\n")

        # h
        unused_frames=0
        p.write("Memory Utilization:")
        p.write("\n")
        p.write("ratio of pages = ")
        index=[]
        for i in range (0,32):
            if memory.reserved[i]==-1:

                unused_frames +=1
            else:
                index.append(i)

        #
        # print(memory.reserved )
        p.write(str(int(32-unused_frames)))
        p.write("/")
        p.write(str(32))
        p.write("\n")
        p.write("percentage of words")
        p.write(str(int(100*(32-unused_frames)/32)))
        p.write("%")
        p.write("\n")


        p.write("ratio of words.")

        wordcounter =0

        ocounter=0
        p.write(str(wordcounter+self.ouputnum))

        p.write("/")
        p.write("256")
        p.write("\n")
        # i
        p.write("Disk utilization")
        p.write("\n")
        p.write("ratio of pages =")
        pagecounter = 0
        for i in disk.Pages:
            pagecounter+=1
        p.write(str(pagecounter))

        p.write("/")
        p.write(str(256))
        p.write("\n")
        p.write("percentage of words = ")
        p.write(str(int(100 *pagecounter / 256 )))
        p.write("%")
        p.write("\n")

        p.write("memory fragmentation (DEC):")
        mfrag =0
        mfrag +=4

        mfrag += 8 - self.inputnum
        mfrag += 8- self.ouputnum
        p.write(str(int(mfrag/3)))
        p.write("  words( acerage of 3 segments")
        p.write("\n")
        p.write("disk fragmentation (DEC):")
        mfrag = 0
        mfrag += 4
        mfrag += 8 - self.inputnum +1
        mfrag += 8 - self.ouputnum +1
        p.write(str(int(mfrag / 3)))
        p.write("  words( acerage of 3 segments")





















        #########################################################################################################
###########################################Page Fault Handler###########################################
    def oreplacement(self,pagenumber,pcb,hitindex,disk ,memory):
        if pcb.opmt[hitindex]['dirtybit']==0:
            pcb.opmt[hitindex]['page'] = pagenumber
            memory.frame[pcb.opmt[hitindex]['frame']]=disk.Pages[pagenumber]
            return hitindex
        else:#it update disk if the dirty bit is not 0
            disk[pcb.opmt[hitindex]['page']]= memory.frame[pcb.opmt[hitindex]['frame']]
            pcb.opmt[hitindex]['page'] = pagenumber
            memory.frame[pcb.opmt[hitindex]['frame']] = disk.Pages[pagenumber]
            return hitindex
    def ireplacement(self,pagenumber,pcb,hitindex,disk ,memory):
        if pcb.ipmt[hitindex]['dirtybit']==0:
            pcb.ipmt[hitindex]['page'] = pagenumber
            memory.frame[pcb.ipmt[hitindex]['frame']]=disk.Pages[pagenumber]
            return hitindex
        else:#it update disk if the dirty bit is not 0
            disk[pcb.ipmt[hitindex]['page']]= memory.frame[pcb.ipmt[hitindex]['frame']]
            pcb.ipmt[hitindex]['page'] = pagenumber
            memory.frame[pcb.ipmt[hitindex]['frame']] = disk.Pages[pagenumber]
            return hitindex



    def replacement(self,pagenumber,pcb,hitindex,disk ,memory):
        if pcb.pmt[hitindex]['dirtybit']==0:
            pcb.pmt[hitindex]['page'] = pagenumber
            memory.frame[pcb.pmt[hitindex]['frame']]=disk.Pages[pagenumber]
            return hitindex
        else:#it update disk if the dirty bit is not 0
            disk[pmt[hitindex]['page']]= memory.frame[pcb.pmt[hitindex]['frame']]
            pcb.pmt[hitindex]['page'] = pagenumber
            memory.frame[pcb.pmt[hitindex]['frame']] = disk.Pages[pagenumber]
            return hitindex





    def PageFaultHandler(self,pc,pcb,disk,memory, segment = 0):
        self.pagefaultnumerator +=10
        self.clock +=1
        replacedindex =0


        if segment==0:

            v=1
            pagenumber =int( pc / 8)
            while v==1 :

                if pcb.pmt[self.hitindex]['ref'] == 0 :#check refrences of each row of pmt
                    pcb.pmt[self.hitindex]['ref']=1
                    replacedindex= self.replacement(pagenumber,pcb ,self.hitindex,disk,memory)
                    if self.hitindex<5:
                        self.hitindex +=1
                    else:
                        self.hitindex =0
                    break
                else:
                    pcb.pmt[self.hitindex]['ref'] = 0

                    if self.hitindex < 5:
                        self.hitindex += 1
                    else:
                        self.hitindex = 0
            self.victimframe=pcb.pmt[replacedindex]['frame']

            for i in range(0,6):
                if self.readCounter>0:
                    if pcb.ipmt[i]['frame'] == self.victimframe:
                        pcb.ipmt[i]['null']=1
                        pcb.ipmt[i]['page'] = -1



                elif self.writeCounter >0:
                    if pcb.opmt[i]['frame'] == self.victimframe:
                        if pcb.opmt[i]['dirtybit']==1:
                            disk.Pages[pcb.opmt[i]['page']][self.writeCounter] = memory.frame[pcb.opmt[i]['frame']]
                            self.writeCounter+=1
                        pcb.opmt[i]['page'] = -1

            return replacedindex
        if segment == 1:
            v = 1
            pagenumber = int(pc)
            while v == 1:

                if pcb.ipmt[self.hitindex]['ref'] == 0:  # check refrences of each row of pmt
                    pcb.ipmt[self.hitindex]['ref'] = 1
                    # pcb.opmt[self.hitindex]['page'] = -1
                    pcb.pmt[self.hitindex]['page'] = -1

                    replacedindex = self.ireplacement(pagenumber, pcb, self.hitindex, disk, memory)
                    if self.hitindex < 5:
                        self.hitindex += 1
                    else:
                        self.hitindex = 0
                    break
                else:
                    pcb.ipmt[self.hitindex]['ref'] = 0

                    if self.hitindex < 5:
                        self.hitindex += 1
                    else:
                        self.hitindex = 0
            self.victimframe = pcb.pmt[replacedindex]['frame']

            for i in range(0, 6):
                if pcb.ipmt[i]['frame'] == self.victimframe:
                    if self.writeCounter>0:
                        if pcb.opmt[i]['dirtybit'] == 1:
                            disk[pcb.pmt[i]['page']] = memory.frame[pmt[i]['frame']]
                    pcb.pmt[i]['page'] = -1




                elif self.writeCounter > 0:

                    if pcb.opmt[i]['frame'] == self.victimframe:

                        if opmt[i]['dirtybit'] == 1:
                            disk[opmt[i]['page']] = memory.frame[opmt[i]['frame']]

                        pcb.opmt[i]['page'] = -1

            return replacedindex
        if segment == 2:
            v = 1
            pagenumber = int(pc )
            while v == 1:

                if pcb.opmt[self.hitindex]['ref'] == 0:  # check refrences of each row of pmt
                    pcb.opmt[self.hitindex]['ref'] = 1
                    pcb.pmt[self.hitindex]['page'] = -1
                    pcb.pmt[self.hitindex]['ref'] = 1
                    pcb.ipmt[self.hitindex]['page'] = -1
                    oreplacedindex = self.oreplacement(pagenumber, pcb, self.hitindex, disk, memory)
                    if self.hitindex < 5:
                        self.hitindex += 1
                    else:
                        self.hitindex = 0
                    break
                else:
                    pcb.opmt[self.hitindex]['ref'] = 0

                    if self.hitindex < 5:
                        self.hitindex += 1
                    else:
                        self.hitindex = 0
            self.victimframe = pcb.opmt[replacedindex]['frame']



            for i in range(0, 6):
                if pcb.opmt[i]['frame'] == self.victimframe:
                    if pcb.pmt[i]['dirtybit'] == 1:

                        disk.Pages[pcb.pmt[i]['page']] = memory.frame[pcb.pmt[i]['frame']]
                    pcb.pmt[i]['page'] = -1
                    pcb.pmt[i]['ref']= 1



                elif self.writeCounter > 0:
                    if pcb.opmt[i]['frame'] == self.victimframe:

                        pcb.ipmt[i]['page'] = -1

            return oreplacedindex





###################################################################################################3

    def offset(self,pc):
        return int(pc%8)
    def pagenumber(self,pc):
        return int(pc/8 )

    def pmtroutin(self,pcb,pc):
        self.pagefault =1
        for i in range(0, 6):
            if pcb.pmt[i]['page'] ==int(pc / 8):
                self.pagefault=0
                return i

        return -1
    def ipmtroutin(self,pcb,pc):
        self.pagefault =1
        for i in range(0, 6):
            if pcb.ipmt[i]['page'] ==int(pc ):
                self.pagefault=0
                return i

        return -1
    def opmtroutin(self,pcb,pc):
        self.pagefault =1
        for i in range(0, 6):
            if pcb.opmt[i]['page'] ==int(pc ):
                self.pagefault=0
                return i

        return -1


    def start(self):
        p = open('output.txt', 'w')
        error = errorHandler()
        disk =Disk()
        memory=Memory()
        ####set the variables
        l = Loader()

        ##l.getlines(sys.argv[1])
        l.getlines(sys.argv[1],disk ,memory,p)

        self.setfirstvars(l.JobID, l.LoadAddress, l.initPC, l.traceflag,l.inputnum,l.outputnum)

        self.beginofinput=l.inputpagesnumbers[0]
        self.beginofoutput= l.outputpagesnumbers[0]
        ##########################put initial variables
        pcb=PCB()



        for i in range(0,6):
            pcb.pmt[i]['frame'] = l.memoryresereves[i]

        pcb.pageframereserved()


        memory.frame[l.memoryresereves[0]]= disk.Pages[self.pagenumber(self.PC)]

        pcb.pmt[0]['page']=self.pagenumber(self.PC)
        pcb.pmt[0]['ref'] = 1
        pcb.pmt[0]['null']=0

        self.IR = memory.frame[pcb.pmt[0]['frame']][self.offset(self.PC)]

        self.CPU_Routin(self.IR,pcb, memory,disk,p)

    def CPU_Routin(self, ir, pcb,memory,disk,p):  # CPU Routin
        error =errorHandler()
        if (self.trace == 1):
            tr = open('trace.txt', 'w')
            tr.write("\n")
        pc = self.PC

        p.write("\n")
        clocker =0
        ir = memory.frame[pcb.pmt[0]['frame']][self.offset(self.PC)]
        self.pageindex=self.pagenumber(pc)
        if (self.trace == 1):
            tr.write(" pc(HEX) " +" IR(HEX)" +"   EA (HEX)  "
                  +" (EA) (HEX)  "
                  +"  TOS(HEX) "+"  (TOS)(HEX) "+"    " + "===>"
                  +"   EA (HEX)  "
                  +"  (EA) (HEX) "+"  TOS  (HEX)  "+"  (TOS)(HEX) ")
            tr.write("\n")


        while True:
            if self.clock>1000:
                error.num(5,p)
            self.pageindex=self.pmtroutin(pcb,pc) # if the page is not in th reserved frames it makes the pagefault

                                                        # 1 else return index and make pagefaule 0

            if self.pagefault == 1:
                self.pageindex=self.PageFaultHandler(pc,pcb,disk,memory)



            ir = memory.frame[pcb.pmt[self.pageindex]['frame']][self.offset(self.PC)]


            flag=0
            if (self.trace == 1):
                tr.write(" " +hex(self.PC) +" " )#write PC in trace
                tr.write("        "+(hex(int(ir, 2)))+"  ")#write ir in hex

                tr.write("     "+hex(self.EA)+"          ")

                tr.write( hex(self.toint(self.memEA))+"          ")

                if len(self.s)>0:
                     x= self.s.pop()
                     tr.write( str(len(self.s)))
                     tr.write("     ")
                     tr.write(hex(int(x,2) )+ "   ")
                     self.s.append(x)
                     tr.write("     ")
                else:
                     tr.write("0" +"    ")

                     tr.write("empty")
                tr.write("====>")






            pc = self.instype(ir, pc,pcb,memory,disk,p)


            if self.clock/15 >clocker:

                clocker +=1
                p.write("cloc in vtu of:")
                p.write (str(self.clock))
                p.write("\n")
                for i in range(0,6):
                    if pcb.pmt[i]['page']>-1:
                        p.write("\n")
                        p.write("program pmt")
                        p.write("\n")
                        p.write("page:")
                        p.write(str(pcb.pmt[i]['page']))
                        p.write("\n")
                        p.write("frame")
                        p.write(str(pcb.pmt[i]['frame']))
                        p.write("\n")
                if self.readCounter==1:
                    p.write("input pmt")
                    for i in range(0, 6):
                        p.write("\n")

                        if pcb.ipmt[i]['page'] > -1:

                            p.write("\n")
                            p.write("page")
                            p.write(str(pcb.ipmt[i]['page']))
                            p.write("\n")
                            p.write("frame")
                            p.write(str(pcb.pmt[i]['frame']))
                            p.write("\n")
                if self.writeCounter>0:
                    for i in range(0, 6):
                         if pcb.opmt[i]['page'] > -1:
                             p.write("output pmt")
                             p.write("\n")
                             p.write("page: ")
                             p.write(str(pcb.opmt[i]['page']))
                             p.write("\n")
                             p.write("frame: ")
                             p.write(str(pcb.pmt[i]['frame']))
                             p.write("\n")


            if (self.trace == 1):
                if (self.trace == 1):
                    tr.write(" " + hex(self.PC) + " ")  # write PC in trace
                    tr.write("        " + (hex(int(ir, 2))) + "  ")  # write ir in hex

                    tr.write("     " + hex(self.EA) + "          ")

                    tr.write(hex(self.toint(self.memEA)) + "          ")

                    if len(self.s) > 0:
                        x = self.s.pop()
                        tr.write(str(len(self.s)))
                        tr.write("     ")
                        tr.write(hex(int(x, 2)) + "   ")
                        self.s.append(x)
                        tr.write("     ")
                    else:
                        tr.write("0" + "    ")

                        tr.write("empty")

                tr.write("\n")
                tr.write("\n")
                tr.write("\n")



        #########################################################################
        #############################  types ####################################
        ##########################################################################

    def instype(self, ir, pc,pcb,memory,disk,p):  ##(we return PC)
        if ir[0] == '0':
            i = 3
            j = 8
            ir = ir
            if ir[3:8] != '00000':
                self.clock +=1
            newpc = self.type0(ir, i, j, self.PC,pcb,memory,disk,p)
            if ir[11:16] != '00000':
                i = 11
                j = 16
                self.clock += 1
                newpc = self.type0(ir, i, j, self.PC,pcb,memory,disk,p)
            if self.PC == newpc:
                self.PC += 1
            return self.PC
            ########    pc wont change in an isntructions unless there is a branch
        else:
            self.clock += 4
            newpc = self.type1(ir, self.PC,pcb,memory,disk,p)
            if self.PC == newpc:
                self.PC += 1
            else:
                return self.PC
        return self.PC

    ###############################################################################
    #############################  type0 ####################################
    ##########################################################################
    def type0(self, ir, i, j, pc,pcb,memory,disk,p):  ### is should return pc  and just run IR
        # x= self
        r = ir
        error = errorHandler()
        if r[i:j] == '00000':
            return pc
        elif r[i:j] == '00001':  # or
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.or0(v1, v2))  # its push
                self.s.append(self.or0(v1, v2))  # its push
                return pc
            else:
                error.num(2,p)

        elif r[i:j] == '00010':  # and
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.and0(v1, v2))
                return pc
            else:
                error.num(2,p)


        elif r[i:j] == '00011':  # not
            if len(self.s) > 0:
                v1 = self.s.pop()
                self.s.append(self.not0(v1))
                return pc
            else:
                error.num(2,p)

        elif r[i:j] == '00100':  # XOR
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.xor0(v1, v2))
                return pc

        elif r[i:j] == '00101':  # ADD
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.add0(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[i:j] == '00110':  # sub
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.sub0(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[i:j] == '00111':  # MUL
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.mul0(v1, v2))
                return pc
            else:
                error.num(2,p)
        elif r[i:j] == '01000':  # DIV

            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.div0(v1, v2))
            else:
                error.num(2,p)

        elif r[i:j] == '01001':  # MOD
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(self.mod(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[i:j] == '01010':  # SL
            if len(self.s) > 0:
                v1 = self.s.pop()
                self.s.append(self.SL(v1))
                return pc

            else:
                error.num(2,p)

        elif r[i:j] == '01011':  # SR
            if len(self.s) > 0:
                v1 = self.s.pop()
                self.s.append(self.SR(v1))
                return pc
            else:
                error.num(2,p)
        elif r[i:j] == '01100':  # CPG
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(v2)
                self.s.append(v1)
                self.s.append(self.CPG(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[i:j] == '01101':#CPL
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(v2)
                self.s.append(v1)
                self.s.append(self.CPL(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[i:j] == '01110':  # CPE
            if len(self.s) > 1:
                v1 = self.s.pop()
                v2 = self.s.pop()
                self.s.append(v2)
                self.s.append(v1)
                self.s.append(self.CPE(v1, v2))
                return pc
            else:
                error.num(2,p)


        ####reading input from memory
        elif r[i:j] == '10011':
            self.readCounter +=1
            if self.readCounter == 1:
                pcb.segfault(inseg=1)
                self.segfaultnumerator+=5
                self.clock+=5

            self.pageindex = self.ipmtroutin(pcb,self.beginofinput )  # if the page is not in th reserved frames it makes the pagefault
            if self.pagefault == 1:
                self.pageindex = self.PageFaultHandler(self.beginofinput, pcb, disk, memory,segment=1)
            v = memory.frame[pcb.ipmt[self.pageindex]['frame']]
            if len(self.s) < 8:
                self.clock+=14

                # v = input("")
                self.iotime+= 15
                self.s.append(v)
                return pc
            else:
                error.num(3,p)

        elif r[i:j] == '10100':  # Prin answer // put the outputin memory
            if len(self.s) > 0:
                self.writeCounter +=1
                if self.writeCounter==1:
                    self.segfaultnumerator +=5
                    pcb.segfault(outseg=1)

                self.pageindex = self.opmtroutin(pcb, self.beginofoutput)
                if self.pagefault == 1:
                    self.pageindex = self.PageFaultHandler(self.beginofoutput, pcb, disk, memory, segment=2)
                ##comeback
                memory.frame[pcb.opmt[self.pageindex]['frame']][self.writeCounter-1] = self.s.pop()



                self.clock+=14
                self.iotime += 15
                v1 = memory.frame[pcb.opmt[self.pageindex]['frame']][self.writeCounter-1]

                self.out=v1

                return pc
            else:
                error.num(2,p)


        elif r[i:j] == '10101':
            self.clock-=1
            if len(self.s) > 0:
                self.PC = self.toint(self.s.pop()) + 1
            else:
                error.num(2,p)

        elif r[i:j] == '11000':#termination


            for i in range(0,6):
                if pcb.opmt[i]['dirtybit']==1:
                    disk.Pages[pcb.opmt[i]['page']]=memory.frame[pcb.opmt[i]['frame']]
            self.outputspooling(disk,memory,pcb,p)
            exit(0)


        ###############################################################################
        #############################  type1 ####################################
        ###############################################################################
        ##########################################################################



    def type1(self, ir, pc,pcb,memory,disk,p):


        r = ir
        self.EA = int(r[9:16], 2)
        ##########################3
        self.pageindex = self.pmtroutin(pcb, self.EA)  # if the page is not in th reserved frames it makes the pagefault


        if self.pagefault == 1:
            self.pageindex = self.PageFaultHandler(self.EA, pcb, disk, memory)
        self.memEA = memory.frame[pcb.pmt[self.pageindex]['frame']][self.offset(self.EA)]


        ##########################3

        error = errorHandler()
        if r[1:6] == '00000':
            return pc



        elif r[1:6] == '00001':  # or
            if len(self.s) > 0:
                v1 = self.s.pop()
                v2 = self.memEA
                self.s.append(self.or0(v1, v2))  # its push
            else:
                error.num(2,p)


        elif r[1:6] == '00010':  # and
            if len(self.s) > 0:
                v1 = self.memEA
                v2 = self.s.pop()
                self.s.append(self.and0(v1, v2))
                return pc

            else:
                error.num(2,p)

        elif r[1:6] == '00100':  # selfOR
            if len(self.s) > 0:
                v1 = self.memEA
                v2 = self.s.pop()
                self.s.append(self.xor0(v1, v2))
                return pc
            else:
                error.num(2,p)
        elif r[1:6] == '00101':  # ADD
            if len(self.s) > 0:
                v1 = self.memEA
                v2 = self.s.pop()
                self.s.append(self.add0(v1, v2))
                return pc

            else:
                error.num(2,p)
        elif r[1:6] == '00110':  # sub

            if len(self.s) > 0:
                v1 = self.s.pop()
                v2 = self.memEA
                self.s.append(self.sub0(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[1:6] == '00111':  # MUL
            if len(self.s) > 0:
                v1 = self.s.pop()
                v2 = self.memEA
                self.s.append(self.mul0(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[1:6] == '01000':  # DIV
            if len(self.s) > 0:
                v1 = self.s.pop()
                v2 = self.memEA
                self.s.append(self.div0(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[1:6] == '01001':  # MOD
            if len(self.s) > 0:
                v1 = self.s.pop()
                v2 = self.memEA
                self.s.append(self.mod(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[1:6] == '01100':  # CPG
            if len(self.s) > 0:
                v2 = self.s.pop()
                v1 = self.memEA
                self.s.append(v2)
                self.s.append(self.CPG(v1, v2))
                return pc
            else:
                error.num(2,p)
        elif r[1:6] == '01101':  # CPL

            if len(self.s) > 0:
                v2 = self.s.pop()
                v1 = self.memEA
                self.s.append(v2)
                self.s.append(self.CPL(v1, v2))
                return pc
            else:
                error.num(2,p)

        elif r[1:6] == '01110':  # CPE
            if len(self.s) > 0:
                v2 = self.s.pop()
                v1 = self.memEA
                self.s.append(v2)
                self.s.append(self.CPE(v1, v2))
                return pc
            else:
                error.num(2,p)
        elif r[1:6] == '01111':  # effective address to PC

            self.PC = self.EA


        elif r[1:6] == '10000':  # check if it is true put EA to PC

            if len(self.s) > 0:
                v1 = self.s.pop()
                if v1 == '1111111111111111':
                    self.PC = self.EA
                else:
                    return pc
            else:
                error.num(2,p)

        elif r[1:6] == '10001':  # check if it is false put EA to PC
            if len(self.s) > 0:
                v1 = self.s.pop()
                if v1 == '0000000000000000':
                    self.PC = self.EA

                else:
                    return pc
            else:
                error.num(2,p)

        elif r[1:6] == '10010':

            self.s.append(self.tobin(self.PC))
            self.PC = self.EA

        elif r[1:6] == '10101':
            if len(self.s) > 0:
                self.PC = self.s.pop()
            else:
                error.num(2,p)

        elif r[1:6] == '10110':  # push
            if len(self.s)<=7:
                self.s.append(self.memEA)
                return pc
            else:
                error.num(3,p)


        elif r[1:6] == '10111':  # pop
            if len(self.s) > 0:
                memory.frame[pcb.pmt[self.pageindex]['frame']][self.offset(self.EA)] = self.s.pop()
                pcb.pmt[self.pageindex]['dirtybit']=1



                return pc
            else:
                error.num(2,p)

        elif r[1:6] == '11000': #termination

            for i in range(0,6):
                if pcb.opmt[i]['dirtybit']==1:
                    disk.Pages[pcb.opmt[i]['page']]=memory.frame[pcb.opmt[i]['frame']]
            self.outputspooling(disk, memory, pcb, p)
            exit()

    ################################################################################
    def setfirstvars(self, JobID, LoadAddress, initPC, traceflag,inputnum,outputnum):
        self.jobID = int(JobID)
        self.trace = int(traceflag)
        self.EA = int(LoadAddress, 16)
        self.PC = int(initPC, 16)
        self.inputnum=int(inputnum)
        self.ouputnum =int(outputnum)


    ##################################################################Convert
    def toint(self, X):

        if X[0] == '1':
            y = int(X, 2)
            x = ~y+1
            l = self.tobin(x)
            h = int(l, 2) * -1
            return h
        return int(X, 2)

    def tobin(self, X):
        o = int(X)
        v = bin(o & (2 ** 16 - 1))[2:].zfill(16)
        return v

    ##################################################################type0

    def or0(self, v1, v2):
        return self.tobin(self.toint(v1) | self.toint(v2))

    def and0(self, v1, v2):
        return self.tobin(self.toint(v1) & self.toint(v2))

    def xor0(self, v1, v2):
        return self.tobin(self.toint(v1) ^ self.toint(v2))

    def not0(self, v1):
        return self.tobin(self.toint(v1) ^ self.toint('1111111111111111'))

    def add0(self, v1, v2):
        return self.tobin(self.toint(v1) + self.toint(v2))

    def sub0(self, v1, v2):
        if self.toint(v1) < self.toint(v2):
            P = abs(self.toint(v1) - self.toint(v2))
            P = (self.tobin(P))
            P = self.NOT0(P)
            P = self.ADD0(P, '1')
            return P
        else:
            return self.tobin(self.toint(v1) - self.toint(v2))

    def mul0(self, v1, v2):
        return self.tobin(self.toint(v1) * self.toint(v2))

    def div0(self, v1, v2):
        if cpu.toint(v2) == 0:
            return 0
        else:
            return (self.tobin(int(self.toint(v1) / self.toint(v2))))

    def mod(self, v1, v2):
        error = errorHandler()
        if cpu.toint(v2) == 0:
            error.num(4,p)
            return 0
        else:
            return (self.tobin(self.toint(v1) % self.toint(v2)))

    def SL(self, v1):
        return (self.tobin(self.toint(v1) << 1))

    def SR(self, v1):
        return (self.tobin(self.toint(v1) >> 1))

    def CPG(self, v1, v2):

        if self.toint(v2) > self.toint(v1):
            return '1111111111111111'

        else:
            return '0000000000000000'

    def CPL(self, v1, v2):
        if self.toint(v2) < self.toint(v1):
            return '1111111111111111'
        else:
            return '0000000000000000'

    def CPE(self, v1, v2):
        if self.toint(v2) == self.toint(v1):
            return '1111111111111111'
        else:
            return '0000000000000000'

    def negbintoint(self, v):
        y= int(v,2)
        x=~y+1
        l= self.tobin(x)
        h=int(l,2) *-1

    def inttotwoscomplementbin(self, v):
        o = int(v)
        v = bin(o & (2 ** 16 - 1))[2:].zfill(16)


###############################################################################
#############################      MAIN     ###################################
###############################################################################

cpu = CPU()
cpu.start()

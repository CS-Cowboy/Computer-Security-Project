import hashlib as hsh
import sys
import io
import time 
import os

#@Author: Jacob Z & Sean J
#A solution to CSCI-476's assignment for this week. 

class DictionaryAttacker:

    def start(self, argV):
        self.encoding = 'utf-8' #necessary to read the strings
        self.bufferLen = io.DEFAULT_BUFFER_SIZE #system buffering limitation
        if(len(argV) == 3):
            self.dictionaryName = str(argV[1])
            self.hashFilename = str(argV[2])
            self.dictionaryFile = open( self.dictionaryName , encoding=self.encoding, errors='ignore') #open file
            self.dictionary = self.dictionaryFile.readlines(self.bufferLen) #initially read it
            self.hashFile = open(self.hashFilename , encoding=self.encoding)
            self.hashes = self.hashFile.readlines(self.bufferLen)
            self.startTime = time.time()
            self.AttackHashes() #lets go!
        else:
            print("Usage: <dictionary> <hashed passwords>")

    def AttackHashes(self): 
        lineCount = 0 #keeps track of how many lines have been read.

        while(lineCount < os.path.getsize(self.dictionaryName)): #exits at EOF
            for line in self.dictionary:
                line = str(line).rstrip() #rstrip() removes the newline on right end
                md5hasher = hsh.md5(line.encode(self.encoding)) #create a new md5 hash object because we want to call hexdigest() with each line, instead of all previous lines concatenated
                hex = str(md5hasher.hexdigest()) #hashes are in hexadecimal format, unsalted. 

                for hash in self.hashes:
                    hash = str(hash).rstrip()

                    if(hex == hash): #derp. self explanatory.
                            print('Found password. Hash=\t',
                                hex, '\tPassword=\t', line)
            self.dictionary = self.dictionaryFile.readlines(self.bufferLen) #read another group of self.bufferLen lines
            lineCount += self.bufferLen #keep track of our lines read.
        self.elapsedTime = time.time() - self.startTime
        print('Time elapsed:\t',self.elapsedTime, '\tseconds')
        self.dictionaryFile.close()
        self.hashFile.close() #don't forget to close the files!
            


g = DictionaryAttacker()
g.start(sys.argv)

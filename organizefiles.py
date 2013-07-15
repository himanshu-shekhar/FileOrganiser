#-------------------------------------------------------------------------------
# Name:        Organize Files
# Purpose:     To organize files according to their extensions
#
# Author:      Rogue
# Version:     2
# Created:     22-10-2012
# Copyright:   (c) Rogue 2012
#-------------------------------------------------------------------------------

#Changes in version 2:
#Added option to move files according to file size.

#version 1:
#Move files according to extensions

import os
import sys
import re
import shutil

#constraints ------------------------------------------
Case_Sensitive=False    #for extensions

#format 'folder name':['min_size','max_size', 'extension name1','ext name2', '...']
#set max_size to 0 for file of any size greater than min_size. max_size is NOT included
#size should be given in Mb. Can be float(eg: 3.5)
#extension names are NOT case sensitive

formats={
    'movies':[300,0,'mkv','avi','mpeg','dat','mov','mp4','mpg','flv','vob','wmv'],
    'videos':[0,300,'mkv','avi','mpeg','dat','mov','mp4','mpg','flv','vob','wmv'],
    'audios':[0,0,'mp3','ogg'],
    'documents':[0,0,'txt','doc','docx','log','pdf'],
    'photos':[0,0,'jpeg','jpg','gif','png'],
    'softwares':[0,0,'exe','msi','apk'],
    'compressed':[0,0,'rar','zip','7z'],
    'codes':[0,0,'java','cpp','c','py','m']
}

#end of constraints -----------------------------------

def move_files(organize_files):
    changed=False

    for i in organize_files:
        #print 'checking:{}'.format(os.path.join(os.getcwd(),i))
        if len(organize_files[i]) and not os.path.isdir(os.path.join(os.getcwd(),i)):
            os.mkdir(os.path.join(os.getcwd(),i))

    for i in organize_files:
        if len(organize_files[i])==0:
            continue
        p=os.path.join(os.getcwd(), i)
        for j in organize_files[i]:
            try:
                shutil.move(j,p)
                organize_files[i].remove(j)
                changed=True
            except:
                pass
        if len(organize_files[i]):
            print '{} files were not moved in directory {} :'.format(len(organize_files[i]), i)
            for j in organize_files[i]:
                print '\t>{}'.format(j)

    return changed

def organize(files, formats):
    organization={}
    flag=False

    for i in formats:
        organization[i]=[]

    for i in formats:
        if formats[i][1]==0:formats[i][1]=float('inf')
        for j in range(2,len(formats[i])):
            if not Case_Sensitive:
                formats[i][j]=re.compile('.{}$'.format(formats[i][j]), re.IGNORECASE)
            else:
                formats[i][j]=re.compile('.{}$'.format(formats[i][j]))

    for i in files:
        for j in formats:
            for k in range(2,len(formats[j])):
                if formats[j][k].search(i):
                    info=os.stat(i)
                    size=(info.st_size*1.0)/(1024*1024)
                    if size>=formats[j][0] and size<formats[j][1]:
                        #print '{} in {}'.format(i,j)
                        organization[j]+=[i]
                        flag=True
                        break
            if flag:
                break
        flag=False

    for i in organization:
        print '{} file(s) in {}'.format(len(organization[i]), i)

    iteration=1
    print '\n\nIteration {}\n\n'.format(iteration)
    while(move_files(organization)):
        iteration+=1
        print 'Iteration {}\n\n'.format(iteration)


def find_files(directory):
    a=[i for i in list(os.walk(directory))[0]]
    #print a
    a=[os.path.join(a[0], i) for i in a[2]]
    a.remove(sys.argv[0])
    return a

def main():
    #print os.getcwd()
    #print "the file is", os.path.basename(sys.argv[0])
    files=find_files(os.getcwd())
    #print files
    #files=['bla.jpg','new.mkv','sh.txt','sh2.tXt']
    organize(files,formats)

if __name__ == '__main__':
    main()

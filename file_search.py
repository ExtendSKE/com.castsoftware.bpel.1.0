import os
import subprocess as sp
import fnmatch
output = []
def directory_search(path,extension):
    error_log = open(path+"/error.log",'w')
    output = depth_search(path,extension,error_log)
    error_log.close()
    return output

def depth_search(path,extension,error_log):
    dirs = os.listdir(path)
    #print(dirs)
    if len(dirs)==0:
        error_log.wrtie("Warning: "+path+" No file exist of extension "+extension+"\n")
        return
    count =0
    for file in dirs:
        index=file.find('~')
        if index ==-1:
            dec = os.path.isfile(path+"/"+file)
            #print(dec)
            if dec is True:
                if fnmatch.fnmatch(file,extension):
                    tmp = []
                    tmp.append(path+"/"+file)
                    tmp.append(file)
                    output.append(tmp)
                    count = count+1
                    #print(file)
            else:
                #print(file)
                depth_search(path+"/"+file,extension,error_log)
    if count == 0:
        error_log.write("Warning: "+path+" No file exist of extension "+extension+"\n")
    return output
if __name__ == "__main__":
    path=sp.getoutput('pwd')
    extension ="*.bpel"
    print(directory_search(path,extension))
    '''
    Multiple Line Comment
    for i in output:
        for j in i:
            print(j," ")
        print()
    '''

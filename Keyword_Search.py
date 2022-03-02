import os
import glob
import codecs
import pdfplumber
import argparse
import time


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    
    allFiles = list()
    
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    
    return allFiles

def check_file_encoding(filename_path):
    flag = 0
    filename = os.path.basename(filename_path)
    try:
        f = codecs.open(filename_path, encoding='utf-8', errors='strict')
        for line in f:
            pass
        flag = 1
    except UnicodeDecodeError:
        flag = 0
    return flag


def convert_to_utf8(ff_name, target_file_name):
    with open(ff_name, 'rb') as source_file:
          with open(target_file_name, 'w+b') as dest_file:
            contents = source_file.read()
            if contents == None:
                pass
            dest_file.write(contents.decode('utf-16').encode('utf-8'))
    return 

def read_files(path, find_str):
    Output = []
    AllFilesList = getListOfFiles(path)
    ListOfFileNames = []
    ListOfConvertedFileNames = []
    flag = 0
    count = 0
    for i in AllFilesList:
        s = os.path.basename(i)
        ListOfFileNames.append(s)

    for i in range(len(ListOfFileNames)):
        if find_str in AllFilesList[i]:
            if count ==0:
                count =count+1
                folder_name = AllFilesList[i].partition(find_str)[0] + find_str
                Output.append(folder_name)
            else:
                pass
        if ".pdf" in ListOfFileNames[i]:
            with pdfplumber.open(AllFilesList[i]) as pdf:
                for page in pdf.pages:
                    s = page.extract_text()
                    if find_str in s:
                        Output.append(str(ListOfFileNames[i]))
                        break
                
        if (".txt" in ListOfFileNames[i] or ".csv" in ListOfFileNames[i] or ".xlsx" in ListOfFileNames[i])==True:
            flag = check_file_encoding(AllFilesList[i])
            if flag == 0:
                
                convertedfilename = "converted_"+str(ListOfFileNames[i])
                convert_to_utf8(AllFilesList[i], convertedfilename)
                
                with codecs.open(convertedfilename, 'r',encoding="utf-8") as read_obj:
                    lines = read_obj.readlines()
                    for line in lines:
                        if find_str in line:
                            Output.append(str(ListOfFileNames[i]))
                            break
                os.remove(convertedfilename)
                
            if flag == 1:
                with codecs.open(AllFilesList[i], 'r',encoding="utf-8") as read_obj:
                    lines = read_obj.readlines()
                    for line in lines:
                        if find_str in line:
                            Output.append(str(ListOfFileNames[i]))
                            break
        else:
            pass

    return Output
                        
        
    
if __name__ == "__main__":
    #If IDLE is to be used, then take input as the
    #below two code lines indiacte
    path = input("Enter the directory/folder path: ")
    s = input("Enter the string to search: ")
    #If input is to be taken from CMD, then use below code lines
    '''parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True)
    parser.add_argument("-f", "--find", required=True)
    args = parser.parse_args()'''
    Output = read_files(path, s)#call read_files
    print(Output)
    #time.sleep(3000)
    


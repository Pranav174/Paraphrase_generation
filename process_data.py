from ssf_api import *
import pickle
import io
# reload(sys)
# sys.setdefaultencoding("utf-8")

import logging
#import utilities
#log = utilities.setup_logger()


def create_rawData_pickles(dataLocation):

    # Walks through the folder to get names/strings of all the files
    FileList = folderWalk(dataLocation)

    # Processed File count
    fileNum = 0

    # Target location to store processed data
    createDirectory("./DATA/PROCESSED-DATA/collection/")

    # Catches all the files which report exception while processing, along with the exception
    errs = "\n{} {}".format('FileName','Exception')


    for rawFilePath in FileList:

        try:
            # sentenceList   : list of ssf_api.Sentence objects
            # globalWordList : list of ssf_api.Word objects
            sentenceList, globalWordList = extractSSFannotations(rawFilePath)

            # Get the SSFInfo object
            ssfinfo = SSFInfo(sentenceList, globalWordList)

            # Populates the ssfinfo.sentenceList[indx].nodeDict['key'].childList
            # For all the indxs in sentenceList and key in nodeDict of that sentence
            createChildList(ssfinfo)

        except Exception as e:
            errs += "\n{} {}".format(os.path.basename(rawFilePath), e)
            continue

        # If the file pointed by rawFilePath doesn't contain any sentence
        if(sentenceList == None):
            print("No sentence in"+rawFilePath+"Continuing")
            continue

        # Pickle the ssinfo Object into the collections
        filee = open("./DATA/PROCESSED-DATA/collection/"+rawFilePath.split('/')[-1]+'.pkl','wb')
        pickle.dump(ssfinfo, filee)
        fileNum+=1
        
        #exportModel("PROCESSED-DATA/annotatedData",discourseFileCollection)
    print("Processed %d raw files correctly",fileNum)
    print("The following raw files could not be processed :"+errs)



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please give RAW-data folder's location")
        print("")
        option = input("\n\tShould ./DATA/RAW-DATA/ be used as the dir? [Y|n]")
        if option == 'y' or option == 'Y':
            dataLocation = './DATA/RAW-DATA/'
        else:
            print("Please re-run the script with command line arguments")
            exit()
    else:
        dataLocation = sys.argv[1]
    
    create_rawData_pickles(dataLocation)
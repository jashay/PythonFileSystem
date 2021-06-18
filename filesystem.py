from datetime import datetime2
import random
import typing

#Each type of file with given fields
class File:
    
    def __init__(self,ID,name,t,ct,children,parent):
        self.id = ID
        self.name = name
        self.type = t
        self.creation_time = ct
        self.children = children
        self.parent = parent


class FileSystem:
    
    def __init__(self):
        self.root = File(1,"MyDocuments","folder",datetime.now(),[],None)
        self.files = {}
        self.files[1] = self.root
        self.file_ids = set()
        self.file_ids.add(1)
        
    
    
    #to check if given file is created and in the list of keys of files dict
    def check_file(self, fileId: int) -> bool:
        if fileId not in self.files.keys():
            return False
        else:
            return True
        
    #To check if given file is type folder
    def check_folder(self, folderId: int) -> bool: 
        if self.files[folderId].type != "folder":
            return False
        else:
            return True
    
    def get_total_dashboards(self) -> int:
        # TODO: implement
        #Breadth First Search
        count = 0
        node = self.root
        q = []
        q.append(node)
        while q:
            temp = q.pop(0)
            if temp.type == "dashboard":
                count+=1
            if len(temp.children) == 0:
                continue
            else:
                for child in temp.children:
                    q.append(child)
        return count
    
    def get_total_worksheets(self) -> int:
        # TODO: implement
        #Breadth First Search
        count = 0
        node = self.root
        q = []
        q.append(node)
        while q:
            temp = q.pop(0)
            if temp.type == "worksheet":
                count+=1
            if len(temp.children) == 0:
                continue
            else:
                for child in temp.children:
                    q.append(child)
        return count
    
    def add_new_file(self, fileName: str, fileType: str, folderId: int) -> bool:
        # TODO: implement  

        if not self.check_file(folderId):
            return False
        elif not self.check_folder(folderId):
            return False
        else:
            fileId = str(random.randint(100,999)) + str(random.randint(100,999))
            
            #checking if random number is already generated
            while int(fileId) in self.file_ids:
                fileId = str(random.randint(100,999)) + str(random.randint(100,999))
            
            fileId = int(fileId)
            self.file_ids.add(fileId) ##CHANGE
            new_file = File(fileId,fileName,fileType,datetime.now(),[],folderId) #creating new file object
            self.files[folderId].children.append(new_file)
            self.files[fileId] = new_file 
            return True

    
    def get_creation_time(self, fileId: int) -> datetime:
        # TODO: implement
        if not self.check_file(fileId):
            return None
        else:
            return self.files[fileId].creation_time

    
    def move_file(self, fileId: int, newFolderId: int) -> bool:
        # TODO: implement
        #print(self.files[fileId].type,self.files[newFolderId].type)
        if not self.check_file(fileId) or not self.check_file(newFolderId):
            print("No such file and/or folder")
            return False
        elif not self.check_folder(newFolderId):
            print("No such folder exists")
            return False
        else:
            old_folder = self.files[fileId].parent
            self.files[old_folder].children.remove(self.files[fileId]) #remove from children list of old folder
            self.files[newFolderId].children.append(self.files[fileId]) # add to children of new folder
            self.files[fileId].parent = newFolderId
            return True

    
    def get_files(self, folderId: int) -> typing.List[str]:
      # TODO: implement
        output = []
        if not self.check_file(folderId):
            return None
        elif not self.check_folder(folderId):
            return None
        else:
            childList = self.files[folderId].children
            if len(childList) == 0:
                return output
            else:
                for child in childList:
                    output.append(child.id)
        return output
    
    def print_files(self) -> None:
        # TODO: implement
        ##Breadth First Search
        node = self.root
        q = []
        q.append(node)
        while q:
            temp = q.pop(0)
            if temp.type == "folder":
                print("Name:"+temp.name+" | Id: "+str(temp.id)+" | File Type: "+temp.type+"| Children: ")                   
                if len(temp.children) == 0:
                    print("None\n")
                else:
                    for child in temp.children:
                        print("Name:"+child.name+" | Id: "+str(child.id)+" | File Type: "+child.type)
                        q.append(child)
                    print("\n")
        return

    
def ask_for_int(question: str) -> int:
    val = input(question)
    try:
        return int(val)
    except:
        print('Please enter a valid integer value\n')
        return ask_for_int(question)
    
def ask_question():
    fs = FileSystem()
    running = True
    print("Note: Id of MyDocuments folder is 1")
    while(running):
        
        command = ask_for_int("\nEnter an integer to indicate a command: \n[1] get_total_dashboards\n[2] get_total_worksheets\n[3] add_new_file\n[4] get_creation_time\n[5] move_file\n[6] get_files \n[7] print_files\n[8] exit\n")
        
        if command == 1:
            totalDashboards = fs.get_total_dashboards()
            print("There are {0} dashboards in the file system.".format(totalDashboards));
        elif command == 2:
            totalWorksheets = fs.get_total_worksheets()
            print("There are {0} worksheets in the file system.".format(totalWorksheets));
        elif command == 3:
            fileName = input("Enter a new file name: ")
            fileType = input("Enter a file type (worksheet, dashboard, or folder): ")
            folderId = ask_for_int("Enter a folder id where you'd like to put this file: ")
            if fs.add_new_file(fileName, fileType, folderId) == True:
                print("{0} has been added to folder {1}".format(fileName, folderId))
            else:
                print("Folder not found!")
        elif command == 4:
            fileId = ask_for_int("Enter a file id: ")
            creationTime = fs.get_creation_time(fileId);
            if creationTime == None:
                print("No Such File Exists!!")
            else:
                print("file {0} was created at {1}".format(fileId, creationTime));
        elif command == 5:
            fileId = ask_for_int("Enter a file id:")
            newFileId = ask_for_int("Enter the folder id where you'd like to move this file: ")
            result = fs.move_file(fileId, newFileId);
            if result == True:
                print("Successfully moved file {0} to folder {1}".format(fileId, newFileId))
        elif command == 6:
            folderId = ask_for_int("Enter a folderId:")
            fileNames = fs.get_files(folderId)
            if fileNames == None:
                print("No Such Folder Exists!!")
            elif (len(fileNames) == 0):
                print("There are no files in folder {0}".format(folderId))
            else:
                print("The following files are in folder {0}: ".format(folderId))
                for fileName in fileNames:
                    print("\t{0}".format(fileName))
        elif command == 7:
            fs.print_files()
        elif command == 8:
            print("Exiting program.")
            running = False
        else:
            print("Invalid command: {0}. Please try again.\n".format(command))
              
ask_question()



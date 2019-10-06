import os
import shutil
import re

class SeriesRenamer:
    def __init__(self, directory, name, season):
        self.name = name
        self.folder = directory
        self.season = season
        self._lift_files()
        os.chdir(self.folder)
        self._delete_directories()
        self._rename_files()
        
    def _lift_files(self):
        for r,d,f in os.walk(self.folder):
            for file in f:
                shutil.move(os.path.join(r,file), os.path.join(self.folder,file))
                
    def _delete_directories(self):
        files = os.listdir(self.folder)
        dirs = [x for x in files if os.path.isdir(x)]
        for d in dirs:
            os.rmdir(d)
            
    def _rename_files(self):
        files = os.listdir(self.folder)
        n_episodes = len([x for x in files if os.path.getsize(x)> 1000000])
        
        for i in range(1,n_episodes+5):
            number = 1
            season = '{num:02d}'.format(num=self.season)
            episode ='{num:02d}'.format(num=i)
            
            ids = "S{}".format(season)
            ide = "E{}".format(episode)
            idx = "{}x{}".format(season,episode)
            idx2 = "{}x{}".format(self.season,episode)
            for file in files:
                matchs = re.search(ids.lower(), file.lower())
                matche = re.search(ide.lower(), file.lower())
                matchx = re.search(idx.lower(), file.lower())
                matchx2 = re.search(idx2.lower(), file.lower())
                if (matchs and matche) or matchx or matchx2:
                    splited = file.split(".")
                    extension = splited[-1]
                
                    newfilename = "{} {}{}.{}".format(self.name,ids,ide,extension)
                    print("renaming {} to {}".format(file,newfilename))
                    try:
                        os.rename(file, newfilename)
                    except(FileExistsError):
                        newfilename = "{} {}{}_{}.{}".format(self.name,ids,ide,number,extension)
                        os.rename(file, newfilename)
                        print("renaming {} to {}".format(file,newfilename))
                        number = number+1

        
 
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", default="D:\\series", type=str, help="Path to series folder")
    
    args = parser.parse_args()
    
    for directory in os.listdir(args.d):
        full_path = os.path.join(args.d,directory)
        if os.path.isdir(full_path):
            print (full_path)
            splited = directory.split()
            print(splited)
            try:
                season = int(splited[-1])
                name = " ".join(splited[:-1])
            except ValueError:
                season = 1
                name = directory
            print("Series name is {}.".format(name))
            renamer = SeriesRenamer(full_path, name, season)
    
    
    
    
    
        
    
        
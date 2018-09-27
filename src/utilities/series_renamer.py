import os
import shutil
import re

class SeriesRenamer:
    def __init__(self, args):
        self.name = args.name
        self.folder = args.folder
        self.season = args.season
        
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
                    filename = '.'.join(splited[0:-1])
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
    parser.add_argument("--folder", default=".", type=str, help="Path to series folder")
    parser.add_argument("--name", default="default_name", type = str, help="Name of the series")
    parser.add_argument("--season", default="1", type = int, help="Number of the season")
    
    args = parser.parse_args()
    if args.name == "default_name":
        splited = os.path.basename(args.folder).split()
        try:
            print(splited)
            season = int(splited[-1])
            
            args.name = " ".join(splited[:-1])
            args.season = season
        except ValueError:
            args.name = os.path.basename(args.folder)
        print("Series name is {}.".format(args.name))
        
    renamer = SeriesRenamer(args)

    
    
    
    
    
        
    
        
import json

class data_explorer():
    def __init__(self,datafile:str) -> None:
        with open(datafile) as f:
            self.the_data:dict = json.load(f)
    
    def traverse(self,level=1):
        return [self.the_data[a] for a in self.the_data.keys() if type(self.the_data[a]) == dict]
        
    
d = data_explorer('thedump.json')

print (d.traverse())


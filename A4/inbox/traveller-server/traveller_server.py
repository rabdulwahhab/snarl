class Character:
    def __init__(self, name):
        self.name=name
        self.town=None

    #town is Town object
    def change_location_town(self, town):
        self.town=town

    def to_string(self):
        out="Name: "+self.name
        if(self.town!=None):
            out+="\nTown: \n     Name: "+self.town.name
        return out
        
class Town:
    
    def __init__(self, name):
        self.name=name
        self.towns=set()
        self.characters=set()

    #character object
    def add_character(self, character):
        self.characters.add(character)
        character.change_location_town(self)
        
    def remove_character(self, character):
        self.characters.remove(character)
        character.change_location_town(None)
        
    def connect_town(self, town):
        self.towns.add(town)
        town.towns.add(self)
        
    def disconnect_town(self):
        for t in self.towns:
            t.remove(self)
        self.towns=set()

    #D is destination town object, seen_town is accumulater for seen town nodes
    def character_free_path_exists(self,D, seen_town):
        if self in seen_town:
            return False
        out=False
        if(self==D):
            return True
        for t in self.towns:
            if(len(t.characters)==0):
                seen_town.add(self)
                out=out or t.character_free_path_exists(D,seen_town)
            else:
                out=out or False
        return out

    #Used for place character
    def safe_passage(self, town, seen_town):
        if self in seen_town:
            return False
        out=False
        if(self==town):
            return True
        for t in self.towns:
            seen_town.add(self)
            out=out or t.safe_passage(town, seen_town)
        return out
    
    def to_string(self):
        out="Name: "+self.name+"\nTowns: "
        for t in self.towns:
            out+="\n     Name: "+t.name
        out+="\nCharacters: "
        for c in self.characters:
            out+="\n     Name: "+c.name
        return out+"\n"

class TownNetwork:

    #Dictionary of towns[town_name]->town object
    #Dictionary of characters[character_name]->character object
    def __init__(self):
        self.towns={}
        self.characters={}
        
    def add_town(self,town_name):
        self.towns[town_name]=Town(town_name)
    
    def remove_town(self,town_name):
        town.disconnect_town()
        self.towns.pop(town_name)
    
    def create_network(self, json_connections): 
        for p in json_connections:
            f=p["from"]
            t=p["to"]
            if not f in self.towns:
                self.add_town(f)
            if not t in self.towns:
                self.add_town(t)
            self.towns[f].connect_town(self.towns[t])
        return True

    #character_name, town_name are unique string names
    def place_character(self, character_name, town_name):
        self.create_new_character_if_not_exists(character_name)
        if self.safe_passage(character_name, town_name) != "Discard":
            self.towns[town_name].add_character(self.characters[character_name])
            return True
        return "Discard"

    def safe_passage(self, character_name, town_name):
        self.create_new_character_if_not_exists(character_name)
        S=self.characters[character_name].town

        #if character no town return
        if S==None or (not town_name in self.towns.keys()):
            return "Discard";

        return S.safe_passage(self.towns[town_name], set())

    def character_free_path_exists(self, character_name, town_name):
        self.create_new_character_if_not_exists(character_name)
        S=self.characters[character_name].town
        
        #if town don't exist discard
        if S==None or (not town_name in self.towns.keys()):
            return "Discard";
        return S.character_free_path_exists(self.towns[town_name],set())

    #can be overloaded to accepting character object instead, depends on implementation
    def create_new_character_if_not_exists(self,character_name):
        if not character_name in self.characters.keys():
            newChar = Character(character_name)
            try:
                newChar.change_location_town(list(self.towns.values())[0])
            except:
                print("didn't call create network first")
            self.characters[character_name] = newChar
        
    def to_string(self):
        out="TownNetwork: \n"
        for t in self.towns.values():
            print(t)
            out=out+t.to_string()+"\n"
        return out
    
    
    
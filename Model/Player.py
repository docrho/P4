import json
from Model.Db import DbManager


class Player:

    def __init__(self, last_name="", first_name="", birth_date="", gender="",
                 ranking="", point='', doc_id=""):
        self.lastname = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
        self.point = point
        self.doc_id = doc_id
        # attribute report from method
        self.all_players = []
        self.all_players_id = []
        # serialized list of player from database
        self.serialized_players_list = []
        self.players_list = []
        self.db = DbManager()

    def __str__(self):
        return str(self.lastname + " " + self.first_name)  # + self.point

    def __repr__(self):
        return str(
            self.lastname + " " + self.first_name)

    def append_player_from_id(self, player_id_list):
        for player_id in player_id_list:
            # getting all player from database with doc_id
            # adding on player selected each player from id
            current_player = self.db.players.get(doc_id=int(player_id))
            self.players_list.append(
                current_player
            )
        self.serialize_player()
        return self.players_list

    def serialize_player(self,):
        self.serialized_players_list = json.dumps(self.players_list)
        return self.serialized_players_list

    def players_id_checking(self, ids: list):  # checking if id exist
        all_id = self.get_all_players_id(self.all_players)
        for id in ids:
            if str(id) not in str(all_id):
                return False
        return True

    @staticmethod
    def list_all_players():
        all_players_data = DbManager().players.all()
        all_players = []
        for player_data in all_players_data:
            all_players.append(Player(
                player_data["lastname"],
                player_data["first_name"],
                player_data["birth_date"],
                player_data["gender"],
                player_data["ranking"],
                player_data["points"],
                player_data.doc_id
                                      )
                               )
        return all_players

    def player_instance(self, players_data):
        for player in players_data:
            self.players_list.append(Player(
                player["lastname"],
                player["first_name"],
                player["birth_date"],
                player["gender"],
                player["ranking"],
                player["points"],
                                      )
                               )
        return self.players_list

    def get_all_players_id(self, all_players):

        for player in all_players:  # taking all id
            self.all_players_id.append(player.doc_id)
        return self.all_players_id

    def get_all_players_from_db(self):
        return self.db.players.all()

    def player_object_to_dict(self):
        returned_dict = {
            "lastname": self.lastname,
            "firstname": self.first_name,
            "birthdate": self.birth_date,
            "gender": self.gender,
            "ranking": self.ranking,
            "point": self.point,
        }
        return returned_dict

    def player_dict_to_object_(self, dictionary_player):
        self.first_name = dictionary_player['firstname']
        self.lastname = dictionary_player['lastname']
        self.birth_date = dictionary_player['birthdate']
        self.gender = dictionary_player['gender']
        self.ranking = dictionary_player['ranking']
        self.point = dictionary_player['point']

        return "self"

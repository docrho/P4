import json

from tinydb import TinyDB
from tinydb.operations import set
from tinydb import where


class DbManager(TinyDB):

    def __init__(self):
        self.db = TinyDB("db.json")
        self.players = self.db.table("players")
        self.tournament = self.db.table('tournament')




#        if for not broken return true

    def store_player(self, player):
        self.players.insert({
            "type": "player", "lastname": player.lastname,
            "first_name": player.first_name,
            "birth_date": player.birth_date, "gender": player.gender,
            "ranking": player.ranking,
            "points": player.point,
        })

    def add_player(self, playerlist, player):
        for playerinlist in playerlist:
            #checking if player exist
            if playerinlist.lastname == player.lastname \
                    and playerinlist.first_name == player.first_name \
                    and playerinlist.birth_date == player.birth_date:
                return False
        self.store_player(player)
        return True

    def store_tournament(self, tournament):
        self.tournament.insert({
            "name": tournament.name,
            "place": tournament.place,
            "date": tournament.date,
            "nb_turn": tournament.nb_turn,
            "players": tournament.players,
            "time": tournament.time,
            "description": tournament.description,
            "rounds_list": tournament.rounds_list,
            "tours_list": tournament.tours_list
        })

    def remove_players(self, lastname, birth_date):
        if self.players.remove(where('lastname') == str(lastname) and
                               where('birth_date') == str(birth_date)):
            return True
        else:
            return False

    def remove_tournament(self, id):
        # check if the tournament id exist
        if self.tournament_id_check(int(id)):
            # remove the tournament if exist
            self.tournament.remove(doc_ids=[int(id), ])
            return True
        else:
            return False  # otherwise return false



    def tournament_id_check(self, id):
        list_id = []
        all_tournaments = self.tournament.all()
        for tournament in all_tournaments:
            list_id.append(tournament.doc_id)
        if id in list_id:
            return True
        else:
            return False

    def update_tournament(self, key, id, update):
        self.tournament.update(set(key, update), doc_ids=[int(id)])
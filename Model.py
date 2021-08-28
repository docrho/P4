from tinydb import TinyDB, Query
from tinydb.operations import set
from tinydb import where


class Player:

    def __init__(self, last_name, first_name, birth_date, gender, ranking):
        self.lastname = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
    def __str__(self):
        return self.lastname

class DbManager(TinyDB):

    def __init__(self):
        self.db = TinyDB("db.json")
        self.players = self.db.table("players")
        self.tournament = self.db.table('tournament')

    def _store_player(self,player):
        self.players.insert({
            "type": "player", "lastname": player.lastname, "first_name": player.first_name,
            "birth_date": player.birth_date, "gender": player.gender, "ranking": player.ranking
        })

    def add_player(self,players_data, player):
        for player_data in players_data:

            if player_data['lastname'] == player.lastname and player_data['first_name'] == player.first_name and \
                    player_data['birth_date'] == player.birth_date:
                return False
        self._store_player(player)
        return True

    def store_tournament(self, tournament):
        self.tournament.insert({
            "type": "player", "name": tournament.name, "place": tournament.place,
            "date": tournament.date, "nb_turn": tournament.nb_turn , "players": tournament.players,
            "time": tournament.time, "description": tournament.description, "tournament_id": tournament.tournament_id
        })

    def remove_players(self, key, value):
        self.players.remove(where(key)==value)

    def remove_tournament(self, id):
        self.tournament.remove(doc_ids=[int(id),])

    def list_all_players(self):
        return self.players.all()

    def tournament_id_check(self, id):
        list_id =[]
        all_tournaments = self.tournament.all()
        for tournament in all_tournaments:
            list_id.append(tournament.doc_id)
        if (id in list_id):
            return True
        else:
            return False
    def update_tournament(self,id,update):
        self.tournament.update(set("name",update),doc_ids=[int(id)])
class Round():
    def __init__(self, player1, player2,match_list):
        self.player1 = player1
        self.player2 = player2
        self.match_list = match_list

    def winner(self):
        return winer

    def pair_generator(self):
        return True


class Tournament():
    def __init__(self, name, place, date, nb_turn, players: Player, time, description, tournament_id):
        self.name = name
        self.place = place
        self.date = date
        self.nb_turn = nb_turn
        self.players = players
        self.time = time
        self.description = description
        self.tournament_id = tournament_id

    def __str__(self):
        return f"{self.name} {self.date}"


import json
from tinydb import TinyDB
from tinydb.operations import set
from tinydb import where


class DbManager(TinyDB):

    def __init__(self):
        self.db = TinyDB("db.json")
        self.players = self.db.table("players")
        self.tournament = self.db.table('tournament')

    def store_player(self, player):

        self.players.insert({
            "type": "player",
            "lastname": player.lastname,
            "first_name": player.first_name,
            "birth_date": player.birth_date,
            "gender": player.gender,
            "ranking": player.ranking,
            "points": player.point,
        })

    def add_player(self, playerlist, player):
        for playerinlist in playerlist:
            # checking if player exist
            if playerinlist.lastname == player.lastname \
                    and playerinlist.first_name == player.first_name \
                    and playerinlist.birth_date == player.birth_date:
                return False
        self.store_player(player)
        return True

    def store_tournament(self, tournament):
        tournament.players = self.serialise_players_object_from_tournament(
            tournament.players
        )
        tournament.rounds_list = self.serialise_round_object_from_tournament(
            tournament.rounds_list
        )
        tournament.tours_list = self.serialise_tour_object_from_tournament(
            tournament.tours_list
        )
        self.tournament.insert({
            "name": tournament.name,
            "place": tournament.place,
            "date": tournament.date,
            "nb_turn": tournament.nb_turn,
            # serialise player

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

    def serialise_players_object_from_tournament(self, tournamentplayer):
        jsonlist = []
        for player in tournamentplayer:
            jsonlist.append(
                json.dumps(player.__dict__, default=lambda o: o.__dict__))
        return jsonlist

    def serialise_round_object_from_tournament(self, tournament_rounds):
        jsonlist = []
        for tournament_rounds in tournament_rounds:

            for round in tournament_rounds:
                round = list(round)
                round[0] = json.dumps(
                    round[0].__dict__, default=lambda o: o.__dict__)
                round[1] = json.dumps(round[1])
                round[2] = json.dumps(
                    round[2].__dict__, default=lambda o: o.__dict__)
                round[3] = json.dumps(round[3])
                jsonlist.append(round)
        return jsonlist

    def serialise_tour_object_from_tournament(self, tournament_tour):
        jsonlist = []
        for tour in tournament_tour:
            jsonlist.append(
                json.dumps(tour))
        return jsonlist

    def update_all_data_from_tournament(self, id, tournament):
        self.tournament.update(
            set("name", tournament.name), doc_ids=[int(id)])
        self.tournament.update(
            set("place", tournament.place), doc_ids=[int(id)])
        self.tournament.update(
            set("date", tournament.date), doc_ids=[int(id)])
        self.tournament.update(
            set("nb_turn", tournament.nb_turn), doc_ids=[int(id)])
        # serialise players object
        player_serialized = self.serialise_players_object_from_tournament(
            tournament.players)
        self.tournament.update(
            set("players", player_serialized), doc_ids=[int(id)])
        self.tournament.update(
            set("time", tournament.time), doc_ids=[int(id)])
        self.tournament.update(
            set("description", tournament.description), doc_ids=[int(id)])
        # select the tournament in the list to serialise them
        tournament.rounds_list = self.serialise_round_object_from_tournament(
            tournament.rounds_list)
        self.tournament.update(
            set("rounds_list", tournament.rounds_list), doc_ids=[int(id)])
        self.tournament.update(
            set("tours_list", tournament.tours_list), doc_ids=[int(id)])
        return True

from Model.Player import Player
from Model.Tour import Tour
import json
from Model.Db import DbManager
from operator import itemgetter


class Tournament:
    def __init__(self, name: str = "", place: str = "",
                 date: str = "", nb_turn: int = "",
                 players: list[Player] = "", time: str = "",
                 description: str = "", doc_id: int = ""
                 ):
        self.name = name
        self.place = place
        self.date = date
        self.nb_turn = nb_turn
        self.players = []
        self.time = time
        self.description = description
        self.tour_number = 0
        # round already played
        self.rounds_list = list()
        self.current_tour = Tour()
        self.tours_list = []
        self.doc_id = doc_id
        # attribute from method
        self.tournament_list = []
        self.all_tournament_list = []
        self.players_in_tournament = []
        self.tournament_info = []
        self.db = DbManager()

    def __str__(self):
        return f"{self.name} {self.date}"

    def deserialise_round_list(self):
        for round in self.rounds_list:
            round[0] = json.loads(round[0])
            round[2] = json.loads(round[2])
        return True

    def add_tournament_info(self, tournament_info, players_list):
        self.name = tournament_info['name']
        self.place = tournament_info['place']
        self.date = tournament_info['date']
        self.time = tournament_info['time']
        self.description = tournament_info['description']
        self.place = tournament_info['place']
        for player in players_list:
            self.players.append(
                Player(
                    player['lastname'],
                    player['first_name'],
                    player['birth_date'],
                    player['gender'],
                    player['ranking'],
                    player['points'],
                )
            )

    def _all_tournament_instance(self, all_tournament):
        for tournament_data in all_tournament:
            self.all_tournament_list.append(
                Tournament(
                    tournament_data["name"],
                    tournament_data["place"],
                    tournament_data["date"],
                    tournament_data["nb_turn"],
                    tournament_data["players"],
                    tournament_data["time"],
                    tournament_data["description"],
                    tournament_data.doc_id,
                )

            )
        return self.all_tournament_list

    def tournament_instance(self, tournament):
        self.rounds_list = []
        self.tour_number = tournament["tour_number"]
        self.name = tournament["name"]
        self.place = tournament["place"]
        self.date = tournament["date"]
        self.nb_turn = tournament["nb_turn"]
        self.rounds_list = self.rounds_instance(tournament["rounds_list"])
        # deserialising player from databse
        # instancing player
        for player in tournament["players"]:
            player = json.loads(player)
            self.players.append(Player(
                player["lastname"],
                player["first_name"],
                player["birth_date"],
                player["gender"],
                player["ranking"],
                player["point"],
            ))
        self.time = tournament["time"]
        self.description = tournament["description"]
        self.doc_id = tournament.doc_id
        return True

    def remove_tournament(self, id: int()):
        return self.db.remove_tournament(id)

    def list_all_tournament(self):
        return self._all_tournament_instance(self.db.tournament.all())

    def tournament_id_checking(self, id):
        return self.db.tournament_id_check(id)

    def get_tournament_by_id(self, id):
        return self.db.tournament.get(doc_id=id)

    def store_match_already_played(self):
        self.rounds_list.append(self.current_tour.match_list)
        return self.rounds_list

    def sort_player_by_rank(self):
        player_list_dict = []
        for player in self.players:
            player_list_dict.append(
                player.player_object_to_dict()
            )
        player_list_dict = sorted(player_list_dict, key=itemgetter("ranking"))
        i = 0
        for player in self.players:
            player.player_dict_to_object_(player_list_dict[i])
            i += 1
        return self.players

    def sort_player_by_points(self):
        player_list_dict = []
        for player in self.players:
            player_list_dict.append(
                player.player_object_to_dict()
            )
        player_list_dict = sorted(player_list_dict, key=itemgetter("point"))
        player_list_dict.reverse()
        i = 0
        for player in self.players:
            player.player_dict_to_object_(player_list_dict[i])
            i += 1
        return self.players

    def adding_score_to_players_instance_from_match(self):
        match_list = self.current_tour.match_list
        # transform the tuple from match into list to manipulate him
        match_list_str = []
        for match in match_list:
            current = list(match)
            match_list_str.append(current)
        # store on the new list string value to manipulate the index
        for match in match_list_str:
            match[0] = str(match[0])
            match[2] = str(match[2])
        # store the score from match to player

        for match in match_list_str:
            for player in self.players:
                try:
                    index_found = match.index(
                        player.lastname+" "+player.first_name)
                    player.point = float(match[index_found+1])
                except ValueError:
                    pass
        return self.players

    def if_tour_greater_than(self, number):
        if self.tour_number < number:
            return False
        return True

    def calculate_how_many_turn_left(self):
        turnleft = 4 - self.tour_number
        return turnleft

    def check_if_same_points(self):
        all_point = []
        all_point_set = []
        for player in self.players:
            all_point.append(player.point)
        all_point_set = set(all_point)
        if (len(all_point) != (len(all_point_set))):
            return True
        else:
            return False

    def rounds_instance(self, rounds_data):
        round_instance = []
        for round in rounds_data:
            round[0] = json.loads(round[0])
            round[2] = json.loads(round[2])
            round_instance.append((
                Player(
                    round[0]["lastname"],
                    round[0]["first_name"],
                    round[0]["birth_date"],
                    round[0]["gender"],
                    round[0]["ranking"],
                    round[0]["point"],
                ),
                float(round[1]),
                Player(
                    round[2]["lastname"],
                    round[2]["first_name"],
                    round[2]["birth_date"],
                    round[2]["gender"],
                    round[2]["ranking"],
                    round[2]["point"],
                ),
                float(round[3])
            ))
        round_instance = [round_instance, ]
        if round_instance.__len__() == 0:
            return self.rounds_list
        else:
            return round_instance

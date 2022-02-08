from Model.Player import Player
import datetime


class Tour:

    def __init__(self):
        self.match_list = []
        self.name = ""
        self.start_time = []
        self.start_Date = ""
        self.end_time = []
        self.end_Date = ""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    # can be static

    def current_datetime(self):
        return datetime.datetime.now()

    def tour1(self, tournament_players: Player()):
        self.start_time.append(self.current_datetime())
        self.name = 'Round1'
        self.match_list = []
        for seq in range(4):

            self.match_list.append((
                Player(
                    tournament_players[seq].lastname,
                    tournament_players[seq].first_name,
                    tournament_players[seq].birth_date,
                    tournament_players[seq].gender,
                    tournament_players[seq].ranking,
                    tournament_players[seq].point,
                ),
                tournament_players[seq].point,
                Player(
                    tournament_players[seq+4].lastname,
                    tournament_players[seq+4].first_name,
                    tournament_players[seq+4].birth_date,
                    tournament_players[seq+4].gender,
                    tournament_players[seq+4].ranking,
                    tournament_players[seq+4].point,
                ),
                tournament_players[seq+4].point,
            ))
        return self.match_list

    def tour2(self, tournament_players):
        self.start_time.append(self.current_datetime())
        self.name = 'Round'
        self.match_list = []
        for seq in range(0, 8, 2):

            self.match_list.append((
                Player(
                    tournament_players[seq].lastname,
                    tournament_players[seq].first_name,
                    tournament_players[seq].birth_date,
                    tournament_players[seq].gender,
                    tournament_players[seq].ranking,
                    tournament_players[seq].point,
                ),
                tournament_players[seq].point,
                Player(
                    tournament_players[seq+1].lastname,
                    tournament_players[seq+1].first_name,
                    tournament_players[seq+1].birth_date,
                    tournament_players[seq+1].gender,
                    tournament_players[seq+1].ranking,
                    tournament_players[seq+1].point,
                ),
                tournament_players[seq+1].point,
            ))
        return self.match_list
        # ajouter condition if point sont egal alors par rank

    # adding result prompt from view to all match from match list

    def add_score_to_match(self, score_from_view: list):
        match_list_update = []

        x = 0
        for match in self.match_list:
            current_match_list = list(match)
            current_match_list[1] = current_match_list[1] + score_from_view[x]
            current_match_list[3] = current_match_list[3] + score_from_view[
                x+1]
            current_match_list = tuple(current_match_list)
            match_list_update.append(current_match_list)
            x += 2
        self.match_list = match_list_update
        return self.match_list

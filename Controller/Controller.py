from View import View
from Model.Db import DbManager
from Model.Player import Player
from Model.Tournament import Tournament
import json


class Controller:

    def __init__(self):
        self.v = View.Views()
        self.db = DbManager()
        self.response = 0
        self.responsemenu = 0
        self.tournament = Tournament()
        self.player = Player()
        self.tournament_id = int()
        self.score = float
    
    def home(self):
        self.v.load_page("home")
        self.response = str(input())
        return self.response

# starting app####
    def loading_tournament(self):
        self.tournament = Tournament()
        self.player = Player()
        # store the response on variable tournament_id
        self.tournament_id = int(
            self.v.load_page("_update_tournament_menu_prompt"))
        # checking if the tournament id exist
        if self.tournament.tournament_id_checking(self.tournament_id):
            # adding tournament from database on tournament instance
            self.tournament.tournament_instance(
                self.tournament.get_tournament_by_id(
                    self.tournament_id)
            )
            # if tour 1 not played
            self.tournament.tour_number = self.tournament.rounds_list[
                0].__len__()
            self.tournament.tour_number = int(self.tournament.tour_number / 4)
            return True
        else:
            return False

    def first_turn(self):
        if (self.tournament.tour_number < 1):
            # store starting time
            self.tournament.current_tour.start_time.append(
                self.tournament.current_tour.current_datetime()
            )
            # show players on console
            self.v.load_page("show_player_on_tournament", self.tournament)
            self.v.load_page("list_tournament", self.tournament)
            # sort player instance in tournament instance
            self.tournament.sort_player_by_rank()

            # starting first tour with player instance from tournament
            self.tournament.current_tour.tour1(self.tournament.players)
            # ask view to type score of the first tour
            self.score = self.v.load_page(
                "add_score_to_match", self.tournament.current_tour.match_list
            )
            # adding score to match list of tuple
            self.tournament.current_tour.add_score_to_match(self.score)
            # store current tour on tour list un tournament
            self.tournament.store_match_already_played()
            self.tournament.adding_score_to_players_instance_from_match()
            # store end time of turn
            self.tournament.current_tour.end_time.append(
                self.tournament.current_tour.current_datetime()
            )
            # asking for rank change
            if self.v.load_page("do_you_want_modify_rank"):
                self.tournament.players = self.v.load_page(
                    "players_modify_rank", self.tournament.players)
            ###############################
            # asking for saving tournament score in actual state
            if self.v.load_page("do_you_want_save_tournament"):
                self.v.load_page("update_all_data_from_tournament",
                                 self.db.update_all_data_from_tournament(
                                     self.tournament_id, self.tournament)
                                 )
            self.tournament.tour_number += 1
            return True
        else:
            return False

    def secondTolastTurn(self):
        # starting second turn and other

        for seq in range(4 - self.tournament.tour_number):

            self.tournament.sort_player_by_points()
            if self.tournament.check_if_same_points():
                self.tournament.sort_player_by_rank()
            else:
                pass
            self.tournament.current_tour.tour2(self.tournament.players)
            self.score = self.v.load_page("add_score_to_match",
                                    self.tournament.current_tour.match_list)
            self.tournament.current_tour.add_score_to_match(self.score)
            self.tournament.store_match_already_played()
            self.tournament.adding_score_to_players_instance_from_match()
            # store end time of turn
            self.tournament.current_tour.end_time.append(
                self.tournament.current_tour.current_datetime()
            )
            # asking for rank change
            if self.v.load_page("do_you_want_modify_rank"):
                self.tournament.players = self.v.load_page(
                    "players_modify_rank", self.tournament.players)
            if self.v.load_page("do_you_want_save_tournament"):
                self.v.load_page("update_all_data_from_tournament",
                                 self.db.update_all_data_from_tournament(
                                     self.tournament_id, self.tournament)
                                 )
        self.v.load_page("update_all_data_from_tournament",
                         self.db.update_all_data_from_tournament(
                             self.tournament_id, self.tournament)
                         )
        return True

    def create_new_tournament(self):
        self.tournament = Tournament()
        self.player = Player()
        # store on attribute all player from database
        list_players = Player.list_all_players()
        self.player.all_players = list_players
        # we are displaying all player ,like this we can choose them by id
        self.v.load_page("display_all_players", list_players)
        # return the 8 player number prompt that we want to select
        player_id_list = self.v.load_page("create_tournament_players")
        # checking up if the id prompted exist
        if self.player.players_id_checking(player_id_list):
            # this method add player and serialize them
            # verifier les id dans append, la methode static
            self.player.append_player_from_id(player_id_list)
            # calling view for ask tournament name prompt ....
            tournament_info = self.v.create_tournament()
            # creating tournament with tournament method
            self.tournament.add_tournament_info(tournament_info,
                                                self.player.players_list)
            # store tournament on database
            self.db.store_tournament(self.tournament)
        else:
            self.v.load_page("error", "player_id")
            return False
        return True

    def add_player(self):
        # init a player that we will send it to view
        player_prompt = self.v.load_page("add_player_view", Player())
        # Taking all player data to compare them with current player,
        # its for avoiding double
        # instancing the deserialized data
        list_all_players = Player.list_all_players()  # static
        # add_player return True if there is no double on database
        added_bol = self.db.add_player(list_all_players, player_prompt)
        # load a page to print successfull or not
        self.v.load_page("player_successfully_added_or_not",
                         added_bol,
                         player_prompt
                         )

    def remove_player(self):
        player_to_remove = self.v.remove_player(Player())
        # player is list of string from view containing date and name
        if self.db.remove_players(player_to_remove.lastname,  # player.remove
                                  player_to_remove.birth_date):
            self.v.load_page("success", "player_removed")
        else:
            self.v.load_page("error", "player_not_removed")

    def list_all_players(self):
        self.player = Player()
        self.v.load_page("display_all_players", self.player.list_all_players())

    def remove_tournament(self):
        self.tournament = Tournament()
        # remove from id
        ###########################
        if self.tournament.remove_tournament(self.v.response_input()):
            self.v.load_page("success", "tournament_removed")
        else:
            self.v.load_page("error", "tournament_not_removed")

    def list_all_tournament(self):
        self.tournament = Tournament()
        self.tournament.list_all_tournament()
        self.v.load_page("list_tournament",
                         self.tournament.all_tournament_list)

    def update_tournament(self):
        self.tournament = Tournament()
        # store the response on variable tournament_id
        self.tournament_id = int(self.v.load_page("_update_tournament_menu_prompt"))
        # checking if the tournament id exist
        if self.tournament.tournament_id_checking(self.tournament_id):
            # adding tournament from database on tournament instance
            self.tournament.tournament_instance(
                self.tournament.get_tournament_by_id(
                    self.tournament_id)
            )
            self.v.load_page("list_tournament", self.tournament)
            while self.responsemenu != "6":  # condition to exit the loop
                self.v.load_page("update_tournament_menu")
                self.responsemenu = self.v.basic_input()
                if self.responsemenu == "1":  # change name condition
                    # passing the id prompted to the method
                    self.db.update_tournament(
                        "name", self.tournament_id,
                        self.v.load_page("change_tournament_prompt"))
                if self.responsemenu == "2":
                    # passing the id prompted to the method
                    self.db.update_tournament(
                        "place", self.tournament_id,
                        self.v.load_page("change_tournament_prompt"))
                if self.responsemenu == "3":
                    # passing the id prompted to the method
                    self.db.update_tournament(
                        "date", self.tournament_id,
                        self.v.load_page("change_tournament_prompt"))
                if self.responsemenu == "4":
                    # passing the id prompted to the method
                    self.db.update_tournament(
                        "description", self.tournament_id,
                        self.v.load_page("change_tournament_prompt"))
                if self.responsemenu == "5":
                    self.tournament.remove_tournament(self.tournament_id)

        else:
            self.v.load_page("error", "tournament_id")

    def display_all_player_from_tournament(self):
        self.tournament = Tournament()
        self.tournament.list_all_tournament()
        self.v.load_page("list_tournament",
                         self.tournament.all_tournament_list)
        print('choose the tournament id')
        self.tournament_id = int(self.v.load_page("_update_tournament_menu_prompt"))
        # checking if the tournament id exist
        if self.tournament.tournament_id_checking(self.tournament_id):
            # adding tournament from database on tournament instance
            self.tournament.tournament_instance(
                self.tournament.get_tournament_by_id(
                    self.tournament_id)
            )
            self.v.load_page("display_all_players", self.tournament.players)

    def list_round_from_tournament(self):
        self.tournament = Tournament()
        self.player = Player()
        # store the response on variable tournament_id

        self.tournament_id = int(self.v.load_page("_update_tournament_menu_prompt"))
        # checking if the tournament id exist
        if self.tournament.tournament_id_checking(self.tournament_id):
            # adding tournament from database on tournament instance
            tour_data = self.tournament.get_tournament_by_id(
                self.tournament_id)

        for round in tour_data["rounds_list"]:
            round[0] = json.loads(round[0])
            round[2] = json.loads(round[2])
        # sending round to view
        self.v.load_page("display_all_round_or_match_from_tournament",
                         tour_data["rounds_list"]
                         )

    def launch(self):

        while True:
            self.responsemenu = self.home()
            if self.responsemenu == "0":  # To quit
                break

            elif self.responsemenu == "1":  # load
                if self.loading_tournament():
                    # if tournament loaded correctly do first turn
                    if self.first_turn():
                        # if first turn played do second turn
                        if self.secondTolastTurn() is not True:
                            print("error")
                    else:
                        #do second turn anyway
                        if self.secondTolastTurn() is not True:
                            print("error")
                else:
                    print('error while loading')

            elif self.responsemenu == "2":  # create new tournament
                if self.create_new_tournament() is not True:
                    print("error")
            elif self.responsemenu == "3":  # add a player on Player database
                self.add_player()
            elif self.responsemenu == "4":  # remove a player in database
                self.remove_player()
            elif self.responsemenu == "5":  # list all players in database
                self.list_all_players()
            elif self.responsemenu == "6":  # Remove a tournament
                self.remove_tournament()
            elif self.responsemenu == "7":  # List all tournament
                self.list_all_tournament()
            elif self.responsemenu == "8":  # update a tournament
                self.update_tournament()
            elif self.responsemenu == "9":
                self.display_all_player_from_tournament()
            elif self.responsemenu == "10":  # List round from tournament
                self.list_round_from_tournament()

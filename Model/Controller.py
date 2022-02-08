from Model import View
from Model.Db import DbManager
from Model.Player import Player
from Model.Tournament import Tournament


v = View.Views()
db = DbManager()
# function######


def home():
    v.load_page("home")
    response = str(input())
    return response

# starting app####


def launch():

    while True:

        responsemenu = home()
        if responsemenu == "0":  # To quit
            break

        elif responsemenu == "1":  # load tournament
            tournament = Tournament()
            player = Player()
            # store the response on variable tournament_id

            tournament_id = int(v.load_page("_update_tournament_menu_prompt"))
            # checking if the tournament id exist
            if tournament.tournament_id_checking(tournament_id):
                # adding tournament from database on tournament instance
                tournament.tournament_instance(tournament.get_tournament_by_id(
                    tournament_id)
                )
                # store starting time
                tournament.current_tour.start_time.append(
                    tournament.current_tour.current_datetime()
                )
                # show players on console
                v.load_page("show_player_on_tournament", tournament)
                v.load_page("list_tournament", tournament)
                # sort player instance in tournament instance
                tournament.sort_player_by_rank()

                # starting first tour with player instance from tournament
                tournament.current_tour.tour1(tournament.players)
                # ask view to type score of the first tour
                score = v.load_page("add_score_to_match",
                                    tournament.current_tour.match_list)
                # adding score to match list of tuple
                tournament.current_tour.add_score_to_match(score)
                # store current tour on tour list un tournament
                tournament.store_match_already_played()
                tournament.adding_score_to_players_instance_from_match()
                # store end time of turn
                tournament.current_tour.end_time.append(
                    tournament.current_tour.current_datetime()
                )
                # asking for rank change
                if v.load_page("do_you_want_modify_rank"):
                    tournament.players = v.load_page(
                        "players_modify_rank", tournament.players)
                ###############################
                # asking for saving tournament score in actual state
                if v.load_page("do_you_want_save_tournament"):
                    v.load_page("update_all_data_from_tournament",
                                db.update_all_data_from_tournament(
                                    tournament_id, tournament)
                                )
                # starting second turn and other

                for seq in range(3):

                    tournament.sort_player_by_points()
                    if tournament.check_if_same_points():
                        tournament.sort_player_by_rank()
                    else:
                        pass
                    tournament.current_tour.tour2(tournament.players)
                    score = v.load_page("add_score_to_match",
                                        tournament.current_tour.match_list)
                    tournament.current_tour.add_score_to_match(score)
                    tournament.store_match_already_played()
                    tournament.adding_score_to_players_instance_from_match()
                    # store end time of turn
                    tournament.current_tour.end_time.append(
                        tournament.current_tour.current_datetime()
                    )
                    # asking for rank change
                    if v.load_page("do_you_want_modify_rank"):
                        tournament.players = v.load_page(
                            "players_modify_rank", tournament.players)
                    v.load_page("update_all_data_from_tournament",
                                db.update_all_data_from_tournament(
                                    tournament_id, tournament)
                                )
                    if v.load_page("do_you_want_save_tournament"):
                        v.load_page("update_all_data_from_tournament",
                                    db.update_all_data_from_tournament(
                                        tournament_id, tournament)
                                    )

        elif responsemenu == "2":  # create new tournament
            tournament = Tournament()
            player = Player()
            # store on attribute all player from database
            list_players = Player.list_all_players()
            player.all_players = list_players
            # we are displaying all player ,like this we can choose them by id
            v.load_page("display_all_players", list_players)
            # return the 8 player number prompt that we want to select
            player_id_list = v.load_page("create_tournament_players")
            # checking up if the id prompted exist
            if player.players_id_checking(player_id_list):
                # this method add player and serialize them
                # verifier les id dans append, la methode static
                player.append_player_from_id(player_id_list)
                # calling view for ask tournament name prompt ....
                tournament_info = v.create_tournament()
                # creating tournament with tournament method
                tournament.add_tournament_info(tournament_info,
                                               player.players_list)
                # store tournament on database
                db.store_tournament(tournament)
            else:
                v.load_page("error", "player_id")

        elif responsemenu == "3":  # add a player on Player database
            # init a player that we will send it to view
            player_prompt = v.load_page("add_player_view", Player())
            # Taking all player data to compare them with current player,
            # its for avoiding double
            # instancing the deserialized data
            list_all_players = Player.list_all_players()  # static
            # add_player return True if there is no double on database
            added_bol = db.add_player(list_all_players, player_prompt)
            # load a page to print successfull or not
            v.load_page("player_successfully_added_or_not",
                        added_bol,
                        player_prompt
                        )

        elif responsemenu == "4":  # remove a player on Player database
            player_to_remove = v.remove_player(Player())
            # player is list of string from view containing date and name
            if db.remove_players(player_to_remove.lastname,  # player.remove
                                 player_to_remove.birth_date):
                v.load_page("success", "player_removed")
            else:
                v.load_page("error", "player_not_removed")

        elif responsemenu == "5":  # list all players from Player database

            player = Player()
            v.load_page("display_all_players", player.list_all_players())

        elif responsemenu == "6":  # Remove a tournament
            tournament = Tournament()
            # remove from id
            ###########################
            if tournament.remove_tournament(v.response_input()):
                v.load_page("success", "tournament_removed")
            else:
                v.load_page("error", "tournament_not_removed")

        elif responsemenu == "7":  # List all tournament
            tournament = Tournament()
            tournament.list_all_tournament()  # static
            v.load_page("list_tournament", tournament.all_tournament_list)

        elif responsemenu == "8":  # update a tournament
            tournament = Tournament()
            # store the response on variable tournament_id
            tournament_id = int(v.load_page("_update_tournament_menu_prompt"))
            # checking if the tournament id exist
            if tournament.tournament_id_checking(tournament_id):
                # adding tournament from database on tournament instance
                tournament.tournament_instance(tournament.get_tournament_by_id(
                    tournament_id)
                )
                v.load_page("list_tournament", tournament)
                while responsemenu != "6":  # condition to exit the loop
                    v.load_page("update_tournament_menu")
                    responsemenu = v.basic_input()
                    if responsemenu == "1":  # change name condition
                        # passing the id prompted to the method
                        db.update_tournament(
                            "name", tournament_id,
                            v.load_page("change_tournament_prompt"))
                    if responsemenu == "2":
                        # passing the id prompted to the method
                        db.update_tournament(
                            "place", tournament_id,
                            v.load_page("change_tournament_prompt"))
                    if responsemenu == "3":
                        # passing the id prompted to the method
                        db.update_tournament(
                            "date", tournament_id,
                            v.load_page("change_tournament_prompt"))
                    if responsemenu == "4":
                        # passing the id prompted to the method
                        db.update_tournament(
                            "description", tournament_id,
                            v.load_page("change_tournament_prompt"))
                    if responsemenu == "5":
                        tournament.remove_tournament(tournament_id)

            else:
                v.load_page("error", "tournament_id")
        elif responsemenu == "9":
            tournament = Tournament()
            tournament.list_all_tournament()
            v.load_page("list_tournament", tournament.all_tournament_list)
            print('choose the tournament id')
            tournament_id = int(v.load_page("_update_tournament_menu_prompt"))
            # checking if the tournament id exist
            if tournament.tournament_id_checking(tournament_id):
                # adding tournament from database on tournament instance
                tournament.tournament_instance(tournament.get_tournament_by_id(
                    tournament_id)
                )
                v.load_page("display_all_players", tournament.players)

        elif responsemenu == "10":  # List round from tournament
            tournament = Tournament()
            player = Player()
            # store the response on variable tournament_id

            tournament_id = int(v.load_page("_update_tournament_menu_prompt"))
            # checking if the tournament id exist
            if tournament.tournament_id_checking(tournament_id):
                # adding tournament from database on tournament instance
                tournament.tournament_instance(tournament.get_tournament_by_id(
                    tournament_id)
                )
            else:
                break
            # deserialising round
            tournament.deserialise_round_list()
            # sending round to view
            v.load_page("display_all_round_or_match_from_tournament",
                        tournament.rounds_list
                        )


class Views:
    def start_match(self):
        print("Type 1 to start match or 0 to leave")
        return input()

    def remove_player(self, player):
        print("Type the Lastname of the player that you want to delete")
        player.lastname = input()
        print("Type the date of birth of the player that you want to delete")
        player.birth_date = input()
        return player

    def player_successfully_added_or_not(self, added, player):
        if added:

            print(f"The player {player.lastname} "
                  f"{player.first_name} was added !!!\n")
        else:
            print("Player already exist, so not added")

    def add_player_view(self, player):
        print("You can now add a player\n")
        print("Type his first name:\n")
        player.first_name = input()
        print("his lastname\n")
        player.lastname = input()
        print("his birth date\n")
        player.birth_date = input()
        print("his gender\n")
        player.gender = input()
        print("his rank \n")
        player.ranking = input()

        return player

    def success(self, success):
        if success == "player_added":
            print('Players added successfully ')
        if success == "player_removed":
            print("Player removed successfully")
        if success == "tournament_removed":
            print("Tournament removed successfully")

    def display_all_players(self, all_players):
        print("Type 1 to display players by alphabetical order\n"
              "Type 2 to display players by ranking point")
        response = int(input())
        player_list = []
        if response == 1:
            for player in all_players:
                player_list.append(f"{player.lastname} "
                                   f"{player.first_name} date :"
                                   f" {player.birth_date}\n"
                                   f" Rank : {player.ranking} id :"
                                   f" {player.doc_id}"
                                   f" Points : {player.point}"
                                   )
            sorted_list = sorted(player_list, key=str.lower)
            print("List of players by alphabetical order\n")
            for player in sorted_list:
                print(player)
            print("\n")

        elif response == 2:
            for player in all_players:
                player_list.append(f"{player.ranking} {player.lastname} "
                                   f"{player.first_name} "
                                   f"date :{player.birth_date}"
                                   f" id : {player.doc_id}"
                                   )
            sorted_list = sorted(player_list)
            print("List of players by ranking order\n")
            for player in sorted_list:
                print(player)
            print("\n")

    def display_all_players_from_tournament(self, all_players):
        print("Player list:\n")
        for player in all_players:
            print(f"{player.lastname} "
                  f"{player.first_name} {player.birth_date}"
                  f" {player.ranking}"
                  )
        print("\n")

    def _error(self, error_name):
        if "player_name_exist" in error_name:
            print("le player name already exist\n")

        if "tournament_id" in error_name:
            print("The tournament id was not found!!\n")
        if "player_id" in error_name:
            print("Error on player id")
        if "player_not_removed" in error_name:
            print("Player not removed")
        if "tournament_not_removed" in error_name:
            print("Tournament not removed")

    def response_input(self):
        print('tapez le numero du tournois a supprimer')
        return input()

    def _base_menu(self):
        print("Hi, Welcome to tournament chess app!\nType "
              "\n1 to load a tournament "
              "\n2 to create new tournament "
              "\n3 to add a player "
              "\n4 to remove a player "
              "\n5 to list all players "
              "\n6 to remove a tournament "
              "\n7 to list all tournaments "
              "\n8 update tournament "
              "\n9 List all player from tournament   "
              "\n10 List all round from tournament   "
              "\n0 to quit the app")

    def _tournaments_displays(self):
        print("ont load le tournament")

    def list_tournaments(self, tournaments):
        if isinstance(tournaments, list):
            for tournament in tournaments:

                print(
                    "tournament name ::  " + tournament.name,
                    "\ntournament place ::  " + tournament.place,
                    "\ntournament date ::  " + tournament.date,
                    "\ntournament description ::  " + tournament.description,
                    "\n tournament id ::  " + str(tournament.doc_id),
                    "\n----------------------------------------"
                    )
        else:
            print(
                "tournament name ::  " + tournaments.name,
                "\ntournament place ::  " + tournaments.place,
                "\ntournament date ::  " + tournaments.date,
                "\n tournament id ::  " + str(tournaments.doc_id),
                "\n----------------------------------------"
            )

    def _create_tournament_players(self):
        choice_list = []
        print(
            "\nWelcome to the tournament creator\n"
            "Please select your 8 players with her id displayed above\n"
            )
        i = 1
        while i <= 8:
            print(f"Type the number of player number {i} !")
            choice_list.append(input())
            i += 1
        return choice_list

    def create_tournament(self):
        tournament_info = {}
        print("Type the tournament name")
        tournament_info["name"] = input()
        print("Type the tournament place")
        tournament_info["place"] = input()
        print("Type the tournament date")
        tournament_info["date"] = input()
        print("Type the tournament time")
        tournament_info["time"] = input()
        print("Type the tournament description")
        tournament_info["description"] = input()

        return tournament_info

    def _update_tournament_menu(self):
        print(
            "\n1 to change name of tournament",
            "\n2 to change place of tournament",
            "\n3 to change date of tournament",
            "\n4 to change description of tournament",
            "\n5 to delete tournament",
            "\n6 to return on main menu",
              )

    def _update_tournament_menu_prompt(self):
        print("Type the tournament number that you want to select")
        return input()

    def change_tournament_prompt(self):
        print("You can input the change now")
        return input()

    def basic_input(self):
        return input()

    def add_score_to_match(self, tour: list):
        score_list = []
        match_list = list(tour)
        for match in match_list:
            print(f"Entrez le score pour ce match \n {match}")
            score_list.append(float(input()))
            score_list.append(float(input()))
        return score_list

    def players_modify_rank(self, players):
        i = 0
        for player in players:
            print(f"id : {i} {player.first_name} {player.lastname}"
                  f" current rank is : {player.ranking}")
            i += 1
        print("Choose your player by tiping his id")
        response = int(input())
        if(response < 0) or (response > 7):
            while (response < 0) or (response > 7):
                print("Bad id choose again")
                response = int(input())
        print(f"Okay you choose {players[response].lastname}"
              f" {players[response].first_name}")
        print("Type the rank that you want to atribute")
        players[response].ranking = input()
        print("The ranking is updated successfully")
        return players

    def do_you_want_modify_rank(self):
        print("Hi The turn is finished"
              " do you want to modify a rank from a player?\n"
              "If yes Type 1 otherwise type something else")
        response = str(input())
        if response == "1":
            return True
        else:
            return False

    def show_player_on_tournament(self, tournament):
        print("This is the list of players playing in this tournament")
        print("---------------------------------------\n")
        for player in tournament.players:
            print(f"{player.lastname} {player.first_name}")
            print(f"current rank: {player.ranking} point: {player.point}")
        print("---------------------------------------\n")
        return True

    def update_all_data_from_tournament(self, response):
        if response:
            print("tournament updated correctly")
        else:
            print("error while updating tournament")
        return response

    def do_you_want_save_tournament(self):
        print("Do you want save the tournament in actual state ?")
        print("Type 1 to say yes , type other key to say no")
        response = int(input())
        if response == 1:
            return True
        else:
            return False

    def display_all_round_or_match_from_tournament(self, round_list):
        i = 0
        x = 1
        r = 1  # round
        t = 1  # turn
        for round in round_list:
            print(f"match number {r} :")
            print(round[i]["lastname"] + " " + round[i]["first_name"] +
                  " point " + round[x]
                  )
            print(round[i+2]["lastname"] + " " + round[i+2]["first_name"] +
                  " point " + round[x+2]
                  )
            if (r % 4) == 0:
                print("-------------------------")
                print(f"Fin du tour numero {t}")
                print("-------------------------")
                t += 1
            r += 1

    def load_page(self, page_name: str, *args,):
        if page_name == "home":
            self._base_menu()
        elif page_name == "display_tournament":
            self._tournaments_displays()
        elif page_name == "create_tournament_players":
            return self._create_tournament_players()
        elif page_name == "list_tournament":
            self.list_tournaments(args[0])

        elif page_name == "update_tournament_menu":
            self._update_tournament_menu()
        elif page_name == "_update_tournament_menu_prompt":
            return self._update_tournament_menu_prompt()
        elif page_name == "change_tournament_prompt":
            return self.change_tournament_prompt()
        elif page_name == "add_player_view":
            return self.add_player_view(args[0])
        elif page_name == "player_successfully_added_or_not":
            # arg[0] is a boolean if added or not, arg[1] is player data
            return self.player_successfully_added_or_not(args[0], args[1])
        elif page_name == "remove_player":
            return self.remove_player(args[0])
        elif page_name == "display_all_players":
            return self.display_all_players(args[0])
        elif page_name == "display_all_players_from_tournament":
            return self.display_all_players_from_tournament(args[0])
        elif page_name == "create_tournament":
            return self.create_tournament()
        elif page_name == "success":
            return self.success(args[0])
        elif page_name == "add_score_to_match":
            return self.add_score_to_match(args[0])
        elif page_name == "players_modify_rank":
            return self.players_modify_rank(args[0])
        elif page_name == "do_you_want_modify_rank":
            return self.do_you_want_modify_rank()
        elif page_name == "show_player_on_tournament":
            return self.show_player_on_tournament(args[0])
        elif page_name == "update_all_data_from_tournament":
            return self.update_all_data_from_tournament(args[0])
        elif page_name == "do_you_want_save_tournament":
            return self.do_you_want_save_tournament()
        elif page_name == "display_all_round_or_match_from_tournament":
            return self.display_all_round_or_match_from_tournament(args[0])
        elif page_name == "basic_input":
            return self.basic_input()
        elif page_name == "error":
            self._error(args)

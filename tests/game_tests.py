import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        self.gametype = GameType()
        self.gametype.label = "Board game"
        self.gametype.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "description": "You move around the game board (a mansion), as of one of the game's six suspects, collecting clues from which to deduce which suspect murdered the game's perpetual victim: Mr. Boddy (Dr. Black, outside of U.S.), and with which weapon and in what room.",
            "title": "Clue",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["description"], "You move around the game board (a mansion), as of one of the game's six suspects, collecting clues from which to deduce which suspect murdered the game's perpetual victim: Mr. Boddy (Dr. Black, outside of U.S.), and with which weapon and in what room.")
        self.assertEqual(json_response["number_of_players"], 6)
        self.assertEqual(json_response["game_type"]["id"], 1)
        self.assertEqual(json_response["gamer"]["id"], 1)

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.game_type = self.gametype
        game.description = "You move around the game board (a mansion), as of one of the game's six suspects, collecting clues from which to deduce which suspect murdered the game's perpetual victim: Mr. Boddy (Dr. Black, outside of U.S.), and with which weapon and in what room."
        game.title = "Monopoly"
        game.number_of_players = 4
        game.gamer_id= 1

        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["description"], "You move around the game board (a mansion), as of one of the game's six suspects, collecting clues from which to deduce which suspect murdered the game's perpetual victim: Mr. Boddy (Dr. Black, outside of U.S.), and with which weapon and in what room.")
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["game_type"]["id"], 1)
        self.assertEqual(json_response["gamer"]["id"], 1)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.game_type = self.gametype
        game.description = "Players move their three or four pieces around the board, attempting to get all of their pieces home before any other player"
        game.title = "Sorry"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameTypeId": 1,
            "description": "Players move their three or four pieces around the board, attempting to get all of their pieces home before any other player",
            "title": "Sorry",
            "numberOfPlayers": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["description"], "Players move their three or four pieces around the board, attempting to get all of their pieces home before any other player")
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["game_type"]["id"], 1)
        self.assertEqual(json_response["gamer"]["id"], 1)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.game_type = self.gametype
        game.description = "Players move their three or four pieces around the board, attempting to get all of their pieces home before any other player"
        game.title = "Sorry"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
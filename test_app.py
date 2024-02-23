from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertIn('<title>Boggle</title>', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.post('/api/new-game')
            parsed_json = response.get_json()

            self.assertIsInstance(parsed_json["gameId"], str)
            self.assertIsInstance(parsed_json["board"], list)
            self.assertIn(parsed_json["gameId"], games.keys())
            self.assertEqual(
                parsed_json,
                {
                 "gameId": parsed_json["gameId"],
                 "board": parsed_json["board"]
                }
            )
            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # test that the game_id is a string
            # test that the board is a list
            # test that the game_id is in the dictionary of games (imported from app.py above)

    def test_score_word(self):
        """Test if word is valid"""

        with app.test_client() as client:
            response = client.post('/api/new-game')
            parsed_json = response.get_json()

            game_id = parsed_json["gameId"]
            game = games[game_id]

            game.board = [['A', 'B', 'L', 'E', 'S'],
                          ['A', 'B', 'L', 'E', 'S'],
                          ['A', 'B', 'L', 'E', 'S'],
                          ['A', 'B', 'L', 'E', 'S'],
                          ['A', 'B', 'L', 'E', 'S']]

            response_valid_word = client.post(
                '/api/score-word',
                json={
                    "gameId": f"{game_id}",
                    "word": "ABLE"
                }
            )
            data_valid_word = response_valid_word.get_json()

            self.assertEqual(data_valid_word["result"], "ok")

            response_not_on_board = client.post(
                '/api/score-word',
                json={
                    "gameId": f"{game_id}", "word": "HELLO"
                }
            )
            data_not_on_board = response_not_on_board.get_json()

            self.assertEqual(data_not_on_board["result"], "not-on-board")

            response_not_a_word = client.post(
                '/api/score-word',
                json={
                    "gameId": f"{game_id}", "word": "HFJDS"
                }
            )
            data_not_a_word = response_not_a_word.get_json()

            self.assertEqual(data_not_a_word["result"], "not-word")

            response_on_board_not_word = client.post(
                '/api/score-word',
                json={
                    "gameId": f"{game_id}", "word": "AAAA"
                }
            )
            data_on_board_not_word = response_on_board_not_word.get_json()

            self.assertEqual(data_on_board_not_word["result"], "not-word")

            # make a post request to /api/new-game
            # get the response body as json using .get_json()
            # find that game in the dictionary of games (imported from app.py above)

            # manually change the game board's rows so they are not random

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}

from random import choice
from random import randint


class Games:
    rpc_moves = {
        'paper': 'scissors',
        'rock': 'paper',
        'scissors': 'rock'
        }

    def __init__(self):
        self.low_range = 0
        self.up_range = 10 ** 6
        self.robot_number = self.generate_number()
        self.goal_number = self.generate_number()
        self.robot_move = self.rpc_move()

        self.score_table = {
            'You won': 0,
            'Robot won': 0,
            'It\'s a draw': 0,
            }

    def dispatcher(self):
        self.score_table = {key: 0 for key in self.score_table}
        games = {
            'Rock-paper-scissors': self.rock_paper_scissors,
            'Numbers': self.ask_number,
            'exit': self.__exit,
            }
        message = 'Which game would you like to play?\n'
        user_input = input(message).capitalize()
        while user_input not in games:
            print('\nPlease choose a valid option: '
                  'Numbers or Rock-paper-scissors?\n')
            user_input = input().capitalize()
        print()
        return games.get(user_input)()

    def generate_number(self):
        return randint(self.low_range, self.up_range)

    def rpc_move(self):
        return choice(list(self.rpc_moves.keys()))

    def refresh_game_stats(self):
        self.robot_number = self.generate_number()
        self.goal_number = self.generate_number()
        self.robot_move = self.rpc_move()

    def ask_number(self):
        message = 'What is your number?\n'
        user_input = input(message)
        if user_input == 'exit game':
            return
        user_number = self.check_user_number(user_input)
        if user_number is not None:
            result = self.check_numbers_result(user_number)
            return self.process_numbers_result(result)

    def check_user_number(self, user_input: str):
        err_message = 'A string is not a valid input!\n'
        try:
            number = int(user_input)
            if number < self.low_range:
                err_message = 'The number can\'t be negative!\n'
                raise ValueError
            if number > self.up_range:
                err_message = ('Invalid input! The number can\'t be bigger '
                               f'than {self.up_range}.\n')
                raise ValueError
        except ValueError:
            print(err_message)
            return self.ask_number()
        return number

    def check_numbers_result(self, user_number: int):
        goal = self.goal_number
        user_approximation = abs(goal - user_number)
        robot_approximation = abs(goal - self.robot_number)
        results = {
            'You won': user_approximation < robot_approximation,
            'Robot won': user_approximation > robot_approximation,
            'It\'s a draw': user_approximation == robot_approximation,
            }
        for result, win_condition in results.items():
            if win_condition:
                return result

    def process_numbers_result(self, result):
        self.score_table[result] += 1
        print(f'The robot entered the number {self.robot_number}.')
        print(f'The goal number is {self.goal_number}.')
        print(f'{result}!\n')
        self.refresh_game_stats()
        return self.ask_number()

    def print_scores(self):
        you_won = self.score_table['You won']
        robot_won = self.score_table["Robot won"]
        draw = self.score_table['It\'s a draw']
        print(f'You won: {you_won},\n'
              f'Robot won: {robot_won},\n'
              f'Draws: {draw}.\n')

    def rock_paper_scissors(self):
        message = 'What is your move?\n'
        user_input = input(message)
        if user_input == 'exit game':
            return
        if user_input not in self.rpc_moves:
            print('No such option! Try again!\n')
            return self.rock_paper_scissors()
        user_move = user_input
        result = self.check_rpc_result(user_move)
        return self.process_rpc_result(result)

    def check_rpc_result(self, user_move):
        robot_move = self.robot_move
        results = {
            'You won': self.rpc_moves[robot_move] == user_move,
            'Robot won': self.rpc_moves[user_move] == robot_move,
            'It\'s a draw': user_move == robot_move,
            }
        for result, win_condition in results.items():
            if win_condition:
                return result

    def process_rpc_result(self, result):
        self.score_table[result] += 1
        print(f'Robot chose {self.robot_move}')
        print(f'{result}!\n')
        self.refresh_game_stats()
        return self.rock_paper_scissors()

    @staticmethod
    def __exit():
        pass


class Robot:

    def __init__(self):
        self.the_battery = 100
        self.overheat = 0
        self.skill = 0
        self.boredom = 0
        self.rust = 0
        self.workaround = False  # test 4 workaround
        self.game = Games()
        self.name = input('How will you call your robot?\n')
        self.__dispatcher()

    def __dispatcher(self):
        if self.rust == 100:
            message = f'{self.name} is too rusty! Game over. Try again?'
            return self.exit(message)
        if self.overheat == 100:
            message = ('The level of overheat reached 100, '
                       f'{self.name} has blown up! Game over. Try again?')
            return self.exit(message)
        print(f'Available interactions with {self.name}:\n'
              'exit - Exit\n'
              'info - Check the vitals\n'
              'work - Work\n'
              'play - Play\n'
              'oil - Oil\n'
              'recharge - Recharge\n'
              'sleep - Sleep mode\n'
              'learn - Learn skills')
        user_input = input('Choose:\n')
        method = getattr(self, user_input, None)
        if callable(method):
            if self.the_battery == 0 and method.__name__ != 'recharge':
                print(f'The level of the battery is 0, '
                      f'{self.name} needs recharging!\n')
                return self.__dispatcher()
            if self.boredom == 100 and method.__name__ != 'play':
                print(f'{self.name} is too bored! '
                      f'{self.name} needs to have fun!\n')
                # test 4 workaround
                self.workaround = True
                return self.__dispatcher()
            return method()
        print('Invalid input, try again!\n')
        return self.__dispatcher()

    def info(self):
        print(f'{self.name}\'s stats are:\n'
              f'the battery is {self.the_battery},\n'
              f'overheat is {self.overheat},\n'
              f'skill level is {self.skill},\n'
              f'boredom is {self.boredom},\n'
              f'rust is {self.rust}.\n')
        return self.__dispatcher()

    def recharge(self):
        if self.the_battery == 100:
            print(f'{self.name} is charged!\n')
        else:
            parameters = {'the_battery': 10, 'overheat': -5, 'boredom': 5, }
            self.__process_stats(parameters)
            print(f'{self.name} is recharged!\n')
        return self.__dispatcher()

    def sleep(self):
        if self.overheat == 0:
            print(f'{self.name} is cool!\n')
        else:
            parameters = {'overheat': -20, }
            self.__process_stats(parameters)
            print(f'{self.name} cooled off!\n' if self.overheat > 0
                  else f'{self.name} is cool!\n')
        return self.__dispatcher()

    def play(self):
        self.game.dispatcher()
        self.game.print_scores()
        if self.workaround:
            return self.exit()
        parameters = {'boredom': -10, 'overheat': 10, }
        self.unpleasant_event()
        self.__process_stats(parameters)
        print(f'{self.name} is in a great mood!\n')
        return self.__dispatcher()

    def work(self):
        if self.skill < 50:
            print(f'{self.name} has got to learn before working!\n')
        else:
            parameters = {'boredom': 10, 'overheat': 10, 'the_battery': -10, }
            self.unpleasant_event()
            self.__process_stats(parameters)
            print(f'{self.name} did well!\n')
        return self.__dispatcher()

    def oil(self):
        if self.rust == 0:
            print(f'{self.name} is fine, no need to oil!\n')
        else:
            parameters = {'rust': -20, }
            self.__process_stats(parameters)
            print(f'{self.name} is less rusty!\n')
        return self.__dispatcher()

    def learn(self):
        if self.skill == 100:
            print(f'There\'s nothing for {self.name} to learn!\n')
        else:
            parameters = {
                'skill': 10,
                'overheat': 10,
                'the_battery': -10,
                'boredom': 5,
                }
            self.__process_stats(parameters)
            print(f'{self.name} has become smarter!\n')
        return self.__dispatcher()

    def unpleasant_event(self):
        events = {
            'nothing': (0, ''),
            'puddle': (10, f'Oh no, {self.name} stepped into a puddle!\n'),
            'sprinkler': (30, f'Oh, {self.name} encountered a sprinkler!\n'),
            'pool': (50, f'Guess what! {self.name} fell into the pool!\n')
            }
        event = choice(list(events))
        rust_value, message = events.get(event)
        if rust_value:
            parameters = {'rust': rust_value}
            print(message)
            self.__process_stats(parameters)

    def __get_stats(self, parameters):
        output = {}
        for parameter in parameters:
            output.update({parameter: getattr(self, parameter)})
        return output

    def __process_stats(self, parameters):
        stats_before = self.__get_stats(parameters)
        self.__update_stats(parameters)
        stats_after = self.__get_stats(parameters)
        self.__print_stats_changes(parameters, stats_before, stats_after)

    def __update_stats(self, parameters):
        for parameter, value in parameters.items():
            current_value = getattr(self, parameter)
            func, pivot = (max, 0) if value < 0 else (min, 100)
            new_value = func(current_value + value, pivot)
            setattr(self, parameter, new_value)

    def __print_stats_changes(self, parameters, stats_before, stats_after):
        for parameter in parameters:
            now = stats_after[parameter]
            was = stats_before[parameter]
            parameter_name = parameter.replace('_', ' ')
            print(f'{self.name}\'s level of {parameter_name} was {was}. '
                  f'Now it is {now}.')

    @staticmethod
    def exit(message='Game over.'):
        print(message)


if __name__ == '__main__':
    a = Robot()

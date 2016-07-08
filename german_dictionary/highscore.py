from german_dictionary.quiz import Quiz
from german_dictionary.db_handler import DatabaseHandler
from datetime import datetime


class HighScore:
    def __init__(self, name, quiz):
        self.name = name
        self.quiz = quiz
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {'Name': self.name, 'Date': self.date, 'Score': self.quiz.score,
                'Questions': self.quiz.answers,
                'Description': "{} with {}".
                format(', '.join(self.quiz.parts_of_speech),
                       ', '.join(self.quiz.fields_to_be_guessed))}

    def add_high_score(self, database):
        DatabaseHandler.add_highscore(self.to_dict(), database)

    def __lt__(self, other):
        return self.quiz.score < other.quiz.score

    @classmethod
    def high_score_fields(self):
        return ('Name', 'Date', 'Score', 'Questions', 'Description')

    @classmethod
    def extract_all_high_scores(self, database):
        return DatabaseHandler.extract_all_high_scores(database)

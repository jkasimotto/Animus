
class Instruction:
    def __init__(self,
                 tf_questions,
                 tf_answers,
                 directions,
                 directions_tf_criteria,
                 directions_tf_answers):
        self.tf_questions = tf_questions
        self.tf_answers = tf_answers
        self.directions = directions
        self.directions_tf_criteria = directions_tf_criteria
        self.directions_tf_answers = directions_tf_answers

    def __str__(self) -> str:
        return f"Instruction({self.tf_questions}, {self.tf_answers}, {self.directions})"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self):
        return {
            "tf_questions": self.tf_questions,
            "tf_answers": self.tf_answers,
            "directions": self.directions,
            "directions_tf_criteria": self.directions_tf_criteria,
            "directions_tf_answers": self.directions_tf_answers
        }

import logging
import os

from weasyprint import HTML
from collections import Counter

logger = logging.getLogger("meeting")



class Meeting:
    KEYS = [
        "speakers",
        "evaluators",
        "hot",
        "humor",
    ]

    def __init__(self):
        self.speakers = list()
        self.evaluators = list()
        self.hot = list()
        self.humor = list()

    def update(self, data):
        for key in self.KEYS:
            if key in data: 
                logger.debug(f"Updating {key} with {data[key]}")

                setattr(self, key, list(data[key]))


    def json(self):
        return {
            "speakers": self.speakers,
            "evaluators": self.evaluators,
            "hot": self.hot, 
            "humor": self.humor
        }

    def __str__(self):
        meeting_str = ""

        for key in self.KEYS:
            meeting_str += f"{key}: {getattr(self, key)}\n"

        return meeting_str



class Voting:
    def __init__(self):
        self.speakers = Counter()
        self.evaluators = Counter()
        self.hot = Counter()
        self.humor = Counter()

    def update(self, attr, value):
        getattr(self, attr).update([value])

    def json(self):
        return {
            "speakers": dict(self.speakers),
            "evaluators": dict(self.evaluators),
            "hot": dict(self.hot),
            "humor": dict(self.humor)
        }
        

class Feedback:
    def __init__(self):
        self.speakers = {}

    def update(self, speaker, data):
        if speaker not in self.speakers:
            for key in data:
                data[key] = [data[key]]

            self.speakers[speaker] = data

            return

        updated_data = self.speakers[speaker]

        for key in data:
            value = data[key]

            if key in updated_data:
                updated_data[key].append(value)
            else:
                updated_data[key] = [value]

        self.speakers[speaker] = updated_data

    def json(self):
        return self.speakers
    


class PDF:
    HEADER = """
    <h1>Informacja zwrotna dla {0}</h1> <br/><br/><br/>
   """

    QUESTION = """
        <h3>{0}</h3>
    """

    ANSWER = """
        <p>{0}</p>
    """

    BREAK = "<br/>"

    def __init__(self, speaker, data):
        self.speaker = speaker
        self.data = data

    def get(self):
        html = self.HEADER.format(self.speaker)

        for question in self.data:
            html += self.QUESTION.format(question)

            for answer in self.data[question]:
                html += self.ANSWER.format(answer)

            html += self.BREAK + self.BREAK

        pdf_file = f"{self.speaker}.pdf"

        HTML(string=html).write_pdf(pdf_file)

        with open(pdf_file, "rb") as f:
            return f.read()

        # TODO: 
        #os.remove(pdf_file)
    

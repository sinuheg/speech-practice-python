import pyttsx3
import speech_recognition as sr

from utilities import clean_phrase

class Phrase:
    def __init__(self, phrase):
        d = dict()
        self.phrase = phrase
        self.clean_phrase = clean_phrase(phrase)
        self.tries = 0
        self.utterances = []
    def __str__(self):
        lines = []
        lines.append(f'Phrase: {self.phrase}')
        lines.append(f'Tries:  {self.tries}')
        lines.append(f'Utterances: ')
        for utterance in self.utterances:
            lines.append(f'        {utterance}')
        return '\n'.join(lines)

class Sequence:
    def __init__(self, total):
        self.total = total
        self.deck = set(range(total))
        self.current = -1
    def next(self):
        self.current += 1
        if self.current >= self.total:
            self.current = 0
        return self.current

    def count(self):
        return len(self.deck)

def load_phrases():
    filename = 'lines.txt'
    f = open(filename, 'r+')
    lines = f.readlines()
    f.close()
    processed_lines = []
    for line in lines:
        clean_line = line.replace('\n','').replace('\r','')
        processed_lines.append(Phrase(clean_line))
    return processed_lines

phrases = load_phrases()

TRIES = 3

def practice():
    engine = pyttsx3.init()
    r = sr.Recognizer()
    m = sr.Microphone()
    sequence = Sequence(len(phrases))

    active = True
    while active and sequence.count() > 0:
        phrase = phrases[sequence.next()]
        correct = False
        while not correct and phrase.tries < TRIES:

            print()
            print('Please repeat after me...')
            print(phrase.phrase)
            engine.say(phrase.phrase)
            engine.runAndWait()

            print("Now your turn")
            print("🎤")
            with m as source: audio = r.listen(source=source, phrase_time_limit=10)
            print("Got it! Now to recognize it...")
            phrase.tries += 1
            try:
                value = r.recognize_google(audio)
                phrase.utterances.append(value)
                if clean_phrase(value) == phrase.clean_phrase:
                    print('Correct!!!!!!!!!!')
                    print()
                    correct = True
                else:
                    print('NOT correct!')
                    print('See the differences:')
                    print('    Me:  ', phrase.phrase)
                    print('    You: ', value)
                    print()
                    print("Let's try again...")
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            
            if not correct:
                typed = input("Press Enter to continue...")
                if typed == 'e':
                    active = False
    
    for phrase in phrases:
        if phrase.tries:
            print()
            print(phrase)

practice()
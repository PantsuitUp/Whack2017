import pyttsx

engine = pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty("rate", 140)

voice = voices[39]
engine.setProperty('voice', voice.id)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()


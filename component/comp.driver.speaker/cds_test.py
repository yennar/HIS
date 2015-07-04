import pyttsx

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-60)
engine.say('hello! This is Julia. Warning! Temperature over threadhold. 40 degrees Celsius')
engine.runAndWait()
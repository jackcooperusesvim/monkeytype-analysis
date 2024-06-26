# CATCHY TITLE - A Data-Driven Analysis of Typing Speed


### The TL;DR - Improve Typing Speed

The goal of this project was to gather, clean, and analyze information to bring direction to my practice so I can find an effective and efficient method to improve my speed. The following are the specific questions regarding data-approachable aspects of typing practice which I sought to answer at the beginning of the project, as well as a quick summary of their respective data-driven answers.

#### Q1: Is it better for improvement to type faster and correct mistakes, or to type slower and ensure proper keystrokes?
##### A1: TODO

#### Q2: Does learning an alternate layout make you progress faster or slower?
##### A2: TODO

#### Q3: How fast can I expect to improve over the next month and year
##### A3: TODO

#### Q4: Is any sort of mental fatigue affecting my typing speed?
##### A4: TODO

#### Q5: How much does the time typing recently affect my typing speed? Is there a "warming up" period?
##### A5: TODO

### Gathering the Data

This data comes from MonkeyType.com, where I have practicing typing for over a year. Unfortunately, not all of the data in that year is available, since I did not create an account until December of ____, but thankfully there remains enough data gathered since then that I have plenty of records. The actual sourcing of the data can be done by downloading a .csv from the profile section. In a future iteration, I would like to scrape the individual test data, but that is beyond my current scope, and involves some heavy javascript-ing which I am not totally up for.

### Understanding the Data

This data is very rich and has a lot of useful information. The following are a summary of each column. Each record is an individual typing test

* _id: Unique Test Identifier (integer stored as object)
* isPb: Is a Personal Best (boolean stored as an object [True or NaN])
* wpm: Words Per Minute of the test not counting erronous typing (float rounded to the 0.01)
* rawWpm: Words Per Minute speed of each individual word that was typed (array of floats rounded to the 0.01)
* consistency: A MonkeyType measurement of how consistent your typing speed is. I do not know how this is calculated. (float64)
* charStats: A string which describes performance on each word in the form of  wpm;incorrectletters;extraletters;missed. Here the variables of extraletters and missed letters refer to letters either typed after typing the length of the word, or letters missed by typing space too early.
* mode and mode2: The type of mode of the test. time indicates a time limit, the length of which is described in mode2, and word indicates a word count to be reached, which is also described in mode2. Quote is a version of word which is usually a pop culture quote, and zen has no time limit or word count, and you can type whatever you want. (object)
* quoteLength: I do not know what this is. I assume it has something to do with the "quote" mode on MonkeyType, but even so, I don't use that mode and I only have 2 unique values of 1 and -1, so I don't plan on using it.
* restartCount: This is how many restarts were used to take this test (int)
* testDuration: represents the length in time of the test (float)
* afkDuration: represents how long during a test the user was predicted to be AFK (Away From Keyboard) (float)
* incompleteTestSeconds: Some variation of afkDuration which I don't quite understand.
* punctuation: Was puncuation available on the test? (Boolean)
* numbers: Were numbers available on the test? (Boolean)
* language: Language typed in as a string (string)
* funbox: Related to some other mode??? (none)
* difficulty: Level of word difficulty typed on the test (string: {"normal"})
* lazyMode: Is Lazy Mode enabled for this test? (boolean)
* blindMode: Is blind Mode enabled for this test? (boolean)
* bailedOut: Did you bail out of the test? (boolean)
* tags: IDK, its always (NaN)
* timestamp: some long number. Maybe units? (int)

### Answering the Questions

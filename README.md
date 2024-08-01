# Slow is smooth, smooth is fast - A data driven mini-study of typing speed with MonkeyType

## Introduction

When I started taking programming seriously (~ 3 years ago), I was not a great programmer. Forget that, I wasn't even a good typist. I remember once it took me a full 10 minutes to find my backslash key to type "/n". In 2022 I decided that this had to change. I started doing typing practice and typing tests. Over the course of a year I improved from 40 words per minute while staring at the keyboard to 75 words per minute, typed with my head looking at the computer screen in front of me. But that was it. I had hit a limit, and no matter how much harder I tried, I felt I couldn't consistently pass that limit.

That is, until 8 months ago when I watched some youtube videos which reccomended that I type slower and focus on accuracy. I thought this was interesting because it drew a parallel to another area of my life: the guitar.

When you have to learn a particularly hard or fast lick on the guitar, the general consensus is that the best way to practice it after you get the pattern in your head, is to play the lick slowly and __perfectly__. The reasoning behind this is that playing it perfectly and consistently engrains a much more *exact* pattern into your muscle memory than faster, more uncontrolled practice. This results in far better playing in the long run. My theory was that typing, being a similar patterned movement of the fingers, is probably similar.

I decided to start practicing more intentionally, and start focusing more on accuracy, and over the course of those 8 months I have improved massively going from an average of ~75 words per minute to my current average of 96 words per minute (and climbing). 

Recently, I discovered that MonkeyType, one of the websites that I use to test and practice typing, has a feature which allows you to download data from all typing tests on your account. Being a Data Analyst, I was intrigued and decided to do a little digging to see exactly how the idea of "slow is smooth, smooth is fast" applied to typing. Should I be going for maximum accuracy or is there some level of acceptable error? If I decide mid-way through a test to abandon it and try another test, does that mean make my reported wpm unreasonably high?

## Analysis


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

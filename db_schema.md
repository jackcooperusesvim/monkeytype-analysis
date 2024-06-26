# Database Structure

Because I want to be able to easily import new data later for updated analysis and to keep track of my progress, as well as filtering out the current non-representative data, I am going to create a database of all my tests. Is this strictly necessary? No, but it is going to make it easier to think about and work with individual test data in the future when I include per-word analysis too.
Also I feel like flexing some SQL right now.




TABLES:
    Tests:
        id (monkeytype assigned id) TEXT
        timestamp INTEGER
        is_Pb BOOLEAN -- NOTE: In Sqlite3, BOOLEAN is just a blank INTEGER subclass. Basically the same thing
        wpm DECIMAL
        consistency DECIMAL
        mode TEXT
        mode2 TEXT
        restartCount INTEGER
        testDuration DECIMAL
        afkDuration DECIMAL
        incompleteTestSeconds DECIMAL
        bailedOut BOOLEAN
        incorrect_letters
        extra_letters
        missed
    Words:
        test_id (foreign key)
        wpm

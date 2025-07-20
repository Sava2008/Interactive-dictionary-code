# Interactive-dictionary v1.2.2

## Random remarks
allows to learn foreign vocabulary by spelling the words.
There are currently three modes in the dictionary application: addition mode, practice mode and search mode.
It is currently recommended to learn one language at a time via this app, to establish that the user is not to get tangled, however it is totally acceptable, since multilingualism cannot affect the app's functionality in any way.
Features such as a faster input, full-fledged multilingualism and bug tracking are planned in future updates, so stay tuned. Any suggestions on improving the app are going to be considered.

### What was added
1. Vocabulary table in the search mode is slightly more optimized.
2. Redundant widgets that had overloaded the interface were removed.
3. The code was completely rewritten in favor of simplicity and readability. No unnecessary nesting is present in the code anymore. The code has become overall more pythonic and explicit.
4. Critical errors and bugs were patched.

### Credits
Programming language - Python 3.13.5
Developer - Sava2008

## ADDITION MODE
This mode has two entries, one for foreign words unknown to the user, and the other for translation to the language familiar to them with intrinsic placeholders.
The user must press the "Submit word" button after typing each word pair. After all the needed words are submitted, the user presses "Main menu" and new vocabulary will be added to the "dict.json" automatically.
There is a "spare_dict.json" file where all data is collected in case some bug occurs and influences the "dict.json" file. Deletion is not actualized yet.
The user can also add words manually in the "dict.json" file, adhering to the "object" json type.

## PRACTICE MODE
This mode's name is self-explanatory. It has two types: the main and the local. Both have a label which represents a translation, an entry which accepts the corresponding foreign word, the "Submit word" button that checks the user's answer when pressed and the "Main menu" button which transmits the user back to the menu and scores their result. 
The main practice mode grabs a random word from the "dict.json" and examines the user. The local practice is accessed via the search mode, which is mentioned below.

## SEARCH MODE
The search mode offers querying the main dictionary, then manipulating that data. Initially, the user faces an entry for input. Words in either language might be passed into the field and the quetied words will appear. This prompt might as well be left empty. Subsequently, the frame with a list of words will appear, accounting the user query. In case the input is empty, every word will be displayed. 
I also implemented a feature exceptionally for German language, where if a word is searched without an article, it will emerge anyway (e.g. both "Der Frühling", "Frühling" and "frühling" would work). 
The words are presented as checkbuttons. The program currently has two operations with the words in this mode: deletion and practice.
Practice works exactly as mentioned above, aside from that in this case only selected words, which may help the user polish their awareness of concrete vocabulary. After exitting practice, the app will return the user's score in percent format, rounded to tenths.
Deletion is achieved by checking unnecessary prompts and pressing "Remove". The whole frame is updated in order to prevent any interaction with removed units.
In addition the user can refresh printed vocabulary by passing in a word or the beginning of the word into the entry and pressing "Sumbit word".

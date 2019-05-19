# Redemption Splits Bot
This discord bot automatically pulls and updates information regarding OSRS splits for members of the clan Redemption PMV using their dedicated Google doc. 

---

## Main Discord Commands:

### **!splits (player)**:
Finds the player (by their RSN) and get's their split value. The search for the user is a bit forgiving for spelling errors. 

### **!update (player), (amount), (items)**
This command requires the bot admin rank.
Finds the player and adds the amount specified in <amount>. This can be a negative number if you wish to reduce their split. 
  
You can also add items or a list of items under <item>. This is entirely optional, and can basically be anything. 
  
When using this command, make sure the number put in for <amount> is just a raw number with no symbols or commas.
  
> !update Jagex, 500000

> !update Jagex, 500000, Swords x3, Cabbage x4

### **!add (player), (split), (date), (items)**
This command requires the bot admin rank.

This adds the player to the end of the spreadsheet, as well as the specified split value, date, and items. 

Note that the last three are completely optional. If you just wish to add a player to the list, you can just specify their RSN.

> !add Jagex - This will add the player Jagex with a split value of 0 and today's join date.

> !add Jagex, 5000000, 1/1/2019 - This will add the player Jagex with a split value of 5,000,000 and join date of Jan 1, 2019.

> !add Jagex, 5000000, 1/1/2019, Swords x3, Cabbage x4 - Same as above but will also add the items specified at the end.

Splits must follow the number format specified in !update. Dates must be of the form M/D/YYYY (following American date format)
Note that while split, date, and items are optional, if you wish to add any of them they must be added in that order and you can't skip an option. For example, say you wanted to add a player who joined last month, but they dont have any split value, must add the split in the command or it will not work.

> !add Jagex, 1/1/2019 - This is INVALID

> !add Jagex, 0, 1/1/2019 - This is VALID

### **!help**
Posts the commands in chat.

---

# Spreadsheet Requirements
The bot was designed for a specific spreadsheet format and must meet the following requirements:

1. RNS need to be in Column A

2. Split Values need to be in Column B

3. Item Names need to be in Column C

4. Clan Join Dates need to be in Column D

Additionally, there should be blank rows below so that additional members can be added. These rows at the very least should have =TODAY() under the clan join date as the bot copies and pastes that when adding a user without a specific join date. 

---

# Setting up the bot

<ADD BELOW>










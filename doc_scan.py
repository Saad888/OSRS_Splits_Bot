import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
from fuzzywuzzy import process as fuzzy_process
import string


class DocScanner:
    """Doc Scanner Object"""

    def __init__(self, ss_name, ws_name):
        """Initiates DocScanner class"""
        self.scope = [
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive'
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json', 
            self.scope
        )
        self.gc = gspread.authorize(self.creds)
        self.sheet = self.gc.open(ss_name).worksheet(ws_name)

    async def _fuzzy_search(self, name, splits_list=None):
        """Returns fuzzy search result for name (with index)"""
        if splits_list is None:
            splits_list = await self._get_all_splits()
        splits_names = [name[0] for name in splits_list if name[1] is not None]
        result = fuzzy_process.extractBests(name, splits_names, score_cutoff=90)
        if len(result) == 0:
            return None
        else:
            fuzz_name = result[0][0]
            return fuzz_name

    async def _exact_search(self, name, splits_list=None):
        """Does exact search for name"""
        if splits_list is None:
            splits_list = await self._get_all_splits()
        for i in range(len(splits_list)):
            if (splits_list[i][0] == name) and (splits_list[i][1] is not None):
                return i
        return -1

    async def _get_name_index(self, name, splits_list=None):
        """If list is passed, searches through it. Otherwise, creates list"""
        if splits_list is None:
            splits_list = await self._get_all_splits()
        fuzz_name = await self._fuzzy_search(name, splits_list)
        if fuzz_name is None:
            return -1
        else:
            index = await self._exact_search(fuzz_name, splits_list)
            return index 

    async def _get_all_splits(self):
        """Gets splits"""
        col1 = self.sheet.col_values(1)
        col2 = self.sheet.col_values(2)
        values = []
        for i in range(len(col1)):
            name = col1[i]
            try:
                amount = int(col2[i].replace(",", "").replace("$", ""))
            except (ValueError):
                amount = None
            values.append((name, amount))
        return values

    async def _copy_row_to_target(self, row, target_row):
        """Copies formula from row and pastes in target row"""
        alphabet = list(string.ascii_uppercase)
        empty_count = 0
        for c in alphabet:
            cell = c + str(row)
            value = self.sheet.acell(cell, value_render_option='FORMULA').value
            value = str(value)
            empty_count = empty_count + 1 if len(value) == 0 else 0
            if empty_count == 3:
                break
            target_cell = c + str(target_row)
            for i in alphabet:
                acell = i + str(row)
                target_acell = i + str(target_row)
                value = value.replace(acell, target_acell)
            self.sheet.update_acell(target_cell, value)

        

    async def _set_split(self, row, value):
        """Update split"""
        self.sheet.update_cell(row, 2, value)

    async def get_split(self, name):
        """Gets individual user split"""
        splits_list = await self._get_all_splits()
        index = await self._get_name_index(name, splits_list)
        return splits_list[index][1] if index != -1 else None

    async def update_split(self, name, delta):
        """Adds value of delta to name's split"""
        splits_list = await self._get_all_splits()
        index = await self._get_name_index(name, splits_list)
        if index >= 0:
            prev_val = splits_list[index][1]
            new_val = prev_val + delta
            await self._set_split(index + 1, new_val)
            return new_val, prev_val
        else:
            print("ERROR: Could not find name")
            return None, None

    async def add_user(self, name, splits=0):
        """Adds user"""

        splits_list = await self._get_all_splits()
        # Confirm if user exists
        check_exists = await self._exact_search(name, splits_list)
        if check_exists != -1:
            return None

        # If user does not exist, add to bottom with split
        max_row = len(splits_list) + 1
        self.sheet.update_cell(max_row, 1, name)
        self.sheet.update_cell(max_row, 2, 0)
        return name


    async def delete_user():
        """ADD COMMANDS"""
        pass





if __name__ == "__main__":
    test = DocScanner("Budget", "test")
    vals = asyncio.run(test._get_all_splits())

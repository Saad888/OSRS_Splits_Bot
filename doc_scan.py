import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
import time


class DocScanner:
    """Doc Scanner Object"""

    def __init__(self, ss_name, ws_name):
        """Initiates DocScanner class"""
        self.scope = [
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive'
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            'creds.json', 
            self.scope
        )
        self.gc = gspread.authorize(self.creds)
        self.sheet = self.gc.open(ss_name).worksheet(ws_name)

    async def get_splits(self):
        """Gets splits"""
        col1 = self.sheet.col_values(1)
        col2 = self.sheet.col_values(2)
        range_ = range(len(col1))
        values = [(col1[i], int(col2[i].replace(",", ""))) for i in range_]
        return values

    async def set_splits(self, row, value):
        """Update split"""
        self.sheet.update_cell(row, 2, value)

    async def get_name_ID(self, name, splits_list=None):
        """If list is passed, searches through it. Otherwise, creates list"""
        if splits_list is None:
            splits_list = await self.get_splits()
        for i in range(len(splits_list)):
            if splits_list[i][0] == name:
                return i
        return -1

    #ADD METHOD FOR UPDATING SHEET

if __name__ == "__main__":
    test = DocScanner("Budget", "test")
    vals = asyncio.run(test.set_splits(2, 100000))
    print(vals)



"""
conershop_scraper.utils.writer.csv
----------------------------------
"""

from csv import writer

from cornershop_scraper.utils.writer.base_writer import Writer


class CsvWriter(Writer):
    def __init__(self, file_path: str = ''):
        super(CsvWriter, self).__init__(file_path=file_path, extension='csv')

    def save_items(self, items, file_name, headers=None):
        headers_keys = headers.keys() if headers else list(items[0].__dict__.keys())
        headers_vals = headers.values() if headers else list(items[0].__dict__.keys())

        file_path = self.make_full_path(file_name=file_name)
        rows = self.apply_headers(items=items, headers_keys=headers_keys)
        with open(file_path, 'w', encoding='utf-8', newline='') as output_file:
            csv_writer = writer(output_file)
            csv_writer.writerow(headers_vals)
            csv_writer.writerows(rows)

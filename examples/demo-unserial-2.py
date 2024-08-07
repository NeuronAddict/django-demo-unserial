import hashlib
import pickle
import base64

if __name__ == '__main__':
    class CsvHandler:
        def __init__(self, csv_file: str):
            self.filename = csv_file
            self.file_handler = open(csv_file, 'rt')

        def content(self):
            return self.file_handler.read()

        def close(self):
            self.file_handler.close()

        # def __reduce__(self):
        #     return self.__class__, (self.filename,)

    csv = CsvHandler('test.csv')
    print(f'csv content: \n{csv.content()}')

    serialized = pickle.dumps(csv)
    print(f'serialized={serialized}')

    encoded = base64.b64encode(serialized)
    print(f'encoded={encoded}')

    # !!
    csv.close()

    deserialized: CsvHandler = pickle.loads(base64.b64decode(encoded))
    print(f'unserialized content: \n{deserialized.content()}')


    # m = hashlib.sha256()
    # m.update(encoded)
    # print(f'm.hexdigest={m.hexdigest()}')
    # print(f'b64 digest={base64.b64encode(m.hexdigest().encode()).decode()}')

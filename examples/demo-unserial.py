import hashlib
import pickle
import base64

if __name__ == '__main__':
    class Message:

        def __init__(self, message: str, author: str):
            self.message = message
            self.author = author

        def __repr__(self):
            return f'<Message: message={self.message}, author={self.author}>'

        # def __reduce__(self):
        #     return print, ('coucou',)

    message = Message('hello!', 'Miss Marple')
    print(f'message={message}')

    serialized = pickle.dumps(message)
    print(f'serialized={serialized}')

    encoded = base64.b64encode(serialized)
    print(f'encoded={encoded}')

    deserialized: Message = pickle.loads(base64.b64decode(encoded))
    print(f'unserialized={deserialized}')

    assert deserialized.message == message.message
    assert deserialized.author == message.author

    # m = hashlib.sha256()
    # m.update(encoded)
    # print(f'm.hexdigest={m.hexdigest()}')
    # print(f'b64 digest={base64.b64encode(m.hexdigest().encode()).decode()}')

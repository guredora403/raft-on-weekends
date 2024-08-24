import msgpack

class MessagePackSerializer:
    @staticmethod
    def pack(data):
        return msgpack.packb(data, use_bin_type=True)

    @staticmethod
    def unpack(data):
        return msgpack.unpackb(data, use_list=True, encoding='utf-8')
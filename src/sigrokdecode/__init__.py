'''
sigrokdecode module stub
'''

class Decoder:
    def put(self, start_sample, end_sample, output_id, data, /):
        raise NotImplementedError('This is a stub.')

    def register(self, output_type, /, proto_id=..., meta=None):
        raise NotImplementedError('This is a stub.')

    def wait(self, condition, /):
        raise NotImplementedError('This is a stub.')

    def has_channel(self, index, /):
        raise NotImplementedError('This is a stub.')


OUTPUT_ANN, OUTPUT_PYTHON, OUTPUT_BINARY, OUTPUT_LOGIC, OUTPUT_META = range(5)
SRD_CONF_SAMPLERATE = 10000

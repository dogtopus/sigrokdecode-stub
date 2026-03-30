class Decoder:
    def put(self, start_sample, end_sample, output_id, data, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        raise NotImplementedError()

    def register(self, output_type, proto_id, meta=None) -> None:
        '''
        Register a new output stream.
        '''
        raise NotImplementedError()

    def wait(self, condition) -> None:
        '''
        Wait for one or more conditions to occur.

        Returns the sample data at the next position where the condition
        is seen. When the optional condition is missing or empty, the next
        sample number is used. The condition can be a dictionary with one
        condition's details, or a list of dictionaries specifying multiple
        conditions of which at least one condition must be true. Dicts can
        contain one or more key/value pairs, all of which must be true for
        the dict's condition to be considered true. The key either is a
        channel index or a keyword, the value is the operation's parameter.

        Supported parameters for channel number keys: 'h', 'l', 'r', 'f',
        or 'e' for level or edge conditions. Other supported keywords:
        'skip' to advance over the given number of samples.
        '''
        raise NotImplementedError()

    def has_channel(self, index) -> bool:
        '''
        Check whether input data is supplied for a given channel.

        Argument: A channel index.
        Returns: A boolean, True if the channel is connected,
        False if the channel is open (won't see any input data).
        '''
        raise NotImplementedError()


OUTPUT_ANN, OUTPUT_PYTHON, OUTPUT_BINARY, OUTPUT_LOGIC, OUTPUT_META = range(5)
SRD_CONF_SAMPLERATE = 10000

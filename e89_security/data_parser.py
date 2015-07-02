from django.http.multipartparser import MultiPartParser, LazyStream, ChunkIter, Parser, FIELD, exhaust
from django.core.files.uploadhandler import StopUpload
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_text

class RawPostParser(MultiPartParser):

    def parse(self):
        """
        Parse the POST data and break it into a FILES MultiValueDict and a POST
        MultiValueDict.

        Returns a tuple containing the POST and FILES dictionary, respectively.
        """
        encoding = self._encoding
        handlers = self._upload_handlers

        # HTTP spec says that Content-Length >= 0 is valid
        # handling content-length == 0 before continuing
        if self._content_length == 0:
            return MultiValueDict(), MultiValueDict()

        # Create the data structures to be used later.
        self._post = MultiValueDict()

        # Instantiate the parser and stream:
        stream = LazyStream(ChunkIter(self._input_data, self._chunk_size))

        # Whether or not to signal a file-completion at the beginning of the loop.
        old_field_name = None
        counters = [0] * len(handlers)

        try:
            for item_type, meta_data, field_stream in Parser(stream, self._boundary):
                if old_field_name:
                    # We run this at the beginning of the next loop
                    # since we cannot be sure a file is complete until
                    # we hit the next boundary/part of the multipart content.
                    self.handle_file_complete(old_field_name, counters)
                    old_field_name = None

                try:
                    disposition = meta_data['content-disposition'][1]
                    field_name = disposition['name'].strip()
                except (KeyError, IndexError, AttributeError):
                    continue

                field_name = force_text(field_name, encoding, errors='replace')

                if item_type == FIELD:
                    # This is a post field, we can just set it in the post
                    data = field_stream.read()
                    self._post.appendlist(field_name, data)
                elif item_type == FILE:
                    # This is a file, ignoring...
                    continue
                else:
                    # If this is neither a FIELD or a FILE, just exhaust the stream.
                    exhaust(stream)
        except StopUpload as e:
            if not e.connection_reset:
                exhaust(self._input_data)
        else:
            # Make sure that the request data is all fed
            exhaust(self._input_data)

        return self._post
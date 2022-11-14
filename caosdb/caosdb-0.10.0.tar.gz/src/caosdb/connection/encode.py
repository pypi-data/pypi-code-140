# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#
# Original work Copyright (c) 2011 Chris AtLee
# Modified work Copyright (c) 2017 Biomedical Physics, MPI for Dynamics and Self-Organization
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""multipart/form-data encoding module.

This module provides functions that faciliate encoding name/value pairs
as multipart/form-data suitable for a HTTP POST or PUT request.

multipart/form-data is the standard way to upload files over HTTP
"""

__all__ = [
    'gen_boundary', 'encode_and_quote', 'MultipartParam', 'encode_string',
    'encode_file_header', 'get_body_size', 'get_headers', 'multipart_encode',
    'ReadableMultiparts',
]
from urllib.parse import quote_plus
from io import UnsupportedOperation
import uuid
import re
import os
import mimetypes
from email.header import Header


def gen_boundary():
    """Returns a random string to use as the boundary for a message."""
    return uuid.uuid4().hex


def encode_and_quote(data):
    """If ``data`` is unicode, return urllib.quote_plus(data.encode("utf-8"))
    otherwise return urllib.quote_plus(data)"""
    if data is None:
        return None

    return quote_plus(data)


class MultipartParam(object):
    """Represents a single parameter in a multipart/form-data request.

    ``name`` is the name of this parameter.

    If ``value`` is set, it must be a string or unicode object to use as the
    data for this parameter.

    If ``filename`` is set, it is what to say that this parameter's filename
    is.  Note that this does not have to be the actual filename any local file.

    If ``filetype`` is set, it is used as the Content-Type for this parameter.
    If unset it defaults to "text/plain; charset=utf8"

    If ``filesize`` is set, it specifies the length of the file ``fileobj``

    If ``fileobj`` is set, it must be a file-like object that supports
    .read().

    Both ``value`` and ``fileobj`` must not be set, doing so will
    raise a ValueError assertion.

    If ``fileobj`` is set, and ``filesize`` is not specified, then
    the file's size will be determined first by stat'ing ``fileobj``'s
    file descriptor, and if that fails, by seeking to the end of the file,
    recording the current position as the size, and then by seeking back to the
    beginning of the file.

    ``callback`` is a callable which will be called from iter_encode with (self,
    current_transferred, total), representing the current parameter, current amount
    transferred, and the total size.
    """

    def __init__(self,
                 name,
                 value=None,
                 filename=None,
                 filetype=None,
                 filesize=None,
                 fileobj=None,
                 callback=None):
        self.name = Header(name).encode()
        self.value = value
        if filename is None:
            self.filename = None
        else:
            bfilename = filename.encode("ascii", "xmlcharrefreplace")
            self.filename = bfilename.decode("UTF-8").replace('"', '\\"')

        self.filetype = filetype

        self.filesize = filesize
        self.fileobj = fileobj
        self.callback = callback

        if self.value is not None and self.fileobj is not None:
            raise ValueError("Only one of value or fileobj may be specified")

        if fileobj is not None and filesize is None:
            # Try and determine the file size
            try:
                self.filesize = os.fstat(fileobj.fileno()).st_size
            except (OSError, AttributeError, UnsupportedOperation):
                try:
                    fileobj.seek(0, 2)
                    self.filesize = fileobj.tell()
                    fileobj.seek(0)
                except BaseException:
                    raise ValueError("Could not determine filesize")

    def __cmp__(self, other):
        attrs = [
            'name', 'value', 'filename', 'filetype', 'filesize', 'fileobj'
        ]
        myattrs = [getattr(self, a) for a in attrs]
        oattrs = [getattr(other, a) for a in attrs]
        return cmp(myattrs, oattrs)

    def reset(self):
        """Reset the file object's read pointer."""
        if self.fileobj is not None:
            self.fileobj.seek(0)
        elif self.value is None:
            raise ValueError("Don't know how to reset this parameter")

    @classmethod
    def from_file(cls, paramname, filename):
        """Returns a new MultipartParam object constructed from the local file
        at ``filename``.

        ``filesize`` is determined by os.path.getsize(``filename``)

        ``filetype`` is determined by mimetypes.guess_type(``filename``)[0]

        ``filename`` is set to os.path.basename(``filename``)
        """

        return cls(
            paramname,
            filename=os.path.basename(filename),
            filetype=mimetypes.guess_type(filename)[0],
            filesize=os.path.getsize(filename),
            fileobj=open(filename, "rb"))

    @classmethod
    def from_params(cls, params):
        """Returns a list of MultipartParam objects from a sequence of name,
        value pairs, MultipartParam instances, or from a mapping of names to
        values.

        The values may be strings or file objects, or MultipartParam
        objects. MultipartParam object names must match the given names
        in the name,value pairs or mapping, if applicable.
        """
        if hasattr(params, 'items'):
            params = params.items()

        retval = []
        for item in params:
            if isinstance(item, cls):
                retval.append(item)
                continue
            name, value = item
            if isinstance(value, cls):
                assert value.name == name
                retval.append(value)
                continue
            if hasattr(value, 'read'):
                # Looks like a file object
                filename = getattr(value, 'name', None)
                if filename is not None:
                    filetype = mimetypes.guess_type(filename)[0]
                else:
                    filetype = None

                retval.append(
                    cls(name=name,
                        filename=filename,
                        filetype=filetype,
                        fileobj=value))
            else:
                retval.append(cls(name, value))
        return retval

    def encode_hdr(self, boundary):
        """Returns the header of the encoding of this parameter."""
        boundary = encode_and_quote(boundary)

        headers = ["--%s" % boundary]

        if self.filename:
            disposition = 'form-data; name="%s"; filename="%s"' % (
                self.name, self.filename)
        else:
            disposition = 'form-data; name="%s"' % self.name

        headers.append("Content-Disposition: %s" % disposition)

        if self.filetype:
            filetype = self.filetype
        else:
            filetype = "text/plain; charset=utf-8"

        headers.append("Content-Type: %s" % filetype)

        headers.append("")
        headers.append("")

        return "\r\n".join(headers)

    def encode(self, boundary):
        """Returns the string encoding of this parameter."""
        if self.value is None:
            value = self.fileobj.read()
        else:
            value = self.value

        if re.search("^--%s$" % re.escape(boundary), value, re.M):
            raise ValueError("boundary found in encoded string")

        return "%s%s\r\n" % (self.encode_hdr(boundary), value)

    def iter_encode(self, boundary, blocksize=4096):
        """Yields the encoding of this parameter If self.fileobj is set, then
        blocks of ``blocksize`` bytes are read and yielded."""
        total = self.get_size(boundary)
        current_transferred = 0
        if self.value is not None:
            block = self.encode(boundary)
            current_transferred += len(block)
            yield block
            if self.callback:
                self.callback(self, current_transferred, total)
        else:
            block = self.encode_hdr(boundary)
            current_transferred += len(block)
            yield block
            if self.callback:
                self.callback(self, current_transferred, total)
            last_block = b""
            encoded_boundary = "--%s" % encode_and_quote(boundary)
            boundary_exp = re.compile("^%s$" % re.escape(encoded_boundary),
                                      re.M)
            while True:
                block = self.fileobj.read(blocksize)
                if not block:
                    current_transferred += 2
                    yield "\r\n"
                    if self.callback:
                        self.callback(self, current_transferred, total)
                    break
                last_block += block
                if boundary_exp.search(last_block.decode("ascii", "ignore")):
                    raise ValueError("boundary found in file data")
                last_block = last_block[-len(encoded_boundary) - 2:]
                current_transferred += len(block)
                yield block
                if self.callback:
                    self.callback(self, current_transferred, total)

    def get_size(self, boundary):
        """Returns the size in bytes that this param will be when encoded with
        the given boundary."""
        if self.filesize is not None:
            valuesize = self.filesize
        else:
            valuesize = len(self.value)

        return len(self.encode_hdr(boundary)) + 2 + valuesize


def encode_string(boundary, name, value):
    """Returns ``name`` and ``value`` encoded as a multipart/form-data
    variable.

    ``boundary`` is the boundary string used throughout a single request
    to separate variables.
    """

    return MultipartParam(name, value).encode(boundary)


def encode_file_header(boundary,
                       paramname,
                       filesize,
                       filename=None,
                       filetype=None):
    """Returns the leading data for a multipart/form-data field that contains
    file data.

    ``boundary`` is the boundary string used throughout a single request to
    separate variables.

    ``paramname`` is the name of the variable in this request.

    ``filesize`` is the size of the file data.

    ``filename`` if specified is the filename to give to this field.  This
    field is only useful to the server for determining the original filename.

    ``filetype`` if specified is the MIME type of this file.

    The actual file data should be sent after this header has been sent.
    """

    return MultipartParam(
        paramname, filesize=filesize, filename=filename,
        filetype=filetype).encode_hdr(boundary)


def get_body_size(params, boundary):
    """Returns the number of bytes that the multipart/form-data encoding of
    ``params`` will be."""
    size = sum(
        p.get_size(boundary) for p in MultipartParam.from_params(params))
    return size + len(boundary) + 6


def get_headers(params, boundary):
    """Returns a dictionary with Content-Type and Content-Length headers for
    the multipart/form-data encoding of ``params``."""
    headers = {}
    boundary = quote_plus(boundary)
    headers['Content-Type'] = "multipart/form-data; boundary=%s" % boundary
    headers['Content-Length'] = str(get_body_size(params, boundary))
    return headers


class MultipartYielder(object):
    """An iterator that yields the parameters of a multipart/formdata http
    body."""

    def __init__(self, params, boundary, callback):
        self.params = params
        self.boundary = boundary
        self.callback = callback

        self.i = 0
        self.current_part = None
        self.param_iter = None
        self.current_transferred = 0
        self.total = get_body_size(params, boundary)

    def __iter__(self):
        return self

    # since python 3
    def __next__(self):
        return self.next()

    def next(self):
        """generator function to yield multipart/form-data representation of
        parameters."""
        if self.param_iter is not None:
            try:
                block = next(self.param_iter)
                self.current_transferred += len(block)
                if self.callback:
                    self.callback(self.current_part,
                                  self.current_transferred, self.total)
                return block
            except StopIteration:
                self.current_part = None
                self.param_iter = None

        if self.i is None:
            raise StopIteration
        elif self.i >= len(self.params):
            self.param_iter = None
            self.current_part = None
            self.i = None
            block = "--%s--\r\n" % self.boundary
            self.current_transferred += len(block)
            if self.callback:
                self.callback(self.current_part,
                              self.current_transferred, self.total)
            return block

        self.current_part = self.params[self.i]
        self.param_iter = self.current_part.iter_encode(self.boundary)
        self.i += 1
        return next(self)

    def reset(self):
        """Reset the iterator."""
        self.i = 0
        self.current_transferred = 0
        for param in self.params:
            param.reset()


def multipart_encode(params, boundary=None, callback=None):
    """Encode ``params`` as multipart/form-data.

    ``params`` should be a sequence of (name, value) pairs or MultipartParam
    objects, or a mapping of names to values.
    Values are either strings parameter values, or file-like objects to use as
    the parameter value.  The file-like objects must support .read() and either
    .fileno() or both .seek() and .tell().

    If ``boundary`` is set, then it as used as the MIME boundary.  Otherwise
    a randomly generated boundary will be used.  In either case, if the
    boundary string appears in the parameter values a ValueError will be
    raised.

    If ``callback`` is set, it should be a callback which will get called as blocks
    of data are encoded.  It will be called with (param, current_transferred, total),
    indicating the current parameter being encoded, the current amount encoded,
    and the total amount to encode.

    Returns a tuple of `datagen`, `headers`, where `datagen` is a
    generator that will yield blocks of data that make up the encoded
    parameters, and `headers` is a dictionary with the assoicated
    Content-Type and Content-Length headers.

    Examples:

    >>> datagen, headers = multipart_encode( [("key", "value1"), ("key", "value2")] )
    >>> s = "".join(datagen)
    >>> assert "value2" in s and "value1" in s

    >>> p = MultipartParam("key", "value2")
    >>> datagen, headers = multipart_encode( [("key", "value1"), p] )
    >>> s = "".join(datagen)
    >>> assert "value2" in s and "value1" in s

    >>> datagen, headers = multipart_encode( {"key": "value1"} )
    >>> s = "".join(datagen)
    >>> assert "value2" not in s and "value1" in s
    """
    if boundary is None:
        boundary = gen_boundary()
    else:
        boundary = quote_plus(boundary)

    headers = get_headers(params, boundary)
    params = MultipartParam.from_params(params)

    return MultipartYielder(params, boundary, callback), headers


class ReadableMultiparts(object):
    """Wraps instances of the MultipartYielder class as a readable and withable
    object."""

    def __init__(self, multipart_yielder):
        self.multipart_yielder = multipart_yielder
        self.current_block = None
        self.left_over = b''

    def read(self, size=-1):
        result = self.left_over
        while size == -1 or len(result) < size:
            try:
                next_chunk = self.multipart_yielder.next()
                if hasattr(next_chunk, "encode"):
                    next_chunk = next_chunk.encode("utf8")
                result += next_chunk
            except StopIteration:
                break

        if size == -1:
            self.left_over = b''
            return result

        self.left_over = result[size:]
        return result[:size]

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.multipart_yielder.reset()

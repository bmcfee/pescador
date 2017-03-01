#!/usr/bin/env python

import pytest
import pescador

import test_utils as T


@pytest.mark.parametrize('dimension', [1, 2, 3])
@pytest.mark.parametrize('batch_size', [1, 2, 5, 17])
@pytest.mark.parametrize('buf_size', [1, 2, 5, 17, 100])
def test_buffer_streamer(dimension, batch_size, buf_size):

    def __serialize_batches(batches):
        for batch in batches:
            for item in batch['X']:
                yield item

    reference = T.md_generator(dimension, 50, size=batch_size)

    reference = list(__serialize_batches(reference))

    gen_stream = pescador.Streamer(T.md_generator, dimension, 50,
                                   size=batch_size)
    estimate = pescador.BufferedStreamer(gen_stream, buf_size)

    estimate = list(__serialize_batches(estimate.generate()))

    T.__eq_lists(reference, estimate)


@pytest.mark.parametrize(
    'n1,n2', [pytest.mark.xfail((5, 10), raises=pescador.PescadorError),
              pytest.mark.xfail((5, 15), raises=pescador.PescadorError),
              pytest.mark.xfail((10, 5), raises=pescador.PescadorError),
              pytest.mark.xfail((15, 5), raises=pescador.PescadorError),
              (5, 5), (10, 10), (15, 15)])
def test_batch_length(n1, n2):
    generator, n = T.__zip_generator(3, n1, n2), n1

    for batch in generator:
        assert pescador.buffered.batch_length(batch) == n


@pytest.mark.parametrize('dimension', [1, 2, 3])
@pytest.mark.parametrize('batch_size', [1, 2, 5, 17])
@pytest.mark.parametrize('buf_size', [1, 2, 5, 17, 100])
def test_buffer_batch(dimension, batch_size, buf_size):
    def __serialize_batches(batches):
        for batch in batches:
            for item in batch['X']:
                yield item

    reference = T.md_generator(dimension, 50, size=batch_size)

    reference = list(__serialize_batches(reference))

    estimate = pescador.buffer_batch(T.md_generator(dimension,
                                                    50,
                                                    size=batch_size),
                                     buf_size)

    estimate = list(__serialize_batches(estimate))

    T.__eq_lists(reference, estimate)

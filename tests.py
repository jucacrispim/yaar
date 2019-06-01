# -*- coding: utf-8 -*-

# Copyright 2019 Juca Crispim <juca@poraodojuca.net>

# This file is part of yaar.

# yaar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# yaar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with yaar. If not, see <http://www.gnu.org/licenses/>.


from asynctest import MagicMock, CoroutineMock
import pytest

import yaar


def test_response():
    resp = yaar.Response(200, 'some text')
    assert resp.text == 'some text'


def test_json():
    resp = yaar.Response(200, yaar.json.dumps({'some': 'json'}))
    assert resp.json()


class MockResponse:

    status = 200

    async def text(self):
        return 'some text'

    async def release(self):
        pass


@pytest.mark.asyncio
async def test_request(mocker):
    method = 'GET'
    url = 'http://somewhere.com'

    csess = MagicMock()
    csess.return_value.request = CoroutineMock(return_value=MockResponse())
    csess.return_value.close = CoroutineMock()
    mocker.patch.object(yaar.aiohttp, 'ClientSession', csess)

    r = await yaar._request(method, url)
    assert r.text == 'some text'


@pytest.mark.asyncio
async def test_request_exception(mocker):
    method = 'GET'
    url = 'http://somewhere.com'

    mock_response = MockResponse()
    mock_response.status = 500

    csess = MagicMock()
    csess.return_value.request = CoroutineMock(return_value=mock_response)
    csess.return_value.close = CoroutineMock()

    mocker.patch.object(yaar.aiohttp, 'ClientSession', csess)

    with pytest.raises(yaar.BadHTTPRequest):
        await yaar._request(method, url)


@pytest.mark.asyncio
async def test_get(mocker):
    mocker.patch.object(yaar, '_request', MagicMock())
    url = 'http://somewhere.com'
    REQ_TYPE = None

    async def req(method, url, **kw):
        nonlocal REQ_TYPE

        REQ_TYPE = method
        return yaar.Response(200, 'some text')

    yaar._request = req

    resp = await yaar.get(url)
    assert REQ_TYPE == 'GET'
    assert resp.text == 'some text'


@pytest.mark.asyncio
async def test_post(mocker):
    mocker.patch.object(yaar, '_request', MagicMock())
    url = 'http://somewhere.com'
    REQ_TYPE = None

    async def req(method, url, **kw):
        nonlocal REQ_TYPE
        REQ_TYPE = method
        return yaar.Response(200, 'some text')

    yaar._request = req

    resp = await yaar.post(url)
    assert REQ_TYPE == 'POST'
    assert resp.text == 'some text'


@pytest.mark.asyncio
async def test_put(mocker):
    mocker.patch.object(yaar, '_request', MagicMock())
    url = 'http://somewhere.com'
    REQ_TYPE = None

    async def req(method, url, **kw):
        nonlocal REQ_TYPE
        REQ_TYPE = method
        return yaar.Response(200, 'some text')

    yaar._request = req

    resp = await yaar.put(url)
    assert REQ_TYPE == 'PUT'
    assert resp.text == 'some text'


@pytest.mark.asyncio
async def test_delete(mocker):
    mocker.patch.object(yaar, '_request', MagicMock())
    url = 'http://somewhere.com'
    REQ_TYPE = None

    async def req(method, url, **kw):
        nonlocal REQ_TYPE
        REQ_TYPE = method
        return yaar.Response(200, 'some text')

    yaar._request = req

    resp = await yaar.delete(url)
    assert REQ_TYPE == 'DELETE'
    assert resp.text == 'some text'

from __future__ import annotations

import socket
import struct
import threading
import time
import typing
from collections import defaultdict
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import lz4.block
from google.protobuf import json_format

from .data_pb2 import GetDataObject

if typing.TYPE_CHECKING:
  from .gamehelper import PoeBot

RESPONSE_TYPES = {
  "/getData": GetDataObject,
}


class Backend:
  def __init__(self, poe_bot: PoeBot, port: int = 55006) -> None:
    self.poe_bot = poe_bot
    self.port = port
    self.host = poe_bot.remote_ip
    self.debug = poe_bot.debug
    self.sock = None
    self.lock = threading.Lock()
    self.cache = defaultdict(lambda: {"current_hash": None, "data": b""})

  def ensure_connection(self) -> None:
    with self.lock:
      if self.sock is None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        try:
          self.sock.connect((self.host, self.port))
          if self.debug:
            print("Successfully established TCP connection")
        except socket.error as e:
          self.sock = None
          raise ConnectionError(f"Connection failed: {str(e)}")

  def do_request(self, path_with_query: str, max_retries: int = 10) -> typing.Optional[bytes]:
    for attempt in range(max_retries):
      try:
        self.ensure_connection()
        with self.lock:
          # Send request
          self.sock.sendall(f"{path_with_query}\n".encode())
          # Read response length
          length_data = b""
          while len(length_data) < 4:
            chunk = self.sock.recv(4 - len(length_data))
            if not chunk:
              raise ConnectionError("Connection closed while reading length")
            length_data += chunk
          length = struct.unpack("<I", length_data)[0]
          # Read response data
          response = b""
          while len(response) < length:
            chunk = self.sock.recv(min(4096, length - len(response)))
            if not chunk:
              raise ConnectionError("Connection closed while reading response")
            response += chunk
          # Process response and update cache
          processed_data = self._process_response(path_with_query, response)
          return processed_data
      except (ConnectionResetError, BrokenPipeError, socket.timeout) as e:
        with self.lock:
          if self.sock:
            self.sock.close()
            self.sock = None
        if self.debug:
          print(f"Attempt {attempt + 1} failed: {str(e)}")
        time.sleep(0.1)
      except Exception as e:
        if self.debug:
          print(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
        time.sleep(0.05)
    return None

  def _parse_response(self, response: bytes, endpoint: str) -> dict:
    if not response:
      return {"error": "Empty response"}
    try:
      base_endpoint = endpoint.split("?")[0]
      proto_class = RESPONSE_TYPES.get(base_endpoint)
      if proto_class:
        obj = proto_class()
        obj.ParseFromString(response)
        return json_format.MessageToDict(obj)
      else:
        return {"raw_response": response.hex()}
    except Exception as e:
      return {"error": f"Parsing error: {str(e)}", "raw_response": response.hex()}

  def _process_response(self, endpoint: str, response: bytes) -> bytes:
    # Clean endpoint for cache key
    parsed = urlparse(endpoint)
    query_params = parse_qs(parsed.query)
    query_params.pop("client_hash", None)
    cleaned_query = urlencode(query_params, doseq=True)
    cleaned_endpoint = urlunparse(parsed._replace(query=cleaned_query))
    cached = self.cache[cleaned_endpoint]

    response_type = response[0]
    if response_type == 0x01:  # Full response
      current_hash = struct.unpack("<Q", response[1:9])[0]
      original_size = struct.unpack("<I", response[9:13])[0]
      compressed_data = response[13:]
      cached["data"] = lz4.block.decompress(compressed_data, uncompressed_size=original_size)
      cached["current_hash"] = current_hash
      return cached["data"]
    elif response_type == 0x02:  # NotModified
      current_hash = struct.unpack("<Q", response[1:9])[0]
      cached["current_hash"] = current_hash
      return cached["data"]
    else:
      raise ValueError(f"Unknown response type: {response_type}")

  def do_request_till_get_json(self, path_with_query: str) -> dict:
    if self.debug:
      print(f"#do_request_till_get_json {path_with_query} call {time.time()}")
    data = self.do_request(path_with_query)
    if data is None:
      print("Data is none, refreshing area")
      self.force_refresh_area()
      time.sleep(0.01)
      data = self.do_request(path_with_query)
      if data is None:
        raise Exception(f"Wrong reply from {path_with_query}")
    return data

  def _endpoint_request(self, endpoint: str, params: typing.Optional[dict] = None) -> dict:
    # Build request path with params
    path = f"/{endpoint}"
    if params:
      query = "&".join([f"{k}={v}" for k, v in params.items()])
      path += f"?{query}"
    # Parse to handle client_hash
    parsed = urlparse(path)
    query_params = parse_qs(parsed.query)
    query_params.pop("client_hash", [None])[0]

    # Cleaned endpoint for cache key
    cleaned_query = urlencode(query_params, doseq=True)
    cleaned_endpoint = urlunparse(parsed._replace(query=cleaned_query))
    cached = self.cache[cleaned_endpoint]

    # Add cached client_hash to request if available
    if cached["current_hash"] is not None:
      query_params["client_hash"] = cached["current_hash"]
    new_query = urlencode(query_params, doseq=True)
    request_path = urlunparse(parsed._replace(query=new_query))

    # Get raw data and parse
    raw_data = self.do_request(request_path)
    if raw_data is None:
      self.force_refresh_area()
      raw_data = self.do_request(request_path)
      if raw_data is None:
        raise Exception(f"Failed to get data for {request_path}")
    return self._parse_response(raw_data, cleaned_endpoint)

  def force_refresh_area(self) -> dict:
    if self.debug:
      print(f"#ForceRefreshArea call {time.time()}")
    data = self.do_request_till_get_json("/ForceRefreshArea")
    if self.debug:
      print(f"#ForceRefreshArea return {time.time()}")
    return data

  def getUltimatumNextWaveUi(self):
    return self._endpoint_request("getUltimatumNextWaveUi")

  def getAnointUi(self):
    return self._endpoint_request("getAnointUi")

  def getNpcDialogueUi(self):
    return self._endpoint_request("getNpcDialogueUi")

  def getIncursionUi(self):
    return self._endpoint_request("getIncursionUi")

  def getMapInfo(self):
    return self._endpoint_request("getMapInfo")

  def getAuctionHouseUi(self):
    return self._endpoint_request("getAuctionHouseUi")

  def forceRefreshArea(self):
    if self.debug:
      print(f"#ForceRefreshArea call {time.time()}")
    data = self.do_request_till_get_json("/ForceRefreshArea")
    if self.debug:
      print(f"#ForceRefreshArea return {time.time()}")
    return data

  def getWholeData(self):
    return self._endpoint_request("getData", {"type": "full"})

  def getPartialData(self):
    if self.poe_bot.debug:
      print(f"#PoeBot.getPartialData call {time.time()}")
    data = self._endpoint_request("getData")
    if self.poe_bot.debug:
      print(f"Data received: {len(str(data)) if data else 'None'}")
    self.last_data = data
    return data

  def getPositionOfThePointOnTheScreen(self, y, x):
    return self._endpoint_request("getScreenPos", {"y": y, "x": x})  # Fixed parameter order

  def getOpenedStashInfo(self):
    data = self._endpoint_request("getOpenedStashInfo")
    try:
      data["items"] = sorted(data["items"], key=lambda item: item["LocationTopLeft"]["Y"])
      data["items"] = sorted(data["items"], key=lambda item: item["LocationTopLeft"]["X"])
    except Exception:
      print("no items getOpenedStashInfo")
      pass
    return data

  def getOpenedInventoryInfo(self):
    data = self._endpoint_request("getInventoryInfo")
    try:
      data["items"] = sorted(data["items"], key=lambda item: item["g"][2])
      data["items"] = sorted(data["items"], key=lambda item: item["g"][0])
    except Exception:
      print("no items getOpenedInventoryInfo")
      pass
    return data

  def getMinimapIcons(self):
    return self._endpoint_request("getMinimapIcons")

  def getGemsToLevelInfo(self):
    return self._endpoint_request("gemsToLevel")

  def getHoveredItemInfo(self):
    return self._endpoint_request("getHoveredItemInfo")

  def getPreloadedFiles(self):
    return self._endpoint_request("getPreloadedFiles")

  def getNecropolisPopupUI(self):
    return self._endpoint_request("getNecropolisPopupUI")

  def getVisibleLabels(self):
    return self._endpoint_request("getVisibleLabels")

  def getItemsOnGroundLabelsVisible(self):
    return self._endpoint_request("getItemsOnGroundLabelsVisible")

  def getVisibleLabelOnGroundEntities(self):
    return self._endpoint_request("getVisibleLabelOnGroundEntities")

  def getWaypointState(self):
    return self._endpoint_request("getWaypointsState")

  def getSkillBar(self):
    return self._endpoint_request("getSkillBar")

  def getQuestStates(self):
    return self._endpoint_request("getQuestStates")

  def getQuestFlags(self):
    return self._endpoint_request("getQuestFlags")

  def mapDeviceInfo(self):
    return self._endpoint_request("mapDeviceInfo")

  def getBanditDialogueUi(self):
    return self._endpoint_request("getBanditDialogueUi")

  def getKirakMissionsUi(self):
    return self._endpoint_request("getKirakMissionsUi")

  def getPurchaseWindowHideoutUi(self):
    return self._endpoint_request("getPurchaseWindowHideoutUi")

  def getRitualUi(self):
    return self._endpoint_request("getRitualUi")

  def atlasProgress(self):
    return self._endpoint_request("getAtlasProgress")

  def getWorldMapUi(self):
    return self._endpoint_request("getWorldMapUi")

  def getResurrectUi(self):
    return self._endpoint_request("getResurrectUi")

  def getLocationOnScreen(self, x, y, z):
    return self._endpoint_request("getLocationOnScreen", {"x": x, "y": y, "z": z})

  def getEntityIdByPlayerName(self, entity_ign: str):
    return self._endpoint_request("getEntityIdByPlayerName", {"name": entity_ign})

  def getPartyInfo(self):
    return self._endpoint_request("getPartyInfo")

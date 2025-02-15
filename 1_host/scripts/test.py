import json
import socket
import struct
from collections import defaultdict
import lz4.block
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from google.protobuf import json_format

from utils.data_pb2 import GetDataObject

# Define response type mappings
RESPONSE_TYPES = {
  "/getData": GetDataObject,
  # Add other endpoints and their corresponding Protobuf classes as needed
}


class ShareDataClient:
  def __init__(self, host: str = "WIN-POE1", port: int = 55006):
    self.host = host
    self.port = port
    self.cache = defaultdict(lambda: {"current_hash": None, "data": b""})

  def send_request(self, endpoint: str):
    # Parse endpoint to remove existing client_hash
    parsed = urlparse(endpoint)
    query_params = parse_qs(parsed.query)
    client_hash = query_params.pop("client_hash", [None])[0]

    # Use cleaned endpoint as cache key
    cleaned_query = urlencode(query_params, doseq=True)
    cleaned_endpoint = urlunparse(parsed._replace(query=cleaned_query))
    cached = self.cache[cleaned_endpoint]

    # Add current client_hash to query if available
    if cached["current_hash"] is not None:
      query_params["client_hash"] = cached["current_hash"]
    new_query = urlencode(query_params, doseq=True)
    request_endpoint = urlunparse(parsed._replace(query=new_query))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(f"{request_endpoint}\n".encode())

      length_data = b""
      while len(length_data) < 4:
        chunk = s.recv(4 - len(length_data))
        if not chunk:
          raise ConnectionError("Connection closed while reading length")
        length_data += chunk
      length = struct.unpack("<I", length_data)[0]

      response = b""
      while len(response) < length:
        chunk = s.recv(length - len(response))
        if not chunk:
          raise ConnectionError("Connection closed while reading response")
        response += chunk

      return self.process_response(cleaned_endpoint, response)

  def process_response(self, endpoint: str, response: bytes):
    cached = self.cache[endpoint]
    response_type = response[0]

    if response_type == 0x01:  # Full
      current_hash = struct.unpack("<Q", response[1:9])[0]
      # Extract original size (4 bytes, little-endian)
      original_size = struct.unpack("<I", response[9:13])[0]
      compressed_data = response[13:]
      # Decompress with known original size
      cached["data"] = lz4.block.decompress(compressed_data, uncompressed_size=original_size)
      cached["current_hash"] = current_hash
      return cached["data"]

    elif response_type == 0x02:  # NotModified
      current_hash = struct.unpack("<Q", response[1:9])[0]
      cached["current_hash"] = current_hash
      return cached["data"]

    else:
      raise ValueError(f"Unknown response type: {response_type}")

  def write_file(self, data: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)

  def run_tests(self):
    # Test /getData endpoint
    for i in range(1):
      raw_data = self.send_request("/getData?type=full")
      parsed_data = self.parse_response(raw_data, "/getData?type=full")
      print(parsed_data)
      self.write_file(parsed_data, f"output_{i}.json")

  def parse_response(self, response: bytes, endpoint: str):
    if not response:
      return {"error": "Empty response"}

    try:
      # Get the appropriate Protobuf class
      proto_class = RESPONSE_TYPES.get(endpoint.split("?")[0])

      if proto_class:
        if endpoint in ["/getVisibleLabels", "/getMinimapIcons", "/getQuestStates"]:
          # Handle repeated fields/list responses
          return [json_format.MessageToDict(proto_class.FromString(chunk)) for chunk in response.split(b"\n") if chunk]
        else:
          # Single message response
          obj = proto_class()
          obj.ParseFromString(response)
          return json_format.MessageToDict(obj)
      else:
        return {"raw_response": response.hex()}

    except Exception as e:
      return {"error": f"Parsing error: {str(e)}", "raw_response": response.hex()}


if __name__ == "__main__":
  client = ShareDataClient()
  client.run_tests()

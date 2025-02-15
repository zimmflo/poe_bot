using System;
using System.Net;
using System.Text;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.IO;

using ExileCore2;

// Libraries for compression and hashing
using Google.Protobuf;
using K4os.Compression.LZ4;
using K4os.Hash.xxHash;
using BsDiff;
using ShareData.Protobuf;
using System.Diagnostics;

// 111 9 11 0 deli activator thing

namespace ShareData;
public partial class ShareData : BaseSettingsPlugin<ShareDataSettings>
{

    private readonly ConcurrentDictionary<string, CacheEntry> _cache = new ConcurrentDictionary<string, CacheEntry>();

    enum ResponseType : byte
    {
        Full = 0x01,
        NotModified = 0x02
    }

    class CacheEntry
    {
        public ulong CurrentHash { get; }
        public byte[] CurrentData { get; }  // Uncompressed current data
        public ulong PreviousHash { get; }
        public byte[] PreviousData { get; }  // Uncompressed previous data

        public CacheEntry(ulong currentHash, byte[] currentData, ulong previousHash, byte[] previousData)
        {
            CurrentHash = currentHash;
            CurrentData = currentData;
            PreviousHash = previousHash;
            PreviousData = previousData;
        }
    }

    public override bool Initialise()
    {
        GameController.LeftPanel.WantUse(() => Settings.Enable);
        Task.Run(() => StartTcpServer());
        Task.Run(() => StartHttpServer()); // Start the HTTP server
        return true;
    }
    private async Task StartHttpServer()
    {
        int httpPort = 55005;
        HttpListener listener = new HttpListener();
        listener.Prefixes.Add($"http://*:{httpPort}/");
        listener.Start();
        DebugWindow.LogMsg($"HTTP server started on port {httpPort}...");

        while (true)
        {
            HttpListenerContext context = await listener.GetContextAsync();
            _ = HandleHttpRequestAsync(context);
        }
    }

    private async Task HandleHttpRequestAsync(HttpListenerContext context)
    {
        try
        {
            string rawRequest = context.Request.Url.LocalPath;
            string query = context.Request.Url.Query;
            string response = ProcessHttpRequest(rawRequest + query);
            byte[] buffer = Encoding.UTF8.GetBytes(response);

            context.Response.ContentLength64 = buffer.Length;
            context.Response.KeepAlive = false; // disable Keep-Alive

            try
            {
                using (Stream output = context.Response.OutputStream)
                {
                    await output.WriteAsync(buffer, 0, buffer.Length).ConfigureAwait(false);
                } // flushes the stream
            }
            catch (HttpListenerException ex) when (ex.ErrorCode == 64 /* Network name gone */)
            {
                // Client disconnected prematurely; log needed
                DebugWindow.LogError($"Client disconnected: {ex.Message}");
                context.Response.Abort();
                return;
            }
            catch (IOException ex)
            {
                // General I/O errors
                DebugWindow.LogError($"I/O error: {ex.Message}");
                context.Response.Abort();
                return;
            }

            // Explicitly close the response
            context.Response.Close();
        }
        catch (Exception ex)
        {
            DebugWindow.LogError($"HTTP request error: {ex}");
            context.Response.Abort(); // Ensure resources are released
        }
    }

    private async Task StartTcpServer()
    {
        int serverPort = 55006;
        var listener = new TcpListener(IPAddress.Any, serverPort);
        listener.Start();
        DebugWindow.LogMsg($"TCP server started on port {serverPort}...");

        while (true)
        {
            var client = await listener.AcceptTcpClientAsync();
            _ = HandleTcpRequestAsync(client);
        }
    }

    private async Task HandleTcpRequestAsync(TcpClient client)
    {
        try
        {
            using (client)
            using (var stream = client.GetStream())
            using (var reader = new StreamReader(stream, Encoding.UTF8))
            {
                while (true)
                {
                    string request;
                    try
                    {
                        request = await reader.ReadLineAsync().ConfigureAwait(false);
                        if (request == null) break; // Normal client disconnect
                    }
                    catch (IOException ex) when (ex.InnerException is SocketException sockEx && sockEx.ErrorCode == 10054)
                    {
                        // Client forcibly closed connection
                        DebugWindow.LogError("Client disconnected abruptly");
                        break;
                    }

                    byte[] response = ProcessTcpRequest(request);
                    byte[] lengthBytes = BitConverter.GetBytes(response.Length);

                    try
                    {
                        // Write length header
                        await stream.WriteAsync(lengthBytes, 0, lengthBytes.Length).ConfigureAwait(false);
                        // Write response
                        await stream.WriteAsync(response, 0, response.Length).ConfigureAwait(false);
                        await stream.FlushAsync().ConfigureAwait(false);
                    }
                    catch (IOException ex) when (ex.InnerException is SocketException sockEx && sockEx.ErrorCode == 10054)
                    {
                        DebugWindow.LogError("Client disconnected during write");
                        break;
                    }
                    catch (ObjectDisposedException)
                    {
                        // Stream was closed concurrently
                        break;
                    }
                }
            }
        }
        catch (Exception ex)
        {
            DebugWindow.LogError($"Client error: {ex}");
        }
    }

    private byte[] ProcessTcpRequest(string request)
    {
        try
        {
            // Split request into path and query
            string[] parts = request.Split(new[] { '?' }, 2);
            string path = parts[0];
            string originalQuery = parts.Length > 1 ? parts[1] : "";

            // Parse query parameters and remove 'client_hash'
            var queryParams = System.Web.HttpUtility.ParseQueryString(originalQuery);
            string clientHashStr = queryParams["client_hash"];
            queryParams.Remove("client_hash");

            // Rebuild the cleaned query string
            List<string> queryParts = [];
            foreach (string key in queryParams.AllKeys)
            {
                foreach (string value in queryParams.GetValues(key))
                {
                    queryParts.Add($"{key}={value}");
                }
            }
            string query = string.Join("&", queryParts);

            // Build cacheKey without client_hash
            string cacheKey = string.IsNullOrEmpty(query) ? path : $"{path}?{query}";
            ulong clientHash = string.IsNullOrEmpty(clientHashStr) ? 0 : ulong.Parse(clientHashStr);

            //DebugWindow.LogMsg($"Received request: {request}");
            //DebugWindow.LogMsg($"Client Path: {path}");
            //DebugWindow.LogMsg($"Client Query: {query}");
            //DebugWindow.LogMsg($"Client Key: {cacheKey}");
            //DebugWindow.LogMsg($"Client Hash: {clientHashStr}");
            //DebugWindow.LogMsg($"Client Hash: {clientHash}");

            switch (path)
            {
                case "/getData":
                    string requestType = ExtractQueryParameter(query, "type", "partial");
                    return ProcessData(cacheKey, SerializeProtobuf(getData(requestType)), clientHash);

                case "/getLocationOnScreen":
                    int x = int.Parse(ExtractQueryParameter(query, "x"));
                    int y = int.Parse(ExtractQueryParameter(query, "y"));
                    int z = int.Parse(ExtractQueryParameter(query, "z"));
                    var screenCoord = GameController.IngameState.Camera.WorldToScreen(new System.Numerics.Vector3(x, y, z));
                    return ProcessData(cacheKey, SerializeProtobuf(new LocationOnScreen { X = (int)screenCoord.X, Y = (int)screenCoord.Y }), clientHash);

                case "/getScreenPos":
                    int sx = int.Parse(ExtractQueryParameter(query, "x"));
                    int sy = int.Parse(ExtractQueryParameter(query, "y"));
                    return ProcessData(cacheKey, SerializeProtobuf(new LocationOnScreen { X = sx, Y = sy }), clientHash);

                case "/getInventoryInfo":
                    return ProcessData(cacheKey, SerializeProtobuf(getInventoryInfo()), clientHash);

                case "/getOpenedStashInfo":
                    return ProcessData(cacheKey, SerializeProtobuf(getStashInfo()), clientHash);

                case "/gemsToLevel":
                    return ProcessData(cacheKey, SerializeProtobufList(getGemsToLevelInfo()), clientHash);

                case "/getVisibleLabelOnGroundEntities":
                    return ProcessData(cacheKey, SerializeProtobufList(getVisibleLabelOnGroundEntities()), clientHash);

                case "/getItemsOnGroundLabelsVisible":
                    return ProcessData(cacheKey, SerializeProtobufList(getItemsOnGroundLabelsVisible()), clientHash);

                case "/mapDeviceInfo":
                    return ProcessData(cacheKey, SerializeProtobuf(mapDeviceInfo()), clientHash);

                case "/getAtlasProgress":
                    return ProcessData(cacheKey, SerializeProtobufList(getAtlasProgress()), clientHash);

                case "/getVisibleLabels":
                    return ProcessData(cacheKey, SerializeProtobufList(getVisibleLabels()), clientHash);

                case "/getHoveredItemInfo":
                    return ProcessData(cacheKey, SerializeProtobuf(getHoveredItemInfo()), clientHash);

                case "/getSkillBar":
                    return ProcessData(cacheKey, SerializeProtobuf(getSkillBar(true)), clientHash);

                case "/getLabTrialsState":
                    return null;
                //return ProcessData(cacheKey, SerializeProtobuf(new Quests_c[] = GameController.IngameState.IngameUi.GetQuests ), clientHash);

                case "/getQuestStates":
                    return ProcessData(cacheKey, SerializeProtobufList(getQuestStates()), clientHash);

                case "/getWaypointsState":
                    return null;
                //return ProcessData(cacheKey, SerializeProtobuf(new WaypointUnlockState { State = GameController.IngameState.Data.ServerData.WaypointsUnlockState }), clientHash);

                case "/getMinimapIcons":
                    return ProcessData(cacheKey, SerializeProtobufList(getMinimapIcons()), clientHash);

                case "/getRitualUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getRitualUi()), clientHash);

                case "/getWorldMapUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getWorldMapUi()), clientHash);

                case "/getUltimatumNextWaveUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getUltimatumNextWaveUi()), clientHash);

                case "/getResurrectUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getResurrectUi()), clientHash);

                case "/getPurchaseWindowHideoutUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getPurchaseWindowHideoutUi()), clientHash);

                case "/getQuestFlags":
                    return null;
                //return ProcessData(cacheKey, SerializeProtobuf(GameController.IngameState.Data.ServerData.QuestFlags), clientHash);

                case "/getPreloadedFiles":
                    return null;
                //return ProcessData(cacheKey, SerializeProtobuf(getPreloadedFiles()), clientHash);

                case "/getAuctionHouseUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getAuctionHouseUi()), clientHash);

                case "/ForceRefreshArea":
                    GameController.Area.ForceRefreshArea();
                    return ProcessData(cacheKey, SerializeProtobuf(new Status { Message = "ForceRefreshArea_OK" }), clientHash);

                case "/getMapInfo":
                    return ProcessData(cacheKey, SerializeProtobuf(getMapInfo()), clientHash);

                case "/getAnointUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getAnointUi()), clientHash);

                case "/getEntityIdByPlayerName":
                    string playerName = ExtractQueryParameter(query, "type");
                    return ProcessData(cacheKey, SerializeProtobuf(new EntityId_c { Id = getEntityIdByPlayerName(playerName) }), clientHash);

                case "/getPartyInfo":
                    return ProcessData(cacheKey, SerializeProtobuf(getPartyInfo()), clientHash);

                case "/getNpcDialogueUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getNpcDialogueUi()), clientHash);

                case "/getNpcRewardUi":
                    return ProcessData(cacheKey, SerializeProtobuf(getNpcRewardUi()), clientHash);

                default:
                    return ProcessData(cacheKey, SerializeProtobuf(new Status { Message = "Unknown request" }), clientHash);
            }
        }
        catch (Exception ex)
        {
            DebugWindow.LogError($"ProcessTcpRequest error: {ex}");
            return ProcessData("Error processing request", SerializeProtobuf(new Status { Message = "Error processing request" }), 0x00);
        }
    }

    private string ProcessHttpRequest(string rawRequest)
    {
        DebugWindow.LogMsg($"Received request: {rawRequest}");
        try
        {
            string path = rawRequest.Split('?')[0];
            string query = rawRequest.Contains('?') ? rawRequest.Split('?')[1] : "";

            switch (path)
            {
                case "/getData":
                    string requestType = ExtractQueryParameter(query, "type", "partial");
                    return SerializeData(getData(requestType));

                case "/getLocationOnScreen":
                    int x = int.Parse(ExtractQueryParameter(query, "x"));
                    int y = int.Parse(ExtractQueryParameter(query, "y"));
                    int z = int.Parse(ExtractQueryParameter(query, "z"));
                    var screenCoord = GameController.IngameState.Camera.WorldToScreen(new System.Numerics.Vector3(x, y, z));
                    return SerializeData(new List<int> { (int)screenCoord.X, (int)screenCoord.Y });

                case "/getScreenPos":
                    int sx = int.Parse(ExtractQueryParameter(query, "x"));
                    int sy = int.Parse(ExtractQueryParameter(query, "y"));
                    return SerializeData(getScreenPos(sx, sy));

                case "/getInventoryInfo":
                    return SerializeData(getInventoryInfo());

                case "/getOpenedStashInfo":
                    return SerializeData(getStashInfo());

                case "/gemsToLevel":
                    return SerializeData(getGemsToLevelInfo());

                case "/getVisibleLabelOnGroundEntities":
                    return SerializeData(getVisibleLabelOnGroundEntities());

                case "/getItemsOnGroundLabelsVisible":
                    return SerializeData(getItemsOnGroundLabelsVisible());

                case "/mapDeviceInfo":
                    return SerializeData(mapDeviceInfo());

                case "/getAtlasProgress":
                    return SerializeData(getAtlasProgress());

                case "/getVisibleLabels":
                    return SerializeData(getVisibleLabels());

                case "/getHoveredItemInfo":
                    return SerializeData(getHoveredItemInfo());

                case "/getSkillBar":
                    return SerializeData(getSkillBar(true));

                case "/getLabTrialsState":
                    return SerializeData(GameController.IngameState.IngameUi.GetQuests);

                case "/getQuestStates":
                    return SerializeData(getQuestStates());

                case "/getWaypointsState":
                    return SerializeData(GameController.IngameState.Data.ServerData.WaypointsUnlockState);

                case "/getMinimapIcons":
                    return SerializeData(getMinimapIcons());

                case "/getRitualUi":
                    return SerializeData(getRitualUi());

                case "/getWorldMapUi":
                    return SerializeData(getWorldMapUi());

                case "/getUltimatumNextWaveUi":
                    return SerializeData(getUltimatumNextWaveUi());

                case "/getResurrectUi":
                    return SerializeData(getResurrectUi());

                case "/getPurchaseWindowHideoutUi":
                    return SerializeData(getPurchaseWindowHideoutUi());

                case "/getQuestFlags":
                    return SerializeData(GameController.IngameState.Data.ServerData.QuestFlags);

                case "/getPreloadedFiles":
                    return SerializeData(getPreloadedFiles());

                case "/getAuctionHouseUi":
                    return SerializeData(getAuctionHouseUi());

                case "/ForceRefreshArea":
                    GameController.Area.ForceRefreshArea();
                    return SerializeData("ForceRefreshArea_OK");

                case "/getMapInfo":
                    return SerializeData(getMapInfo());

                case "/getAnointUi":
                    return SerializeData(getAnointUi());

                case "/getEntityIdByPlayerName":
                    string playerName = ExtractQueryParameter(query, "name");
                    return SerializeData(getEntityIdByPlayerName(playerName));

                case "/getPartyInfo":
                    return SerializeData(getPartyInfo());

                case "/getNpcDialogueUi":
                    return SerializeData(getNpcDialogueUi());

                case "/getNpcRewardUi":
                    return SerializeData(getNpcRewardUi());

                default:
                    return "Unknown request";
            }
        }
        catch (Exception ex)
        {
            DebugWindow.LogError($"ProcessRequest error: {ex}");
            return "Error processing request";
        }
    }

    private byte[] ProcessData(string cacheKey, byte[] originalData, ulong clientHash)
    {
        ulong currentHash = XXH64.DigestOf(originalData);

        // Check if client provided a hash
        if (clientHash != 0)
        {
            if (_cache.TryGetValue(cacheKey, out var cached))
            {
                if (clientHash == cached.CurrentHash)
                {
                    // Client has current data
                    return CreateResponsePacket(ResponseType.NotModified, currentHash, 0, []);
                }
            }
        }

        // Send full data and update cache
        var newCacheEntry = new CacheEntry(
            currentHash,
            originalData,
            _cache.TryGetValue(cacheKey, out var existing) ? existing.CurrentHash : 0,
            _cache.TryGetValue(cacheKey, out existing) ? existing.CurrentData : []
        );
        _cache[cacheKey] = newCacheEntry;

        return CreateResponsePacket(ResponseType.Full, currentHash, originalData.Length, originalData);
    }

    static byte[] CompressData(byte[] rawData)
    {
        byte[] compressed = new byte[LZ4Codec.MaximumOutputSize(rawData.Length)];
        int compressedSize = LZ4Codec.Encode(rawData, 0, rawData.Length, compressed, 0, compressed.Length);

        Array.Resize(ref compressed, compressedSize);
        return compressed;
    }

    private static byte[] CreateResponsePacket(ResponseType type, ulong hash, int originalSize, byte[] data)
    {
        List<byte> packet = [(byte)type, .. BitConverter.GetBytes(hash)];
        if (type == ResponseType.Full)
        {
            packet.AddRange(BitConverter.GetBytes(originalSize));
        }
        packet.AddRange(CompressData(data));
        return [.. packet];
    }

    private static string ExtractQueryParameter(string query, string key, string defaultValue = "")
    {
        var parameters = query.Split('&');
        foreach (var param in parameters)
        {
            var keyValue = param.Split('=');
            if (keyValue.Length == 2 && keyValue[0] == key)
            {
                return keyValue[1];
            }
        }
        return defaultValue;
    }

    private static string SerializeData(object data)
    {
        return Newtonsoft.Json.JsonConvert.SerializeObject(data, Newtonsoft.Json.Formatting.None);
    }

    private static byte[] SerializeProtobuf<T>(T data) where T : IMessage<T>
    {
        //return new Status { Message = "Just a simple static string for testing binary diff......." }.ToByteArray();
        return data.ToByteArray();
    }

    private static byte[] SerializeProtobufList<T>(List<T> dataList) where T : IMessage
    {
        using (var memoryStream = new MemoryStream())
        {
            foreach (var data in dataList)
            {
                data.WriteTo(memoryStream);
            }
            return memoryStream.ToArray();
        }
    }

}


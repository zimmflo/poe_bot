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
using K4os.Compression.LZ4;
using K4os.Hash.xxHash;
using BsDiff;

// 111 9 11 0 deli activator thing

namespace ShareData;
public partial class ShareData : BaseSettingsPlugin<ShareDataSettings>
{

    private readonly ConcurrentDictionary<string, (ulong Hash, byte[] Data)> _cache =
        new ConcurrentDictionary<string, (ulong, byte[])>();

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
            _ = HandleHttpRequestAsync(context); // Handle each HTTP request asynchronously
        }
    }

    private async Task HandleHttpRequestAsync(HttpListenerContext context)
    {
        try
        {
            string rawRequest = context.Request.Url.LocalPath;
            string query = context.Request.Url.Query;

            string response = ProcessRequest(rawRequest + query);

            byte[] buffer = Encoding.UTF8.GetBytes(response);
            context.Response.ContentLength64 = buffer.Length;
            await context.Response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
            context.Response.OutputStream.Close();
        }
        catch (Exception ex)
        {
            DebugWindow.LogError($"HTTP request error: {ex}");
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
            _ = HandleTcpTequestAsync(client); // Handle each client asynchronously
        }
    }

    private async Task HandleTcpTequestAsync(TcpClient client)
    {
        try
        {
            using (client)
            using (var stream = client.GetStream())
            using (var reader = new StreamReader(stream, Encoding.UTF8))
            using (var writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true })
            {
                while (true)
                {
                    string request = await reader.ReadLineAsync();
                    if (request == null) break; // Client disconnected

                    string response = ProcessRequest(request);
                    await writer.WriteLineAsync(response);
                }
            }
        }
        catch (Exception ex)
        {
            DebugWindow.LogError($"Client error: {ex}");
        }
    }
    
    private string ProcessRequest(string rawRequest)
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
                    string playerName = ExtractQueryParameter(query, "type");
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

    private string ExtractQueryParameter(string query, string key, string defaultValue = "")
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

    private string SerializeData(object data)
    {
        return Newtonsoft.Json.JsonConvert.SerializeObject(data, Newtonsoft.Json.Formatting.None);
    }
}


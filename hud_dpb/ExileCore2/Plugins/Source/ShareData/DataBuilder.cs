using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using ExileCore2;
using ExileCore2.PoEMemory.Elements;
using ExileCore2.PoEMemory.MemoryObjects;
using ExileCore2.Shared;
using ExileCore2.Shared.Helpers;
using GameOffsets2;
using GameOffsets2.Native;

using System.Collections.Generic;
using Newtonsoft.Json;
using System;
using System.Reflection;
using System.Text;

class DataBuilder
{

    public static byte WalkableValue(byte[] data, int bytesPerRow, long c, long r)
    {
        var offset = r * bytesPerRow + c / 2;
        if (offset < 0 || offset >= data.Length)
        {
            throw new Exception(string.Format($"WalkableValue failed: ({c}, {r}) [{bytesPerRow}] => {offset}"));
        }

        byte b;
        if ((c & 1) == 0)
        {
            b = (byte)(data[offset] & 0xF);
        }
        else
        {
            b = (byte)(data[offset] >> 4);
        }
        return b;
    }

    // private TerrainData _terrainMetadata;
    public static StringBuilder generateMinimap()
    {
        StringBuilder sb = new StringBuilder();
        int MapCellSizeI = 23;
        // _terrainMetadata = GameController.IngameState.Data.DataStruct.Terrain;
        // var MeleeLayerPathfindingData = GameController.Memory.ReadStdVector<byte>(Cast(_terrainMetadata.LayerMelee));

        // var BytesPerRow = _terrainMetadata.BytesPerRow;
        // var Rows = _terrainMetadata.NumRows;
        // var Cols = _terrainMetadata.NumCols;

        // for (var r = Rows * MapCellSizeI - 1; r >= 0; --r)
        // {
        //     for (var c = 0; c < Cols * MapCellSizeI; c++)
        //     {
        //         var b = WalkableValue(MeleeLayerPathfindingData, BytesPerRow, c, r);
        //         // var b = 1;
        //         var ch = b.ToString()[0];
        //         if (b == 0)
        //             ch = '0';
        //         sb.AppendFormat("{0}", ch);
        //     }
        //     sb.AppendLine();
        // }
        return sb;
    }



    public static List<float> getScreenPos(int grid_x, int grid_y)
    {
        List<float> coords = new List<float>();
        // int screenX, screenY;
        // var loc = new Vector2i(grid_x,grid_y);
        // LokiPoe.ClientFunctions.WorldToScreen(loc.MapToWorld3(), out screenX, out screenY);
        coords.Add(11);
        coords.Add(12);
        return coords;

    }



    internal static ShareDataContent updatedData = new ShareDataContent();

    public static string ContentAsJson()
    {
        return JsonConvert.SerializeObject(updatedData, Formatting.Indented);
    }

    public static Dictionary<string, ShareDataEntity> BuildItemsOnGroundLabels(GameController Controller)
    {
        Dictionary<string, ShareDataEntity> dict = new Dictionary<string, ShareDataEntity>();

        try
        {
            foreach (var value in Controller.IngameState.IngameUi.ItemsOnGroundLabels)
            {
                ShareDataEntity entity = new ShareDataEntity();

                entity.bounds_center_pos = $"{value.ItemOnGround.BoundsCenterPos}";
                entity.grid_pos = $"{value.ItemOnGround.GridPos}";
                entity.pos = $"{value.ItemOnGround.Pos}";
                entity.distance_to_player = $"{value.ItemOnGround.DistancePlayer}";
                entity.on_screen_position = $"{Controller.IngameState.Camera.WorldToScreen(value.ItemOnGround.BoundsCenterPos)}";
                entity.additional_info = $"{value.ItemOnGround}";

                dict.Add($"{value.ItemOnGround.Type}-{value.ItemOnGround.Address:X}", entity);

            }
        } catch (Exception e)
        {
            DebugWindow.LogMsg($"ShareData cannot Cannot build ItemsOnGroundLabels data -> {e}");
        }

        return dict;
    }

    public static Dictionary<string, string> BuildServerData(GameController Controller) {
        Dictionary<string, string> dict = new Dictionary<string, string>();
        return dict;
    }

    public static ShareDataEntity ParsePlayerData(GameController Controller)
    {
        ShareDataEntity playerData = new ShareDataEntity();
        
        try
        {

            Entity PlayerData = Controller.EntityListWrapper.Player;

            playerData.bounds_center_pos = $"{PlayerData.BoundsCenterPos}";
            playerData.grid_pos = $"{PlayerData.GridPos}";
            playerData.pos = $"{PlayerData.Pos}";
            playerData.distance_to_player = $"{PlayerData.DistancePlayer}";
            playerData.on_screen_position = $"{Controller.IngameState.Camera.WorldToScreen(PlayerData.BoundsCenterPos)}";
            playerData.additional_info = $"{PlayerData}";

        }
        catch (Exception e) {
            DebugWindow.LogMsg($"ShareData cannot build player data -> {e}");
        }
        return playerData;
    }

    public static string BuildMousePositionData(GameController Controller)
    {
        try
        {
            var mousePosX = Controller.IngameState.GetType().GetProperty("MousePosX").GetValue(Controller.IngameState);
            var mousePosY = Controller.IngameState.GetType().GetProperty("MousePosY").GetValue(Controller.IngameState);

            return $"X:{mousePosX} Y:{mousePosY}";
        }
        catch (Exception e) {
            DebugWindow.LogMsg($"ShareData cannot build mouse position data -> {e}");
        }

        return "";
    }

    public static void UpdateContentData(GameController Controller)
    {
        ShareDataContent content = new ShareDataContent();

        content.items_on_ground_label = BuildItemsOnGroundLabels(Controller);
        content.player_data = ParsePlayerData(Controller);
        content.mouse_position = BuildMousePositionData(Controller);

        updatedData = content;
    }
}
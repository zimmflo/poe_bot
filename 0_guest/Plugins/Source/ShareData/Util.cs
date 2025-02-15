using System;
using System.Runtime.InteropServices;
using System.Text;
using GameOffsets2.Native;

namespace ShareData;

public partial class ShareData
{
    public static byte WalkableValue(byte[] data, int bytesPerRow, long c, long r)
    {
        var offset = r * bytesPerRow + c / 2;
        if (offset < 0 || offset >= data.Length)
        {
            throw new Exception(string.Format(
                $"WalkableValue failed: ({c}, {r}) [{bytesPerRow}] => {offset}"
            ));
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

    private static StdVector Cast(NativePtrArray nativePtrArray)
    {
        //PepeLa
        //this is going to break one day and everyone's gonna be sorry, but I'm leaving this
        return MemoryMarshal.Cast<NativePtrArray, StdVector>(stackalloc NativePtrArray[] { nativePtrArray })[0];
    }

    public StringBuilder generateMinimap()
    {
        // https://www.ownedcore.com/forums/mmo/path-of-exile/894162-finding-map-data-memory.html
        StringBuilder sb = new StringBuilder();
        int MapCellSizeI = 23;
        var _terrainMetadata = GameController.IngameState.Data.DataStruct.Terrain;
        var MeleeLayerPathfindingData = GameController.Memory.ReadStdVector<byte>(Cast(_terrainMetadata.LayerMelee));

        var BytesPerRow = _terrainMetadata.BytesPerRow;
        var Rows = _terrainMetadata.NumRows;
        var Cols = _terrainMetadata.NumCols;

        for (var r = Rows * MapCellSizeI - 1; r >= 0; --r)
        {
            for (var c = 0; c < Cols * MapCellSizeI; c++)
            {
                var b = WalkableValue(MeleeLayerPathfindingData, BytesPerRow, c, r);
                // var b = 1;
                var ch = b.ToString()[0];
                if (b == 0)
                    ch = '0';
                sb.AppendFormat("{0}", ch);
            }
            sb.AppendLine();
        }
        return sb;
    }
}
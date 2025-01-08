// 还原 Shader

#define RESOLUTION_X 1920.0
#define RESOLUTION_Y 1080.0

#define TILE_SIZE 120
#define A_INV 29
#define SEED 1

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;

    float tileSizeUVX = TILE_SIZE / RESOLUTION_X;
    float tileSizeUVY = TILE_SIZE / RESOLUTION_Y;

    int tileX = int(uv.x / tileSizeUVX);
    int tileY = int(uv.y / tileSizeUVY);

    int tilesX = int(RESOLUTION_X / TILE_SIZE);
    int tilesY = int(RESOLUTION_Y / TILE_SIZE);
    int totalTiles = tilesX * tilesY;

    int shuffledIndex = tileY * tilesX + tileX;

    int c = SEED % totalTiles;
    int originalIndex = (A_INV * (shuffledIndex - c)) % totalTiles;

    if (originalIndex < 0)
    {
        originalIndex += totalTiles;
    }

    int originalX = originalIndex % tilesX;
    int originalY = originalIndex / tilesX;

    float2 tileOffsetUV = frac(uv / float2(tileSizeUVX, tileSizeUVY));

    float2 newUV = (float2(originalX, originalY) * float2(tileSizeUVX, tileSizeUVY)) + tileOffsetUV * float2(tileSizeUVX, tileSizeUVY);

    return image.Sample(textureSampler, newUV);
}

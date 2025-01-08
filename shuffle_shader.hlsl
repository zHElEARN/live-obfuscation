// Shuffle Shader

#define RESOLUTION_X 1920.0
#define RESOLUTION_Y 1080.0

#define TILE_SIZE 120
#define A 5
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

    int index = tileY * tilesX + tileX;

    int a = A;
    int c = SEED % totalTiles;

    int shuffledIndex = (a * index + c) % totalTiles;

    int shuffledX = shuffledIndex % tilesX;
    int shuffledY = shuffledIndex / tilesX;

    float2 tileOffsetUV = frac(uv / float2(tileSizeUVX, tileSizeUVY));

    float2 newUV = (float2(shuffledX, shuffledY) * float2(tileSizeUVX, tileSizeUVY)) + tileOffsetUV * float2(tileSizeUVX, tileSizeUVY);

    return image.Sample(textureSampler, newUV);
}

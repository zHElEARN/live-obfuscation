import math


def extended_gcd(a, b):
    """
    扩展欧几里得算法
    返回 (gcd, x, y) 使得 a*x + b*y = gcd
    """
    if b == 0:
        return a, 1, 0
    else:
        gcd_val, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd_val, x, y


def compute_a_inv(a, m):
    """
    计算 a 在模 m 下的乘法逆元 a_inv
    """
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        raise ValueError(f"a = {a} 和 m = {m} 不互质，没有乘法逆元。")
    else:
        return x % m


def find_common_divisors(width, height):
    """
    找到同时能整除 width 和 height 的所有正整数
    """
    divisors = []
    gcd_val = math.gcd(width, height)
    for i in range(1, gcd_val + 1):
        if gcd_val % i == 0:
            divisors.append(i)
    return divisors


def find_coprime_a(m):
    """
    找到所有与 m 互质的 a 值
    """
    coprimes = [a for a in range(1, m) if math.gcd(a, m) == 1]
    return coprimes


def main():
    print("=== LCG 参数计算器 ===\n")

    # 输入分辨率
    while True:
        try:
            resolution_input = input("请输入分辨率（格式为宽x高，例如1920x1080）: ")
            if "x" not in resolution_input.lower():
                raise ValueError("格式错误，请使用宽x高格式（例如1920x1080）。")
            width_str, height_str = resolution_input.lower().split("x")
            width = int(width_str.strip())
            height = int(height_str.strip())
            if width <= 0 or height <= 0:
                raise ValueError("宽度和高度必须为正整数。")
            break
        except ValueError as ve:
            print(f"输入错误: {ve}\n请重新输入。")

    # 找到所有符合条件的tile宽度
    common_divisors = find_common_divisors(width, height)
    print(f"\n可选的格子宽度（tileSize）: {common_divisors}")

    # 用户选择tile宽度
    while True:
        try:
            tile_size_input = input("请输入格子宽度（tileSize）: ")
            tile_size = int(tile_size_input)
            if tile_size not in common_divisors:
                raise ValueError("tileSize 必须是分辨率宽度和高度的公约数。")
            break
        except ValueError as ve:
            print(f"输入错误: {ve}\n请重新输入。")

    # 计算总格子数m
    tiles_x = width // tile_size
    tiles_y = height // tile_size
    m = tiles_x * tiles_y
    print(f"\n总格子数 m = {tiles_x} * {tiles_y} = {m}")

    # 找到所有与m互质的a值
    coprime_as = find_coprime_a(m)
    if len(coprime_as) == 0:
        print("没有找到与m互质的a值。请检查tileSize是否正确。")
        return

    # 选择前10个a值
    num_a = min(10, len(coprime_as))
    selected_as = coprime_as[:num_a]

    # 计算a_inv
    a_inv_list = []
    for a in selected_as:
        try:
            a_inv = compute_a_inv(a, m)
            a_inv_list.append(a_inv)
        except ValueError as e:
            # 理论上不会发生，因为a和m互质
            a_inv_list.append(None)

    # 显示结果
    print("\n=== 计算结果 ===")
    print(f"分辨率: {width}x{height}")
    print(f"格子宽度（tileSize）: {tile_size}")
    print(f"总格子数（m）: {m}\n")

    print(f"找到 {len(selected_as)} 个符合要求的 (a, a_inv) 对:")
    print("{:<5} {:<10}".format("a", "a_inv"))
    print("-" * 20)
    for a, a_inv in zip(selected_as, a_inv_list):
        print("{:<5} {:<10}".format(a, a_inv))

    # 提示用户如何使用这些参数
    print("\n你可以将以下参数输入到 Shader 中：")
    print(f"tileSize = {tile_size}")
    print("选择其中一个 (a, a_inv) 对来配置 Shuffle Shader 和 Inverse Shuffle Shader。")
    print("确保在 Inverse Shuffle Shader 中使用相同的 a_inv 和 seed。")


if __name__ == "__main__":
    main()

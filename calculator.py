#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工业门尺寸与价格估算器（快速卷帘门 / 硬质快速门 / 工业滑升门 / 堆积门 / 卷帘门）

用法:
    python calculator.py                                  # 交互式
    python calculator.py --list                           # 查看门型与系数
    python calculator.py --type 快速卷帘门 --w 3.0 --h 3.0 --qty 2

说明: 参考价 = 总面积 × 单价系数（默认系数为市场示例值，请按当地行情修改 DOOR_TYPES）。
免责: 所有结果为估算，实际以现场测量与正式报价为准。
"""
from __future__ import annotations

import argparse

# 门型参数：price_low / price_high = 参考单价区间（元/㎡），max_w / max_h = 常规单樘尺寸上限（米）
DOOR_TYPES = {
    "快速卷帘门": {"price_low": 550, "price_high": 900, "max_w": 6.0, "max_h": 6.0,
                   "desc": "PVC 软帘，高频通行，适合车间 / 仓库"},
    "硬质快速门": {"price_low": 1500, "price_high": 2800, "max_w": 8.0, "max_h": 8.0,
                   "desc": "铝合金 / 钢制硬质门板，抗风、保温好"},
    "工业滑升门": {"price_low": 380, "price_high": 750, "max_w": 8.0, "max_h": 8.5,
                   "desc": "保温门板沿导轨提升，适合厂房大门"},
    "堆积门": {"price_low": 450, "price_high": 850, "max_w": 7.0, "max_h": 8.0,
               "desc": "软帘向上堆积，节省顶部空间"},
    "卷帘门": {"price_low": 160, "price_high": 380, "max_w": 6.5, "max_h": 6.5,
               "desc": "普通电动卷帘，经济实用"},
}
FOOTNOTE = "⚠️ 结果为估算值，实际以现场测量与正式报价为准。"


def estimate(door_type: str, width: float, height: float, qty: int = 1) -> dict:
    info = DOOR_TYPES[door_type]
    area = width * height
    total_area = area * qty
    body = area * 1.08            # 门体材料（含搭接 / 裁剪损耗）
    guide = (height + 0.6) * 2    # 两侧导轨 / 边柱长度（米）
    low = total_area * info["price_low"]
    high = total_area * info["price_high"]
    warns = []
    if width > info["max_w"]:
        warns.append(f"单樘宽度 {width:.1f}m 超常规上限 {info['max_w']}m：可能需分节 / 加强或定制")
    if height > info["max_h"]:
        warns.append(f"单樘高度 {height:.1f}m 超常规上限 {info['max_h']}m：可能需加强或定制")
    return {
        "area": area, "total_area": total_area,
        "body": body, "guide": guide,
        "low": low, "high": high, "warns": warns,
    }


def render(door_type: str, width: float, height: float, qty: int, r: dict) -> None:
    print()
    print(f"门型: {door_type}    ({DOOR_TYPES[door_type]['desc']})")
    print(f"单樘: {width:.2f}m × {height:.2f}m    数量: {qty}")
    print(f"单樘面积: {r['area']:.2f} ㎡    总面积: {r['total_area']:.2f} ㎡")
    print(f"用料估算(单樘): 门体材料 ≈ {r['body']:.2f} ㎡ ; 导轨/边柱 ≈ {r['guide']:.1f} m")
    print(f"参考价: ¥{r['low']:,.0f} ~ ¥{r['high']:,.0f}   (中值 ¥{(r['low'] + r['high']) / 2:,.0f})")
    for msg in r["warns"]:
        print("⚠️ ", msg)
    print(FOOTNOTE)


def interactive() -> None:
    names = list(DOOR_TYPES)
    print("支持门型:")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}  ({DOOR_TYPES[name]['desc']})")
    sel = input("选择门型编号: ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(names)):
        raise SystemExit("无效的门型编号")
    door_type = names[int(sel) - 1]
    width = float(input("门洞宽度 (米): ").strip())
    height = float(input("门洞高度 (米): ").strip())
    qty_s = input("数量 (樘, 默认 1): ").strip()
    qty = int(qty_s) if qty_s else 1
    render(door_type, width, height, qty, estimate(door_type, width, height, qty))


def main() -> None:
    ap = argparse.ArgumentParser(description="工业门尺寸与价格估算器")
    ap.add_argument("--type", help="门型（见 --list）")
    ap.add_argument("--w", type=float, help="门洞宽度（米）")
    ap.add_argument("--h", type=float, help="门洞高度（米）")
    ap.add_argument("--qty", type=int, default=1, help="数量（樘，默认 1）")
    ap.add_argument("--list", action="store_true", help="列出支持的门型")
    args = ap.parse_args()

    if args.list:
        for name, info in DOOR_TYPES.items():
            print(f"{name}: ¥{info['price_low']}~{info['price_high']}/㎡  |  {info['desc']}")
        return

    if args.type is None or args.w is None or args.h is None:
        interactive()
        return

    if args.type not in DOOR_TYPES:
        raise SystemExit(f"未知门型：{args.type}（用 --list 查看）")
    render(args.type, args.w, args.h, args.qty, estimate(args.type, args.w, args.h, args.qty))


if __name__ == "__main__":
    main()

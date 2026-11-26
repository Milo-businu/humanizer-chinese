#!/usr/bin/env python3
"""Rule-based router for the humanizer-chinese skill family.

Given text, recommend which version should handle it. Transparent: every
recommendation comes with the keyword hits that produced it.

Usage:
    python3 route_version.py "帮我看看这段论文摘要"
    python3 route_version.py --file draft.md
    echo "写个小红书段子" | python3 route_version.py
    python3 route_version.py --explain  # print the full rule table
"""

import argparse
import re
import sys
from pathlib import Path

VERSIONS = {
    "学术版": {
        "name": "humanizer-academic",
        "desc": "三不变：事实、引文、结论不动",
        "strong": ["论文", "摘要", "引言", "文献综述", "期刊", "投稿", "学术",
                   "基金申请", "学位论文", "毕业论文", "参考文献", "实验结果", "方法论"],
        "weak": ["研究", "数据", "分析", "表明", "显著", "样本", "论证"],
    },
    "营销版": {
        "name": "humanizer-marketing",
        "desc": "去空泛自夸，不去销售力",
        "strong": ["卖点", "广告语", "详情页", "落地页", "CTA", "转化", "营销",
                   "产品文案", "品牌故事", "促销", "商品描述", "slogan"],
        "weak": ["用户", "购买", "体验", "优势", "方案", "客户"],
    },
    "文学创作版": {
        "name": "humanizer-literary",
        "desc": "意图不变话变，方言碎句是资产",
        "strong": ["小说", "散文", "诗歌", "对白", "剧本", "网文", "文学",
                   "叙事", "人物", "情节", "show don't tell", "意识流"],
        "weak": ["描写", "场景", "意象", "情绪", "节奏", "视角"],
    },
    "社交媒体版": {
        "name": "humanizer-social",
        "desc": "按平台语域改写，给多标题多版本",
        "strong": ["小红书", "公众号", "知乎", "微博", "抖音", "朋友圈", "口播",
                   "种草", "笔记", "标题", "话题标签", "短视频", "软文"],
        "weak": ["分享", "测评", "安利", "互动", "涨粉", "流量"],
    },
    "包袱版": {
        "name": "humanizer-baofu",
        "desc": "唯一主动造笑的版本",
        "strong": ["段子", "包袱", "笑话", "脱口秀", "相声", "小品", "喜剧",
                   "好笑", "笑点", "梗", "幽默", "抖包袱", "吐槽"],
        "weak": [" funny", "搞笑", "反转", "谐音", "冷笑话", "无语"],
    },
}

GENERIC = {
    "version": "通用版",
    "name": "humanizer-chinese",
    "desc": "去 AI 腔，像人说话",
}

# Explicit user instruction overrides keyword scoring.
EXPLICIT_PATTERNS = [
    (r"用\s*(学术版|营销版|文学创作版|社交媒体版|包袱版|通用版)", "explicit"),
    (r"(学术版|营销版|文学创作版|社交媒体版|包袱版)\s*(帮我|处理|改|润色|看看)", "explicit"),
    (r"用\s*(humanizer-[a-z-]+)", "name"),
]


def score_text(text: str):
    """Return {version: {'strong': [...], 'weak': [...], 'score': int}}."""
    results = {}
    lowered = text.lower()
    for version, rules in VERSIONS.items():
        strong_hits = [w for w in rules["strong"] if w.lower() in lowered]
        weak_hits = [w for w in rules["weak"] if w.lower() in lowered]
        # A strong hit counts 3, a weak hit counts 1. Weak hits only matter
        # when at least one strong hit exists (avoids noise from common words).
        score = len(strong_hits) * 3 + (len(weak_hits) if strong_hits else 0)
        if score:
            results[version] = {
                "strong": strong_hits,
                "weak": weak_hits,
                "score": score,
            }
    return results


def check_explicit(text: str):
    for pattern, kind in EXPLICIT_PATTERNS:
        m = re.search(pattern, text)
        if not m:
            continue
        token = m.group(1)
        if kind == "name":
            for version, rules in VERSIONS.items():
                if rules["name"] == token:
                    return version, f"显式指定调用名 {token}"
            if token == GENERIC["name"]:
                return GENERIC["version"], f"显式指定调用名 {token}"
        else:
            return token, f"用户显式指定「{token}」"
    return None


def route(text: str):
    explicit = check_explicit(text)
    if explicit:
        version, reason = explicit
        info = VERSIONS.get(version, GENERIC)
        return {
            "version": version,
            "name": info.get("name", GENERIC["name"]),
            "desc": info.get("desc", GENERIC["desc"]),
            "confidence": "high",
            "reason": reason,
            "hits": [],
            "alternatives": [],
        }

    scores = score_text(text)
    if not scores:
        return {
            "version": GENERIC["version"],
            "name": GENERIC["name"],
            "desc": GENERIC["desc"],
            "confidence": "medium",
            "reason": "没有命中任何专属关键词，走通用版",
            "hits": [],
            "alternatives": [],
        }

    ranked = sorted(scores.items(), key=lambda x: -x[1]["score"])
    top_version, top = ranked[0]
    total = sum(v["score"] for _, v in ranked)
    ratio = top["score"] / total if total else 0

    if ratio >= 0.65:
        confidence = "high"
    elif ratio >= 0.45 or len(ranked) == 1:
        confidence = "medium"
    else:
        confidence = "low"

    hits = [f"{w}(强)" for w in top["strong"]] + [f"{w}(弱)" for w in top["weak"]]
    alternatives = [v for v, _ in ranked[1:3]]

    reason_parts = []
    if top["strong"]:
        reason_parts.append("命中专属词：" + "、".join(top["strong"]))
    if len(ranked) > 1:
        reason_parts.append("与 " + "、".join(alternatives) + " 有重叠")
    if confidence == "low":
        reason_parts.append("建议确认平台/体裁后再动手")

    info = VERSIONS[top_version]
    return {
        "version": top_version,
        "name": info["name"],
        "desc": info["desc"],
        "confidence": confidence,
        "reason": "；".join(reason_parts),
        "hits": hits,
        "alternatives": alternatives,
    }


def print_rules():
    print("版本路由规则\n")
    print("用户显式指定（最高优先级）：用 <版本名> / 用 <调用名> / <版本名> 帮我改")
    print("\n关键词打分：强命中 3 分，弱命中 1 分（弱命中需至少一个强命中才计入）")
    print("\n")
    for version, rules in VERSIONS.items():
        print(f"【{version}】{rules['name']} — {rules['desc']}")
        print(f"  强：{'、'.join(rules['strong'])}")
        print(f"  弱：{'、'.join(rules['weak'])}")
        print()
    print(f"【通用版】{GENERIC['name']} — {GENERIC['desc']}（无命中时的默认）")
    print("\n置信度：占比≥65% 高，≥45% 中，其余低（低时建议先确认场景）")


def format_result(result: dict) -> str:
    lines = [
        f"推荐版本：{result['version']}（{result['name']}）",
        f"定位：{result['desc']}",
        f"置信度：{result['confidence']}",
        f"理由：{result['reason']}",
    ]
    if result["hits"]:
        lines.append("命中词：" + "、".join(result["hits"]))
    if result["alternatives"]:
        lines.append("次选：" + "、".join(result["alternatives"]))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="中文去 AI 味 skill 版本路由器")
    parser.add_argument("text", nargs="?", help="待判断的文本")
    parser.add_argument("--file", help="从文件读取待判断文本")
    parser.add_argument("--explain", action="store_true", help="打印完整规则表")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    if args.explain:
        print_rules()
        return

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.error("请提供文本、--file 或通过 stdin 输入")

    result = route(text)

    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))


if __name__ == "__main__":
    main()

# 版本路由脚本：关键词匹配推荐版本

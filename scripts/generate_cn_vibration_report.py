#!/usr/bin/env python3
"""Generate Chinese vibration analysis report with high-DPI figures."""

from __future__ import annotations

import textwrap
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import image as mpimg
from matplotlib import font_manager

DATA = Path("/home/ubuntu/.cursor/projects/workspace/uploads/__17__1701_170022_21________markdown_7688.md")
OUT = Path("/workspace/artifacts/vibration_plots")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "WenQuanYi Micro Hei"
plt.rcParams.update(
    {
        "font.sans-serif": [FONT, "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    }
)

DPI = 300


def load_records():
    lines = [l for l in DATA.read_text(encoding="utf-8").splitlines() if l.startswith("| SH |")]
    records = []
    for line in lines:
        p = [x.strip() for x in line.split("|") if x.strip()]
        vals = np.array([float(x) for x in p[8:]], dtype=float)
        fs = float(p[7])
        t = datetime.strptime(p[4], "%Y-%m-%d %H:%M:%S")
        n = len(vals)
        rms = float(np.sqrt(np.mean(vals**2)))
        peak = float(np.max(np.abs(vals)))
        records.append(
            {
                "time": t,
                "fs": fs,
                "vals": vals,
                "rms": rms,
                "peak": peak,
                "time_str": p[4],
                "time_axis": np.arange(n) / fs,
            }
        )
    records.sort(key=lambda r: r["time"])
    return records


def spectrum(vals: np.ndarray, fs: float):
    arr = vals - np.mean(vals)
    n = len(arr)
    mag = np.abs(np.fft.rfft(arr)) / n * 2
    freqs = np.fft.rfftfreq(n, d=1 / fs)
    return freqs, mag


def dominant_freq(vals: np.ndarray, fs: float, lo=10, hi=800):
    freqs, mag = spectrum(vals, fs)
    valid = (freqs >= lo) & (freqs <= hi)
    if not valid.any():
        return 0.0, 0.0
    idx = np.argmax(mag[valid])
    f = freqs[valid][idx]
    a = mag[valid][idx]
    return float(f), float(a)


def save_fig(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def generate_figures(records):
    quiet = min(records, key=lambda r: r["rms"])
    harsh = max(records, key=lambda r: r["rms"])
    median = sorted(records, key=lambda r: r["rms"])[len(records) // 2]
    selected = [("平稳", quiet, "#10b981"), ("中等", median, "#f59e0b"), ("剧烈", harsh, "#ef4444")]
    cluster = [r for r in records if r["time"].hour == 9 and r["time"].minute == 29]
    times = [r["time"] for r in records]
    rms_vals = [r["rms"] for r in records]
    peak_vals = [r["peak"] for r in records]
    paths = {}

    # 1 RMS时序
    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.plot(times, rms_vals, "o-", color="#2563eb", linewidth=2.2, markersize=8, label="RMS (g)")
    ax.fill_between(times, 0, rms_vals, alpha=0.12, color="#2563eb")
    ax.axhline(2.0, color="#f59e0b", linestyle="--", linewidth=1.4, label="偏高阈值 2 g")
    ax.axhline(0.5, color="#10b981", linestyle="--", linewidth=1.4, label="平稳阈值 0.5 g")
    for r in sorted(records, key=lambda x: x["rms"], reverse=True)[:3]:
        ax.annotate(
            f"{r['rms']:.1f}g",
            (r["time"], r["rms"]),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=9,
            color="#dc2626",
            fontweight="bold",
        )
    ax.set_title("上海17号线 1701-170022 车 21位 — 36条样本 RMS 时序", fontweight="bold", pad=12)
    ax.set_xlabel("采集时间（2026-05-28）")
    ax.set_ylabel("RMS 加速度 (g)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    plt.xticks(rotation=35)
    ax.grid(True, alpha=0.28, linewidth=0.8)
    ax.legend(loc="upper right")
    ax.set_ylim(0, max(rms_vals) * 1.18)
    paths["rms_timeseries_cn.png"] = save_fig(fig, "rms_timeseries_cn.png")

    # 2 RMS与峰值
    fig, ax1 = plt.subplots(figsize=(14, 5.5))
    ax2 = ax1.twinx()
    ax1.bar(times, rms_vals, width=0.00045, color="#3b82f6", alpha=0.75, label="RMS")
    ax2.plot(times, peak_vals, "s-", color="#ef4444", linewidth=2, markersize=6, label="峰值")
    ax1.set_ylabel("RMS (g)", color="#1d4ed8")
    ax2.set_ylabel("峰值 (g)", color="#b91c1c")
    ax1.set_title("RMS 与峰值双指标时序对比", fontweight="bold", pad=12)
    ax1.set_xlabel("采集时间（2026-05-28）")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.xticks(rotation=35)
    ax1.grid(True, alpha=0.28)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left")
    paths["rms_peak_timeseries_cn.png"] = save_fig(fig, "rms_peak_timeseries_cn.png")

    # 3 主频时序
    dom_freqs, dom_amps = [], []
    for r in records:
        f, a = dominant_freq(r["vals"], r["fs"])
        dom_freqs.append(f)
        dom_amps.append(a)
    fig, ax = plt.subplots(figsize=(14, 5.5))
    sc = ax.scatter(times, dom_freqs, c=rms_vals, cmap="RdYlGn_r", s=110, edgecolors="#374151", linewidth=0.6)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("RMS (g)")
    ax.axhline(520, color="#dc2626", linestyle="--", alpha=0.7, linewidth=1.4, label="参考频率 520 Hz")
    ax.set_title("主频（10-800 Hz）随时间变化", fontweight="bold", pad=12)
    ax.set_xlabel("采集时间（2026-05-28）")
    ax.set_ylabel("主频 (Hz)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.xticks(rotation=35)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.28)
    paths["dominant_freq_timeseries_cn.png"] = save_fig(fig, "dominant_freq_timeseries_cn.png")

    # 4 三栏波形
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    for ax, (label, r, color) in zip(axes, selected):
        ax.plot(r["time_axis"], r["vals"], color=color, linewidth=0.75)
        ax.axhline(0, color="#9ca3af", linewidth=0.6)
        ax.set_ylabel("加速度 (g)")
        ax.set_title(
            f"{label}工况 — {r['time_str']}  RMS={r['rms']:.3f}g  峰值={r['peak']:.2f}g  采样率={r['fs']:.0f}Hz",
            fontsize=12,
        )
        ax.grid(True, alpha=0.28)
        ax.set_xlim(0, r["time_axis"][-1])
    axes[-1].set_xlabel("时间 (s)")
    fig.suptitle("典型工况时域波形对比", fontsize=16, fontweight="bold", y=1.01)
    fig.tight_layout()
    paths["waveform_comparison_3panel_cn.png"] = save_fig(fig, "waveform_comparison_3panel_cn.png")

    # 5 波形叠加
    fig, ax = plt.subplots(figsize=(14, 5.5))
    for label, r, color in selected:
        n_show = int(min(0.5 * r["fs"], len(r["vals"])))
        ax.plot(r["time_axis"][:n_show], r["vals"][:n_show], label=f"{label} (RMS={r['rms']:.2f}g)", color=color, linewidth=1.0)
    ax.axhline(0, color="#9ca3af", linewidth=0.6)
    ax.set_xlabel("时间 (s)")
    ax.set_ylabel("加速度 (g)")
    ax.set_title("前 0.5 秒波形叠加对比", fontweight="bold", pad=12)
    ax.legend()
    ax.grid(True, alpha=0.28)
    paths["waveform_overlay_0p5s_cn.png"] = save_fig(fig, "waveform_overlay_0p5s_cn.png")

    # 6 0929簇波形
    fig, ax = plt.subplots(figsize=(14, 5.5))
    colors = ["#ef4444", "#f97316", "#eab308", "#8b5cf6"]
    for i, r in enumerate(sorted(cluster, key=lambda x: x["time"])):
        ax.plot(
            r["time_axis"],
            r["vals"],
            label=f"{r['time_str']} RMS={r['rms']:.2f}g",
            color=colors[i % len(colors)],
            linewidth=0.85,
        )
    ax.axhline(0, color="#9ca3af", linewidth=0.6)
    ax.set_xlabel("时间 (s)")
    ax.set_ylabel("加速度 (g)")
    ax.set_title("09:29 高振动簇波形对比", fontweight="bold", pad=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.28)
    paths["waveform_0929_cluster_cn.png"] = save_fig(fig, "waveform_0929_cluster_cn.png")

    # 7 36波形网格
    fig, axes = plt.subplots(6, 6, figsize=(18, 14))
    norm = plt.Normalize(min(rms_vals), max(rms_vals))
    cmap = plt.cm.RdYlGn_r
    for ax, r in zip(axes.flat, records):
        color = cmap(norm(r["rms"]))
        ax.plot(r["time_axis"], r["vals"], color=color, linewidth=0.45)
        ax.axhline(0, color="#d1d5db", linewidth=0.3)
        ax.set_title(f"{r['time'].strftime('%H:%M:%S')}\nRMS={r['rms']:.2f}g", fontsize=8)
        ax.tick_params(labelsize=6)
        ax.grid(True, alpha=0.18)
    fig.suptitle("36 条振动波形全览（颜色随 RMS 由绿到红加深）", fontsize=16, fontweight="bold")
    fig.tight_layout()
    paths["waveform_grid_36_cn.png"] = save_fig(fig, "waveform_grid_36_cn.png")

    # 8 三栏频谱
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    for ax, (label, r, color) in zip(axes, selected):
        freqs, mag = spectrum(r["vals"], r["fs"])
        mask = freqs <= 800
        ax.plot(freqs[mask], mag[mask], color=color, linewidth=0.9)
        idx = np.argmax(mag[1 : mask.sum()]) + 1
        ax.annotate(
            f"{freqs[idx]:.1f} Hz\n{mag[idx]:.2f} g",
            (freqs[idx], mag[idx]),
            fontsize=9,
            color=color,
            xytext=(12, 6),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, alpha=0.85),
        )
        ax.set_ylabel("幅值 (g)")
        ax.set_title(f"{label}工况 — {r['time_str']}  RMS={r['rms']:.3f}g", fontsize=12)
        ax.grid(True, alpha=0.28)
    axes[-1].set_xlabel("频率 (Hz)")
    fig.suptitle("典型工况频谱对比（0-800 Hz）", fontsize=16, fontweight="bold", y=1.01)
    fig.tight_layout()
    paths["spectrum_comparison_3panel_cn.png"] = save_fig(fig, "spectrum_comparison_3panel_cn.png")

    # 9 频谱叠加
    fig, ax = plt.subplots(figsize=(14, 5.5))
    for label, r, color in selected:
        freqs, mag = spectrum(r["vals"], r["fs"])
        mask = freqs <= 800
        ax.plot(freqs[mask], mag[mask], label=f"{label} RMS={r['rms']:.2f}g", color=color, linewidth=1.1)
    ax.axvspan(500, 550, alpha=0.15, color="#ef4444", label="主能量带 500-550 Hz")
    ax.set_xlabel("频率 (Hz)")
    ax.set_ylabel("幅值 (g)")
    ax.set_title("频谱叠加对比（0-800 Hz）", fontweight="bold", pad=12)
    ax.legend()
    ax.grid(True, alpha=0.28)
    paths["spectrum_overlay_0_800hz_cn.png"] = save_fig(fig, "spectrum_overlay_0_800hz_cn.png")

    # 10 低频频谱
    fig, ax = plt.subplots(figsize=(14, 5.5))
    for label, r, color in selected:
        freqs, mag = spectrum(r["vals"], r["fs"])
        mask = freqs <= 50
        ax.plot(freqs[mask], mag[mask], label=f"{label} RMS={r['rms']:.2f}g", color=color, linewidth=1.1)
    ax.set_xlabel("频率 (Hz)")
    ax.set_ylabel("幅值 (g)")
    ax.set_title("低频段频谱对比（0-50 Hz）", fontweight="bold", pad=12)
    ax.legend()
    ax.grid(True, alpha=0.28)
    paths["spectrum_lowfreq_0_50hz_cn.png"] = save_fig(fig, "spectrum_lowfreq_0_50hz_cn.png")

    # 11 0929簇频谱
    fig, ax = plt.subplots(figsize=(14, 5.5))
    for i, r in enumerate(sorted(cluster, key=lambda x: x["time"])):
        freqs, mag = spectrum(r["vals"], r["fs"])
        mask = freqs <= 800
        ax.plot(
            freqs[mask],
            mag[mask],
            label=f"{r['time_str']} RMS={r['rms']:.2f}g",
            color=colors[i % len(colors)],
            linewidth=0.95,
        )
    ax.axvspan(500, 550, alpha=0.12, color="#6b7280")
    ax.set_xlabel("频率 (Hz)")
    ax.set_ylabel("幅值 (g)")
    ax.set_title("09:29 高振动簇频谱对比", fontweight="bold", pad=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.28)
    paths["spectrum_0929_cluster_cn.png"] = save_fig(fig, "spectrum_0929_cluster_cn.png")

    # 12 36频谱网格
    fig, axes = plt.subplots(6, 6, figsize=(18, 14))
    for ax, r in zip(axes.flat, records):
        freqs, mag = spectrum(r["vals"], r["fs"])
        mask = freqs <= 800
        color = cmap(norm(r["rms"]))
        ax.plot(freqs[mask], mag[mask], color=color, linewidth=0.55)
        ax.set_title(f"{r['time'].strftime('%H:%M:%S')}\nRMS={r['rms']:.2f}g", fontsize=8)
        ax.tick_params(labelsize=6)
        ax.grid(True, alpha=0.18)
    fig.suptitle("36 条频谱全览（0-800 Hz，颜色随 RMS 加深）", fontsize=16, fontweight="bold")
    fig.tight_layout()
    paths["spectrum_grid_36_cn.png"] = save_fig(fig, "spectrum_grid_36_cn.png")

    return paths, quiet, harsh, median, cluster, dom_freqs


def build_analyses(records, quiet, harsh, median, cluster, dom_freqs):
    rms_vals = [r["rms"] for r in records]
    peak_vals = [r["peak"] for r in records]
    high_count = sum(1 for r in rms_vals if r >= 2)
    low_count = sum(1 for r in rms_vals if r < 0.5)

    analyses = [
        (
            "图1  RMS 时序图",
            "rms_timeseries_cn.png",
            [
                f"该图展示 36 条样本在 2026-05-28 08:12 至 13:02 期间的 RMS 变化趋势。",
                f"RMS 范围为 {min(rms_vals):.3f} ~ {max(rms_vals):.3f} g，均值 {np.mean(rms_vals):.3f} g。",
                "全天最突出的高峰出现在 09:29 附近，最高达 10.0 g，其次为 12:47 的 5.6 g。",
                "12:00 之后整体水平明显回落，多数记录低于 2 g 偏高阈值。",
                "曲线呈间歇性冲击特征：基线较低，少数时刻突然跃升，符合轨道不平顺或道岔通过事件模式。",
                "建议将 RMS>5 g 的时刻与列车运行图、区段里程进行关联核查。",
            ],
        ),
        (
            "图2  RMS 与峰值双指标时序",
            "rms_peak_timeseries_cn.png",
            [
                f"蓝色柱为 RMS，红色折线为峰值。峰值范围 {min(peak_vals):.2f} ~ {max(peak_vals):.2f} g。",
                "RMS 与峰值总体同向变化，但峰值对单次冲击更敏感。",
                "09:29:58 峰值达 34.6 g，为全天最高，说明该时刻存在极强瞬时加速度。",
                "部分时刻 RMS 中等但峰值偏高，提示除持续振动外还存在孤立尖峰。",
                "运维上建议同时监控 RMS（能量水平）和峰值（冲击强度）两个指标。",
            ],
        ),
        (
            "图3  主频时序散点图",
            "dominant_freq_timeseries_cn.png",
            [
                "每个点代表一条样本在 10-800 Hz 范围内的主频，颜色代表 RMS 大小。",
                f"多数高 RMS 记录（红/橙色点）主频集中在 500-550 Hz，尤其接近 520 Hz 参考线。",
                "低 RMS 记录主频分布更分散，部分落在 100 Hz 以下或 600-700 Hz。",
                "这说明剧烈振动并非宽带噪声，而是具有明显窄带特征。",
                "520 Hz 主频可能与轮轨耦合、轨面周期性缺陷或转向架共振有关，需结合车速核算。",
            ],
        ),
        (
            "图4  典型工况三栏波形对比",
            "waveform_comparison_3panel_cn.png",
            [
                f"平稳样本（09:05:26）：RMS=0.234 g，波形幅值极小，接近本底噪声。",
                f"中等样本（09:14:19）：RMS=1.718 g，出现周期性起伏，峰值约 9 g。",
                f"剧烈样本（09:29:53）：RMS=10.009 g，大幅振荡并呈拍频调制，峰值约 34 g。",
                "三栏对比直观显示不同工况下振幅差异可达数十倍。",
                "剧烈工况波形密集且连续，属于持续性强振动，而非单次撞击。",
                "可将 09:05:26 记录作为健康基线，用于后续趋势对比。",
            ],
        ),
        (
            "图5  前 0.5 秒波形叠加",
            "waveform_overlay_0p5s_cn.png",
            [
                "将平稳、中等、剧烈三类波形在前 0.5 秒叠加，便于直接比较振幅量级。",
                "绿线（平稳）几乎贴合零轴；橙线（中等）振幅约 ±5 g；红线（剧烈）达 ±30 g。",
                "剧烈波形频率高、幅值大，在短时段内即可完成多次大幅往复。",
                "该图适合用于向非专业人员展示振动严重程度差异。",
            ],
        ),
        (
            "图6  09:29 高振动簇波形对比",
            "waveform_0929_cluster_cn.png",
            [
                "展示 09:29:42 至 09:29:58 共 4 条连续记录，时间间隔仅 16 秒。",
                "4 条波形形态相似，说明列车在同一区段或同一工况下连续通过。",
                "09:29:53 RMS 最高（10.01 g），09:29:58 峰值最高（34.6 g）。",
                "前两条（42/50 秒）振幅相对较弱，后两条急剧增强，可能正在进入激励区段。",
                "建议重点核查该时刻列车位置是否处于道岔、曲线、焊缝或轨面缺陷区域。",
            ],
        ),
        (
            "图7  36 条波形全览",
            "waveform_grid_36_cn.png",
            [
                f"6×6 网格展示全部 36 条波形，颜色按 RMS 由绿（低）到红（高）编码。",
                f"共 {high_count} 条 RMS≥2 g，{low_count} 条 RMS<0.5 g。",
                "09:29 时段出现最红的两条记录，午后（12:00 后）多为绿色。",
                "部分低 RMS 记录可见孤立尖峰（如 08:48、12:12），属偶发冲击型。",
                "全览图有助于快速定位异常时段，而不必逐条查看数值。",
            ],
        ),
        (
            "图8  典型工况频谱三栏对比",
            "spectrum_comparison_3panel_cn.png",
            [
                "平稳工况：能量集中在 0.3 Hz 附近，高频段几乎可忽略。",
                "中等工况：主频约 673 Hz，幅值 0.70 g，高频成分开始显现。",
                "剧烈工况：主频约 517.5 Hz，幅值高达 6.05 g，500-550 Hz 带能量突出。",
                "从平稳到剧烈，频谱从低频主导转为中频窄带主导，工况识别特征明显。",
                "剧烈工况低频段（<5 Hz）也有约 3 g 成分，说明车体整体颠簸与局部高频共振并存。",
            ],
        ),
        (
            "图9  频谱叠加对比",
            "spectrum_overlay_0_800hz_cn.png",
            [
                "三色曲线叠加显示：平稳（绿）频谱接近零，剧烈（红）在 500-550 Hz 有显著峰群。",
                "红色阴影标注的主能量带 500-550 Hz 是异常识别的关键特征频率。",
                "中等工况能量分散在较高频段（约 650-700 Hz），与剧烈工况频谱形态不同。",
                "可基于 500-550 Hz 带能量设置频域报警阈值，提高异常检出率。",
            ],
        ),
        (
            "图10  低频段频谱对比",
            "spectrum_lowfreq_0_50hz_cn.png",
            [
                "聚焦 0-50 Hz 低频段，反映车体整体晃动和线路低频激励。",
                "平稳工况在 0.3 Hz 有明显峰值，属于正常运行中的低频摆动。",
                "剧烈工况在低频段幅值显著增大（约 3 g），说明车体整体颠簸加剧。",
                "低频分析适合评估乘坐舒适性，高频分析适合评估部件冲击损伤风险。",
            ],
        ),
        (
            "图11  09:29 簇频谱对比",
            "spectrum_0929_cluster_cn.png",
            [
                "4 条记录的频谱主峰均落在 500-550 Hz，形态高度一致。",
                "09:29:53 在 517 Hz 附近幅值达 6.0 g，为簇内最强。",
                "09:29:42/50 能量较弱，09:29:53/58 能量显著增强，与时域结论一致。",
                "频谱一致性进一步证实：这是同一物理事件在不同时刻的连续采样。",
                "建议将该频段的幅值积分能量作为该区段健康监测的特征参数。",
            ],
        ),
        (
            "图12  36 条频谱全览",
            "spectrum_grid_36_cn.png",
            [
                "6×6 网格展示全部频谱，颜色编码与波形全览一致。",
                "高 RMS 记录（红/橙色）在 500-600 Hz 均有明显峰群。",
                "低 RMS 记录（绿色）频谱平坦或仅有低频峰。",
                "09:29 和 12:47 时段频谱能量最集中，与 RMS 时序图高峰对应。",
                "该图可作为振动监测看板的参考模板，用于日常巡检快速筛查。",
            ],
        ),
    ]
    return analyses


def wrap_text(text: str, width: int = 52) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def add_text_page(pdf: PdfPages, title: str, lines: list[str], fontsize: int = 11):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor("white")
    y = 0.93
    fig.text(0.07, y, title, fontsize=16, fontweight="bold", va="top")
    y -= 0.04
    for line in lines:
        for wrapped in textwrap.wrap(line, width=46):
            y -= 0.028
            fig.text(0.07, y, wrapped, fontsize=fontsize, va="top")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_figure_analysis_page(pdf: PdfPages, title: str, image_path: Path, analysis_lines: list[str]):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor("white")
    fig.text(0.5, 0.97, title, ha="center", va="top", fontsize=15, fontweight="bold")

    ax_img = fig.add_axes([0.03, 0.40, 0.94, 0.54])
    img = mpimg.imread(image_path)
    ax_img.imshow(img)
    ax_img.axis("off")

    fig.text(0.05, 0.36, "【图表分析】", fontsize=13, fontweight="bold", va="top", color="#1e3a8a")
    y = 0.33
    for i, line in enumerate(analysis_lines, 1):
        block = textwrap.fill(f"{i}. {line}", width=48, subsequent_indent="   ")
        for row in block.split("\n"):
            y -= 0.026
            fig.text(0.05, y, row, fontsize=10.5, va="top")

    pdf.savefig(fig, dpi=200, bbox_inches="tight")
    plt.close(fig)


def build_pdf(records, paths, analyses, quiet, harsh):
    pdf_path = OUT / "上海17号线_1701_170022_21位_振动分析报告.pdf"
    rms_vals = [r["rms"] for r in records]
    peak_vals = [r["peak"] for r in records]
    fs_vals = [r["fs"] for r in records]

    with PdfPages(pdf_path) as pdf:
        # 封面
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.patch.set_facecolor("white")
        fig.text(0.5, 0.68, "振动数据分析报告", ha="center", fontsize=30, fontweight="bold")
        fig.text(0.5, 0.58, "上海地铁 17 号线（L17）", ha="center", fontsize=20)
        fig.text(0.5, 0.52, "1701 编组 · 170022 车 · 21 位测点", ha="center", fontsize=17)
        fig.text(0.5, 0.44, "数据日期：2026-05-28", ha="center", fontsize=14, color="#374151")
        fig.text(0.5, 0.38, "36 条样本 · 每条约 4096 点 · 加速度单位 g", ha="center", fontsize=12, color="#6b7280")
        fig.text(0.5, 0.30, "含时域分析、频域分析、逐图解读", ha="center", fontsize=12, color="#6b7280")
        fig.text(0.5, 0.12, "自动生成 · 高清 300 DPI 图表", ha="center", fontsize=10, color="#9ca3af")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # 摘要
        summary = [
            "一、数据概况",
            f"  样本数量：36 条；每条 4096 个连续采样点；记录时长约 1 秒。",
            f"  时间范围：08:12:34 — 13:02:34。",
            f"  采样频率：{min(fs_vals):.0f} — {max(fs_vals):.0f} Hz，均值约 {np.mean(fs_vals):.0f} Hz。",
            f"  RMS 范围：{min(rms_vals):.3f} — {max(rms_vals):.3f} g，均值 {np.mean(rms_vals):.3f} g。",
            f"  峰值范围：{min(peak_vals):.2f} — {max(peak_vals):.2f} g，均值 {np.mean(peak_vals):.2f} g。",
            "",
            "二、主要发现",
            "  1. 振动呈间歇性冲击模式，约 44% 记录 RMS ≥ 2 g。",
            "  2. 09:29 时段出现全天最严重事件（RMS 10.01 g，峰值 34.62 g）。",
            "  3. 剧烈工况主频集中在 517-534 Hz，具窄带特征。",
            f"  4. 最平稳基线：{quiet['time_str']}，RMS={quiet['rms']:.3f} g。",
            f"  5. 最剧烈事件：{harsh['time_str']}，RMS={harsh['rms']:.3f} g。",
            "  6. 午后（12:00 后）整体振动水平回落。",
            "",
            "三、建议",
            "  · 将 09:29 和 12:47 时刻与列车运行日志、区段位置交叉核对。",
            "  · 以 520 Hz 带能量和 RMS 联合设置报警阈值。",
            "  · 用 09:05:26 平稳记录作为健康基线开展趋势监测。",
        ]
        add_text_page(pdf, "报告摘要", summary)

        # 每图一页：图 + 分析
        for title, fname, analysis in analyses:
            add_figure_analysis_page(pdf, title, OUT / fname, analysis)

        # 结论
        conclusions = [
            "综合结论",
            "",
            "1. 时域结论",
            "   数据覆盖全天多个工况，振动强度差异极大。09:29 高振动簇是最需关注的事件，",
            "   4 条连续记录形态一致，表明列车通过了同一激励源区段。",
            "",
            "2. 频域结论",
            "   剧烈振动以 500-550 Hz 窄带能量为主，不是随机宽带噪声。该频率可能与轮轨",
            "   周期性激励或转向架局部共振相关，建议结合车速和轮径进一步核算。",
            "",
            "3. 运维建议",
            "   · 预警：RMS > 5 g 或峰值 > 25 g 时触发告警。",
            "   · 巡检：重点检查 09:29 和 12:47 对应里程的轨面状态。",
            "   · 监测：建立 RMS + 520Hz 带能量双指标趋势曲线。",
            "   · 基线：以 RMS=0.23 g 的 09:05:26 记录为参考健康状态。",
        ]
        add_text_page(pdf, "综合结论与建议", conclusions)

        d = pdf.infodict()
        d["Title"] = "上海17号线振动分析报告"
        d["Author"] = "Auto Analysis"
        d["Subject"] = "SH L17 1701-170022 Position 21 Vibration"

    return pdf_path


def main():
    records = load_records()
    paths, quiet, harsh, median, cluster, dom_freqs = generate_figures(records)
    analyses = build_analyses(records, quiet, harsh, median, cluster, dom_freqs)
    pdf_path = build_pdf(records, paths, analyses, quiet, harsh)
    print(f"Generated {len(paths)} figures at {DPI} DPI")
    for p in sorted(paths.values()):
        print(f"  {p.name} ({p.stat().st_size // 1024} KB)")
    print(f"PDF: {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

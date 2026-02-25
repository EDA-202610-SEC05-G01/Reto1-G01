"""Benchmark de req_1 a req_6 por porcentaje de dataset.

Ejecuta cada requerimiento 10 veces para cada tamaño de muestra:
10%, 20%, ..., 100% del dataset. Luego genera:
- Resumen en consola
- CSV con estadisticas por requerimiento
- Grafica N (numero de datos) vs tiempo promedio por requerimiento

Uso:
    python run_requirements_tests.py
"""

from __future__ import annotations

import csv
from collections import Counter
from statistics import mean

from App import logic
from DataStructures.List import array_list as lt

PERCENTAGES = list(range(10, 101, 10))
RUNS_PER_PERCENTAGE = 10
DATA_FILE = "computer_prices_large.csv"
OUTPUT_CSV = "benchmark_requirements_results.csv"
OUTPUT_PLOT = "benchmark_requirements_n_vs_time.png"
OUTPUT_PLOT_FALLBACK = "benchmark_requirements_n_vs_time.svg"


def _ok(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _stats(times_ms: list[float]) -> tuple[float, float, float]:
    return mean(times_ms), min(times_ms), max(times_ms)


def _build_hard_params(catalog: dict) -> dict:
    """Construye parametros exigentes basados en frecuencia del dataset."""
    brand_counter = Counter()
    cpu_tier_counter = Counter()
    cpu_gpu_counter = Counter()
    resolution_counter = Counter()

    price_min = None
    price_max = None

    size = lt.size(catalog["computers"])
    _ok(size > 0, "El catalogo no puede estar vacio")

    for i in range(size):
        computer = lt.get_element(catalog["computers"], i)

        brand_counter[computer["brand"]] += 1
        cpu_tier_counter[(computer["cpu_brand"], computer["cpu_tier"])] += 1
        cpu_gpu_counter[(computer["cpu_brand"], computer["gpu_model"])] += 1
        resolution_counter[computer["resolution"]] += 1

        price = float(computer["price"])
        if price_min is None or price < price_min:
            price_min = price
        if price_max is None or price > price_max:
            price_max = price

    req_1_brand = brand_counter.most_common(1)[0][0]
    req_3_cpu_brand, req_3_cpu_tier = cpu_tier_counter.most_common(1)[0][0]
    req_4_cpu_brand, req_4_gpu_model = cpu_gpu_counter.most_common(1)[0][0]
    req_5_resolution = resolution_counter.most_common(1)[0][0]

    return {
        "req_1_brand": req_1_brand,
        "req_2_min_price": price_min,
        "req_2_max_price": price_max,
        "req_3_cpu_brand": req_3_cpu_brand,
        "req_3_cpu_tier": req_3_cpu_tier,
        "req_4_cpu_brand": req_4_cpu_brand,
        "req_4_gpu_model": req_4_gpu_model,
        "req_5_filter": "CARO",
        "req_5_resolution": req_5_resolution,
        "req_5_start_year": 2018,
        "req_5_end_year": 2025,
        "req_6_start_year": 2018,
        "req_6_end_year": 2025,
    }


def _build_sample_catalog(full_catalog: dict, sample_size: int) -> dict:
    """Crea un nuevo catalogo con los primeros N elementos del catalogo completo."""
    catalog = logic.new_logic()
    full_size = lt.size(full_catalog["computers"])
    sample_size = min(sample_size, full_size)

    for i in range(sample_size):
        lt.add_last(catalog["computers"], lt.get_element(full_catalog["computers"], i))

    return catalog


def _run_req_1(catalog: dict, hard: dict) -> float:
    result = logic.req_1(catalog, hard["req_1_brand"])
    _ok(len(result) == 20, "req_1 debe retornar 20 elementos")
    _ok(result[1] >= 1, "req_1 no encontro resultados con una marca existente")
    return float(result[0])


def _run_req_2(catalog: dict, hard: dict) -> float:
    result = logic.req_2(catalog, hard["req_2_min_price"], hard["req_2_max_price"])
    _ok(len(result) == 9, "req_2 debe retornar 9 elementos")
    _ok(result[1] >= 1, "req_2 no encontro resultados para el rango de precios")
    return float(result[8])


def _run_req_3(catalog: dict, hard: dict) -> float:
    result = logic.req_3(catalog, hard["req_3_cpu_brand"], hard["req_3_cpu_tier"])
    _ok(len(result) == 10, "req_3 debe retornar 10 elementos")
    _ok(result[0] >= 1, "req_3 no encontro resultados con CPU existente")
    return float(result[9])


def _run_req_4(catalog: dict, hard: dict) -> float:
    result = logic.req_4(catalog, hard["req_4_cpu_brand"], hard["req_4_gpu_model"])
    _ok(len(result) == 7, "req_4 debe retornar 7 elementos")
    _ok(result[1] >= 1, "req_4 no encontro resultados para combinacion CPU/GPU existente")
    return float(result[0])


def _run_req_5(catalog: dict, hard: dict) -> float:
    result = logic.req_5(
        catalog,
        hard["req_5_filter"],
        hard["req_5_resolution"],
        hard["req_5_start_year"],
        hard["req_5_end_year"],
    )
    _ok(len(result) == 7, "req_5 debe retornar 7 elementos")
    _ok(result[2] >= 1, "req_5 no encontro resultados con resolucion/rango de anios")
    _ok(result[3] is not None, "req_5 no devolvio computador destacado")
    return float(result[0])


def _run_req_6(catalog: dict, hard: dict) -> float:
    result = logic.req_6(catalog, hard["req_6_start_year"], hard["req_6_end_year"])
    _ok(len(result) == 5, "req_6 debe retornar 5 elementos")
    _ok(result[1] >= 1, "req_6 no encontro resultados para el rango 2018-2025")
    return float(result[0])


def _save_csv(rows: list[dict]) -> None:
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["percentage", "n", "requirement", "avg_ms", "min_ms", "max_ms"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _plot_results_svg(results_by_req: dict[str, list[tuple[int, float]]]) -> None:
    """Grafica fallback en SVG para no depender de librerias externas."""
    width = 1100
    height = 700
    margin_left = 90
    margin_right = 40
    margin_top = 60
    margin_bottom = 90

    all_points = [point for points in results_by_req.values() for point in points]
    n_values = [n for n, _ in all_points]
    t_values = [t for _, t in all_points]

    min_n, max_n = min(n_values), max(n_values)
    min_t, max_t = min(t_values), max(t_values)
    if max_t == min_t:
        max_t = min_t + 1.0

    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    def x_map(n: int) -> float:
        return margin_left + ((n - min_n) / (max_n - min_n)) * plot_w if max_n != min_n else margin_left

    def y_map(t: float) -> float:
        return margin_top + (1 - ((t - min_t) / (max_t - min_t))) * plot_h

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="550" y="30" text-anchor="middle" font-size="22" font-family="Arial">N vs tiempo de ejecucion promedio por requerimiento</text>',
        f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#333" stroke-width="2"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height - margin_bottom}" stroke="#333" stroke-width="2"/>',
        f'<text x="{width / 2}" y="{height - 20}" text-anchor="middle" font-size="16" font-family="Arial">Numero de datos (N)</text>',
        f'<text x="28" y="{height / 2}" transform="rotate(-90,28,{height / 2})" text-anchor="middle" font-size="16" font-family="Arial">Tiempo promedio (ms)</text>',
    ]

    for n in sorted(set(n_values)):
        x = x_map(n)
        svg_parts.append(
            f'<line x1="{x:.2f}" y1="{height - margin_bottom}" x2="{x:.2f}" y2="{height - margin_bottom + 6}" stroke="#666"/>'
        )
        svg_parts.append(
            f'<text x="{x:.2f}" y="{height - margin_bottom + 24}" text-anchor="middle" font-size="12" font-family="Arial">{n}</text>'
        )

    y_ticks = 8
    for i in range(y_ticks + 1):
        value = min_t + (max_t - min_t) * i / y_ticks
        y = y_map(value)
        svg_parts.append(
            f'<line x1="{margin_left - 6}" y1="{y:.2f}" x2="{margin_left}" y2="{y:.2f}" stroke="#666"/>'
        )
        svg_parts.append(
            f'<line x1="{margin_left}" y1="{y:.2f}" x2="{width - margin_right}" y2="{y:.2f}" stroke="#ddd" stroke-dasharray="4 4"/>'
        )
        svg_parts.append(
            f'<text x="{margin_left - 10}" y="{y + 4:.2f}" text-anchor="end" font-size="12" font-family="Arial">{value:.1f}</text>'
        )

    legend_x = width - margin_right - 190
    legend_y = margin_top + 10

    for idx, (req_name, points) in enumerate(results_by_req.items()):
        color = colors[idx % len(colors)]
        poly = " ".join(f"{x_map(n):.2f},{y_map(t):.2f}" for n, t in points)
        svg_parts.append(
            f'<polyline points="{poly}" fill="none" stroke="{color}" stroke-width="2.5"/>'
        )

        for n, t in points:
            svg_parts.append(
                f'<circle cx="{x_map(n):.2f}" cy="{y_map(t):.2f}" r="3" fill="{color}"/>'
            )

        y_leg = legend_y + idx * 24
        svg_parts.append(
            f'<line x1="{legend_x}" y1="{y_leg}" x2="{legend_x + 28}" y2="{y_leg}" stroke="{color}" stroke-width="3"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 36}" y="{y_leg + 4}" font-size="13" font-family="Arial">{req_name}</text>'
        )

    svg_parts.append("</svg>")

    with open(OUTPUT_PLOT_FALLBACK, "w", encoding="utf-8") as file:
        file.write("\n".join(svg_parts))


def _plot_results(results_by_req: dict[str, list[tuple[int, float]]]) -> tuple[bool, str | None, str | None]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        _plot_results_svg(results_by_req)
        return True, f"matplotlib no esta instalado; se genero {OUTPUT_PLOT_FALLBACK}", OUTPUT_PLOT_FALLBACK

    plt.figure(figsize=(10, 6))

    for req_name, points in results_by_req.items():
        n_values = [n for n, _ in points]
        avg_values = [avg for _, avg in points]
        plt.plot(n_values, avg_values, marker="o", linewidth=1.8, label=req_name)

    plt.title("N vs tiempo de ejecucion promedio por requerimiento")
    plt.xlabel("Numero de datos (N)")
    plt.ylabel("Tiempo promedio (ms)")
    plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT, dpi=150)
    plt.close()

    return True, None, OUTPUT_PLOT


def main() -> int:
    full_catalog = logic.new_logic()
    total, _, _, _, _, _ = logic.load_data(full_catalog, DATA_FILE)
    _ok(total > 0, "No se cargaron computadores")

    req_runners = [
        ("req_1", _run_req_1),
        ("req_2", _run_req_2),
        ("req_3", _run_req_3),
        ("req_4", _run_req_4),
        ("req_5", _run_req_5),
        ("req_6", _run_req_6),
    ]

    rows: list[dict] = []
    results_by_req: dict[str, list[tuple[int, float]]] = {name: [] for name, _ in req_runners}

    print(f"Dataset total cargado: {total} registros")
    print(
        f"Ejecucion: {RUNS_PER_PERCENTAGE} corridas por requerimiento para cada porcentaje "
        f"{PERCENTAGES[0]}%..{PERCENTAGES[-1]}%\n"
    )

    for percentage in PERCENTAGES:
        sample_size = max(1, int(total * percentage / 100))
        catalog = _build_sample_catalog(full_catalog, sample_size)
        hard = _build_hard_params(catalog)

        print(f"[{percentage:>3}%] N={sample_size}")

        for req_name, runner in req_runners:
            times: list[float] = []
            for _ in range(RUNS_PER_PERCENTAGE):
                times.append(runner(catalog, hard))

            avg_ms, min_ms, max_ms = _stats(times)
            results_by_req[req_name].append((sample_size, avg_ms))
            rows.append(
                {
                    "percentage": percentage,
                    "n": sample_size,
                    "requirement": req_name,
                    "avg_ms": f"{avg_ms:.6f}",
                    "min_ms": f"{min_ms:.6f}",
                    "max_ms": f"{max_ms:.6f}",
                }
            )
            print(
                f"  - {req_name}: avg={avg_ms:.3f} ms "
                f"min={min_ms:.3f} ms max={max_ms:.3f} ms"
            )

        print("")

    _save_csv(rows)
    print(f"Resultados tabulares guardados en: {OUTPUT_CSV}")

    plotted, plot_error, plot_path = _plot_results(results_by_req)
    if plotted:
        print(f"Grafica guardada en: {plot_path}")
        if plot_error is not None:
            print(plot_error)
        return 0

    print(f"No se pudo crear la grafica: {plot_error}")
    print("Instala matplotlib para generar la imagen PNG: python -m pip install matplotlib")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

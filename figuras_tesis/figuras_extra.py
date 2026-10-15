"""Figuras adicionales para el plan de tesis y el paper, con el mismo estilo que figuras_tesis.py (v2).

Uso: <python del .venv del proyecto> figuras_extra.py <carpeta_salida>
- figA_ejemplos_clases: un incisivo lateral inferior por clase (foto original + corte CBCT vestíbulo-lingual).
  Casos elegidos con criterio objetivo: clasificados correctamente por el ensamble en desarrollo (OOF)
  con confianza >= 0.92.
- figB_flujo_cohorte: diagrama de selección de la cohorte y partición por paciente (desde las tablas).
- fig2_matrices_confusion_prueba_compacta: las 4 matrices de prueba en una fila (para el paper, 9 páginas).
"""
import sys
from pathlib import Path

PROY = Path(r"C:\Cursos\Ciclo IX\Computación Grafica\ProyectoComputaciónGrafica")
sys.path.insert(0, str(PROY / "auditoria"))
import figuras_tesis as ft  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from PIL import Image  # noqa: E402

OUT = Path(sys.argv[1])
CM = ft.CM
ANCHO = ft.ANCHO
EJEMPLOS = [("N", "013_42", "Normal"), ("F", "231_32", "Fenestración"), ("D", "089_32", "Dehiscencia")]


def guardar(fig, nombre):
    for ext, kw in (("pdf", {}), ("png", {"dpi": 600})):
        fig.savefig(OUT / f"{nombre}.{ext}", **kw)
    w, h = fig.get_size_inches() / CM
    print(f"{nombre}: {w:.1f} x {h:.1f} cm")
    plt.close(fig)


def fig_ejemplos():
    fig = plt.figure(figsize=(ANCHO, 5.9 * CM), layout="constrained")
    sub = fig.subfigures(1, 3, wspace=0.02)
    for s, (et, clave, titulo) in zip(sub, EJEMPLOS):
        foto = Image.open(PROY / "fdtooth_preprocesado/fotos/original" / f"{clave}.jpg")
        hu = np.load(PROY / "fdtooth_roi_cbct/roi" / f"{clave}.npz")["hu"].astype(float) * 4000 / 255 - 1000
        corte = np.flipud(hu[:, 23:28, :].mean(1).T)   # corona abajo, como la foto en orientación canónica
        rel = (foto.width / foto.height, corte.shape[1] / corte.shape[0])   # misma altura, sin deformar
        a1, a2 = s.subplots(1, 2, gridspec_kw={"width_ratios": rel, "wspace": 0.04})
        a1.imshow(foto)
        a2.imshow(corte, cmap="gray", vmin=-200, vmax=1800)
        for a, rot in ((a1, "Fotografía"), (a2, "CBCT")):
            a.axis("off")
            a.text(0.5, -0.03, rot, transform=a.transAxes, ha="center", va="top", fontsize=7)
        a2.text(0.04, 0.97, "L", transform=a2.transAxes, color="white", fontsize=7, va="top", bbox=dict(fc="black", ec="none", pad=0.6))
        a2.text(0.96, 0.97, "V", transform=a2.transAxes, color="white", fontsize=7, va="top", ha="right", bbox=dict(fc="black", ec="none", pad=0.6))
        s.suptitle(f"({'abc'['NFD'.index(et)]}) {titulo} ({et})", fontsize=8)
    guardar(fig, "figA_ejemplos_clases")


def caja(ax, x, y, w, h, texto, fondo="#FFFFFF", borde="#000000", negrita=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012",
                                fc=fondo, ec=borde, lw=0.7))
    lineas = texto.split("\n")
    if negrita:
        ax.text(x + w / 2, y + h - 0.025, negrita, ha="center", va="top", fontsize=7.5, weight="bold")
        ax.text(x + w / 2, y + h - 0.075, "\n".join(lineas), ha="center", va="top", fontsize=7,
                linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=7, linespacing=1.35)


def flecha(ax, x0, y0, x1, y1):
    ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", lw=0.7, color="#000000",
                                                        shrinkA=0, shrinkB=0, mutation_scale=7))


def fig_flujo():
    d = pd.read_csv(PROY / "fdtooth_preprocesado/tablas/dientes.csv", dtype={"ID": str})
    p = pd.read_csv(PROY / "fdtooth_preprocesado/tablas/pacientes.csv", dtype={"ID": str})
    e = pd.read_csv(PROY / "fdtooth_preprocesado/tablas/excluidos.csv", dtype={"ID": str})
    c = pd.read_csv(PROY / "fdtooth_roi_cbct/tablas/dientes_cbct.csv", dtype={"ID": str})
    n_csv = int(e.motivo.str.startswith("CSV vs JSON").sum())
    n_tot = len(p) + len(e)
    cnt = lambda q: q.etiqueta.value_counts().reindex(list("NFD")).tolist()  # noqa: E731
    sp = {s: (int((p.split == s).sum()), len(d[d.split == s]), cnt(d[d.split == s])) for s in ("development", "test")}
    sin_roi = int((~c.cbct_encontrado).sum())
    print("flujo:", n_tot, len(e), n_csv, len(p), len(d), cnt(d), sp, sin_roi)

    fig = plt.figure(figsize=(ANCHO, 7.6 * CM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    N, F, D = cnt(d)
    xc = 0.35   # eje de la columna principal
    caja(ax, 0.13, 0.79, 0.44, 0.19, f"{n_tot} pacientes con fotografía intraoral\nfrontal y CBCT",
         negrita="Dataset FDTooth")
    caja(ax, 0.13, 0.50, 0.44, 0.21,
         f"{len(p)} pacientes · {len(d)} dientes anteriores\nN {N} · F {F} · D {D}\n"
         f"CBCT segmentado: {len(d) - sin_roi} de {len(d)} dientes", negrita="Cohorte analizada")
    caja(ax, 0.63, 0.64, 0.35, 0.22, f"{len(e)} pacientes\n{n_csv}: discordancia CSV–JSON\n"
         f"{len(e) - n_csv}: coordenadas incompatibles", fondo="#F2F2F2", negrita="Excluidos")
    flecha(ax, xc, 0.79, xc, 0.71)
    flecha(ax, xc, 0.75, 0.63, 0.75)
    flecha(ax, xc, 0.50, xc, 0.44)
    ax.text(xc, 0.42, "Partición por paciente", ha="center", va="center", fontsize=7, style="italic")
    ax.plot([xc, xc], [0.40, 0.385], color="#000000", lw=0.7)
    ax.plot([0.255, 0.745], [0.385, 0.385], color="#000000", lw=0.7)
    for x, s, tit, extra in ((0.03, "development", "Desarrollo",
                              "Validación cruzada anidada,\n5 folds agrupados por paciente"),
                             (0.52, "test", "Prueba retenida", "Evaluada una sola vez\ncon los modelos ya elegidos")):
        npac, ndie, (n, f, dd) = sp[s]
        flecha(ax, x + 0.225, 0.385, x + 0.225, 0.32)
        caja(ax, x, 0.07, 0.45, 0.25, f"{npac} pacientes · {ndie} dientes\nN {n} · F {f} · D {dd}\n{extra}",
             negrita=tit)
    guardar(fig, "figB_flujo_cohorte")


def fig_matrices_compacta():
    test, _ = ft.cargar_prueba()
    ids = [ft.FINAL, "M2_fusion_convnextv2_tiny", "M1_cbct_rf", "M3_cbct_dinov2_lr"]
    fig, ejes = plt.subplots(1, 4, figsize=(ANCHO, 4.6 * CM), layout="constrained", sharey=True)
    for k, (ax, i) in enumerate(zip(ejes, ids)):
        cm = test.filas[i]["confusion_matrix"]
        fr = cm / cm.sum(1, keepdims=True)
        ax.imshow(fr, cmap="Blues", vmin=0, vmax=1)
        for r in range(3):
            for c in range(3):
                ax.text(c, r, f"{cm[r, c]}\n{fr[r, c]:.0%}", ha="center", va="center", fontsize=6,
                        color="white" if fr[r, c] > 0.5 else "#000000", linespacing=1.1)
        ax.set_xticks(range(3), ft.CLASES)
        ax.set_yticks(range(3), ft.CLASES)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(f"({'abcd'[k]}) {ft.corto(i)}\nMacro-F1 {test.filas[i]['macro_f1']:.3f}", fontsize=7)
        ax.set_xlabel("Predicha")
        print(ft.corto(i), cm.tolist())
    ejes[0].set_ylabel("Real")
    guardar(fig, "fig2_matrices_confusion_prueba_compacta")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    with plt.rc_context(ft.ESTILO2):
        fig_ejemplos()
        fig_flujo()
        fig_matrices_compacta()


def fig1_v3():
    """Igual que fig1_v2, pero el antecedente (0.548, solo medido en desarrollo) se dibuja solo en el panel (a)."""
    dev, (test, _) = ft.cargar_desarrollo(), ft.cargar_prueba()
    fig, ejes = plt.subplots(1, 2, figsize=(ANCHO, 6.0 * CM), sharey=True, layout="constrained")
    ancho = 0.26
    for ax, conj, titulo in ((ejes[0], dev, "(a) Desarrollo (validación cruzada, 174 pacientes)"),
                             (ejes[1], test, "(b) Prueba retenida (43 pacientes)")):
        series = [(m, ft.EN_TEST[m], np.arange(3) + (k - 1) * ancho) for k, m in enumerate(("M1", "M2", "M3"))]
        series.append(("E", [ft.FINAL if conj is test else ft.FINAL_DEV], np.array([3.0])))
        for m, ids, x in series:
            v = np.array([conj.filas[i]["macro_f1"] for i in ids])
            ic = np.array([conj.ic(i) for i in ids])
            ax.bar(x, v, ancho - 0.03, color=ft.COLOR2[m], label=ft.LEYENDA2[m], zorder=2)
            ax.errorbar(x, v, yerr=[v - ic[:, 0], ic[:, 1] - v], fmt="none", ecolor="#000000", elinewidth=0.6,
                        capsize=1.5, capthick=0.6, zorder=3)
            for xi, vi, hi in zip(x, v, ic[:, 1]):
                ax.text(xi, hi + 0.02, f"{vi:.2f}", ha="center", va="bottom", fontsize=6.5, rotation=90)
            print(titulo[:3], [f"{ft.corto(i)} {conj.filas[i]['macro_f1']:.3f}" for i in ids])
        if conj is dev:
            ax.axhline(0.548, color="#000000", ls="--", lw=0.8, zorder=1,
                       label="Antecedente (solo foto, desarrollo)")
        ax.set_xticks([0, 1, 2, 3], ["Foto", "CBCT", "Fusión", "Ensamble"])
        ax.set_xlim(-0.5, 3.4)
        ax.set_ylim(0, 1.08)
        ax.set_yticks(np.arange(0, 1.01, 0.2))
        ax.yaxis.set_major_formatter("{x:.2f}")
        ax.set_title(titulo, loc="left", fontsize=7.5)
        ft.rejilla_y(ax)
    ejes[0].set_ylabel("Macro-F1")
    h, lab = ejes[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="outside lower center", ncol=3, handlelength=1.6, columnspacing=1.2)
    guardar(fig, "fig1_macro_f1_metodologias_v3")


if __name__ == "__main__":
    with plt.rc_context(ft.ESTILO2):
        fig1_v3()

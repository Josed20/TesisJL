"""Figuras del paper con una sola metodología: ensambles híbridos (Deep Learning + Machine Learning).

Uso: <python del .venv del proyecto> figuras_hibrido.py <carpeta_salida>
No entrena nada: lee las predicciones guardadas con auditoria/figuras_tesis.py.
- figC_macro_f1_componentes: Macro-F1 (desarrollo y prueba) del ensamble híbrido seleccionado y de sus
  componentes, con ConvNeXt V2 solo foto y el antecedente (0.548, solo desarrollo) como referencia.
- figD_matrices_confusion_hibrido: matrices de prueba del ensamble y de sus tres componentes, en una fila.
- figE_matriz_confusion_ensamble: solo la matriz de prueba del ensamble elegido (Fig. 4 del paper).
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
from sklearn.metrics import confusion_matrix  # noqa: E402

OUT = Path(sys.argv[1])
CM = ft.CM
ANCHO = ft.ANCHO
# (id en desarrollo, id en prueba, etiqueta)
MODELOS = [("M2_foto_convnextv2_tiny",) * 2 + ("ConvNeXt V2\n(Foto)",),
           ("M1_cbct_rf",) * 2 + ("RF\n(CBCT)",),
           ("M2_cbct_convnextv2_tiny",) * 2 + ("ConvNeXt V2\n(CBCT)",),
           ("M2_fusion_convnextv2_tiny",) * 2 + ("ConvNeXt V2\n(Foto+CBCT)",),
           (ft.FINAL_DEV, ft.FINAL, "Ensamble\nhíbrido")]
COL_DEV, COL_TEST = "#9DB9E0", "#2F5597"


def guardar(fig, nombre):
    for ext, kw in (("pdf", {}), ("png", {"dpi": 600})):
        fig.savefig(OUT / f"{nombre}.{ext}", **kw)
    w, h = fig.get_size_inches() / CM
    print(f"{nombre}: {w:.1f} x {h:.1f} cm")
    plt.close(fig)


def fig_componentes(dev, test):
    fig, ax = plt.subplots(figsize=(ANCHO, 5.6 * CM), layout="constrained")
    ancho = 0.36
    x = np.arange(len(MODELOS))
    for desp, conj, k, col, lab in ((-ancho / 2, dev, 0, COL_DEV, "Desarrollo (validación cruzada, 174 pacientes)"),
                                    (ancho / 2, test, 1, COL_TEST, "Prueba retenida (43 pacientes)")):
        ids = [m[k] for m in MODELOS]
        v = np.array([conj.filas[i]["macro_f1"] for i in ids])
        ic = np.array([conj.ic(i) for i in ids])
        ax.bar(x + desp, v, ancho - 0.03, color=col, label=lab, zorder=2)
        ax.errorbar(x + desp, v, yerr=[v - ic[:, 0], ic[:, 1] - v], fmt="none", ecolor="#000000",
                    elinewidth=0.6, capsize=1.5, capthick=0.6, zorder=3)
        for xi, vi, hi in zip(x + desp, v, ic[:, 1]):
            ax.text(xi, hi + 0.015, f"{vi:.3f}", ha="center", va="bottom", fontsize=6, rotation=90)
        print(lab[:10], [f"{i} {conj.filas[i]['macro_f1']:.3f} [{a:.3f}, {b:.3f}]" for i, (a, b) in zip(ids, ic)])
    ax.axhline(0.548, color="#000000", ls="--", lw=0.8, zorder=1, label="Antecedente (solo foto, desarrollo)")
    ax.axvline(0.5, color="#BFBFBF", lw=0.6, zorder=1)
    ax.set_xticks(x, [m[2] for m in MODELOS])
    ax.set_xlim(-0.55, len(MODELOS) - 0.45)
    ax.set_ylim(0, 1.08)
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.yaxis.set_major_formatter("{x:.2f}")
    ax.set_ylabel("Macro-F1")
    ft.rejilla_y(ax)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside lower center", ncol=2, handlelength=1.6,
               columnspacing=1.2)
    guardar(fig, "figC_macro_f1_componentes")


def fig_matrices(test):
    ids = [(ft.FINAL, "Ensamble híbrido"), ("M2_fusion_convnextv2_tiny", "ConvNeXt V2 (Foto+CBCT)"),
           ("M2_cbct_convnextv2_tiny", "ConvNeXt V2 (CBCT)"), ("M1_cbct_rf", "RF (CBCT)")]
    fig, ejes = plt.subplots(1, 4, figsize=(ANCHO, 4.6 * CM), layout="constrained", sharey=True)
    for k, (ax, (i, tit)) in enumerate(zip(ejes, ids)):
        pred = test.probas[i].argmax(1)
        cm = confusion_matrix(test.y, pred, labels=[0, 1, 2])
        if i in test.filas:
            assert (cm == test.filas[i]["confusion_matrix"]).all(), i
        mf1 = ft.macro_f1(test.y, pred)[0]
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
        ax.set_title(f"({'abcd'[k]}) {tit}\nMacro-F1 {mf1:.3f}", fontsize=6)
        ax.set_xlabel("Predicha")
        print(tit, cm.tolist(), f"{mf1:.3f}")
    ejes[0].set_ylabel("Real")
    guardar(fig, "figD_matrices_confusion_hibrido")


def fig_matriz_ensamble(test):
    """Solo la matriz del ensamble elegido (Ambas + RF), para el paper."""
    pred = test.probas[ft.FINAL].argmax(1)
    cm = confusion_matrix(test.y, pred, labels=[0, 1, 2])
    assert (cm == test.filas[ft.FINAL]["confusion_matrix"]).all()
    fr = cm / cm.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(6.0 * CM, 5.4 * CM), layout="constrained")
    ax.imshow(fr, cmap="Blues", vmin=0, vmax=1)
    for r in range(3):
        for c in range(3):
            ax.text(c, r, f"{cm[r, c]}\n{fr[r, c]:.0%}", ha="center", va="center", fontsize=8,
                    color="white" if fr[r, c] > 0.5 else "#000000", linespacing=1.1)
    ax.set_xticks(range(3), ft.CLASES)
    ax.set_yticks(range(3), ft.CLASES)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("Clase predicha")
    ax.set_ylabel("Clase real")
    print("Ensamble", cm.tolist())
    guardar(fig, "figE_matriz_confusion_ensamble")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    dev, (test, _) = ft.cargar_desarrollo(), ft.cargar_prueba()
    with plt.rc_context(ft.ESTILO2):
        fig_componentes(dev, test)
        fig_matrices(test)
        fig_matriz_ensamble(test)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def run_report(fba_result, thermo_result, ode_result):
    os.makedirs('output', exist_ok=True)

    # -- Графики
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    reactions = thermo_result['reactions']
    dg_std = thermo_result['dg_std']
    dg_min = thermo_result['dg_min']
    dg_max = thermo_result['dg_max']
    colors_bar = ['red' if v > 0 else ('orange' if v > -5 else 'green') for v in dg_std]
    err_lo = [abs(s - mn) for s, mn in zip(dg_std, dg_min)]
    err_hi = [abs(mx - s) for s, mx in zip(dg_std, dg_max)]
    ax1.bar(reactions, dg_std, color=colors_bar, alpha=0.8, yerr=[err_lo, err_hi], capsize=5)
    ax1.axhline(0, color='black', linewidth=1.2, linestyle='--')
    ax1.set_xlabel('Реакция')
    ax1.set_ylabel('ΔG, кДж/моль')
    ax1.set_title('Термодинамический анализ пути синтеза n-бутанола')
    plt.tight_layout()
    fig1.savefig('output/thermo.png', dpi=150)
    plt.close()

    t = ode_result['t']
    sol_free = ode_result['sol_free']
    sol_immob = ode_result['sol_immob']
    enzymes = ode_result['enzymes']
    kd_free = ode_result['kd_free']
    kd_immob = ode_result['kd_immob']
    n = len(enzymes)

    fig2, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(t, sol_free[:, n+1],  label='Свободные ферменты')
    axes[0].plot(t, sol_immob[:, n+1], label='Иммобилизованные ферменты')
    axes[0].set_xlabel('Время, ч')
    axes[0].set_ylabel('n-Бутанол, ммоль/л')
    axes[0].set_title('Накопление продукта')
    axes[0].legend()
    axes[1].bar(enzymes, [np.log(2)/kd_free[e] for e in enzymes], alpha=0.7, label='Свободные')
    axes[1].bar(enzymes, [np.log(2)/kd_immob[e] for e in enzymes], alpha=0.7, label='Иммобилизованные')
    axes[1].set_ylabel('t½, ч')
    axes[1].set_title('Периоды полуинактивации ферментов')
    axes[1].legend()
    plt.tight_layout()
    fig2.savefig('output/kinetics.png', dpi=150)
    plt.close()

    # -- PDF
    doc = SimpleDocTemplate('output/report.pdf', pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Title'], fontSize=14, spaceAfter=12, fontName='Arial-Bold')
    h_style = ParagraphStyle('h', parent=styles['Heading2'], fontSize=12, spaceAfter=6, fontName='Arial-Bold')
    body_style = ParagraphStyle('body', parent=styles['Normal'], fontName='Arial')

    story = []

    story.append(Paragraph('ButanolPathOptimizer: Отчёт анализа', title_style))
    story.append(Paragraph('Пайплайн оценки бесклеточного синтеза n-бутанола', body_style))
    story.append(Spacer(1, 0.5*cm))

    # FBA
    story.append(Paragraph('1. Стехиометрическое моделирование (FBA)', h_style))
    fba_data = [
        ['Параметр', 'Значение'],
        ['Статус оптимизации', fba_result['status']],
        ['Поток бутанола', f"{fba_result['flux_btol']:.4f}"],
        ['Поток глюкозы', f"{abs(fba_result['flux_glc']):.4f}"],
        ['Молярный выход', f"{fba_result['yield_mol']:.3f} моль/моль"],
        ['Массовый выход', f"{fba_result['yield_g_g']:.3f} г/г"],
    ]
    t1 = Table(fba_data, colWidths=[9*cm, 7*cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (-1,0), 'Arial-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Arial'),
    ]))
    story.append(t1)
    story.append(Spacer(1, 0.5*cm))

    # Thermo
    story.append(Paragraph('2. Термодинамический анализ', h_style))
    story.append(Image('output/thermo.png', width=16*cm, height=8*cm))
    story.append(Spacer(1, 0.3*cm))
    thermo_data = [['Реакция', 'ΔG (кДж/моль)', 'Статус']]
    for r, dg, flag in zip(thermo_result['reactions'], thermo_result['dg_std'], thermo_result['flags']):
        thermo_data.append([r, str(dg), flag])
    t2 = Table(thermo_data, colWidths=[6*cm, 5*cm, 5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (-1,0), 'Arial-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Arial'),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.5*cm))

    # ODE
    story.append(Paragraph('3. Кинетическое моделирование (ODE)', h_style))
    story.append(Image('output/kinetics.png', width=16*cm, height=6*cm))
    story.append(Spacer(1, 0.3*cm))
    ode_data = [
        ['Сценарий', 'Выход бутанола (ммоль/л)', 'Выход (%)'],
        ['Свободные ферменты', f"{ode_result['yield_free']:.2f}", f"{ode_result['yield_free']/ode_result['S0']*100:.1f}%"],
        ['Иммобилизованные ферменты', f"{ode_result['yield_immob']:.2f}", f"{ode_result['yield_immob']/ode_result['S0']*100:.1f}%"],
    ]
    t3 = Table(ode_data, colWidths=[7*cm, 5*cm, 4*cm])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (-1,0), 'Arial-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Arial'),
    ]))
    story.append(t3)

    doc.build(story)
    print("[Report] PDF сохранён: output/report.pdf")
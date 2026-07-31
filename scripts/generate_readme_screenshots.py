"""
DevScope - GitHub README Screenshot Generator
Renders high-resolution, dark-themed executive visualization mockups for
repository documentation and portfolio presentation.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI

SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Dark Executive Palette
BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
TEXT_COLOR = "#F8FAFC"
ACCENT_BLUE = "#38BDF8"
ACCENT_GREEN = "#10B981"
ACCENT_PURPLE = "#A855F7"
ACCENT_AMBER = "#F59E0B"
GRID_COLOR = "#334155"

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": CARD_COLOR,
    "axes.edgecolor": GRID_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "grid.color": GRID_COLOR,
    "font.sans-serif": "DejaVu Sans",
    "font.family": "sans-serif"
})

def generate_dashboard_overview():
    """Generates screenshots/dashboard_overview.png"""
    fig = plt.figure(figsize=(14, 8), dpi=150)
    gs = fig.add_gridspec(2, 4, height_ratios=[1, 2], wspace=0.3, hspace=0.35)
    
    # KPI Cards
    kpis = [
        ("Market Health Index", "78.4 / 100", ACCENT_BLUE),
        ("AI Adoption Rate", "27.5%", ACCENT_GREEN),
        ("Remote Share", "42.1%", ACCENT_PURPLE),
        ("Median Salary USD", "$67,500", ACCENT_AMBER)
    ]
    
    for i, (title, val, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.add_patch(patches.Rectangle((0, 0), 1, 1, color=CARD_COLOR, ec=GRID_COLOR, lw=1.5, transform=ax.transAxes))
        ax.text(0.5, 0.65, title, ha="center", va="center", fontsize=11, color="#94A3B8", fontweight="bold", transform=ax.transAxes)
        ax.text(0.5, 0.3, val, ha="center", va="center", fontsize=20, color=color, fontweight="bold", transform=ax.transAxes)
        
    # Main Chart 1: Remote Work Distribution
    ax_main1 = fig.add_subplot(gs[1, :2])
    modes = ["Remote", "Hybrid", "In-person"]
    counts = [131069, 124738, 55521]
    bars = ax_main1.barh(modes, counts, color=[ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER], edgecolor=GRID_COLOR, height=0.55)
    ax_main1.set_title("Workplace Policy Distribution (311K Respondents)", fontsize=12, fontweight="bold", pad=12)
    ax_main1.grid(axis="x", linestyle="--", alpha=0.4)
    ax_main1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, n: f"{int(x/1000)}k"))
    for bar in bars:
        width = bar.get_width()
        ax_main1.text(width + 2000, bar.get_y() + bar.get_height()/2, f"{int(width):,}", ha="left", va="center", color=TEXT_COLOR, fontsize=10)

    # Main Chart 2: Top Roles Distribution
    ax_main2 = fig.add_subplot(gs[1, 2:])
    roles = ["Full-Stack", "Backend", "Frontend", "Data/AI", "DevOps/Cloud"]
    role_counts = [112400, 95300, 48200, 31500, 24000]
    ax_main2.bar(roles, role_counts, color=ACCENT_BLUE, edgecolor=GRID_COLOR, width=0.55)
    ax_main2.set_title("Developer Role Composition", fontsize=12, fontweight="bold", pad=12)
    ax_main2.grid(axis="y", linestyle="--", alpha=0.4)
    ax_main2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, n: f"{int(x/1000)}k"))

    plt.suptitle("DevScope — Executive Workforce Intelligence Dashboard", fontsize=16, fontweight="bold", color=TEXT_COLOR, y=0.98)
    out_path = SCREENSHOTS_DIR / "dashboard_overview.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path.name}")

def generate_language_distribution():
    """Generates screenshots/language_distribution.png"""
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    langs = ["JavaScript", "HTML/CSS", "Python", "SQL", "TypeScript", "Java", "C#", "C++", "PHP", "Go", "Rust"]
    counts = [182400, 168200, 154100, 142300, 128500, 98400, 89200, 71500, 62100, 41200, 28500]
    
    colors = [ACCENT_BLUE if l in ["Python", "Rust", "TypeScript"] else "#475569" for l in langs]
    bars = ax.barh(langs[::-1], counts[::-1], color=colors[::-1], edgecolor=GRID_COLOR, height=0.6)
    ax.set_title("Programming Language Popularity (1.59M Recorded Tags)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Total Mentions Across Survey Respondents", fontsize=11, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, n: f"{int(x/1000)}k"))
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 2000, bar.get_y() + bar.get_height()/2, f"{int(width):,}", ha="left", va="center", color=TEXT_COLOR, fontsize=10)

    out_path = SCREENSHOTS_DIR / "language_distribution.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path.name}")

def generate_salary_analysis():
    """Generates screenshots/salary_analysis.png"""
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    exp_tiers = ["0-2 years (Entry)", "3-5 years (Mid)", "6-10 years (Senior)", "11+ years (Lead/Executive)"]
    medians = [42000, 68000, 95000, 135000]
    remotes = [48000, 78000, 112000, 155000]
    
    x = np.arange(len(exp_tiers))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, medians, width, label="In-Person / Hybrid Median", color="#475569", edgecolor=GRID_COLOR)
    rects2 = ax.bar(x + width/2, remotes, width, label="Remote Median (+17.4% Premium)", color=ACCENT_GREEN, edgecolor=GRID_COLOR)
    
    ax.set_title("Median Annual Compensation USD by Experience Tier & Work Mode", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(exp_tiers, fontsize=10, fontweight="bold")
    ax.set_ylabel("Compensation (USD)", fontsize=11, fontweight="bold")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, n: f"${int(y/1000)}k"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(facecolor=CARD_COLOR, edgecolor=GRID_COLOR, fontsize=10)
    
    for bar in rects2:
        height = bar.get_height()
        ax.annotate(f"${int(height/1000)}k",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', color=ACCENT_GREEN, fontweight='bold', fontsize=10)

    out_path = SCREENSHOTS_DIR / "salary_analysis.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path.name}")

def generate_ai_adoption():
    """Generates screenshots/ai_adoption.png"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)
    
    # AI Tool Share
    tools = ["ChatGPT", "GitHub Copilot", "Claude", "Google Gemini", "Other AI"]
    tool_counts = [48200, 24500, 6800, 4200, 2037]
    ax1.pie(tool_counts, labels=tools, colors=[ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_AMBER, "#64748B"],
            autopct="%1.1f%%", startangle=140, textprops={'color': TEXT_COLOR, 'fontsize': 10, 'weight': 'bold'})
    ax1.set_title("AI Developer Tool Utilization Share (85.7K Mentions)", fontsize=12, fontweight="bold", pad=12)
    
    # Seniority Lag
    tiers = ["Senior-level", "Mid-level", "Entry-level"]
    rates = [76.5, 54.2, 32.5]
    bars = ax2.barh(tiers, rates, color=[ACCENT_GREEN, ACCENT_BLUE, ACCENT_AMBER], edgecolor=GRID_COLOR, height=0.5)
    ax2.set_title("AI Adoption Rate by Developer Seniority Tier", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("AI Adoption Rate (%)", fontsize=11, fontweight="bold")
    ax2.set_xlim(0, 100)
    ax2.grid(axis="x", linestyle="--", alpha=0.4)
    
    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 2, bar.get_y() + bar.get_height()/2, f"{w}%", ha="left", va="center", color=TEXT_COLOR, fontweight="bold")

    plt.suptitle("DevScope — AI Adoption & Workflow Penetration Intelligence", fontsize=15, fontweight="bold", y=1.02)
    out_path = SCREENSHOTS_DIR / "ai_adoption.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path.name}")

def generate_data_model():
    """Generates screenshots/data_model.png"""
    fig, ax = plt.subplots(figsize=(13, 7), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")
    
    # Draw Fact Box (Center)
    fact_box = patches.FancyBboxPatch((3.5, 2.5), 3.0, 2.0, boxstyle="round,pad=0.2", fc=CARD_COLOR, ec=ACCENT_BLUE, lw=2)
    ax.add_patch(fact_box)
    ax.text(5.0, 3.8, "FACT TABLE\nRespondents", ha="center", va="center", fontsize=12, fontweight="bold", color=ACCENT_BLUE)
    ax.text(5.0, 3.0, "• respondent_id (PK)\n• survey_year (PK)\n• country, exp, comp\n• remote_work_mode", ha="center", va="center", fontsize=9, color="#94A3B8")

    # Dimensions
    dims = [
        ("DimRespondentLanguages", (0.5, 4.5), "1-to-Many on ID+Year\n• language_name"),
        ("DimRespondentCloud", (0.5, 0.8), "1-to-Many on ID+Year\n• cloud_name"),
        ("DimRespondentAITools", (6.5, 4.5), "1-to-Many on ID+Year\n• ai_tool_name"),
        ("DimJobPostings", (6.5, 0.8), "Skill Cross-Ref\n• job_id, salary_range")
    ]
    
    for name, (x, y), desc in dims:
        patch = patches.FancyBboxPatch((x, y), 3.0, 1.6, boxstyle="round,pad=0.2", fc=CARD_COLOR, ec=GRID_COLOR, lw=1.5)
        ax.add_patch(patch)
        ax.text(x + 1.5, y + 1.1, name, ha="center", va="center", fontsize=10, fontweight="bold", color=TEXT_COLOR)
        ax.text(x + 1.5, y + 0.5, desc, ha="center", va="center", fontsize=8, color="#94A3B8")
        
        # Connectors to center Fact
        ax.annotate("", xy=(5.0, 3.5), xytext=(x + 1.5, y + 0.8),
                    arrowprops=dict(arrowstyle="<->", color=ACCENT_GREEN, lw=1.5, ls="--"))

    ax.set_title("DevScope Relational Star Schema Data Model (SQLite / PostgreSQL)", fontsize=14, fontweight="bold", pad=15)
    out_path = SCREENSHOTS_DIR / "data_model.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path.name}")

if __name__ == "__main__":
    generate_dashboard_overview()
    generate_language_distribution()
    generate_salary_analysis()
    generate_ai_adoption()
    generate_data_model()
    print("All README screenshot visuals generated successfully in screenshots/!")

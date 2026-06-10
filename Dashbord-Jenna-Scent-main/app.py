import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Penjualan Jenna Scent",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded"
)

from pathlib import Path

@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent
    excel_file = BASE_DIR / "penjualan-jenna.xlsx"

    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()

    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    df = df.dropna(subset=["Tanggal"])

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)

    if "Stok Barang" not in df.columns:
        df["Stok Barang"] = 0
    else:
        df["Stok Barang"] = pd.to_numeric(df["Stok Barang"], errors="coerce").fillna(0).astype(int)

    if "Varian" not in df.columns:
        df["Varian"] = "Tidak Ada Varian"

    if "Aroma" not in df.columns:
        df["Aroma"] = "Tidak Ada Aroma"

    df["Bulan"] = df["Tanggal"].dt.to_period("M").astype(str)
    df["Tahun"] = df["Tanggal"].dt.year.astype(str)
    df["Minggu"] = df["Tanggal"].dt.to_period("W").astype(str)
    return df

df = load_data()

try:
    logo = Image.open("Jenna-Logo.jpeg")
except Exception:
    logo = None

st.sidebar.markdown(
    """
    <div class="brand-box">
        <div class="brand-icon">J</div>
        <div>
            <div class="brand-title">Jenna Scent</div>
            <div class="brand-subtitle">Sales Analytics</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### Pengaturan Dashboard")

tema = st.sidebar.radio(
    "Tema Tampilan",
    ["Light Mode", "Dark Mode"],
    index=0
)

mode_tampilan = st.sidebar.selectbox(
    "Mode Tampilan",
    ["Sidang", "Laporan"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filter Waktu")

mode_waktu = st.sidebar.selectbox(
    "Pilih Periode",
    ["Harian", "Mingguan", "Bulanan", "Tahunan"]
)

if mode_waktu == "Harian":
    tanggal = st.sidebar.date_input("Pilih Tanggal", df["Tanggal"].max().date())
    df_filter = df[df["Tanggal"].dt.date == tanggal]
    label_periode = tanggal.strftime("%d %B %Y")

elif mode_waktu == "Mingguan":
    minggu = st.sidebar.selectbox("Pilih Minggu", sorted(df["Minggu"].unique(), reverse=True))
    df_filter = df[df["Minggu"] == minggu]
    label_periode = f"Minggu {minggu}"

elif mode_waktu == "Bulanan":
    bulan = st.sidebar.selectbox("Pilih Bulan", sorted(df["Bulan"].unique(), reverse=True))
    df_filter = df[df["Bulan"] == bulan]
    label_periode = bulan

else:
    tahun = st.sidebar.selectbox("Pilih Tahun", sorted(df["Tahun"].unique(), reverse=True))
    df_filter = df[df["Tahun"] == tahun]
    label_periode = f"Tahun {tahun}"

st.sidebar.markdown("---")
st.sidebar.markdown("### Filter Varian")

all_varian = sorted(df["Varian"].dropna().unique())
selected_varian = st.sidebar.multiselect(
    "Pilih Varian",
    all_varian,
    default=all_varian
)

df_filter = df_filter[df_filter["Varian"].isin(selected_varian)]

if df_filter.empty:
    st.warning("Tidak ada data pada filter yang dipilih.")
    st.stop()

if tema == "Dark Mode":
    app_bg = "#0f172a"
    sidebar_bg = "#111827"
    card_bg = "#1e293b"
    text_color = "#f8fafc"
    muted_color = "#cbd5e1"
    border_color = "rgba(255,255,255,0.09)"
    hero_gradient = "linear-gradient(135deg, #020617 0%, #111827 48%, #92400e 100%)"
    plot_template = "plotly_dark"
else:
    app_bg = "#f7f9fb"
    sidebar_bg = "#ffffff"
    card_bg = "#ffffff"
    text_color = "#191c1e"
    muted_color = "#6b7280"
    border_color = "rgba(15,23,42,0.08)"
    hero_gradient = "linear-gradient(135deg, #131b2e 0%, #1f2937 50%, #d97706 100%)"
    plot_template = "plotly_white"

gold = "#d97706"
gold_soft = "#fbbf24"
navy = "#131b2e"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Serif:wght@500;600;700&display=swap');

    .stApp {{
        background: {app_bg};
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}

    section[data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}

    .block-container {{
        max-width: 1320px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    .brand-box {{
        display:flex;
        align-items:center;
        gap:12px;
        padding: 12px 4px 24px 4px;
    }}

    .brand-icon {{
        width:42px;
        height:42px;
        border-radius:50%;
        background: linear-gradient(135deg, #f59e0b, #ffedd5);
        color:#1f2937;
        display:flex;
        align-items:center;
        justify-content:center;
        font-family:'Noto Serif', serif;
        font-size:24px;
        font-weight:700;
        box-shadow: 0 10px 22px rgba(217,119,6,0.25);
    }}

    .brand-title {{
        font-family:'Noto Serif', serif;
        font-size:19px;
        font-weight:700;
        letter-spacing:0.12em;
        text-transform:uppercase;
        color:{text_color};
    }}

    .brand-subtitle {{
        color:{muted_color};
        font-size:12px;
        text-transform:uppercase;
        letter-spacing:0.12em;
    }}

    .hero {{
        background: {hero_gradient};
        border-radius: 28px;
        padding: 34px 40px;
        min-height: 235px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 55px rgba(15,23,42,0.22);
        margin-bottom: 24px;
    }}

    .hero::before {{
        content:"";
        position:absolute;
        right:-80px;
        top:-100px;
        width:330px;
        height:330px;
        background:rgba(255,255,255,0.09);
        border-radius:50%;
    }}

    .hero-label {{
        display:inline-flex;
        padding:7px 14px;
        border-radius:999px;
        background:rgba(255,255,255,0.13);
        border:1px solid rgba(255,255,255,0.18);
        font-size:12px;
        letter-spacing:0.08em;
        text-transform:uppercase;
        font-weight:700;
        margin-bottom:16px;
    }}

    .hero-title {{
        font-family:'Noto Serif', serif;
        font-size:46px;
        font-weight:700;
        line-height:1.12;
        margin:0 0 12px 0;
        letter-spacing:-0.02em;
    }}

    .hero-desc {{
        max-width:760px;
        color:rgba(255,255,255,0.82);
        line-height:1.7;
        font-size:16px;
        margin:0;
    }}

    .hero-logo-card {{
        background:{card_bg};
        border:1px solid {border_color};
        border-radius:24px;
        padding:25px;
        min-height:235px;
        display:flex;
        align-items:center;
        justify-content:center;
        box-shadow: 0 14px 34px rgba(15,23,42,0.08);
    }}

    .section-title {{
        font-family:'Noto Serif', serif;
        font-size:28px;
        font-weight:700;
        color:{text_color};
        margin:18px 0 4px 0;
    }}

    .section-subtitle {{
        color:{muted_color};
        font-size:14px;
        margin-bottom:14px;
    }}

    .kpi-card {{
        background:{card_bg};
        border:1px solid {border_color};
        border-radius:22px;
        padding:22px;
        min-height:150px;
        box-shadow:0 12px 30px rgba(15,23,42,0.08);
        transition: all .25s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow:0 18px 38px rgba(15,23,42,0.13);
    }}

    .kpi-top {{
        display:flex;
        justify-content:space-between;
        align-items:flex-start;
        gap:12px;
    }}

    .kpi-title {{
        color:{muted_color};
        font-size:12px;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:0.08em;
    }}

    .kpi-icon {{
        width:36px;
        height:36px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#ffedd5;
        color:#9a3412;
        font-size:18px;
    }}

    .kpi-value {{
        font-size:34px;
        font-weight:800;
        color:{text_color};
        margin-top:20px;
        line-height:1;
    }}

    .kpi-note {{
        color:{muted_color};
        font-size:13px;
        margin-top:8px;
    }}

    .insight-card {{
        background:{card_bg};
        border:1px solid {border_color};
        border-left:5px solid {gold};
        border-radius:22px;
        padding:24px 26px;
        margin: 18px 0;
        box-shadow:0 12px 30px rgba(15,23,42,0.08);
    }}

    .insight-title {{
        font-family:'Noto Serif', serif;
        font-size:24px;
        font-weight:700;
        color:{text_color};
        margin-bottom:8px;
    }}

    .insight-text {{
        color:{muted_color};
        line-height:1.7;
        font-size:15px;
        max-width:980px;
    }}

    .chart-card {{
        background:{card_bg};
        border:1px solid {border_color};
        border-radius:24px;
        padding:20px;
        box-shadow:0 12px 30px rgba(15,23,42,0.08);
        margin-bottom:18px;
    }}

    .chart-title {{
        font-size:13px;
        color:{muted_color};
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.08em;
        margin-bottom:10px;
    }}

    .footer {{
        text-align:center;
        color:{muted_color};
        font-size:13px;
        margin-top:30px;
        padding:16px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def format_number(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except Exception:
        return str(value)

def plot_style(fig, height=410):
    fig.update_layout(
        template=plot_template,
        height=height,
        margin=dict(l=24, r=24, t=30, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=13),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.18)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.18)")
    return fig

total_terjual = int(df_filter["Quantity"].sum())
jumlah_varian = int(df_filter["Varian"].nunique())
jumlah_aroma = int(df_filter["Aroma"].nunique())
total_stok = int(df_filter["Stok Barang"].sum())
total_transaksi = len(df_filter)

varian_total = (
    df_filter.groupby("Varian", as_index=False)["Quantity"]
    .sum()
    .sort_values("Quantity", ascending=False)
)

produk_terlaris = "-"
produk_qty = 0
if not varian_total.empty:
    produk_terlaris = varian_total.iloc[0]["Varian"]
    produk_qty = int(varian_total.iloc[0]["Quantity"])

hero_col, logo_col = st.columns([0.76, 0.24])

with hero_col:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-label">Jenna Scent Sales Analytics</div>
            <h1 class="hero-title">Dashboard Monitoring Penjualan</h1>
            <p class="hero-desc">
                Pantau performa penjualan parfum berdasarkan periode terpilih.
                Dashboard ini menyajikan ringkasan penjualan, stok, transaksi,
                varian terlaris, distribusi produk, dan tren penjualan secara visual.
            </p>
            <div class="hero-label" style="margin-top:20px; margin-bottom:0;">
                {mode_waktu} • {label_periode}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with logo_col:
    st.markdown('<div class="hero-logo-card">', unsafe_allow_html=True)
    if logo is not None:
        st.image(logo, use_container_width=True)
    else:
        st.markdown("<h2>Jenna<br>Scent</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h2 class="section-title">Ringkasan Utama</h2>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Indikator performa berdasarkan filter yang sedang aktif.</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

kpi_items = [
    ("Total Terjual", format_number(total_terjual), "Qty produk", "🛍️"),
    ("Jumlah Varian", format_number(jumlah_varian), "Varian aktif", "🏷️"),
    ("Jumlah Aroma", format_number(jumlah_aroma), "Kategori aroma", "🌬️"),
    ("Total Stok", format_number(total_stok), "Unit tersedia", "📦"),
    ("Total Transaksi", format_number(total_transaksi), "Transaksi", "🧾"),
]

for col, item in zip([k1, k2, k3, k4, k5], kpi_items):
    title, value, note, icon = item
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <div class="kpi-title">{title}</div>
                    <div class="kpi-icon">{icon}</div>
                </div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    f"""
    <div class="insight-card">
        <div class="insight-title">💡 Insight Performa</div>
        <div class="insight-text">
            Pada periode <b>{label_periode}</b>, total produk terjual sebanyak
            <b>{format_number(total_terjual)}</b> unit dari <b>{format_number(total_transaksi)}</b> transaksi.
            Varian dengan performa terbaik adalah <b>{produk_terlaris}</b>
            dengan total penjualan <b>{format_number(produk_qty)}</b> unit.
            Informasi ini dapat digunakan untuk evaluasi stok, strategi promosi,
            dan pemantauan penjualan Jenna Scent.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<h2 class="section-title">Analisis Penjualan</h2>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Visualisasi penjualan berdasarkan varian, aroma, dan tanggal transaksi.</div>', unsafe_allow_html=True)

chart_left, chart_right = st.columns([0.60, 0.40])

with chart_left:
    st.markdown('<div class="chart-card"><div class="chart-title">Total Penjualan per Varian</div>', unsafe_allow_html=True)

    fig_bar = px.bar(
        varian_total,
        x="Varian",
        y="Quantity",
        text="Quantity",
        color="Quantity",
        color_continuous_scale=["#fff7ed", "#f59e0b", "#7c2d12"]
    )
    fig_bar.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Total terjual: %{y} unit<extra></extra>"
    )
    fig_bar.update_layout(
        xaxis_title="Varian",
        yaxis_title="Quantity",
        coloraxis_showscale=False
    )
    st.plotly_chart(plot_style(fig_bar, 430), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with chart_right:
    st.markdown('<div class="chart-card"><div class="chart-title">Distribusi Penjualan Varian</div>', unsafe_allow_html=True)

    fig_pie = px.pie(
        varian_total,
        names="Varian",
        values="Quantity",
        hole=0.58,
        color_discrete_sequence=["#131b2e", "#d97706", "#fbbf24", "#64748b", "#94a3b8", "#0f766e"]
    )
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>%{value} unit<br>%{percent}<extra></extra>"
    )
    st.plotly_chart(plot_style(fig_pie, 430), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

trend_col, aroma_col = st.columns([0.58, 0.42])

with trend_col:
    st.markdown('<div class="chart-card"><div class="chart-title">Tren Penjualan Berdasarkan Tanggal</div>', unsafe_allow_html=True)

    trend = (
        df_filter.groupby("Tanggal", as_index=False)["Quantity"]
        .sum()
        .sort_values("Tanggal")
    )

    fig_line = px.line(
        trend,
        x="Tanggal",
        y="Quantity",
        markers=True
    )
    fig_line.update_traces(
        line=dict(width=4, color=gold),
        marker=dict(size=9, color=navy, line=dict(width=2, color=gold_soft)),
        fill="tozeroy",
        fillcolor="rgba(217,119,6,0.12)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Terjual: %{y} unit<extra></extra>"
    )
    fig_line.update_layout(
        xaxis_title="Tanggal",
        yaxis_title="Quantity"
    )
    st.plotly_chart(plot_style(fig_line, 380), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with aroma_col:
    st.markdown('<div class="chart-card"><div class="chart-title">Penjualan Berdasarkan Aroma</div>', unsafe_allow_html=True)

    aroma_total = (
        df_filter.groupby("Aroma", as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=True)
    )

    fig_aroma = px.bar(
        aroma_total,
        x="Quantity",
        y="Aroma",
        orientation="h",
        text="Quantity",
        color="Quantity",
        color_continuous_scale=["#e0f2fe", "#38bdf8", "#0f172a"]
    )
    fig_aroma.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total terjual: %{x} unit<extra></extra>"
    )
    fig_aroma.update_layout(
        xaxis_title="Quantity",
        yaxis_title="Aroma",
        coloraxis_showscale=False
    )
    st.plotly_chart(plot_style(fig_aroma, 380), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h2 class="section-title">Ranking Varian Terlaris</h2>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Urutan varian parfum berdasarkan jumlah produk terjual.</div>', unsafe_allow_html=True)

ranking = varian_total.copy()
ranking.insert(0, "Peringkat", range(1, len(ranking) + 1))

aroma_map = df_filter.groupby("Varian")["Aroma"].first().reset_index()
ranking = ranking.merge(aroma_map, on="Varian", how="left")

stok_map = df_filter.groupby("Varian")["Stok Barang"].sum().reset_index()
ranking = ranking.merge(stok_map, on="Varian", how="left")

st.dataframe(ranking, use_container_width=True, hide_index=True)

if mode_tampilan == "Laporan":
    st.markdown('<h2 class="section-title">Data Detail Penjualan</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Data transaksi sesuai filter yang dipilih pada sidebar.</div>', unsafe_allow_html=True)

    df_tampil = df_filter.copy()
    df_tampil["Tanggal"] = df_tampil["Tanggal"].dt.strftime("%d %B %Y")

    st.dataframe(df_tampil, use_container_width=True, hide_index=True)

st.markdown(
    """
    <div class="footer">
        Dashboard Penjualan Jenna Scent • Sistem Monitoring Penjualan Berbasis Visualisasi Interaktif
    </div>
    """,
    unsafe_allow_html=True
)

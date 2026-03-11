import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from tkinter import filedialog, Tk

# =================================================================
# 1. HYPERPARAMETER CONFIGURATION
# =================================================================
CONFIG = {
    "FLOOR_MODEL_RANGE": (-4.0, 4.0),   
    "DISCARD_LIMIT": -10.0,            
    "TIRE_START_THR": 5.0,             # 타이어 물체가 시작/끝남을 판단하는 높이 기준 (바닥 제외)
    "ABS_THR_TD": 0.55, 
    "MIN_DROP_TD": 3.0, 
    "ABS_THR_BEAD": 1.2, 
    "SMOOTHING_KERNEL": 11, 
    "GRADIENT_WINDOW": 5
}

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =================================================================
# 2. HELPER FUNCTIONS
# =================================================================
def extract_profile_data(filename):
    try:
        df = pd.read_csv(filename, header=None, on_bad_lines='skip')
        if df.shape[1] >= 5:
            col4 = pd.to_numeric(df[4], errors='coerce')
            numbers = col4[col4 != -999.999].dropna().values
            if len(numbers) > 100: return numbers.astype(float)
        return None
    except: return None

def draw_v_arrow(ax, x, y1, y2, text, color='red', text_loc=0.5):
    ax.annotate('', xy=(x, y1), xytext=(x, y2), arrowprops=dict(arrowstyle='<->', color=color, lw=1.2))
    pos_y = y1 + (y2 - y1) * text_loc
    ax.text(x, pos_y, text, color=color, ha='center', va='center', fontsize=7, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.7))

# =================================================================
# 3. CORE ANALYSIS FUNCTION
# =================================================================
def analyze_tire_full(filename, ax, config):
    raw_y_src = extract_profile_data(filename)
    if raw_y_src is None: return None
    
    data_len = len(raw_y_src); x_idx = np.arange(data_len)

    # [1] 바닥 보정 (Center Floor 기준 수평 맞춤)
    mask = (raw_y_src >= config["FLOOR_MODEL_RANGE"][0]) & (raw_y_src <= config["FLOOR_MODEL_RANGE"][1])
    if np.sum(mask) > 50:
        slope, intercept = np.polyfit(x_idx[mask], raw_y_src[mask], 1)
        theta = np.arctan(slope)
        cos_t, sin_t = np.cos(-theta), np.sin(-theta)
        y_centered = raw_y_src - intercept
        y_rot = x_idx * sin_t + y_centered * cos_t
        x_rot = x_idx * cos_t - y_centered * sin_t
        y_leveled = np.interp(x_idx, x_rot, y_rot, left=np.nan, right=np.nan)
    else:
        y_leveled = raw_y_src.copy()

    # [2] 데이터 필터링 및 보간 (오차 해결의 핵심 부분: limit_area='inside')
    y_filtered = np.where(y_leveled < config["DISCARD_LIMIT"], np.nan, y_leveled)
    # inside 옵션은 타이어 바깥쪽 허공을 채우지 않고 순수 물체 내부의 끊김만 보간합니다.
    y_interp = pd.Series(y_filtered).interpolate(limit_area='inside').fillna(0).values
    processed_y = np.convolve(y_interp, np.ones(config["SMOOTHING_KERNEL"])/config["SMOOTHING_KERNEL"], mode='same')

    # [3] 특징점 탐색
    mid = data_len // 2
    l_p = np.argmax(processed_y[:mid]); r_p = mid + np.argmax(processed_y[mid:])
    dy = np.gradient(processed_y)
    dy_s = np.convolve(dy, np.ones(config["GRADIENT_WINDOW"])/config["GRADIENT_WINDOW"], mode='same')

    def find_cliff(p_idx, target, thr, min_d):
        step = 1 if p_idx < target else -1
        curr = p_idx
        while curr != target:
            if abs(processed_y[p_idx] - processed_y[curr]) > min_d:
                if abs(dy_s[curr]) > thr: return curr
            curr += step
        return p_idx

    td_l = find_cliff(l_p, 0, config["ABS_THR_TD"], config["MIN_DROP_TD"])
    td_r = find_cliff(r_p, data_len-1, config["ABS_THR_TD"], config["MIN_DROP_TD"])
    bead_l = find_cliff(l_p, mid, config["ABS_THR_BEAD"], 5.0)
    bead_r = find_cliff(r_p, mid, config["ABS_THR_BEAD"], 5.0)

    # [4] OD & ID 측정 (바닥 구간 제외하고 타이어 물체 끝단만 잡기)
    try:
        # OD: 외곽 노이즈를 피하기 위해 타이어 양쪽 최고점(l_p, r_p)에서 바깥쪽으로 탐색
        out_l = l_p
        while out_l > 0 and processed_y[out_l] >= config["TIRE_START_THR"]:
            out_l -= 1
            
        out_r = r_p
        while out_r < data_len - 1 and processed_y[out_r] >= config["TIRE_START_THR"]:
            out_r += 1
            
        val_od = out_r - out_l
        
        # ID: 두 덩어리 사이 내측 간격 (0점에 가까운 구간)
        temp_in_l = np.where(processed_y[l_p:mid] < config["TIRE_START_THR"])[0]
        in_l = l_p + temp_in_l[0] if len(temp_in_l) > 0 else mid
        
        temp_in_r = np.where(processed_y[mid:r_p] < config["TIRE_START_THR"])[0]
        in_r = mid + temp_in_r[-1] if len(temp_in_r) > 0 else mid
        
        val_id = in_r - in_l
    except Exception as e:
        val_od, val_id, out_l, out_r, in_l, in_r = 0, 0, 0, 0, mid, mid

    res = {
        "File": os.path.basename(filename), 
        "OD": val_od, "ID": val_id,
        "L_SW": processed_y[l_p], "R_SW": processed_y[r_p],
        "L_TD_H": processed_y[td_l], "R_TD_H": processed_y[td_r],
        "L_Bead_H": processed_y[bead_l], "R_Bead_H": processed_y[bead_r]
    }

    # [5] 시각화
    ax.scatter(x_idx, y_leveled, color='gray', s=0.2, alpha=0.2)
    ax.plot(x_idx, y_filtered, color='b', lw=0.8, alpha=0.7)
    ax.axhline(0, color='black', lw=1.0, ls='--')
    
    ymax_disp = np.nanmax(y_filtered) if not np.all(np.isnan(y_filtered)) else 100
    ax.set_ylim(-20, ymax_disp * 1.3)

    if val_od > 0:
        # OD 치수선 (빨간색, 상단)
        ax.annotate('', xy=(out_l, ymax_disp+5), xytext=(out_r, ymax_disp+5), arrowprops=dict(arrowstyle='<->', color='red'))
        ax.text((out_l+out_r)/2, ymax_disp+10, f'OD:{val_od}', color='red', ha='center', fontweight='bold', fontsize=8)
    if val_id > 0:
        # ID 치수선 (빨간색, 하단)
        ax.annotate('', xy=(in_l, 15), xytext=(in_r, 15), arrowprops=dict(arrowstyle='<->', color='red'))
        ax.text((in_l+in_r)/2, 22, f'ID:{val_id}', color='red', ha='center', fontweight='bold', fontsize=8)

    draw_v_arrow(ax, l_p, 0, res["L_SW"], f'LSW:{res["L_SW"]:.1f}', text_loc=0.8)
    draw_v_arrow(ax, r_p, 0, res["R_SW"], f'RSW:{res["R_SW"]:.1f}', text_loc=0.8)
    draw_v_arrow(ax, td_l, 0, res["L_TD_H"], f'LTD:{res["L_TD_H"]:.1f}', text_loc=0.5)
    draw_v_arrow(ax, td_r, 0, res["R_TD_H"], f'RTD:{res["R_TD_H"]:.1f}', text_loc=0.5)

    ax.set_title(res["File"], fontsize=8); ax.axis('off')
    return res

# =================================================================
# 4. MAIN PROCESS & STATISTICS
# =================================================================
def main():
    root = Tk(); root.withdraw()
    files = filedialog.askopenfilenames(title="분석할 타이어 CSV들을 선택하세요")
    if not files: return
    files = sorted(files); num = len(files)
    
    cols = 3
    rows = (num + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4.5 * rows))
    axes = np.atleast_1d(axes).flatten()
    
    results = []
    for i, f in enumerate(files):
        res = analyze_tire_full(f, axes[i], CONFIG)
        if res: results.append(res)
    for j in range(num, len(axes)): axes[j].set_visible(False)
    plt.tight_layout(); plt.show()
    
    if results:
        df = pd.DataFrame(results)
        print("\n" + "="*110)
        print(" [반복 측정 정밀도 통계 분석 리포트 - 좌/우 통합 분석]")
        print(" (OD: 타이어 물체 전체 폭 | ID: 내측 간격 | 모든 치수선: RED)")
        print("="*110)
        
        for metric in ['OD', 'ID']:
            avg = df[metric].mean()
            diff = df[metric].max() - df[metric].min()
            print(f" {metric:18} 평균: {avg:8.2f} | 최대 편차(Max-Min): {diff:8.2f}")
        
        groups = {
            "Sidewall (L+R)": ["L_SW", "R_SW"],
            "Tread_H (L+R)": ["L_TD_H", "R_TD_H"],
            "Bead_H (L+R)": ["L_Bead_H", "R_Bead_H"]
        }
        
        for name, cols in groups.items():
            combined = pd.concat([df[cols[0]], df[cols[1]]])
            avg = combined.mean()
            diff = combined.max() - combined.min()
            print(f" {name:18} 평균: {avg:8.2f} | 최대 편차(Max-Min): {diff:8.2f}")
            
        print("-" * 110)
        detail_cols = ['File', 'OD', 'ID', 'L_SW', 'R_SW', 'L_TD_H', 'R_TD_H', 'L_Bead_H', 'R_Bead_H']
        print(df[detail_cols].to_string(index=False))
        print("="*110)

if __name__ == "__main__":
    main()
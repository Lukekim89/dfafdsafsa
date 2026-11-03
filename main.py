import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math

# 페이지 설정
st.set_page_config(
    page_title="고등학교 과학 공식 모음",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터베이스 정의 (70+ 공식)
FORMULAS_DB = [
    # ---------------- 통합과학 ----------------
    {
        "id": "sc1_vel", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "역학",
        "name": "평균 속도", "latex": r"v = \frac{\Delta s}{\Delta t}",
        "desc": "변위를 걸린 시간으로 나눈 값으로, 운동의 방향과 빠르기를 나타냅니다.",
        "vars": [("v", "평균 속도", "m/s"), ("Δs", "변위", "m"), ("Δt", "걸린 시간", "s")],
        "calc_type": "v_calc", "inputs": [("ds", "변위 Δs (m)", 10.0), ("dt", "시간 Δt (s)", 2.0)]
    },
    {
        "id": "sc1_p", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "역학",
        "name": "운동량", "latex": r"p = m \cdot v",
        "desc": "운동하는 물체의 운동 효과 크기를 나타내는 물리량입니다.",
        "vars": [("p", "운동량", "kg·m/s"), ("m", "질량", "kg"), ("v", "속도", "m/s")],
        "calc_type": "p_calc", "inputs": [("m", "질량 m (kg)", 5.0), ("v", "속도 v (m/s)", 10.0)]
    },
    {
        "id": "sc1_I", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "역학",
        "name": "충격량", "latex": r"I = F \cdot \Delta t = \Delta p",
        "desc": "물체에 가해진 힘과 작용 시간의 곱으로, 운동량의 변화량과 같습니다.",
        "vars": [("I", "충격량", "N·s"), ("F", "힘", "N"), ("Δt", "시간", "s")],
        "calc_type": "I_calc", "inputs": [("f", "힘 F (N)", 20.0), ("dt", "시간 Δt (s)", 0.5)]
    },
    {
        "id": "sc1_ep", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "역학",
        "name": "중력 위치 에너지", "latex": r"E_p = m \cdot g \cdot h",
        "desc": "기준면으로부터 높이 h에 위치한 물체가 중력에 의해 가지는 에너지입니다.",
        "vars": [("E_p", "위치 에너지", "J"), ("m", "질량", "kg"), ("g", "중력가속도", "9.8 m/s²"), ("h", "높이", "m")],
        "calc_type": "ep_calc", "inputs": [("m", "질량 m (kg)", 2.0), ("h", "높이 h (m)", 5.0)]
    },
    {
        "id": "sc1_ek", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "역학",
        "name": "운동 에너지", "latex": r"E_k = \frac{1}{2} m v^2",
        "desc": "속도 v로 운동하는 질량 m인 물체가 가지는 에너지입니다.",
        "vars": [("E_k", "운동 에너지", "J"), ("m", "질량", "kg"), ("v", "속도", "m/s")],
        "calc_type": "ek_calc", "inputs": [("m", "질량 m (kg)", 2.0), ("v", "속도 v (m/s)", 4.0)]
    },
    {
        "id": "sc1_ohm", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "전자기",
        "name": "옴의 법칙", "latex": r"V = I \cdot R",
        "desc": "회로에 흐르는 전류는 전압에 비례하고 저항에 반비례합니다.",
        "vars": [("V", "전압", "V"), ("I", "전류", "A"), ("R", "저항", "Ω")],
        "calc_type": "ohm_calc", "inputs": [("i", "전류 I (A)", 2.0), ("r", "저항 R (Ω)", 5.0)]
    },
    {
        "id": "sc1_power", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "전자기",
        "name": "소비 전력", "latex": r"P = V \cdot I = I^2 R = \frac{V^2}{R}",
        "desc": "전기 기구가 1초 동안 소비하는 전기 에너지를 의미합니다.",
        "vars": [("P", "전력", "W"), ("V", "전압", "V"), ("I", "전류", "A")],
        "calc_type": "power_calc", "inputs": [("v", "전압 V (V)", 220.0), ("i", "전류 I (A)", 2.0)]
    },
    {
        "id": "sc1_ploss", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "전자기",
        "name": "송전선 손실 전력", "latex": r"P_{\text{loss}} = I^2 \cdot R",
        "desc": "송전선의 저항 R과 송전 전류 I에 의해 열로 손실되는 전력입니다.",
        "vars": [("P_loss", "손실 전력", "W"), ("I", "송전 전류", "A"), ("R", "송전선 저항", "Ω")],
        "calc_type": "ploss_calc", "inputs": [("i", "송전 전류 I (A)", 10.0), ("r", "저항 R (Ω)", 4.0)]
    },
    {
        "id": "sc1_transformer", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "전자기",
        "name": "변압기 감은수와 전압 비", "latex": r"\frac{V_1}{V_2} = \frac{N_1}{N_2} = \frac{I_2}{I_1}",
        "desc": "변압기의 1차, 2차 코일 감은수 비율과 전압 및 전류의 관계입니다.",
        "vars": [("V", "전압", "V"), ("N", "감은 수", "회"), ("I", "전류", "A")],
        "calc_type": "trans_calc", "inputs": [("v1", "1차 전압 V1 (V)", 220.0), ("n1", "1차 감은수 N1", 1000.0), ("n2", "2차 감은수 N2", 100.0)]
    },
    {
        "id": "sc1_mole", "grade": "고등학교 1학년", "subject": "통합과학 1·2", "category": "화학",
        "name": "몰수(n) 구하기", "latex": r"n = \frac{m}{M} = \frac{N}{6.02 \times 10^{23}}",
        "desc": "물질의 양(몰수)은 질량을 화학식량(몰질량)으로 나눈 값입니다.",
        "vars": [("n", "몰수", "mol"), ("m", "질량", "g"), ("M", "몰질량", "g/mol")],
        "calc_type": "mole_calc", "inputs": [("m", "질량 m (g)", 36.0), ("m_w", "몰질량 M (g/mol)", 18.0)]
    },

    # ---------------- 물리학Ⅰ ----------------
    {
        "id": "phy1_fma", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "역학",
        "name": "운동 방정식 (뉴턴 제2법칙)", "latex": r"F = m \cdot a",
        "desc": "물체에 가해진 알짜힘 F는 질량 m과 가속도 a의 곱과 같습니다.",
        "vars": [("F", "알짜힘", "N"), ("m", "질량", "kg"), ("a", "가속도", "m/s²")],
        "calc_type": "fma_calc", "inputs": [("m", "질량 m (kg)", 10.0), ("a", "가속도 a (m/s²)", 2.5)]
    },
    {
        "id": "phy1_v", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "역학",
        "name": "등가속도 속도 공식", "latex": r"v = v_0 + a \cdot t",
        "desc": "등가속도 직선 운동을 하는 물체의 시간 t 후 나중 속도입니다.",
        "vars": [("v", "나중 속도", "m/s"), ("v₀", "초기 속도", "m/s"), ("a", "가속도", "m/s²"), ("t", "시간", "s")],
        "calc_type": "v_t_calc", "inputs": [("v0", "초기속도 v0 (m/s)", 0.0), ("a", "가속도 a (m/s²)", 3.0), ("t", "시간 t (s)", 4.0)]
    },
    {
        "id": "phy1_s", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "역학",
        "name": "등가속도 변위 공식", "latex": r"s = v_0 t + \frac{1}{2} a t^2",
        "desc": "등가속도 운동하는 물체가 시간 t 동안 이동한 변위입니다.",
        "vars": [("s", "변위", "m"), ("v0", "초기속도", "m/s"), ("a", "가속도", "m/s²"), ("t", "시간", "s")],
        "calc_type": "s_t_calc", "inputs": [("v0", "초기속도 v0 (m/s)", 0.0), ("a", "가속도 a (m/s²)", 2.0), ("t", "시간 t (s)", 5.0)]
    },
    {
        "id": "phy1_2as", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "역학",
        "name": "등가속도 시간 제거 공식", "latex": r"2as = v^2 - v_0^2",
        "desc": "시간 t를 모를 때 초기속도, 나중속도, 가속도, 변위의 관계식입니다.",
        "vars": [("a", "가속도", "m/s²"), ("s", "변위", "m"), ("v", "나중속도", "m/s"), ("v0", "초기속도", "m/s")],
        "calc_type": "2as_calc", "inputs": [("v", "나중속도 v (m/s)", 10.0), ("v0", "초기속도 v0 (m/s)", 0.0), ("a", "가속도 a (m/s²)", 2.0)]
    },
    {
        "id": "phy1_thermo1", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "열역학",
        "name": "열역학 제1법칙", "latex": r"Q = \Delta U + W",
        "desc": "기체에 가한 열량 Q는 내부에너지 변화량 ΔU와 외부에 한 일 W의 합입니다.",
        "vars": [("Q", "열량", "J"), ("ΔU", "내부에너지 변화", "J"), ("W", "한 일", "J")],
        "calc_type": "thermo1_calc", "inputs": [("du", "내부에너지 변화 ΔU (J)", 150.0), ("w", "한 일 W (J)", 50.0)]
    },
    {
        "id": "phy1_efficiency", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "열역학",
        "name": "열기관의 열효율", "latex": r"e = \frac{W}{Q_{in}} = \frac{Q_{in} - Q_{out}}{Q_{in}} = 1 - \frac{Q_{out}}{Q_{in}}",
        "desc": "공급된 열량 대비 한 일의 비율로 표현되는 열기관의 효율입니다.",
        "vars": [("e", "열효율", "-"), ("Qin", "공급 열량", "J"), ("Qout", "방출 열량", "J"), ("W", "한 일", "J")],
        "calc_type": "eff_calc", "inputs": [("qin", "공급 열량 Q_in (J)", 500.0), ("qout", "방출 열량 Q_out (J)", 300.0)]
    },
    {
        "id": "phy1_snell", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "파동",
        "name": "굴절의 법칙 (스넬의 법칙)", "latex": r"n_1 \sin \theta_1 = n_2 \sin \theta_2",
        "desc": "서로 다른 매질 경계면에서 빛이 굴절할 때의 굴절률과 각도의 관계입니다.",
        "vars": [("n1", "매질1 굴절률", "-"), ("θ1", "입사각", "°"), ("n2", "매질2 굴절률", "-"), ("θ2", "굴절각", "°")],
        "calc_type": "snell_calc", "inputs": [("n1", "매질1 굴절률 n1", 1.0), ("theta1", "입사각 θ1 (도)", 30.0), ("n2", "매질2 굴절률 n2", 1.5)]
    },
    {
        "id": "phy1_debroglie", "grade": "고등학교 2학년", "subject": "물리학Ⅰ", "category": "현대물리",
        "name": "드브로이 물질파 파장", "latex": r"\lambda = \frac{h}{p} = \frac{h}{m \cdot v}",
        "desc": "질량 m과 속도 v로 운동하는 입자가 가지는 파동 파장입니다.",
        "vars": [("λ", "물질파 파장", "m"), ("h", "플랑크 상수", "6.63×10⁻³⁴ J·s"), ("p", "운동량", "kg·m/s")],
        "calc_type": "debroglie_calc", "inputs": [("m", "질량 m (kg)", 9.11e-31), ("v", "속도 v (m/s)", 1.0e6)]
    },

    # ---------------- 화학Ⅰ ----------------
    {
        "id": "ch1_molarity", "grade": "고등학교 2학년", "subject": "화학Ⅰ", "category": "용액",
        "name": "몰농도 (Molarity)", "latex": r"M = \frac{n \text{ (mol)}}{V \text{ (L)}}",
        "desc": "용액 1L 속에 용해되어 있는 용질의 몰수입니다.",
        "vars": [("M", "몰농도", "M (mol/L)"), ("n", "용질 몰수", "mol"), ("V", "용액 부피", "L")],
        "calc_type": "molarity_calc", "inputs": [("n", "용질 몰수 n (mol)", 0.5), ("v", "용액 부피 V (L)", 2.0)]
    },
    {
        "id": "ch1_molality", "grade": "고등학교 2학년", "subject": "화학Ⅰ", "category": "용액",
        "name": "몰랄농도 (Molality)", "latex": r"m = \frac{n \text{ (mol)}}{W_{\text{solvent}} \text{ (kg)}}",
        "desc": "용매 1kg 속에 녹아 있는 용질의 몰수입니다.",
        "vars": [("m", "몰랄농도", "m (mol/kg)"), ("n", "용질 몰수", "mol"), ("W", "용매 질량", "kg")],
        "calc_type": "molality_calc", "inputs": [("n", "용질 몰수 n (mol)", 0.2), ("w", "용매 질량 W (kg)", 0.5)]
    },
    {
        "id": "ch1_ph", "grade": "고등학교 2학년", "subject": "화학Ⅰ", "category": "수용액 반응",
        "name": "pH 및 pOH 관계식", "latex": r"\text{pH} = -\log_{10}[\text{H}^+], \quad \text{pH} + \text{pOH} = 14",
        "desc": "수용액 속 수소 이온 농도 [H+]로부터 pH를 계산합니다.",
        "vars": [("pH", "수소 이온 지수", "-"), ("[H+]", "수소 이온 농도", "M"), ("pOH", "수산화 이온 지수", "-")],
        "calc_type": "ph_calc", "inputs": [("h_conc", "수소 이온 농도 [H+] (M)", 1.0e-3)]
    },
    {
        "id": "ch1_neutralization", "grade": "고등학교 2학년", "subject": "화학Ⅰ", "category": "수용액 반응",
        "name": "산-염기 중화 적정", "latex": r"n \cdot M \cdot V = n' \cdot M' \cdot V'",
        "desc": "완전 중화 반응 시 산의 H+ 몰수와 염기의 OH- 몰수는 같습니다.",
        "vars": [("n, n'", "산/염기 가수", "-"), ("M, M'", "산/염기 몰농도", "M"), ("V, V'", "산/염기 부피", "mL")],
        "calc_type": "neutral_calc", "inputs": [("n1", "산 가수 n1", 1.0), ("m1", "산 몰농도 M1 (M)", 0.1), ("v1", "산 부피 V1 (mL)", 20.0), ("n2", "염기 가수 n2", 1.0), ("v2", "염기 부피 V2 (mL)", 10.0)]
    },
    {
        "id": "ch1_heat", "grade": "고등학교 2학년", "subject": "화학Ⅰ", "category": "열화학",
        "name": "반응 열량 계산", "latex": r"Q = c \cdot m \cdot \Delta T",
        "desc": "물질의 비열 c, 질량 m, 온도 변화량 ΔT로 전달된 열량을 구합니다.",
        "vars": [("Q", "열량", "J"), ("c", "비열", "J/(g·°C)"), ("m", "질량", "g"), ("ΔT", "온도 변화", "°C")],
        "calc_type": "heat_calc", "inputs": [("c", "비열 c (J/g·°C)", 4.18), ("m", "질량 m (g)", 100.0), ("dt", "온도변화 ΔT (°C)", 10.0)]
    },

    # ---------------- 생명과학Ⅰ ----------------
    {
        "id": "bio1_hw", "grade": "고등학교 2학년", "subject": "생명과학Ⅰ", "category": "유전",
        "name": "하디-바인베르크 평형 법칙", "latex": r"p + q = 1, \quad p^2 + 2pq + q^2 = 1",
        "desc": "이상 집단에서 유전자형 빈도와 대립유전자 빈도의 관계입니다.",
        "vars": [("p", "우성 유전자 빈도", "-"), ("q", "열성 유전자 빈도", "-"), ("2pq", "이형접합자 빈도", "-")],
        "calc_type": "hw_calc", "inputs": [("p", "우성 대립유전자 빈도 p (0~1)", 0.7)]
    },
    {
        "id": "bio1_conduction", "grade": "고등학교 2학년", "subject": "생명과학Ⅰ", "category": "신경",
        "name": "신경 흥분 전도 속도", "latex": r"v = \frac{d}{t}",
        "desc": "축삭 돌기를 따라 활동 전위가 이동하는 속도를 계산합니다.",
        "vars": [("v", "전도 속도", "cm/ms"), ("d", "거리", "cm"), ("t", "경과 시간", "ms")],
        "calc_type": "conduction_calc", "inputs": [("d", "이동 거리 d (cm)", 6.0), ("t", "걸린 시간 t (ms)", 2.0)]
    },

    # ---------------- 지구과학Ⅰ ----------------
    {
        "id": "ea1_stefan", "grade": "고등학교 2학년", "subject": "지구과학Ⅰ", "category": "천문",
        "name": "슈테판-볼츠만 법칙", "latex": r"E = \sigma \cdot T^4",
        "desc": "흑체가 단위 면적당 단위 시간에 방출하는 에너지는 절대온도 T의 4제곱에 비례합니다.",
        "vars": [("E", "방출 에너지", "W/m²"), ("T", "절대 온도", "K"), ("σ", "상수", "5.67×10⁻⁸")],
        "calc_type": "stefan_calc", "inputs": [("t", "표면 절대온도 T (K)", 6000.0)]
    },
    {
        "id": "ea1_wien", "grade": "고등학교 2학년", "subject": "지구과학Ⅰ", "category": "천문",
        "name": "빈의 변위 법칙", "latex": r"\lambda_{\text{max}} = \frac{A}{T} \quad (A \approx 2.898 \times 10^6 \text{ nm}\cdot\text{K})",
        "desc": "최대 에너지를 방출하는 파장 λmax는 표면 절대온도 T에 반비례합니다.",
        "vars": [("λmax", "최대 파장", "nm"), ("T", "절대 온도", "K")],
        "calc_type": "wien_calc", "inputs": [("t", "절대온도 T (K)", 5800.0)]
    },
    {
        "id": "ea1_doppler", "grade": "고등학교 2학년", "subject": "지구과학Ⅰ", "category": "천문",
        "name": "빛의 도플러 효과 (시선 속도)", "latex": r"v = c \cdot \frac{\Delta \lambda}{\lambda_0}",
        "desc": "천체의 후퇴/접근 운동으로 인한 스펙트럼 변화량으로 시선속도를 산출합니다.",
        "vars": [("v", "시선 속도", "km/s"), ("c", "빛의 속도", "300,000 km/s"), ("Δλ", "파장 변화량", "nm"), ("λ0", "고유 파장", "nm")],
        "calc_type": "doppler_calc", "inputs": [("dlam", "파장 변화량 Δλ (nm)", 0.2), ("lam0", "고유 파장 λ0 (nm)", 500.0)]
    },
    {
        "id": "ea1_hubble", "grade": "고등학교 2학년", "subject": "지구과학Ⅰ", "category": "우주",
        "name": "허블의 법칙", "latex": r"v = H_0 \cdot d",
        "desc": "외부 은하의 후퇴 속도 v는 은하까지의 거리 d에 비례합니다.",
        "vars": [("v", "후퇴 속도", "km/s"), ("H0", "허블 상수", "70 km/s/Mpc"), ("d", "거리", "Mpc")],
        "calc_type": "hubble_calc", "inputs": [("d", "거리 d (Mpc)", 50.0)]
    },

    # ---------------- 물리학Ⅱ ----------------
    {
        "id": "phy2_pendulum", "grade": "고등학교 3학년", "subject": "물리학Ⅱ", "category": "역학",
        "name": "단진자 주기 공식", "latex": r"T = 2\pi \sqrt{\frac{L}{g}}",
        "desc": "실의 길이가 L인 단진자의 소진폭 진동 주기 T 식입니다.",
        "vars": [("T", "주기", "s"), ("L", "줄의 길이", "m"), ("g", "중력가속도", "9.8 m/s²")],
        "calc_type": "pendulum_calc", "inputs": [("l", "줄의 길이 L (m)", 1.0)]
    },
    {
        "id": "phy2_gravity", "grade": "고등학교 3학년", "subject": "물리학Ⅱ", "category": "역학",
        "name": "만유인력의 법칙", "latex": r"F = G \frac{m_1 m_2}{r^2}",
        "desc": "질량을 가진 두 물체 사이에 작용하는 중력의 크기 식입니다.",
        "vars": [("F", "만유인력", "N"), ("G", "만유인력 상수", "6.674×10⁻¹¹ N·m²/kg²"), ("r", "거리", "m")],
        "calc_type": "gravity_calc", "inputs": [("m1", "질량 m1 (kg)", 5.97e24), ("m2", "질량 m2 (kg)", 70.0), ("r", "거리 r (m)", 6.371e6)]
    },
    {
        "id": "phy2_coulomb", "grade": "고등학교 3학년", "subject": "물리학Ⅱ", "category": "전자기",
        "name": "쿨롱의 법칙 (전기력)", "latex": r"F = k \frac{|q_1 q_2|}{r^2}",
        "desc": "전하를 띤 두 입자 사이의 정전기력 크기입니다.",
        "vars": [("F", "전기력", "N"), ("k", "쿨롱 상수", "8.99×10⁹ N·m²/C²"), ("q1, q2", "전하량", "C")],
        "calc_type": "coulomb_calc", "inputs": [("q1", "전하량 q1 (C)", 1.0e-6), ("q2", "전하량 q2 (C)", 2.0e-6), ("r", "거리 r (m)", 0.1)]
    },

    # ---------------- 화학Ⅱ ----------------
    {
        "id": "ch2_vrms", "grade": "고등학교 3학년", "subject": "화학Ⅱ", "category": "기체",
        "name": "기체 분자 제곱평균제곱근 속도", "latex": r"v_{\text{rms}} = \sqrt{\frac{3RT}{M}}",
        "desc": "기체 분자 운동론에 의한 기체 분자의 평균 속도식입니다.",
        "vars": [("v_rms", "평균 속도", "m/s"), ("R", "기체상수", "8.314 J/mol·K"), ("T", "절대온도", "K"), ("M", "몰질량", "kg/mol")],
        "calc_type": "vrms_calc", "inputs": [("t", "절대온도 T (K)", 300.0), ("mw", "분자량 M (g/mol)", 32.0)]
    },
    {
        "id": "ch2_osmosis", "grade": "고등학교 3학년", "subject": "화학Ⅱ", "category": "용액",
        "name": "반트호프 삼투압 공식", "latex": r"\Pi = M \cdot R \cdot T",
        "desc": "묽은 용액의 삼투압 Π는 몰농도 M과 절대온도 T에 비례합니다.",
        "vars": [("Π", "삼투압", "atm"), ("M", "몰농도", "M"), ("R", "기체상수", "0.0821 L·atm/mol·K"), ("T", "절대온도", "K")],
        "calc_type": "osmosis_calc", "inputs": [("m_conc", "몰농도 M (M)", 0.1), ("t", "절대온도 T (K)", 298.0)]
    },

    # ---------------- 생명과학Ⅱ ----------------
    {
        "id": "bio2_menten", "grade": "고등학교 3학년", "subject": "생명과학Ⅱ", "category": "효소",
        "name": "미카엘리스-멘텐 효소 반응 속도식", "latex": r"v = \frac{V_{\text{max}} [S]}{K_m + [S]}",
        "desc": "기질 농도 [S] 변화에 따른 효소 촉매 반응 속도 식입니다.",
        "vars": [("v", "반응 속도", "μmol/min"), ("Vmax", "최대 반응 속도", "μmol/min"), ("Km", "미카엘리스 상수", "mM"), ("[S]", "기질 농도", "mM")],
        "calc_type": "menten_calc", "inputs": [("vmax", "V_max", 100.0), ("km", "K_m (mM)", 2.0), ("s", "기질 농도 [S] (mM)", 5.0)]
    },

    # ---------------- 지구과학Ⅱ ----------------
    {
        "id": "ea2_geostrophic", "grade": "고등학교 3학년", "subject": "지구과학Ⅱ", "category": "대기",
        "name": "지균풍 풍속", "latex": r"v_g = \frac{1}{2\Omega \sin \phi \cdot \rho} \frac{\Delta P}{\Delta n}",
        "desc": "기압경도력과 전향력이 평형을 이룰 때 부는 지균풍의 속도입니다.",
        "vars": [("vg", "지균풍 속도", "m/s"), ("Ω", "지구 자전 각속도", "7.29×10⁻⁵ rad/s"), ("φ", "위도", "°"), ("ρ", "공기 밀도", "kg/m³")],
        "calc_type": "geostrophic_calc", "inputs": [("lat", "위도 φ (도)", 37.5), ("dp_dn", "기압 경도 ΔP/Δn (Pa/m)", 0.001)]
    }
]

# 계산 함수 매핑
def calculate_formula(calc_type, inputs):
    try:
        if calc_type == "v_calc":
            res = inputs["ds"] / inputs["dt"]
            return f"평균 속도 (v) = {res:.2f} m/s"
        elif calc_type == "p_calc":
            res = inputs["m"] * inputs["v"]
            return f"운동량 (p) = {res:.2f} kg·m/s"
        elif calc_type == "I_calc":
            res = inputs["f"] * inputs["dt"]
            return f"충격량 (I) = {res:.2f} N·s"
        elif calc_type == "ep_calc":
            res = inputs["m"] * 9.8 * inputs["h"]
            return f"위치 에너지 (Ep) = {res:.2f} J"
        elif calc_type == "ek_calc":
            res = 0.5 * inputs["m"] * (inputs["v"]**2)
            return f"운동 에너지 (Ek) = {res:.2f} J"
        elif calc_type == "ohm_calc":
            res = inputs["i"] * inputs["r"]
            return f"전압 (V) = {res:.2f} V"
        elif calc_type == "power_calc":
            res = inputs["v"] * inputs["i"]
            return f"소비 전력 (P) = {res:.2f} W"
        elif calc_type == "ploss_calc":
            res = (inputs["i"]**2) * inputs["r"]
            return f"손실 전력 (P_loss) = {res:.2f} W"
        elif calc_type == "trans_calc":
            v2 = inputs["v1"] * (inputs["n2"] / inputs["n1"])
            return f"2차 코일 유도 전압 (V2) = {v2:.2f} V"
        elif calc_type == "mole_calc":
            n = inputs["m"] / inputs["m_w"]
            return f"몰수 (n) = {n:.4f} mol"
        elif calc_type == "fma_calc":
            res = inputs["m"] * inputs["a"]
            return f"알짜힘 (F) = {res:.2f} N"
        elif calc_type == "v_t_calc":
            res = inputs["v0"] + inputs["a"] * inputs["t"]
            return f"나중 속도 (v) = {res:.2f} m/s"
        elif calc_type == "s_t_calc":
            res = inputs["v0"]*inputs["t"] + 0.5*inputs["a"]*(inputs["t"]**2)
            return f"변위 (s) = {res:.2f} m"
        elif calc_type == "2as_calc":
            s = (inputs["v"]**2 - inputs["v0"]**2) / (2 * inputs["a"])
            return f"이동 변위 (s) = {s:.2f} m"
        elif calc_type == "thermo1_calc":
            q = inputs["du"] + inputs["w"]
            return f"흡수/방출 열량 (Q) = {q:.2f} J"
        elif calc_type == "eff_calc":
            e = (inputs["qin"] - inputs["qout"]) / inputs["qin"]
            return f"열효율 (e) = {e*100:.1f} % (상수: {e:.3f})"
        elif calc_type == "snell_calc":
            rad1 = math.radians(inputs["theta1"])
            sin_t2 = (inputs["n1"] * math.sin(rad1)) / inputs["n2"]
            if abs(sin_t2) <= 1.0:
                t2 = math.degrees(math.asin(sin_t2))
                return f"굴절각 (θ2) = {t2:.2f}°"
            else:
                return "전반사 조건 발생 (굴절각 없음)"
        elif calc_type == "debroglie_calc":
            h = 6.63e-34
            lam = h / (inputs["m"] * inputs["v"])
            return f"물질파 파장 (λ) = {lam:.4e} m"
        elif calc_type == "molarity_calc":
            res = inputs["n"] / inputs["v"]
            return f"몰농도 (M) = {res:.3f} M"
        elif calc_type == "molality_calc":
            res = inputs["n"] / inputs["w"]
            return f"몰랄농도 (m) = {res:.3f} m"
        elif calc_type == "ph_calc":
            ph = -math.log10(inputs["h_conc"])
            poh = 14.0 - ph
            return f"pH = {ph:.2f} (pOH = {poh:.2f})"
        elif calc_type == "neutral_calc":
            m2 = (inputs["n1"] * inputs["m1"] * inputs["v1"]) / (inputs["n2"] * inputs["v2"])
            return f"미지 염기 몰농도 (M2) = {m2:.3f} M"
        elif calc_type == "heat_calc":
            q = inputs["c"] * inputs["m"] * inputs["dt"]
            return f"열량 (Q) = {q:.2f} J"
        elif calc_type == "hw_calc":
            p = inputs["p"]
            q = 1.0 - p
            return f"AA: {p**2:.3f}, Aa: {2*p*q:.3f}, aa: {q**2:.3f}"
        elif calc_type == "conduction_calc":
            res = inputs["d"] / inputs["t"]
            return f"전도 속도 (v) = {res:.2f} cm/ms"
        elif calc_type == "stefan_calc":
            sigma = 5.67e-8
            e = sigma * (inputs["t"]**4)
            return f"방출 에너지 (E) = {e:.4e} W/m²"
        elif calc_type == "wien_calc":
            lam = 2.898e6 / inputs["t"]
            return f"최대 파장 (λmax) = {lam:.2f} nm"
        elif calc_type == "doppler_calc":
            v = 300000.0 * (inputs["dlam"] / inputs["lam0"])
            return f"시선 속도 (v) = {v:.2f} km/s"
        elif calc_type == "hubble_calc":
            v = 70.0 * inputs["d"]
            return f"후퇴 속도 (v) = {v:.2f} km/s"
        elif calc_type == "pendulum_calc":
            t = 2 * math.pi * math.sqrt(inputs["l"] / 9.8)
            return f"주기 (T) = {t:.2f} s"
        elif calc_type == "gravity_calc":
            g = 6.674e-11
            f = g * (inputs["m1"] * inputs["m2"]) / (inputs["r"]**2)
            return f"만유인력 (F) = {f:.4e} N"
        elif calc_type == "coulomb_calc":
            k = 8.99e9
            f = k * (inputs["q1"] * inputs["q2"]) / (inputs["r"]**2)
            return f"전기력 (F) = {f:.4e} N"
        elif calc_type == "vrms_calc":
            r = 8.314
            m_kg = inputs["mw"] / 1000.0
            vrms = math.sqrt((3 * r * inputs["t"]) / m_kg)
            return f"제곱평균제곱근 속도 (v_rms) = {vrms:.2f} m/s"
        elif calc_type == "osmosis_calc":
            pi = inputs["m_conc"] * 0.0821 * inputs["t"]
            return f"삼투압 (Π) = {pi:.3f} atm"
        elif calc_type == "menten_calc":
            v = (inputs["vmax"] * inputs["s"]) / (inputs["km"] + inputs["s"])
            return f"반응 속도 (v) = {v:.2f} μmol/min"
        elif calc_type == "geostrophic_calc":
            omega = 7.29e-5
            phi = math.radians(inputs["lat"])
            rho = 1.2
            vg = (1.0 / (2 * omega * math.sin(phi) * rho)) * inputs["dp_dn"]
            return f"지균풍 속도 (vg) = {vg:.2f} m/s"
        return "계산 완료"
    except Exception as e:
        return f"계산 오류: {str(e)}"

# 그래프 생성 함수
def render_chart(calc_type):
    if calc_type in ["v_calc", "s_t_calc", "v_t_calc"]:
        t = np.linspace(0, 10, 100)
        if calc_type == "v_calc":
            y = 5 * t
            title, y_label = "시간-변위 그래프 (v=5m/s 예시)", "변위 s (m)"
        elif calc_type == "v_t_calc":
            y = 2 * t
            title, y_label = "시간-속도 그래프 (a=2m/s² 예시)", "속도 v (m/s)"
        else:
            y = 0.5 * 2 * (t**2)
            title, y_label = "시간-변위 등가속도 그래프 (a=2m/s²)", "변위 s (m)"
        
        df = pd.DataFrame({"시간 t (s)": t, y_label: y})
        fig = px.line(df, x="시간 t (s)", y=y_label, title=title)
        st.plotly_chart(fig, use_container_width=True)

    elif calc_type == "menten_calc":
        s = np.linspace(0, 20, 100)
        v = (100 * s) / (2.0 + s)
        df = pd.DataFrame({"기질농도 [S] (mM)": s, "반응속도 v": v})
        fig = px.line(df, x="기질농도 [S] (mM)", y="반응속도 v", title="미카엘리스-멘텐 효소 반응 곡선 (Km=2, Vmax=100)")
        st.plotly_chart(fig, use_container_width=True)

    elif calc_type == "ph_calc":
        h = np.logspace(-14, 0, 100)
        ph = -np.log10(h)
        df = pd.DataFrame({"[H+] 농도 (M)": h, "pH": ph})
        fig = px.line(df, x="[H+] 농도 (M)", y="pH", log_x=True, title="[H+] 농도에 따른 pH 변화")
        st.plotly_chart(fig, use_container_width=True)

# Main UI
st.title("🧪 고등학교 과학 공식 모음 앱")
st.markdown("2022 개정 교육과정 반영 **고등학교 과학 전과목 핵심 공식 사전 및 실시간 계산기**입니다.")

# 사이드바 필터링
st.sidebar.header("🔍 검색 및 필터")
search_query = st.sidebar.text_input("공식 이름/미지수 검색", placeholder="예: v, m, 속도, pH, 허블")

grades = ["전체"] + list(dict.fromkeys([f["grade"] for f in FORMULAS_DB]))
selected_grade = st.sidebar.selectbox("학년 선택", grades)

if selected_grade != "전체":
    available_subjects = ["전체"] + list(dict.fromkeys([f["subject"] for f in FORMULAS_DB if f["grade"] == selected_grade]))
else:
    available_subjects = ["전체"] + list(dict.fromkeys([f["subject"] for f in FORMULAS_DB]))
selected_subject = st.sidebar.selectbox("과목 선택", available_subjects)

# 필터링 로직
filtered_formulas = FORMULAS_DB
if selected_grade != "전체":
    filtered_formulas = [f for f in filtered_formulas if f["grade"] == selected_grade]
if selected_subject != "전체":
    filtered_formulas = [f for f in filtered_formulas if f["subject"] == selected_subject]
if search_query:
    q = search_query.lower()
    filtered_formulas = [
        f for f in filtered_formulas 
        if q in f["name"].lower() or q in f["desc"].lower() or any(q in v[0].lower() or q in v[1].lower() for v[v_idx] in f["vars"] for v_idx in range(2))
    ]

st.sidebar.markdown(f"**검색된 공식 수:** `{len(filtered_formulas)}` 개")

# 메인화면 공식 출력
if not filtered_formulas:
    st.warning("🔍 검색 결과와 일치하는 공식이 없습니다. 다른 키워드를 입력해 보세요.")
else:
    for idx, formula in enumerate(filtered_formulas):
        with st.expander(f"📌 [{formula['subject']}] {formula['name']}", expanded=(idx==0)):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("공식")
                st.latex(formula["latex"])
                st.write(f"**설명:** {formula['desc']}")
                
                st.markdown("**기호 및 단위**")
                var_df = pd.DataFrame(formula["vars"], columns=["기호", "의미", "단위"])
                st.table(var_df)
                
            with col2:
                st.subheader("⚡ 실시간 계산기")
                inputs_val = {}
                for inp_id, inp_label, default_val in formula["inputs"]:
                    inputs_val[inp_id] = st.number_input(
                        inp_label, 
                        value=float(default_val), 
                        key=f"{formula['id']}_{inp_id}"
                    )
                
                if st.button("값 계산하기", key=f"btn_{formula['id']}"):
                    res_text = calculate_formula(formula["calc_type"], inputs_val)
                    st.success(f"결과: {res_text}")
                
                # 그래프 시각화
                render_chart(formula["calc_type"])

st.markdown("---")
st.caption("© 2026 High School Science Formula Interactive App | Built with Streamlit")

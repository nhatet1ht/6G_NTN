# Phản biện bài báo & định hướng nghiên cứu

> Dùng để (a) viết mục "critical review" trong báo cáo, (b) chuẩn bị gặp cô, (c) chốt đề tài.
> Bổ sung cho `../ILCHO_phan-tich-bai-bao.md` §6–8 của bạn.

---

## 1. Bốn hiểu lầm cần tránh khi trình bày bài này

### 1.1. "ILCHO dự đoán handover"
**Sai.** ILCHO **không dự đoán** một đại lượng bất định. Nó:
- Lấy vị trí vệ tinh **tất định** từ ephemeris (Lemma 1) — đây là **cơ học quỹ đạo**, không phải ML.
- Dùng MARL để **chọn** vệ tinh đích tối ưu (bài toán **điều khiển/tối ưu tuần tự**).

Câu "LEO satellite movement predictions made by its MARL system" ở Mục VII là **cách diễn đạt gây
nhầm** — cái được "predict" là quỹ đạo (tính bằng công thức Kepler), MARL chỉ chọn hành động.
→ Nếu đề tài bạn là *prediction-based*, phải nói rõ ILCHO là *decision-based* và đây là ranh giới.

### 1.2. "3 Lemma là đóng góp lý thuyết lớn"
**Nói giảm.** Lemma 1–2 = biến đổi hình học/cơ học quỹ đạo cổ điển, đóng gói lại. Lemma 3 = reduction
về Generalized Assignment Problem, khá hiển nhiên. Giá trị thật: chúng **biện minh** cho (a) thay đo
bằng tính, (b) cắt action space xuống `N_max`, (c) dùng học máy thay tối ưu chính xác.

### 1.3. "ILCHO tốt vì QMIX"
**Chưa đủ.** Ablation của bài chỉ so **sigmoid vs linear reward**, **không** so QMIX vs VDN/IQL/MAPPO
trong chính môi trường này. Cải thiện lớn nhất so với baseline có thể đến từ **thiết kế action space
(N_max) + reward đa mục tiêu phi tuyến**, chứ không nhất thiết từ riêng QMIX. Đây là điểm phản biện
mạnh.

### 1.4. "Kết quả áp dụng được cho Starlink thật"
**Thận trọng.** Mô phỏng: 1 khu vực [39–41°N/E], VSAT cố định, không Doppler, không lỗi ephemeris,
không mô phỏng RACH/T304, train offline. Khoảng cách tới triển khai thật còn xa.

---

## 2. Danh sách phản biện chi tiết (theo mức độ nghiêm trọng)

### Nhóm A — Giả định thu hẹp phạm vi
| # | Vấn đề | Ảnh hưởng | Bài có thừa nhận? |
|---|--------|-----------|------------------|
| A1 | **UE cố định (VSAT)** | Bỏ qua handheld/IoT/tàu/máy bay/HSR — nơi HO khó nhất | Có, viện [19,20,...] |
| A2 | **Bỏ qua Doppler** | Doppler + Doppler-rate ảnh hưởng đồng bộ, HOF thật | Có, viện 3GPP + [39-41] |
| A3 | **Ephemeris hoàn hảo, luôn hợp lệ** | Thực tế T430 hết hạn → sai số vị trí → chọn nhầm | Không bàn |
| A4 | **1 khu vực địa lý hẹp** | Chưa quét vĩ độ; vùng cực (Walker-Delta phủ yếu) chưa thử | Không |
| A5 | **Hard HO, 1 kết nối** | Không multi-connectivity/DAPS | Không |
| A6 | **Chỉ satellite HO** | Không beam HO, không ISL HO, không feeder-link HO | Không |

### Nhóm B — Phương pháp & đánh giá
| # | Vấn đề | Vì sao quan trọng |
|---|--------|-------------------|
| B1 | **Không ablation thuật toán MARL** (QMIX vs VDN/IQL/QTRAN/MAPPO) | Không tách được đóng góp của QMIX khỏi đóng góp của action-space/reward |
| B2 | **Không sensitivity analysis** cho `p_1, p_2, c_1, c_2, c_3, O_off, ζ, ψ_min, J` | Kết quả có thể nhạy với tinh chỉnh tay |
| B3 | **Thiếu thống kê**: số seed, độ lệch chuẩn, khoảng tin cậy | Không biết kết quả có ổn định qua lần chạy |
| B4 | **Baseline LBSH/HSNF "bị ghép" vào môi trường mới** | Bài tự nhận LBSH/HSNF thiết kế cho chòm nhỏ → so sánh có phần "sân nhà" |
| B5 | **Chi phí huấn luyện**: 3 000–30 000 episodes × 600 bước × K agent | Không cho wall-clock, không bàn online/continual learning trên RIC thật |
| B6 | **Không so overhead báo hiệu CHO** dù đó là động lực từ [30] | Đóng góp "giảm HO thừa" chưa được đo trực tiếp bằng overhead |
| B7 | **Định nghĩa HOF hẹp** (3 điều kiện tài nguyên/RVT/accessible) | Không gồm RACH fail, T304 expiry, mis-sync do Doppler → HOF thực có thể cao hơn |
| B8 | **Thiếu chi tiết tái lập**: kiến trúc GRU (lớp/nơ-ron), giá trị hằng số reward, `T_t`, `b`, optimizer | Khó reproduce |

### Nhóm C — Trình bày
- C1: OCR/công thức có lỗi nhỏ (`ω = √(GM_E/a_s²)` nên là `a_s³`; eq (19) target update viết cả 2 vế `θ'`).
- C2: Trích [32] (QMIX) ở chỗ nói về IQL — IQL kinh điển là Tan 1993.
- C3: Đánh số mục lộn ("Section VI provides an overview..." — đúng ra là Section IV).
- C4: Nhiều số liệu chỉ đọc được từ hình (Fig. 8, 9) → không có bảng chính xác cho Phase 2-a.

---

## 3. Điểm mạnh cần ghi nhận (để review cân bằng)

1. **Giải đúng nút thắt scale**: action = `N_max` (hằng số) → O(K) → chạy được ở quy mô Starlink,
   nơi các bài RL trước ([27],[28]) thất bại vì curse of dimensionality. Đây là đóng góp thật.
2. **Reward có cơ sở vật lý**: phân tích quan hệ throughput (phi đơn điệu) vs RVT (đơn điệu giảm) →
   chọn sigmoid → có ablation chứng minh linear không hội tụ. Lập luận sạch.
3. **Mô hình từ tham số thương mại thật** (Bảng I, hồ sơ FCC) thay vì < 100 vệ tinh giả định.
4. **Đánh giá đa chiều**: không chỉ #HO/throughput mà cả JFI (0,9798) và variance occupancy (0,072).
5. **Đặt vào kiến trúc khả thi**: near-RT RIC (O-RAN) train, on-board inference, biện minh bỏ trễ
   báo hiệu bằng T430.
6. **Ổn định theo tải**: #HO gần như phẳng khi UE 5→100 — tính chất vận hành rất đáng giá.

---

## 4. Câu hỏi nên hỏi cô (đã tinh chỉnh từ file phân tích của bạn)

**Về hướng đề tài**
1. Đề tài "dự đoán Handover" — cô muốn:
   - (a) Xây **mô hình dự đoán một đại lượng bất định** (RSRP/SINR tương lai, xác suất HOF, thời điểm
     link suy giảm, RVT hiệu dụng có fading) để **làm điều kiện trigger cho CHO** — khác hẳn ILCHO
     (vốn chỉ dùng hình học tất định); hay
   - (b) **Nhúng đặc trưng dự đoán vào state** của một khung RL/MARL kiểu ILCHO rồi đánh giá "giá trị
     của thông tin dự đoán"; hay
   - (c) **Tái hiện + mở rộng** ILCHO (thêm UE mobility / Doppler / multi-connectivity), phần "dự
     đoán" chỉ là lan truyền quỹ đạo?
2. Output mong muốn của mô hình dự đoán (nếu đi hướng a/b): đại lượng nào, horizon bao nhiêu bước,
   nhãn lấy từ đâu (simulator? dataset công khai?).
3. Có cần **so sánh định lượng với ILCHO** làm baseline không? Nếu có → cần **reproduce** ILCHO
   (Python/PyTorch, QMIX) — cô có chấp nhận dùng lại code QMIX mã nguồn mở (PyMARL/EPyMARL) không?

**Về phạm vi & công cụ**
4. Simulator: tự viết (như ILCHO) hay dùng NS-3 NTN / Hypatia / MATLAB Satellite Toolbox?
5. Chòm sao: Starlink shell nào? Có cần TLE thật không hay tham số Walker là đủ?
6. Có cần xét UE di động / Doppler / lỗi ephemeris không, hay giữ giả định như ILCHO?

**Về hình thức & tiến độ**
7. Báo cáo phân tích lần này: độ sâu tổng quan hay phản biện kỹ thuật (toán + thực nghiệm)? Dài bao
   nhiêu? Deadline?
8. Survey: phạm vi TN + NTN hay chỉ NTN? Số lượng bài tối thiểu? Có template không?

---

## 5. Ba đề xuất đề tài cụ thể (kèm đóng góp & rủi ro)

### Đề xuất 1 — "Predictive-CHO": dự báo SINR hiệu dụng để trigger CHO trong LEO NTN
- **Ý tưởng**: LSTM/Temporal-Fusion-Transformer dự báo **SINR hiệu dụng N bước tới** cho từng cặp
  UE–vệ tinh khả kiến, có tính **fading + tải dự kiến**. Điều kiện *preparation* = "SINR dự báo của
  serving sẽ tụt dưới ngưỡng trong ≤ N bước". Điều kiện *execution* = so SINR dự báo target vs serving.
- **So với**: A3-RSRP, A2/A3 khoảng cách (ILCHO), ILCHO đầy đủ.
- **KPI**: lead-time dự đoán, RMSE/MAE SINR, #HO, HOF, ping-pong, throughput, overhead CHO.
- **Đóng góp**: lấp G1 (file 06). Phần chọn WHERE có thể tái dùng QMIX của ILCHO.
- **Rủi ro**: cần simulator có fading + mô hình tải → công phu; nhãn SINR phải sạch.

### Đề xuất 2 — "Load-aware Predictive MARL": thêm dự báo occupancy vào state QMIX
- **Ý tưởng**: mở rộng `o_k` của ILCHO bằng **occupancy dự báo** của mỗi vệ tinh khả kiến (một mạng
  dự báo tải riêng, hoặc đặc trưng đếm số UE có RVT chồng lấn). Giữ nguyên QMIX/CTDE.
- **So với**: ILCHO gốc (chỉ `I,D,L,RVT`) — ablation "giá trị của thông tin dự báo tải".
- **KPI**: variance occupancy, JFI, HOF do nghẽn, #HO.
- **Đóng góp**: lấp G6; định lượng đóng góp của "prediction" tách khỏi "decision".
- **Rủi ro**: cần reproduce ILCHO trước; cải thiện có thể nhỏ nếu phạt HOF đã đủ tốt.

### Đề xuất 3 — "ILCHO + UE mobility + Doppler"
- **Ý tưởng**: bỏ giả định VSAT: UE di chuyển (ô tô/HSR), thêm Doppler biến thiên + sai số bù, thêm
  lỗi ephemeris (T430). Đánh giá độ bền của QMIX-CHO.
- **KPI**: HOF (định nghĩa mở rộng gồm mis-sync), #HO, throughput theo tốc độ UE.
- **Đóng góp**: lấp G2+G3; kiểm định tính tổng quát của ILCHO.
- **Rủi ro**: nhiều thứ phải mô hình hoá thêm; ít phần "dự đoán" nếu cô muốn hướng prediction.

---

## 6. Việc nên làm ngay (trước khi gặp cô)

- [ ] Đọc `01_ILCHO_phan-tich-chi-tiet.md` + bản dịch HTML song song, đánh dấu chỗ chưa hiểu.
- [ ] Đọc lướt file 02–05 để có nền; đọc kỹ file 05 (QMIX) và file 06 §2 (trục prediction vs decision).
- [ ] Tải & lướt: 3GPP **TR 38.821** (mục 7.3 mobility/HO), **QMIX** [arXiv:1803.11485],
      **ref [28]** (Lee et al., HO protocol learning) để so cách đặt bài toán.
- [ ] Viết bản tóm tắt 1 trang: Vấn đề → CHO+MARL/QMIX → Kết quả → 3 phản biện chính (§1) → 1 câu hỏi
      lớn cho cô (§4.1).
- [ ] Chuẩn bị danh sách câu hỏi §4 in ra giấy.
- [ ] (Nếu có thời gian) clone **EPyMARL/PyMARL** để biết QMIX chạy thế nào — ước lượng công sức
      reproduce.

---

## Nguồn tham khảo (ngoài bài báo)
- T. Rashid et al., *QMIX*, ICML 2018 — https://arxiv.org/abs/1803.11485
- J.-H. Lee et al., *Handover Protocol Learning for LEO Satellite Networks*, IEEE TWC 2024 (= ref [28]) — https://ieeexplore.ieee.org/document/10onwards (tra IEEE Xplore theo tiêu đề)
- E. Juan et al., *Performance Evaluation of the 5G NR Conditional Handover in LEO-based NTN*, WCNC 2022 (= ref [30]) — https://ieeexplore.ieee.org/document/9771987/
- *Reactive to Predictive Mobility Management: A Systematic Review of ML-Driven Handover Optimization*, MAKE 2025 — https://doi.org/10.3390/make8050133
- PyMARL / EPyMARL (code QMIX) — https://github.com/oxwhirl/pymarl ; https://github.com/uoe-agents/epymarl
- 3GPP TR 38.821 — https://www.3gpp.org

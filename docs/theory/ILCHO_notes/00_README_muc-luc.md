# Bộ tài liệu học tập: ILCHO & "AI cho Handover trong NTN/LEO"

> Mục tiêu: giúp bạn (1) đọc hiểu sâu bài báo **ILCHO** (IEEE TMC, 5/2026) tới mức phản biện được,
> và (2) có đủ nền tảng để viết một **survey** về chủ đề *dùng AI/ML cho handover*, đặc biệt trong
> mạng phi mặt đất (NTN) dùng vệ tinh LEO.

Tất cả các file trong thư mục này do Claude soạn ngày **2026-09-04** dựa trên:
- File PDF gốc của bài báo (trong thư mục cha).
- Bản dịch tiếng Việt `../ILCHO_ban_dich_tieng_viet.html` và bản phân tích `../ILCHO_phan-tich-bai-bao.md` bạn đã có.
- Khảo sát bổ sung trên web cho các kiến thức nền — **mọi nguồn ngoài đều được ghi link** ở cuối từng file.

---

## Thứ tự đọc đề xuất

| # | File | Nội dung | Khi nào đọc |
|---|------|----------|-------------|
| 1 | [`01_ILCHO_phan-tich-chi-tiet.md`](01_ILCHO_phan-tich-chi-tiet.md) | Mổ xẻ bài báo theo từng mục: 3 Lemma + toàn bộ công thức, mô hình hệ thống, MDP/QMIX, Algorithm 1, mọi bảng số liệu, điểm mạnh/yếu | Đọc song song với bản dịch HTML |
| 2 | [`02_Nen-tang_Handover.md`](02_Nen-tang_Handover.md) | Handover là gì; các loại HO (hard/soft, BHO, CHO, DAPS); sự kiện đo A1–A6; quy trình HO; HOF/RLF/ping-pong; MRO & KPI | Nếu bạn chưa nắm chắc HO trong mạng mặt đất |
| 3 | [`03_Nen-tang_NTN_LEO.md`](03_Nen-tang_NTN_LEO.md) | NTN là gì; lộ trình chuẩn hoá 3GPP Rel-15→19; LEO/MEO/GEO/HEO; payload trong suốt vs tái sinh; cơ học quỹ đạo (Kepler, Walker-Delta, ephemeris); mô hình kênh 38.811/38.821; Doppler; vì sao HO trong NTN khó | Trước khi đọc Mục III–IV của bài báo |
| 4 | [`04_Conditional_Handover_CHO.md`](04_Conditional_Handover_CHO.md) | CHO chi tiết: động cơ, sự kiện chuẩn bị/thực thi, các trigger cho NTN (thời gian, vị trí, elevation), SIB19/ephemeris, so sánh BHO/CHO/DAPS | Trước khi đọc Mục IV-A của bài báo |
| 5 | [`05_Nen-tang_RL_MARL.md`](05_Nen-tang_RL_MARL.md) | RL: MDP, hàm giá trị, Bellman, Q-learning, DQN. MARL: Dec-POMDP, non-stationarity, CTDE, IQL, VDN, **QMIX**, QTRAN/QPLEX, MADDPG, MAPPO, DRQN | Trước khi đọc Mục IV-B, IV-C, V của bài báo |
| 6 | [`06_Survey_AI-cho-Handover.md`](06_Survey_AI-cho-Handover.md) | Khung phân loại cho survey: *dự đoán* vs *ra quyết định*; supervised/RL/DRL/MARL/FL; TN vs NTN; bảng công trình tiêu biểu; 4 baseline của ILCHO; khoảng trống nghiên cứu; phương pháp đánh giá | Khi bắt đầu viết survey |
| 7 | [`07_Thuat-ngu_ky-hieu.md`](07_Thuat-ngu_ky-hieu.md) | Từ điển thuật ngữ + bảng ký hiệu toán học của bài báo | Tra cứu bất cứ lúc nào |
| 8 | [`08_Cau-hoi-phan-bien_huong-nghien-cuu.md`](08_Cau-hoi-phan-bien_huong-nghien-cuu.md) | Đánh giá phản biện, câu hỏi mở, các hướng luận văn khả thi, nên reproduce gì | Khi chuẩn bị gặp cô / chốt đề tài |

---

## Tóm tắt 30 giây về bài báo

**ILCHO (Intelligent LEO satellite Conditional Handover)** = **CHO** (chuyển giao có điều kiện của 3GPP Rel-16)
+ **MARL/QMIX** (học tăng cường đa tác tử) làm bộ chọn vệ tinh đích.

- **Bài toán:** trong chòm sao LEO siêu dày (Starlink), mỗi UE phải HO liên tục (mỗi ~6–130 s). Đo RSRP kiểu mạng mặt đất không đáng tin (các cell vệ tinh ở xa, tín hiệu gần giống nhau). Cần chọn vệ tinh đích sao cho **throughput toàn mạng cao nhất** mà **số HO ít nhất** → chứng minh là **NP-hard** (Lemma 3).
- **Ý tưởng cốt lõi:** vị trí vệ tinh là **xác định trước** từ ephemeris (Lemma 1) ⇒ tập vệ tinh "khả kiến" tính trước được (Lemma 2) ⇒ giới hạn **không gian hành động = N_max** (số vệ tinh khả kiến tối đa) thay vì = tổng số vệ tinh ⇒ MARL **scale tuyến tính O(K)** theo số UE.
- **Kết quả:** so với 4 baseline (MD, MVT, HSNF, LBSH), ILCHO giữ số HO gần như không đổi khi UE tăng 5→100, HOF < 1.4, throughput cao nhất (~3.76–3.85 bps/Hz), JFI = 0.9798.
- **Điểm cần phản biện:** đây là bài toán **tối ưu hoá quyết định**, không phải **dự đoán** đại lượng bất định. "Prediction" trong bài chỉ là **lan truyền quỹ đạo Kepler** (tất định). Xem file 08.

---

## Quy ước trong bộ tài liệu

- 🔵 **[BÀI BÁO]** — nội dung lấy trực tiếp từ bài báo ILCHO.
- 🟢 **[NGOÀI]** — kiến thức nền khảo sát thêm; có link nguồn ở mục *Nguồn tham khảo* cuối file.
- Ký hiệu toán giữ nguyên như bản gốc (subscript, chữ Hy Lạp) để đối chiếu.

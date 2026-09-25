# Đọc hiểu: phần nào là trọng tâm bài toán ILCHO, phần nào là làm thêm

File này chia toàn bộ việc đã làm thành 3 nhóm để biết cái gì cần nắm chắc (trọng tâm), cái gì
chỉ là kiểm chứng thêm, và cái gì nằm ngoài bài toán:

| Nhóm | Là gì | Mức độ cần nắm |
|---|---|---|
| **A. Trọng tâm** | Thuật toán ILCHO và các kết quả của chính ILCHO mà bài báo công bố | Phải hiểu kỹ, đây là nội dung chính khi báo cáo |
| **B. Kiểm chứng bổ sung** | Thử nghiệm tự làm thêm quanh ILCHO, bài báo **không** có | Hiểu ý chính và kết luận là đủ |
| **C. Ngoài bài toán** | Thuật toán của bài khác mà ILCHO đem vào so sánh (HSNF, LBSH) | Chỉ cần biết đang là bản rút gọn, để làm sau |

Số liệu chi tiết của mọi thử nghiệm: `bao_cao/latex_baocao_ket_qua/ket_qua_tai_hien.tex` và
`gpu100_repro/REPORT.md`.

---

## A. Trọng tâm — thuật toán ILCHO

### A.1 Bài toán

Trong chòm vệ tinh LEO mật độ cao (Starlink), UE phải chuyển giao liên tục. CHO của 3GPP cho
phép chuẩn bị trước vệ tinh đích, nhưng **không nói nên chọn vệ tinh đích nào** khi hàng trăm UE
cùng tranh kênh. Chọn theo tiêu chí đơn (gần nhất, nhìn thấy lâu nhất) làm nhiều UE dồn vào
cùng một vệ tinh → nghẽn → chuyển giao thất bại (HOF) tăng vọt.

ILCHO = **CHO + học tăng cường đa tác tử QMIX** để chọn vệ tinh đích cho từng UE.

### A.2 Các thành phần của thuật toán và vị trí trong code

Tất cả đã được tái hiện đầy đủ:

| Thành phần (theo bài báo) | Ý nghĩa | Code |
|---|---|---|
| Lemma 1 | Vị trí vệ tinh là hàm tất định của thời gian (từ tham số quỹ đạo Walker-Delta) → tính trước được, không cần đo | `src/ilcho/constellation.py` |
| Lemma 2 | Điều kiện "khả kiến" UE–vệ tinh → tập vệ tinh khả kiến, suy ra `N_max` | `constellation.py`, `sanity.py` |
| Lemma 3 | Bài toán gán tối ưu là NP-hard → lý do dùng học tăng cường thay vì giải chính xác | (lý thuyết, không có code) |
| Mô hình kênh | 3GPP TR 38.811/38.821, SE theo Shannon | `channel.py` |
| CHO 3 pha | Chuẩn bị (RL chọn đích) → Thực thi (sự kiện khoảng cách, Eq. 28) → Hoàn tất | `environment.py` |
| Agent | Mỗi UE là 1 agent | `environment.py` |
| Quan sát | `N_max` vệ tinh ứng viên × đặc trưng (chỉ số, khoảng cách, số kênh đang dùng, RVT) | `environment.py:255-265` |
| Hành động | Chọn 1 trong `N_max` vệ tinh → không gian hành động không phụ thuộc tổng số vệ tinh | `environment.py` |
| Hàm thưởng | Phạt HOF nặng, phạt HO nhẹ, còn lại dùng hàm sigmoid của SE và RVT (Eq. 27); biến thể tuyến tính (Eq. 30) | `environment.py:395-413` |
| QMIX | DRQN (GRU) cho từng agent + mạng trộn đơn điệu dùng hypernetwork → `Q_tot`; huấn luyện tập trung, thực thi phân tán | `qmix.py` |
| Algorithm 1 | Replay buffer, target network, epsilon-greedy | `qmix.py`, `rollout.py`, `train.py` |

**Ý tưởng quan trọng nhất của bài:** không gian hành động = `N_max` (số vệ tinh khả kiến tối
đa, ~27) thay vì toàn bộ hàng nghìn vệ tinh → độ phức tạp tuyến tính theo số UE, mở rộng được
lên quy mô Starlink.

### A.3 Chỗ bản cài khác bài báo (nên nói rõ khi báo cáo)

Không cái nào làm thay đổi thuật toán:

1. Quan sát có **5** đặc trưng thay vì 4: thêm cờ `is_serving` (vệ tinh này có đang phục vụ UE
   không) — `environment.py:173`.
2. Trạng thái toàn cục đưa vào mạng trộn là **trung bình + max** quan sát của mọi agent
   (`qmix.py:192-194`), vì bài không định nghĩa rõ và ghép toàn bộ 100 agent thì tốn bộ nhớ.
3. Hằng số bài **không công bố** phải tự chọn: `c1, c2, c3` (sigmoid), `w1, w2` (tuyến tính),
   `O_off`, tần số sóng mang (`config.py:128-145`).
4. `batch = 8` thay vì 32 (GPU 8 GB không đủ), 3.000–4.000 episode thay vì tới 30.000 (nhưng
   đường cong huấn luyện đã bão hòa từ ~2.400).

### A.4 Các kết quả của bài báo đã được tái hiện lại

Mỗi dòng dưới đây tương ứng với một hình/bảng **có trong bài báo**:

| Thử nghiệm | Hình/bảng bài báo | Kết quả tái hiện |
|---|---|---|
| Số vệ tinh khả kiến theo vĩ độ | Fig. 5 | Phase 1-a đỉnh 17 (khớp); Phase 2-a đỉnh 29 (bài: 27) |
| Huấn luyện ILCHO 100 agent, 600 s | Fig. 6 | Hội tụ mượt, bão hòa ~episode 2.400 |
| Đối chứng hàm thưởng sigmoid / tuyến tính | Fig. 6–7 | **Không khớp**: tuyến tính cũng hội tụ ổn định, kết quả tương đương sigmoid |
| HO, HOF, SE theo số UE trên Phase 2-a | Fig. 8 | HOF của ILCHO thấp hơn hẳn MD-CHO, MVT-CHO ở mọi số UE (khớp xu hướng) |
| Phase 1-a, Phase 2-a, hybrid | Fig. 10, Table III | Hybrid giảm HOF (khớp); Phase 1-a bão hòa ở 70–100 UE |
| Độ công bằng (JFI, CDF) | Fig. 11 | JFI 0,995–0,998 (bài: 0,9798) |
| Cân bằng tải | Table IV | Đúng xu hướng nhưng chênh lệch nhỏ hơn nhiều so với bài |

**Số liệu của chính ILCHO so với bài báo (Phase 2-a, 5→100 UE, trung bình 3 seed):**

| Chỉ số | Bài báo | Tái hiện | Nhận xét |
|---|---|---|---|
| HOF / UE | thấp, tối đa 1,38 ở 100 UE | 0,05 → 4,52 | Cùng xu hướng, giá trị cao hơn |
| HO / UE | 10,8 → 13,0 (ổn định) | ~10 tới 40 UE, giảm còn 4,3 ở 100 UE | Ổn định tới tải vừa |
| SE [bps/Hz] | 3,85 → 3,76 | 2,69 → 2,49 | Thấp hơn (phụ thuộc tần số sóng mang, hằng số thưởng) |
| JFI | 0,9798 | 0,995–0,998 | Tốt hơn |

MD-CHO và MVT-CHO cũng nằm trong nhóm A: đó là hai luật chọn đơn giản (gần nhất, nhìn thấy lâu
nhất) do chính bài ILCHO định nghĩa, cài đúng hoàn toàn (`baselines.py:30-61`).

**Kết luận trọng tâm:** thuật toán ILCHO đã được tái hiện đầy đủ; ý chính của bài báo — RL giữ
HOF thấp khi các luật chọn đơn giản sụp lúc tải tăng — **tái hiện được**. Giá trị tuyệt đối
chưa khớp hoàn toàn do tham số bài không công bố.

---

## B. Kiểm chứng bổ sung — tự làm thêm, bài báo không có

Mục đích chung: kiểm tra xem kết quả ở nhóm A có đáng tin không. Chỉ cần nhớ kết luận.

| Thử nghiệm | Làm gì | Kết luận |
|---|---|---|
| 3 lượt tăng quy mô | 16 → 48 → 100 agent, 300 → 600 s | HOF ILCHO ở 100 UE: 47,4 → 21,1 → 4,95 — quy mô huấn luyện ảnh hưởng rất mạnh |
| Benchmark CPU/GPU | Đo tốc độ, bộ nhớ | Giải thích vì sao dùng `batch = 8` |
| 3 seed huấn luyện | Train lại 2 lần độc lập | Kết luận không đổi, không phải do may mắn |
| Quét hệ số pha `F` | Thử hết 48 giá trị | Không giá trị nào ra đỉnh 27 → lệch 27/29 không do `F` |
| Khảo sát độ nhạy | Đổi `O_off`, thời gian guard, số kênh `J` | Thứ hạng các phương pháp không đổi |
| Zero-shot | Chính sách train trên Phase 2-a chạy trên chòm khác | Vẫn hơn MD/MVT tới tải vừa |
| Train riêng từng chòm | Train native Phase 1-a, hybrid | HOF thấp hơn zero-shot 2,4–5,1 lần ở tải vừa |
| OneWeb | Chòm có trong Table I nhưng bài không thử | Mọi phương pháp sụp từ 70 UE vì thiếu vệ tinh khả kiến |
| `batch = 4` | So với `batch = 8` | Không khác biệt đáng kể |

Chi tiết: `gpu100_repro/REPORT.md` (§1, §4.3, §6, §7), `gpu100_repro/BAO_CAO_2026-09-16.md`,
`gpu100_repro/runs/f_sweep/f_sweep.json`.

---

## C. Ngoài bài toán — HSNF và LBSH

Đây là thuật toán của **bài báo khác** mà ILCHO đem vào làm đối thủ so sánh:

| Tên | Bài gốc | Bản hiện tại trong code |
|---|---|---|
| HSNF | [22] S. Zhang et al., "A network-flows-based satellite handover strategy for LEO satellite networks", IEEE WCL 2021 | Gán tham lam theo SE tức thời, có giới hạn kênh — **không** có đồ thị luồng, không nhìn trước theo thời gian (`baselines.py:64-114`) |
| LBSH | [26] N. Badini et al., "Reinforcement learning-based load balancing satellite handover using NS-3", IEEE ICC 2023 | ILCHO bỏ mạng trộn (IQL), thưởng tuyến tính SE + RVT, phạt HO nặng — **không** có thành phần tải trong hàm thưởng, dùng chung `N_max = 27` (`qmix.py` mode `iql`, `train.py:33-39`) |

Lưu ý: một số file cũ (`CHUA_LAM_DUOC.md`, `KE_HOACH_TAI_TAO_DAY_DU.md`) ghi LBSH là của He et al.
(GLOBECOM 2020) — sai, đó là bài [25]. LBSH là [26] Badini et al.

**Hệ quả:** hai kết quả "HSNF có SE cao nhất" và "LBSH không sụp ở tải cao" khác bài báo, nhưng
không kết luận được là bài báo sai, vì đối thủ đang là bản rút gọn. Mọi so sánh ILCHO với
HSNF/LBSH chỉ mang tính tham khảo.

**Trạng thái:** việc cài đúng hai bài gốc (mục A3 trong `gpu100_repro/CHUA_LAM_DUOC.md`) để làm
sau. Không ảnh hưởng tới nhóm A.

---

## Tóm tắt một câu

> Thuật toán ILCHO đã tái hiện đầy đủ và kết luận chính của bài tái hiện được (nhóm A); các thử
> nghiệm nhóm B là kiểm chứng thêm cho thấy kết quả đáng tin; HSNF/LBSH (nhóm C) là thuật toán
> của bài khác, đang dùng bản rút gọn và sẽ xử lý sau.

## Thứ tự đọc gợi ý

1. File này.
2. `docs/theory/ILCHO_notes/01_ILCHO_phan-tich-chi-tiet.md` — hiểu sâu bài báo (nhóm A).
3. `docs/PHUONG_PHAP_XAY_DUNG_CODE.md` — cách dựng code từ bài báo (nhóm A).
4. `bao_cao/latex_baocao_ket_qua/ket_qua_tai_hien.tex` hoặc `gpu100_repro/REPORT.md` — số liệu
   đầy đủ (nhóm A và B).
5. `gpu100_repro/CHUA_LAM_DUOC.md` — những gì còn lại (nhóm C và các giới hạn).

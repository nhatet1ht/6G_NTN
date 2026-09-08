# Bắt đầu từ đây

Đây là **điểm vào của repo** — thứ tự đọc toàn bộ tài liệu, và nhật ký các phiên làm việc.
Mục đích: dù hội thoại/phiên Claude nào đó kết thúc, bất kỳ ai (bạn, hoặc một phiên Claude
khác sau này) mở file này ra là biết ngay repo đang ở đâu, đã làm gì, và nên đọc/làm gì tiếp.

**Quy tắc sống còn của file này:** mỗi khi có việc mới đáng kể (chạy xong một lượt tái hiện,
thử nghiệm mới, phát hiện mới, quyết định mới) — **thêm một dòng vào "Nhật ký phiên làm việc"
ở cuối file**, không chỉ để trong lịch sử chat. Chat sẽ mất, file này thì không.

---

## 1. Bức tranh tổng thể (30 giây)

Repo này tái hiện bài báo **ILCHO** — M. Choi et al., "Intelligent Handover Scheme for
Improved 6G NTN LEO Satellite Network Performance," IEEE TMC, 5/2026 — trên máy cá nhân,
không có mã nguồn gốc (đã tra cứu, không tồn tại công khai). Ý tưởng bài báo: 3GPP Conditional
Handover (CHO) + multi-agent RL (QMIX) để chọn vệ tinh đích trong chòm sao LEO mật độ cao.

Đã có **3 lượt tái hiện**, mỗi lượt gần bài báo hơn lượt trước nhờ phần cứng tốt hơn:

| Lượt | Phần cứng | Agent train | Horizon train | Báo cáo |
|---|---|--:|--:|---|
| 1 | CPU | 12–16 | 300 s | (gộp trong `REPORT.md`) |
| 2 | CPU | 48 | 420 s | `REPORT.md` (gốc repo) |
| **3 (mới nhất, gần bài báo nhất)** | **GPU** | **100 (= max bài báo)** | **600 s (= đúng bài báo)** | **`gpu100_repro/REPORT.md`** |

---

## 2. Thứ tự đọc

### Nếu chưa biết gì về bài báo / nền tảng NTN-RL

1. [`docs/theory/ILCHO_notes/00_README_muc-luc.md`](docs/theory/ILCHO_notes/00_README_muc-luc.md)
   — mục lục riêng cho phần lý thuyết nền (Handover, NTN/LEO, CHO, RL/MARL, thuật ngữ), có
   thứ tự đọc 8 file bên trong nó, đi kèm bản dịch/phân tích bài báo gốc trong cùng thư mục.

### Nếu đã hiểu bài báo, muốn hiểu code được dựng ra sao

2. [`README.md`](README.md) — tổng quan repo, cách chạy.
3. [`docs/PHUONG_PHAP_XAY_DUNG_CODE.md`](docs/PHUONG_PHAP_XAY_DUNG_CODE.md) — code được dựng
   từ bài báo thế nào, module theo module, vì sao chọn cách làm đó.
4. [`docs/METHODOLOGY.html`](docs/METHODOLOGY.html) — cùng nội dung, có sơ đồ; §2 là bảng
   thuật ngữ NTN/3GPP + RL/MARL kèm nguồn đọc thêm.

### Kết quả tái hiện — **đọc lượt mới nhất trước**

5. **[`gpu100_repro/REPORT.md`](gpu100_repro/REPORT.md)** — lượt 3 (GPU, 100 agent, horizon
   600s đúng bài báo). **Đọc file này trước nếu chỉ có thời gian đọc một báo cáo kết quả** —
   nó tự so sánh ngược lại với lượt 1/2 ở §0 và §4.1.
6. **[`gpu100_repro/CHUA_LAM_DUOC.md`](gpu100_repro/CHUA_LAM_DUOC.md)** — mọi thứ **chưa làm
   được**, chia 3 loại (làm được nếu có thêm thời gian / bị chặn cứng vì bài báo giấu tham số
   / đã thử nhưng không tái hiện được). Đây là danh sách sống — cập nhật mỗi khi đóng hoặc mở
   thêm một mục.
7. [`REPORT.md`](REPORT.md) (gốc repo) — lượt 1+2 (CPU). Vẫn cần giữ vì `gpu100_repro/REPORT.md`
   §4.1 dẫn số liệu từ đây để chứng minh xu hướng "quy mô train càng lớn càng sát bài báo".
8. [`docs/KE_HOACH_TAI_TAO_DAY_DU.md`](docs/KE_HOACH_TAI_TAO_DAY_DU.md) — roadmap viết **trước**
   lượt 3, một phần đã lỗi thời (bước 1–2 nay đã xong) — xem bảng cập nhật trạng thái ở
   `gpu100_repro/CHUA_LAM_DUOC.md` §4 trước khi tin nội dung file này.

---

## 3. Trạng thái hiện tại (cập nhật lần cuối: 2026-09-08)

**Đã xong:** lượt 3 tái hiện (100 agent/600s/GPU) hoàn chỉnh — training, eval 4 chòm vệ tinh
(Phase 2-a, Phase 1-a, hybrid, OneWeb), reward ablation, sensitivity; đã merge vào `main`.
Đã thử dò hệ số phasing Walker `F` (kết quả âm tính — xem `gpu100_repro/CHUA_LAM_DUOC.md` C4).

**Đang treo, chờ quyết định:** train đa-seed cho 3 policy (mục A2) — đã tính effort cụ thể
(seed=0 đã có sẵn từ lượt 3; cần thêm ~17h46p cho 2 seed nữa hoặc ~35h32p cho 4 seed nữa, xem
bảng trong `gpu100_repro/CHUA_LAM_DUOC.md` §A2). **Chưa chạy** — người dùng muốn đọc hết tài
liệu hiện có trước, rồi mới quyết định chạy bao nhiêu seed. Khi quay lại, hỏi thẳng "chạy đa-seed
chưa" hoặc chờ người dùng chủ động yêu cầu.

**Đang mở / có thể làm tiếp** (chi tiết + effort ước tính ở `gpu100_repro/CHUA_LAM_DUOC.md`):
- Nhóm [A] (làm được, cần thêm thời gian): train đa-seed, cài đúng HSNF/LBSH theo bài gốc
  [22]/[26], `batch=32` đúng Table II (cần GPU ≥16GB), train native cho Phase 1-a/hybrid,
  quét trục batch/learn-every.
- Nhóm [B] (chặn cứng, cần tác giả): 5 tham số bài báo không công bố (tần số sóng mang,
  `O_off`, hằng số reward, hyperparameter HSNF/LBSH gốc — `F` đã loại khỏi nhóm này vì đã
  quét hết, xem C4). Liên hệ: Jong-Moon Chung, `jmc@yonsei.ac.kr`.

---

## 4. Nhật ký phiên làm việc

*(mới nhất ở trên cùng — mỗi dòng: ngày, việc đã làm, file liên quan)*

- **2026-09-08** — Tính effort cụ thể cho train đa-seed (mục A2): ~17h46p thêm cho 3 seed,
  ~35h32p thêm cho 5 seed (seed=0 đã có sẵn). Người dùng chọn **đọc tài liệu trước, chưa chạy**
  — xem mục 3 ở trên.
- **2026-09-08** — Dò hệ số phasing Walker `F` (0–47) cho Starlink Phase 2-a để tìm giá trị
  khớp đỉnh khả kiến 27 (bài báo). **Kết quả âm tính**: không `F` nào cho ra 27, dải kết quả
  29–32, `F=1` (giá trị đang dùng) đã là tốt nhất có thể. → `gpu100_repro/runs/f_sweep/f_sweep.json`,
  cập nhật `gpu100_repro/CHUA_LAM_DUOC.md` (mục C4) và `gpu100_repro/REPORT.md` (§2, §8).
- **2026-09-08** — Bổ sung eval OneWeb Phase 1 (có trong Table I bài báo, chưa từng được so
  sánh ở lượt 1/2). Vùng quan tâm chỉ ~6-7 vệ tinh khả kiến (quỹ đạo gần cực, không hướng vùng
  vĩ độ trung bình) → 70-100 UE mọi phương pháp đều vỡ trận, thiếu dung lượng vật lý, không
  phải lỗi thuật toán. → `gpu100_repro/REPORT.md` §7.3, `runs/g100_eval_oneweb_phase_1/`.
- **2026-09-08** — Chạy lượt tái hiện thứ 3 (GPU, RTX 3060 Ti, sau khi đổi máy): 100 agent
  (= max bài báo), `N_max=27`, horizon 600s cho **cả train lẫn eval** (đúng Table II — 2 lượt
  trước phải giảm vì CPU đơn nhân). Benchmark xác nhận GPU tăng tốc `learn()` ~10-15× nhưng bị
  giới hạn VRAM 8GB ở `batch=8` (không phải 32 như Table II). Khoảng cách HOF ILCHO-vs-HSNF/LBSH
  ở 100 UE thu hẹp từ 6,3× (lượt 2) xuống 1,47× (lượt 3). → `gpu100_repro/REPORT.md`,
  `gpu100_repro/CHUA_LAM_DUOC.md` (tạo mới), merge thẳng vào `main` (commit `5400d90`).
- **2026-09-07** — Thêm ghi chú lý thuyết và tài liệu tham khảo bài báo dưới `docs/theory/`
  (commit `8b2bf50`).
- **2026-09-06** — Lượt tái hiện 1+2 (CPU): dựng toàn bộ code từ bài báo (`src/ilcho/`), lượt 1
  quy mô nhỏ (12-16 agent), lượt 2 quy mô lớn hơn (48 agent, `N_max=27` đúng bài báo). Kết quả
  và toàn bộ phân tích trong `REPORT.md` gốc repo (commit `e6c27e8`).

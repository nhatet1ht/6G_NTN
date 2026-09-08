# Những gì chưa làm được — cập nhật sau lượt 3 (GPU, 100 agent)

Tài liệu này liệt kê **rõ ràng, không tô hồng** những gì bản tái hiện ILCHO (cả 3 lượt, tính
đến `gpu100_repro/REPORT.md`) **chưa làm**, chia làm 3 loại có bản chất khác nhau:

- **[A] Chưa làm nhưng làm được** — chỉ cần thêm thời gian/phần cứng/công sức kỹ thuật.
- **[B] Không thể làm được** — bị chặn cứng vì bài báo không công bố thông tin cần thiết.
- **[C] Đã thử và không tái hiện được** — không phải "chưa làm", mà là kết quả thật, khác
  bài báo, đã kiểm chứng nhiều lượt.

(Tài liệu liên quan: `../docs/KE_HOACH_TAI_TAO_DAY_DU.md` viết trước lượt 3 — nhiều mục ở đó
**đã xong** sau lượt này; bảng ở §4 dưới đây cập nhật trạng thái từng bước.)

---

## [A] Chưa làm nhưng làm được — nếu có thêm thời gian/phần cứng

### A1. `batch_size = 8` thay vì 32 (Table II)

Lượt 3 dùng batch=8 vì GPU 8 GB VRAM bị OOM ở batch=16/32 (đo thực tế, xem
`gpu100_repro/REPORT.md` §1). **Cách khắc phục đã biết nhưng chưa làm:**
- GPU ≥16 GB (ví dụ RTX 4080/4090, hoặc thuê cloud), hoặc
- Cài **truncated BPTT** (chia chuỗi 600 bước thành đoạn ngắn hơn khi backward) hoặc
  **gradient checkpointing** cho `nn.GRU` — giảm bộ nhớ đỉnh mà không cần đổi GPU.

Chưa rõ mức ảnh hưởng thực tế của batch nhỏ hơn tới sample efficiency — quan sát được là
huấn luyện vẫn hội tụ mượt và bão hòa sớm (§3 báo cáo chính), nhưng chưa loại trừ hoàn toàn
khả năng batch=32 hội tụ nhanh hơn hoặc ổn định hơn nữa.

### A2. Huấn luyện đa-seed (chỉ eval mới có đa-seed)

Mỗi policy (`g100_ilcho_sigmoid`, `g100_ilcho_linear`, `g100_lbsh`) hiện chỉ có **một lần
train** (`--seed 0`). Việc **eval** đã dùng 3 seed để lấy trung bình ± độ lệch chuẩn, nhưng
bản thân quá trình học — vốn có thể hội tụ về nghiệm khác nhau tùy seed khởi tạo mạng — chưa
được lặp lại độc lập. Cần train mỗi cấu hình **3–5 lần với seed khác nhau** rồi báo cáo
mean±std của chính sách cuối cùng để biết kết quả ở `REPORT.md` §4 có ổn định qua random seed
hay chỉ là một lần chạy may mắn. Với tốc độ ~3,6 s/episode hiện tại, nhân 3–5 lần cho ra
~1,5–2 ngày chạy nền — làm được, chỉ chưa làm vì ngân sách thời gian lượt này giới hạn overnight.

### A3. Cài đặt đầy đủ HSNF (ref. [22]) và LBSH (ref. [26]) theo đúng bài gốc

Bản hiện tại (`src/ilcho/baselines.py`, `src/ilcho/qmix.py` mode `iql`):
- **HSNF** = gán tham lam theo SE cao nhất, ràng buộc capacity, **không nhìn trước theo thời
  gian** (không phải min-cost-flow đa thời điểm như tên "network flow" ngụ ý).
- **LBSH** = IQL chia sẻ tham số + reward tải cân bằng, **không phải** thuật toán cụ thể của
  He et al. (IEEE GLOBECOM 2020).

Hệ quả quan sát được (không đổi qua cả 3 lượt): HSNF-xấp-xỉ thắng throughput tuyệt đối mọi
lúc; LBSH-xấp-xỉ không "vỡ trận" ở tải cao như bài báo mô tả. **Chưa làm** vì cần đọc kỹ 2 bài
tham chiếu gốc trước khi cài lại — ước tính ~0,5 ngày đọc + ~1 ngày code/kiểm thử (xem
`../docs/KE_HOACH_TAI_TAO_DAY_DU.md` §3, vẫn còn nguyên giá trị).

### A4. ~~Dò `F`~~ ✅ Đã thử — kết quả âm tính, chuyển sang mục [C3] bên dưới

### A5. Chưa train riêng cho từng chòm vệ tinh — mọi kết quả Phase 1-a/hybrid đều là *zero-shot*

`g100_ilcho_sigmoid` chỉ train trên Starlink Phase 2-a; kết quả ở Phase 1-a và hybrid
(`REPORT.md` §7) đều là **chuyển giao chính sách chưa từng thấy chòm vệ tinh đó lúc train**.
Chưa thử train một policy riêng, native cho Phase 1-a hoặc hybrid (lượt 1 có làm việc này ở
quy mô nhỏ — thư mục cũ `runs/xeval_phase1a_native/` — nhưng chưa lặp lại ở quy mô 100 agent).
Việc này tốn thêm ~2,5–4 giờ train mỗi chòm vệ tinh muốn thử riêng.

### A6. ~~OneWeb Phase 1~~ ✅ Đã làm (bổ sung sau khi viết tài liệu này)

`CONSTELLATIONS["oneweb_phase_1"]` (1.200 km, nghiêng 87,9°, 720 vệ tinh) có trong Table I
bài báo nhưng chưa từng được đưa vào so sánh ở lượt 1/2. Đã chạy bổ sung
(`gpu100_repro/runs/g100_eval_oneweb_phase_1/`, xem `REPORT.md` §7.3): zero-shot với 3 policy
đã train, tới 40 UE ILCHO vẫn tốt/ngang HSNF-LBSH và hơn hẳn MD-CHO/MVT-CHO, nhưng 70–100 UE
**mọi phương pháp đều vỡ trận** — vùng quan tâm [39–41°N] chỉ có ~6-7 vệ tinh khả kiến với
OneWeb (nghiêng gần cực, đỉnh khả kiến thật sự ở vĩ độ 86°) nên hệ thống thiếu dung lượng vật
lý ở tải cao, không phải lỗi thuật toán. Không còn nằm trong danh sách "chưa làm".

### A7. Chưa thử `learn_every` nhỏ hơn kết hợp batch lớn hơn khi có GPU mạnh hơn

Lượt 3 chọn `learn-every=1, batch=8` vì đó là điểm khả thi duy nhất đã đo được trên RTX 3060
Ti 8 GB. Chưa thử các điểm khác trên trục đánh đổi batch/tần suất học (ví dụ `batch=16,
learn-every=2` — cùng tổng số mẫu học nhưng khác cách chia) để xem có nhạy với cách chia này
không.

---

## [B] Không thể làm được — bị chặn cứng bởi bài báo không công bố

Không đổi so với `../docs/KE_HOACH_TAI_TAO_DAY_DU.md` §5 — liệt kê lại cho đầy đủ, vì đây là
phần **sẽ không bao giờ tự đóng được** dù đầu tư thêm bao nhiêu thời gian/phần cứng:

| Tham số | Bài báo nói gì | Ảnh hưởng nếu đoán sai |
|---|---|---|
| Tần số sóng mang chính xác | chỉ nói "Ka-band" | dịch SE tuyệt đối, không đổi thứ hạng phương pháp (đã kiểm chứng §6 báo cáo chính) |
| `O_off` — offset thực thi CHO (Eq. 28) | không công bố giá trị | đã khảo sát 10–100 km, thứ hạng không đổi |
| `c1, c2, c3` (sigmoid, Eq. 27), `w1, w2` (linear, Eq. 30), `p1, p2` | không công bố | **là nguyên nhân khả dĩ nhất** khiến ablation reward (§5 báo cáo chính) không tái hiện được |
| Hệ số phasing Walker `F` | không công bố cho Starlink | lệch đỉnh khả kiến P2a 29 vs 27 (~7%) |
| Siêu tham số HSNF/LBSH gốc | chỉ có tên bài tham chiếu [22]/[26], không có giá trị cụ thể | không tách được "cài sai" khỏi "tham số khác" khi so sánh |

**Cách duy nhất đóng hoàn toàn khoảng trống này:** liên hệ tác giả liên lạc của bài báo —
**Jong-Moon Chung** (`jmc@yonsei.ac.kr`), Khoa Kỹ thuật Điện và Điện tử, Đại học Yonsei. Đã
tra cứu không có mã nguồn/preprint/tài liệu bổ sung công khai nào (xem
`../docs/KE_HOACH_TAI_TAO_DAY_DU.md` §2). Đây là việc của bạn, không tự ý thay bạn liên hệ.

---

## [C] Đã thử, không tái hiện được — là phát hiện, không phải thiếu sót

Ba điều này đã được kiểm chứng lặp lại qua **cả 3 lượt** (16→48→100 agent), kể cả ở lượt 3
đúng quy mô bài báo — nên đây là kết luận có độ tin cậy cao, không phải do chưa đủ compute:

1. **"ILCHO có throughput cao nhất trong mọi phương pháp"** — sai trong bản tái hiện này.
   HSNF (bản xấp xỉ, xem A3) luôn thắng throughput thô ở mọi số UE, mọi lượt.
2. **"Reward tuyến tính (Eq. 30) huấn luyện bất ổn, kém hơn sigmoid"** — sai trong bản tái
   hiện này. Cả hai hội tụ mượt, chính sách cuối gần như tương đương, kể cả ở đúng quy mô
   100 agent/600s (lượt 3, §5 báo cáo chính).
3. **Đỉnh vệ tinh khả kiến Phase 2-a = 27** — bản này luôn ra 29 (±7%), do `F` không công bố
   (xem B). **Đã quét thử để xác nhận (2026-09-08):** thử toàn bộ `F` nguyên từ 0 đến 47
   (`num_planes-1`) cho Starlink Phase 2-a — **không có giá trị `F` nào cho đỉnh đúng 27**;
   toàn dải kết quả nằm trong khoảng 29–32, và `F=1` (giá trị đang dùng) hóa ra đã là một
   trong những lựa chọn *thấp nhất* có thể trong toàn bộ không gian tìm kiếm. Kết luận: lệch
   27 vs 29 **không đến từ `F`** — phải do một chi tiết khác bài báo không công bố (cách tính
   "đỉnh" của họ, độ phân giải lấy mẫu, offset RAAN/epoch, hay quy ước Walker khác). Đây là
   kết quả âm tính thật (đã tìm hết không gian rời rạc hợp lệ), không phải do tìm chưa đủ kỹ,
   và **không nằm trong nhóm [B]** nữa theo nghĩa "chưa quét" — quét rồi, không ra. Dữ liệu thô:
   `runs/f_sweep/f_sweep.json`.

Bốn mục này **không nằm trong danh sách A** — không phải "chưa làm", mà "đã làm, kết quả khác
bài báo", và lặp lại nhất quán (hoặc đã quét hết không gian hợp lệ) nên nhiều khả năng phản
ánh khác biệt thật về cách cài đặt baseline hoặc tham số ẩn, không phải lỗi hay thiếu sót của
bản tái hiện.

---

## 4. Trạng thái các bước trong `../docs/KE_HOACH_TAI_TAO_DAY_DU.md` (cập nhật sau lượt 3)

| Bước (tài liệu cũ) | Trạng thái sau lượt 3 |
|---|---|
| 1. Vector hoá `environment.py` | ✅ **Xong** (đã có trước lượt 3, dùng trong cả 3 lượt) |
| 2. Train đúng quy mô bài báo (100 agent, 600s, N_max=27) | ✅ **Xong** ở mức 3.000–4.000 episode (chưa thử 30.000, xem A2/A7 — nhưng đã bão hòa sớm, xem `REPORT.md` §3) |
| 3. Cài đầy đủ HSNF/LBSH theo bài gốc [22]/[26] | ❌ **Chưa** — xem A3 |
| 4. Đa seed | ⚠️ **Một nửa** — eval đã đa-seed (3), train vẫn 1 seed — xem A2 |
| 5. Liên hệ tác giả | ❌ **Chưa** — việc của bạn, xem [B] |

---

## Tóm tắt 1 dòng cho từng mục

| # | Việc | Loại | Effort nếu muốn làm |
|---|---|---|---|
| A1 | batch=32 đúng Table II | A | GPU ≥16GB hoặc truncated BPTT |
| A2 | Train đa-seed (3–5 lần/policy) | A | ~1,5–2 ngày chạy nền |
| A3 | Cài đúng HSNF [22] / LBSH [26] | A | ~1,5 ngày đọc+code |
| A4 | ~~Dò `F` cho đúng đỉnh N_max=27~~ | A | ✅ đã xong — kết quả âm tính, xem C4 |
| A5 | Train native cho Phase 1-a/hybrid | A | ~2,5–4h/chòm vệ tinh |
| A6 | ~~Thêm OneWeb Phase 1 vào so sánh~~ | A | ✅ đã xong — xem `REPORT.md` §7.3 |
| A7 | Quét trục batch/learn-every | A | vài giờ |
| B  | 5 tham số ẩn bài báo không công bố | B | không tự làm được — cần tác giả |
| C1–C4 | 4 tuyên bố/số liệu không khớp (kể cả `F`, mới thêm) | C | đã kết luận, không cần làm thêm |

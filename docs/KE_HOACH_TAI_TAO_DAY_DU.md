# Kế hoạch tái tạo hoàn toàn bài báo ILCHO

Tài liệu này trả lời câu hỏi: **"Làm sao để tái tạo hoàn toàn bài báo?"** — dựa trên
những gì bản tái hiện hiện tại (`REPORT.md`, `PHUONG_PHAP_XAY_DUNG_CODE.md`) đã đạt được
và chưa đạt được.

---

## 1. Hai nghĩa khác nhau của "tái tạo hoàn toàn"

| | Nghĩa (A): Đúng phương pháp &amp; đúng quy mô | Nghĩa (B): Khớp từng con số tuyệt đối |
|---|---|---|
| Là gì | Cùng cơ chế CHO+QMIX, cùng quy mô huấn luyện (số agent, số episode, N_max) như bài báo | Mọi bảng/hình ra đúng y số liệu bài báo công bố |
| Có làm được không | **Có** — chỉ tốn thời gian tính toán và công sức kỹ thuật | **Không** — bị chặn cứng bởi tham số bài báo không công bố |
| Vì sao bị chặn | — | Bài báo **không công bố**: tần số sóng mang, offset `O_off` (Eq. 28), hằng số hàm
thưởng `c1, c2, c3, p1, p2` (Eq. 27/30), hệ số phasing Walker `F`. Không có mã nguồn, không
có preprint, không có tài liệu bổ sung công khai (đã tra cứu — xem §5). |

**Kết luận:** mục tiêu khả thi và có ý nghĩa khoa học là tiến gần nhất có thể tới nghĩa
**(A)**. Tài liệu này là lộ trình cho việc đó.

---

## 2. Đã tra cứu — xác nhận giới hạn cứng

Đã tìm kiếm trên web (WebSearch/WebFetch) các nguồn sau, không tìm thấy mã nguồn hay tài
liệu bổ sung nào của chính bài báo:

- Trang xuất bản chính thức của Yonsei University (elsevierpure) — chỉ có DOI
  (`10.1109/TMC.2025.3642278`) và tóm tắt, **không có link code/supplementary**.
- Tìm theo tên bài + "ILCHO" + "github"/"arxiv" — không ra kết quả trùng khớp là bản
  preprint hay repo của chính nhóm tác giả.

→ Cách duy nhất để có được các tham số ẩn là **liên hệ trực tiếp tác giả**. Trong bài báo,
tác giả liên hệ (corresponding author) là **Jong-Moon Chung** (`jmc@yonsei.ac.kr`), Khoa Kỹ
thuật Điện và Điện tử, Đại học Yonsei. Đây là việc của bạn nếu muốn thực hiện — không tự ý
thay bạn liên hệ.

---

## 3. Lộ trình 5 bước để tiến gần nghĩa (A)

### Bước 1 — Vector hoá `environment.py` *(điều kiện tiên quyết)*

**Hiện trạng:** hàm `CHOEnv.step()` xử lý từng UE bằng vòng lặp Python
(`for k in range(K): ...`) để giải quyết tranh chấp kênh công bằng theo đúng thứ tự ngẫu
nhiên. Với K nhỏ (10–16, như đã train) chi phí này chấp nhận được; với K = 100 (đúng quy mô
bài báo) vòng lặp Python trở thành điểm nghẽn chính.

**Cần làm:** viết lại phần giải quyết tranh chấp kênh + tính reward bằng phép toán mảng
NumPy có xử lý va chạm theo lô (batch), thay vì lặp từng agent; đồng thời cho phép chạy
**nhiều episode song song** (batched rollout) để một lần forward/backward của mạng nơ-ron
xử lý nhiều chuỗi cùng lúc — tận dụng CPU đa nhân tốt hơn, và là điều kiện để dùng GPU có
ý nghĩa (xem lại phần "vì sao không dùng GPU" — với batch đủ lớn, GPU mới thật sự có lợi).

**Công sức ước tính:** ~nửa ngày viết code + kiểm thử lại toàn bộ (so khớp kết quả trước/sau
vector hoá trên cùng seed để đảm bảo không đổi hành vi mô phỏng).

**Vì sao phải làm trước:** nếu không, Bước 2 sẽ mất **2–3 tuần** chạy liên tục thay vì vài
ngày (xem ước tính bên dưới).

### Bước 2 — Huấn luyện đúng quy mô bài báo

| Tham số | Bản hiện tại | Đúng bài báo |
|---|---|---|
| `N_max` (kích thước không gian hành động) | 16 | 27 |
| Số agent lúc train | 12–16 | tới 100 |
| Độ dài episode | 300 s | 600 s |
| Số episode | 800–1.800 | 3.000–30.000 |

**Ước tính thời gian** (suy từ tốc độ đo được thực tế: ~3,7 s/episode ở 16 agent/300 s trên
CPU hiện tại, chưa vector hoá):
- Hệ số phóng đại ≈ (100/16 agent) × (600/300 s) × (episode 3.000→30.000/1.800)
  ≈ 6,25 × 2 × (1,7→16,7) ≈ **21× đến 209×**
- Chưa vector hoá: **≈ 1,6 ngày** (ở mức tối thiểu 3.000 episode) đến **≈ 16 ngày** (ở mức
  tối đa 30.000 episode) chạy liên tục.
- Sau khi vector hoá (Bước 1), kỳ vọng giảm còn khoảng **1/5 – 1/10** thời gian trên, tức
  **vài giờ đến 2–3 ngày** tuỳ mức episode chọn.

**Đề xuất thực tế:** bắt đầu ở mức "vừa phải" — `N_max=27`, 50 agent, 5.000 episode — trước
khi thử đúng 100 agent / 30.000 episode, để phát hiện sớm nếu có vấn đề hội tụ ở quy mô lớn.

### Bước 3 — Cài đặt đầy đủ HSNF và LBSH theo đúng bài gốc

Bản hiện tại dùng **xấp xỉ**: HSNF = gán tham lam theo capacity (không phải mô hình luồng
mạng đầy đủ như ref. [22]); LBSH = IQL chia sẻ tham số (không phải cài đặt đầy đủ như ref.
[26]). Hai bài tham chiếu đó cần được tìm và đọc kỹ:

- [22] — bài về "HO strategy based on network flows" (Zhang et al., dẫn trong bài ILCHO)
- [26] — bài về "Load balancing satellite HO" dùng multi-agent Q-learning (He et al., IEEE
  GLOBECOM 2020)

**Công sức ước tính:** ~nửa ngày tìm & đọc 2 bài, ~1 ngày cài đặt lại + kiểm thử.

**Lý do quan trọng:** kết quả hiện tại cho thấy **bản HSNF xấp xỉ của tôi thắng ILCHO về
throughput thô** và **bản LBSH xấp xỉ không bị "vỡ trận" ở tải cao như bài báo mô tả** — cả
hai đều là dấu hiệu bản xấp xỉ chưa đúng hành vi gốc, nên đây là ưu tiên cao nếu muốn so
sánh công bằng.

### Bước 4 — Chạy nhiều seed để có ý nghĩa thống kê

Mỗi cấu hình (mỗi tổ hợp constellation × reward × số agent train) nên chạy **3–5 seed** độc
lập rồi lấy trung bình ± độ lệch chuẩn, thay vì 1 seed như phần lớn kết quả hiện tại. Việc
này nhân thời gian ở Bước 2–3 lên 3–5 lần nhưng bù lại: đã thấy trong `REPORT.md` §7.1 rằng
huấn luyện natively cho Phase 1-a bị **phương sai giữa các lần chạy** (chạy tự nhiên trên
Phase 1-a lại kém hơn chạy chuyển giao zero-shot) — chỉ 1 seed không đủ để kết luận chắc
chắn.

### Bước 5 — (Tuỳ chọn) Liên hệ tác giả

Cách duy nhất đóng hoàn toàn khoảng trống ở nghĩa (B). Không nằm trong khả năng của tôi —
là quyết định và hành động của bạn.

---

## 4. Bảng tổng hợp effort

| Bước | Việc | Ai làm | Thời gian ước tính |
|---|---|---|---|
| 1 | Vector hoá môi trường | tôi (code) | ~0,5 ngày |
| 2 | Train quy mô đầy đủ (sau bước 1) | máy tính (nền) | vài giờ – 3 ngày tuỳ mức episode |
| 3 | Cài lại HSNF/LBSH đúng bài gốc | tôi (đọc + code) | ~1,5 ngày |
| 4 | Đa seed | máy tính (nền) | ×3–5 thời gian bước 2–3 |
| 5 | Liên hệ tác giả | bạn | không xác định |

**Nếu muốn bắt đầu ngay:** cho tôi biết bạn muốn ưu tiên bước nào trước — vector hoá +
train ở mức "vừa phải" (khoảng 1–2 ngày chạy nền), hay cài lại HSNF/LBSH cho đúng bài gốc
trước (không cần chờ máy chạy lâu), hay cả hai song song.

---

## 5. Những gì KHÔNG đổi dù làm hết 5 bước trên

Ngay cả khi hoàn thành cả 5 bước, các điểm sau **vẫn là giả định**, vì bản chất chúng không
thể suy ra từ bất cứ thông tin công khai nào:

- Tần số sóng mang chính xác (bài chỉ nói "Ka-band")
- Giá trị offset `O_off` trong Eq. (28)
- Hằng số `c1, c2, c3` của hàm thưởng sigmoid, và `p1, p2`
- Hệ số phasing Walker `F` của các chòm Starlink

Những mục này sẽ luôn được đánh dấu **GIẢ ĐỊNH** trong `config.py` và trong
`PHUONG_PHAP_XAY_DUNG_CODE.md`, bất kể quy mô huấn luyện lớn tới đâu.

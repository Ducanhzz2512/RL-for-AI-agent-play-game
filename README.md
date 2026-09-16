# Flappy Bird RL: So sánh On-Policy (PPO), Off-Policy (DQN) và các họ thuật toán mở rộng


## Tổng quan

Dự án xây dựng và đánh giá các AI agent tự học chơi Flappy Bird bằng Reinforcement Learning, tập trung vào **cơ chế thuật toán** thay vì chỉ so điểm cuối. Trọng tâm là lượng hóa trade-off **Sample Efficiency ↔ Stability ↔ Chi phí tính toán** giữa các họ thuật toán, với giao thức so sánh công bằng, có kiểm định thống kê và tái lập được.

## Mục tiêu dự án

- **Agent PPO và DQN tự học chơi Flappy Bird** từ tương tác, không lập trình luật cứng.
- **Bộ kết quả thực nghiệm có thể tái lập**: seed cố định, config YAML, log đầy đủ.
- **So sánh định lượng PPO vs DQN** trên cùng môi trường, cùng ngân sách env-steps.
- **Kiểm định thống kê với nhiều seed**: báo cáo mean ± std, kiểm định Wilcoxon.
- **Phân tích trade-off Sample Efficiency ↔ Stability** giữa hai cơ chế học.
- **Đường cong ảnh hưởng của Replay Buffer Size** như núm điều chỉnh "độ off-policy".
- **Làm rõ vai trò của Experience Replay** trong Off-Policy RL.

## Câu hỏi nghiên cứu

| Mã | Câu hỏi |
|---|---|
| RQ1 | DQN có đạt sample efficiency cao hơn PPO trên Flappy Bird state thủ công? |
| RQ2 | PPO có ổn định hơn (variance giữa các seed thấp hơn)? |
| RQ3 | Tồn tại ngưỡng replay size mà sample efficiency tăng nhưng stability giảm? |
| RQ4 | Cả hai agent RL có vượt baseline heuristic? |
| RQ5 | Học không gradient (GA) và học có giám sát (MLP) khác biệt thế nào về hiệu quả mẫu và trần hiệu năng? |

## Giả thuyết

- **H1:** DQN (off-policy) sample-efficient hơn PPO nhờ tái sử dụng dữ liệu qua replay buffer.
- **H2:** PPO (on-policy) ổn định hơn, std giữa các seed thấp hơn.
- **H3:** Replay buffer quá lớn → dữ liệu cũ gây lệch phân phối → stability giảm dù sample efficiency tăng.
- **H4:** Cả PPO và DQN đều vượt baseline heuristic sau ngân sách env-steps xác định.
- **H5:** GA (không gradient) đạt hiệu năng cuối tương đương trên trạng thái nhỏ nhưng kém hiệu quả mẫu hơn nhiều so với PPO/DQN.
- **H6:** Khi song song hóa, GA cạnh tranh về thời gian chạy dù thua về tổng số tương tác.
- **H7:** GA có phương sai giữa các seed cao hơn PPO, nhưng không gặp bất ổn do gradient.
- **H8:** MLP học có giám sát (behavior cloning) đạt hiệu năng xấp xỉ heuristic và hội tụ với rất ít tương tác.
- **H9:** Khi gặp trạng thái ngoài phân phối chuyên gia, MLP suy giảm mạnh hơn RL.
- **H10:** PPO/DQN vượt trần heuristic, còn MLP bị chặn ở trần này.

## Các họ thuật toán

### Trục chính

| Nhóm | Thuật toán chính | Cơ chế ổn định |
|---|---|---|
| On-Policy | **PPO** (clip + GAE) | Clipped surrogate objective, GAE cân bằng bias-variance |
| Off-Policy | **DQN** (Experience Replay + target network) | Replay phá tương quan mẫu, target network ổn định mục tiêu |

### Mở rộng

| Họ | Đại diện | Nguồn học | Dùng gradient | Cần reward |
|---|---|---|---|---|
| Off-Policy | DQN | Reward | Có | Có |
| On-Policy | PPO | Reward | Có | Có |
| Di truyền | GA | Fitness | Không | Có (fitness) |
| Học có giám sát | MLP (BC) | Nhãn | Có | Không |

- **Biến độc lập duy nhất:** cơ chế học (on-policy vs off-policy).
- **Cố định:** state representation, kiến trúc MLP, số env-steps, tuning budget, env seed.

### Ghi chú về họ mở rộng

- **GA (tiến hóa trọng số):** mỗi cá thể là vector trọng số MLP; độ thích nghi = điểm trung bình qua N ván; toán tử chọn lọc, lai ghép, đột biến. Không cần gradient, dễ song song hóa nhưng kém hiệu quả mẫu.
- **MLP học có giám sát (behavior cloning):** dùng heuristic (Tầng B) sinh dữ liệu `(state, action)`, train MLP dự đoán hành động. Trần hiệu năng bằng chuyên gia; không khám phá; dễ suy giảm khi lệch phân phối.

## Môi trường

- **L0 – CartPole:** sanity check, xác minh code PPO/DQN đúng trước khi chuyển sang môi trường chính. Không nằm trong đóng góp.
- **L1 – Flappy Bird (chính):** state thủ công gồm vị trí, vận tốc nhân vật, khoảng cách tới pipe; hành động rời rạc (nhảy/không nhảy). Chọn vì action ít, state đơn giản, thời gian huấn luyện ngắn — so sánh thuật toán không bị nhiễu bởi bài toán thị giác.
- **L2 – Pixel input (tùy chọn):** khảo sát ảnh hưởng biểu diễn trạng thái. Không áp dụng cho GA.

## Thiết kế thực nghiệm

- **Seed:** tối thiểu 3 seed/cấu hình; đánh giá trên seed khởi tạo khác seed train.
- **Kiểm định:** Wilcoxon rank-sum (phi tham số, phù hợp mẫu nhỏ).
- **Ablation chính:** quét replay size DQN ở 3 mức (10k / 50k / 200k) → vẽ đường cong trade-off sample efficiency ↔ stability.

### Quy tắc so sánh công bằng

- **Đếm số tương tác với môi trường**, không đếm số ván.
- GA song song hóa dễ (mỗi cá thể độc lập) → báo cáo **cả thời gian chạy tuần tự và song song**.
- Với MLP có giám sát: **tính cả chi phí sinh nhãn** (số tương tác của heuristic) vào ngân sách.
- Cân bằng ngân sách tinh chỉnh tham số cho mọi họ.
- Ghi rõ khác biệt bản chất: GA không có tín hiệu gán công theo từng bước; BC dùng nhãn thay vì reward — đây là khác biệt cơ chế, không phải lỗi.

### Tiêu chí đánh giá

| Chỉ số | Cách đo | Ý nghĩa |
|---|---|---|
| Sample efficiency | AUC learning curve đến ngưỡng | Tốc độ học / env-step |
| Final performance | Điểm trung bình cuối train | Chất lượng hội tụ |
| Stability | Std giữa các seed + variance trong train | Độ tin cậy, tái lập |
| Chi phí | Env-steps, wall-clock (serial & parallel) | Hiệu quả tài nguyên |
| Điểm số | Trung bình & cao nhất | Hiệu năng trực quan |

**Trình bày:** learning curve có dải tin cậy (shaded CI), bảng thống kê mean ± std kèm p-value, biểu đồ so sánh, và đường cong trade-off sample efficiency ↔ stability theo replay size.

### Ba tầng so sánh

- **Tầng A:** PPO vs DQN tự train — đóng góp chính.
- **Tầng B:** baseline random + heuristic — mốc chuẩn hóa hiệu năng.
- **Tầng C:** tham chiếu pretrained SB3 / leaderboard env chuẩn — chỉ làm bối cảnh, không so điểm thô khác môi trường.

## Kết quả kỳ vọng

1. Agent PPO và DQN tự học chơi Flappy Bird, vượt baseline heuristic.
2. Bảng so sánh định lượng PPO vs DQN có kiểm định thống kê.
3. Đường cong trade-off **Sample Efficiency ↔ Stability** theo replay size.
4. Phân tích định lượng vai trò của **Experience Replay** trong off-policy RL.
5. Đối chiếu bổ sung với GA và MLP có giám sát về hiệu quả mẫu và trần hiệu năng.

## Đóng góp dự kiến

1. **Giao thức so sánh on/off-policy công bằng, tái lập được, có kiểm định thống kê.**
2. **Đường cong trade-off** sample efficiency ↔ stability theo mức off-policyness.
3. **Kết quả ablation định lượng** về vai trò của replay buffer.
4. **So sánh mở rộng** giữa học có gradient, không gradient và có giám sát trên cùng môi trường.

## Công nghệ

- Python, PyTorch
- Gymnasium, `flappy-bird-gymnasium`, Pygame
- NumPy, Pandas, Matplotlib
- TensorBoard (logging), YAML (config), seed cố định (tái lập)


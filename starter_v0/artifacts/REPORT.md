# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: Zone 7 / Team 1
- Members: Phùng Gia Bảo / Hoàng Thanh Chiến / Mạc Văn Thanh
- Provider/model: Openrouter

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent là một trợ lý nghiên cứu đa tác vụ, hỗ trợ tra cứu tin tức thời sự/kiến thức chung trên Web, tương tác mạng xã hội Twitter/X (lọc theo xu hướng/tài khoản), tìm kiếm repository trên GitHub (sắp xếp và lọc timeframe linh hoạt), tra cứu tài liệu khoa học trên arXiv (đọc và trích xuất PDF), và đối chiếu thông tin quy định nội bộ công ty (Policy). Đồng thời, Agent hỗ trợ tổng hợp thông tin thành bản tin định dạng đẹp mắt và gửi trực tiếp lên Telegram sau khi được người dùng phê duyệt rõ ràng.

**Link dùng thử (deploy):**

URL: https://ones-dictionary-equation-volunteer.trycloudflare.com/

## A2. Tool agent có

Bộ 11 công cụ chuyên biệt mà Agent sử dụng bao gồm:

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Gửi câu hỏi làm rõ (dạng văn bản hoặc lựa chọn Yes/No) khi thiếu thông tin quan trọng hoặc yêu cầu xác nhận. | không |
| timeline | Lấy các dòng trạng thái (tweets) gần đây nhất của một tài khoản Twitter/X cụ thể qua screenname. | không |
| social_search | Tìm kiếm các bài viết thảo luận trên Twitter/X theo từ khóa chủ đề (hỗ trợ sắp xếp Latest hoặc Top). | không |
| lookup | Tra cứu thông tin trên Internet (chủ đề general/news) kèm bộ lọc khoảng thời gian (day/week/month/year). | không |
| fetch | Lấy và đọc nội dung chi tiết dạng văn bản thô từ một URL công khai. | không |
| format | Trình bày danh sách tin tức thu thập được thành bản tin theo các khuôn mẫu bố cục đẹp mắt. | không |
| send | Gửi trực tiếp văn bản bản tin lên Telegram channel (yêu cầu phê duyệt rõ ràng từ người dùng). | không |
| policy | Tìm kiếm trong quy định nội bộ của công ty (Citation, Data Privacy, Publishing...). | không |
| papers | Tìm kiếm các bài báo khoa học học thuật trên arXiv theo từ khóa. | không |
| paper_text | Tải PDF và đọc nội dung bài báo khoa học cụ thể trên arXiv để phân tích chuyên sâu. | không |
| github_search | Tìm kiếm các repository trên GitHub . | có |

## A3. Câu hỏi mẫu để thử

Dưới đây là 5 câu hỏi/yêu cầu mẫu để team khác có thể trải nghiệm toàn bộ tính năng thông minh của Agent:

1. **Github Search Fallback**: *"top 5 repo nhiều star nhất trên github trong tuần"* (Kiểm tra cách Agent tự động làm sạch query thành `""`, thiết lập `timeframe="week"`, và fallback an toàn sang `stars:>1` mà không bị crash).
2. **Missing Info Clarification**: *"Tóm tắt bài viết này hộ mình"* (Kiểm tra việc Agent phát hiện thiếu link cụ thể và chủ động hỏi xin URL).
3. **Twitter Handle Mapping**: *"Lấy 5 tweet mới nhất của Elon Musk"* (Kiểm tra cách Agent tự động ánh xạ tên Elon Musk thành handle `@elonmusk` để gọi công cụ).
4. **Safety Confirmation**: *"Đăng bản tin này lên Telegram giúp mình"* (Kiểm tra cơ chế an toàn: luôn hỏi xác nhận Yes/No trước khi thực hiện hành động ghi/gửi).
5. **Out of Scope Boundary**: *"Viết giúp mình một hàm Python tính Fibonacci bằng recursion."* (Kiểm tra khả năng tự nhận thức ranh giới tác vụ và lịch sự từ chối viết code của Agent).

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Prompt Hash | Tools Hash | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---|---|---:|---:|---|
| v0 | None | `eb1c8179815bd79d34de7d326420bb99b3072e6e8ae96464c02d4411f905fc68` | `6cdb53d5d7b8de80d60b298b1357f462cedbedfae261d5ba60b08ccc401687c5` | Establish baseline performance | 0.00 | 0.65 | [v0_B_base_openrouter_20260602T123911898331.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/runs/v0_B_base_openrouter_20260602T123911898331.json) |
| v1 | [system_prompt.md](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/artifacts/system_prompt.md) | `e5fae69973b7e03a56b87dd73db3df7c56366c35e9fa607e0997a282c5293a27` | `6cdb53d5d7b8de80d60b298b1357f462cedbedfae261d5ba60b08ccc401687c5` | Adding out-of-scope refusals and clarification protocols | 0.65 | 0.80 | [v1_B_base_openrouter_20260602T143300376366.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/runs/v1_B_base_openrouter_20260602T143300376366.json) |
| v2 | [system_prompt.md](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/artifacts/system_prompt.md) | `2644e5a6d5acfd6da7633b1b798d2dc71a088940777c61653cec6ff050fb9d45` | `6cdb53d5d7b8de80d60b298b1357f462cedbedfae261d5ba60b08ccc401687c5` | Prioritizing yes_no confirmation and strict parallel boundaries | 0.80 | 1.00 | [v2_B_base_openrouter_20260602T144917459487.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/runs/v2_B_base_openrouter_20260602T144917459487.json) |
| v3 | [system_prompt.md](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/artifacts/system_prompt.md), [tools.yaml](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/artifacts/tools.yaml) | `f22c0d93361864f12bc25dfc6676c705f275043264b0e28ee0e4002ada743fa7` | `9853ee135a7c6f858a5b51a5959a376b114e780fa878f9ce1b19356346873a81` | Integrating github_search tool and routing protocols to support GitHub repository search requests | 1.00 | 1.00 | [v3_B_base_openrouter_20260602T173214234618.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/runs/v3_B_base_openrouter_20260602T173214234618.json) |

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| [R12_confirm_before_send](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_base.json#L95-L101) | `wrong_boundary` | `clarify(question="Bạn có thể cung cấp nội dung cụ thể...", response_type="text")` | Model ưu tiên hỏi xin nội dung còn thiếu thay vì hỏi xác nhận `yes_no` trước hành động nhạy cảm (send). | Bổ sung quy tắc độ ưu tiên xác nhận (Priority Confirmation Rule) yêu cầu hỏi `yes_no` ngay lập tức. |
| [M01_clarify_then_fill](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_base.json#L122-L132) | `missing_info` | `timeline(screenname="elonmusk", limit=5)` và `social_search(query="Elon Musk", ...)` | Trong hội thoại nhiều lượt, model tự động kích hoạt song song 2 công cụ tìm kiếm khi xác định được tên đối tượng. | Bổ sung quy tắc Parallel Execution: chỉ kích hoạt song song khi có yêu cầu rõ ràng; phân định rõ timeline (by user) vs social_search (about topic). |
| [M02_carryover_timeframe](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_base.json#L134-L144) | `wrong_arg_value` | `lookup(query="robotics", ...)` và `social_search(query="robotics", ...)` | Kế thừa tham số cũ từ lượt trước gây nhầm lẫn nền tảng và gọi cả Web Search lẫn Twitter Search song song. | Giới hạn việc gọi song song; phân định chặt chẽ từ khóa tìm kiếm theo nền tảng tương ứng. |
| [M06_switch_tool](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_base.json#L182-L192) | `wrong_tool` | `lookup(query="OpenAI", ...)` và `social_search(query="OpenAI", ...)` | Model tiếp tục gọi công cụ từ nền tảng cũ ở lượt sau mặc dù người dùng đã yêu cầu bỏ nền tảng cũ (Twitter) ở lượt trước. | Bổ sung quy tắc chuyển đổi công cụ nghiêm ngặt (Strict Tool Switching Rule) trong system prompt để vô hiệu hóa hoàn toàn công cụ cũ. |

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| [G01_user_tweets_handle_map](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L15-L36) | Ánh xạ tên thường sang Twitter handle và lấy 5 tweet. | `timeline(screenname="karpathy", limit=5)` | PASS |
| [G02_search_tweets_latest](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L37-L59) | Tìm tweet 'mới nhất' (Latest) về một chủ đề. | `social_search(query="Gemini AI", search_type="Latest")` | PASS |
| [G03_read_url_no_search](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L60-L81) | Tìm thấy link cụ thể thì gọi fetch trực tiếp chứ không tìm kiếm. | `fetch(url="https://deepmind.google/technologies/gemini/")` | PASS |
| [G04_out_of_scope_weather](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L82-L97) | Nhận diện câu hỏi thời tiết ngoài phạm vi và từ chối. | `no_tool=true`, từ chối/hướng dẫn lại | PASS |
| [G05_parallel_user_and_search](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L98-L125) | Gọi đồng thời timeline của một người và search tweet về một chủ đề khác. | `timeline(screenname="ylecun", limit=5)` & `social_search(query="AI safety", search_type="Top", limit=5)` | PASS |
| [G06_multiturn_missing_topic](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L126-L162) | Kế thừa timeframe, bổ sung query dần dần và hoàn thành qua nhiều lượt. | `lookup(query="blockchain", topic="news", timeframe="month")` | PASS |
| [G07_multiturn_correction_person](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L163-L198) | Nhầm đối tượng và sửa đổi sang người khác, lấy 7 tweet. | `timeline(screenname="sundarpichai", limit=7)` | PASS |
| [G08_multiturn_carryover_search_type](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L199-L234) | Kế thừa search_type=Top từ lượt 1, chỉ sửa query ở các lượt sau. | `social_search(query="Claude AI", search_type="Top")` | PASS |
| [G09_multiturn_clarify_url_then_fetch](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L235-L269) | Lượt 1 thiếu URL, lượt 2 cung cấp URL, lượt 3 xác nhận và đọc đúng link. | `fetch(url="https://techcrunch.com/2025/01/ai-agents")` | PASS |
| [G10_multiturn_switch_to_twitter](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/data/eval_group.json#L270-L305) | Chuyển đổi nền tảng từ web sang Twitter, giữ nguyên chủ đề và lấy Top tweet. | `social_search(query="Meta AI", search_type="Top")` | PASS |

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| Turn 1 (v2) | "Cho mình xem repository crewai nổi bật nhất trên GitHub" | `github_search(query="crewai", sort_by="stars", limit=5)` | [v2_openrouter_20260602T150401735696.transcript.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/transcripts/v2_openrouter_20260602T150401735696.transcript.json#L19-L82) | Gọi công cụ `github_search` chính xác với các đối số và xuất danh sách các repo CrewAI nổi bật định dạng markdown đẹp mắt. |
| Turn 1 (v0) | "Cho tôi xem repo có số sao nhiều nhất trên github" | `github_search(query="", sort_by="stars", limit=5)` | [v0_openrouter_20260602T165455235381.transcript.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/transcripts/v0_openrouter_20260602T165455235381.transcript.json#L19-L83) | Gọi đúng tool `github_search` với truy vấn trống để fallback tìm các repo nhiều sao nhất chung. |
| Turn 3 (v0) | "Tìm tài liệu về \"Stabe Diffusion\" trên arxiv" | `papers(query="Stable Diffusion", max_results=5)` | [v0_openrouter_20260602T165455235381.transcript.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/transcripts/v0_openrouter_20260602T165455235381.transcript.json#L365-L522) | Kích hoạt công cụ `papers` tìm kiếm các bài báo arXiv liên quan đến Stable Diffusion và hiển thị PDF link, tác giả. |
| Turn 4 (v0) | "Summary this link http://arxiv.org/abs/2302.04304v3" | `fetch(url="http://arxiv.org/abs/2302.04304v3")` | [v0_openrouter_20260602T165455235381.transcript.json](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/transcripts/v0_openrouter_20260602T165455235381.transcript.json#L676-L738) | Nhận diện link cụ thể và gọi đúng tool `fetch` thay vì gọi tìm kiếm, tóm tắt chính xác nội dung bài báo Q-Diffusion. |

## B5. Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | [tool.py](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/tools/send/tool.py) | Gửi thành công nội dung bản tin lên Telegram channel qua bot API (`sendMessage`) khi có cờ `confirmed=True`. | Nguy cơ spam/rò rỉ dữ liệu. Đã chặn bằng cơ chế bắt buộc xác nhận từ người dùng qua `clarify(response_type='yes_no')` trước khi gọi `send`. |
| arXiv/company policy | [policy/tool.py](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/tools/policy/tool.py), [papers/tool.py](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/tools/papers/tool.py), [paper_text/tool.py](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/tools/paper_text/tool.py) | Đọc và tìm kiếm tài liệu khoa học trên arXiv, tải và trích xuất PDF văn bản thô. Tra cứu tài liệu quy định nội bộ công ty hiệu quả. | Nguy cơ dính instruction injection trong tài liệu. Đã chặn bằng cách lọc bỏ các dòng văn bản chứa marker nguy hiểm (`suspicious_markers` như `ignore`, `bỏ qua`, `trợ lý`) trong `_split_trusted_facts` của policy tool. |
| UI | [app.py](file:///f:/AI%20thuc%20chien/git/Day04-C401-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/app.py) | Giao diện hiện đại tùy biến CSS đẹp mắt (gradient, font chữ Outfit/Space Grotesk, bubble chat bo góc), hộp thoại hiển thị các vòng công cụ (tool runs) thu gọn và form làm rõ (clarification card) sinh động. | Người dùng gửi input gây lỗi UI. Đã xử lý bằng cách sử dụng các component chuẩn Streamlit, vô hiệu hóa khung chat khi đang chờ phản hồi làm rõ. |

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**
  - Các chỉnh sửa liên quan đến tư duy, quy tắc nghiệp vụ và điều kiện biên: ánh xạ tên sang Twitter handle, quy định Platform Mapping để chọn đúng tool cho từng nền tảng, quy tắc yêu cầu làm rõ (Clarification Protocol) khi thiếu thông tin, quy tắc xác nhận ghi dữ liệu (Priority Confirmation Rule) và ranh giới từ chối câu hỏi ngoài phạm vi (Out-of-Scope). Bổ sung quy tắc Parallel Execution boundaries và quy tắc chuyển đổi công cụ nghiêm ngặt (Strict Tool Switching Rule).
- **Which fixes belonged in `tools.yaml`?**
  - Các định nghĩa về mô tả công cụ, tham số và kiểu dữ liệu: mô tả rõ ràng mục đích của `clarify` và tham số `response_type`, cấu hình enum giới hạn cho `search_type` (`Latest`, `Top`) và `timeframe` (`day`, `week`, `month`, `year`) để mô hình không truyền các đối số tùy tiện, và cấu trúc định nghĩa cho công cụ mới `github_search`.
- **Which failure needed manual review instead of automatic grading?**
  - Các ca kiểm thử liên quan đến chất lượng nội dung văn bản từ chối của mô hình (Refusal text quality) như `R08` (toán tích phân) và `R14` ( Fibonacci python) hay câu hỏi meta `R09`. Quá trình chấm tự động chỉ kiểm tra cờ `no_tool` và trường `behavior: refuse`/`answer_without_tool`, nhưng việc kiểm tra tính thân thiện, định hướng chính xác và lịch sự của câu trả lời thô (`actual_text`) đòi hỏi phải có sự đánh giá thủ công của con người.
- **What would you improve next?**
  - Tích hợp thêm các giải pháp kiểm duyệt an toàn (Guardrails) như Llama Guard để tự động quét và chặn các prompt tấn công injection ẩn trong nội dung bài báo khoa học hoặc trang web được tải về.
  - Cải tiến thuật toán tìm kiếm policy bằng kỹ thuật Hybrid Search (Vector Database + BM25) thay vì chỉ đối chiếu tập từ khóa `query_terms` thủ công để nâng cao độ chính xác khi truy vấn.
  - Quản lý hội thoại dài thông qua cơ chế Summary Memory thay vì chỉ sử dụng cửa sổ cố định `history_window`.

# Retrieval test — Task 4 Step 2 (sau slim SKILL.md)

Method: mỗi rep = 1 single-shot subagent, chỉ được đọc SKILL.md (không đọc file khác trong skill dir), hỏi về render argv + detect shell. CẢ PHẢI trả lời đúng 3 dòng: pattern cụ thể, file chi tiết, câu trích dẫn dẫn về file đó.

## Rep 1 — passed
1. Chạy `python scripts/shell_detect.py --json` (read-only, advisory) để xác định shell trước khi render argv; render dùng argument arrays + quoting đúng shell.
2. File chi tiết: `references/universal-shell.md`.
3. Trích: "The full details — cross-platform command rendering and optimization, the hybrid selection order (agent-native tools → project automation → API/MCP/SDK → CLI → helper scripts), helper script usage (`shell_detect.py`, `command_optimize.py`, `command_validate.py`), per-agent adapter notes (`adapters/`), and related playbooks — live in `references/universal-shell.md`."

## Rep 2 — passed
1. Chạy `python scripts/shell_detect.py --json` (read-only) để biết shell của user trước, rồi render argv theo shell đó — phần render chi tiết do `command_optimize.py` xử lý, tất cả nằm trong tài liệu tham chiếu universal-shell.
2. File chứa chi tiết đầy đủ: `references/universal-shell.md`.
3. Trích (trích cùng câu trên, chỉ dòng 157).

## Rep 3 — passed
1. Dùng `python scripts/shell_detect.py --json` — lệnh chỉ-đọc, advisory, để xác định shell của user khi môi trường chưa biết; khi render thì dùng argument arrays/structured tool parameters và quote đúng syntax cho shell đang hoạt động.
2. File chi tiết đầy đủ: `references/universal-shell.md`.
3. Trích: cùng câu "The full details — ... live in `references/universal-shell.md`."

Kết quả: 3/3 dẫn về đúng file; câu dẫn trong SKILL.md liệt kê đủ 3 helper scripts và adapters nên agent tìm được cả khi chỉ đọc SKILL.md.

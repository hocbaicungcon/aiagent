"""Sinh sơ đồ SVG nhúng trong bài viết. Màu và kiểu chữ nằm trong dist/assets/article.css (lớp .dg).

Trong content/*.html chèn `{{fig:ten-so-do|Chú thích}}`; build.py thay bằng <figure>.
"""
from html import escape as e

W = 560


def svg(name, label, h, inner):
    return (
        f'<svg class="dg" viewBox="0 0 {W} {h}" role="img" aria-label="{e(label)}" xmlns="http://www.w3.org/2000/svg">'
        f'<defs><marker id="ah-{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M1 1L9 5L1 9z" class="ahead"/></marker></defs>{inner}</svg>'
    )


def text(x, y, s, cls="t", anchor="middle"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{e(s)}</text>'


def box(x, y, w, h, title, subs=(), kind=""):
    n = 1 + len(subs)
    top = y + h / 2 - (n * 19) / 2 + 14
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="box {kind}"/>'
    out += text(x + w / 2, round(top, 1), title, "t " + kind)
    for i, s in enumerate(subs):
        out += text(x + w / 2, round(top + 19 * (i + 1) - 2, 1), s, "s " + kind)
    return out


def arrow(name, pts, dashed=False):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return f'<path d="{d}" class="arr{" dash" if dashed else ""}" marker-end="url(#ah-{name})"/>'


def vflow(name, label, steps, numbered="n", accent=(), loop=None):
    bw, bh, gap, x = 470, 62, 26, 20
    inner, ys = "", []
    for i, (title, sub) in enumerate(steps):
        y = 12 + i * (bh + gap)
        ys.append(y)
        kind = "a" if i in accent else ""
        inner += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" class="box {kind}"/>'
        tag = f"{i + 1}" if numbered == "n" else numbered[i]
        inner += f'<circle cx="{x + 32}" cy="{y + bh / 2}" r="17" class="dot {kind}"/>'
        inner += text(x + 32, y + bh / 2 + 5, tag, "t num " + kind)
        inner += text(x + 66, y + 27, title, "t " + kind, "start")
        inner += text(x + 66, y + 47, sub, "s " + kind, "start")
        if i:
            inner += arrow(name, [(x + bw / 2, y - gap + 2), (x + bw / 2, y - 3)])
    if loop:
        a, b = loop  # từ bước a quay lại bước b
        ya, yb = ys[a] + bh / 2, ys[b] + bh / 2
        inner += arrow(name, [(x + bw, ya), (x + bw + 34, ya), (x + bw + 34, yb), (x + bw + 2, yb)], dashed=True)
        inner += f'<text transform="translate({x + bw + 50} {(ya + yb) / 2}) rotate(-90)" class="s" text-anchor="middle">lặp lại</text>'
    return svg(name, label, 12 + len(steps) * (bh + gap) - gap + 12, inner)


def cycle4(name, label, items, center):
    pos = [(30, 20), (300, 20), (300, 150), (30, 150)]
    inner = ""
    for i, ((t, subs), (x, y)) in enumerate(zip(items, pos)):
        inner += box(x, y, 230, 72, f"{i + 1}. {t}", subs, "a" if i == 0 else "")
    inner += arrow(name, [(262, 56), (298, 56)])
    inner += arrow(name, [(415, 94), (415, 148)])
    inner += arrow(name, [(298, 186), (262, 186)])
    inner += arrow(name, [(145, 148), (145, 94)])
    inner += text(280, 126, center, "s")
    return svg(name, label, 240, inner)


def f_vong_lap():
    return cycle4(
        "vong-lap",
        "Vòng lặp của AI Agent: quan sát, lập kế hoạch, hành động, đánh giá",
        [("Quan sát", ["Nhận mục tiêu và ngữ cảnh"]), ("Lập kế hoạch", ["Chọn bước tiếp theo"]),
         ("Hành động", ["Gọi công cụ, đọc, ghi"]), ("Đánh giá", ["Đã đạt mục tiêu chưa?"])],
        "lặp lại đến khi xong",
    )


def f_chatbot_agent():
    n = "chatbot-agent"
    inner = text(140, 26, "Chatbot", "t") + text(420, 26, "AI Agent", "t")
    inner += box(30, 44, 220, 52, "Bạn hỏi", ["một câu"]) + arrow(n, [(140, 98), (140, 120)])
    inner += box(30, 122, 220, 52, "AI trả lời", ["bằng văn bản"], "b")
    steps = [("Bạn giao mục tiêu", []), ("Agent lập kế hoạch", []), ("Dùng công cụ, kiểm tra", []), ("Công việc hoàn thành", [])]
    ys = [44, 106, 168, 230]
    for i, ((t, s), y) in enumerate(zip(steps, ys)):
        inner += box(310, y, 220, 44, t, s, "a" if i == 3 else "")
        if i:
            inner += arrow(n, [(420, y - 16), (420, y - 1)])
    inner += arrow(n, [(530, 190), (548, 190), (548, 128), (532, 128)], dashed=True)
    inner += text(140, 214, "chatbot nói", "s") + text(140, 232, "agent làm", "t")
    return svg(n, "So sánh chatbot chỉ trả lời với AI Agent tự thực hiện nhiều bước", 290, inner)


def f_mcp_kien_truc():
    n = "mcp-kien-truc"
    inner = box(15, 24, 150, 96, "Ứng dụng AI", ["trợ lý, agent,", "trình soạn code"], "a")
    inner += box(205, 24, 150, 96, "Máy chủ MCP", ["mô tả công cụ", "theo chuẩn chung"], "b")
    inner += box(395, 24, 150, 96, "Công cụ, dữ liệu", ["Drive, CSDL,", "CRM, email"])
    for x1, x2 in ((167, 203), (357, 393)):
        inner += f'<path d="M{x1} 72 L{x2} 72" class="arr" marker-start="url(#ah-{n})" marker-end="url(#ah-{n})"/>'
    inner += text(280, 150, "máy chủ cung cấp 3 loại thứ:", "s")
    for i, t in enumerate(["Công cụ (tools)", "Tài nguyên (resources)", "Mẫu chỉ dẫn (prompts)"]):
        x = 15 + i * 183
        inner += f'<rect x="{x}" y="164" width="170" height="34" rx="17" class="pill"/>' + text(x + 85, 186, t, "s")
    return svg(n, "Kiến trúc MCP: ứng dụng AI kết nối máy chủ MCP rồi tới công cụ và dữ liệu", 212, inner)


def f_mcp_mxn():
    n = "mcp-mxn"
    inner = text(140, 22, "Không có chuẩn: 3 × 3 = 9 kết nối", "t") + text(420, 22, "Có MCP: 3 + 3 = 6 kết nối", "t")
    ys = [60, 120, 180]
    for x in (30, 250):
        for y in ys:
            inner += f'<circle cx="{x}" cy="{y}" r="12" class="dot"/>'
    for ya in ys:
        for yb in ys:
            inner += f'<path d="M42 {ya} L238 {yb}" class="thin"/>'
    inner += text(18, 214, "ứng dụng AI", "s", "start") + text(262, 214, "công cụ", "s", "end")
    for y in ys:
        inner += f'<circle cx="310" cy="{y}" r="12" class="dot"/><circle cx="530" cy="{y}" r="12" class="dot"/>'
        inner += f'<path d="M322 {y} L405 120" class="thin"/><path d="M518 {y} L435 120" class="thin"/>'
    inner += f'<rect x="395" y="96" width="50" height="48" rx="12" class="box a"/>' + text(420, 125, "MCP", "t a")
    inner += text(298, 214, "ứng dụng AI", "s", "start") + text(542, 214, "công cụ", "s", "end")
    return svg(n, "So sánh 9 kết nối riêng lẻ với 6 kết nối khi dùng chuẩn MCP chung", 232, inner)


def f_luong_tu_dong():
    n = "luong-tu-dong"
    steps = [("Kích hoạt", "Email mới, tệp tải lên, đến giờ hẹn"), ("Chuẩn bị dữ liệu", "Lấy nội dung, làm sạch, ẩn thông tin nhạy cảm"),
             ("Xử lý bởi AI Agent", "Phân loại, trích xuất, soạn nháp"), ("Kiểm tra bằng quy tắc cứng", "Đúng định dạng, thuộc danh sách cho phép"),
             ("Hành động", "Ghi hệ thống, gửi thông báo, tạo công việc")]
    inner = ""
    bw, bh, gap, x = 350, 62, 26, 20
    for i, (t, s) in enumerate(steps):
        y = 12 + i * (bh + gap)
        k = "a" if i == 2 else ""
        inner += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" class="box {k}"/>'
        inner += f'<circle cx="{x + 32}" cy="{y + 31}" r="17" class="dot {k}"/>' + text(x + 32, y + 36, str(i + 1), "t num " + k)
        inner += text(x + 66, y + 27, t, "t " + k, "start") + text(x + 66, y + 47, s, "s " + k, "start")
        if i:
            inner += arrow(n, [(x + bw / 2, y - gap + 2), (x + bw / 2, y - 3)])
    y4 = 12 + 3 * (bh + gap)
    inner += box(400, y4 - 4, 150, 70, "Người duyệt", ["ca không", "chắc chắn"], "b")
    inner += arrow(n, [(x + bw + 2, y4 + 31), (398, y4 + 31)], dashed=True)
    return svg(n, "Luồng tự động hóa năm khối, có người duyệt ở bước kiểm tra", 12 + 5 * (bh + gap) - gap + 12, inner)


def f_luong_email():
    n = "luong-email"
    inner = box(150, 10, 260, 54, "Email mới đến", ["lấy tiêu đề và nội dung"])
    inner += arrow(n, [(280, 66), (280, 90)])
    inner += box(110, 92, 340, 66, "AI Agent phân loại", ["trả về JSON: nhãn, lý do, độ chắc chắn"], "a")
    inner += arrow(n, [(280, 160), (280, 184)])
    inner += box(110, 186, 340, 54, "Kiểm tra bằng quy tắc cứng", ["JSON hợp lệ? nhãn trong danh sách?"], "b")
    inner += arrow(n, [(200, 242), (200, 282), (140, 282), (140, 292)])
    inner += arrow(n, [(360, 242), (360, 282), (420, 282), (420, 292)])
    inner += box(30, 294, 220, 54, "Gắn nhãn tự động", ["đạt kiểm tra, chắc chắn"])
    inner += box(310, 294, 220, 54, "Chuyển người xem", ["lỗi hoặc không chắc chắn"], "b")
    inner += text(120, 270, "đạt", "s") + text(440, 270, "không đạt", "s")
    return svg(n, "Luồng agent phân loại email: phân loại, kiểm tra, rồi gắn nhãn hoặc chuyển cho người xem", 362, inner)


def f_bay_buoc():
    return vflow(
        "bay-buoc", "Bảy bước tạo AI Agent đầu tiên",
        [("Chọn một mục tiêu cụ thể", "Lặp lại, kiểm tra được, rủi ro thấp"), ("Mô tả quy trình bằng tay", "Ghi từng bước và các ngoại lệ"),
         ("Liệt kê công cụ vừa đủ", "Quyền tối thiểu cho mỗi công cụ"), ("Viết chỉ dẫn rõ ràng", "Vai trò, quy tắc, định dạng đầu ra"),
         ("Đặt giới hạn và điểm dừng", "Số bước, chi phí, người duyệt"), ("Thử với dữ liệu mẫu", "Đếm tỷ lệ đúng, xem các ca sai"),
         ("Chạy song song có giám sát", "Agent đề xuất, người quyết định")],
        accent={5}, loop=(5, 3),
    )


def f_cay_quyet_dinh():
    n = "cay-quyet-dinh"
    inner = ""
    qs = [(20, "Việc lặp lại thường xuyên?"), (130, "Dữ liệu có cấu trúc, quy tắc rõ?"), (240, "Sai một lần có hậu quả nặng?")]
    for y, q in qs:
        inner += box(20, y, 290, 60, q, [], "b")
    inner += arrow(n, [(165, 82), (165, 128)]) + text(180, 110, "Có", "s", "start")
    inner += arrow(n, [(165, 192), (165, 238)]) + text(180, 220, "Không", "s", "start")
    inner += arrow(n, [(165, 302), (165, 338)]) + text(180, 326, "Không", "s", "start")
    inner += box(20, 340, 290, 52, "AI Agent, có kiểm tra", ["và người duyệt khi cần"], "a")
    for (y, q), lab, out in zip(qs, ["Không", "Có", "Có"], [["Làm tay,", "chưa đáng tự động hóa"], ["Automation", "thông thường"], ["AI chỉ hỗ trợ,", "người quyết định"]]):
        inner += arrow(n, [(312, y + 30), (378, y + 30)]) + text(345, y + 22, lab, "s")
        inner += box(380, y - 6, 170, 72, out[0], [out[1]])
    return svg(n, "Cây quyết định khi nào nên dùng AI Agent", 410, inner)


def f_pho_cong_cu():
    n = "pho-cong-cu"
    inner = '<rect x="30" y="52" width="500" height="10" rx="5" class="bar"/>'
    inner += text(30, 30, "Dễ và nhanh", "s", "start") + text(530, 30, "Linh hoạt, kiểm soát cao", "s", "end")
    cards = [("Agent dựng sẵn", ["dùng ngay", "ít tùy biến"]), ("No-code, low-code", ["dựng trong vài giờ", "có sẵn kết nối"]), ("Framework, SDK", ["tùy biến sâu", "cần kỹ năng"])]
    for i, (t, s) in enumerate(cards):
        x = 15 + i * 183
        cx = x + 85
        inner += f'<circle cx="{cx}" cy="57" r="9" class="dot a"/>' + arrow(n, [(cx, 70), (cx, 96)])
        inner += box(x, 98, 170, 80, t, s, "a" if i == 1 else "")
    return svg(n, "Phổ công cụ xây AI Agent từ dễ nhanh đến linh hoạt kiểm soát cao", 196, inner)


def f_json():
    n = "json-cau-truc"
    inner = text(135, 24, "Prompt thường", "t") + text(425, 24, "JSON prompt", "t")
    inner += '<rect x="20" y="40" width="230" height="150" rx="14" class="box"/>'
    for i, wd in enumerate([190, 200, 170, 195, 180, 120]):
        inner += f'<rect x="35" y="{58 + i * 22}" width="{wd}" height="9" rx="4.5" class="bar"/>'
    inner += arrow(n, [(254, 115), (296, 115)])
    inner += '<rect x="300" y="40" width="240" height="150" rx="14" class="box b"/>'
    for i, k in enumerate(['{', '  "vai_tro": "...",', '  "nhiem_vu": "...",', '  "rang_buoc": [...],', '  "dinh_dang": "..."', '}']):
        inner += text(316, 64 + i * 22, k, "mono", "start")
    inner += text(135, 212, "một đoạn văn dài", "s") + text(420, 212, "mỗi yếu tố một khóa riêng", "s")
    return svg(n, "So sánh prompt viết thành đoạn văn với JSON prompt chia theo khóa", 226, inner)


def f_vong_phan_bien():
    return cycle4(
        "vong-phan-bien", "Vòng làm việc với AI phản biện: ý tưởng, phản biện, chỉnh sửa, kiểm chứng",
        [("Ý tưởng của bạn", ["kế hoạch, lập luận"]), ("AI phản biện", ["dùng 1 trong 9 prompt"]),
         ("Bạn chỉnh sửa", ["vá điểm yếu tìm được"]), ("Kiểm chứng", ["đối chiếu nguồn gốc"])],
        "quyết định cuối cùng là của bạn",
    )


def f_gamma():
    return vflow(
        "gamma", "Năm bước tạo bài thuyết trình bằng Gamma",
        [("Chuẩn bị nội dung", "Mục đích, người nghe, thông điệp, số liệu thật"), ("Chọn cách tạo", "Từ mô tả, dán văn bản hoặc nhập tệp"),
         ("Viết mô tả rõ ràng", "Ngôn ngữ, số slide, giọng điệu, cấu trúc"), ("Rà soát và chỉnh sửa", "Dàn ý, số liệu, hình ảnh, giao diện"),
         ("Chia sẻ hoặc xuất bài", "Liên kết, PDF, PowerPoint")],
        accent={3},
    )


def f_phuc_che():
    return vflow(
        "phuc-che", "Quy trình phục chế ảnh cũ từng bước nhỏ",
        [("Chuẩn bị ảnh gốc", "Quét chất lượng cao, giữ bản gốc"), ("Phục hồi cơ bản", "Xóa xước, khử ố, giữ nguyên gương mặt"),
         ("So sánh với ảnh gốc", "Gương mặt, tay, chi tiết nền"), ("Làm nét hoặc tô màu", "Mỗi lần một thay đổi nhỏ"),
         ("Lưu các phiên bản", "Giữ cả bản gốc và bản phục chế")],
        accent={2}, loop=(2, 1),
    )


def f_lo_trinh():
    return vflow(
        "lo-trinh", "Lộ trình tự học AI sáu tuần",
        [("Hiểu nền tảng", "AI, mô hình ngôn ngữ, giới hạn"), ("Dùng thành thạo trợ lý AI", "Đưa AI vào việc hằng ngày"),
         ("Viết prompt hiệu quả", "Cấu trúc, ví dụ, thư viện prompt"), ("Công cụ AI chuyên biệt", "Slide, ảnh, so sánh công cụ"),
         ("Tự động hóa một quy trình", "Dựng agent nhỏ có người duyệt"), ("Dự án cuối và đánh giá", "Đo hiệu quả, chọn việc kế tiếp")],
        numbered=["T1", "T2", "T3", "T4", "T5", "T6"], accent={5},
    )


def f_plus_api():
    n = "plus-api"
    inner = text(140, 22, "ChatGPT Plus", "t") + text(420, 22, "ChatGPT API", "t")
    left = [("Bạn", ["dùng trực tiếp"], ""), ("Ứng dụng trò chuyện", ["web, điện thoại"], "b"), ("Thuê bao cố định", ["trả theo tháng"], "a")]
    right = [("Phần mềm của bạn", ["website, quy trình, agent"], ""), ("API", ["gọi mô hình từ mã hoặc công cụ"], "b"), ("Trả theo lượng dùng", ["tính theo token vào và ra"], "a")]
    for col, items in ((20, left), (300, right)):
        for i, (t, sb, k) in enumerate(items):
            y = 40 + i * 84
            inner += box(col, y, 240, 58, t, sb, k)
            if i:
                inner += arrow(n, [(col + 120, y - 24), (col + 120, y - 2)])
    return svg(n, "ChatGPT Plus thuê bao cố định so với ChatGPT API trả theo lượng dùng", 280, inner)


def f_vong_cai_thien():
    return cycle4(
        "vong-cai-thien", "Vòng cải thiện prompt: viết, chạy bộ kiểm thử, xem ca sai, chỉnh một yếu tố",
        [("Viết prompt", ["theo cấu trúc rõ ràng"]), ("Chạy bộ kiểm thử", ["20 đến 50 ví dụ có đáp án"]),
         ("Xem các ca sai", ["thiếu chỉ dẫn hay ví dụ?"]), ("Chỉnh một yếu tố", ["rồi đo lại"])],
        "mỗi lần chỉ đổi một thứ",
    )


def f_nhom_slide():
    n = "nhom-slide"
    cols = [("Tích hợp sẵn", ["Copilot (PowerPoint)", "Gemini (Slides)", "Canva"], "b"),
            ("Chuyên biệt", ["Gamma", "Beautiful.ai", "Pitch", "Prezi", "Visme"], "a"),
            ("Tiện ích thêm", ["SlidesAI", "Plus AI", "Decktopus"], "b")]
    inner = ""
    for i, (t, subs, k) in enumerate(cols):
        x = 10 + i * 185
        inner += box(x, 14, 170, 150, t, subs, k)
    inner += text(95, 190, "3 công cụ", "s") + text(280, 190, "5 công cụ", "s") + text(465, 190, "3 công cụ", "s")
    return svg(n, "11 ứng dụng AI làm PowerPoint chia thành ba nhóm", 204, inner)


def cam(x, y, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot})"><rect x="-11" y="-7" width="22" height="14" rx="3" class="dot a"/>'
            f'<path d="M11 -4 L20 -9 L20 9 L11 4z" class="dot a"/></g>')


def f_camera():
    n = "camera"
    panels = [(15, 10), (285, 10), (15, 146), (285, 146)]
    labels = ["Pan: xoay ngang tại chỗ", "Dolly: tiến lại gần chủ thể", "Orbit: quay quanh chủ thể", "Crane: nâng lên theo chiều dọc"]
    inner = ""
    for (x, y), lab in zip(panels, labels):
        inner += f'<rect x="{x}" y="{y}" width="260" height="122" rx="14" class="box b"/>' + text(x + 130, y + 110, lab, "s")
    x, y = panels[0]
    inner += cam(x + 70, y + 52) + f'<path d="M{x+110} {y+30} Q{x+160} {y+8} {x+205} {y+30}" class="arr" marker-end="url(#ah-{n})"/>'
    inner += f'<path d="M{x+110} {y+52} L{x+205} {y+52}" class="thin"/>'
    x, y = panels[1]
    inner += cam(x + 44, y + 52) + arrow(n, [(x + 76, y + 52), (x + 150, y + 52)]) + f'<circle cx="{x+205}" cy="{y+52}" r="15" class="dot"/>'
    x, y = panels[2]
    inner += f'<circle cx="{x+130}" cy="{y+52}" r="40" class="thin" stroke-dasharray="5 5"/><circle cx="{x+130}" cy="{y+52}" r="13" class="dot"/>'
    inner += cam(x + 170, y + 52, 90) + f'<path d="M{x+177} {y+70} Q{x+160} {y+88} {x+134} {y+92}" class="arr" marker-end="url(#ah-{n})"/>'
    x, y = panels[3]
    inner += cam(x + 70, y + 86) + arrow(n, [(x + 70, y + 70), (x + 70, y + 20)]) + f'<circle cx="{x+190}" cy="{y+52}" r="15" class="dot"/>'
    return svg(n, "Bốn chuyển động camera cơ bản nhìn từ trên xuống: pan, dolly, orbit, crane", 284, inner)


def f_nhom_phong_cach():
    n = "nhom-phong-cach"
    groups = [("Ảnh chụp, điện ảnh", "phong cách 1 đến 10", ""), ("Hoạt hình, minh họa", "phong cách 11 đến 20", "b"),
              ("Hội họa, nghệ thuật", "phong cách 21 đến 30", "b"), ("Đồ họa, thiết kế", "phong cách 31 đến 40", ""),
              ("3D, sáng tạo", "phong cách 41 đến 50", "a")]
    pos = [(15, 14), (285, 14), (15, 100), (285, 100), (150, 186)]
    inner = ""
    for (t, sb, k), (x, y) in zip(groups, pos):
        inner += box(x, y, 260, 70, t, [sb], k)
    return svg(n, "50 phong cách tạo hình chia thành năm nhóm, mỗi nhóm mười phong cách", 270, inner)


def f_text_to_cad():
    return vflow(
        "text-to-cad", "Quy trình từ mô tả bằng chữ đến mô hình CAD",
        [("Mô tả bằng chữ", "Kích thước, hình dạng, ràng buộc"), ("AI sinh mã tham số", "OpenSCAD, CadQuery hoặc tập lệnh CAD"),
         ("Chạy mã dựng mô hình", "Ra bản 3D có thể chỉnh sửa"), ("Kiểm tra kích thước", "So với yêu cầu, đo thử"),
         ("Xuất tệp sản xuất", "STL, STEP cho in 3D hoặc gia công")],
        accent={1}, loop=(3, 0),
    )


FIGS = {
    "vong-lap": f_vong_lap, "chatbot-agent": f_chatbot_agent, "mcp-kien-truc": f_mcp_kien_truc, "mcp-mxn": f_mcp_mxn,
    "luong-tu-dong": f_luong_tu_dong, "luong-email": f_luong_email, "bay-buoc": f_bay_buoc, "cay-quyet-dinh": f_cay_quyet_dinh,
    "pho-cong-cu": f_pho_cong_cu, "json-cau-truc": f_json, "vong-phan-bien": f_vong_phan_bien, "gamma": f_gamma,
    "phuc-che": f_phuc_che, "lo-trinh": f_lo_trinh,
    "plus-api": f_plus_api, "vong-cai-thien": f_vong_cai_thien, "nhom-slide": f_nhom_slide, "camera": f_camera,
    "nhom-phong-cach": f_nhom_phong_cach, "text-to-cad": f_text_to_cad,
}

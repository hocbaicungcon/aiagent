# aiagent.vn

Landing page tiếng Việt về AI Agent. Website tĩnh nằm trong `dist/` và được xuất bản bằng GitHub Pages.

## Triển khai lên GitHub Pages

1. Tạo một repository GitHub (ví dụ `aiagent`) trong tài khoản của bạn. Không cần chọn README hoặc template khi tạo vì thư mục này đã có mã nguồn.
2. Tại thư mục dự án, kết nối và đẩy mã nguồn lên GitHub:

   ```bash
   git remote add origin https://github.com/<TEN_TAI_KHOAN>/aiagent.git
   git add README.md .gitignore .github/workflows/pages.yml dist/index.html
   git commit -m "Deploy aiagent.vn with GitHub Pages"
   git push -u origin main
   ```

   Nếu repository đã có remote `origin`, dùng `git remote set-url origin ...` thay cho `git remote add origin ...`.
3. Trong GitHub: **Settings → Pages → Build and deployment → Source → GitHub Actions**. Mở tab **Actions** và đợi workflow **Deploy GitHub Pages** chạy thành công. Trang sẽ có địa chỉ tạm `https://<TEN_TAI_KHOAN>.github.io/aiagent/`.
4. Trong **Settings → Pages → Custom domain**, nhập `aiagent.vn` và lưu. GitHub sẽ bắt đầu kiểm tra DNS. Khi tùy chọn xuất hiện, bật **Enforce HTTPS**.

## Cấu hình DNS tại Nhân Hòa

Trong vùng DNS thực sự đang quản lý `aiagent.vn`, tạo bốn bản ghi `A` cho tên `@`:

| Loại | Tên | Giá trị |
| --- | --- | --- |
| A | @ | `185.199.108.153` |
| A | @ | `185.199.109.153` |
| A | @ | `185.199.110.153` |
| A | @ | `185.199.111.153` |

Xóa các bản ghi `A`/`AAAA` cũ ở `@` trỏ tới dịch vụ web khác nếu có. Giữ nguyên các bản ghi email (`MX`, SPF, DKIM, DMARC) và những bản ghi không liên quan. Có thể thêm bốn bản ghi `AAAA` theo [tài liệu GitHub](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) nếu cần IPv6.

Nếu muốn `www.aiagent.vn` cũng hoạt động, tạo `CNAME` tên `www` trỏ tới `<TEN_TAI_KHOAN>.github.io` (thay bằng tên tài khoản hoặc tổ chức sở hữu repository). GitHub sẽ chuyển hướng giữa `www` và tên miền gốc khi cấu hình đúng.

> `CNAME` trong mã nguồn không cần thiết khi xuất bản bằng GitHub Actions. Tên miền phải được khai báo trong Settings → Pages.

## Chỉnh sửa

Sửa `dist/index.html`, commit và push lên `main`. Workflow sẽ tự xuất bản phiên bản mới. Có thể mở `dist/index.html` trực tiếp trong trình duyệt để xem trước.
